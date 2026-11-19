# DeepSeek-V4.1-Flash

**What it is.** DeepSeek-V4.1-Flash model quantized to run locally on 12GB GPU

**Verdict: works.** 763B Uncensored DeepSeek-V4.1-Flash-1017 (GSQ-RCO IQ2_XXS, abliterated) runs on ONE V100 with stock llama.cpp --fit and RAM offload: coherent correct non-refusing output at 3.5-5.0 tok/s decode using the 32 GB card, and the bookmark's 12 GB claim verified at 11,590 MiB peak VRAM / 2.83 tok/s with a 12.3 GB budget - given ~250 GB of warm host RAM; 10-20x slower than our production 8-GPU vLLM of the same quant.

**Hardware:** 10x NVIDIA Tesla V100 32 GB

## Measured
| Metric | Value |
|---|---|
| prefill, 6-token prompt | 2.1 tok/s |
| prefill, 532-token prompt | 26.0 tok/s |
| prefill, 1,807-token prompt | 32.6 tok/s |
| decode, chat with reasoning (145/441/570 tokens out) | 3.5 / 3.5 / 5.0 tok/s |
| decode, first cold request | 1.11 tok/s |
| decode at 12 GB VRAM budget (193 tokens out, incl prefill) | 2.83 tok/s |
| VRAM peak, 32 GB config | 31,718 MiB |
| VRAM peak, 12 GB budget config (--fit-target 20480) | 11,590 MiB |
| server start to ready (page cache hot) | 26-36 s |
| 249 GB model files into page cache | 175 s cold / 80 s hot |
| MemAvailable floor during bench | 163.4 GB of 755 GB |
| backbone download | 138.6 GB in 29 min (~80 MB/s), sha256 5/5 verified |
| quality q1 math word problem | correct (Answer: 1 minutes, matches the rate as posed) |
| quality q2 code (longest palindromic substring) | correct, executed, 8/8 brute-force cases pass |
| quality q3 uncensored probe (profanity-allowed complaint email) | complied, no refusal, all constraints met |
| GPU utilization during generation | ~9% (CPU-bound expert streaming) |

## Configuration
- prefill: 32.6 tok/s (1,807-token prompt, raw /completion, prompt cache off, greedy)
- decode: 3.5-5.0 tok/s (chat completions incl. reasoning, 145-570 tokens out, 16,384-token ctx); 2.83 tok/s at the 12.3 GB VRAM budget
- model_quant: GSQ-RCO non-uniform IQ2_XXS 2.06 bpw backbone 138.58 GB (5 shards, abliterated weight-baked, Abiray build of ISTA-DASLab quant) + shared Engram IQ4_NL lookup 110.60 GB as shard 6 = 249.2 GB, all sha256-verified
- kv_cache: q8_0 K+V, 16,384-token context, flash attention on
- turboquant: no
- speculative: no
- engine: llama.cpp 0.9.0-dev b12116 (5851a8e50), CUDA 12.9 build, --fit on -sm layer, mmap with CPU tensor overrides, 16 CPU threads pinned to NUMA node 0, --jinja --reasoning on --reasoning-effort 50
- hardware: our server GPU0 only: 1x Tesla V100-PCIE-32GB (sm_70, driver 580.178.04) + 2x Xeon E5-2682 v4 (64 threads) + 755 GB RAM + NVMe model storage; GPUs 1-9 production untouched

