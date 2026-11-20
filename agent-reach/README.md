# Agent-Reach

**What it is.** CLI tool that gives AI agents web scraping and search capabilities across Twitter, Reddit, YouTube, GitHub, Bilibili, XiaoHongShu without API fees

**Verdict: works.** Agent-Reach 1.6.1 installs from GitHub in 26 s on CPU, and every key-free default channel command (GitHub search/read, YouTube search, web search, URL read) returned real structured JSON in 1.1-2.1 s; repo's own 608 tests all pass — useful as a zero-key web-reading layer for BIM's agents.

**Hardware:** CPU only, on the NVIDIA Tesla V100 server

## Measured
| Metric | Value |
|---|---|
| clean install time | 26.1 s (venv + pip + deps + version smoke, CPU) |
| github search latency | 1.90 s wall for 3 results (tool-reported 1655 ms), 3/3 relevant |
| github repo read latency | 1.73 s wall, full README in one JSON item (tool-reported 1456 ms) |
| youtube search latency | 2.09 s wall for 3 results, yt-dlp backend (tool-reported 1846 ms) |
| web search latency | 1.08 s wall for 3 results, exa backend, mixed title quality (tool-reported 849 ms) |
| url read latency | 1.55 s wall, auto channel selection, 9,417-char README text (tool-reported 1278 ms) |
| repo test suite | 608 passed, 0 failed in 43.5 s |
| peak memory per command | 31.7 MB RSS |
| disk footprint | 4.0 MB repo + 154 MB venv |
| gpu needed | none (no torch/CUDA in dependencies; GPU0 never claimed) |

## Configuration
- prefill: n/a (no LLM inference in this tool)
- decode: n/a (no LLM inference in this tool)
- model_quant: n/a (no model)
- kv_cache: n/a
- turboquant: no
- speculative: no
- engine: Python 3.12 CLI v1.6.1 (requests 2.32.5, loguru 0.7.3, PyYAML 6.0.3, yt-dlp 2026.8.19)
- hardware: our server CPU (64 threads, 755 GB RAM), no GPU required

## Upstream
- https://github.com/Panniantong/Agent-Reach

Upstream code and weights keep their own licence.
