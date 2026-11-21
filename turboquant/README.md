# TurboQuant+

**What it is.** experimental weight-compression mode for LLMs (e.g. shrinks Gemma4 31B from 30.4GB to 18.9GB) plus KV-cache compression

**Verdict: works.** TQ4_1S Config I on Qwen3-1.7B Q8_0 cut weights from 1743.77 MiB to 1221.77 MiB (5.96 BPW) and decoded at 233.33 tok/s on GPU0 (f16 KV, 256 tokens, depth 0). Gemma 4 31B 30.4 GB to 18.9 GB was not measured.

**Hardware:** 1x NVIDIA Tesla V100 32 GB

## Measured
| Metric | Value |
|---|---|
| source_model_size | 1743.77 MiB (8.50 BPW, 1828474880 bytes, Qwen3-1.7B Q8_0) |
| tq4_1s_config_i_model_size | 1221.77 MiB (5.96 BPW, 1281118208 bytes) |
| weight_reduction | 522.00 MiB (29.935% of llama-bench model_size) |
| output_file_bytes | 1287069344 bytes |
| source_file_bytes | 1834426016 bytes |
| quantize_time | 12969.52 ms (wall 13.17 s) |
| prefill_q8_f16kv | 10797.76 tok/s ± 533.23 tok/s (2048 tokens, 6 reps, depth 0) |
| decode_q8_f16kv | 225.60 tok/s ± 0.65 tok/s (256 tokens, depth 0) |
| prefill_tq4_f16kv | 10526.35 tok/s ± 516.84 tok/s (2048 tokens, 6 reps, depth 0) |
| decode_tq4_f16kv | 233.33 tok/s ± 0.35 tok/s (256 tokens, depth 0) |
| prefill_tq4_turbo4v | 9990.32 tok/s ± 482.19 tok/s (2048 tokens, 6 reps, depth 0) |
| decode_tq4_turbo4v | 155.97 tok/s ± 0.27 tok/s (256 tokens, depth 0) |
| gpu0_peak_q8_f16kv | 4012 MiB (baseline 1318 MiB, delta 2694 MiB) |
| gpu0_peak_tq4_f16kv | 3868 MiB (baseline 1318 MiB, delta 2550 MiB) |
| gpu0_peak_tq4_turbo4v | 3740 MiB (baseline 1318 MiB, delta 2422 MiB) |
| prompts_coherent | 3 of 3 on Q8_0 and 3 of 3 on TQ4_1S Config I |
| tq4_1s_tensors | 144 |
| q4_k_tensors | 24 |

## Configuration
- prefill: 10526.35 tok/s TQ4_1S Config I and 10797.76 tok/s Q8_0 (2048 tokens, 6 reps, f16 KV); 9990.32 tok/s with q8_0 K + turbo4 V
- decode: 233.33 tok/s TQ4_1S Config I and 225.60 tok/s Q8_0 (256 tokens, n_depth 0, f16 KV); 155.97 tok/s with turbo4 V
- model_quant: source Q8_0 8.50 BPW; Config I layers 2-25 attn_q/k/v/output + ffn_gate + ffn_up = tq4_1s (144), ffn_down = q4_K (24), layers 0-1 and 26-27 left Q8_0; output 5.96 BPW, 1221.77 MiB. GGUF ftype label remains Q8_0.
- kv_cache: f16 K / f16 V at n_depth 0 for the headline pair (bench does not fill a 2048-token context before decode); third run q8_0 K + turbo4 V
- turboquant: yes
- speculative: no
- engine: TheTom/llama-cpp-turboquant feature/turboquant-kv-cache commit 4185b90, llama-bench, CUDA sm_70
- hardware: our server GPU0 Tesla V100-PCIE-32GB 32768 MiB, CUDA 12.9.86, 8 threads, batch 2048, ubatch 512, flash attention on, n_gpu_layers 99

## Upstream
- https://github.com/TheTom/turboquant_plus/blob/main/docs/getting-started.md#weight-compression-tq4_1s--experimental

Upstream code and weights keep their own licence.
