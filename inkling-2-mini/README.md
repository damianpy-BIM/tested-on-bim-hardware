# Inkling 2 Mini

**What it is.** 

**Verdict: works.** Works on 1x Tesla V100 GPU0 as Unsloth Mainline UD-Q4_K_M: llama-bench prefill 558.55 tok/s at 4096 tokens, decode 29.43 tok/s at depth 4096 (n_gen 128, q8_0 KV), 3/3 coding prompts matched expected stdout. Decode is in the same band as the 2026-11-20 Qwen3.8-27B Q4_K_M llama-server record (31.98 tok/s after 3749 tokens); prefill is slower than that record (745.69 tok/s at 3749 tokens).

**Hardware:** 1x NVIDIA Tesla V100 32 GB

## Measured
| Metric | Value |
|---|---|
| prefill_pp512_tok_per_s | 690.99 tok/s ± 14.64 tok/s (512 tokens, n_ctx 512, 2 repeats) |
| prefill_pp4096_tok_per_s | 558.55 tok/s ± 2.13 tok/s (4096 tokens, n_ctx 4096, 2 repeats) |
| decode_tg128_depth0_tok_per_s | 30.43 tok/s ± 0.12 tok/s (n_gen 128, n_depth 0, n_ctx 128, markdown table) |
| decode_tg128_depth0_jsonl_tok_per_s | 30.15 tok/s (avg 30.151561, stddev 0.357213, samples 29.899 and 30.4041 tok/s, n_ctx 128) |
| decode_tg128_depth512_tok_per_s | 30.57 tok/s (avg 30.566179, stddev 0.371596, samples 30.3034 and 30.8289 tok/s, n_ctx 640) |
| decode_tg128_depth4096_tok_per_s | 29.43 tok/s (avg 29.433694, stddev 0.208050, samples 29.2866 and 29.5808 tok/s, n_ctx 4224) |
| gpu0_peak_memory_used | 24990 MiB (nvidia-smi, includes resident OCR at 8154 MiB; llama-bench process about 16830 MiB) |
| gpu0_vram_reported | 32494 MiB |
| weight_file_bytes | 16610544608 bytes |
| tensor_bytes | 16598564864 bytes |
| parameter_count | 26070390272 parameters |
| coding_prompts_passed | 3 of 3 |
| llama_cli_q1_retry_generation | 28.3 tok/s (prompt 171.9 tok/s, n_predict 2048, c 4096) |
| llama_cli_q2_generation | 28.1 tok/s (prompt 229.8 tok/s, n_predict 768, c 4096) |
| llama_cli_q3_generation | 28.0 tok/s (prompt 240.4 tok/s, n_predict 768, c 4096) |
| bench_wall_time | 40 s (2026-11-21T04:03:17Z to 04:03:57Z) plus 41 s depth (to 04:04:38Z) |
| qwen38_27b_q4km_record_prefill_3749 | 745.69 tok/s (3749 tokens, llama-server, 2026-11-20, base_off/server.log) |
| qwen38_27b_q4km_record_decode_after_3749 | 31.98 tok/s (512 tokens, llama-server, 2026-11-20) |
| qwen38_27b_q4km_record_prefill_10412 | 678.53 tok/s then 677.14 tok/s (10412 tokens, llama-server, 2026-11-20) |
| qwen38_27b_q4km_record_decode_after_10412 | 29.96 tok/s (512 tokens, llama-server, 2026-11-20) |
| qwen38_27b_q4km_record_prefill_13329 | 549.87 tok/s then 547.99 tok/s (13329 tokens, llama-server, 2026-11-20) |
| qwen38_27b_q4km_record_decode_after_13329 | 27.65 tok/s (512 tokens, llama-server, 2026-11-20) |

## Configuration
- prefill: 558.55 tok/s (4096 tokens, n_ctx 4096); also 690.99 tok/s (512 tokens, n_ctx 512)
- decode: 29.43 tok/s (n_ctx 4224 = n_gen 128 + depth 4096); also 30.57 tok/s at n_ctx 640 and 30.15 tok/s at n_ctx 128 (depth JSON); first-table tg128 30.43 tok/s at n_ctx 128
- model_quant: Unsloth Mainline UD-Q4_K_M (ftype Q4_K - Medium), 16610544608 bytes, arch inkling2_loop
- kv_cache: q8_0, n_ctx 4224 at the depth-4096 decode point; pp4096 uses n_ctx 4096
- turboquant: no
- speculative: no
- engine: llama.cpp 1.0.0-dev build 12601 commit 2a28df0f9, CUDA sm_70, PR #32704 inkling2_loop
- hardware: 1x Tesla V100-PCIE-32GB GPU0, 32494 MiB, CUDA 12.9, Intel Xeon E5-2682 v4 at 2.50 GHz, 32 threads

