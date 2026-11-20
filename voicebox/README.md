# Voicebox

**What it is.** Local voice cloning + multi-engine TTS app (7 TTS engines, 23 languages, MCP server) replacing ElevenLabs/WisprFlow

**Verdict: works.** Voicebox 0.6.0 LuxTTS cloned a 3.00 s clip and synthesized 3 English lines on CPU at 1.186–1.54 x realtime. GPU0 stayed at 1318 MiB under glide-decide, so no CUDA command ran.

**Hardware:** CPU only, on the NVIDIA Tesla V100 server

## Measured
| Metric | Value |
|---|---|
| lux_load_time | 19.578 s |
| prompt_encode_time | 19.929 s |
| en_1_synth_time | 2.913 s |
| en_1_audio_duration | 4.459 s |
| en_1_realtime_factor | 1.53 x |
| en_2_synth_time | 2.825 s |
| en_2_audio_duration | 4.352 s |
| en_2_realtime_factor | 1.54 x |
| en_3_synth_time | 2.266 s |
| en_3_audio_duration | 2.688 s |
| en_3_realtime_factor | 1.186 x |
| output_sample_rate | 48000 Hz |
| process_rss_peak | 2265.1 MiB |
| gpu0_vram_used_by_this_test | 0 MiB |
| gpu0_memory_used | 1318 MiB |
| reference_clip_duration | 3.00 s |
| weights_on_disk | 1337277328 bytes |
| wav_files_written | 3 files |

## Configuration
- prefill: not measured (TTS, no LLM)
- decode: not measured (TTS, no LLM)
- model_quant: LuxTTS ONNX FP32 (fm_decoder.onnx 477534010 bytes, text_encoder.onnx 17633735 bytes) plus openai/whisper-tiny
- kv_cache: not used, 0 tokens
- turboquant: no
- speculative: no
- engine: Voicebox 0.6.0, zipvoice LuxTTS CPU ONNX, 8 threads, num_steps 4, guidance_scale 3.0, t_shift 0.5, speed 1.0
- hardware: our server CPU, 8 of 64 threads, CUDA hidden. GPU0 Tesla V100-PCIE-32GB not used (1318 MiB held by glide-decide).

