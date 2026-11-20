# FastFrames-L on a 16 GB Apple M4

**What it is.** Apple's open video model, 81 frames at 480p from one model per frame

**Verdict: cannot-run.** FastFrames-L cannot run on a 16 GiB Apple M4: it needs 64.6 GB (39.6 GB weights + 25.0 GB KV cache); MPS refused the 26.61 GiB and 24.99 GiB buffers and the CUDA reference path is not compiled. It ran on our 8x V100 node (277 s per 5.06 s clip).

**Hardware:** Apple M4 Mac mini

## Measured
| Metric | Value |
|---|---|
| weights_plus_kv | 64.6 GB total (69,350,914,450 bytes: 39.594 GiB inference weights + 24.994 GiB KV cache) |
| mps_dit_allocation | RuntimeError: Invalid buffer size: 26.61 GiB (DiT data 28,576,983,168 bytes, 14,288,491,584 BF16 params; 0.00030 s, RSS unchanged) |
| mps_kv_allocation | RuntimeError: Invalid buffer size: 24.99 GiB (26,836,992,000 bytes, 40 layers x k+v, shape [1, 32760, 40, 128]; 0.0048 s, RSS unchanged) |
| hardware_ram | 17,179,869,184 bytes (16 GiB unified) |
| inference_weights_sum | 42,513,922,450 bytes before KV cache and activations |
| dit_file | 28,577,096,680 bytes (HF Content-Length and tree size, 2026-11-20) |
| kv_refiner_file | 1,780,342,784 bytes |
| pixel_decoder_file | 286,952,688 bytes |
| umt5_xxl_bf16 | 11,361,920,418 bytes (Wan-AI/Wan2.1-T2V-14B models_t5_umt5-xxl-enc-bf16.pth) |
| wan_vae | 507,609,880 bytes (Wan2.1_VAE.pth) |
| clip_recipe | 21 latent frames, 81 RGB frames, 832x480 px, 16 fps = 5.0625 s clip (hardcoded in FastFramesConfig) |
| tokens_per_latent_frame | 1,560 (60*104/4, code-derived, not a timed run) |
| mps_small_allocations | 1 MiB and one 0.625 GiB layer cache allocated ok (0.764 s / 0.271 s) |
| cuda_path | AssertionError: Torch not compiled with CUDA enabled (reference device is cuda; official pin torch==2.9.1+cu128) |
| peak_rss | 304,414,720 bytes (probe; unchanged on both rejected allocations) |
| weights_on_disk | 4,194,440 bytes (DiT header range only; bodies not downloaded) |
| prior_v100_run | partly on our 8x V100 node: 26.8 GB KV offload, 277 s per 5.06 s clip (task brief from that run, not re-measured here) |

## Configuration
- prefill: per-frame causal forward_frame; no separate long prefill in generate(). Not timed (run not reached)
- decode: 21 latent frames, 81 RGB frames, 16 fps, 832x480. Not timed (run not reached)
- model_quant: BF16 as stored, 1095/1095 tensors, 14,288,491,584 params, 28,576,983,168 data bytes. No int8/fp8/TurboQuant
- kv_cache: bf16 persistent per layer, 26,836,992,000 bytes for the only published 21-frame 480p recipe. allocate_kv_cache device default cuda. No inference offload flag
- turboquant: n/a
- speculative: no (none in scripts/generate.py)
- engine: Apple ml-fastframes PyTorch a65c592 (2026-11-18). Host torch 2.15.0 MPS. Official pin torch==2.9.1+cu128. CUDA not compiled
- hardware: Mac16,10 Apple M4, 10 CPU, 17,179,869,184 bytes unified memory

## Upstream
- https://github.com/apple/ml-fastframes

Upstream code and weights keep their own licence.
