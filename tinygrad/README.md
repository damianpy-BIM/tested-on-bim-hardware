# tinygrad

**What it is.** Minimal machine learning framework/compiler for running models on heterogeneous hardware.

**Verdict: partly.** tinygrad 0.14.0 runs correct MatMuls and real training on this machine: out of the box on GPU0 (V100, sm_70) via CUDA/NVRTC and OpenCL, and on CPU only after setting DEV=CPU:LLVM (its default CPU renderer needs a clang binary this box lacks); throughput is far below the serving engines already on the V100 fleet, so it is not useful for BIM.

**Hardware:** CPU only, on the NVIDIA Tesla V100 server

## Measured
| Metric | Value |
|---|---|
| GPU0 CUDA fp32 matmul N=1024 | 99.1 GFLOP/s (median 21.67 ms, 5 warm reps) |
| GPU0 CUDA fp32 matmul N=2048 | 534.8 GFLOP/s (median 32.12 ms, 3 warm reps) |
| GPU0 CUDA fp32 matmul N=4096 | 1185.2 GFLOP/s (median 115.97 ms); 921.9 GFLOP/s in a repeat run (median 149.09 ms) |
| GPU0 CUDA fp16 matmul N=4096 | 2022.6 GFLOP/s (median 67.95 ms, 3 warm reps) |
| GPU0 OpenCL fp32 matmul N=1024 | 178.6 GFLOP/s (median 12.02 ms) |
| CPU LLVM fp32 matmul N=1024 | 8.8 GFLOP/s (median 242.94 ms, single fused vectorized kernel) |
| CPU LLVM fp32 matmul N=512 | 7.0 GFLOP/s (median 38.15 ms) |
| CPU LLVM fp32 matmul N=256 | 2.9 GFLOP/s (median 11.42 ms) |
| reference numpy BLAS fp32 matmul N=1024 (CPU, 64 threads) | 143.8 GFLOP/s (median 143.77 ms-equivalent; tinygrad/BLAS ratio 0.061) |
| correctness fp32 vs numpy | max relative error 1.10e-6 to 6.91e-7 (GPU and CPU, all shapes) |
| correctness fp16 vs fp32 reference | max absolute 0.160 (fp16 rounding only; sm_70 has no BF16) |
| GPU0 VRAM peak during test | 632 MiB at fp32 N=4096; 954 MiB for the OpenCL run at N=1024 |
| host RAM peak (process RSS) | 1094.5 MiB at N=4096 GPU; 128.2 MiB at N=256 CPU |
| first kernel compile (NVRTC, GPU) | 1.604 s cold at fp32 N=1024; 2.25 s cold at fp16 N=4096 |
| first kernel compile (LLVM JIT, CPU) | 0.53 s to 1.39 s cold |
| tinygrad module import time | about 0.30 s |
| MLP forward+backward training (README LinearNet, 4 samples, 10 Adam steps, CPU) | 3.85 s wall; loss 10.2038 to 0.0060; post-train argmax matches target |
| install | pip install -e from GitHub source, 0 required runtime dependencies; tested commit 62cf281036ba (2026-11-19), version 0.14.0 |

## Configuration
- prefill: n/a (no LLM inference in this test)
- decode: n/a (no LLM inference in this test)
- model_quant: n/a (no pretrained weights; random-init fp32 and fp16 tensors)
- kv_cache: n/a (no transformer in test)
- turboquant: no
- speculative: no
- engine: tinygrad 0.14.0 (master 62cf2810): CUDA renderer via NVRTC PTX JIT + OpenCL renderer on GPU0; CPULLVMRenderer LLVM JIT (DEV=CPU:LLVM) on CPU; default CLANG CPU renderer failed (no clang binary); NV driverless backend rejected (Ampere+ only)
- hardware: our server: 64-thread Xeon CPU, 755 GB RAM; GPU0 only = Tesla V100-PCIE-32GB (sm_70, no BF16), CUDA 12.9, Python 3.12 venv

## Upstream
- https://github.com/tinygrad/tinygrad

Upstream code and weights keep their own licence.
