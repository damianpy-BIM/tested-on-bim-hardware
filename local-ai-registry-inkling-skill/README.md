# local-ai-registry (Inkling skill)

**What it is.** Registry and agent skill that lets any LLM agent set up and run the new 'Inkling' model locally on a 24GB+ device, with results pushed to a shoutout page

**Verdict: works.** Inkling-2-Small UD-Q4_K_XL loads on GPU0 with routed experts on CPU and answers three prompts; warm decode is 1.049 tok/s.

**Hardware:** 1x NVIDIA Tesla V100 32 GB

## Measured
| Metric | Value |
|---|---|
| load time | 1378.213 s |
| host RSS | 324.732 GB |
| GPU0 llama-server memory | 11542 MiB |
| GPU0 memory at first health ok | 13508 MiB |
| weights on disk | 354150089945 bytes |
| prefill tok/s (27 prompt tokens, request 1, graph alloc) | 0.0345 tok/s |
| decode tok/s (5 tokens, context 32 tokens, request 1) | 0.156 tok/s |
| prefill tok/s (60 prompt tokens, request 2) | 0.704 tok/s |
| decode tok/s (38 tokens, context 98 tokens, request 2) | 0.567 tok/s |
| prefill tok/s (58 prompt tokens, request 3) | 1.486 tok/s |
| decode tok/s (38 tokens, context 96 tokens, request 3) | 1.049 tok/s |

## Configuration
- prefill: 1.486 tok/s (58 prompt tokens)
- decode: 1.049 tok/s (96 tokens context)
- model_quant: UD-Q4_K_XL
- kv_cache: f16, 8192 tokens
- turboquant: no
- speculative: no
- engine: llama.cpp llama-server 0.9.0-dev fork a45f662, experts on CPU, -ub 2048, -t 32, -fa on, -lm none
- hardware: our server GPU0 Tesla V100-PCIE-32GB sm_70, CUDA 12.9, RAM offload, GLiDE 0.4B resident on the same card

## Upstream
- https://github.com/sybil-solutions/local-ai-registry

Upstream code and weights keep their own licence.
