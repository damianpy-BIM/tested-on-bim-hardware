# Tested on BIM hardware

Open models and tools we ran on our own machines, with the numbers we measured and the scripts to run them yourself.
One folder per item: what it is, the hardware, the measured result (good or not), and how to reproduce it.

| Item | What | Hardware | Verdict |
|---|---|---|---|
| [qwen3.5-4b-3d-coders](qwen3.5-4b-3d-coders/) | text -> Three.js 3D asset (GLB) or scene, with a browser check and retry | 1 x NVIDIA V100 32 GB | works (GLB coder), partly (scene coder) |
| [dsh-superagent](dsh-superagent/) | DeepSeek's prototype GitHub coding agent: build + test suite in a sandbox | 64-thread x86-64 CPU | partly |
| [metal-capability-layer-for-macos-vms](metal-capability-layer-for-macos-vms/) | Process-scoped Metal capability layer enabling GPU acceleration for AI models on | Apple M5 Max MacBook Pro, macOS guest VM | works |
| [apple-neural-engine-training-compiler](apple-neural-engine-training-compiler/) | Compiler and framework enabling neural network training on Apple Neural Engine ( | Apple M4 Mac mini | works |
| [thermite](thermite/) |  | 64-thread x86-64 CPU | partly |
| [autoresearch-mlx](autoresearch-mlx/) | Native Apple Silicon MLX port of Karpathy's autoresearch | Apple M4 Mac mini | works |
| [icloud-s3](icloud-s3/) | Rust tool to sync or backup iCloud data to Amazon S3 | 64-thread x86-64 CPU | works |
| [qwen4-open-weight-models](qwen4-open-weight-models/) | Open-weight Qwen4 LLM weights likely for local/self-hosted inference. | 1x NVIDIA V100 32 GB | works |
| [ltx-2.3-uncensored](ltx-2.3-uncensored/) | Text-to-video and image-to-video generation model | 1x NVIDIA V100 32 GB | works |
| [macaq](macaq/) | Open-source quantization tool for LLMs/multimodal models that produces GGUF/vLLM | 1x NVIDIA Tesla V100 32 GB | partly |
| [rumble-2-flash](rumble-2-flash/) | 0.5B open-weight speech-to-text (Qwen3-ASR fine-tune, arch qwen3_asr) for accent | 1x NVIDIA Tesla V100 32 GB | partly |
| [esp-mosaico](esp-mosaico/) | GitHub starter repo with MCP/Claude Code/Codex configs and simulator for ESP32-S | CPU only, on the NVIDIA Tesla V100 server | works |
| [agent-desktop](agent-desktop/) | Agent framework for parallel computer automation across macOS, Windows, and Linu | CPU only, on the NVIDIA Tesla V100 server | works |
| [strata-engine](strata-engine/) | LLM inference engine version 0.1.60 with a prefill performance regression on V10 | 1x NVIDIA Tesla V100 32 GB | partly |
| [gemma-4](gemma-4/) | A local AI model the post suggests running for sensitive company data. | 1x NVIDIA Tesla V100 32 GB | works |
| [deepseek-v4.1-flash](deepseek-v4.1-flash/) | DeepSeek-V4.1-Flash model quantized to run locally on 12GB GPU | 10x NVIDIA Tesla V100 32 GB | works |
| [deepseek-v4.1-flash-1017-gsq-rco-coder](deepseek-v4.1-flash-1017-gsq-rco-coder/) | Quantized/pruned 551.9B parameter code generation model compressed to 72.1GB GGU | 10x NVIDIA Tesla V100 32 GB | works |
| [imagination-studio](imagination-studio/) | All-in-one creative studio with 61+ integrated apps for video, music, audio, vis | 1x NVIDIA Tesla V100 32 GB | partly |
| [harnessrouter](harnessrouter/) | Open-source infrastructure layer that standardizes routing and execution of task | CPU only, on the NVIDIA Tesla V100 server | works |
| [qwopus3.8-27b-coder-flash](qwopus3.8-27b-coder-flash/) | 27B coding and reasoning model fine-tuned on 200K examples with 20K agent intera | 10x NVIDIA Tesla V100 32 GB | works |
| [llama.cpp](llama.cpp/) | C++ inference engine for LLMs with CPU/GPU support and quantization | CPU only, on the NVIDIA Tesla V100 server | works |
| [adcode](adcode/) | iOS/macOS app for running local AI coding models (GLM, Qwen, etc.) without API k | CPU only, on the NVIDIA Tesla V100 server | partly |

Rules for this repository: figures are measured, never estimated, and come with the hardware, quantisation, engine and context
they were measured with. Upstream code and weights are linked, not copied, and keep their own licence. Our scripts are MIT.

Hardware and more results: https://www.bim-computing.com
