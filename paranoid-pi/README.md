# paranoid-pi

**What it is.** Privacy-focused LLM daemon wrapper with Tor circuits, cover traffic, zkAPI, and local prompt rewriting

**Verdict: partly.** Partly works: the zkAPI privacy daemon builds clean and its per-conversation Tor circuit isolation is verified live (3 SOCKS identities -> 3 distinct exit IPs), but OpenAI-compatible chat is unusable today - both networks' vault manifests are not_deployed and chat needs a funded ETH note - and the documented local rewrite model runs at 2.29 tok/s on CPU, so every rewrite exceeds the 90 s budget and fails closed.

**Hardware:** CPU only, on the NVIDIA Tesla V100 server

## Measured
| Metric | Value |
|---|---|
| build | OK with Go 1.26.11; binary 15.5 MB (15,494,304 bytes); commit 0fb263b (branch feat/client-concession-local) |
| race_suite | 8/8 packages pass under go test -race, 0 data races; internal/zkapi took 788.1 s and needs -timeout 30m (first run hit the default 10-min timeout wall, not a hang or race) |
| tor_circuits | 3 IsolateSOCKSAuth identities produced 3 distinct exit IPs (localhost, localhost, localhost) - separate circuits confirmed |
| tor_setup_gotcha | Tor SocksPort bound to localhost inside a rootless-podman container is unreachable through port-publishing (curl rc=97); SocksPort localhost:9050 fixes it |
| list_models | exits with deployment_not_deployed after 1.27 s, before any Tor request; no model catalog returned |
| serve_openai_api | exits at the deployment gate in under 4 s; localhost:8787/v1 never listened (3 HTTP probes: connection refused) |
| rewriter_live_tests | 5/5 project live tests fail closed at 90.08-90.09 s (daemon 90 s rewrite budget); the original prompt was never leaked to the target model (fail-closed contract holds) |
| rewrite_model_decode_speed | 2.29 tok/s (400 tokens / 174.3 s, solo, llama.cpp server print_timing); 1.11 tok/s measured under contention |
| rewrite_model_prefill_speed | ~24.7 tok/s solo (343-token prompt, ~13.9 s phase); 0.53 tok/s measured while an abandoned slot was still running |
| rewrite_model_load_time | 182.2 s for the 78.1 GiB IQ3_S GGUF (mmap, CPU) |
| rewrite_model_memory | 69.5 GiB RSS while serving; 0 MiB VRAM (CPU-only run) |
| quality_prompts | 17*23 -> '391' correct (28 output tokens, 146.8 s); verbose restaurant rewrite request: reasoning consumed the whole 400-token cap and final content was empty - no rewrite emitted within budget on this CPU |
| cover_traffic | configured (rate 1/s, 2 sanctioned HTTPS:443 URLs) but not observable live because serve exits at the deployment gate in <4 s; validated instead by the project's own race tests (internal/cover ok in 2.14 s) |
| weights | 83,863,586,496 bytes (78.1 GiB) IQ3_S GGUF split in 2 parts, already on the machine; 0 bytes newly downloaded for this test |
| gpu_need | none - the daemon is pure Go and the bring-your-own rewrite model was run CPU-only; no GPU slot claimed |

## Configuration
- prefill: ~24.7 tok/s (343-token prompt, ~13.9 s prefill phase, solo; 0.53 tok/s when measured behind an abandoned generating slot)
- decode: 2.29 tok/s (400 tokens / 174.3 s solo, server-measured); 1.11 tok/s under contention
- model_quant: IQ3_S with GSQ+RCO (abliterated), 78.1 GiB, 2-part GGUF
- kv_cache: 8192-token context, q8_0 K cache + q8_0 V cache
- turboquant: n/a (llama.cpp CPU build, no turboquant)
- speculative: none
- engine: llama.cpp b55 (5851a8e50), CPU-only (-ngl 0 -t 48); zkapi-clientd commit 0fb263b, Go 1.26.11
- hardware: our server CPU slot: 64 threads, 755 GB RAM, no GPU used (project needs none: pure-Go daemon + CPU rewrite model)

