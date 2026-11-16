# autoresearch-mlx

**What it is.** Native Apple Silicon MLX port of Karpathy's autoresearch

**Verdict: works.** Native MLX port of Karpathy's autoresearch runs cleanly on Apple Silicon, no PyTorch/CUDA: full prep+train loop completed in 7.7 min, peak 7.5GB on a 16GB Mac mini M4.

**Hardware:** Apple M4 Mac mini

## Measured
| Metric | Value |
|---|---|
| data_prep_time_s | 20.1 |
| model_compile_time_s | 30.7 |
| training_wall_time_s | 410.4 |
| eval_time_s | 18.2 |
| total_run_time_s | 459.5 |
| training_steps | 4 |
| training_throughput_tok_s | 433-932 |
| val_bpb | 2.735677 |
| peak_unified_memory_mb | 7512.5 |
| model_params_M | 11.5 |
| data_downloaded_mb | 291 |

## Configuration
- prefill: n/a (training loop, not inference)
- decode: 433-932 tok/s (training fwd+bwd, 2048 ctx, 4 steps)
- model_quant: fp32 (MLX default, repo does not quantize)
- kv_cache: n/a (training only, no KV cache), seq_len 2048
- turboquant: no
- speculative: no
- engine: MLX (native Apple Silicon)
- hardware: Mac mini M4, 16GB unified memory

## Upstream
- https://github.com/trevin-creator/autoresearch-mlx

Upstream code and weights keep their own licence.
