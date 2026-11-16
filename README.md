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

Rules for this repository: figures are measured, never estimated, and come with the hardware, quantisation, engine and context
they were measured with. Upstream code and weights are linked, not copied, and keep their own licence. Our scripts are MIT.

Hardware and more results: https://www.bim-computing.com
