# Scrapling

**What it is.** Python web scraping framework with adaptive selectors and anti-bot bypass

**Verdict: works.** works: Scrapling 0.5.1 returned 10 quotes in 0.331 s and passed bot.sannysoft WebDriver on CPU; useful for public-page scraping

**Hardware:** CPU only, on the NVIDIA Tesla V100 server

## Measured
| Metric | Value |
|---|---|
| Fetcher quotes HTTP status | HTTP 200 |
| Fetcher quotes extracted | 10 quotes |
| Fetcher wall time median | 0.331 s |
| Fetcher wall time run 1 | 0.602 s |
| Fetcher wall time run 2 | 0.330 s |
| Fetcher wall time run 3 | 0.331 s |
| StealthyFetcher quotes wall time | 3.628 s |
| StealthyFetcher quotes extracted | 10 quotes |
| bot.sannysoft wall time | 3.609 s |
| bot.sannysoft WebDriver | missing (passed) |
| bot.sannysoft failed cells | 1 cell (SwiftShader WebGL under forced software GL) |
| httpbin Scrapling User-Agent | Chrome/localhost |
| httpbin urllib User-Agent | Python-urllib/3.12 |
| adaptive relocated heading | Product 1 |
| parse 5000 divs median | 26.074 ms |
| parse 5000 divs repeats | 20 repeats |
| GPU0 memory delta | 0 MiB |

## Configuration
- prefill: n/a (not an LLM)
- decode: n/a (not an LLM)
- model_quant: n/a (not an LLM)
- kv_cache: n/a, n/a
- turboquant: no
- speculative: no
- engine: Scrapling 0.5.1 + curl_cffi 0.17.0 + patchright 1.64.4 Chromium localhost
- hardware: our server CPU (64 threads, 755 GB RAM); GPU0 not used, memory.used 1318 MiB before and after

## Upstream
- https://github.com/D4Vinci/Scrapling

Upstream code and weights keep their own licence.
