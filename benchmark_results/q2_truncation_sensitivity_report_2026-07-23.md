# Q2 truncation sensitivity check

This check uses first-repetition quality scores and groups finish reasons by question. The three fixed-seed repetitions had the same finish reason for every Q2 question.

| Subset | n | Q2 mean quality | Q4 mean quality on same questions | Mean Q4-Q2 gap | Q2 completeness | Q4 completeness |
|---|---:|---:|---:|---:|---:|---:|
| All 40 questions | 40 | 2.683 | 3.433 | 0.750 | 1.925 | 2.650 |
| Q2 naturally finished (same 32 questions for Q4) | 32 | 2.766 | 3.568 | 0.802 | 2.000 | 2.719 |
| Q2 length-stopped (same 8 questions for Q4) | 8 | 2.354 | 2.896 | 0.541 | 1.625 | 2.375 |

## Interpretation

- Eight of the 40 Q2 questions reached the 512-token limit. Across the three identical repetitions, this appears as 24 of 120 outputs.
- On the 32 questions where Q2 finished naturally, Q2 still averaged 2.766, compared with 3.568 for Q4 on exactly the same questions.
- The quality gap therefore remains after the length-stopped Q2 answers are excluded. Truncation may reduce completeness, but it does not explain the full Q2 quality difference.
- The eight length-stopped questions were harder for both configurations, because Q4 also scored lower on that subset than on its other questions.

## Q2 length-stopped question IDs

Q013, Q016, Q020, Q024, Q025, Q031, Q033, Q040
