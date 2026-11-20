# Gortex

**What it is.** Code graph indexer exposed via CLI/MCP/web UI to cut AI coding agent token usage

**Verdict: works.** Gortex v0.64.11 indexed 4 Python files into 16 nodes and 23 edges on the v100 CPU, CLI and MCP both returned tax_cents, and the 50x token claim was not measured.

**Hardware:** CPU only, on the NVIDIA Tesla V100 server

## Measured
| Metric | Value |
|---|---|
| version | v0.64.11+c7abb9b9 |
| binary_size | 319493880 bytes |
| index_files | 4 files |
| index_nodes | 16 nodes |
| index_edges | 23 edges |
| index_settle_time | 1.0 s |
| warmup_time | 1926 ms |
| track_wall_time | 9.82 s |
| daemon_rss | 158236 KiB |
| store_db_size | 668.0 KiB |
| store_wal_size | 197.2 KiB |
| cli_stats_wall_time | 0.09 s |
| cli_symbol_wall_time | 0.25 s |
| cli_callers_wall_time | 0.09 s |
| cli_dependents_by_id_wall_time | 0.09 s |
| cli_symbol_hits | 1 hit |
| cli_dependents_depth3_nodes | 4 nodes |
| cli_dependents_depth3_edges | 3 edges |
| mcp_initialize_time | 0.0969 s |
| mcp_tools_list_time | 0.0275 s |
| mcp_tools_listed | 145 tools |
| mcp_graph_stats_time | 0.0045 s |
| mcp_search_symbols_time | 0.0061 s |
| mcp_search_hits | 1 hit |
| tool_tokens_saved | 0 tokens |
| tool_tokens_returned | 1975 tokens |
| gpu_vram | 0 MiB |

## Configuration
- prefill: n/a (not an LLM)
- decode: n/a (not an LLM)
- model_quant: n/a (static Go binary, no model)
- kv_cache: n/a, no LLM context
- turboquant: no
- speculative: no
- engine: gortex v0.64.11+c7abb9b9, SQLite graph, MCP stdio newline JSON
- hardware: our server CPU (64 threads, 755 GB RAM). GPU not used: README and install docs are a static CPU binary with no CUDA, torch, vLLM, or llama.cpp.

