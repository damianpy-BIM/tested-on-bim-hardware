# Strata engine

**What it is.** LLM inference engine version 0.1.60 with a prefill performance regression on V100 GPUs

**Verdict: partly.** Strata engine 0.1.60 starts and answers on the V100 but reads prompts 11-39% slower than 0.1.59 (6,695-token prompt: 653.5 vs 1,066.8 tok/s) and takes 58 s longer to load, so 0.1.59 stays the right engine for BIM-length jobs; the awaited fix is not out (v0.2.15 still ships 0.1.60).

**Hardware:** 1x NVIDIA Tesla V100 32 GB

## Measured
| Metric | Value |
|---|---|
| prefill 485-token prompt, engine 0.1.59 | 352.3 tok/s (read in 1.35 s) |
| prefill 485-token prompt, engine 0.1.60 | 312.1 tok/s (read in 1.55 s) |
| prefill 1,723-token prompt, engine 0.1.59 | 499.5 tok/s (read in 3.45 s) |
| prefill 1,723-token prompt, engine 0.1.60 | 414.1 tok/s (read in 4.17 s) |
| prefill 6,695-token prompt, engine 0.1.59 | 1,066.8 tok/s (read in 6.28 s) |
| prefill 6,695-token prompt, engine 0.1.60 | 653.5 tok/s (read in 10.24 s) |
| prefill change at 6,695 tokens | -38.7% (read time +63.2%) |
| prefill change at 1,723 tokens | -17.1% |
| prefill change at 485 tokens | -11.4% |
| engine 0.1.60 prefill with STRATA_NV_CHUNK=0 (8,192-token chunk) | 135.1 tok/s at 485 tokens, 339.3 tok/s at 1,723 tokens, 690.0 tok/s at 6,695 tokens |
| decode 128 tokens at 483-token context, engine 0.1.59 | 43.2 tok/s (drafts accepted 74 of 91) |
| decode 128 tokens at 483-token context, engine 0.1.60 | 60.6 tok/s (drafts accepted 67 of 84) |
| decode 128 tokens at 1,721-token context, engine 0.1.59 | 62.3 tok/s (drafts accepted 58 of 74) |
| decode 128 tokens at 1,721-token context, engine 0.1.60 | 64.2 tok/s (drafts accepted 57 of 73) |
| engine ready to first request, 0.1.59 | 46.1 s |
| engine ready to first request, 0.1.60 | 104.1 s |
| VRAM peak during bench, 0.1.59 | 30,600 MiB |
| VRAM peak during bench, 0.1.60 | 30,594 MiB |
| prompt chunk chosen by --prefill auto, 0.1.59 | 8,192 tokens (prompt path borrowed 2,301 cache slots, 4.38 GiB) |
| prompt chunk chosen by --prefill auto, 0.1.60 | 32,768 tokens (prompt path borrowed 7,020 cache slots, 13.30 GiB) |
| word-problem answer (greedy) | identical correct answer on both engines (80 trips, 175 tokens) |
| code prompt answer, engine 0.1.59 | code returned in content, 254 characters within the 192-token limit |
| code prompt answer, engine 0.1.60 | content empty, finish_reason length, all 192 tokens in reasoning_content (3 of 3 samples) |
| BIM-explanation answer | coherent three paragraphs on both engines (751 characters on 0.1.59, 719-777 on 0.1.60) |
| engine 0.1.59 package | 949,797,317 bytes, sha256 4bf321cb0c2d7ff15fe221f22a29aeb8371f24fa77a4425c920eb01a520babbc, signed ed25519 key 5d1bc23abbeffd0d |
| engine 0.1.60 package | 875,179,152 bytes, sha256 a50a4d1efd7fbf0da03a0a2d4d91b0ac059d92579ae41f611e49bc9228262856, signed ed25519 key 5d1bc23abbeffd0d |

## Configuration
- prefill: 653.5 tok/s (0.1.60) vs 1,066.8 tok/s (0.1.59), 6,695-token prompt, single request, prompt cache off
- decode: 64.2 tok/s (0.1.60) / 62.3 tok/s (0.1.59), 1,721-token context, 128 tokens out
- model_quant: Qwen3.8-Flash-Next-GSQ-RCO-abliterated, IQ3_S GGUF native shard + IQ3_S PLE shard (RAM-resident expert/PLE offload)
- kv_cache: int8, 32,768 cells resident in VRAM, 262,144-token maximum context
- turboquant: no
- speculative: DFlash2 draft model (--draft dflash2 --draft-model qwen3.8-flash-next-dflash2.q4_0-selq4.pack --spec 6 --draft-conf 0.5; 57 of 73 drafts accepted; mandatory with this native IQ pack, which refuses to start without --spec >= 2)
- engine: Strata engine 0.1.59 vs 0.1.60, linux-x86_64-cuda-cuda12 build, CUDA 12.9, sm_70, driver 580.178.04
- hardware: 1x Tesla V100-PCIE-32GB (sm_70, GPU0 only, claimed and idle during every measurement) + 755.8 GiB system RAM for expert offload, PCIe 5.7 GB/s host-to-device

