# Mini Pilot Scoring Summary

**Date:** 2026-06-19  
**Run ID:** `MINI_C2_20260619_174335`  
**Model configuration:** C2 - Llama 3.2 1B Instruct Q4_K_M  
**Server flags:** `--ctx-size 4096 --parallel 1 --cache-ram 0 --no-cache-prompt --ctx-checkpoints 0`  
**Questions scored:** Q001-Q005

## Quality Scores

| Question | Average Score | Main Observation |
|---|---:|---|
| Q001 | 2.50 | Partly relevant but misframes RAG as mainly stored pre-trained knowledge. |
| Q002 | 1.83 | Major conceptual error: treats RAG as a generative adversarial network. |
| Q003 | 3.50 | Broadly explains provenance and trust, but not strongly source-grounded. |
| Q004 | 3.00 | Captures retrieval, but includes wrong terminology and unnecessary paper-specific claims. |
| Q005 | 3.33 | Mostly correct but includes unsupported knowledge-graph framing. |

Mean quality score across five questions: **2.83 / 5**.

## Pilot Finding

C2 is slower and uses more memory than C1 in this pilot, while also making several terminology errors. It is still worth keeping in the benchmark because those errors are useful comparison evidence.

