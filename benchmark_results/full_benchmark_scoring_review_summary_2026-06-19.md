# Full Benchmark Scoring Review Summary

**Created:** 2026-06-19

This file describes the combined scoring review sheet generated from the full C1/C2/C3 benchmark runs.

## Output

- Review CSV: `full_benchmark_scoring_review_C1_C2_C3_2026-06-19.csv`
- Total rows: 360

## Rows by Model

| Model Config | Rows |
|---|---:|
| C1 | 120 |
| C2 | 120 |
| C3 | 120 |

## How to Use

Score each row using the six 0-5 quality dimensions:

- relevance
- correctness
- faithfulness_to_source
- completeness
- hallucination_risk
- source_grounding

Then calculate `average_quality_score` as the mean of the six dimensions.

The CSV includes the question, expected-answer notes, evidence location, generated answer, retrieved sources, and system metrics on the same row.
