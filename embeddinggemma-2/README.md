# EmbeddingGemma 2

**What it is.** Google's small open embedding model for local semantic search/RAG, runs in ~0.5GB RAM

**Verdict: works.** EmbeddingGemma 2 text-only (271002624 parameters, float32, 8 CPU threads) ranked 3/3 short queries first at 768 dimensions; 833.25 tok/s on a 505-token document, 2146.1 MiB RSS, 0 MiB VRAM.

**Hardware:** 1x NVIDIA Tesla V100 32 GB

## Measured
| Metric | Value |
|---|---|
| embedding_dimension | 768 |
| parameters | 271002624 |
| load_time | 4.164 s |
| document_batch_throughput | 488.47 tok/s (176 tokens, 6 documents, 0.3603 s) |
| query_batch_throughput | 323.07 tok/s (50 tokens, 3 queries, 0.1548 s) |
| long_document_throughput | 833.25 tok/s (505 tokens, 0.6061 s) |
| rss_after_load | 2136.7 MiB |
| rss_after_encode | 2146.1 MiB |
| vram_used_by_this_test | 0 MiB |
| cosine_aurora_query | 0.8066 (second 0.5763, margin 0.2302) |
| cosine_python_query | 0.8293 (second 0.5496, margin 0.2797) |
| cosine_invoice_query | 0.7802 (second 0.5721, margin 0.2081) |
| ranking | 3 of 3 correct |
| vector_l2_norm | 1.0 |

## Configuration
- prefill: 833.25 tok/s (505 tokens, one document, embedding forward)
- decode: 0 tok/s (embedding model, no token generation)
- model_quant: BF16 safetensors on disk (1488915288 bytes), inference float32
- kv_cache: none, single forward, model context window 8192 tokens
- turboquant: no
- speculative: no
- engine: sentence-transformers 6.3.0 + transformers 5.23.0 + torch 2.14.1+cu130, eager attention, text encoders only
- hardware: our server CPU, 8 threads, CUDA_VISIBLE_DEVICES empty; GPU0 left to glide-decide (1318 MiB used by that service)

