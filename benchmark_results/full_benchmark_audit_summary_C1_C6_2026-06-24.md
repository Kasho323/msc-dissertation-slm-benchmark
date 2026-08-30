# Final C1-C6 Benchmark Audit Summary

**Created:** 2026-06-24
**Blind randomisation seed:** `20260624`
**Generation seed:** `42`
**Generation limit:** `max_tokens=512`

## Scope

- Configurations: 6
- Questions per configuration: 40
- Repetitions per question: 3
- Total generated answers: 720
- Rep-1 blind-scoring rows: 240

## System Summary

| Config | Quant | Size MiB | Mean latency s | P95 latency s | Tokens/s | Mean RSS MiB | Mean output tokens | stop | length | errors |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| C1 | Q4_K_M | 468.6 | 4.450 | 7.527 | 103.42 | 568.37 | 171.93 | 114 | 6 | 0 |
| C2 | Q4_K_M | 770.3 | 7.013 | 9.800 | 76.07 | 1479.16 | 319.18 | 105 | 15 | 0 |
| C3 | Q4_K_M | 768.7 | 6.821 | 9.835 | 67.15 | 1001.06 | 246.57 | 117 | 3 | 0 |
| C4 | Q2_K | 718.0 | 6.215 | 9.447 | 82.74 | 906.26 | 247.10 | 96 | 24 | 0 |
| C5 | Q4_K_M | 1065.6 | 4.711 | 6.210 | 62.15 | 1793.69 | 108.03 | 120 | 0 | 0 |
| C6 | Q8_0 | 1806.8 | 6.581 | 9.943 | 42.82 | 1829.38 | 129.18 | 117 | 3 | 0 |

## Retrieval Fairness

- Questions checked: 40
- Questions with inconsistent source signatures: 0
- Every question used the same retrieved source signature across all six models and repetitions.

## Repetition Consistency

- Model-question groups checked: 240
- Groups with exactly identical answers across all three repetitions: 240
- Because the generation seed was fixed, exact repetition agreement is expected. Score repetition 1 for answer quality and retain all three repetitions for system-metric variability.

## Scoring Files

- Primary human scoring file: `full_benchmark_blind_scoring_rep1_only_C1_C6_2026-06-24.csv`
- All repetitions: `full_benchmark_blind_scoring_C1_C6_2026-06-24.csv`
- Hidden model key: `full_benchmark_blind_model_key_C1_C6_2026-06-24.csv`
- Do not open the model key before human scoring is complete.

## Interpretation Rules

- System metrics are now final-run measurements, but answer-quality conclusions remain pending scoring.
- `observed_llama_server_rss_mb` is process RSS after requests, not a profiler-derived true peak.
- Compare latency alongside output length and throughput; longer answers can increase latency.
- Do not select a best model until the blinded quality scores have been combined with system metrics.
