# Final Results (2026-07-09)

Quality = AI second-rater (LLM-as-judge) over all 240 answers (rep 1 x 6 configs x 40 questions).
Validated on a 30-answer independent human subset: Spearman rho = 0.80, human systematically stricter.
System metrics from the final max_tokens=512 run, seed 42, same laptop, Balanced power plan.

## Table T1 - Answer quality by configuration (0-5)

| Config | Model | Relevance | Correct. | Faithful. | Complete. | Halluc.(hi=good) | Grounding | Overall |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| C1 | Qwen2.5 0.5B Q4_K_M | 3.48 | 2.90 | 2.98 | 2.42 | 3.67 | 2.98 | **3.07** |
| C2 | Llama 3.2 1B Q4_K_M | 3.70 | 2.95 | 2.92 | 2.75 | 3.33 | 2.95 | **3.10** |
| C3 | Gemma 3 1B Q4_K_M | 4.00 | 3.50 | 3.45 | 3.12 | 3.95 | 3.42 | **3.57** |
| C4 | Qwen2.5 1.5B Q2_K | 2.98 | 2.52 | 2.65 | 1.93 | 3.38 | 2.65 | **2.68** |
| C5 | Qwen2.5 1.5B Q4_K_M | 3.80 | 3.23 | 3.42 | 2.65 | 4.12 | 3.38 | **3.43** |
| C6 | Qwen2.5 1.5B Q8_0 | 3.88 | 3.33 | 3.35 | 2.70 | 4.08 | 3.35 | **3.45** |

## Table T2 - System metrics by configuration

| Config | Model | Size (MB) | Mean latency (s) | P95 latency (s) | Tokens/s | Mean RSS (MB) | Truncated (of 120) |
|---|---|---:|---:|---:|---:|---:|---:|
| C1 | Qwen2.5 0.5B Q4_K_M | 468.64 | 4.4498 | 7.527 | 103.42 | 568.37 | 6 |
| C2 | Llama 3.2 1B Q4_K_M | 770.28 | 7.0135 | 9.7995 | 76.07 | 1479.16 | 15 |
| C3 | Gemma 3 1B Q4_K_M | 768.72 | 6.8214 | 9.835 | 67.15 | 1001.06 | 3 |
| C4 | Qwen2.5 1.5B Q2_K | 718.0 | 6.2154 | 9.4471 | 82.74 | 906.26 | 24 |
| C5 | Qwen2.5 1.5B Q4_K_M | 1065.56 | 4.7106 | 6.2103 | 62.15 | 1793.69 | 0 |
| C6 | Qwen2.5 1.5B Q8_0 | 1806.77 | 6.5811 | 9.9432 | 42.82 | 1829.38 | 3 |

## Table T3 - Quantisation sensitivity, Qwen2.5 1.5B (same model, only precision changes)

| Quant | Overall quality | Size (MB) | Mean latency (s) | Tokens/s | Mean RSS (MB) | Truncated |
|---|---:|---:|---:|---:|---:|---:|
| Q2_K | 2.68 | 718.0 | 6.2154 | 82.74 | 906.26 | 24 |
| Q4_K_M | 3.43 | 1065.56 | 4.7106 | 62.15 | 1793.69 | 0 |
| Q8_0 | 3.45 | 1806.77 | 6.5811 | 42.82 | 1829.38 | 3 |

## Table T4 - Overall quality by question type

| Config | boundary_limitation | comparison | explanation | fact_retrieval | source_grounded_synthesis |
|---|---:|---:|---:|---:|---:|
| C1 | 3.33 | 2.71 | 3.19 | 3.22 | 2.56 |
| C2 | 3.33 | 3.29 | 3.19 | 2.98 | 2.72 |
| C3 | 3.23 | 4.12 | 3.67 | 3.46 | 3.42 |
| C4 | 2.80 | 2.58 | 2.98 | 2.43 | 2.25 |
| C5 | 3.00 | 3.46 | 3.66 | 3.54 | 3.03 |
| C6 | 3.43 | 3.67 | 3.56 | 3.39 | 3.08 |

## Notes for writing

- Quality is AI-rated; treat as indicative and cite the human-validation rho=0.80.
- Memory is observed llama-server RSS, not profiler peak.
- Q2_K shows the most truncation (24/120) and lowest quality - a clear over-compression finding.
- Conditional recommendation style: 'If priority is X, choose Y.'