# speech-to-speech

**What it is.** Modular real-time voice AI pipeline (ASR->LLM->TTS) with swappable Whisper/LLM/TTS components, runs locally on GPU

**Verdict: works.** speech-to-speech 1.1.0 on the M4 completed 3/3 speech-in/speech-out turns (Parakeet TDT + Qwen3.5-4B-4bit + Qwen3-TTS 6-bit); isolated LLM prefill 390.546 tok/s at 512 tokens, decode 35.029 tok/s.

**Hardware:** Apple M4 Mac mini

## Measured
| Metric | Value |
|---|---|
| turns completed | 3 of 3 |
| client errors | 0 |
| e2e turn 1 | 56.57 s |
| e2e turn 2 | 31.09 s |
| e2e turn 3 | 4.40 s |
| STT final turn 1 | 1.08 s |
| STT final turn 2 | 0.53 s |
| STT final turn 3 | 0.31 s |
| LLM stage turn 1 | 37.40 s |
| LLM stage turn 2 | 23.22 s |
| LLM stage turn 3 | 3.03 s |
| TTS time to first audio turn 1 | 2.48 s |
| TTS time to first audio turn 2 | 0.31 s |
| TTS time to first audio turn 3 | 0.20 s |
| TTS audio turn 1 | 1.96 s audio in 3.94 s (RTF 0.50) |
| TTS audio turn 2 | 3.79 s audio in 3.25 s (RTF 1.17) |
| TTS audio turn 3 | 4.04 s audio in 2.43 s (RTF 1.66) |
| LLM tokens turn 1 | 359 input tokens, 7 output tokens |
| LLM tokens turn 2 | 383 input tokens, 15 output tokens |
| LLM tokens turn 3 | 411 input tokens, 13 output tokens |
| assistant audio written | 9.788 s, 16 kHz, mono PCM16, 313272 bytes |
| pipeline footprint | 9283 MB |
| pipeline graphics memory | 7359 MB |
| prefill | 390.546 tok/s (512 tokens) |
| decode | 35.029 tok/s (576 tokens) |
| LLM-only peak memory | 3.263 GB |
| server ready | 126.4 s from first log line to Uvicorn, including the weight download |
| weight files kept | 8234150398 bytes |

## Configuration
- prefill: 390.546 tok/s (512 tokens)
- decode: 35.029 tok/s (576 tokens: 512 prompt + 64 generated)
- model_quant: mlx-community/Qwen3.5-4B-4bit, 4-bit affine, group size 64
- kv_cache: bfloat16 KVCache, 576 tokens
- turboquant: no
- speculative: no
- engine: mlx-lm 0.31.3 (mlx 0.32.3) inside speech-to-speech 1.1.0
- hardware: Mac mini M4 (Mac16,10), 16 GB unified memory

## Upstream
- https://github.com/huggingface/speech-to-speech

Upstream code and weights keep their own licence.
