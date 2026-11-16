# Qwen4 open-weight models

**What it is.** Open-weight Qwen4 LLM weights likely for local/self-hosted inference.

**Verdict: works.** Official Qwen3.8-27B weights (the X post's 'Qwen4-27B' does not exist on the Qwen Hugging Face org) run entirely on our server GPU0 as a 17.44 GB Q4_K_M GGUF: 786.7 tok/s prefill and 33.8 tok/s decode in llama-bench, 641.8 tok/s prefill / 27.9 tok/s decode on a real 1039-token llama-server request, 39.2 tok/s with the model's own MTP draft head (+37.5%), peak GPU0 memory 17,546 MiB, correct answers on 4/4 test prompts.

**Hardware:** 1x NVIDIA V100 32 GB

## Measured
| Metric | Value |
|---|---|
| tested_weights | Qwen/Qwen3.8-27B (Apache-2.0, released 2026-11-07) as community GGUF bartowski/Qwen3.8-27B-GGUF Q4_K_M - the Qwen org publishes safetensors only, and no model named Qwen4 exists there |
| prefill_llama_bench_512 | 856.2 tok/s (512-token prompt) |
| prefill_llama_bench_2048 | 842.1 tok/s (2048-token prompt) |
| prefill_llama_bench_8192 | 786.7 tok/s (8192-token prompt, 10.414 s for the pass) |
| prefill_llama_server_1039_tok | 641.8 tok/s (1039-token real markdown prompt, -c 8192, Prometheus counter delta 1.619 s) |
| prefill_llama_server_short_prompt | 130.5 tok/s aggregate over three 39-52-token prompts (139 tokens in 1.065 s); about 0.4 s to first token |
| decode_llama_bench | 33.8 tok/s (128 tokens generated from an empty context) |
| decode_llama_server | 28.5 tok/s (491 tokens generated over 3 short prompts, 17.236 s) |
| decode_llama_server_1k_context | 27.9 tok/s (128 tokens generated after a 1039-token prompt, 4.580 s) |
| decode_with_MTP_speculation | 39.2 tok/s (160 tokens, 595-token prompt, -c 4096, draft-mtp 3 draft tokens) vs 28.5 tok/s in the same A/B run = +37.5% |
| prefill_with_MTP_speculation | 366.6 tok/s vs 424.4 tok/s without speculation on the same 595-token prompt = -13.6% |
| peak_gpu0_memory_server_ctx8192 | 17,546 MiB (17.1 GiB) on a 32,494 MiB device, sampled every 8 s |
| peak_gpu0_memory_MTP_ctx4096 | 17,856 MiB (17.4 GiB) |
| gpu0_headroom_at_peak | about 14.9 GB still free on GPU0 at the 8192-token context |
| model_load_time | 8.1 s from load_model start to 'model loaded' in the llama-server log (11.8 s wall including process start) |
| weights_file_size | 17,442,399,968 bytes = 17.44 GB (16,635 MiB) |
| parameter_count | 27,320,697,856 (llama-bench model_n_params field for this GGUF) |
| cpu_offloaded_layers | 0 (all layers on GPU, no offload or out-of-memory line in any log) |
| quality_4_prompts | 4/4 correct: RAID-1 mirror explanation, complete working Python merge of two sorted linked lists, 7 crates x 24 boxes x 15 units = 2,520, and a 1039-token summarisation that stayed inside the source and flagged the cut-off table instead of inventing numbers |
| measured_repetition | 1 repetition per measurement (-r 1), single samples not averages; peak VRAM during the llama-bench run itself was not captured (sampler bug), the peaks above come from the server and CLI/MTP runs |

## Configuration
- prefill: 786.7 tok/s (8192-token prompt, llama-bench) - also measured 641.8 tok/s (1039-token prompt, llama-server) and 130.5 tok/s (39-52-token prompts, llama-server)
- decode: 33.8 tok/s (empty context, llama-bench); 27.9 tok/s at ~1.1k-token live context in llama-server; 39.2 tok/s at 595-token prompt with MTP
- model_quant: Q4_K_M (17.44 GB file, 16,635 MiB of weights, 27.32 B parameters)
- kv_cache: f16 K/V, 8192-token context (-c 8192, 4 slots, unified KV, flash-attn on; f16 K/V also in the llama-bench run); hybrid qwen35 arch - 16 full-attention layers + 48 Gated DeltaNet layers, no KV for the delta-net layers
- turboquant: no
- speculative: MTP (llama.cpp --spec-type draft-mtp --spec-draft-n-max 3, using the model's own MTP head, no second model loaded); baseline without speculation measured in the same run
- engine: llama.cpp commit 5851a8e50, build 55, ggml 0.29.0, llama 0.9.0, CUDA backend (CUDA 12.9), -ngl 99, -fa on, 32 CPU threads, CUDA graph reuse observed; instruct sampler per official README (temp 0.7, top_p 0.8, top_k 20, min_p 0, presence_penalty 1.5, --reasoning off)
- hardware: our server GPU0 - Tesla V100-PCIE-32GB (sm_70 / CC 7.0, no BF16, 32,494 MiB reported), Intel Xeon E5-2682 v4 @ 2.50GHz, ran under the GPU0 flock lease

