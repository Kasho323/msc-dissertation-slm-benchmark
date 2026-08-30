# Mini Pilot Scoring Summary

**Date:** 2026-06-19  
**Run ID:** `MINI_C3_20260619_174949`  
**Model configuration:** C3 - Gemma 3 1B IT Q4_K_M  
**Server flags:** `--ctx-size 4096 --parallel 1 --cache-ram 0 --no-cache-prompt --ctx-checkpoints 0`  
**Questions scored:** Q001-Q005

## Quality Scores

| Question | Average Score | Main Observation |
|---|---:|---|
| Q001 | 4.00 | Clear answer about external knowledge sources, though not fully complete. |
| Q002 | 3.17 | Reasonable retrieval-plus-generation answer, but memory distinction is fuzzy. |
| Q003 | 4.17 | Strong provenance answer connecting trust, verification, and factuality. |
| Q004 | 3.00 | Correct opening, then adds distracting and partly unsupported retrieval details. |
| Q005 | 4.00 | Good answer about external lookup and updating knowledge without changing weights. |

Mean quality score across five questions: **3.67 / 5**.

## Pilot Finding

C3 gives the best quality in this controlled five-question pilot, but it is the slowest and has lower throughput than C1/C2. It is a strong candidate for the final benchmark because it shows a clear quality-speed trade-off.

