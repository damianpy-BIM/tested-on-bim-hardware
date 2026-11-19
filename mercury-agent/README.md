# Mercury Agent

**What it is.** Multi-agent orchestration framework with bot coordination, sandboxing, and background task execution

**Verdict: works.** Mercury Agent v1.5.4 installed clean, ran a lead bot + 2 crew bots through 3 end-to-end pipelines, and survived both a graceful restart (1.17 s) and a kill -9 mid-run — the queued job was re-claimed after restart and finished on its own.

**Hardware:** CPU only, on the NVIDIA Tesla V100 server

## Measured
| Metric | Value |
|---|---|
| install | ~40 s, 114 MB binary (sha256-verified, smoke test passed) |
| daemon_restart_graceful | 1.17 s (fleet 3/3, journals, deliverables, device token all intact) |
| restart_after_sigkill | 0.77 s to relaunch; queued job auto re-claimed ~1 s later and completed; DLQ 0, needsYou false |
| daemon_idle_ram | 114 MB RSS (state dir 1.1 MB, queue.db 36 KB) |
| fleet_create | 3 API calls (lead + 2 crew), ~50 ms total |
| pipeline_e2e | 3 min 31 s clean post-restart run (4 bot turns, incl. ~2 min owner-approval wait) |
| bot_turns | lead dispatch 58-78 s / lead wake 24-26 s / crew stage 30-61 s (turns without approval waits) |
| tokens_per_run | ~84k in / ~1.7k out per pipeline run (peak 5.2-6.3k input per turn, system prompt re-sent each step) |
| quality | 3/3 tasks produced instruction-faithful deliverables (exact bullet count, word limit); haikus demonstrably chained from stage-1 notes via {{previous}} handoff |
| restart_survival | fleet 3/3 bots, journal 11/11 rows, deliverables 7/7 files intact; queued run survived kill -9 and completed; one in-flight wake-up turn lost only its journal row (deliverable already on disk) |
| approval_gate | 3/3 runs parked on owner-approval when crew read a file outside its self-scope; approvals API answered them; approval requests survived the restart |

## Configuration
- prefill: 120.3 tok/s (306-token prompt)
- decode: 30.0 tok/s (ctx ~300, MTP speculative: draft 15, accepted 12, --spec 4)
- model_quant: Qwen3.8-Flash-Next-GSQ-RCO-abliterated IQ3_S GGUF
- kv_cache: int8, 262144 ctx
- turboquant: no
- speculative: MTP (--spec 4, draft 15 accepted 12)
- engine: strata serve.server (OpenAI-compatible) behind lq proxy localhost:8095 -> :8422; Mercury provider = openaiCompat
- hardware: our server, CPU slot (64 threads) — no GPU needed and none claimed: Mercury is an orchestrator daemon that downloads no weights and runs no inference; all LLM calls went to the pre-existing model server on production GPU5, untouched

