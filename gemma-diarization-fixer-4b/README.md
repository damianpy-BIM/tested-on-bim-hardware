# Gemma Diarization Fixer 4B

**What it is.** 4B Gemma model fine-tuned to post-process ASR output and fix speaker diarization labels

**Verdict: works.** Q4_K_M GGUF on GPU0 corrected both mislabeled transcripts and left the correct one unchanged (decode 100.86-104.70 tok/s).

**Hardware:** 1x NVIDIA Tesla V100 32 GB

## Measured
| Metric | Value |
|---|---|
| prefill prompt 1 | 224.46 tok/s (54 tokens) |
| decode prompt 1 | 100.86 tok/s (46 tokens) |
| llama.cpp total time prompt 1 | 746.63 ms |
| wall time prompt 1 | 3.35 s |
| prefill prompt 2 | 259.84 tok/s (53 tokens) |
| decode prompt 2 | 102.87 tok/s (50 tokens) |
| llama.cpp total time prompt 2 | 733.56 ms |
| wall time prompt 2 | 3.51 s |
| prefill prompt 3 | 348.00 tok/s (73 tokens) |
| decode prompt 3 | 104.70 tok/s (65 tokens) |
| llama.cpp total time prompt 3 | 887.20 ms |
| wall time prompt 3 | 3.77 s |
| GPU0 peak memory | 5284 MiB |
| GPU0 baseline memory | 1318 MiB |
| weight file size | 5300582656 bytes |
| corrections | 2 of 2 mislabeled prompts retagged, words unchanged |
| preservation | 1 of 1 already-correct prompt unchanged |

## Configuration
- prefill: 224.46 tok/s (54 tokens, prompt 1)
- decode: 100.86 tok/s (46 tokens, n_ctx 4096)
- model_quant: Q4_K_M
- kv_cache: f16, 4096 tokens (V padded to 1024 because flash attention is off)
- turboquant: no
- speculative: no
- engine: llama.cpp 0.9.0-dev build 55 commit 5851a8e50 llama-completion, CUDA arch 700, -ngl 99 -t 8 -b 2048 -ub 512 -fa off --temp 0
- hardware: Tesla V100-PCIE-32GB GPU0, sm_70, 32768 MiB

## Upstream
- https://huggingface.co/google

Upstream code and weights keep their own licence.
