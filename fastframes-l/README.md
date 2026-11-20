# FastFrames-L

**What it is.** Apple's FastFrames-L model generates videos at interactive latency.

**Verdict: works.** apple/FastFrames-L (14.3B BF16 video DiT, FF_L recipe) generated 3/3 clean 81-frame 832x480 16 fps clips on the MacBook M5 Max 128 GB over MPS, end-to-end 536-652 s (8.9-10.9 min) per clip after porting fixes (umT5 evicted before rollout, oMLX VL serving stopped for the run); this is 2-2.4x slower per clip than one our server V100 (277 s mean), where the Mac's early DiT passes are actually ~2.7x faster (1.7-3 s vs 5.4 s mean) but degrade to 20-35 s/pass as the autoregressive context and allocator cache grow to ~133 GiB.

**Hardware:** 1x NVIDIA Tesla V100 32 GB

## Measured
| Metric | Value |
|---|---|
| video spec | 81 frames, 832x480, 16 fps = 5.0625 s per clip (h264, ffmpeg frame-count + dims verified on every clip) |
| clips (prompts/seeds identical to the V100 run) | corgi seed0 524.9 s rollout / 536 s e2e; piano2 seed1 553.5 s / 564 s e2e; site seed2 643.1 s / 652 s e2e - all 3/3 visually on-prompt, no artifacts (vlread-verified frames) |
| DiT pass latency (45 passes per clip) | early passes 1.7-3.5 s, late passes 20-35 s; mean 11.7-14.3 s/pass (run4 curve: pass 8 t=14 s, pass 24 t=117 s, pass 40 t=451 s, pass 45 t=622 s) |
| model load (disk cache warm) | 55.6-60.2 s per process |
| text encode | 0.2-0.3 s per prompt (umT5-XXL bf16 MPS-resident), encoder evicted from MPS before rollout (-11.4 GiB) |
| pixel decode per clip | 7.6-9.6 s |
| peak MPS driver memory (cached incl. allocator reuse) | 131.9-133.3 GiB; swap grew to 58-63 GB during clips - unified memory + compression, no allocation failure |
| quality (same script on Mac clips and the V100 clips; brightness / frame-diff / Laplacian-variance) | Mac corgi 87.9/4.6/170.0 vs V100 corgi 71.7/4.4/204.1; Mac piano2 69.5/4.8/687.3 vs V100 piano 76.3/4.9/795.8; Mac site 94.3/2.5/808.7 vs V100 site 100.1/2.8/997.6 - same content, bf16 vs fp16 tonal drift only |
| comparison V100 (same repo, a local path | V100 277 s mean per clip (5.4 s/pass flat, fp16 + 26.8 GB KV paged from pinned RAM); M5 Max 536-652 s per clip with stock BF16 fully resident; a single V100 stays ~2x faster per clip on this workload |
| download size | 42.5 GB already archived (unchanged): DiT 26.6 GiB + refiner 1.7 GiB + pixel decoder 0.27 GiB + umT5-XXL 11.4 GB |

## Configuration
- prefill: umT5-XXL text encode 0.2-0.3 s/prompt on MPS then evicted; first frame = 4 denoise steps
- decode: frame-causal autoregressive diffusion, 2 steps/frame, 45 DiT passes of 1560 tokens per clip, 11.7-14.3 s/pass mean (1.7-3.5 s early -> 20-35 s late as context grows), one pixel decode 7.6-9.6 s
- model_quant: bfloat16 native (weights as shipped; no fp16 conversion needed on Apple bf16 MMA, unlike sm_70)
- context_quant: 26.8 GB KV cache BF16 fully resident in the 128 GB unified memory (no CPU paging, unlike the V100 run); peak driver-allocated 133 GiB incl. allocator cache, swap absorbed the rest
- turboquant: no
- speculative: n/a (video diffusion, not LLM decoding)
- engine: FastFrames reference PyTorch 2.9.1 MPS + FF_L stock recipe with fast_ops (fused QKV) ON; port changes: cuDNN SDPA -> torch SDPA bf16 on MPS, autocast cuda->mps, float64/complex128 RoPE + scheduler x0 step on CPU, umT5 eviction before rollout (ff_mac2.py)
- hardware: Damian's MacBook Pro, Apple M5 Max, 128 GB unified, macOS 26.6.2, on AC; headless over ssh, nothing on screen

## Upstream
- https://huggingface.co/apple/FastFrames-L

Upstream code and weights keep their own licence.
