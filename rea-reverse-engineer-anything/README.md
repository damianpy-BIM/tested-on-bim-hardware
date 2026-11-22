# REA (Reverse Engineer Anything)

**What it is.** Open-source reverse-engineering toolkit for decompiling binaries and tracing execution via MCP and CLI

**Verdict: works.** REA CLI (npm rea-agents 6.9.0) with the free Kuna 1.1001 provider decompiled a small ELF x86-64 binary on pure CPU and returned exact, evidence-stamped pseudocode, xrefs and string search — a ready-made RE layer for AI agents, no GPU, no LLM, no account.

**Hardware:** CPU only, on the NVIDIA Tesla V100 server

## Measured
| Metric | Value |
|---|---|
| engine_overhead_is_rea_not_decompiler | True |
| rea_decompile_fnv1a_wall_s | 17.11 |
| rea_decompile_parse_port_wall_s | 17.35 |
| rea_decompile_main_wall_s | 14.96 |
| rea_analyze_inventory_wall_s | 10.58 |
| rea_xrefs_wall_s | 9.6 |
| rea_search_wall_s | 8.46 |
| rea_function_summary_dossier_wall_s | 14.18 |
| rea_decompile_stripped_0x1300_wall_s | 10.27 |
| rea_hardening_inspect_wall_s | 2.67 |
| rea_elf_notes_wall_s | 4.08 |
| rea_layout_pwntools_wall_s | 4.46 |
| rea_doctor_wall_s | 6.31 |
| rea_max_rss_MB | 308 |
| kuna_alone_decompile_wall_s_range | [0.15, 0.21] |
| kuna_alone_max_rss_MB | 78 |
| rea_per_call_overhead_vs_kuna_alone_s_range | [6, 17] |
| npm_install_time_s | 23 |
| npm_packages_installed | 30 |
| node_modules_MB | 327 |
| kuna_exe_MB | 56 |
| pwnenv_venv_MB | 236 |
| test_binary_bytes | 16128 |
| test_binary_functions_found | 15 |
| test_binary_functions_expected | 15 |
| test_binary_strings_found | 20 |
| quality_functions_exact_out_of_tested | 3 of 3 named functions (fnv1a, parse_port, main) match demo.c line-by-line: FNV constants 0xcbf29ce484222325/0x100000001b3, parse_port returns -1/-2/-3, main recovers parse_port/fnv1a/strncpy/__printf_chk calls, mix constant 0x9e3779b97f4a7c15 and magic divide by 251 |
| stripped_binary_recovered | identical pseudocode at 0x1300 renamed sub_1300 |
| xrefs_result | 1 caller site 0x1141 (the real call inside main) |
| search_result | string 'entries=%d mix=%llu\n' found at 0x2004 with encoding and 21-byte length |
| evidence_provenance | sha256 of subject + evidence_id + provider id/version + limitations/unknowns on every JSON output |
| install_total_downloaded_bytes_no_weights_over_100MB | 86055778 |

## Configuration
- note: no LLM speed reported — REA/Kuna contain no LLM; this config block describes the analysis engines only
- engine: REA 6.9.0 (npm rea-agents, Node.js v22.23.5) orchestrating Kuna 1.1001 (Apache-2.0 static x86-64 executable, official Noelo-Lab/kuna GitHub release)
- hardware: our server CPU slot, 64 threads, 755 GB RAM, no GPU used
- os: Ubuntu, Linux 6.8.0-147-generic
- target: gcc-13 -O2 -fno-inline ELF x86-64 PIE, 16,128 bytes
- env_vars_set: REA_KUNA_COMMAND, REA_KUNA_CACHE_DIR, REA_PWNTOOLS_PYTHON (pwntools 4.15.0/pyelftools 0.33/unicorn 2.1.2 venv)
- timings_method: GNU time wall + max RSS per command; REA internal milliseconds via --timings JSON

