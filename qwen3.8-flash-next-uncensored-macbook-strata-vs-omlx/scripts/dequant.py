# Expand an MLX quantized model back to bf16, tensor by tensor, so it can be re-quantized locally (no download).
import os, json, os, shutil, sys, glob
import mlx.core as mx
src = os.environ.get("MLX_SRC", "./Qwen3.8-Flash-Next-Uncensored-Mixed-omlx")
out = os.environ.get("BF16_DIR", "./Qwen3.8-Flash-Next-Uncensored-bf16")
os.makedirs(out, exist_ok=True)
cfg = json.load(open(f"{src}/config.json"))
q = cfg.get("quantization") or cfg.get("quantization_config") or {}
dflt = {"bits": q.get("bits", 4), "group_size": q.get("group_size", 64), "mode": q.get("mode", "affine")}
def params(base):
    p = q.get(base)
    return p if isinstance(p, dict) else dflt
wmap, buf, size, n = {}, {}, 0, [0]
def flush():
    global buf, size
    if not buf: return
    n[0] += 1; name = f"model-{n[0]:05d}.safetensors"
    mx.save_safetensors(f"{out}/{name}", buf, metadata={"format": "mlx"})
    for k in buf: wmap[k] = name
    print("wrote", name, len(buf), flush=True); buf, size = {}, 0
for shard in sorted(glob.glob(f"{src}/*.safetensors")):
    t = mx.load(shard)
    for k in sorted(t):
        if k.endswith((".scales", ".biases")) and k.rsplit(".", 1)[0] + ".weight" in t: continue
        v = t[k]
        if k.endswith(".weight") and k[:-7] + ".scales" in t:
            b = k[:-7]; p = params(b)
            v = mx.dequantize(v, t[b + ".scales"], t.get(b + ".biases"), group_size=p["group_size"], bits=p["bits"], mode=p.get("mode", "affine"))
        v = v.astype(mx.bfloat16) if mx.issubdtype(v.dtype, mx.floating) else v
        mx.eval(v); buf[k] = v; size += v.nbytes
        if size > 3e9: flush()
    del t; flush()
for f in os.listdir(src):
    if os.path.isfile(f"{src}/{f}") and not f.endswith(".safetensors") and f != "model.safetensors.index.json": shutil.copy(f"{src}/{f}", out)
cfg.pop("quantization", None); cfg.pop("quantization_config", None)
for k in ("text_config", "vision_config"):
    if isinstance(cfg.get(k), dict): cfg[k].pop("quantization", None); cfg[k].pop("quantization_config", None)
json.dump(cfg, open(f"{out}/config.json", "w"), indent=2)
json.dump({"metadata": {}, "weight_map": wmap}, open(f"{out}/model.safetensors.index.json", "w"), indent=2)
print("DEQUANT DONE", len(wmap), flush=True)
