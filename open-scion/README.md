# open_scion

**What it is.** A Git replacement with partial clones, server-side operations, merge features, and agent-focused capabilities

**Verdict: works.** Partial clone genuinely works: 'graft clone --sparse numpy/_core/' materialized exactly the 617 requested files in 0.320 s (full clone of the same 42,571-commit repo: 8.245 s; plain git clone: 23.983 s), all 617 sha256 hashes identical to the source blobs, zero files outside the prefix — useful for per-discipline checkouts of big BIM repos and for server-side history/blame/search without any checkout.

**Hardware:** CPU only, on the NVIDIA Tesla V100 server

## Measured
| Metric | Value |
|---|---|
| reference_git_clone_time | 23.983 s (git clone --no-local) |
| reference_git_clone_size | 221,098,220 bytes on disk (181,652,895 bytes of it .git) |
| full_clone_time | 8.245 s |
| full_clone_files | 2,451 files |
| full_clone_size | 79,086,386 bytes on disk (39,641,135 bytes .graft metadata) |
| full_clone_wire_bytes | 39,072,733 bytes (strace on client unix socket, incl. gRPC framing) |
| partial_clone_time | 0.320 s (--sparse numpy/_core/) |
| partial_clone_files | 617 files |
| partial_clone_size | 26,478,994 bytes on disk |
| partial_clone_wire_bytes | 13,150,091 bytes (34% of full clone's) |
| partial_vs_full_speedup | 25.8x |
| partial_vs_git_clone_speedup | 74.9x |
| partial_vs_git_clone_disk | 12.0% of reference clone's size |
| files_outside_requested_prefix | 0 files |
| content_verification_partial | 617/617 files sha256-identical to source blobs |
| content_verification_full | 2,451/2,451 files sha256-identical to source blobs |
| sparse_prefix_no_trailing_slash | identical result: 617 files, 0.320 s, 26,478,994 bytes |
| lazy_expand_time | 0.315 s via 'graft sparse doc/source' on a 0-file workspace (+5,729,998 bytes) |
| server_side_read_time | 0.052 s via 'graft cat main:README.md' from a 0-file workspace |
| warm_clone_time | 1.258 s vs 8.245 s cold (6.6x; 2,425 cache object hits, 0 misses) |
| cache_tier_after_runs | hit rate 43.3%, 39,486,030 bytes / 2,425 entries, 0 verify failures |
| server_side_blame_time | 0.582 s, matches git blame commit-for-commit (git blame: 0.343 s) |
| server_side_search_time | 0.066 s for 50 'ndarray' hits (git grep: 0.042 s) |
| submodule_gitlinks_skipped | 4 of the repo's 7 gitlinks fall inside numpy/_core (empty content; explains 617 vs 621 count delta) |
| test_repo | 42,571 commits, 2,451 files, 39,445,251 bytes of content (numpy snapshot, tip 85c4843a) |

## Configuration
- prefill: n/a (not an LLM benchmark)
- decode: n/a
- model_quant: n/a
- kv_cache: n/a
- turboquant: no
- speculative: n/a
- engine: git-ai (Graft) v0.4.2 built from source: gitaly serve standalone + graft-cache daemon tier (2 GiB), token auth, unix-socket gRPC
- hardware: our server, CPU only (64 threads, 755 GB RAM; built -j 16), no GPU claimed

