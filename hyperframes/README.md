# HyperFrames

**What it is.** AI agent video rendering tool that converts HTML animations to MP4

**Verdict: works.** HyperFrames renders HTML+GSAP compositions to real MP4 entirely on CPU (headless Chrome screenshots + x264), byte-identical across runs and frame-accurate, with zero GPU, zero keys and zero per-render cost — useful for BIM: agent-made intro, dashboard and report videos.

**Hardware:** CPU only, on the NVIDIA Tesla V100 server

## Measured
| Metric | Value |
|---|---|
| output_file | valid MP4, H.264 1920x1080, 30 fps, 150 frames, 5.000 s, 198226 bytes (317 kbps, CRF 16) |
| render_wall_time_default_5_workers | 47.65 s for a 5 s clip (calibration 32.96 s + capture 5.65 s + encode 1.43 s) |
| capture_throughput | 26.5 frames/s at 5 workers; 0.7-0.9 frames/s at 1 worker under host loadavg 25-30 |
| h264_encode_speed | 105 frames/s (150 frames in 1.43 s) |
| determinism | byte-identical MP4 across 2 renders, MD5 b4b54b3aa90c849731becde5ad102717 |
| peak_memory | 1.74 GB single largest process, ~256 MB per Chrome worker (5 workers) |
| animation_accuracy | frame-exact: counter 41% at t=2.500 s vs 40.6% timeline math |
| install | 78 npm packages in 16 s (hyperframes@0.9.72), no weights, no download over 100 MB |
| gpu_needed | none - all renders verified with --no-browser-gpu (software SwiftShader) |

## Configuration
- prefill: n/a (video renderer, not an LLM)
- decode: n/a (video renderer, not an LLM)
- model_quant: n/a
- kv_cache: n/a
- turboquant: no
- speculative: no
- engine: HyperFrames 0.9.72: headless Chrome for Testing 153 per-frame seek+screenshot, FFmpeg 6.1.1 x264 software encode, SwiftShader, --no-browser-gpu
- hardware: CPU only: our server, 64 threads, 755 GB RAM; GPU0 never claimed; host under production load avg 25-30 during test

