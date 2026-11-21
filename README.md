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
| [ovhcloud-cli](ovhcloud-cli/) | Command-line interface for managing OVHcloud cloud infrastructure and services | CPU only, on the NVIDIA Tesla V100 server | works |
| [open-scion](open-scion/) | A Git replacement with partial clones, server-side operations, merge features, a | CPU only, on the NVIDIA Tesla V100 server | works |
| [paranoid-pi](paranoid-pi/) | Privacy-focused LLM daemon wrapper with Tor circuits, cover traffic, zkAPI, and  | CPU only, on the NVIDIA Tesla V100 server | partly |
| [mercury-agent](mercury-agent/) | Multi-agent orchestration framework with bot coordination, sandboxing, and backg | CPU only, on the NVIDIA Tesla V100 server | works |
| [claude-code](claude-code/) | Anthropic's CLI coding agent for automated software development | CPU only, on the NVIDIA Tesla V100 server | works |
| [superfluid](superfluid/) | Inference orchestration layer that prioritizes interactive requests over backgro | CPU only, on the NVIDIA Tesla V100 server | works |
| [claude-motion](claude-motion/) | Motion graphics framework using Claude Opus 5.5 to generate and validate video f | CPU only, on the NVIDIA Tesla V100 server | works |
| [ods](ods/) | One-click Local AI platform that detects hardware, downloads appropriate models, | CPU only, on the NVIDIA Tesla V100 server | partly |
| [tinygrad](tinygrad/) | Minimal machine learning framework/compiler for running models on heterogeneous  | CPU only, on the NVIDIA Tesla V100 server | partly |
| [hyperframes](hyperframes/) | AI agent video rendering tool that converts HTML animations to MP4 | CPU only, on the NVIDIA Tesla V100 server | works |
| [agent-reach](agent-reach/) | CLI tool that gives AI agents web scraping and search capabilities across Twitte | CPU only, on the NVIDIA Tesla V100 server | works |
| [fastframes-l-on-a-16-gb-apple-m4](fastframes-l-on-a-16-gb-apple-m4/) | Apple's open video model, 81 frames at 480p from one model per frame | Apple M4 Mac mini | cannot-run |
| [fastframes-l](fastframes-l/) | Apple 14.3B autoregressive video diffusion generating 832x480 clips | 1x NVIDIA Tesla V100 32 GB + Apple M5 Max 128 GB | works |
| [opencode-lora-on-aeon-27b](opencode-lora-on-aeon-27b/) | RL-trained ~300MB LoRA for Qwen3.8-27B optimised for OpenCode, applied at runtim | 1x NVIDIA Tesla V100 32 GB | works |
| [openworker](openworker/) | Desktop AI coworker that runs locally and produces finished documents (e.g. secu | CPU only, on the NVIDIA Tesla V100 server | partly |
| [docetl](docetl/) | Python library/CLI for building agentic LLM-powered data processing and ETL pipe | CPU only, on the NVIDIA Tesla V100 server | works |
| [wicked-tutu-31b-v0.1](wicked-tutu-31b-v0.1/) | 31B uncensored LLM fine-tuned (high-rank LoRA) for dark fiction / unfiltered rol | 1x NVIDIA Tesla V100 32 GB | works |
| [anydoc](anydoc/) | Rust CLI/library converting 14 doc formats (docx, pptx, xlsx, PDF, epub, rtf...) | CPU only, on the NVIDIA Tesla V100 server | works |
| [termix](termix/) | self-hosted web app for managing SSH connections: terminal, tunnels, snippets, h | CPU only, on the NVIDIA Tesla V100 server | works |
| [sentrysearch](sentrysearch/) | Semantic search over long video footage: describe a moment in natural language a | 1x NVIDIA Tesla V100 32 GB | works |
| [minicpm-v-4.7](minicpm-v-4.7/) | 35B-A3B MoE multimodal (vision-language) model for document parsing, sign readin | 1x NVIDIA Tesla V100 32 GB | works |
| [obsidian-mind](obsidian-mind/) | Gives AI coding agents (Claude Code, Codex CLI, Gemini CLI) persistent memory vi | CPU only, on the NVIDIA Tesla V100 server | works |
| [unlimited-ocr](unlimited-ocr/) | 3B-param OCR model that parses 100-page PDFs in one pass with 32K context, multi | 1x NVIDIA Tesla V100 32 GB | cannot-run |
| [rmux](rmux/) | Rust terminal multiplexer, tmux-compatible, keeps SSH sessions alive, with SDK f | CPU only, on the NVIDIA Tesla V100 server | works |
| [gortex](gortex/) | Code graph indexer exposed via CLI/MCP/web UI to cut AI coding agent token usage | CPU only, on the NVIDIA Tesla V100 server | works |
| [voicebox](voicebox/) | Local voice cloning + multi-engine TTS app (7 TTS engines, 23 languages, MCP ser | CPU only, on the NVIDIA Tesla V100 server | works |
| [portable-ai-usb](portable-ai-usb/) | Toolkit/scripts to run large uncensored AI models (likely via llama.cpp) self-co | CPU only, on the NVIDIA Tesla V100 server | works |
| [kaneo](kaneo/) | self-hosted minimal project management tool (Docker Compose + PostgreSQL) | CPU only, on the NVIDIA Tesla V100 server | works |
| [mission-control](mission-control/) | self-hosted local dashboard for delegating, prioritizing and supervising tasks a | CPU only, on the NVIDIA Tesla V100 server | works |
| [scrapling](scrapling/) | Python web scraping framework with adaptive selectors and anti-bot bypass | CPU only, on the NVIDIA Tesla V100 server | works |
| [lightpanda](lightpanda/) | headless browser written in Zig, built for AI agents/scraping, faster and lighte | CPU only, on the NVIDIA Tesla V100 server | works |
| [heretic](heretic/) | Automated tool that abliterates/decensors LLMs (removes refusal behavior) in one | CPU only, on the NVIDIA Tesla V100 server | works |
| [open-source-2b-tts-zero-shot-voice-clone](open-source-2b-tts-zero-shot-voice-clone/) | 2B-param TTS model with zero-shot voice cloning, 48kHz output, 30+ languages inc | 1x NVIDIA Tesla V100 32 GB | works |

Rules for this repository: figures are measured, never estimated, and come with the hardware, quantisation, engine and context
they were measured with. Upstream code and weights are linked, not copied, and keep their own licence. Our scripts are MIT.

Hardware and more results: https://www.bim-computing.com
