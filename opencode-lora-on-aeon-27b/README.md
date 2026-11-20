# OpenCode LoRA on AEON 27B

**What it is.** RL-trained ~300MB LoRA for Qwen3.8-27B optimised for OpenCode, applied at runtime to our uncensored AEON build

**Verdict: works.** The OpenCode LoRA applies at runtime to AEON 27B Q4_K_M on one V100: temp-0 A/B flips tool-call 2/3->3/3 and borderline 4/6->5/6 for ~6% prefill and 19-22% decode cost; MTP on sm_70 accepted 0/441 drafts and cost 44% of decode, so it must stay off.

**Hardware:** 1x NVIDIA Tesla V100 32 GB

## Measured
| Metric | Value |
|---|---|
| adapter_bytes | 318,802,400 bytes (F16 GGUF LoRA, HF harness-hub/Qwen3.8-27B-opencode-adapted-GGUF) |
| base_file | 16,810,715,168 bytes Q4_K_M (Qwen3.8-27B-AEON-ULTIMATE-UNCENSORED) |
| quality_ab_temp0 | base coding 4/4, tool-call 2/3, math 1/4, borderline 4/6; +LoRA coding 4/4, tool-call 3/3, math 1/4, borderline 5/6 (14-prompt suite, temp 0, reproduced in 2 passes; 11/14 rows byte-identical, 3 differ: 'read src/utils.py' BAD->OK, pickpocket prompt REFUSED/THIN->ANSWERED, one code timing) |
| prefill_mtp_off_base | 745.7 / 678.5 (677.1 repeat) / 549.9 (548.0) tok/s at 3,749 / 10,412 / 13,329 prompt tokens |
| prefill_mtp_off_lora | 688.7 / 636.0 (629.0) / 516.3 (520.2) tok/s at the same prompts = -6% mean |
| decode_mtp_off_base | 31.98 / 29.96 / 27.65 tok/s (512 generated at ~4.3k / 10.9k / 13.8k context) |
| decode_mtp_off_lora | 24.89 / 23.69 / 22.32 tok/s = -22% / -21% / -19% |
| mtp_on_sm_70 | draft acceptance 0.00000 in every server run (0/441); same base with MTP on: prefill 644.9 / 652.7 / 511.7, decode 18.05 / 16.77 / 15.43 tok/s = 44% below MTP-off |
| swe_bench_claim | the tweet's 35.3% -> 51.0% on SWE-bench Pro hard-51 is Hugging Face's number on the STOCK Qwen3.8-27B; we ran our AEON uncensored build on a 14-prompt tool suite, not SWE-bench, so that headline is not reproduced here |
| lora_applied_proof | controlled: identical build @5851a8e50, identical server config, temp 0, sole variable --lora -> semantic flips reproduced in both passes; the LoRA server answered on port 8922 (only reachable when the branch fires) and its /props was captured |
| gpu0_serialization | all runs under flock a local path + .gpu0-claim, GPU0 only, serving GPUs untouched |

## Configuration
- prefill: 688.7 tok/s (3,749-token prompt)
- decode: 24.89 tok/s (512 tokens at ~4.3k context; 23.69 at 10.9k, 22.32 at 13.8k)
- model_quant: Q4_K_M base 16,810,715,168 bytes + F16 LoRA adapter 318,802,400 bytes
- kv_cache: q8_0 KV (-ctk q8_0 -ctv q8_0), n_ctx 33,000
- turboquant: no
- speculative: no (MTP measured 0.00000 acceptance on sm_70, 0/441 -> disabled for all published figures)
- engine: llama.cpp 5851a8e50 llama-server, CUDA 12.9, -fa on, -t 32, -b 2048 -ub 512
- hardware: 1x Tesla V100 32 GB (sm_70, GPU0 test slot on the 8x V100 node), 755 GB RAM host

