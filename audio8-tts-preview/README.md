# Audio8-TTS Preview

**What it is.** 0.6B open-weight TTS model with zero-shot voice cloning, 11 languages, bundled 44.1kHz codec

**Verdict: works.** Works: Audio8-TTS Preview 0.6B zero-shot clone at 44100 Hz on GPU0 FP16; Whisper matched 3/3 prompts; 0.332–0.364× realtime; peak 2206.8 MiB.

**Hardware:** 1x NVIDIA Tesla V100 32 GB

## Measured
| Metric | Value |
|---|---|
| load_time | 2.116 s |
| peak_gpu_allocated | 2206.8 MiB |
| model_params_excluding_codec | 601159424 |
| weight_dtype_on_gpu | float16 |
| checkpoint_dtype | bfloat16 |
| output_sample_rate | 44100 Hz |
| en_clone_generate_time | 17.983 s |
| en_clone_audio_duration | 6.548 s |
| en_clone_realtime_factor | 0.364 x |
| en_clone_codec_frames | 141 frames |
| en_clone_frame_rate | 7.841 frames/s |
| fr_clone_generate_time | 16.752 s |
| fr_clone_audio_duration | 5.991 s |
| fr_clone_realtime_factor | 0.358 x |
| fr_clone_codec_frames | 129 frames |
| fr_clone_frame_rate | 7.701 frames/s |
| en_noref_generate_time | 10.756 s |
| en_noref_audio_duration | 3.576 s |
| en_noref_realtime_factor | 0.332 x |
| en_noref_codec_frames | 77 frames |
| en_noref_frame_rate | 7.159 frames/s |
| whisper_matches | 3 of 3 prompts |

## Configuration
- prefill: n/a (TTS; reference encode and prefill not timed separately)
- decode: 7.841 frames/s (141 codec frames, 6.548 s audio, en_clone)
- model_quant: BF16 checkpoint loaded as FP16 (601159424 AR params; codec.pth separate)
- kv_cache: transformers dynamic cache, max_seq_len 2048, max_new_tokens 1024
- turboquant: no
- speculative: no
- engine: transformers 4.57.6 ArkttsModel, torch 2.7.1+cu126
- hardware: 1x Tesla V100-PCIE-32GB GPU0 sm_70, driver 580.178.04, CUDA wheel 12.6, FP16

