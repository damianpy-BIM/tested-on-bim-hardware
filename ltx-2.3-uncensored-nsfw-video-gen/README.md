# LTX-2.3 Uncensored NSFW Video Gen

**What it is.** Open video+audio generation model (LTX-2.3 merged with Eros10 NSFW LoRA, DMD distillation, ICLoRA detailer) with refusals removed, runs on 14GB consumer GPU

**Verdict: works.** LTX-2.3 uncensored v1.4 Q4_K_M generates 1.042 s joint video+audio on GPU0 (768x512): 150.1 s wall at 8 steps (21306 MiB, audio mean -15.1 dB) and 85.3 s at 4 steps (20286 MiB, audio mean -57.1 dB). Same files as lab-45711875. Offline only.

**Hardware:** 1x NVIDIA Tesla V100 32 GB

## Measured
| Metric | Value |
|---|---|
| t2v_8step_wall_time | 150.1 s |
| t2v_8step_clip_duration | 1.042 s |
| t2v_8step_resolution | 768x512 px |
| t2v_8step_frames | 25 frames at 24 fps |
| t2v_8step_wall_per_output_second | 144.1 s per 1 s of video |
| t2v_8step_model_load | 47.18 s |
| t2v_8step_prompt_encode | 19.4 s |
| t2v_8step_sampler | 77.62 s (9.70 s/step, 8 steps) |
| t2v_8step_av_decode | 4.49 s |
| t2v_8step_vram_peak | 21306 MiB |
| t2v_8step_vram_total | 32768 MiB |
| t2v_8step_audio_mean | -15.1 dB |
| t2v_8step_audio_max | -3.0 dB |
| t2v_8step_file_size | 255122 bytes |
| t2v_4step_wall_time | 85.3 s |
| t2v_4step_clip_duration | 1.042 s |
| t2v_4step_resolution | 768x512 px |
| t2v_4step_wall_per_output_second | 81.9 s per 1 s of video |
| t2v_4step_model_load | 20.53 s |
| t2v_4step_prompt_encode | 15.7 s |
| t2v_4step_sampler | 41.82 s (10.46 s/step, 4 steps) |
| t2v_4step_av_decode | 3.41 s |
| t2v_4step_vram_peak | 20286 MiB |
| t2v_4step_audio_mean | -57.1 dB |
| t2v_4step_audio_max | -28.4 dB |
| t2v_4step_file_size | 521723 bytes |
| weights_on_disk | 26609124150 bytes |

## Configuration
- prefill: Gemma-3-12B GGUF Q4_K_M prompt encode 19.4 s (8-step run) and 15.7 s (4-step run); not an LLM tok/s figure
- decode: joint video+audio VAE decode 4.49 s (8-step) and 3.41 s (4-step) for 25 frames at 768x512; DiT 9.70 s/step at 8 steps and 10.46 s/step at 4 steps
- model_quant: DiT LTX-2.3 22B GGUF Q4_K_M (14183407072 bytes) + Gemma-3-12B Q4_K_M text encoder; VAEs and projections fp16 safetensors; FP8 not used (sm_70)
- kv_cache: n/a (diffusion). ComfyUI dynamic VRAM, fp16 latents, V100 sm_70
- turboquant: no
- speculative: no
- engine: ComfyUI headless + ComfyUI-GGUF-Loader LTXV23 nodes, torch 2.14.1+cu126, Python 3.12, single-stage dmd schedule, CFG 3.5, euler_ancestral
- hardware: our server GPU0 only, Tesla V100-PCIE-32GB, sm_70, CUDA_VISIBLE_DEVICES=0, flock gpu0.lock. glide-decide held 1314 MiB on the same card during the run.

