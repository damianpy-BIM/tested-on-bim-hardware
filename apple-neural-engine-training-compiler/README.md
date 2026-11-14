# Apple Neural Engine Training Compiler

**What it is.** Compiler and framework enabling neural network training on Apple Neural Engine (ANE) via reverse-engineered APIs

**Verdict: works.** Real: reverse-engineered private ANE APIs run genuine backprop training on-chip, matching published benchmark numbers almost exactly, but not useful for BIM's fleet today.

**Hardware:** Apple M4 Mac mini

## Measured
| Metric | Value |
|---|---|
| ane_fp16_throughput_128x_conv_512ch_64x64 | 18.54 TOPS |
| ane_int8_throughput_128x_conv_512ch_64x64 | 34.44 TOPS |
| int8_vs_fp16_speedup | 1.86x |
| ane_peak_conv_throughput_measured | 12.00 TFLOPS |
| tiny_model_params | 7.5M |
| tiny_model_train_step_time | 6.6 ms/step |
| tiny_model_kernel_compile_time_onetime | 2292 ms |
| tiny_model_step0_loss | 6.2986 (theoretical random-init ln(512)=6.238) |
| ane_kernels_compiled | 10 |
| free_ram_during_test | 343MB to 186MB unused (of 16GB) |

## Configuration
- prefill: n/a (training benchmark, not inference)
- decode: n/a (training benchmark, not inference)
- model_quant: FP16 weights (INT8 W8A8 variant also tested, see measured)
- kv_cache: n/a (no inference run; training uses forward taps for gradient reuse)
- turboquant: no
- speculative: no
- engine: custom runtime via reverse-engineered _ANEClient/_ANECompiler private APIs, MIL generated at runtime (Objective-C), no CoreML training API, no Metal/GPU
- hardware: Apple M4, 10-core CPU, 16-core Neural Engine, 16GB unified memory (Mac mini), macOS 26.6.2

