# dsh-superagent (DeepSeek) on a 64-thread CPU

**What it is.** [deepseek-ai/dsh-superagent-prototype](https://github.com/deepseek-ai/dsh-superagent-prototype) (MIT): DeepSeek's
prototype coding agent for one GitHub repository, packaged as a bundle for DeepSeek Harness (DSH). It watches issues and
mentions, opens a ticket per request, works in its own session and answers with a pull request.

**Verdict: partly.** The code builds and its own test suite passes (1196 of 1197). The live GitHub triage was not run:
it needs a dedicated bot GitHub account, a model provider for DSH and a service that posts on a real repository.

## Hardware and software
| | |
|---|---|
| CPU | x86-64, 64 threads, 755 GB RAM, no GPU visible to the test |
| Software | Node.js 22.23.5, pnpm 11.7.0, commit `8c32a9d` (31/10/2026) |
| Sandbox | bubblewrap: home directory hidden, network only for the clone and the install |

## Measured (14/11/2026)
| Step | Result | Time |
|---|---|---|
| `pnpm install` (234 packages) | ok | 5.7 s |
| `pnpm typecheck` | 0 errors | 14.8 s |
| `pnpm test` (vitest) | 1196 / 1197 tests, 58 / 59 files | 16.0 s |
| `pnpm build` (tsdown) | ok | 4.9 s |
| Whole run | | 46.9 s |

The failing test: `tests/sources.spec.ts > feishu event consumer > ... reports a malformed line without stopping` (the health
state stayed `ready` instead of `error`). On a second, 8-core machine a different single test failed and the build stopped on a
missing optional config loader; the 64-thread run built cleanly.

## Run it
```bash
NODE_DIR=/path/to/node-v22 ./run.sh ./dsh-run     # needs bwrap and Node.js >= 22.19
```
The upstream code is not copied here: `run.sh` clones it at the measured commit. Its licence is the upstream MIT licence.
