# Heretic

**What it is.** Automated tool that abliterates/decensors LLMs (removes refusal behavior) in one command, works on Llama/Qwen/Gemma etc.

**Verdict: works.** Works: Heretic ARA, 4 trials (default 100), on Qwen2.5-0.5B-Instruct FP16 cut keyword refusals from 14/16 to 0/16 at KL 0.0749 nats, and three benign answers stayed coherent. Prefill 11101.38 tok/s at 512 tokens. Decode 20.51 tok/s over 128 tokens.

**Hardware:** CPU only, on the NVIDIA Tesla V100 server

## Measured
| Metric | Value |
|---|---|
| refusal_rate_base | 14/16 prompts |
| refusal_rate_heretic | 0/16 prompts |
| kl_divergence_saved_trial | 0.0749 nats |
| kl_divergence_trial_4_not_saved | 15.2455 nats |
| abliteration_elapsed | 1 min 9 s |
| allocated_vram_abliteration | 0.95 GB |
| resident_ram_heretic | 1.88 GB |
| prefill_heretic | 11101.38 tok/s (512 tokens) |
| decode_heretic | 20.51 tok/s (128 tokens, context 29 to 157) |
| prefill_base | 12586.21 tok/s (512 tokens) |
| decode_base | 26.62 tok/s (128 tokens, context 29 to 157) |
| peak_allocated_vram_inference | 1099.7 MiB |
| gpu0_smi_during_inference | 2864 MiB (includes glide 1314 MiB) |

## Configuration
- prefill: 11101.38 tok/s (512 tokens)
- decode: 20.51 tok/s (128 tokens, context 29 to 157)
- model_quant: FP16
- kv_cache: dynamic FP16, 157 tokens
- turboquant: no
- speculative: no
- engine: transformers 5.23.0 + torch 2.7.1+cu126 + heretic 2.2.0.dev0
- hardware: Tesla V100-PCIE-32GB GPU0 sm_70, CUDA_VISIBLE_DEVICES=0, CUDA 12.9

## Upstream
- https://github.com/p-e-w/heretic

Upstream code and weights keep their own licence.
