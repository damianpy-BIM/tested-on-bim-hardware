# PXA

**What it is.** Self-hosted inference engine with speculative decoding/MTP and PXA Control.

**Verdict: works.** PXA 4.0.1 loaded a 27B model onto one 32 GB V100 in ten seconds and served it at 61-85 tokens per second with its built-in draft speculation (43.3 without) - the Volta speedups it claims held up on our card.

**Hardware:** 1x NVIDIA Tesla V100 32 GB

## Measured
| Metric | Value |
|---|---|
| server_load_to_healthy | 10 s (13.57 GB model; 7-12 s across three runs) |
| decode_with_speculation_prose | 61.3 tok/s (256 tokens generated, greedy) |
| decode_with_speculation_code | 80.1 tok/s (256 tokens); 85.0 tok/s (774 tokens) |
| decode_with_speculation_chat | 69.8 tok/s (128 tokens) |
| decode_without_speculation | 43.3 tok/s (256 tokens, greedy) |
| speculation_speedup | 1.42x (same prose prompt, 256 tokens) |
| prefill | 728.7 tok/s (939-token prompt) |
| mtp_draft_acceptance | 0.56-0.78 (engine-reported) |
| vram_peak_while_serving | 14644 MiB of 32768 MiB |
| gpu_utilisation_decode | ~96 % |

## Configuration
- prefill: 728.7 tok/s (939-token prompt)
- decode: 61.3-85.0 tok/s (context 0.4k-1.1k of 4096, MTP speculation on); 43.3 tok/s (same, speculation off)
- model_quant: PXQN (allocator mix over N3/N3S8/N4/q8_0, ~4-bit class), Qwen3.8-27B OneCard, 13.57 GB, all 65 layers on GPU
- kv_cache: f16, 4096 tokens (-ub 2048, chosen by engine auto-tune)
- turboquant: no
- speculative: MTP (head in model, n_max=3, confidence floor 0.5) with n-gram front stage; n-gram+MTP measured, off-state also measured
- engine: PXA 4.0.1 (llama.cpp-derived, bundled CUDA 12.8 runtime), -ngl 999 -fa on, greedy temp 0
- hardware: 1x Tesla V100-PCIE-32GB (sm_70), driver 580.178.04, our server GPU0

