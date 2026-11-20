# RMUX

**What it is.** Rust terminal multiplexer, tmux-compatible, keeps SSH sessions alive, with SDK for AI agent orchestration

**Verdict: works.** RMUX 0.10.0 works on the CPU: the session kept running after the SSH client was killed, and tmux-style commands succeeded. No GPU was needed.

**Hardware:** CPU only, on the NVIDIA Tesla V100 server

## Measured
| Metric | Value |
|---|---|
| tmux-compatible commands listed | 90 commands |
| new-session over SSH | 333.8 ms |
| reconnect check over SSH | 330.9 ms |
| list-sessions median over SSH (5 samples) | 322.7 ms |
| capture-pane median over SSH (5 samples) | 316.5 ms |
| list-commands median over SSH (5 samples) | 327.7 ms |
| list-sessions median inside the container (7 samples) | 4 ms |
| capture-pane median inside the container (7 samples) | 3 ms |
| has-session median inside the container (7 samples) | 3 ms |
| ticks written after SSH client kill | 6 ticks |
| tick interval | 0.4 s |
| installed prefix size | 36664087 bytes |
| release tarball size | 16253094 bytes |
| tiny CLI size | 2913776 bytes |
| daemon size | 15152272 bytes |
| full CLI helper size | 18114464 bytes |
| GPU memory used by this test | 0 MiB |

## Configuration
- prefill: n/a (not an LLM)
- decode: n/a (not an LLM)
- model_quant: n/a (not a weight)
- kv_cache: n/a, n/a
- turboquant: no
- speculative: no
- engine: RMUX 0.10.0 CLI + rmux-daemon, tag v0.10.0, commit dfd68c774ca0f4212139a21d37d09c90f75f8bd7
- hardware: our server CPU, 64 threads, 755 GB RAM; GPU0 not used (no CUDA, torch, vLLM, llama.cpp, or ROCm in the project)

