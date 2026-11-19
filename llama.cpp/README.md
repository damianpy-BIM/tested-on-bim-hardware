# llama.cpp

**What it is.** C++ inference engine for LLMs with CPU/GPU support and quantization

**Verdict: works.** Official llama.cpp b12541 CPU-only binaries ran a quantized Qwen2.5-1.5B (Q4_K_M) on a CUDA-less Xeon CPU at 28-30 tok/s decode and 107-112 tok/s prefill with 1.75 GiB peak RAM - works out of the box and useful for BIM as the standard no-CUDA local LLM engine

**Hardware:** CPU only, on the NVIDIA Tesla V100 server

## Measured
| Metric | Value |
|---|---|
| decode_chat | 28.3-29.8 tok/s (llama-cli, 8 threads, temp 0) |
| prefill_chat | 107.1-112.5 tok/s (llama-cli, 8 threads) |
| decode_bench_128tok | 22.34 tok/s (8 threads) / 5.52 tok/s (1 thread), llama-bench |
| prefill_bench_512tok | 84.30 tok/s (8 threads) / 13.16 tok/s (1 thread), llama-bench |
| peak_ram | 1.75 GiB (1,838,504 KB, 8 threads, ctx 2048, incl. model) |
| model_file | 1,117,320,736 bytes Q4_K_M GGUF (Qwen2.5-1.5B-Instruct, 1.78 B params) |
| model_download | 1.04 GiB in 12 seconds (~93 MB/s, official Qwen Hugging Face repo) |
| end_to_end_run | 2.85-4.72 s per chat run (process start + model load + generation) |
| quality | 3 prompts: 2/3 fully correct (27*43=1161; correct French translation), 1/3 fluent but vague; 3/3 on-task and fluent |
| cpu_backend | libggml-cpu-haswell.so (AVX2) auto-dispatched, CPU-only build |
| node_contention | load average 79-100 on 64 threads during test (shared node, other tenants); 16/32/64-thread bench rows contention-corrupted |

## Configuration
- prefill: 107.1-112.5 tok/s (chat prompt ~30 tokens) / 84.30 tok/s (512-token bench prompt), 8 threads
- decode: 28.3-29.8 tok/s (ctx 2048, 8 threads) / 22.34 tok/s (ctx 640, 128-token bench gen, 8 threads)
- model_quant: Q4_K_M, Qwen2.5-1.5B-Instruct GGUF, 1,117,320,736 bytes
- kv_cache: f16, ctx 2048 (chat runs) / f16, ctx 640 (llama-bench pp512/tg128)
- turboquant: no
- speculative: no
- engine: llama.cpp b12541 (commit 76f186df7), official ubuntu-x64 prebuilt CPU-only binaries, ggml CPU backend libggml-cpu-haswell.so (AVX2), 8 threads
- hardware: our server CPU only: 2x Intel Xeon E5-2682 v4 @ 2.50GHz (64 threads), 755 GB RAM, no GPU visible (CUDA_VISIBLE_DEVICES=), shared node load avg 79-100 during test

## Upstream
- https://github.com/ggerganov/llama.cpp

Upstream code and weights keep their own licence.
