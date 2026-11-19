# Qwopus3.8-27B-Coder-Flash

**What it is.** 27B coding and reasoning model fine-tuned on 200K examples with 20K agent interaction samples, available in GGUF quantizations

**Verdict: works.** Qwopus3.8-27B-Coder-Flash Q4_K_M runs entirely on one V100-32GB (peak 16464 MiB) at 840 tok/s prefill / 34 tok/s decode (55 tok/s with built-in MTP), and its generated code passed 17/17 of its own unit tests across 3 coding prompts.

**Hardware:** 10x NVIDIA Tesla V100 32 GB

## Measured
| Metric | Value |
|---|---|
| model_size | 16.81 GB (16,810,715,392 bytes Q4_K_M GGUF, matches HF listing) |
| prefill_pp512 | 839.63 tok/s (512-token prompt, llama-bench, batch 2048 / ubatch 512) |
| prefill_pp2048 | 829.73 tok/s (2048-token prompt, llama-bench) |
| prefill_pp8192 | 779.61 tok/s (8192-token prompt, llama-bench) |
| decode_tg128 | 33.98 tok/s (128 generated tokens, 8k ctx, no speculative decoding) |
| decode_tg512 | 34.04 tok/s (512 generated tokens, 8k ctx, no speculative decoding) |
| decode_tg1024 | 34.22 tok/s (1024 generated tokens, 8k ctx, no speculative decoding) |
| decode_mtp | 55.4 tok/s (prompt p2, seed 42, 8k ctx, --spec-type draft-mtp; baseline same run 32.7 tok/s, +69%) |
| peak_vram_gpu0 | 16464 MiB (ctx 8192, f16 KV, all layers on GPU, sampled every 2 s) |
| weights_on_gpu | 15.65 GiB, -ngl all, no CPU offload |
| code_quality | 17/17 model-generated unit tests passed when executed (merge_intervals 5/5, chunk_sequence 7/7, LRUCache 5/5) |
| end_to_end_per_prompt | 47.6-74 s wall per prompt (load from page cache + prefill + 0.9-1.6k-token answer) |
| download_time | 4.5 min at 62-67 MB/s from huggingface.co |
| caveat | long chain-of-thought: one run truncated mid-code at -n 2048; completed and passed at -n 4096; vision mmproj (1.84 GB) not tested |

## Configuration
- prefill: 839.63 tok/s (512-token prompt); 779.61 tok/s (8192-token prompt), llama-bench batch 2048 / ubatch 512
- decode: 34.04 tok/s (tg512, 8k ctx, no spec); 55.4 tok/s (prompt p2, seed 42, 8k ctx, MTP draft-mtp)
- model_quant: Q4_K_M (16.81 GB GGUF, 27.32 B params, arch qwen35 hybrid SSM)
- kv_cache: f16, 8192 tokens (hybrid arch: full attention only every 4th layer, 24 Q / 4 KV heads, head dim 256)
- turboquant: no
- speculative: MTP (built-in nextn_predict head, --spec-type draft-mtp)
- engine: llama.cpp 0.9.0-dev build 55 (commit 5851a8e50), CUDA 12.9, -ngl all
- hardware: our server GPU0 only, Tesla V100-PCIE-32GB (sm_70, no BF16), 755 GB host RAM, model fully on GPU

