# Mini Pilot Scoring Summary

**Date:** 2026-06-19  
**Run ID:** `MINI_C1_20260619_175319`  
**Model configuration:** C1 - Qwen2.5 0.5B Instruct Q4_K_M  
**Server flags:** `--ctx-size 4096 --parallel 1 --cache-ram 0 --no-cache-prompt --ctx-checkpoints 0`  
**Questions scored:** Q001-Q005

## Quality Scores

| Question | Average Score | Main Observation |
|---|---:|---|
| Q001 | 3.17 | Relevant but blurs external retrieval with knowledge stored inside the model. |
| Q002 | 4.00 | Good retriever/generator answer, though the memory distinction could be clearer. |
| Q003 | 0.50 | Clear failure: returns bibliography/related-work text instead of answering provenance. |
| Q004 | 3.83 | Correct but narrow explanation focused on training/ablation evidence. |
| Q005 | 3.83 | Mostly correct and concise, but brief. |

Mean quality score across five questions: **3.07 / 5**.

## Pilot Finding

C1 is the fastest and uses the least memory in this controlled pilot, but it has a severe failure on Q003. This makes it useful as a lightweight baseline, not necessarily the best quality option.

