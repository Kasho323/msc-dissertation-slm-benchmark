# Full Benchmark Blind Scoring and Audit Summary

**Created:** 2026-06-20
**Randomisation seed:** `20260620`

## Generated Files

- Blind scoring CSV: `full_benchmark_blind_scoring_C1_C2_C3_2026-06-20.csv`
- Rep-1-only blind scoring CSV: `full_benchmark_blind_scoring_rep1_only_C1_C2_C3_2026-06-20.csv`
- Blind model key: `full_benchmark_blind_model_key_C1_C2_C3_2026-06-20.csv`
- Finish reason audit: `full_benchmark_finish_reason_audit_C1_C2_C3_2026-06-20.csv`
- Source consistency audit: `full_benchmark_source_consistency_audit_C1_C2_C3_2026-06-20.csv`
- Source consistency summary: `full_benchmark_source_consistency_summary_C1_C2_C3_2026-06-20.csv`
- Memory sanity audit: `full_benchmark_memory_sanity_audit_C1_C2_C3_2026-06-20.csv`

## Blind Scoring

- Rows: 360
- Rep-1-only rows: 120
- Model identifiers are hidden behind random blind codes.
- Row order is shuffled.
- Latency, memory, and throughput are excluded from the blind scoring sheet to reduce scoring bias.
- Do not open the blind model key until after scoring is completed.

## Finish Reason Audit

| Model | stop | length | other/blank | total |
|---|---:|---:|---:|---:|
| C1 | 96 | 24 | 0 | 120 |
| C2 | 26 | 94 | 0 | 120 |
| C3 | 58 | 62 | 0 | 120 |

## Source Consistency Audit

- Questions checked: 40
- Questions with inconsistent retrieved source signatures: 16
- Inconsistent question IDs: Q002, Q006, Q007, Q008, Q009, Q014, Q016, Q018, Q019, Q024, Q025, Q027, Q028, Q032, Q036, Q037

## Memory Sanity Note

The existing `peak_memory_mb` field should be interpreted as an observed llama-server process RSS estimate after each request, not as a true peak-memory profiler measurement.

| Model | Mean observed RSS MiB | Min | Max | Rows |
|---|---:|---:|---:|---:|
| C1 | 566.28 | 553.61 | 568.36 | 120 |
| C2 | 1479.27 | 1470.00 | 1480.65 | 120 |
| C3 | 1001.03 | 998.44 | 1001.40 | 120 |

## Seed and Reproducibility Note

The C1-C3 full benchmark runs did not specify an explicit generation seed in llama.cpp. This should be reported as `seed not specified`. The three repetitions per question still provide repeated observations under the same temperature and prompt settings, but the runs are not bit-level reproducible from a recorded seed.

For C4/C5, use the same seed policy as C1-C3 unless the protocol is explicitly amended and the earlier models are rerun.
