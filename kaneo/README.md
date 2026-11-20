# Kaneo

**What it is.** self-hosted minimal project management tool (Docker Compose + PostgreSQL)

**Verdict: works.** Kaneo v2.50.0 on CPU created a project and the task Measure the board (still present after reload); idle RSS 215.2 MB; no GPU.

**Hardware:** CPU only, on the NVIDIA Tesla V100 server

## Measured
| Metric | Value |
|---|---|
| api_health | HTTP 200, body {"status":"ok"} |
| image_pull_time | 77.68 s |
| compose_up_wall_time | 192.26 s |
| signup_page_load_time | 1.232 s |
| signup_to_onboarding_time | 1.010 s |
| project_create_time | 2.357 s |
| task_create_time | 1.403 s |
| ui_script_wall_time | 12.40 s |
| tasks_on_board_after_reload | 6 tasks |
| kaneo_idle_rss | 215.2 MB |
| kaneo_idle_cpu_sample | 15.88% |
| postgres_idle_rss | 9.368 MB |
| postgres_idle_cpu_sample | 1.65% |
| kaneo_image_size | 495728282 bytes (472.77 MiB) |
| postgres_image_size | 297476938 bytes (283.69 MiB) |
| home_document | 6748 bytes in 0.001919 s |
| gpu_memory_used_by_test | 0 MiB |
| app_version_in_ui | v2.50.0 |

## Configuration
- prefill: not measured (not an LLM, 0 tokens)
- decode: not measured (not an LLM, 0 tokens)
- model_quant: none (no model weights)
- kv_cache: none, 0 tokens
- turboquant: no
- speculative: no
- engine: ghcr.io/usekaneo/kaneo:latest UI v2.50.0 + postgres:16-alpine via podman 4.9.3 and podman-compose 1.6.0
- hardware: our server CPU, 64 threads, 755 GiB RAM, GPU not used

## Upstream
- https://github.com/usekaneo/kaneo

Upstream code and weights keep their own licence.
