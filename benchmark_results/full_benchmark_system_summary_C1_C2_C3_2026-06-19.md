# Full Benchmark System Summary

**Date:** 2026-06-19  
**Scope:** C1, C2, and C3 full benchmark runs  
**Question set:** 40 frozen questions  
**Repetitions:** 3 per question  
**Total answers per model:** 120  
**Corpus:** D1-D4 final benchmark corpus  
**Backend settings:** `k=10`, `n=3`, `temperature=0.2`, `max_tokens=200`  
**llama.cpp settings:** `--ctx-size 4096 --parallel 1 --cache-ram 0 --no-cache-prompt --ctx-checkpoints 0`

## Completed Runs

| Config | Model | Run Folder | Answers | Raw JSON | Errors | Status |
|---|---|---|---:|---:|---:|---|
| C1 | Qwen2.5 0.5B Instruct Q4_K_M | `full_benchmark_C1_20260619_224126` | 120 | 120 | 0 | completed |
| C2 | Llama 3.2 1B Instruct Q4_K_M | `full_benchmark_C2_20260619_225653` | 120 | 120 | 0 | completed |
| C3 | Gemma 3 1B IT Q4_K_M | `full_benchmark_C3_20260619_231534` | 120 | 120 | 0 | completed |

The earlier `full_benchmark_C1_20260619_223429` and `full_benchmark_C1_20260619_224035` folders are one-question smoke tests, not final full benchmark runs.

## System Metrics

| Config | Model Size (MB) | Mean Latency (s) | Min-Max Latency (s) | Mean Peak Memory (MiB) | Mean Tokens/s |
|---|---:|---:|---:|---:|---:|
| C1 | 468.64 | 3.738 | 2.760-4.947 | 566.28 | 114.27 |
| C2 | 770.28 | 5.127 | 2.957-6.009 | 1479.27 | 77.20 |
| C3 | 768.72 | 5.793 | 3.683-7.318 | 1001.03 | 61.35 |

## Initial Interpretation

C1 is the strongest efficiency baseline: it has the lowest model size, lowest latency, lowest memory use, and highest throughput.

C2 is slower and uses the most memory in these runs. Its memory estimate is much higher than C3 despite similar model file size, so this should be noted in the deployment-practicality discussion.

C3 is the slowest and has the lowest throughput, but the mini pilot suggested better answer quality. Its final value depends on manual scoring of `answer_scoring.csv`.

## Next Step

The system metrics are ready. The next major task is manual quality scoring for the three full benchmark runs:

- `full_benchmark_C1_20260619_224126/answer_scoring.csv`
- `full_benchmark_C2_20260619_225653/answer_scoring.csv`
- `full_benchmark_C3_20260619_231534/answer_scoring.csv`

After scoring, combine quality and system metrics into the final Results tables.
