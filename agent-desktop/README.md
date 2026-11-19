# agent-desktop

**What it is.** Agent framework for parallel computer automation across macOS, Windows, and Linux with multi-cursor desktop control

**Verdict: works.** agent-desktop v1.3.1 runs CPU-only headless on our server: background semantic desktop control verified (cursor never stolen, physical clicks proven via X11 probe) and two parallel agents on one machine gave 1.71x speedup with zero cross-talk.

**Hardware:** CPU only, on the NVIDIA Tesla V100 server

## Measured
| Metric | Value |
|---|---|
| click_reliability | 10/10 semantic clicks executed the app handler (counter 1->11 exactly) |
| latency_solo_ms | {'n': 10, 'snapshot': {'min': 70, 'median': 77, 'max': 82}, 'click': {'min': 67, 'median': 92, 'max': 100}, 'verify_find': {'min': 71, 'median': 78, 'max': 85}, 'full_step_median': 247} |
| wall_10_steps_incl_300ms_sleeps_ms | 4775 |
| batch_3_clicks_one_call_ms | 285 |
| latency_under_parallel_contention_ms | {'snapshot': [218, 344], 'click': [466, 805]} |
| cursor_move_ms | 15 |
| physical_mouse_click_ms | 37 |
| cursor_control | mouse-move --xy set the real X pointer to 211,505 then 987,333 (verified by independent XQueryPointer probe); mouse-click at 121,65 moved the pointer and incremented the app counter 35->36 |
| headless_no_cursor_steal | headless ref click changed app state while pointer stayed at 640,400 |
| parallel_vs_sequential | {'parallel_wall_ms': 7588, 'sequential_wall_ms': 12960, 'speedup': 1.71, 'iterations': 10, 'counters_after': 'A 25->30 (alpha), B 0->5 (beta), no cross-talk'} |
| peak_rss_per_cli_invocation_kb | 8704 |
| binary_size_mb | 11 |
| mcp_tools_exposed | 75 |
| mcp_protocol | 2024-11-05 |
| list_displays_ms | 9 |

## Configuration
- engine: agent-desktop v1.3.1 CLI (vercel-labs, Apache-2.0) - no LLM inside, agent loop external (bash); no API key used
- hardware: our server, 64 threads, 755 GB RAM, GPU invisible (CUDA_VISIBLE_DEVICES empty; GPUs 0-9 untouched)
- os: Linux 6.8.0-147-generic x86_64, Ubuntu-family userland, no sudo, nothing system-installed
- display: private Xvfb :99 1280x800x24 + private dbus session bus + on-demand at-spi2 + custom Xlib EWMH fake-WM seeding (xseed)
- target_app: custom GTK3 test app (2 instances) with real signal handlers
- session: run-1794847594068-23933-0 started with --cursor --multi-agent; agents alpha/beta/gamma/delta via --agent-id
- iterations: n=10 timed solo loop; n=5 per agent parallel + sequential
- known_limits: on WM-less Xvfb: screenshot reports false 'covered', focus-window/move-window/ref-targeted headed click need a real window manager; clipboard and screenshot need mode-700 dirs (security checks); no resident daemon on Linux - held-input commands fail closed by design

