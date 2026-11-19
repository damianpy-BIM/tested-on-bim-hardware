# Imagination Studio

**What it is.** All-in-one creative studio with 61+ integrated apps for video, music, audio, visual effects, agents, depth mapping, audio separation, and content editing

**Verdict: partly.** Image jobs work fully on GPU0 (864x480 PNG in 68 s); video jobs generate fully on GPU0 inside 32 GB via RAM offload (56-frame clip, 119 s, peak 32,140 MiB) but produce nothing usable on this BF16-less card: the shipped job crashes at audio encoding (NaN waveform under forced FP16) and the patched job comes out a black, silent mp4, while the 5-second default clip does not fit 32 GB at all.

**Hardware:** 1x NVIDIA Tesla V100 32 GB

## Measured
| Metric | Value |
|---|---|
| image job time | 68 s per 864x480 PNG on GPU0 (scout quality, seed 42, output verified good) |
| video job time | 119 s end-to-end for an 864x480, 56-frame, 2 s clip (model's own record 99.6 s), with one-line audio patch; unpatched shipped job died at the audio-mux step at 117 s after all 4 sampler steps and both decodes |
| video sampler speed | ~8.6 s per sampler step at 864x480 / 56 frames (4 steps per job) |
| peak GPU0 VRAM | 32,140 MiB of 32,768 MiB on jobs that stayed in bounds (video, windows 4/6/7); 32,208 MiB and 32,494 MiB in windows ending in OOM/allocator abort |
| RAM at video peak | min RAM available 263,219 MiB during the heaviest run (of 773,899 MiB total); 299,762 MiB min during the successful patched run; the 93 GB of weights inflate 'used' with page cache, RAM offload never exhausted host RAM |
| app startup | 4-6 s to HTTP 200 on localhost:17871; ~23 s warm model init before first sampler step |
| model weights on disk | 93 GB across 7 checkpoints (MiniMax FastH3 42 GB + text encoder 26 GB + audio VAE 0.5 GB + video VAE 3 GB + image stack) |
| video output file | 14 KB H.264 mp4, 864x480, 56 frames, 2.33 s, AAC 32 kHz at -91 dB (silent); every frame identical, mean luma YAVG=16 (solid black) - byte-identical with FP16 and FP32 VAEs |
| stock (no-flag) video job | CUDA OOM at model init in 43 s: BF16 weights upcast to FP32 on sm_70, single 49.78 GiB allocation on a 31.73 GiB card |
| 5 s clip fit | does not fit: 124-frame job requests 24.89 GiB at init with 2.93 GiB free under the only allocator stable on this card (CUDA OOM at 43 s) |
| cudaMallocAsync default allocator | aborts on this Volta/driver pair after 1,436 s holding the card (CUDA error: invalid argument) |

## Configuration
- prefill: n/a (image/video diffusion sampler, not a token LLM)
- decode: ~8.6 s per sampler step at 864x480, 56 frames, 4 steps per job
- model_quant: FastH3 42 GB main weights (pruned, BF16-native) run FP16-forced via --force-fp16 on sm_70 (stock behaviour upcasts to FP32 and OOMs); 26 GB text encoder checkpoint ships int8-convrot; video VAE 3 GB int8-convrot; audio VAE 0.5 GB FP32 (verified loaded as float32); image jobs use a separate Qwen-Image-2.1-turbo stack: 13.9 GB BF16 model + 9.1 GB int8-convrot text encoder + 0.66 GB VAE
- kv_cache: n/a (diffusion)
- turboquant: no
- speculative: none
- engine: cuda (ComfyUI b9b290e, MiniMax FastH3 dense attention, --use-split-cross-attention, --force-fp16 --disable-cuda-malloc, dynamic VRAM loading with RAM offload via comfy-kitchen 0.2.39 / comfy-aimdo 0.5.6; one 1-line lab patch to nodes_audio.py in the throwaway copy)
- hardware: our server GPU0 only: Tesla V100-PCIE-32GB sm_70 (no BF16), 32,768 MiB VRAM, CUDA 12.9 driver, torch 2.14.1+cu126, 773,899 MiB system RAM

