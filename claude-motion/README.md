# claude-motion

**What it is.** Motion graphics framework using Claude Opus 5.5 to generate and validate video frames

**Verdict: works.** claude-motion runs end to end on CPU with no GPU and no API key: the shipped 22 s 1080x1080@60 example built in 1 min 55 s (render 15.4 frames/s) and a new piece I authored with its own pipeline rendered in 27.5 s (21.8 frames/s), sound auto-mastered to -14 LUFS — useful for BIM for fast captioned feature/launch clips.

**Hardware:** CPU only, on the NVIDIA Tesla V100 server

## Measured
| Metric | Value |
|---|---|
| shipped_example | out/effort.mp4: 22.0 s, 1080x1080, h264 60 fps + AAC 48 kHz stereo, 6.4 MB, 2.32 Mbps |
| full_build_wall_time | 1 min 54.7 s for the 22 s example (npm sfx + remotion render + ffmpeg mux, incl. first-time browser download) |
| render_throughput_shipped_example | 15.4 frames/s at 1080x1080 60 fps, 1,320 frames in 1 min 25.8 s (CPU, headless Chrome, browser cached) |
| render_throughput_agent_authored_piece | 21.8 frames/s at 1080x1080 60 fps, my own 10 s piece (600 frames) in 27.5 s (CPU) |
| agent_authored_piece | 10.0 s, 1080x1080, 60 fps, 2.4 MB; typecheck clean; repo review-loop contact-sheet pass clean first try; 20 timeline beats all synced in wave check |
| peak_ram | 1.07 GB (full build), 783 MB (render alone); 0 MiB GPU used |
| audio_shipped_cue_sheet | -14 LUFS integrated (target -14 +/-1), true peak -2.3 dBFS |
| audio_authored_cue_sheet | -14.0 LUFS integrated, true peak -1.9 dBFS, 27 sounds from 1 cue file, pure Python stdlib |
| web_sim_build | 3 offline HTML pages (948 KB with three.js inlined) in 0.34 s |
| web_sim_capture | 0.81 frames/s at 1080x1350 60 fps; completed 6.0 s clip in 7 min 34 s; full 24 s at 1440x1800 measured 0.70 frames/s (~34 min, CPU SwiftShader software rendering) |
| install | npm install: 259 packages in 11 s; repo unit tests 7/7 pass |
| gpu_need | none - zero CUDA/torch/vLLM references in repo; everything ran with GPU untouched (GPU0 never claimed) |

## Configuration
- prefill: n/a (no LLM inference in the product; the agent driving it was the local session)
- decode: n/a (no LLM inference in the product)
- model_quant: n/a (no model weights)
- kv_cache: n/a
- turboquant: no
- speculative: no
- engine: Remotion 4.0.529 (headless Chrome software render) + Python 3.12 sfx engine + ffmpeg 6.1 libx264
- hardware: our server CPU slot, 64 threads, no GPU used (GPU0 untouched)

## Upstream
- https://github.com/whaleyxbt/claude-motion

Upstream code and weights keep their own licence.
