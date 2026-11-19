# OVHcloud CLI

**What it is.** Command-line interface for managing OVHcloud cloud infrastructure and services

**Verdict: works.** Official OVHcloud CLI v0.17.2 downloads sha256-verified from GitHub and runs on CPU only (version command median 51 ms over 10 runs; the Oct-19 compromised-range v0.15.0 asset also runs, offline in a net-none container), but this fleet holds 0 OVHcloud credentials so there is nothing here for it to drive.

**Hardware:** CPU only, on the NVIDIA Tesla V100 server

## Measured
| Metric | Value |
|---|---|
| latest release tested | v0.17.2 (commit fb2127d6, built 2026-11-19T11:52:23Z) |
| version command startup | median 51 ms (min 45 ms, max 56 ms, 10 runs, warm cache) |
| help render | 46 ms, 48 top-level product commands |
| download size (official Linux x86_64 asset) | 10,114,522 bytes |
| download time | 604 ms (16.2 MiB/s) |
| sha256 checksum verification | OK for v0.17.2 x86_64 + i386 and v0.10.0 i386 against official checksums.txt |
| compromised-range v0.15.0 asset run (podman ubuntu:24.04, --network none) | runs, prints v0.15.0 / commit 760fd72d (2026-09-11); 0.94 s wall incl. container start |
| implant evidence in currently-published assets (4 binaries) | 0 (single ELF magic each, identical section tables clean vs 0.15.0 vs 0.17.2, 0 exfil hosts/IPv4 unique to 0.15.0, 0 MD5 matches vs advisory malicious list) |
| compromised releases v0.11.0-v0.15.0 assets remaining on GitHub | 4 of 10 per release, no checksums.txt (malicious assets deleted per GHSA-862f-55f5-vmvw) |
| host IOC sweep (envchecker-* temp dirs in /tmp) | 0 |
| official install.sh checksum-verification lines | 0 in 278 lines |
| OVH credentials on this fleet (vault + ssh config) | 0 |
| GPU needed | none (pure OVHcloud REST-API client; no GPU was shown to or used by the test) |

## Configuration
- hardware: our server CPU only (64 threads, 755 GB RAM); no GPU needed — the CLI only calls the OVHcloud REST API, no LLM inference involved
- software: ovhcloud CLI v0.17.2 (static Go binary, Linux x86_64 official GitHub release asset), run unauthenticated with sandboxed HOME; v0.15.0 i386 asset run in podman ubuntu:24.04 with --network none
- llm_speed: n/a (not an LLM — command-line tool test)

## Upstream
- https://github.com/ovh/ovhcloud-cli

Upstream code and weights keep their own licence.
