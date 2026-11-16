# icloud-s3

**What it is.** Rust tool to sync or backup iCloud data to Amazon S3

**Verdict: works.** icloud-s3 builds in 44 s and passes 10/10 conformance evals with bit-exact boto3 S3 roundtrips (up to 79.5 MB/s GET) and bit-exact cold-boot replay on CPU-only Linux, but real iCloud Shared Album import needs macOS Photos.app, and it is self-declared satire — a fun Rust hack, not a BIM-grade store.

**Hardware:** 64-thread x86-64 CPU

## Measured
| Metric | Value |
|---|---|
| build_time_release | 43.58 s wall (64 threads, cargo 1.100.0) |
| binary_size | 10.3 MB |
| conformance_evals | 10/10 PASS in 5.32 s |
| boto3_put_get_p50_1KiB | 4.39 ms / 3.69 ms, bit-exact |
| boto3_put_get_p50_64KiB | 5.23 ms / 3.90 ms = 12.5 / 16.8 MB/s, bit-exact |
| boto3_put_get_p50_1MiB | 42.67 ms / 19.89 ms = 24.6 / 52.7 MB/s, bit-exact |
| boto3_put_get_p50_5MiB_3frame_burst | 183.54 ms / 65.92 ms = 28.6 / 79.5 MB/s, bit-exact |
| png_carrier_overhead | 1.19x (6,433,536 B raw -> 7,692,827 B PNG) |
| cold_boot_replay | 4/4 keys reconstructed from PNGs, SHA-256 match; 50-object eval replay in 77.87 ms |
| sharding_put_throughput_1_vs_8_albums | 8.1 -> 57.4 req/s (p50 986.9 -> 123.7 ms) |
| server_idle_rss | 7.7 MB |
| vram_used | 0 GB (pure CPU tool, CUDA_VISIBLE_DEVICES=) |

## Configuration
- prefill: n/a (not an LLM)
- decode: n/a (not an LLM)
- model_quant: n/a (not an LLM)
- kv_cache: n/a (not an LLM)
- turboquant: no
- speculative: no
- engine: icloud-s3 0.1.0 (Rust, axum/tokio), cargo 1.100.0 release build; client boto3 1.44.3 SigV4
- hardware: our server, 64-thread x86 CPU, 755 GB RAM, no GPU shown (CUDA_VISIBLE_DEVICES=)

## Upstream
- https://github.com/ashayas/icloud-s3

Upstream code and weights keep their own licence.
