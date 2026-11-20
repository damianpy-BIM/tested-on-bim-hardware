# Portable-AI-USB

**What it is.** Toolkit/scripts to run large uncensored AI models (likely via llama.cpp) self-contained from a USB drive

**Verdict: works.** Ollama 0.40.16 from Portable-AI-USB served Huihui Qwythos 9B Q6_K on GPU0 only: 279.48 tok/s prefill (74 tokens) and 75.57 tok/s decode (111 tokens, f16 KV, 4096 context); default Vulkan mode sees every V100, so the kit is not safe unmodified on this host.

**Hardware:** CPU only, on the NVIDIA Tesla V100 server

## Measured
| Metric | Value |
|---|---|
| prefill_arith | 279.48 tok/s (74 tokens, 264.778 ms) |
| decode_arith | 75.57 tok/s (111 tokens, 1.469 s, 4096 context slot) |
| prefill_code | 448.74 tok/s (75 tokens, 167.133 ms) |
| decode_code | 44.11 tok/s (128 tokens, 2.902 s, 4096 context slot) |
| prefill_usb | 207.88 tok/s (71 tokens, 341.545 ms) |
| decode_usb | 74.52 tok/s (128 tokens, 1.718 s, 4096 context slot) |
| arith_answer | 391 |
| first_model_load | 49.799 s |
| arith_wall | 51.587 s |
| code_wall | 3.147 s |
| usb_wall | 2.243 s |
| gpu0_memory_used_peak | 8368 MiB |
| gpu0_utilization_during | 89 % |
| model_buffer_gpu0 | 6212.17 MiB |
| kv_cache_gpu0 | 128.00 MiB |
| layers_on_gpu | 34/34 layers |
| gpu0_memory_after_stop | 1318 MiB |

## Configuration
- prefill: 279.48 tok/s (74 tokens)
- decode: 75.57 tok/s (4096 context slot, 111 generated tokens)
- model_quant: Q6_K (GGUF file_type 18, 6.57 BPW, 7.03 GiB)
- kv_cache: f16, 4096 tokens (K 64.00 MiB + V 64.00 MiB, 8 full-attention layers)
- turboquant: no
- speculative: no
- engine: Ollama 0.40.16 llama-server, cuda_v12, flash-attn off, -c 4096 -b 512 -ub 512, n_threads 32
- hardware: our server GPU0 Tesla V100-PCIE-32GB sm_70, CUDA_VISIBLE_DEVICES=0, OLLAMA_VULKAN=false, 34/34 layers on GPU, driver 580.178.04

## Upstream
- https://github.com/techjarves/Portable-AI-USB

Upstream code and weights keep their own licence.
