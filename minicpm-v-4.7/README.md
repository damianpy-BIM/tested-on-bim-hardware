# MiniCPM-V 4.7

**What it is.** 35B-A3B MoE multimodal (vision-language) model for document parsing, sign reading, visual reasoning, with a 1B lightweight variant for edge devices

**Verdict: works.** MiniCPM-V 4.7 35B-A3B IQ3_M reads a sign, an invoice, and a loading rule exactly on one V100 at 98.25 tok/s decode.

**Hardware:** 1x NVIDIA Tesla V100 32 GB

## Measured
| Metric | Value |
|---|---|
| prefill_pp512_tok_per_s | 763.11 tok/s ± 10.34 tok/s |
| decode_tg128_tok_per_s | 98.25 tok/s ± 1.33 tok/s |
| bench_context | 640 tokens |
| model_size | 14.37 GiB |
| parameter_count | 34.66 B |
| weight_bytes | 15440064448 bytes |
| mmproj_bytes | 1119575840 bytes |
| gpu0_peak | 17074 MiB |
| image_encode_sign | 420 ms |
| image_encode_invoice | 394 ms |
| image_encode_loading | 270 ms |
| vision_prompt_tokens_sign | 325 tokens |
| vision_prompt_tokens_invoice | 325 tokens |
| vision_prompt_tokens_loading | 199 tokens |
| vision_decode_sign | 76.23 tok/s |
| vision_decode_invoice | 82.87 tok/s |
| vision_decode_loading | 81.09 tok/s |
| sign_lines_correct | 5 of 5 |
| invoice_fields_correct | 6 of 6 |
| loading_answer | No |

## Configuration
- prefill: 763.11 tok/s ± 10.34 tok/s (512 prompt tokens)
- decode: 98.25 tok/s ± 1.33 tok/s (128 generated tokens, n_ctx 640)
- model_quant: IQ3_M filename; llama-bench IQ3_S mix, 3.66 bpw; GGUF file_type 27
- kv_cache: f16, 640 tokens
- turboquant: no
- speculative: no
- engine: llama.cpp 5851a8e50 (0.9.0-dev build 55), CUDA 12.9 V12.9.86
- hardware: 1x Tesla V100-PCIE-32GB sm_70, GPU0, ngl 99, threads 16, batch 2048, ubatch 512, flash attention on

## Upstream
- https://huggingface.co/openbmb

Upstream code and weights keep their own licence.
