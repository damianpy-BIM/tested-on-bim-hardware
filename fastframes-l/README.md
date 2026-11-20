# FastFrames-L

**What it is.** Apple's FastFrames-L (14.3B BF16 video DiT) generates 832x480 video clips at interactive-style latency.

**Verdict: works.** 3/3 clean 81-frame 832x480 16 fps clips on two of our machines: one Tesla V100 32 GB (277 s mean per clip, after FP16 + 26.8 GB KV-cache offload to pinned RAM) and an Apple M5 Max MacBook with 128 GB unified memory (536-652 s per clip, native BF16, cache fully resident, no paging). The Mac's early DiT passes run at 1.7-3.5 s versus the V100's 5.4 s mean; the full clip is ~2x slower because per-pass cost grows to 20-35 s as the autoregressive context accumulates.

**Hardware:** 1x NVIDIA Tesla V100 32 GB and an Apple M5 Max MacBook with 128 GB unified memory

## Measured (Apple M5 Max run, 20/11/2026)
| Metric | Value |
|---|---|
| video spec | 81 frames, 832x480, 16 fps = 5.0625 s per clip (ffmpeg frame-count + dims verified on every clip) |
| end-to-end per clip | 536-652 s (8.9-10.9 min): rollout 524.9 / 553.5 / 643.1 s, pixel decode 7.6-9.6 s |
| DiT pass latency (45 passes/clip) | mean 11.7-14.3 s/pass; early passes 1.7-3.5 s, late passes 20-35 s as the context grows |
| model load | 55.6-60.2 s (warm disk cache; BF16 weights 26.6 GiB) |
| text encode | 0.2-0.3 s per prompt (umT5-XXL bf16 on MPS, evicted before rollout) |
| peak memory | 131.9-133.3 GiB driver-allocated incl. allocator cache; 26.8 GB BF16 KV cache fully resident; swap absorbed the overflow (58-63 GB) |
| quality vs the V100 clips (same script: brightness / frame-diff / Laplacian variance) | corgi 87.9/4.6/170.0 vs 71.7/4.4/204.1; piano 69.5/4.8/687.3 vs 76.3/4.9/795.8; site 94.3/2.5/808.7 vs 100.1/2.8/997.6 - same content, bf16 vs fp16 tonal drift only |

## Measured (V100 run, 18/11/2026)
| Metric | Value |
|---|---|
| end-to-end per clip | 255.7-294.1 s, mean 277.1 s at 31.3 GB peak VRAM |
| DiT step latency | mean 5.4 s per 1560-token pass, 45 passes/clip, 286.9 token/s incl. KV streaming |
| adaptation | FP16 (sm_70 has no BF16 MMA), 26.8 GB KV cache in pinned host RAM streamed per layer, fused-QKV fast ops off |

## Configuration (M5 Max run)
- prefill: umT5-XXL text encode 0.2-0.3 s/prompt on MPS, then evicted; first frame = 4 denoise steps
- decode: frame-causal autoregressive diffusion, 2 steps/frame, 45 DiT passes of 1560 tokens per clip, one pixel decode 7.6-9.6 s
- model_quant: bfloat16 native (weights as shipped)
- context_quant: 26.8 GB BF16 KV cache fully resident in unified memory (no CPU paging)
- turboquant: no
- speculative: n/a (video diffusion, not LLM decoding)
- engine: FastFrames reference PyTorch 2.9.1 MPS + FF_L stock recipe with fused-QKV fast ops ON; port changes: cuDNN SDPA -> torch SDPA bf16 on MPS, float64/complex128 RoPE + scheduler x0 step computed on CPU, umT5 eviction before rollout

## Run it on Apple Silicon
`ff_mac2.py` (MPS port driver) and `quality_mac.py` (frame verification + metrics) are in this folder's `mac/` subdirectory.
Weights: apple/FastFrames-L + Wan2.1 umT5-XXL (42.5 GB total). Needs ~80 GB of free unified memory with nothing else
served; log lines are flushed per DiT pass so a stall is visible.

## Upstream
- https://huggingface.co/apple/FastFrames-L

Upstream code and weights keep their own licence.
