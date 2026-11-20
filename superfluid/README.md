# Superfluid

**What it is.** Inference orchestration layer that prioritizes interactive requests over background agents to reduce latency

**Verdict: works.** Verified on a V100: with 8 agents each streaming ~6,000-token documents, an interactive request with header x-superfluid-qos:interactive got its first token in 0.736 s (repeat 0.991 s) vs 31.6 s without the header and 34.7 s for llama-server on the identical build — but single-stream speed halves (65 vs 124 decode tok/s) and agent queue wall time roughly doubles, so QoS is bought with throughput.

**Hardware:** CPU only, on the NVIDIA Tesla V100 server

## Measured
| Metric | Value |
|---|---|
| interactive_ttft_under_8_agent_load | 0.736 s (Superfluid + qos header, pass 1); 0.991 s (repeat pass); 31.617 s (Superfluid, no header); 34.684 s (llama-server baseline) |
| idle_interactive_ttft | 0.243 s Superfluid vs 0.110 s llama-server |
| agent_ttft_p50 | 33.5-47.0 s across Superfluid passes; 14.0-15.8 s llama-server |
| agent_queue_wall_8_agents | 78.2-108.1 s Superfluid passes vs 35.6-38.9 s llama-server; 0 agents failed, max stall 22.8 s (limit 30 s) |
| prefill_speed | 2,212 tok/s Superfluid vs 3,457 tok/s llama-server (3,501-token prompt, single stream, V100) |
| decode_speed | 65.2 tok/s Superfluid vs 123.6 tok/s llama-server (256 tokens, single stream) |
| model_load_time | 3.8 s Superfluid vs 3.4 s llama-server |
| vram_used | 7,534 MiB Superfluid vs 9,912 MiB llama-server on GPU0 during generation (2.7 GB Q4_K_M weights) |
| quality | 3/3 acceptable on both servers (fizzbuzz self-corrected, bat-and-ball $0.05 correct, JSON extract correct); outputs byte-identical across systems at temp 0 seed 1 |

## Configuration
- prefill: 2,212 tok/s measured under Superfluid vs 3,457 tok/s llama-server baseline, single stream, batch 8 lanes available
- decode: 65.2 tok/s measured under Superfluid vs 123.6 tok/s llama-server baseline, single stream
- model_quant: Q4_K_M (GGUF, qwen35 hybrid SSM, 2,708,804,096 bytes)
- kv_cache: f16 cache-type-k/v, KV offload on, 8 lanes x 8,192 ctx (Superfluid); llama-server baseline unified KV -kvu per-slot 8,192 x 8 slots
- turboquant: none (suite passes f16 cache types)
- speculative: off (--speculate off)
- engine: Superfluid v0.2.0 daemon + llama.cpp worker b12535-cuda-12.8; baseline llama-server b12535-cuda-12.8 (same build, installed by Superfluid's runtime installer)
- hardware: our server GPU0, Tesla V100-PCIE-32GB (sm_70, no BF16), CUDA 12.9 host / 12.8 runtime, driver 580.178.04

