# Hy-Memory-30B-A3B

**What it is.** Tencent MoE model specialized in deciding what an AI agent should write to long-term memory

**Verdict: works.** Official Hy-Memory-30B-A3B Q4_K_M writes, updates, and drops memories on GPU0 at 845.99 tok/s prefill and 112.70 tok/s decode.

**Hardware:** 1x NVIDIA Tesla V100 32 GB

## Measured
| Metric | Value |
|---|---|
| prefill | 845.99 tok/s (512 prompt tokens) |
| prefill_stddev | 9.96 tok/s (2 samples) |
| decode | 112.70 tok/s (n_gen 128, n_depth 0) |
| decode_stddev | 0.53 tok/s (2 samples) |
| server_extract_prefill | 296.69 tok/s (128 prompt tokens, 0 cached) |
| server_extract_decode | 106.42 tok/s (69 generated tokens) |
| server_update_prefill | 457.86 tok/s (45 prompt tokens, 83 cached) |
| server_update_decode | 106.80 tok/s (54 generated tokens) |
| server_ignore_prefill | 398.68 tok/s (23 prompt tokens, 83 cached) |
| server_ignore_decode | 95.79 tok/s (7 generated tokens) |
| extract_wall | 1.126 s |
| update_wall | 0.613 s |
| ignore_wall | 0.140 s |
| quality | 3/3 prompts passed (extract, update, empty bank) |
| vram_peak_used | 19468 MiB |
| vram_peak_free | 13027 MiB |
| vram_idle_after | 1552 MiB (glide-decide only) |
| model_increment | 17916 MiB (19468 MiB peak minus 1552 MiB resident) |
| weight_file | 18236702464 bytes |
| gguf_model_size | 18231574016 bytes |
| parameters | 30064725888 |
| sha256 | e417fc86d0a2bb058ed253028f4617d144aa874b8af35711cca0c7009bd63446 |

## Configuration
- prefill: 845.99 tok/s (512 prompt tokens)
- decode: 112.70 tok/s (n_gen 128, n_depth 0)
- model_quant: Q4_K_M (hy_v3 30B.A3B Q4_K - Medium)
- kv_cache: q8_0, llama-bench n_depth 0; llama-server context 4096 tokens
- turboquant: no
- speculative: no
- flash_attn: flag on; runtime disabled Flash Attention over K/V rows on sm_70
- engine: llama.cpp 0.9.0-dev build 55 commit 5851a8e50, CUDA 12.9
- hardware: 1x Tesla V100-PCIE-32GB sm_70 GPU0, 32768 MiB, ngl 99, threads 32, batch 2048, ubatch 512, glide-decide co-resident 1552 MiB

## Upstream
- https://huggingface.co/tencent/Hy-Memory-30B-A3B

Upstream code and weights keep their own licence.
