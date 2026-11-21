# Open-source 2B TTS (zero-shot voice clone)

**What it is.** 2B-param TTS model with zero-shot voice cloning, 48kHz output, 30+ languages incl. 8 Chinese dialects

**Verdict: works.** VoxCPM2 zero-shot clone runs on one V100 in FP16 at 48000 Hz; steady RTF 1.72 wall_s/audio_s, peak PyTorch alloc 5933.4 MiB.

**Hardware:** 1x NVIDIA Tesla V100 32 GB

## Measured
| Metric | Value |
|---|---|
| output_sample_rate | 48000 Hz |
| load_time | 32.459 s |
| en_generate_time | 40.241 s |
| en_audio_duration | 4.960 s |
| en_rtf | 8.113 wall_s/audio_s |
| fr_generate_time | 7.218 s |
| fr_audio_duration | 4.160 s |
| fr_rtf | 1.735 wall_s/audio_s |
| zh_generate_time | 8.802 s |
| zh_audio_duration | 5.120 s |
| zh_rtf | 1.719 wall_s/audio_s |
| peak_pytorch_allocated | 5933.4 MiB |
| gpu0_memory_used_after_zh | 7933.9 MiB |
| glide_resident | 1314 MiB |
| clip_fraction | 0 |
| en_energy_above_8khz | 0.8214 % |
| fr_energy_above_8khz | 1.1770 % |
| zh_energy_above_8khz | 0.5222 % |
| reference_energy_above_8khz | 0.2477 % |

## Configuration
- prefill: n/a (TTS, no LLM prefill bench)
- decode: n/a (TTS, no LLM decode tok/s)
- model_quant: FP16 runtime (safetensors stored BF16, config dtype float16)
- kv_cache: float16, max_length 8192
- turboquant: no
- speculative: no
- engine: voxcpm 2.0.3, PyTorch 2.5.1+cu124, CUDA 12.4
- hardware: our server GPU0 Tesla V100-PCIE-32GB sm_70, CUDA_VISIBLE_DEVICES=0

