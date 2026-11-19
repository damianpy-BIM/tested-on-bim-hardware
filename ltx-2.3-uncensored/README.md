# LTX 2.3 Uncensored

**What it is.** Text-to-video and image-to-video generation model

**Verdict: works.** Runs locally on our server GPU0 (V100-32GB, Q4_K_M GGUF): genuine joint audio+video, 1280x704/736 5.04 s clips in 681-931 s per clip, clean on bright scenes, two-stage upscale pass bands on dark scenes - useful for offline BIM walkthrough renders, not interactive.

**Hardware:** 1x NVIDIA V100 32 GB

## Measured
| Metric | Value |
|---|---|
| t2v_two_stage_1280x704 | {'wall_s': 702.1, 'clip_duration_s': 5.04, 'wall_per_output_video_second_s': 139.3, 'resolution_px': '1280x704', 'frames': 121, 'fps': 24, 'stage1_s_per_step': 20.31, 'stage2_s_per_step': 102.74, 'model_load_s': 44.01, 'prompt_encode_s': 22.08, 'av_vae_decode_s': 32.96, 'save_s': 5.83, 'vram_peak_mib': 28728, 'vram_total_mib': 32768, 'audio_mean_dbfs': -6.1, 'audio_max_dbfs': 0.0, 'output_size_mb': 1.34} |
| t2v_single_stage_readme_1280x736 | {'wall_s': 930.9, 'clip_duration_s': 5.04, 'wall_per_output_video_second_s': 184.6, 'resolution_px': '1280x736', 'frames': 121, 'fps': 24, 's_per_step_full_res': 104.74, 'model_load_s': 30.57, 'prompt_encode_s': 18.2, 'av_vae_decode_s': 36.51, 'save_s': 6.45, 'vram_peak_mib': 25888, 'audio_mean_dbfs': -27.9, 'audio_max_dbfs': -6.3, 'output_size_mb': 2.61} |
| i2v_two_stage_1280x704 | {'wall_s': 680.9, 'clip_duration_s': 5.04, 'wall_per_output_video_second_s': 135.0, 'resolution_px': '1280x704', 'frames': 121, 'fps': 24, 'stage1_s_per_step': 20.15, 'stage2_s_per_step': 102.63, 'model_load_s': 24.96, 'prompt_encode_s': 16.41, 'av_vae_decode_s': 37.33, 'save_s': 7.55, 'vram_peak_mib': 29870, 'vram_headroom_mib': 2898, 'audio_mean_dbfs': -8.0, 'audio_max_dbfs': 0.0, 'output_size_mb': 2.36} |
| disk_and_memory | {'weights_total_gib': 24.8, 'dit_gguf_gib': 13.21, 'te_gguf_gib': 6.8, 'dit_loaded_fully_on_gpu_mib': 13643, 'te_staged_gb_offloaded_to_host_ram': 28, 'host_ram_total_gib': 756} |
| quality_assessment | 3 prompts tested: bright architectural-studio dolly (T2) and daylight I2V flight (T3) render clean and near-photorealistic with stable geometry and faithful first frame; dark neon car scene (T1) shows banding/stripe artifacts introduced by the x2 latent-upscale refine. Audio tracks non-silent and scene-plausible. Plan drawings render as illegible blobs - no readable text. |

## Configuration
- prefill: gemma-3-12b-it GGUF Q4_K_M text encoder via NestedTensor prep: 16.4-22.1 s per prompt; 28 GB staged with dynamic VRAM + CPU offload
- decode: video+audio VAE decode 33.0-37.3 s per 121-frame 720p clip; DiT sampling 20.2-20.3 s/step at 640x352 stage-1 latent, 102.6-104.7 s/step at full 1280x704/736 latent
- model_quant: DiT 22B GGUF Q4_K_M (13.21 GiB, full GPU load) + text encoder GGUF Q4_K_M; VAEs/projections/upscaler fp16 safetensors
- kv_cache: n/a for LLM sense; ComfyUI dynamic VRAM manages TE offload to 756 GiB host RAM, diffusion latents fp16 (V100 sm_70, no BF16)
- turboquant: n/a (not used)
- speculative: n/a (diffusion); distilled 'dmd (8 steps)' sigma schedule keeps sampling to 9+4 or single-stage 8 steps
- engine: ComfyUI 0.46.0 headless API + ComfyUI-GGUF-Loader (CCTech Suite) 2.21.0 with clone-local import-guard patch, torch 2.14.1+cu126 eager backend, Python 3.12.3
- hardware: our server GPU0 only: NVIDIA Tesla V100 32 GB (sm_70, FP16-only), 756 GiB host RAM, CUDA_VISIBLE_DEVICES=0, flock gpu0.lock + 30 min timeout per command

## Upstream
- https://huggingface.co/ChrisColeTech/LTX-2.3-uncensored-v1.4-FP8

Upstream code and weights keep their own licence.
