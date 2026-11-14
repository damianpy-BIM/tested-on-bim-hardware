# thermite

**What it is.** 

**Verdict: partly.** Partly: the source, its 3,171-test suite and its own CPU judge benchmark all build and run correctly on this CPU-only host (2.01 / 1.21 / 1.60 GFLOP/s), but the published container compose deployment cannot run here (no Docker/Podman, no sudo) and an agent campaign needs a model endpoint.

**Hardware:** 64-thread x86-64 CPU

## Measured
| Metric | Value |
|---|---|
| test_suite | 3165 of 3171 pass, 3 fail, 3 skip; wall time 12 min 55 s |
| test_failures_cause | 3 failures only from missing host 'zip' binary (spawnSync ENOENT); 4/4 pass in 0.75 s with a throwaway python zip shim on PATH |
| test_parallel_part | 2952 of 2958 pass in 230.7 s |
| test_judge_broker_part | 213 of 213 pass in 533.0 s |
| npm_ci | 14.9 s, 199 packages |
| typecheck | pass in 5.85 s, peak RSS 1.75 GB |
| lint | pass in 0.76 s, 7 warnings, 1894 files |
| build | pass in 4.31 s |
| doctor | exit 1 in 0.67 s: fails on container engine and NVIDIA container toolkit; OK on port 8800, 226 GB free disk, clock synced, GPU driver listed |
| dashboard_demo | HTTP ready in 3.60 s; RSS about 200 MB; GET /ui 200 (185,283 bytes); GET /v1/health 200; GET /v1/leaderboard 200 (654 bytes) |
| smoke_bench_small | 2.01 GFLOP/s (median 0.50 s wall, 3 timed runs, RSS 1.5 MB) |
| smoke_bench_large | 1.21 GFLOP/s (median 1.11 s wall, 3 timed runs, RSS 2.0 MB) |
| smoke_bench_held | 1.60 GFLOP/s (median 0.53 s wall, 3 timed runs, RSS 2.0 MB) |
| smoke_bench_check | pass=true on 3/3 cells; max absolute error vs float64 reference 1.42e-6 (small) and 4.46e-6 (large); dispatch probe ref_calls=0 |

## Configuration
- prefill: n/a (no LLM run in this test)
- decode: n/a (no LLM run in this test)
- model_quant: n/a (no model)
- kv_cache: n/a (no model)
- turboquant: no
- speculative: no
- engine: Node.js 22.23.5 + TypeScript 7.0.2 (node --experimental-strip-types); C judge bench via cc -O2 -std=c11; no container engine
- hardware: our server, 64 threads, 755 GB RAM, CPU only (CUDA_VISIBLE_DEVICES empty; GPUs 0-9 not allocated to this test)

## Upstream
- https://github.com/iammrduncan/thermite

Upstream code and weights keep their own licence.
