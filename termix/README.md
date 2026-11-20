# Termix

**What it is.** self-hosted web app for managing SSH connections: terminal, tunnels, snippets, host groups

**Verdict: works.** Termix 26.11.2 on CPU served the web UI, showed lab-sshd Online, and an SSH shell printed uid=1000(labssh) in 113 ms from the socket open.

**Hardware:** CPU only, on the NVIDIA Tesla V100 server

## Measured
| Metric | Value |
|---|---|
| termix_image_size | 808372550 bytes |
| openssh_image_size | 37980191 bytes |
| backend_startup | 137.201 s |
| http_status | 200 |
| http_get_time | 0.001259 s |
| termix_container_memory | 673.6MB |
| sshd_container_memory | 17.78MB |
| termix_cpu_at_sample | 9.32% |
| sshd_cpu_at_sample | 0.33% |
| first_ssh_prompt_with_host_key_accept | 276 ms |
| trusted_host_shell_prompt | 104 ms |
| ssh_command_after_prompt | 9 ms |
| ssh_command_from_websocket_open | 113 ms |
| command_output | TERMIX_OK_OUT; uid=1000(labssh) gid=1000(users) |
| ui_version | 26.11.2 |
| host_status | Online, 1/1 hosts |
| gpu | not used |

## Configuration
- prefill: n/a (not an LLM)
- decode: n/a (not an LLM)
- model_quant: n/a (not an LLM)
- kv_cache: n/a (not an LLM)
- turboquant: no
- speculative: no
- engine: Termix 26.11.2, image ghcr.io/termix-ssh/termix:latest, podman 4.9.3, docker-compose 2.32.4
- hardware: our server CPU, 64 threads, 755 GB RAM. No GPU: README.md and package.json have no CUDA, torch, vLLM, ROCm, or NVIDIA. GPU0 was not claimed.

## Upstream
- https://github.com/Termix-SSH/Termix

Upstream code and weights keep their own licence.
