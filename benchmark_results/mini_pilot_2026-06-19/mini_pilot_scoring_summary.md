# Mini Pilot Scoring Summary

**Date:** 2026-06-19  
**Run ID:** `MINI_C1_20260619_172658`  
**Model configuration:** C1 - Qwen2.5 0.5B Instruct Q4_K_M  
**Questions scored:** Q001-Q005  

## Quality Scores

| Question | Average Score | Main Observation |
|---|---:|---|
| Q001 | 3.00 | Partly relevant but misses important RAG motivation and includes one incorrect framing. |
| Q002 | 3.17 | Understands retriever/generator structure but confuses some mechanics. |
| Q003 | 0.67 | Clear failure: answer is off-topic and does not answer provenance question. |
| Q004 | 3.33 | Mostly relevant, but incomplete explanation of retriever's role. |
| Q005 | 4.33 | Strongest answer in the pilot; mostly correct and grounded. |

Mean quality score across five questions: **2.90 / 5**.

## Pilot Finding

The pipeline works technically: it returns answers, timing data, token data, memory estimates, and source references.

The main quality issue is not infrastructure failure but answer reliability. Q003 shows that the small model can produce an off-topic answer even when the retrieved source file is correct. This supports the dissertation's need for a structured quality rubric rather than relying only on whether an answer is returned.

## Implication for Full Benchmark

The result templates are usable for the final experiment. The full benchmark should keep:

- raw answer logging
- retrieved-source logging
- manual scoring with notes
- failure examples for the Discussion chapter
