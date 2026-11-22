# 
import os, sys, time
sys.path.insert(0, os.environ.get("OMLX_RES", "/Applications/oMLX.app/Contents/Resources"))
from omlx.oq import quantize_oq_streaming
src = os.environ.get("BF16_DIR", "./Qwen3.8-Flash-Next-Uncensored-bf16")
out = os.environ.get("OUT_DIR", "./Qwen3.8-Flash-Next-Uncensored-oQ2e-mtp")
last = [0]
def cb(phase, pct):
    if time.time() - last[0] > 30 or pct >= 100:
        last[0] = time.time(); print(time.strftime("%H:%M:%S"), phase, round(pct, 1), flush=True)
quantize_oq_streaming(src, out, int(os.environ.get("OQ_LEVEL", "2")),  # 2 = oQ2e (72 GB), 3 = oQ3e (86 GB)
                       progress_callback=cb, preserve_mtp=True, enhanced=True,
                      stream_calibration=True,
                      imatrix_cache_path=os.environ.get("IMATRIX", "./imatrix.npz"))
print("DONE", out, flush=True)
