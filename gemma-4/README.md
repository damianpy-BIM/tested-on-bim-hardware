# Gemma 4

**What it is.** A local AI model the post suggests running for sensitive company data.

**Verdict: works.** Gemma 4 12B (official QAT Q4_0 GGUF) loads and generates on our server GPU0 at 1682.6 tok/s prefill and 69.6 tok/s decode (142.8 tok/s with the MTP head) using 8.2 GB VRAM, with all 3 quality prompts correct — useful for BIM.

**Hardware:** 1x NVIDIA Tesla V100 32 GB

## Measured
| Metric | Value |
|---|---|
| prefill_speed | 1682.56 ± 3.33 tok/s (llama-bench pp2048, 2048-token prompt, FA on, -ngl 99) |
| decode_speed | 69.60 ± 0.15 tok/s (llama-bench tg128 after 2048-token prefill, FA on, -ngl 99) |
| decode_speed_quality_runs | 62.6-64.3 tok/s (llama-cli, temp 0.2, ctx 8192, short prompts; short-prompt prefill 226-359 tok/s) |
| decode_speed_mtp_speculative | 142.8 tok/s (same Q1 prompt, -n 700, temp 0.2, ctx 8192, official MTP Q4_0 head 253.7 MB via --spec-type draft-mtp; 2.3x the 62.6 tok/s baseline; answer still correct) |
| vram_peak_gpu0 | 8204 MiB (ctx 8192, f16 KV cache, -ngl 99, 2 s sampling) |
| model_size_on_disk | 6.98 GB (6,975,879,296 bytes) GGUF QAT Q4_0, 11.91 B params |
| wall_time_per_generation_run | approx 10 s incl. model load (warm page cache); approx 12 s incl. MTP draft load |
| quality_prompts_passed | 3/3 (Q1 arithmetic correct: 1,367 EUR total, 59.43 EUR average; Q2 JSON valid with 5/5 keys, machine-verified; Q3 48-word constrained text, no banned words) |

## Configuration
- prefill: 1682.56 tok/s (2048-token prompt, llama-bench pp2048, FA on)
- decode: 69.60 tok/s (2048-token context, llama-bench tg128, FA on); 142.8 tok/s with MTP speculative decoding (ctx 8192, quality-run context)
- model_quant: google/gemma-4-12B-it-qat-q4_0-gguf, QAT Q4_0, 6.98 GB, 11.91 B params, Apache 2.0
- kv_cache: f16 (default), 8192 tokens, FA on
- turboquant: no
- speculative: MTP (official ggml-org MTP head Q4_0, 253.7 MB, --spec-type draft-mtp, n_max 3 default; non-QAT head on QAT target per Google card caveat)
- engine: llama.cpp v0.9.0-dev build 55 (commit 5851a8e50), CUDA backend, -ngl 99, -fa on, --jinja
- hardware: our server GPU0, NVIDIA V100 32 GB (sm_70, FP16/GGUF, CUDA 12.9), all layers in VRAM, RAM offload not needed

