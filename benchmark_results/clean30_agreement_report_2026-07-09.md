# CLEAN 30 Independent Human Scoring - Validation and Human-AI Agreement

Generated 2026-07-09. Human scores produced with NO AI scores visible (independent).

## 1. Validation
- All 30 rows complete, every dimension 0-5, all matched to AI ratings. PASS.

## 2. Human score distribution (scale usage)
| Score | Count | % |
|---|---:|---:|
| 0 | 20 | 11% |
| 1 | 46 | 26% |
| 2 | 49 | 27% |
| 3 | 39 | 22% |
| 4 | 22 | 12% |
| 5 | 4 | 2% |

## 3. Mean quality by blind code (still anonymised)
| Blind code | n | Human mean | AI mean |
|---|---:|---:|---:|
| A7 | 5 | 3.17 | 3.50 |
| F3 | 5 | 1.70 | 1.77 |
| K8 | 5 | 1.67 | 2.27 |
| M4 | 5 | 1.63 | 2.83 |
| R9 | 5 | 2.37 | 3.03 |
| T2 | 5 | 1.77 | 2.20 |

## 4. Human vs AI agreement (n=30)
- **Overall average score: Spearman rho = 0.799** (p=1.2e-07)
- Mean absolute difference of averages: 0.76 points on the 0-5 scale

| Dimension | Spearman rho | Weighted kappa | Exact % | Within +/-1 % |
|---|---:|---:|---:|---:|
| relevance | 0.85 | 0.79 | 37% | 97% |
| correctness | 0.78 | 0.71 | 40% | 90% |
| faithfulness_to_source | 0.62 | 0.49 | 33% | 87% |
| completeness | 0.82 | 0.63 | 17% | 90% |
| hallucination_risk | 0.84 | 0.75 | 30% | 93% |
| source_grounding | 0.66 | 0.55 | 27% | 83% |

## 5. Largest human-AI disagreements
| Blind ID | Human avg | AI avg | diff |
|---|---:|---:|---:|
| M4-Q003-R1 | 0.50 | 3.00 | 2.50 |
| R9-Q007-R1 | 3.17 | 4.67 | 1.50 |
| M4-Q007-R1 | 3.17 | 4.67 | 1.50 |
| K8-Q020-R1 | 0.50 | 2.00 | 1.50 |
| F3-Q003-R1 | 1.67 | 0.17 | 1.50 |
| A7-Q036-R1 | 3.17 | 4.33 | 1.17 |

Guide: Spearman >0.7 strong, 0.5-0.7 moderate. Weighted kappa >0.6 substantial, 0.4-0.6 moderate.