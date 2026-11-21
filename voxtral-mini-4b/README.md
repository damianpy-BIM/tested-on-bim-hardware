# Voxtral-Mini-4B

**What it is.** Streaming multilingual ASR model (13 languages, <500ms latency) from Mistral AI, demoed running in-browser via WebGPU

**Verdict: works.** Voxtral Mini 4B Realtime Q8_0 on GPU0 transcribes faster than realtime: JFK 11.00 s audio in 2.71 s (4.06x, WER 0%), TIMIT 2.92 s in 0.96 s (3.03x, WER 9.09%).

**Hardware:** 1x NVIDIA Tesla V100 32 GB

## Measured
| Metric | Value |
|---|---|
| jfk_audio_duration | 11.00 s |
| jfk_stream_time | 2.71 s |
| jfk_realtime_factor | 4.06 x |
| jfk_encoder_time | 1.14 s |
| jfk_decoder_time | 1.56 s |
| jfk_step_latency | 18.2 ms per 80 ms audio |
| jfk_generated_tokens | 149 tokens |
| jfk_decode_speed | 95.5 tok/s |
| jfk_wer | 0% (0 errors / 22 words) |
| jfk_wall_time_including_load | 6.74 s |
| bcn_weather_audio_duration | 11.04 s |
| bcn_weather_stream_time | 2.19 s |
| bcn_weather_realtime_factor | 5.04 x |
| bcn_weather_encoder_time | 0.86 s |
| bcn_weather_decoder_time | 1.33 s |
| bcn_weather_step_latency | 14.7 ms per 80 ms audio |
| bcn_weather_generated_tokens | 149 tokens |
| bcn_weather_decode_speed | 112.0 tok/s |
| bcn_weather_wer | not scored (no published reference transcript) |
| bcn_weather_wall_time_including_load | 11.23 s |
| timit_ldc93s1_audio_duration | 2.92 s |
| timit_ldc93s1_stream_time | 0.96 s |
| timit_ldc93s1_realtime_factor | 3.03 x |
| timit_ldc93s1_encoder_time | 0.50 s |
| timit_ldc93s1_decoder_time | 0.46 s |
| timit_ldc93s1_step_latency | 20.1 ms per 80 ms audio |
| timit_ldc93s1_generated_tokens | 48 tokens |
| timit_ldc93s1_decode_speed | 104.3 tok/s |
| timit_ldc93s1_wer | 9.09% (1 substitution / 11 words) |
| timit_ldc93s1_wall_time_including_load | 5.20 s |
| gpu0_peak_memory | 15396 MiB |
| gpu0_memory_before_run | 8160 MiB |
| gpu0_memory_added_by_this_run | 7236 MiB |

## Configuration
- prefill: encoder 0.86 s (11.04 s audio, bcn_weather); no separate text prefill
- decode: 112.0 tok/s (149 tokens, decoder 1.33 s, context 149 tokens, n_ctx 8192)
- model_quant: Q8_0 text GGUF + Q8_0 voxtral_rt mmproj
- kv_cache: f16, 8192 tokens
- turboquant: no
- speculative: no
- engine: llama.cpp llama-mtmd-cli 1.0.0-dev commit 50518b64c, mtmd voxtral_rt stream, temp 0, flash-attn off, ngl 99, threads 32
- hardware: our server GPU0 Tesla V100-PCIE-32GB sm_70, CUDA_VISIBLE_DEVICES=0, CUDA 12.9

## Upstream
- https://huggingface.co/mistralai

Upstream code and weights keep their own licence.
