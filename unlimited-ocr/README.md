# Unlimited OCR

**What it is.** 3B-param OCR model that parses 100-page PDFs in one pass with 32K context, multilingual

**Verdict: cannot-run.** Official baidu/Unlimited-OCR weights are on disk (6672547120 bytes, BF16) but GPU0 stayed at 1318 MiB held by glide.server pid 64634, which does not release on .gpu0-claim; fn1 was already down and the service was not stopped.

**Hardware:** 1x NVIDIA Tesla V100 32 GB

## Measured
| Metric | Value |
|---|---|
| weight_file_bytes | 6672547120 bytes |
| gpu0_memory_used_after_240s_claim | 1318 MiB |
| glide_process_gpu_memory | 1314 MiB |
| claim_wait | 240 s |
| ocr_pages_run | 0 pages |

