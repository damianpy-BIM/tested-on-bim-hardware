# ADCODE

**What it is.** iOS/macOS app for running local AI coding models (GLM, Qwen, etc.) without API keys

**Verdict: partly.** ADCODE 2.6.2 crashes on Ubuntu 24.04 (pty.node needs GLIBC 2.42; runs after a source rebuild) and blocks its custom-endpoint flow without an OS keyring, but Qwen3.8 27B UD-Q4_K_M itself hit 33 tok/s decode / 734 tok/s prefill on the V100 with flawless code on 3/3 prompts.

**Hardware:** CPU only, on the NVIDIA Tesla V100 server

## Measured
| Metric | Value |
|---|---|
| model_load_cold | 12 min 34 s (16.5 GB GGUF, first read) |
| vram_in_use | 16610 MiB of 32768 (GPU0 V100) |
| prefill_throughput | 733.9 tok/s (2086-token prompt); 82-120 tok/s on 29-79-token prompts |
| decode_throughput | 33.0 tok/s (500-token run, 8192 ctx) |
| prompt1_two_sum | 11.3 s wall, 329 completion tokens, correct |
| prompt2_ts_debounce | 6.5 s wall, 182 completion tokens, correct |
| prompt3_rate_limiter | 6.0 s wall, 169 completion tokens, correct |
| code_quality | 3/3 correct first try, idiomatic style |

## Configuration
- prefill tok/s (prompt length): 733.9 (2086 tokens)
- decode tok/s (context): 33.0 (8192 ctx)
- model_quant: UD-Q4_K_M GGUF (Q4_K - Medium, 16.56 GB)
- kv_cache: f16 unified, -c 8192, n_slots 4
- turboquant: no
- speculative: no
- engine: llama.cpp 0.9.0-dev build 55 (5851a8e50)
- hardware: our server GPU0, V100 32GB (sm_70), -ngl 99

