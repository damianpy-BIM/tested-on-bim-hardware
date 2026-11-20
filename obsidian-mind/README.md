# Obsidian Mind

**What it is.** Gives AI coding agents (Claude Code, Codex CLI, Gemini CLI) persistent memory via a local Obsidian vault

**Verdict: works.** Obsidian Mind hooks and MCP remember/recall work on CPU: 2233 tests passed, a 755-byte note written in 179 ms was recalled in 6 ms by a new process, and the next SessionStart listed it.

**Hardware:** CPU only, on the NVIDIA Tesla V100 server

## Measured
| Metric | Value |
|---|---|
| npm_test_passed | 2233 tests |
| npm_test_failed | 0 tests |
| npm_test_skipped | 19 tests |
| npm_test_duration | 21.68 s |
| claude_session_start_1 | 423 ms |
| codex_session_start_hook | 370 ms |
| claude_session_start_2 | 380 ms |
| remember_time | 179 ms |
| recall_time | 6 ms |
| memory_note_size | 755 bytes |
| session1_injected_context | 1.7 kB |
| session2_injected_context | 2.4 kB |
| injection_budget | 9.0 kB |

## Configuration
- prefill: n/a (not an LLM run)
- decode: n/a (not an LLM run)
- model_quant: none (markdown vault, no model loaded)
- kv_cache: none, 0 tokens
- turboquant: no
- speculative: no
- engine: Node v22.23.5 --experimental-strip-types hooks + om MCP (Claude Code 2.1.283 plugin validate)
- hardware: our server CPU, 64 threads, 755 GB RAM; GPU0 not used because the hook path has no CUDA requirement

## Upstream
- https://github.com/breferrari/obsidian-mind

Upstream code and weights keep their own licence.
