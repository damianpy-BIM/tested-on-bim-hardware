# Qwen3.8 27B Heretic Abliterated

**What it is.** GGUF-quantized 27B Qwen3.8 model abliterated to remove safety filters for uncensored text generation

**Verdict: works.** RVN Q4_K_M loads on GPU0 and answered 3/3 prompts with no refusal; prefill 840.64 tok/s at 512 tokens, decode 33.51 tok/s at 128 tokens, depth 0, speculative off.

**Hardware:** 1x NVIDIA Tesla V100 32 GB

## Measured
| Metric | Value |
|---|---|
| prefill | 840.64 tok/s (512 tokens, 3 runs, stddev 10.89 tok/s) |
| decode | 33.51 tok/s (128 tokens, depth 0, 3 runs, stddev 0.024 tok/s) |
| combined_pp512_tg128 | 140.74 tok/s |
| combined_pp2048_tg128 | 344.06 tok/s |
| gpu0_memory_used_peak | 17746 MiB of 32768 MiB |
| glide_resident_before_bench | 1314 MiB |
| weight_file | 16547400224 bytes |
| model_parameters | 26895998464 parameters |
| chat_p1_prompt | 72.9 tok/s |
| chat_p1_generation | 29.4 tok/s |
| chat_p2_prompt | 138.9 tok/s |
| chat_p2_generation | 32.3 tok/s |
| chat_p3_prompt | 123.5 tok/s |
| chat_p3_generation | 32.3 tok/s |
| refusals | 0 of 3 prompts |
| prompt1_answer | 391 and Paris |

## Configuration
- prefill: 840.64 tok/s (512 tokens)
- decode: 33.51 tok/s (128 tokens, depth 0)
- model_quant: Q4_K_M
- kv_cache: q8_0, bench sized to 512 prefill / 128 decode; chat -c 4096
- turboquant: no
- speculative: no
- engine: llama.cpp llama-bench and llama-cli b55 commit 5851a8e50, CUDA
- hardware: 1x Tesla V100-PCIE-32GB sm_70, CUDA_VISIBLE_DEVICES=0, threads 32, batch 2048, ubatch 512, flash attention on, n_gpu_layers 99

