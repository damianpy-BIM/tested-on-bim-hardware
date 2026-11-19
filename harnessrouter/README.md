# HarnessRouter

**What it is.** Open-source infrastructure layer that standardizes routing and execution of tasks across multiple AI agent harnesses via a Unified Harness Protocol

**Verdict: works.** HarnessRouter 0.41.23 installed rootless (no sudo, no cost, no account) and really routed agent tasks to three different coding agents (fast-agent, aider, vibe) behind a free local CPU model: file artifacts verified, streaming, cancellation and session continuity all worked, and it passed 41/41 of its own UHP core conformance suite; tasks are slow only because the CPU-only 4B model I plugged in decodes 1–11 tok/s under the node's 72–100 load.

**Hardware:** CPU only, on the NVIDIA Tesla V100 server

## Measured
| Metric | Value |
|---|---|
| fast-agent smoke task time | 67.8 s (1811 input / 3 output tokens) |
| aider smoke task time | 120.5 s (3118 input / 3 output tokens) |
| vibe file-writing task time | 818.7 s, 13 min 39 s (9498 input / 114 output tokens) |
| fast-agent file-writing tool task time | 181.2 s (wrote notes.md with verified content "7 * 11 = 77") |
| session-continuation turn time | 20.2 s (1816 tokens reported as cache_read) |
| SSE streaming | 52 data events in 64.6 s, live deltas |
| cancellation | background task reported cancelled within 20 s of the cancel call |
| UHP core conformance, harness registered | 41 passed / 41 checks, 0 failed, 0 skipped (CONFORMANT, suite ran real agent tasks) |
| UHP core conformance, no harness registered | 16 passed / 41, 25 skipped, 0 failed |
| UHP full-class conformance, minimal CPU install | 40 passed / 111, 18 failed (environmental: codex CLI absent, checks before harness registration, runner environment 502), 53 skipped |
| container image size | 1.98 GB |
| container steady-state RAM | ≈200 MB |
| catalogue models marked available | 24 / 1536 |
| conformance suite duration (core, registered) | 4 min 39 s wall |

## Configuration
- prefill: 26.33 tok/s (556-token prompt, node load ≈75); 48.39 tok/s (27-token prompt, load ≈72)
- decode: 1.07 tok/s (587-token context, load ≈75); 11.48 tok/s (91-token context, load ≈72)
- model_quant: Q4_K_M GGUF (Huihui-Qwen3-VL-4B-Instruct-abliterated, 4.02 B params)
- kv_cache: llama.cpp default f16, 16384-token context
- turboquant: no
- speculative: no
- engine: llama.cpp llama-server, CPU backend (-ngl 0, -t 16, --jinja, -fa on, thinking disabled) as BYOK provider; HarnessRouter Community Edition 0.41.23 gateway+runner in one rootless-podman container (console localhost:3105)
- hardware: our server, CPU only (CUDA_VISIBLE_DEVICES unset; 64 threads, shared node load 72–100 during the test)

