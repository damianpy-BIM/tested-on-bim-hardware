# DeepSeek-V4.1-Flash-1017-GSQ-RCO-Coder

**What it is.** Quantized/pruned 551.9B parameter code generation model compressed to 72.1GB GGUF via RCO and GSQ

**Verdict: works.** The 182.7 GB pruned coder (72.1 GB IQ2_XXS backbone + 110.6 GB Engram) runs coding inference on one 32 GB V100 with RAM offload: decode 2.9-5.8 tok/s, prefill 47-68 tok/s warm, 3 of 4 execution-verified coding probes passed.

**Hardware:** 10x NVIDIA Tesla V100 32 GB

## Measured
| Metric | Value |
|---|---|
| download_verified | 5 of 5 backbone shards sha256-verified against official HF LFS oids (72.12 GB); Engram local file sha256 == official shard-6 oid, hard-linked as shard 6 (saved 110.6 GB re-download) |
| model_total_gb | 182.72 |
| backbone_gb | 72.12 |
| engram_gb | 110.6 |
| vram_peak_mib | 31486 |
| vram_limit_mib | 32768 |
| mem_available_min_gb | 226.1 |
| host_ram_total_gb | 755 |
| page_cache_prewarm_s | 80 |
| page_cache_prewarm_s_warm_rerun | 45 |
| server_ready_after_prewarm_s | 23 |
| server_ready_warm_rerun_s | 19 |
| cold_decode_tok_s | 1.69 |
| prefill_tok_s_by_prompt | [{'prompt_tokens': 6, 'prefill_tok_s': 3.9, 'note': 'startup-cost dominated, not meaningful'}, {'prompt_tokens': 532, 'prefill_tok_s': 47.0, 'repeat_run_tok_s': 52.7}, {'prompt_tokens': 1807, 'prefill_tok_s': 65.6, 'repeat_run_tok_s': 68.1}, {'prompt_tokens': 48, 'prefill_tok_s': 10.8, 'note': 'first chat request, includes slot init'}] |
| decode_tok_s_by_context | [{'context_tokens': 134, 'decode_tok_s': 2.86}, {'context_tokens': 660, 'decode_tok_s': 3.18}, {'context_tokens': 1935, 'decode_tok_s': 5.75}, {'context_tokens': 2096, 'decode_tok_s': 5.83, 'note': 'sustained over 2048 generated tokens'}] |
| decode_note | measured with ignore_eos because the coder chose EOS after 1 token on the two raw summary prompts; first decode after start is 1.7 tok/s cold, rises to 2.9-5.8 tok/s once warm |
| quality_probes | [{'probe': 'generate sieve(n)', 'pass': True, 'detail': 'executed, matches reference primes for n in {0,1,2,10,100,1000,10000}', 'wall_s': 79.5, 'completion_tokens': 360}, {'probe': 'generate lcs_length(a,b)', 'pass': True, 'detail': 'matches DP reference on 12 fixed+random cases', 'wall_s': 31.4, 'completion_tokens': 169}, {'probe': 'fix infinite-loop binary search', 'pass': True, 'detail': 'correct index/-1 on 12 targets, no hang under 5 s alarm', 'wall_s': 87.7, 'completion_tokens': 342}, {'probe': 'pelican-on-bicycle SVG', 'pass': False, 'detail': 'reasoning-only at both 1024 and 2048 token caps (6560 reasoning chars, 0 answer chars, finish=length); no SVG emitted', 'wall_s_at_cap': 355.8, 'completion_tokens_at_cap': 2048}] |
| quality_summary | 3 of 4 probes pass (all 3 executable coding tasks); free-form SVG probe failed on reasoning token budget, not on correctness |
| gpu0_claim_windows_utc | 15:18-15:31 and 15:33-15:45 on 2026-11-18; fn1 vacated and returned (30566 MiB back); claim released |
| comparison_same_hardware_same_config | vs unpruned Abiray IQ2_XXS (lab-2696503b): prefill 2x faster (65.6 vs 32.6 tok/s at 1807 prompt tokens), decode at least equal (5.75 vs 3.5-5.0 tok/s), 66.5 GB smaller backbone, same VRAM peak class (31,486 MiB) |

## Configuration
- engine: llama.cpp 0.9.0-dev b12111-5-g5851a8e50 (local build), CUDA 12.9, flash attention on
- hardware: our server GPU0 only: 1x Tesla V100-SXM2 32 GB (sm_70, no BF16), 2x Xeon E5-2682 v4, 755 GB host RAM, numactl node-0 pinning, -t 16 -tb 16
- model_quant: GGUF IQ2_XXS GSQ-RCO-Coder, 6 shards, 72.12 GB backbone (~1.05 effective bpw; retained experts IQ2_XXS 2.06 bpw, 28 layers IQ1_M, 192/384 experts pruned by RCO) + Engram IQ4_NL 110.60 GB (page-cache resident, mmap) = 182.72 GB; sha256-verified
- offload: llama.cpp --fit on -sm layer (layer split GPU/RAM), mmap, model fully in page cache
- kv_cache: q8_0 (-ctk q8_0 -ctv q8_0), -c 16384, 1 slot, fa on
- turboquant: no
- speculative: no
- sampling: greedy (temperature 0), reasoning on, reasoning-effort 50 (model card measurement setting), prompt cache off for speed rows, n_predict 128 (ignore_eos in forced-decode pass)
- measurement: timings reported by llama-server itself (native /completion + /v1/chat/completions); VRAM sampled every 2 s via nvidia-smi -i 0

