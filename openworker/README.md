# OpenWorker

**What it is.** Desktop AI coworker that runs locally and produces finished documents (e.g. security reviews, incident reports) instead of chat replies

**Verdict: partly.** OpenWorker 0.3.4 wrote 3 markdown drafts through llama.cpp Qwen3.5-9B Q4_K_M on CPU (prefill 41.89 tok/s at 5139 tokens, decode 5.31 tok/s over 1682 tokens, context 16384, KV f16, VRAM 0 MiB). The security review matched the sample bugs. The incident report repeated the sample key, and both narrative drafts invented remediations. No GPU: the harness has no CUDA dependency, and GPU0 stayed at 8748 MiB under other tests plus glide-decide.service.

**Hardware:** CPU only, on the NVIDIA Tesla V100 server

## Measured
| Metric | Value |
|---|---|
| prefill | 41.89 tok/s (5139 tokens, one call, llama.cpp slot task 47) |
| prefill_weighted | 41.26 tok/s (7236 tokens across 12 calls, warmup task 0 excluded) |
| decode | 5.31 tok/s (1682 tokens across 12 calls, context 16384, warmup task 0 excluded) |
| decode_warmup_excluded | 1.42 tok/s (44 tokens, task 0, not used) |
| context_window | 16384 tokens |
| kv_cache | f16, 16384 tokens, 1 slot, kv_unified false (llama.cpp default; --cache-type-k/v not set) |
| vram_this_test | 0 MiB |
| gpu0_memory_used_at_check | 8748 MiB (other processes, not this test) |
| threads | 24 of 64 |
| model_file | 5680522464 bytes (5.681 GB), Q4_K_M, already on disk, not downloaded by this test |
| wall_p1_incident | 234.1 s |
| wall_p2_review | 112.2 s |
| wall_p3_note | 158.8 s |
| wall_sum | 505.1 s |
| tokens_in_p1 | 5414 tokens |
| tokens_out_p1 | 530 tokens |
| cache_read_p1 | 11041 tokens |
| tokens_in_p2 | 522 tokens |
| tokens_out_p2 | 497 tokens |
| cache_read_p2 | 15915 tokens |
| tokens_in_p3 | 1300 tokens |
| tokens_out_p3 | 655 tokens |
| cache_read_p3 | 34988 tokens |
| tokens_in_sum | 7236 tokens |
| tokens_out_sum | 1682 tokens |
| cache_read_sum | 61944 tokens |
| runs_completed | 3 of 3 |
| tool_calls_denied | 0 |
| tool_calls_error | 0 |
| incident_report | 239 words, 1751 bytes |
| security_review | 220 words, 1542 bytes |
| public_note | 220 words, 1414 bytes (asked 150 words) |
| app_py_sha256 | 5baea5cc66036e816ebdfad6e740230b4e2f02df5b2db63780ebd6fc7455bca5 (unchanged, 486 bytes) |
| cost | 0 USD |

## Configuration
- prefill: 41.89 tok/s (5139 tokens)
- decode: 5.31 tok/s (16384 context, 1682 generated tokens)
- model_quant: Q4_K_M
- kv_cache: f16, 16384 tokens
- turboquant: no
- speculative: no
- engine: OpenWorker 0.3.4 git 7f7d638 + llama.cpp 0.9.0-dev build 55 commit 5851a8e50
- hardware: our server CPU, 24 of 64 threads, CUDA_VISIBLE_DEVICES empty, -ngl 0 --no-op-offload, VRAM 0 MiB, NVIDIA driver 580.178.04 present but not used

## Upstream
- https://github.com/andrewyng/openworker

Upstream code and weights keep their own licence.
