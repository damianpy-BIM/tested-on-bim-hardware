# SuperQwen3.8-27b-abliterated

**What it is.** Abliterated/uncensored 27B Qwen3.8-based LLM with fixed weights, 1M context, multimodal

**Verdict: works.** Q4_K_M fits GPU0 and answered 3 prompts with no refusal; prefill 843.73 tok/s at 512 tokens, decode 33.48 tok/s with speculative off and 72.81 tok/s with MTP K=6.

**Hardware:** 1x NVIDIA Tesla V100 32 GB

## Measured
| Metric | Value |
|---|---|
| prefill_tok_per_s | 843.73 tok/s |
| prefill_prompt_length | 512 tokens |
| prefill_stddev | 6.18 tok/s |
| prefill_samples_tok_per_s | 836.59, 847.58, 847.00 |
| decode_tok_per_s | 33.48 tok/s |
| decode_context | n_ctx 128 tokens, depth 0, n_gen 128 |
| decode_stddev | 0.013 tok/s |
| decode_samples_tok_per_s | 33.47, 33.49, 33.48 |
| llama_bench_repetitions | 3 |
| combined_pp512_tg128_throughput | 144.42 tok/s |
| combined_pp2048_tg128_throughput | 345.32 tok/s |
| mtp_decode_tok_per_s | 72.81 tok/s |
| mtp_decode_generated | 128 tokens |
| mtp_decode_prompt | 32 tokens |
| mtp_prefill_tok_per_s | 69.27 tok/s |
| mtp_draft_acceptance | 75.912 % (104 accepted / 137 generated) |
| mtp_mean_accepted_length | 5.52 tokens |
| mtp_draft_n_max | 6 |
| llama_bench_process_vram | 15764 MiB |
| llama_server_mtp_process_vram | 17828 MiB |
| gpu0_memory_used_with_glide_during_mtp_server | 19146 MiB |
| glide_resident | 1314 MiB |
| sampler_peak_gpu0_memory_used | 19184 MiB |
| chat_p1_generation | 30.6 tok/s |
| chat_p2_generation | 32.4 tok/s |
| chat_p3_generation | 32.7 tok/s |
| weight_file_q4_k_m | 16547400704 bytes |
| weight_file_mtp_q4_0 | 1680272000 bytes |
| model_parameters | 26895998464 |

## Configuration
- prefill: 843.73 tok/s (512 tokens)
- decode: 33.48 tok/s (n_ctx 128, depth 0)
- model_quant: Q4_K_M
- kv_cache: q8_0, n_ctx 512 prefill / 128 decode
- turboquant: no
- speculative: no
- engine: llama.cpp llama-bench b55 commit 5851a8e50, CUDA
- hardware: 1x Tesla V100-PCIE-32GB sm_70, CUDA_VISIBLE_DEVICES=0, threads 32, batch 2048, ubatch 512, flash attention on, n_gpu_layers 99

