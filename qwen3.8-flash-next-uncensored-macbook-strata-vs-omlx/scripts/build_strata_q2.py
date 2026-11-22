#!/usr/bin/env python3
"""Our orcarouter Qwen3.8-Flash-Next-Uncensored weights (bf16 copy expanded from the on-disk 4.8 bpw build)
-> Strata GGUF in the same layout as the 3080's GSQ-RCO Q2_0 (template header only, its weights unused).


Transforms = llama.cpp conversion/qwen.py + qwen4exp.py (Qwen3Next / V-reorder / Qwen4Exp classes).
Types: experts (and every tensor the template stores Q2_0) -> Q2_0 with imatrix-weighted scale search;
template F32/F16/BF16/Q8_0 kept; template K/IQ types -> Q8_0; PLE table -> Q8_0 (separate file, mmap'd by Strata).
Usage: build_strata_q2.py [--layers 0,1,3] [--out DIR]   (--layers = test run on a subset)
"""
import os, argparse, json, os, struct, sys, time
import numpy as np

SRC = os.environ.get("BF16_DIR", "./Qwen3.8-Flash-Next-Uncensored-bf16")
TPL = os.environ.get("TEMPLATE_GGUF1", "./template/shard1.gguf")
TPL2 = os.environ.get("TEMPLATE_GGUF2", "./template/shard2.gguf")
IMX = os.environ.get("IMATRIX", "./imatrix.npz")
F32, F16, Q8_0, BF16, Q2_0 = 0, 1, 8, 30, 42
BLK = {F32: (1, 4), F16: (1, 2), BF16: (1, 2), Q8_0: (32, 34), Q2_0: (64, 18)}

# ---------------------------------------------------------------- GGUF header (raw KV bytes kept verbatim)
def read_header(path):
    f = open(path, "rb")
    def u(fmt): return struct.unpack("<" + fmt, f.read(struct.calcsize("<" + fmt)))[0]
    SZ = {0: 1, 1: 1, 2: 2, 3: 2, 4: 4, 5: 4, 6: 4, 7: 1, 10: 8, 11: 8, 12: 8}
    def skip(t):
        if t == 8: f.seek(u("Q"), 1)
        elif t == 9:
            et = u("I"); n = u("Q")
            if et in SZ: f.seek(SZ[et] * n, 1)
            else:
                for _ in range(n): skip(et)
        else: f.seek(SZ[t], 1)
    assert f.read(4) == b"GGUF"; u("I"); nt = u("Q"); nkv = u("Q")
    kvs = []
    for _ in range(nkv):
        start = f.tell(); kl = u("Q"); key = f.read(kl).decode(); t = u("I")
        vstart = f.tell(); skip(t); end = f.tell()
        f.seek(start); raw = f.read(end - start); kvs.append((key, t, raw, vstart - start))
    tens = []
    for _ in range(nt):
        n = f.read(u("Q")).decode(); nd = u("I"); dims = [u("Q") for _ in range(nd)]; ty = u("I"); off = u("Q")
        tens.append((n, dims, ty, off))
    return kvs, tens

def kv_bytes(key, t, payload):
    k = key.encode(); return struct.pack("<Q", len(k)) + k + struct.pack("<I", t) + payload

def kv_str(key, s): b = s.encode(); return kv_bytes(key, 8, struct.pack("<Q", len(b)) + b)
def kv_u16(key, v): return kv_bytes(key, 2, struct.pack("<H", v))
def kv_i32(key, v): return kv_bytes(key, 5, struct.pack("<i", v))
def kv_u32(key, v): return kv_bytes(key, 4, struct.pack("<I", v))

# ---------------------------------------------------------------- source tensors (bf16 safetensors, memmap)
class Src:
    def __init__(self, d):
        self.d = d; self.idx = json.load(open(f"{d}/model.safetensors.index.json"))["weight_map"]; self.hdr = {}
    def meta(self, k):
        fn = self.idx[k]
        if fn not in self.hdr:
            h = open(f"{self.d}/{fn}", "rb"); n = struct.unpack("<Q", h.read(8))[0]; self.hdr[fn] = (8 + n, json.loads(h.read(n)))
        base, hd = self.hdr[fn]; return fn, base, hd[k]
    def get(self, k):
        fn, base, m = self.meta(k); a, b = m["data_offsets"]
        mm = np.memmap(f"{self.d}/{fn}", mode="r", offset=base + a, shape=(b - a,), dtype=np.uint8)
        if m["dtype"] == "BF16":
            x = (mm.view(np.uint16).astype(np.uint32) << 16).view(np.float32)
        elif m["dtype"] == "I64": x = mm.view(np.int64)
        else: x = mm.view({"F32": np.float32, "F16": np.float16}[m["dtype"]]).astype(np.float32)
        return x.reshape(m["shape"])
    def has(self, k): return k in self.idx

# ---------------------------------------------------------------- quantizers (vectorised; layouts = ggml)
def q8_0(x):
    b = x.reshape(-1, 32).astype(np.float32)
    amax = np.abs(b).max(1); d = amax / 127.0; inv = np.where(d > 0, 1.0 / np.where(d > 0, d, 1), 0)
    q = np.clip(np.rint(b * inv[:, None]), -127, 127).astype(np.int8)
    out = np.empty((b.shape[0], 34), np.uint8)
    out[:, :2] = d.astype(np.float16).view(np.uint8).reshape(-1, 2); out[:, 2:] = q.view(np.uint8)
    return out.tobytes()

FACT = np.linspace(0.70, 1.45, 16, dtype=np.float32)
def q2_0(x, imp=None):
    """Q2_0 block = fp16 d + 16 bytes of 2-bit codes, value = (code-1)*d, code in 0..3 (levels -1,0,1,2).
    d may be negative, so the +2 level goes on whichever side has the largest magnitude. d is chosen per
    block by an importance-weighted MSE search (imatrix in_sum2 per input column); Strata's reference uses d=amax."""
    rows = x.reshape(-1, x.shape[-1]); C = rows.shape[1]; assert C % 64 == 0
    b = rows.reshape(-1, 64).astype(np.float32)                       # blocks along the innermost axis
    w = np.ones_like(b) if imp is None else np.broadcast_to(imp.reshape(-1, C), rows.shape).reshape(-1, 64)
    i = np.abs(b).argmax(1); m = b[np.arange(b.shape[0]), i]          # signed extreme
    best_err = np.full(b.shape[0], np.inf, np.float32); best_d = np.zeros(b.shape[0], np.float32)
    best_q = np.zeros(b.shape, np.uint8)
    cands = [m[:, None] / 2 * FACT[None, :], np.abs(m)[:, None]]      # search around m/2, plus Strata's d=amax
    for cand in (c for c in np.concatenate(cands, 1).T):
        d = cand.astype(np.float16).astype(np.float32); dd = np.where(d == 0, 1, d)
        q = np.clip(np.rint(b / dd[:, None]) + 1, 0, 3)
        e = ((b - (q - 1) * d[:, None]) ** 2 * w).sum(1)
        better = e < best_err
        best_err[better] = e[better]; best_d[better] = d[better]; best_q[better] = q[better].astype(np.uint8)
    qq = best_q.reshape(-1, 16, 4)
    packed = (qq[..., 0] | (qq[..., 1] << 2) | (qq[..., 2] << 4) | (qq[..., 3] << 6)).astype(np.uint8)
    out = np.empty((b.shape[0], 18), np.uint8)
    out[:, :2] = best_d.astype(np.float16).view(np.uint8).reshape(-1, 2); out[:, 2:] = packed
    return out.tobytes()

def encode(x, ty, imp=None):
    if ty == F32: return x.astype(np.float32).tobytes()
    if ty == F16: return x.astype(np.float16).tobytes()
    if ty == BF16: return (x.astype(np.float32).view(np.uint32) >> 16).astype(np.uint16).tobytes()  # truncation; source is bf16 already
    if ty == Q8_0: return q8_0(x)
    if ty == Q2_0: return q2_0(x, imp)
    raise ValueError(ty)

def nbytes(dims, ty):
    n = int(np.prod(dims)); e, b = BLK[ty]; assert n % e == 0, (dims, ty); return n // e * b

# ---------------------------------------------------------------- name map + llama.cpp transforms
def reorder_v(t, dim, nk, vpk, hd):
    sh = list(t.shape); dim %= len(sh)
    t = t.reshape(sh[:dim] + [nk, vpk, hd] + sh[dim + 1:])
    perm = list(range(t.ndim)); perm[dim], perm[dim + 1] = perm[dim + 1], perm[dim]
    return np.ascontiguousarray(t.transpose(perm)).reshape(sh)

def build_plan(cfg, tpl_tensors, layers):
    tc = cfg.get("text_config", cfg)
    nk, nv = tc["linear_num_key_heads"], tc["linear_num_value_heads"]; kd, vd = tc["linear_key_head_dim"], tc["linear_value_head_dim"]
    vpk = nv // nk; nq_idx = tc["indexer_n_heads"] * tc["indexer_head_dim"]
    P = "language_model.model."; plan = {}   # gguf name -> (fn producing float32 array in numpy order, imatrix key or None)
    def add(g, fn, imk=None): plan[g] = (fn, imk)
    def raw(k): return lambda: S.get(k)
    def plus1(k): return lambda: S.get(k) + 1
    add("token_embd.weight", raw(P + "embed_tokens.weight"))
    add("output.weight", raw("language_model.lm_head.weight"), "language_model.lm_head")
    add("output_hc_down.weight", raw(P + "hyper_connection_mixer.input_mix_weight_down.weight"))
    add("output_hc_up.weight", raw(P + "hyper_connection_mixer.input_mix_weight_up.weight"))
    add("output_hc_norm.weight", plus1(P + "hyper_connection_mixer.hc_norm.weight"))
    for L in layers:
        p = f"{P}layers.{L}."; g = f"blk.{L}."
        for part, short in (("attn_hyper_connection", "attn"), ("mlp_hyper_connection", "ffn")):
            add(g + f"hc_{short}_down.weight", raw(p + f"{part}.input_mix_weight_down.weight"), p + f"{part}.input_mix_weight_down")
            add(g + f"hc_{short}_up.weight", raw(p + f"{part}.input_mix_weight_up.weight"), p + f"{part}.input_mix_weight_up")
            add(g + f"hc_{short}_inject.weight", raw(p + f"{part}.block_inject_weight.weight"))
            add(g + f"hc_{short}_norm.weight", plus1(p + f"{part}.hc_norm.weight"))
        if S.has(p + "linear_attn.in_proj_qkv.weight"):
            la = p + "linear_attn."
            def qkv(la=la):
                t = S.get(la + "in_proj_qkv.weight"); q = kd * nk
                return np.concatenate([t[:q], t[q:2 * q], reorder_v(t[2 * q:], 0, nk, vpk, vd)], 0)
            add(g + "attn_qkv.weight", qkv, la + "in_proj_qkv")
            add(g + "attn_gate.weight", lambda la=la: reorder_v(S.get(la + "in_proj_z.weight"), 0, nk, vpk, vd), la + "in_proj_z")
            add(g + "ssm_alpha.weight", lambda la=la: reorder_v(S.get(la + "in_proj_a.weight"), 0, nk, vpk, 1), la + "in_proj_a")
            add(g + "ssm_beta.weight", lambda la=la: reorder_v(S.get(la + "in_proj_b.weight"), 0, nk, vpk, 1), la + "in_proj_b")
            add(g + "ssm_a", lambda la=la: -np.exp(reorder_v(S.get(la + "A_log")[:, None], 0, nk, vpk, 1)[:, 0]))
            add(g + "ssm_dt.bias", lambda la=la: reorder_v(S.get(la + "dt_bias")[:, None], 0, nk, vpk, 1)[:, 0])
            def conv(la=la):
                d = S.get(la + "conv1d.weight").reshape(nk * kd * 2 + nv * vd, -1); qk = kd * nk * 2
                return np.concatenate([d[:qk], reorder_v(d[qk:], 0, nk, vpk, vd)], 0)
            add(g + "ssm_conv1d.weight", conv)
            add(g + "ssm_norm.weight", raw(la + "norm.weight"))                       # linear_attn.norm: no +1
            add(g + "ssm_out.weight", lambda la=la: reorder_v(S.get(la + "out_proj.weight"), 1, nk, vpk, vd), la + "out_proj")
        else:
            sa = p + "self_attn."
            add(g + "attn_q.weight", raw(sa + "q_proj.weight"), sa + "q_proj")
            add(g + "attn_k.weight", raw(sa + "k_proj.weight"), sa + "k_proj")
            add(g + "attn_v.weight", raw(sa + "v_proj.weight"), sa + "v_proj")
            add(g + "attn_output.weight", raw(sa + "o_proj.weight"), sa + "o_proj")
            add(g + "attn_q_norm.weight", plus1(sa + "q_norm.weight"))
            add(g + "attn_k_norm.weight", plus1(sa + "k_norm.weight"))
            add(g + "indexer.q_proj.weight", lambda sa=sa: S.get(sa + "indexer.index_qk_proj.weight")[:nq_idx], sa + "indexer.index_qk_proj")
            add(g + "indexer.k_proj.weight", lambda sa=sa: S.get(sa + "indexer.index_qk_proj.weight")[nq_idx:], sa + "indexer.index_qk_proj")
            add(g + "indexer.q_norm.weight", plus1(sa + "indexer.q_layernorm.weight"))
            add(g + "indexer.k_norm.weight", plus1(sa + "indexer.k_layernorm.weight"))
        m = p + "mlp."
        add(g + "ffn_gate_inp.weight", raw(m + "gate.weight"), m + "gate")
        add(g + "ffn_gate_inp_shexp.weight", lambda m=m: S.get(m + "shared_expert_gate.weight").reshape(-1), m + "shared_expert_gate")
        for a, b in (("gate", "gate_proj"), ("up", "up_proj"), ("down", "down_proj")):
            add(g + f"ffn_{a}_shexp.weight", raw(m + f"shared_expert.{b}.weight"), m + f"shared_expert.{b}")
            add(g + f"ffn_{a}_exps.weight", raw(m + f"switch_mlp.{b}.weight"), m + f"switch_mlp.{b}")
        if S.has(p + "ple.key_proj.weight"):
            q = p + "ple."
            add(g + "ple_conv1d.weight", lambda q=q: S.get(q + "conv1d.weight").reshape(S.get(q + "conv1d.weight").shape[0], -1))
            add(g + "ple_key.weight", raw(q + "key_proj.weight"), q + "key_proj")
            add(g + "ple_value.weight", raw(q + "value_proj.weight"), q + "value_proj")
            for n in ("conv", "key", "query"): add(g + f"ple_norm_{n}.weight", plus1(q + f"norm_{n}.weight"))
    return plan

def tensor_type(tpl_ty, gname):
    if tpl_ty in (F32, F16, BF16, Q8_0, Q2_0): return tpl_ty
    return Q8_0                                                                         # K / IQ types: no quantizer here

def imatrix_for(Z, key, shape):
    if key is None or (key + ".in_sum2") not in Z: return None
    s = Z[key + ".in_sum2"].astype(np.float32); c = Z[key + ".counts"].astype(np.float32)
    v = s / np.maximum(c.reshape(-1, *([1] * (s.ndim - 1))), 1)
    if v.ndim == 2:                                                                     # per expert: [E, in] -> rows [E*out, in]
        E, C = v.shape; rows = int(np.prod(shape[:-1])) // E
        return np.repeat(v, rows, axis=0)
    return v                                                                            # [in], broadcast over rows

def write_gguf(path, kv_list, tensors, produce):
    """tensors: [(name, numpy_shape, ty)], produce(name) -> bytes. Header first, then aligned data."""
    align = 32; offs = []; o = 0
    for n, sh, ty in tensors:
        o = (o + align - 1) // align * align; offs.append(o); o += nbytes(sh, ty)
    with open(path, "wb") as f:
        f.write(b"GGUF" + struct.pack("<IQQ", 3, len(tensors), len(kv_list)))
        for kv in kv_list: f.write(kv)
        for (n, sh, ty), off in zip(tensors, offs):
            nb = n.encode(); dims = list(reversed(sh))
            f.write(struct.pack("<Q", len(nb)) + nb + struct.pack("<I", len(dims)) + struct.pack(f"<{len(dims)}Q", *dims) + struct.pack("<IQ", ty, off))
        base = (f.tell() + align - 1) // align * align; f.write(b"\0" * (base - f.tell()))
        t0 = time.time()
        import multiprocessing as mp
        W = int(os.environ.get("Q2_WORKERS", "3"))
        pool = mp.get_context("fork").Pool(W, maxtasksperchild=8) if W > 1 else None
        gen = pool.imap(produce, [t[0] for t in tensors]) if pool else map(produce, [t[0] for t in tensors])
        for i, ((n, sh, ty), off) in enumerate(zip(tensors, offs)):
            f.write(b"\0" * (base + off - f.tell())); data = next(gen)
            if isinstance(data, (bytes, bytearray)): data = [data]
            tot = 0
            for chunk in data: f.write(chunk); tot += len(chunk)                     # a generator streams (PLE table: 54 GB)
            assert tot == nbytes(sh, ty), (n, tot, nbytes(sh, ty))
            print(f"{time.strftime('%H:%M:%S')} [{i+1}/{len(tensors)}] {n} {sh} type{ty} {tot/1e6:.1f}MB ({time.time()-t0:.0f}s)", flush=True)

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--layers"); ap.add_argument("--out", default="./out-gguf")
    ap.add_argument("--skip-ple", action="store_true"); ap.add_argument("--ple-only", action="store_true"); a = ap.parse_args()
    global S; S = Src(SRC); cfg = json.load(open(f"{SRC}/config.json")); Z = np.load(IMX)
    kvs, tpl = read_header(TPL); tpl_ty = {n: ty for n, d, ty, o in tpl}; tpl_shape = {n: list(reversed(d)) for n, d, ty, o in tpl}
    nl = cfg.get("text_config", cfg)["num_hidden_layers"]
    layers = [int(x) for x in a.layers.split(",")] if a.layers else list(range(nl))
    plan = build_plan(cfg, tpl, layers)
    names = [n for n, d, ty, o in tpl if n in plan]                                    # template order
    missing = [n for n, d, ty, o in tpl if n not in plan and (a.layers is None or not n.startswith("blk.") or int(n.split(".")[1]) in layers)]
    if missing: sys.exit(f"no source for template tensors: {missing[:10]} ... ({len(missing)})")
    tensors = [(n, tpl_shape[n], tensor_type(tpl_ty[n], n)) for n in names]
    drop = ("quantize.", "split.", "general.name", "general.file_type", "general.quantized_by", "general.description", "general.tags", "general.repo_url")
    kv_list = [raw for key, t, raw, _ in kvs if not key.startswith(drop)]
    kv_list += [kv_str("general.name", "Qwen3.8-Flash-Next-Uncensored Q2_0 (local build from orcarouter weights)"),
                kv_u16("split.no", 0), kv_u16("split.count", 2), kv_i32("split.tensors.count", len(tensors) + 1)]
    os.makedirs(a.out, exist_ok=True)
    global produce
    def produce(n):
        fn, imk = plan[n]; x = np.asarray(fn(), dtype=np.float32)
        assert list(x.shape) == tpl_shape[n] or x.size == int(np.prod(tpl_shape[n])), (n, x.shape, tpl_shape[n])
        x = x.reshape(tpl_shape[n]); ty = dict((t[0], t[2]) for t in tensors)[n]
        imp = imatrix_for(Z, imk, x.shape) if ty == Q2_0 else None
        if ty == Q2_0 and x.ndim == 3 and imp is not None:                              # experts: chunk to bound memory
            E = x.shape[0]; per = imp.shape[0] // E; out = []
            for e0 in range(0, E, 16):
                out.append(q2_0(x[e0:e0 + 16], imp[e0 * per:(e0 + 16) * per]))
            return b"".join(out)
        if ty == Q2_0 and x.ndim == 3:
            return b"".join(q2_0(x[e0:e0 + 16]) for e0 in range(0, x.shape[0], 16))
        return encode(x, ty, imp)
    if not a.ple_only:
        write_gguf(f"{a.out}/Qwen3.8-Flash-Next-Uncensored-Q2_0-00001-of-00002.gguf", kv_list, tensors, produce)
    if a.skip_ple: return
    # shard 2: the PLE n-gram table (row-concat of the 128 shards), Q8_0, read through mmap by Strata
    kv2, tpl2 = read_header(TPL2); pname = tpl2[0][0]; pshape = list(reversed(tpl2[0][1]))
    P = "language_model.model.layers."; ple = [k for k in S.idx if ".ngram_embedding.shards." in k]
    ple.sort(key=lambda k: int(k.split(".shards.")[1].split(".")[0]))
    kvl2 = [raw for key, t, raw, _ in kv2 if not key.startswith(drop)] + [kv_u16("split.no", 1), kv_u16("split.count", 2), kv_i32("split.tensors.count", len(tensors) + 1)]
    os.environ["Q2_WORKERS"] = "1"                                                     # one tensor: no pool (a lambda cannot be pickled)
    write_gguf(f"{a.out}/Qwen3.8-Flash-Next-Uncensored-Q2_0-00002-of-00002.gguf", kvl2, [(pname, pshape, Q8_0)],
               lambda n: (q8_0(S.get(k)) for k in ple))

if __name__ == "__main__":
    main()
