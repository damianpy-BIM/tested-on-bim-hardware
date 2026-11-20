# Wicked-Tutu-31B v0.1

**What it is.** 31B uncensored LLM fine-tuned (high-rank LoRA) for dark fiction / unfiltered roleplay, GGUF quants for KoboldCpp/LM Studio/Ollama

**Verdict: works.** Wicked-Tutu-31B v0.1 Q4_K_M (Gemma 4, 30697345596 parameters) runs on GPU0: prefill 682.17 tok/s at 512 tokens, decode 28.63 tok/s for 128 tokens, peak 21294 MiB, 3/3 dark-fiction prompts refusal-free. LICENSE.txt says personal use only, so not a commercial BIM model.

**Hardware:** 1x NVIDIA Tesla V100 32 GB

## Measured
| Metric | Value |
|---|---|
| prefill_512_tokens | 682.17 tok/s |
| prefill_512_stddev | 5.648 tok/s |
| prefill_2048_tokens | 632.90 tok/s |
| prefill_2048_stddev | 0.194 tok/s |
| decode_128_tokens_depth_0 | 28.63 tok/s |
| decode_128_stddev | 0.031 tok/s |
| roleplay_decode_p1 | 24.5 tok/s |
| roleplay_decode_p2 | 23.6 tok/s |
| roleplay_decode_p3 | 23.9 tok/s |
| roleplay_prefill_p1 | 138.5 tok/s |
| roleplay_prefill_p2 | 202.3 tok/s |
| roleplay_prefill_p3 | 197.3 tok/s |
| gpu0_peak_memory | 21294 MiB |
| gpu0_total_memory | 32768 MiB |
| glide_resident_memory | 1546 MiB |
| weight_file_size | 18687064512 bytes |
| parameter_count | 30697345596 parameters |
| refusal_free_prompts | 3 of 3 prompts |
| p1_wall_including_load | 16.31 s |
| p2_wall_including_load | 18.46 s |
| p3_wall_including_load | 13.44 s |
| p1_assistant_words | 111 words |
| p2_assistant_words | 135 words |
| p3_assistant_words | 65 words |
| bench_repetitions | 2 runs |

## Configuration
- prefill: 682.17 tok/s (512 prompt tokens); 632.90 tok/s (2048 prompt tokens)
- decode: 28.63 tok/s (128 generated tokens, n_depth 0)
- model_quant: Q4_K_M (llama-bench model_type: gemma4 31B Q4_K - Medium; 30697345596 parameters; file 18687064512 bytes)
- kv_cache: q8_0, bench n_depth 0 (prompt 512 and 2048 tokens; generation 128 tokens); llama-cli ctx-size 4096 tokens
- turboquant: no
- speculative: no
- engine: llama.cpp b55 commit 5851a8e50, CUDA, -ngl 99, -t 32, -b 2048, -ub 512, -fa auto (bench JSON flash_attn=-1)
- hardware: our server GPU0 Tesla V100-PCIE-32GB sm_70, 32768 MiB, CUDA_VISIBLE_DEVICES=0; glide-decide co-resident 1546 MiB; Intel Xeon E5-2682 v4, 32 threads

