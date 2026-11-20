# DocETL

**What it is.** Python library/CLI for building agentic LLM-powered data processing and ETL pipelines over documents

**Verdict: works.** DocETL 0.3.0 works as a CPU client: map then reduce on 3 sample docs against already-served Strata (Qwen3.8 Flash-Next IQ3_S) extracted and summarized every document correctly at 0.00 USD. No GPU was needed in the library (no torch, CUDA, vLLM, or llama.cpp dependency); the LLM stays on the existing Strata process.

**Hardware:** CPU only, on the NVIDIA Tesla V100 server

## Measured
| Metric | Value |
|---|---|
| pipeline wall time | 83.51 s |
| documents in | 3 documents |
| map calls | 3 calls |
| reduce calls | 3 calls |
| extract fields correct | 3/3 documents |
| reduce groups correct | 3/3 groups |
| endpoint cost | 0.00 USD |
| prefill prompt 1 | 159.4 tok/s (194 prompt tokens) |
| prefill prompt 2 | 207.5 tok/s (184 prompt tokens) |
| prefill prompt 3 | 229.3 tok/s (187 prompt tokens) |
| decode prompt 1 | 66.5 tok/s (34 output tokens) |
| decode prompt 2 | 79.9 tok/s (24 output tokens) |
| decode prompt 3 | 73.7 tok/s (28 output tokens) |
| speculative draft accepted prompt 1 | 28 of 30 draft tokens |
| speculative draft accepted prompt 2 | 19 of 25 draft tokens |
| speculative draft accepted prompt 3 | 21 of 26 draft tokens |
| DocETL process GPU memory | 0 MiB |
| serving GPU 5 resident VRAM | 32028 MiB of 32768 MiB (pre-existing Strata process, not allocated by this test) |

## Configuration
- prefill: 159.4 tok/s (194 prompt tokens); 207.5 tok/s (184 prompt tokens); 229.3 tok/s (187 prompt tokens)
- decode: 66.5 tok/s (34 output tokens); 79.9 tok/s (24 output tokens); 73.7 tok/s (28 output tokens); server n_ctx 262144 tokens
- model_quant: IQ3_S (Qwen3.8-Flash-Next-GSQ-RCO-abliterated)
- kv_cache: int8, 262144 tokens (kv-resident 32768 tokens)
- turboquant: no
- speculative: DFlash
- engine: Strata 0.1.56 (component engine, CUDA 12, --spec 4, drafting dflash2, --mtp)
- hardware: our server Tesla V100-PCIE-32GB sm_70 GPU 5 already serving; DocETL 0.3.0 client on CPU (64 threads, no torch)

## Upstream
- https://github.com/ucbepic/docetl

Upstream code and weights keep their own licence.
