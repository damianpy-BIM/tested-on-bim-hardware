# Lightpanda

**What it is.** headless browser written in Zig, built for AI agents/scraping, faster and lighter than Chrome

**Verdict: works.** Lightpanda 1.1.0 nightly on our server CPU fetched a JS page, extracted product text after XHR, and answered an MCP run call; no GPU (no render engine, no CUDA).

**Hardware:** CPU only, on the NVIDIA Tesla V100 server

## Measured
| Metric | Value |
|---|---|
| binary_size | 76473672 bytes (72.93 MiB) |
| binary_version | 1.1.0-nightly.12329+0eb33c8c9 |
| source_commit | f3a9e6abbdc8be98e4c27a679984faa3b9a9a70d |
| local_html_dump_wall_time | 0.03 s |
| local_html_dump_peak_rss | 21504 KiB (21.00 MiB) |
| local_markdown_dump_wall_time | 0.03 s |
| local_markdown_dump_peak_rss | 21504 KiB (21.00 MiB) |
| local_png_dump_wall_time | 0.05 s |
| local_png_dump_peak_rss | 26112 KiB (25.50 MiB) |
| local_png_size | 10853 bytes, 1920x228 |
| local_pandascript_wall_time | 0.04 s |
| local_pandascript_peak_rss | 25048 KiB (24.46 MiB) |
| example_com_markdown_wall_time | 0.10 s |
| example_com_peak_rss | 24064 KiB (23.50 MiB) |
| example_com_markdown_size | 1344 bytes |
| campfire_load_only_wall_time | 0.32 s |
| campfire_load_only_peak_rss | 23040 KiB (22.50 MiB) |
| campfire_load_only_markdown_size | 1362 bytes |
| campfire_after_xhr_wall_time | 0.44 s |
| campfire_after_xhr_peak_rss | 24020 KiB (23.46 MiB) |
| campfire_after_xhr_markdown_size | 4312 bytes |
| campfire_product_price | 244.99 USD (page text $244.99) |
| hn_markdown_wall_time | 0.90 s |
| hn_peak_rss | 23552 KiB (23.00 MiB) |
| hn_markdown_size | 19486 bytes |
| hn_external_story_links | 29 links |
| mcp_run_tool | HTTP 200, isError false, same extract as PandaScript |
| gpu | not used (0 MiB claimed; GPU0 claim file absent) |

## Configuration
- prefill: n/a (not an LLM)
- decode: n/a (not an LLM)
- model_quant: n/a (not an LLM)
- kv_cache: n/a, n/a
- turboquant: no
- speculative: no
- engine: Lightpanda 1.1.0-nightly.12329+0eb33c8c9 official x86_64-linux binary (V8, libcurl). Telemetry off via LIGHTPANDA_DISABLE_TELEMETRY=true.
- hardware: our server CPU, 64 threads, host 755 GiB RAM. Process had no GPU (CUDA_VISIBLE_DEVICES unset, GPU0 not claimed).

## Upstream
- https://github.com/lightpanda-io/browser

Upstream code and weights keep their own licence.
