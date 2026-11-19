# ESP-Mosaico

**What it is.** GitHub starter repo with MCP/Claude Code/Codex configs and simulator for ESP32-S31 embedded hardware

**Verdict: works.** ESP-Mosaico's agent workspace and both Espressif host simulators ran on CPU-only Linux with no board and no ESP-IDF; a one-line C edit by the agent compiled and visibly rendered in the official GSP simulator — but it is an embedded touch-panel dev kit, not a BIM tool.

**Hardware:** CPU only, on the NVIDIA Tesla V100 server

## Measured
| Metric | Value |
|---|---|
| clone_repo_wall_s | 16.27 |
| clone_repo_size_MB_approx | 11 |
| submodule_init_wall_s | 47.63 |
| submodule_added_data_MB_approx | 64 |
| agent_files | CLAUDE.md + AGENTS.md + 6 SKILL.md + .mcp.json with 2 Espressif MCP servers |
| mosaico_project_init_wall_s | 1.413 |
| esp_idf_installed | False |
| gsp_tool_cache_total_MB | 38.19 |
| gsp_tools_source | https://dl.espressif.com/AE/gsp/ (gspc 0.6.1, sim 1.5.1) |
| gsp_first_run_wall_s_incl_download | 8.748 |
| gsp_preview_frames | 90 |
| gsp_preview_sim_elapsed_ms | 43 |
| gsp_preview_effective_fps | 2093 |
| gsp_preview_wall_s_range | 0.79-1.38 s warm |
| scene_bundle_bytes | 95056 |
| c_backend_full_run_wall_s | 4.473 |
| c_backend_full_run_exit_code | 0 |
| c_backend_stdout | hello_backend: count=0, last_error=0 |
| agent_c_edit_render_test | app_hello.c changed 00->42; rebuilt backend attached to sim renders '42 hellos' in the dumped frame |
| tap_run_frames | 31 |
| tap_run_sim_elapsed_ms | 1088 |
| final_frame_png_bytes | 20376 |
| final_frame_resolution | 480x480 px |
| scripted_tap_increment | none (count=0, hit-test unverified) |
| skyhop_600f_state_hash | 99ab84b1 |
| skyhop_render_mean_ms_per_frame | 0.356 |
| determinism_300f_twice_state_hash | 00f0fc33 == 00f0fc33 (identical) |
| shooter_300f_state_hash | fdd92572 |
| shooter_render_mean_ms_per_frame | 0.644 |
| tomb_raycast_300f_state_hash | 53dfb99b |
| tomb_raycast_render_mean_ms_per_frame | 2.115 |
| screen_resolution | 480x480 px, 30 ticks/s |
| mcp_endpoints_http_status_initialize | [200, 200] |
| llm_tokens_per_s | n/a - no LLM anywhere in this toolchain |
| vram_used_MB | 0 |
| model_weights_downloaded_bytes | 0 |

## Configuration
- prefill: n/a (no LLM used in this test)
- decode: n/a (no LLM used in this test)
- model_quant: n/a (no LLM used in this test)
- kv_cache: n/a (no LLM used in this test)
- turboquant: n/a (no LLM used in this test)
- speculative: n/a (no LLM used in this test)
- engine: gsp-sim 1.5.1 (Rust/WASI) + gspc 0.6.1 + raylib-lite-engine host runner (gcc-compiled C via CMake/ctypes); Claude Code (Opus) acted as the coding agent - no local model inference involved
- hardware: CPU-only test host (our server class): 64 threads, 755 GB RAM, no GPU presented (CUDA_VISIBLE_DEVICES empty)

