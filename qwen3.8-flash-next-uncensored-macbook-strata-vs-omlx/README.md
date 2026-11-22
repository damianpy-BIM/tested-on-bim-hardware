# Qwen3.8-Flash-Next Uncensored on one MacBook (M5 Max 128 GB): Strata vs oMLX, 512K context, built from weights already on disk

[中文说明](README.zh-CN.md)

We took an uncensored Qwen3.8-Flash-Next build we already had on disk (MLX, 4.8 bits per weight, 101 GB), and rebuilt it locally into two 2-bit models, with no new weight download:

- **oQ2e-mtp** for oMLX (72 GB, oMLX's own quantizer, calibrated, MTP kept)
- **Q2_0 GGUF** for Strata (39.8 GB + a 54.4 GB n-gram table read from SSD), written by our converter `scripts/build_strata_q2.py`

Then we measured both engines on the same Mac, one engine at a time, nothing else using the GPU.

## Results (MacBook Pro M5 Max, 40-core GPU, 128 GB, macOS 26.6.2)

Fresh prompt every run (no cache hits), 512-token replies unless noted.

| Engine, build, KV cache | Context | Prefill | Decode |
|---|---|---|---|
| Strata Q2_0, KV 8-bit K / 4-bit V | 4k | 1,868 tok/s | 63.6 tok/s |
| | 32k | 2,129 tok/s | 62.9 tok/s |
| | 128k | 1,819 tok/s | 59.3 tok/s |
| | 493k (YaRN x2) | 1,582 tok/s | 82.3 tok/s (53-token answer) |
| Strata Q2_0, KV 8-bit (int8) | 254k (native) | 1,655 tok/s | 62.8 tok/s (~400-token answer) |
| oMLX oQ2e-mtp, KV 8-bit | 4k | 2,545 tok/s | 70.8 tok/s |
| | 32k | 1,772 tok/s | 58.3 tok/s |
| | 128k | 1,941 tok/s | 46.4 tok/s |
| | 493k (YaRN x2) | 1,695 tok/s | 9.1 tok/s (53-token answer) |
| oMLX oQ2e-mtp, KV 4-bit | 4k | 2,057 tok/s | 67.2 tok/s |
| | 32k | 1,985 tok/s | 59.7 tok/s |
| | 128k | 2,002 tok/s | 51.8 tok/s |
| | 254k (native) | 1,974 tok/s | 37.3 tok/s (~400-token answer) |
| | 493k (YaRN x2) | 1,446 tok/s | 30.1 tok/s (~400-token answer) |

Config of every row: TurboQuant off; speculative decoding on (Strata: 4 drafts per step; oMLX: Lightning MTP). Model quant: Strata Q2_0 experts + 8-bit for the other projections; oMLX oQ2e (oMLX "enhanced" 2-bit, about 2.9 bpw). oMLX 0.8.2, Strata terminal 0.1.63 (Metal engine).

What we read from it:
- **Prefill is about equal**, 1,450-2,550 tok/s on both engines at every length.
- **Decode: Strata stays flat with context (about 60 tok/s from 4k to 254k); oMLX falls** (71 to 37 tok/s with 4-bit KV). A likely reason, not verified: the model's attention layers select only the top 2,048 past tokens (QSA indexer), and Strata's kernels use that selection.
- **YaRN x2 (524,288 tokens) works on both.** Needle test at 493,266 tokens, 3 facts at 10 %, 50 % and 90 % depth: **3/3 on both engines.** Same at 254,445 tokens without YaRN: 3/3 on both.

Correctness, same 11 checks on both engines (`scripts/quality.py`): 4/4 maths, Python code that runs and passes asserts, a tool call, French and Chinese answers, JSON extraction, no refusal on a borderline request. 10/11 on both; the one "miss" is our test's fault (an apples puzzle where 3.5 is a valid answer).

## Reproduce it

### What you need
- An Apple Silicon Mac with 128 GB (64 GB works for Strata with SSD streaming, not tested here).
- Source weights: [orcarouter/Qwen3.8-Flash-Next-Uncensored](https://huggingface.co/orcarouter/Qwen3.8-Flash-Next-Uncensored) (BF16, 360 GB) or any MLX quantization of it (we started from a mixed 4.8 bpw MLX build; [ddark-il/Qwen3.8-Flash-Next-Uncensored](https://huggingface.co/ddark-il/Qwen3.8-Flash-Next-Uncensored) is a public one of that kind).
- Engines: [oMLX](https://github.com/jundot/omlx) 0.8.2 and Strata Terminal 0.1.63 darwin-arm64 with its Metal engine (tarball `strata-terminal-0.1.63-darwin-arm64.tar.gz`; overview: [modelfit.io on Strata](https://modelfit.io/blog/strata-qwen38-flash-next-mac/)).
- Conversion rules follow llama.cpp's [`conversion/qwen4exp.py`](https://github.com/ggml-org/llama.cpp/blob/master/conversion/qwen4exp.py) and [`conversion/qwen.py`](https://github.com/ggml-org/llama.cpp/blob/master/conversion/qwen.py).
- A GGUF **header only** (about 11 MB, not the weights) from [SC117/Qwen3.8-Flash-Next-GSQ-RCO-abliterated-GGUF](https://huggingface.co/SC117/Qwen3.8-Flash-Next-GSQ-RCO-abliterated-GGUF): our converter copies its tensor layout and metadata keys.

### Steps
```bash
# 1. MLX -> bf16, tensor by tensor (skip if you have the BF16 original)
MLX_SRC=./Qwen3.8-Flash-Next-Uncensored-Mixed-omlx BF16_DIR=./bf16 \
  PYTHONPATH=/Applications/oMLX.app/Contents/Resources/Python/framework-mlx-base/lib/python3.11/site-packages \
  /Applications/oMLX.app/Contents/Resources/Python/cpython-3.11/bin/python3 scripts/dequant.py

# 2. oMLX oQ2e-mtp (also writes the calibration file imatrix.npz used in step 4)
BF16_DIR=./bf16 OUT_DIR=./Qwen3.8-Flash-Next-Uncensored-oQ2e-mtp IMATRIX=./imatrix.npz \
  PYTHONPATH=...same as above... python3 scripts/build_oq2e.py
#    move the output into ~/.omlx/models/, set KV 8-bit (affine8) or 4-bit (affine4) in oMLX model settings

# 3. GGUF template headers only (2 x ~11 MB, HTTP range requests)
mkdir template
curl -L -r 0-12000000 -o template/shard1.gguf https://huggingface.co/SC117/Qwen3.8-Flash-Next-GSQ-RCO-abliterated-GGUF/resolve/main/Q2_0/Qwen3.8-Flash-Next-GSQ-RCO-abliterated-Q2_0-00001-of-00002.gguf
curl -L -r 0-1000000  -o template/shard2.gguf https://huggingface.co/SC117/Qwen3.8-Flash-Next-GSQ-RCO-abliterated-GGUF/resolve/main/Q2_0/Qwen3.8-Flash-Next-GSQ-RCO-abliterated-Q2_0-00002-of-00002.gguf

# 4. Strata Q2_0 GGUF from bf16 (imatrix-weighted 2-bit scales), then the n-gram table file
BF16_DIR=./bf16 IMATRIX=./imatrix.npz Q2_WORKERS=3 python3 scripts/build_strata_q2.py --out ./out-gguf

# expert-profile.bin: copy data/expert-profile.bin from the Strata terminal folder next to the configs
# 5. Strata pack + serve (one heavy model job at a time on the Mac: stop oMLX first)
cd <strata terminal dir>/tools && ../python/bin/python3 iq_pack.py --gguf ./out-gguf/Qwen3.8-Flash-Next-Uncensored-Q2_0-00001-of-00002.gguf --out ./pack
strata serve --profile configs/strata-262k.json --port 8301        # or configs/strata-512k-yarn.json
```
For oMLX at 512K, use `configs/omlx-oq2e-config-yarn512k.json` as the model's `config.json` (YaRN factor 2, original 262,144).

### Measure
```bash
python3 scripts/strata_one.py 131072 512 seed1          # Strata, 128k prompt, 512-token reply
python3 scripts/omlx_one.py   131072 512 seed1          # oMLX (set your oMLX API key inside)
python3 scripts/needle.py http://127.0.0.1:8301/v1/chat/completions <model id> 470000   # ~493k-token needle test
python3 scripts/quality.py http://127.0.0.1:8301/v1/chat/completions <model id>         # 11 correctness checks
```

### Traps we hit
- Run **one heavy model job at a time**: oMLX holding the model plus the converter (or Strata) at once crashed our Mac out of memory.
- oMLX refuses long prompts when its memory ceiling is too tight: with an 80 GB model, set the ceiling to about 108 GB and the hot cache to 2 GB for 128k+.
- Strata's Metal engine: `--kv int8` failed at start for us once (`kv_block_bytes has no Metal implementation yet`) and worked in a later start; `k8v4` (8-bit K, 4-bit V) always started.
- Short replies inflate decode figures with speculative decoding: measure with a few hundred tokens.

No weights are shipped here. Code: MIT. Measured on hardware by BIM Computing — https://www.bim-computing.com
