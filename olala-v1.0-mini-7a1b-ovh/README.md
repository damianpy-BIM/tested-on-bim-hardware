# Olala v1.0 mini 7A1B (OVH)

**What it is.** 

**Verdict: works.** Olala v1.0 mini 7A1B Q5_K_M works on one V100 GPU0: prefill 888.487 tok/s at 512 tokens, decode 39.632 tok/s at 128 tokens (depth 0), and 3/3 short prompts answered correctly.

**Hardware:** 1x NVIDIA Tesla V100 32 GB

## Measured
| Metric | Value |
|---|---|
| prefill | 888.487 tok/s (512 tokens, 3 runs, stddev 4.390 tok/s) |
| decode | 39.632 tok/s (128 tokens, depth 0, 3 runs, stddev 0.923 tok/s) |
| prefill_samples | 883.612 tok/s, 892.128 tok/s, 889.720 tok/s |
| decode_samples | 40.563 tok/s, 38.717 tok/s, 39.615 tok/s |
| gpu0_peak | 14500 MiB |
| gpu0_baseline | 8160 MiB (unlimited-ocr already resident, 8154 MiB) |
| olala_added_at_peak_sample | 6340 MiB |
| wall_time | 41 s (05:20:13 to 05:20:54 UTC) |
| file_size | 5990551040 bytes |
| loaded_model_size | 5984548352 bytes |
| parameters | 6775272608 |
| quality | 3/3 answers correct (391; Paris; La facture est payée.) |
| cli_prompt_q1 | 391.7 tok/s |
| cli_generation_q1 | 39.5 tok/s |
| cli_prompt_q2 | 404.8 tok/s |
| cli_generation_q2 | 39.9 tok/s |
| cli_prompt_q3 | 413.2 tok/s |
| cli_generation_q3 | 38.8 tok/s |
| past_prefill_4096_2026-11-20 | 853.275 tok/s (4096 tokens, depth 0, a local path |
| past_decode_256_2026-11-20 | 41.098 tok/s (256 tokens, depth 0, same file) |
| past_prefill_4096_depth_16384_2026-11-20 | 792.226 tok/s (4096 tokens, depth 16384, same file) |
| past_decode_256_depth_16384_2026-11-20 | 40.216 tok/s (256 tokens, depth 16384, same file) |

## Configuration
- prefill: 888.487 tok/s (512 tokens)
- decode: 39.632 tok/s (128 tokens, depth 0)
- model_quant: Q5_K_M
- kv_cache: f16, 512 tokens (prefill) / 128 tokens (decode)
- turboquant: no
- speculative: no
- engine: OVHai-LLM llama.cpp fork commit 55c22dc, llama-bench, CUDA, flash attention auto
- hardware: 1x Tesla V100-PCIE-32GB sm_70 GPU0, 32494 MiB, CUDA 12.9, Xeon E5-2682 v4, 32 threads, batch 2048, ubatch 512, n_gpu_layers 99

