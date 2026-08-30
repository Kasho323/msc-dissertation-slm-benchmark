# Stage 1 Human Scoring - Validation and Human-AI Agreement

Generated: 2026-06-30. Human file: human_stage1_independent_60_2026-06-29_HUMAN_SCORED.csv

## 1. Validation / 文件校验

- All 60 rows complete; every dimension 0-5; averages correct; all rows matched to AI ratings. PASS.

## 2. Human score distribution / 打分分布

| Score | Count | % |
|---|---:|---:|
| 0 | 10 | 2.8% |
| 1 | 70 | 19.4% |
| 2 | 83 | 23.1% |
| 3 | 92 | 25.6% |
| 4 | 76 | 21.1% |
| 5 | 29 | 8.1% |

| Blind code | n | Human mean | AI mean (from earlier report) |
|---|---:|---:|---:|
| A7 | 10 | 3.167 | 3.575 |
| F3 | 10 | 2.450 | 3.071 |
| K8 | 10 | 1.833 | 2.683 |
| M4 | 10 | 3.117 | 3.433 |
| R9 | 10 | 3.050 | 3.446 |
| T2 | 10 | 2.400 | 3.1 |

(AI means are over all 40 questions; human means are over the 10 Stage-1 questions, so levels are not directly comparable - ranking direction is the thing to watch.)

## 3. Human vs AI agreement on the same 60 answers / 人机一致性

- **Overall average score: Spearman rho = 0.995** (p = 1e-59), n = 60
- Mean absolute difference between human and AI averages: 0.03 points (0-5 scale)

| Dimension | Spearman rho | Weighted kappa (quadratic) | Exact match % | Within +/-1 % |
|---|---:|---:|---:|---:|
| relevance | 0.995 | 0.995 | 98% | 100% |
| correctness | 0.980 | 0.981 | 95% | 100% |
| faithfulness_to_source | 1.000 | 1.000 | 100% | 100% |
| completeness | 0.989 | 0.977 | 93% | 100% |
| hallucination_risk | 0.974 | 0.974 | 90% | 100% |
| source_grounding | 0.998 | 0.995 | 98% | 100% |

### Largest disagreements (top 8) / 分歧最大的答案

| Blind ID | Question | Human avg | AI avg | |diff| |
|---|---|---:|---:|---:|
| K8-Q008-R1 | Q008 | 1.50 | 1.83 | 0.33 |
| T2-Q034-R1 | Q034 | 4.17 | 4.00 | 0.17 |
| T2-Q008-R1 | Q008 | 2.33 | 2.17 | 0.17 |
| R9-Q017-R1 | Q017 | 2.33 | 2.17 | 0.17 |
| R9-Q008-R1 | Q008 | 4.17 | 4.00 | 0.17 |
| M4-Q034-R1 | Q034 | 4.17 | 4.00 | 0.17 |
| A7-Q008-R1 | Q008 | 2.17 | 2.33 | 0.17 |
| A7-Q007-R1 | Q007 | 1.00 | 1.17 | 0.17 |

## Interpretation guide / 解读参考

- Spearman rho: >0.7 strong, 0.5-0.7 moderate, <0.5 weak rank agreement.
- Weighted kappa: >0.6 substantial, 0.4-0.6 moderate, <0.4 fair/poor.
- If a dimension shows weak agreement, review that dimension manually in Stage 2 rather than trusting AI drafts for it.