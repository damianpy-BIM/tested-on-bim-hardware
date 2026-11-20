# ODS

**What it is.** One-click Local AI platform that detects hardware, downloads appropriate models, and provides local inference with agents, voice, RAG, image generation, and plugins

**Verdict: partly.** ODS's six-phase installer completed rootless, hardware auto-detection and model download worked exactly as claimed and local inference served real answers — but only after a docker→podman shim, the documented CPU override, and two .env port fixes; as a self-hosted BIM chat+API bundle it is genuinely useful.

**Hardware:** CPU only, on the NVIDIA Tesla V100 server

## Measured
| Metric | Value |
|---|---|
| model_download | 5.29 GiB (5,680,522,464 bytes) in ~40 s (~109 MB/s), SHA256 verified |
| model_load_time | 8.3 s |
| stack_bringup | ~20 s to healthy llama-server with images cached; Open WebUI HTTP 200 within ~90 s |
| container_images | ~6.76 GB total (5.93 GB pulled + 0.83 GB built) |
| prefill_speed | 16.4–18.6 tok/s on 47–418-token prompts; 17.9–18.0 tok/s at 2,602–2,616 tokens |
| decode_speed | 5.2–5.6 tok/s (65,536-token ctx, 8 threads, CPU) |
| inference_wall_time | 12.1 s / 43.9 s / 191.2 s for the 3 test prompts |
| ram_llama_server | 4.84 GiB cgroup (RSS 9.94 GiB incl. mmap'd weights in page cache) |
| ram_whole_stack | ~6.7 GiB cgroup across 8 containers |
| hardware_detection | correct: 10× Tesla V100-PCIE-32GB via sysfs validation, 755.8 GiB RAM, 5,976 GB free disk, tier T3 |
| answer_quality | 3/3 BIM prompts substantively correct (LOD 350, BEP extraction, 3,314 m³ total and £670.68/m² both hand-verified); 1 mislabeled citation (cited 'Clause 2.1/RICS Red Book' where source says Clause 2) |

## Configuration
- prefill: 16.4–18.6 tok/s (47–418 token prompts); 17.9–18.0 tok/s (2,602–2,616 tokens)
- decode: 5.2–5.6 tok/s (65,536-token context, 8 threads, host load ~90)
- model_quant: Q4_K_M (Qwen 3.5 9B, 5,680,522,464 bytes)
- kv_cache: q8_0 K+V, 65536-token ctx (cache-ram 1024 MiB, 4 context checkpoints)
- turboquant: no
- speculative: ngram-mod
- engine: llama.cpp llama-server server-b9014 (ghcr.io/ggml-org/llama.cpp@sha256:2e7953df...) via standalone Docker Compose v2 v5.8.0 on rootless podman 4.9.3, CPU backend (GPU_BACKEND=cpu)
- hardware: our server: 64-thread CPU, 755 GiB RAM, no GPU used — NVIDIA Container Toolkit needs sudo (unavailable on this rootless-podman host); ODS's own detection saw 10× Tesla V100-PCIE-32GB (10 shown in capability profile)

