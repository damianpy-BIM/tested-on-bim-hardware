# Mission Control

**What it is.** self-hosted local dashboard for delegating, prioritizing and supervising tasks across AI agents

**Verdict: works.** Local Next.js dashboard tracks one task assigned to researcher through Done, inbox, and activity. Not a fleet control layer.

**Hardware:** CPU only, on the NVIDIA Tesla V100 server

## Measured
| Metric | Value |
|---|---|
| server_ready | 2.6 s |
| first_page_compile | 14.5 s |
| task_create | 1142.1 ms |
| kanban_in_progress_update | 75.0 ms |
| kanban_done_update | 269.6 ms |
| dashboard_warm_median | 59.7 ms |
| tasks_list_warm_median | 53.6 ms |
| page_warm_median | 294.0 ms |
| next_server_rss | 2017.8 MiB |
| create_to_completed | 2.509 s |
| gpu_memory_used | 0 MiB |

## Configuration
- prefill: not an LLM
- decode: not an LLM
- model_quant: none
- kv_cache: none
- turboquant: no
- speculative: no
- engine: Next.js 15.5.12, Node.js 22.23.5
- hardware: CPU only, 64 threads, 755 GB RAM, no GPU used

