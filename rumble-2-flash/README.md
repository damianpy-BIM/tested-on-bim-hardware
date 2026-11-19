# Rumble-2-Flash

**What it is.** 0.5B open-weight speech-to-text (Qwen3-ASR fine-tune, arch qwen3_asr) for accents, crosstalk, phone calls, noise; 45 languages; Apache-2.0

**Verdict: partly.** Rumble-2-Flash (0.5B, FP16) on one V100: 1.15 s median for 8-12 s clips (RTF 0.12), clean-clip median error 2.87% (whisper-large-v3-turbo on the same box: 0.79 s, 0.0%). 5-min: EN 10.14% not char-truncated, FR 14.79% not char-truncated. Truncated longs: FR 60s, ZH 60s. Whisper EN 5-min err 50.55% (char-truncated).

**Hardware:** 1x NVIDIA Tesla V100 32 GB

## Measured
| Metric | Value |
|---|---|
| load_sec | 2.6 |
| vram_after_load_mib | 973 |
| vram_peak_mib | 3242 |
| clip_median_wall_s | {'rumble': 1.15, 'whisper_v100': 0.79, 'ane_clean': 1.18} |
| clip_median_rtf | {'rumble': 0.12, 'whisper_v100': 0.08} |
| err_pct_median_clean_by_lang | {'rumble': {'EN': 4.1, 'FR': 0.0, 'ES': 0.0, 'ZH': 2.49}, 'whisper_v100_gpu1': {'EN': 3.85, 'FR': 0.0, 'ES': 0.0, 'ZH': 3.08}} |
| rumble_err_pct_median_by_variant | {'clean': 2.87, 'phone': 0.0, 'noisy': 7.42, 'opus': 0.0} |
| rumble_noisy_split_err_pct_med | {'snr_lt10db': 60.87, 'snr_ge10db': 0.0} |
| long_form | {'rumble': [{'lang': 'EN', 'name': '60s', 'sec': 61.1, 'wall_s': 5.81, 'rtf': 0.095, 'err_pct': 2.67, 'chars': '957/931', 'truncated': False}, {'lang': 'EN', 'name': '5min', 'sec': 305.8, 'wall_s': 25.96, 'rtf': 0.0849, 'err_pct': 10.14, 'chars': '3731/3872', 'truncated': False}, {'lang': 'FR', 'name': '60s', 'sec': 65.0, 'wall_s': 7.97, 'rtf': 0.1226, 'err_pct': 23.39, 'chars': '867/1107', 'truncated': True}, {'lang': 'FR', 'name': '5min', 'sec': 297.2, 'wall_s': 40.91, 'rtf': 0.1376, 'err_pct': 14.79, 'chars': '4073/4313', 'truncated': False}, {'lang': 'ES', 'name': '60s', 'sec': 60.7, 'wall_s': 7.12, 'rtf': 0.1173, 'err_pct': 3.23, 'chars': '771/764', 'truncated': False}, {'lang': 'ZH', 'name': '60s', 'sec': 63.9, 'wall_s': 3.74, 'rtf': 0.0585, 'err_pct': 27.49, 'chars': '196/501', 'truncated': True}], 'whisper_v100': [{'lang': 'EN', 'name': '60s', 'sec': 61.1, 'wall_s': 4.12, 'rtf': 0.0674, 'err_pct': 40.0, 'chars': '593/931', 'truncated': True}, {'lang': 'EN', 'name': '5min', 'sec': 305.8, 'wall_s': 10.37, 'rtf': 0.0339, 'err_pct': 50.55, 'chars': '2001/3872', 'truncated': True}, {'lang': 'FR', 'name': '60s', 'sec': 65.0, 'wall_s': 4.96, 'rtf': 0.0763, 'err_pct': 0.0, 'chars': '1121/1107', 'truncated': False}, {'lang': 'FR', 'name': '5min', 'sec': 297.2, 'wall_s': 13.34, 'rtf': 0.0449, 'err_pct': 32.01, 'chars': '3225/4313', 'truncated': True}, {'lang': 'ES', 'name': '60s', 'sec': 60.7, 'wall_s': 4.25, 'rtf': 0.07, 'err_pct': 3.23, 'chars': '776/764', 'truncated': False}, {'lang': 'ZH', 'name': '60s', 'sec': 63.9, 'wall_s': 1.95, 'rtf': 0.0305, 'err_pct': 54.18, 'chars': '129/501', 'truncated': True}], 'ane': [{'lang': 'EN', 'name': '60s', 'sec': 61.1, 'wall_s': 1.65, 'rtf': 0.0269, 'err_pct': 6.0, 'chars': '979/931', 'truncated': False}, {'lang': 'EN', 'name': '5min', 'sec': 305.8, 'wall_s': 2.53, 'rtf': 0.0083, 'err_pct': 11.7, 'chars': '4112/3872', 'truncated': False}, {'lang': 'FR', 'name': '60s', 'sec': 65.0, 'wall_s': 1.41, 'rtf': 0.0216, 'err_pct': 0.58, 'chars': '1125/1107', 'truncated': False}, {'lang': 'FR', 'name': '5min', 'sec': 297.2, 'wall_s': 3.02, 'rtf': 0.0102, 'err_pct': 12.09, 'chars': '4302/4313', 'truncated': False}, {'lang': 'ES', 'name': '60s', 'sec': 60.7, 'wall_s': 1.47, 'rtf': 0.0242, 'err_pct': 4.84, 'chars': '766/764', 'truncated': False}, {'lang': 'ZH', 'name': '60s', 'sec': 63.9, 'wall_s': 6.34, 'rtf': 0.0993, 'err_pct': 5.98, 'chars': '261/501', 'truncated': True}]} |
| language_autodetect | {'rumble_all_correct': True, 'detail': [{'truth': 'EN', 'raw': 'language English<asr_text>The UN also hopes to finalise a fund to help countries', 'gen_s': 1.16}, {'truth': 'FR', 'raw': "language French<asr_text>L'ONU espère également finaliser un fonds pour aider le", 'gen_s': 1.39}, {'truth': 'ES', 'raw': 'language Spanish<asr_text>Argentina es famosa por contar con uno de los mejores ', 'gen_s': 0.84}, {'truth': 'ZH', 'raw': 'language Chinese<asr_text>联合国还希望最终成立一项基金，帮助有关国家应对全球变暖的影响。', 'gen_s': 1.16}]} |
| groq_production_reference_ms | {'p50': 446, 'p95': 916, 'max': 1736, 'n': 6094, 'fail': 32, 'note': 'p50/p95/max = nearest-rank on the last 60 successful durations in stats.json; n and fail are cumulative; failure durations not stored; last call 2026-11-19T05:43:47Z'} |

## Configuration
- prefill: n/a (audio encoder + prompt prefill folded into wall_s; prep_s reported per clip)
- decode: autoregressive, max_new_tokens=512 (clips) / 1024 (60 s) / 3072 (5 min), FP16, sdpa attention
- model_quant: FP16 weights (V100 sm_70 has no BF16); 0.5B params, 1.02 GB safetensors
- kv_cache: transformers 5.21.1 default
- turboquant: n/a
- speculative: none
- engine: transformers 5.21.1 + torch 2.14.1+cu126, AutoModelForMultimodalLM, podman container localhost/rumble-bench:1
- hardware: our server GPU0 (Tesla V100-PCIE-32GB, exclusive via flock lease, CUDA_VISIBLE_DEVICES=0); whisper baseline on GPU1 (production card, shared with Strata fn2)

## Upstream
- https://huggingface.co/Reson8/Rumble-2-Flash

Upstream code and weights keep their own licence.
