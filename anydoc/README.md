# anydoc

**What it is.** Rust CLI/library converting 14 doc formats (docx, pptx, xlsx, PDF, epub, rtf...) to GitHub-Flavored Markdown locally, no ML/cloud

**Verdict: works.** anydoc 0.2.5 converts 14 office formats to GFM on CPU; 60/60 fixture snapshots match; malformed, encrypted, and scanned PDFs fail with a category.

**Hardware:** CPU only, on the NVIDIA Tesla V100 server

## Measured
| Metric | Value |
|---|---|
| docx warm median (10159 B, 50 calls) | 4.271 ms |
| pptx warm median (15734 B, 50 calls) | 3.724 ms |
| pdf text warm median (90060 B, 50 calls) | 22.911 ms |
| xlsx warm median (7106 B, 50 calls) | 2.321 ms |
| csv warm median (210 B, 50 calls) | 0.718 ms |
| doc warm median (20480 B, 50 calls) | 1.186 ms |
| rtf warm median (20136 B, 50 calls) | 3.362 ms |
| epub warm median (6167 B, 50 calls) | 1.438 ms |
| docx x500 wall (same 10159 B file) | 1051.973 ms |
| docx x500 per document | 2.104 ms |
| fixture one-pass conversion sum (66 files) | 1193.493 ms |
| fixtures converted | 60 files |
| fixtures failed as designed | 6 files |
| markdown snapshot matches | 60 of 60 files |
| snapshot mismatches | 0 files |
| cli docx wall including node start | 64.178 ms |
| cli pptx wall including node start | 76.568 ms |
| cli pdf wall including node start | 84.396 ms |
| fake docx (JSON bytes) exit | 1 |
| scanned pdf exit | 3 |
| encrypted odt exit | 1 |
| native addon size | 7.9 MB |
| vram used | 0 MiB |

## Configuration
- prefill: n/a (not an LLM)
- decode: n/a (not an LLM)
- model_quant: none (no model weights)
- kv_cache: none, n/a
- turboquant: no
- speculative: no
- engine: @firecrawl/anydoc 0.2.5 NAPI linux-x64-gnu, Node v22.23.5
- hardware: our server CPU, 64 threads, 755 GB RAM, no GPU (no CUDA in the project)

## Upstream
- https://github.com/firecrawl/anydoc

Upstream code and weights keep their own licence.
