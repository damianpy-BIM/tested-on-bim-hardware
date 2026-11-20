# SentrySearch

**What it is.** Semantic search over long video footage: describe a moment in natural language and get back the matching trimmed clip, using a local 2B model (new MLX backend for Apple Silicon)

**Verdict: works.** Works on GPU0: 3/3 queries saved the correct clip (scores 0.731816, 0.733855, 0.784011); 4-bit Qwen3-VL-Embedding-2B added 2650 MiB and took 59.91 s per 8 s chunk.

**Hardware:** 1x NVIDIA Tesla V100 32 GB

## Measured
| Metric | Value |
|---|---|
| top-1 accuracy | 3/3 queries |
| APPLE top similarity | 0.784011 |
| BOAT top similarity | 0.733855 |
| TRAIN top similarity | 0.731816 |
| unrelated sushi top similarity | 0.366353 |
| chunk embed time | 61.83 s, 56.51 s, 61.40 s |
| mean chunk embed time | 59.91 s per 8 s chunk |
| mean query embed time | 0.605 s |
| index wall time | 218.43 s for 3 files |
| GPU0 memory peak | 4202 MiB |
| GPU0 memory baseline | 1552 MiB |
| embedder memory above baseline | 2650 MiB |
| GPU0 utilization peak | 60% |
| embedding width | 768 |
| weights size | 4271282992 bytes |

## Configuration
- prefill: n/a (embedding model, no generative prefill)
- decode: n/a (embedding model, no generative decode)
- model_quant: Qwen3-VL-Embedding-2B 4-bit bitsandbytes, compute fp16
- kv_cache: n/a, single forward, MRL embedding 768
- turboquant: no
- speculative: no
- engine: sentrysearch 0.1.0 local PyTorch, torch 2.6.0+cu124, transformers 5.23.0
- hardware: Tesla V100-PCIE-32GB GPU0 sm_70, CUDA_VISIBLE_DEVICES=0

