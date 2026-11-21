# Qwen-Image-2.1 GGUF (uncensored)

**What it is.** 7B text-to-image/editing model with GGUF quants, uncensored upstream weights, supports generation+editing, transparent RGBA, multi-reference editing

**Verdict: works.** Qwen-Image-2.1 Q4_K_M (4604558112 bytes) made three 1024x1024 images on one V100 in 116.72-119.59 s each, text encoder 8324.85 MB in RAM, nvidia-smi peak 14542 MiB.

**Hardware:** 1x NVIDIA Tesla V100 32 GB

## Measured
| Metric | Value |
|---|---|
| diffusion file size | 4604558112 bytes |
| text encoder file size | 9350798360 bytes |
| params total | 13360.48 MB |
| text encoder RAM | 8324.85 MB |
| diffusion VRAM | 4391.25 MB |
| VAE VRAM | 644.38 MB |
| params VRAM | 5035.63 MB |
| text encoder CUDA_Host | 6630.50 MB |
| text encoder CPU buffer | 594.08 MB |
| nvidia-smi baseline | 1318 MiB |
| nvidia-smi peak | 14542 MiB |
| GPU memory total | 32768 MiB |
| teapot generate_image | 119.59 s |
| teapot condition | 17.17 s |
| teapot sampling | 99.67 s |
| teapot VAE decode | 2.69 s |
| teapot process elapsed | 124 s |
| teapot PNG | 1463154 bytes |
| lake generate_image | 116.72 s |
| lake condition | 20.27 s |
| lake sampling | 94.28 s |
| lake VAE decode | 2.11 s |
| lake process elapsed | 120 s |
| lake PNG | 1978486 bytes |
| gear generate_image | 119.42 s |
| gear condition | 23.39 s |
| gear sampling | 94.00 s |
| gear VAE decode | 1.96 s |
| gear process elapsed | 122 s |
| gear PNG | 624385 bytes |
| steps | 20 steps |
| cfg-scale | 6.0 |
| output | 1024x1024 px |
| image_seq_len | 4096 tokens |

## Configuration
- prefill: n/a (image model, not an LLM)
- decode: n/a (image model, not an LLM)
- model_quant: Q4_K_M diffusion GGUF (q4_K 165 + q6_K 64 + bf16 68) + INT8 convrot text encoder (f32 254 + i8 254 + bf16 496)
- kv_cache: prefix cache default, not separately measured; image_seq_len 4096
- turboquant: no
- speculative: no
- engine: stable-diffusion.cpp master-1043-3be2378 (sd-cli-v100), FLOW Euler 20 steps, cfg-scale 6.0, flash attention off, --params-backend te=cpu
- hardware: Tesla V100-PCIE-32GB GPU0, sm_70, 32768 MiB, CUDA 12.9, host RAM offload for the text encoder

## Upstream
- https://huggingface.co/Qwen/Qwen-Image-2.1

Upstream code and weights keep their own licence.
