# Metal capability layer for macOS VMs

**What it is.** Process-scoped Metal capability layer enabling GPU acceleration for AI models on macOS virtual machines

**Verdict: works.** Inside the macOS guest VM on the M5 Max MacBook, the Cua Metal capability shim made llama.cpp 12.5x faster on prefill and 21.1x faster on decode (TinyLlama 1.1B Q4_K_M). Useful for LLM work inside our macOS VMs.

**Hardware:** Apple M5 Max MacBook Pro, macOS guest VM

## Measured
| Metric | Value |
|---|---|
| prefill stock VM (512 tokens) | 511.17 tok/s |
| prefill with shim (512 tokens) | 6389.10 tok/s |
| decode stock VM (128 tokens) | 17.12 tok/s |
| decode with shim (128 tokens) | 361.99 tok/s |
| prefill speedup | 12.50x |
| decode speedup | 21.14x |
| reported Apple GPU family 9 | no -> yes |
| max threadgroup memory | 32768 B -> 65536 B |

## Configuration
- prefill: 6389.10 tok/s with shim, 511.17 tok/s stock (512-token prompt)
- decode: 361.99 tok/s with shim, 17.12 tok/s stock (128 tokens generated)
- model_quant: tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf (Q4_K_M)
- kv_cache: f16, 640 tokens
- turboquant: no
- speculative: no
- engine: llama.cpp b10167 official macOS arm64 release, Metal backend, llama-bench -p 512 -n 128 -r 10 -t 8 -ngl -1 (medians of 10)
- hardware: Apple M5 Max MacBook Pro host, macOS 26.5 guest VM (UTM, Apple Virtualization, 10 vCPU, 16 GB), Apple Paravirtual GPU


## Default-on variant (our modification)
`LumeMetalCapabilities-lazy.m` links libobjc only and installs the hook when Metal loads, so it can sit in
`DYLD_INSERT_LIBRARIES` for every process at no cost (empty program 1.47 ms -> 1.44 ms; the upstream build adds about 5 ms per
process). `metal-shim on|off|status` (run with sudo inside a macOS guest VM) installs it in /usr/local/lib and exports it from
/etc/zshenv. With it on, llama.cpp b10167 TinyLlama Q4_K_M ran with no prefix at 6347 tok/s prefill (512 tokens) and
362 tok/s decode (128 tokens), against 511 tok/s and 17 tok/s stock.

Limits: launchd drops DYLD_* (apps opened from the Dock never get it); hardened or notarized apps ignore it; SIP clears it for
children of /bin/sh, bash, /usr/bin/python3 and make. Linux containers have no Metal. A DYLD_INSERT_LIBRARIES path that does
not exist kills every process: the zshenv line checks the file and `off` never deletes it.
