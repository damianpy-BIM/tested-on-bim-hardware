# MACaQ

**What it is.** Open-source quantization tool for LLMs/multimodal models that produces GGUF/vLLM/Diffusers/PyTorch quantized models

**Verdict: partly.** MACaQ's GGUF pipeline ran end-to-end on one V100 (Qwen3-4B in 31 min, peak ~4.9 GB VRAM) and the 2.26 GB output generates correct, fluent text at parity quality with IQ4_XS+imatrix — but only in MACaQ's own forked llama.cpp (standard llama.cpp refuses to load it: 'expected 650, got 398 tensors'), and it runs ~8% slower than a plain IQ4_XS+imatrix GGUF on this GPU, so the advertised 2.33x/2.58x speedups did not reproduce on sm_70.

**Hardware:** 1x NVIDIA Tesla V100 32 GB

## Measured
| Metric | Value |
|---|---|
| quantize_wall_time (Qwen3-4B, 1xV100, full pipeline) | 31 min 09 s total = imatrix 1 min 39 s + transform/rotated-imatrix 3 min 14 s + llama-quantize 3 min 42 s + Flip-Refinement 22 min 34 s (refine = 72% of time, no resume) |
| peak_gpu_vram (quantize+refine stage) | 4860 MiB (direct nvidia-smi query; 3418 MiB via 30 s sampling) |
| peak_gpu_vram (whole measurement battery) | 8150 MiB (during f16 llama-bench load) |
| output_file_size | 2,259,854,080 bytes (2.26 GB), sha256 500011c8103748848a5180597e886b014c687a43592f10e4655d7668da58fe3c |
| prefill_speed (llama-bench pp512, ctx 2048, -ngl 99, KV f16, fork build) | 4021 tok/s with Triton h64 kernels; 3627 tok/s on fallback ggml path |
| decode_speed (llama-bench tg128, ctx 2048, -ngl 99, KV f16, fork build) | 149.9 tok/s with Triton h64 kernels; 126.3 tok/s fallback |
| baseline_speed_iq4xs_imatrix_same_fork_build (pp512 / tg128) | 4300 tok/s prefill / 163.1 tok/s decode — MACaQ = 0.94x prefill, 0.92x decode |
| baseline_speed_iq4xs_imatrix_standard_build (pp512 / tg128) | 4548 tok/s prefill / 168.2 tok/s decode |
| decode_speed_real_generation (short prompt, 96 tokens out, fork build) | 118.3 tok/s |
| perplexity (654-token held-out corpus, 256-token window) | MACaQ 49.63 +/- 11.57 vs IQ4_XS+imatrix 48.43 +/- 11.27 vs f16 48.83 +/- 11.45 (fork build) — parity within noise, small sample |
| quality_check (3 greedy prompts: planet, 17+26, sky-blue) | 3/3 correct and fluent; kernel vs fallback outputs byte-identical; standard llama.cpp load: FAILED (wrong number of tensors, expected 650 got 398) |

## Configuration
- prefill: 4021 tok/s (pp512, ctx 2048)
- decode: 149.9 tok/s (tg128, ctx 2048)
- model_quant: MACaQ vector-codebook IQ4_XS-class (4.25 bpw) + per-channel prescale + block-Hadamard rotation, q6_K embeddings/output tensors, 2-sweep Hessian Flip-Refinement (MACaQ-R), Qwen3-4B
- kv_cache: f16, 2048 tokens
- turboquant: no
- speculative: no
- engine: MACaQ fork llama.cpp (pin 86632248188c, Aug 2026) + AOT Triton h64 kernels (MACAQ_TRITON_KERNEL_DIR); compared against standard llama.cpp 5851a8e50 b55 (Nov 2026); CUDA 12.9, torch 2.11.0+cu126
- hardware: 1x Tesla V100-PCIE-32GB (sm_70, GPU0) on our server, Xeon E5-2682 v4, 64 GB RAM

