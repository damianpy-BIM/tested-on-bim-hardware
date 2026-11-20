#!/usr/bin/env python3
"""FastFrames-L on Apple Silicon MPS, v2 (20/11/2026).

v1 (19/11) kept umT5-XXL (11.4 GB) + fused-QKV fast_ops copies (+5.6 GiB) + the 26.8 GB
KV cache all resident at once (~74 GiB) while oMLX VL serving held ~91 GB: the run thrashed
into swap (pass cost 13.7 s -> 45 s and rising) and died at pass 31/45 without a clip.

v2 changes, same FF_L stock recipe (BF16, fast_ops) otherwise:
  * encode ALL prompts first, then evict umT5-XXL from MPS (del + gc + empty_cache): -11.4 GB
    before the KV cache is touched;
  * every DiT pass logs wall t, driver-allocated GiB and used swap GB, so a thrash shows up
    in the log immediately instead of 20 minutes later;
  * measured_mac json written after each prompt (a mid-run death keeps its data);
  * MACRUN_DONE / MACRUN_FAIL sentinel lines for the watchers.
Run with oMLX stopped (omlx-powerguard off) — that is the memory this job needs.
"""
import argparse
import dataclasses
import gc
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

os.environ.setdefault("PYTORCH_MPS_HIGH_WATERMARK_RATIO", "0.0")
sys.path.insert(0, str(Path(__file__).resolve().parent / "repo"))

import numpy as np  # noqa: E402
import torch  # noqa: E402
import torch.nn.functional as F  # noqa: E402

import fastframes.models.kv_refinement as kvref_mod  # noqa: E402
import fastframes.pipeline as ffp  # noqa: E402
import fastframes.wan.attention as attn_mod  # noqa: E402
import fastframes.wan.causal_model as causal_mod  # noqa: E402
import fastframes.wan.model as wan_model_mod  # noqa: E402
from fastframes.models.pixel_decoder import align_frames  # noqa: E402
from fastframes.pipeline import FF_L, MODELS, FastFrames, to_uint8  # noqa: E402
from fastframes.wan.causal_model import FastOps  # noqa: E402
from fastframes.wan.scheduler import FlowMatchScheduler  # noqa: E402

DEV = torch.device("mps")
BF16 = torch.bfloat16


def log(msg):
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)


def sync():
    torch.mps.synchronize()


def swap_gb():
    try:
        s = subprocess.run(["/usr/sbin/sysctl", "-n", "vm.swapusage"],
                           capture_output=True, text=True).stdout
        m = re.search(r"used = ([0-9.]+)M", s)
        return float(m.group(1)) / 1024.0 if m else -1.0
    except Exception:
        return -1.0


# ------------------------------------------------------------- attention (no cuDNN on MPS)
def attention_impl(q, k, v, causal=False, dropout_p=0.0, backend="cudnn"):
    out_dtype = q.dtype
    q, k, v = (t.transpose(1, 2).to(BF16) for t in (q, k, v))
    out = F.scaled_dot_product_attention(q, k, v, is_causal=causal, dropout_p=dropout_p)
    return out.transpose(1, 2).contiguous().to(out_dtype)


for _mod in (attn_mod, causal_mod, wan_model_mod):
    _mod.attention = attention_impl
attn_mod.cross_attention = lambda q, k, v: attention_impl(q, k, v)
wan_model_mod.cross_attention = attn_mod.cross_attention
kvref_mod._sdpa = lambda q, k, v: F.scaled_dot_product_attention(q, k, v)


# ------------------------------------------------- float64 math on the CPU (MPS has none)
def _cpu64(fn):
    def wrapped(dim, position):
        return fn(dim, position.detach().cpu()).float().to(position.device)
    return wrapped


causal_mod.sinusoidal_embedding_1d = _cpu64(wan_model_mod.sinusoidal_embedding_1d)
wan_model_mod.sinusoidal_embedding_1d = _cpu64(wan_model_mod.sinusoidal_embedding_1d)
kvref_mod.sinusoidal_embedding_1d = _cpu64(kvref_mod.sinusoidal_embedding_1d)


def _flow_to_x0(self, flow, xt, timestep):
    dev, dtype = flow.device, flow.dtype
    flow, xt, sigmas, timesteps = (x.detach().cpu().double()
                                   for x in (flow, xt, self.sigmas, self.timesteps))
    sigma = sigmas[self._index(timestep.detach().cpu().double(), timesteps)].reshape(-1, 1, 1, 1)
    return (xt - sigma * flow).to(dtype).to(dev)


FlowMatchScheduler.flow_to_x0 = _flow_to_x0


def build_fast_ops(model, height, width, num_frames):
    """Stock FastOps, with the complex128 RoPE tables built on the CPU then moved as FP32."""
    fo = FastOps.__new__(FastOps)
    patch = model.patch_embedding
    fo.patch_weight = patch.weight.detach().reshape(model.dim, -1)
    fo.patch_bias = patch.bias
    fo.qkv = []
    for block in model.blocks:
        sa = block.self_attn
        fo.qkv.append((torch.cat([sa.q.weight, sa.k.weight, sa.v.weight], 0).detach().contiguous(),
                       torch.cat([sa.q.bias, sa.k.bias, sa.v.bias], 0).detach().contiguous()))
    h, w = height // model.patch_size[1], width // model.patch_size[2]
    half = model.dim // model.num_heads // 2
    freqs = model.freqs.cpu()
    temporal, vertical, horizontal = freqs.split([half - 2 * (half // 3), half // 3, half // 3], dim=1)
    fo.rope = [
        torch.view_as_real(torch.cat((
            temporal[f:f + 1].view(1, 1, 1, -1).expand(1, h, w, -1),
            vertical[:h].view(1, h, 1, -1).expand(1, h, w, -1),
            horizontal[:w].view(1, 1, w, -1).expand(1, h, w, -1),
        ), dim=-1).reshape(h * w, 1, half)).float().contiguous().to(patch.weight.device)
        for f in range(num_frames)]
    # fast path never reads freqs; a same-device dummy stops forward_frame moving complex128 to MPS
    model.freqs = torch.zeros(1, device=patch.weight.device)
    return fo


class MacFastFrames(FastFrames):
    def __init__(self, config, dit, refiner, decoder, text_encoder=None):
        super().__init__(dataclasses.replace(config, fast_ops=False), dit, refiner, decoder, text_encoder)
        self.config = config
        height, width = config.latent_size
        self.fast = build_fast_ops(dit, height, width, config.num_frames) if config.fast_ops else None

    def autocast(self):
        return torch.autocast("mps", dtype=BF16, cache_enabled=False)

    def _predict(self, *args, **kwargs):
        self._step = getattr(self, "_step", 0) + 1
        out = super()._predict(*args, **kwargs)
        mem = torch.mps.driver_allocated_memory() / 2**30
        self._peak = max(getattr(self, "_peak", 0), mem)
        log(f"  DiT pass {self._step}/45  t={time.time() - self._t0:.0f}s  mem={mem:.1f} GiB  swap={swap_gb():.1f} GB")
        return out

    @torch.inference_mode()
    def decode(self, features, modulation):
        height, width = self.config.latent_size
        grid = torch.tensor([[modulation.shape[1], height // 2, width // 2]], device=self.device, dtype=torch.long)
        with torch.autocast("mps", dtype=BF16):
            pixels = self.decoder(features, modulation, grid)
        return align_frames(pixels, self.config.num_pixel_frames)


def save_mp4(path, frames, fps=16):
    import imageio.v2 as imageio
    with imageio.get_writer(path, fps=fps, codec="libx264", quality=8, pixelformat="yuv420p",
                            macro_block_size=16) as wr:
        for fr in frames:
            wr.append_data(fr)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", type=Path, required=True)
    ap.add_argument("--prompt", action="append", required=True)
    ap.add_argument("--seed", action="append", type=int, default=[])
    ap.add_argument("--out", action="append", default=[])
    ap.add_argument("--measure", type=Path, default=Path(__file__).resolve().parent / "measured_mac2.json")
    args = ap.parse_args()
    n = len(args.prompt)
    seeds, outs = (args.seed * n)[:n], (args.out * n)[:n]

    spec = MODELS["ff-l"]
    ffp.configure_backends(spec.config)
    log(f"torch {torch.__version__}, MPS {torch.backends.mps.is_available()}, FF_L stock BF16 + fast_ops, umT5 evicted before rollout")
    t0 = time.time()
    root = args.root
    model = MacFastFrames.from_pretrained(spec.config, root / spec.wan_dir, root / spec.dit,
                                          root / spec.refiner, root / spec.decoder, device=DEV)
    sync()
    load_s = time.time() - t0
    log(f"model loaded in {load_s:.1f} s, driver memory {torch.mps.driver_allocated_memory() / 2**30:.1f} GiB, swap {swap_gb():.1f} GB")

    # ---- 1) encode every prompt with umT5 resident, then EVICT it before the KV cache grows
    embeds = []
    for i, prompt in enumerate(args.prompt):
        t = time.time()
        e = model.encode_prompt(prompt)
        sync()
        embeds.append(e)
        log(f"text encode {i + 1}/{n}: {time.time() - t:.1f} s")
    model.text_encoder = None
    del spec
    gc.collect()
    sync()
    torch.mps.empty_cache()
    sync()
    gc.collect()
    log(f"umT5-XXL evicted: driver memory now {torch.mps.driver_allocated_memory() / 2**30:.1f} GiB, swap {swap_gb():.1f} GB")

    results = []

    def write_measured():
        args.measure.write_text(json.dumps({
            "device": "Apple M5 Max 128 GB (MPS), oMLX serving stopped for the run",
            "torch": torch.__version__, "dtype": "bfloat16", "fast_ops": True,
            "umT5": "evicted from MPS before rollout (encoded first)",
            "load_s": load_s, "runs": results}, indent=2))

    # ---- 2) rollouts
    for i, (prompt, seed, out) in enumerate(zip(args.prompt, seeds, outs)):
        log(f"=== prompt {i + 1}/{n}: {prompt!r} seed={seed} ===")
        st = {}
        model._step, model._peak, model._t0 = 0, 0.0, time.time()
        t = time.time(); _, features, modulation = model.rollout(embeds[i], seed); sync()
        st["rollout_s"] = time.time() - t
        st["dit_steps"] = len(FF_L.first_frame_timesteps) + 1 + (FF_L.num_frames - 1) * len(FF_L.timesteps)
        st["ms_per_dit_step"] = st["rollout_s"] * 1000 / st["dit_steps"]
        t = time.time(); pixels = model.decode(features, modulation); frames = to_uint8(pixels[0]).cpu().numpy(); sync()
        st["decode_s"] = time.time() - t
        t = time.time(); Path(out).parent.mkdir(parents=True, exist_ok=True); save_mp4(out, frames); st["save_s"] = time.time() - t
        st["peak_mps_driver_gib"] = round(model._peak, 2)
        st["peak_swap_gb"] = round(swap_gb(), 1)
        st["video"] = {"frames": int(frames.shape[0]), "size": f"{frames.shape[2]}x{frames.shape[1]}", "fps": 16,
                       "seconds": frames.shape[0] / 16}
        st.update(prompt=prompt, seed=seed, out=str(out))
        results.append(st)
        log(json.dumps(st))
        write_measured()
        log(f"CLIP_DONE {out}")
        del features, modulation, pixels, frames
        torch.mps.empty_cache()

    write_measured()
    log("MACRUN_DONE")


if __name__ == "__main__":
    try:
        main()
    except BaseException:
        import traceback
        traceback.print_exc()
        print("MACRUN_FAIL", flush=True)
        sys.exit(1)
