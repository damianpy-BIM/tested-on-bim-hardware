# Claude Code

**What it is.** Anthropic's CLI coding agent for automated software development

**Verdict: works.** Claude Code 2.1.329 CLI installs and runs unmodified on our server CPU with no GPU needed — version check, headless prompts and real Bash/Write tool-use agent loops all passed against the fleet's local Anthropic-compatible endpoint; it is exactly the agent engine our fleet already uses.

**Hardware:** CPU only, on the NVIDIA Tesla V100 server

## Measured
| Metric | Value |
|---|---|
| claude --version | 2.1.329 (Claude Code) |
| install time (official npm) | 6.1 s |
| install size | 377,757,087 bytes (361 MB, native client binary; no model weights) |
| version-check startup | 0.01 s wall |
| CLI memory | 23 MB peak RSS (--version) |
| headless prompt 'Reply with exactly: LAB_OK' | exact match, 2.16 s wall / 2.04 s API, 18 output tokens, 8.8 tok/s |
| agent Bash-tool test (nproc) | correct answer 64, 2 turns, 7.24 s wall / 7.07 s API, 68 output tokens, 9.6 tok/s |
| agent Write-tool test (7x6 to answer.txt) | correct answer 42, file verified on disk, 3 turns, 14.60 s wall / 14.29 s API, 307 output tokens, 21.5 tok/s |
| CLI CPU overhead per run (wall minus API time) | 0.12-0.31 s |
| system prompt per turn | 11,705 tokens, served from server prompt-cache (cache_read hit), 0 thinking tokens |
| reported context window (local endpoint) | 1,000,000 tokens in / 32,000 tokens max out |
| GPU used | none (pure client, needs_cuda=false) |

## Configuration
- prefill: not separable from CLI-side timing (11,705-token system prompt served from server prompt-cache, cache_read=11,705 tok)
- decode: 9.6 tok/s (2-turn tool loop, 68 output tokens); 8.8 tok/s on the 18-token prompt, 21.5 tok/s on the 307-token task — end-to-end through CLI incl. server contention
- model_quant: IQ3_S (qwen3.8-flash-next-iq3_s, per model name; client-side n/a — Claude Code ships no weights)
- kv_cache: server-side; 1,000,000-token context, ephemeral prompt cache active (11,705 tok cached)
- turboquant: no
- speculative: no (server-side, not visible from the CLI)
- engine: claude-code 2.1.329 native Bun binary (npm @anthropic-ai/claude-code) -> lq Anthropic-compatible proxy at localhost:8095
- hardware: our server CPU (64 threads, 755 GB RAM); GPU0 untouched — client process needs no GPU (23 MB RSS, no CUDA/torch/vLLM in the project)

## Upstream
- https://github.com/anthropics/claude-code

Upstream code and weights keep their own licence.
