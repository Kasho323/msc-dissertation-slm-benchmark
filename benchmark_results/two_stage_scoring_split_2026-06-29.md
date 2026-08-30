# Two-Stage Human Scoring Split (2026-06-29)

Random seed: 20260629 (deterministic, reproducible)

## Stage 1 - independent human scoring (no AI shown)
- File: human_stage1_independent_60_2026-06-29.csv
- 10 questions x 6 blind codes = 60 answers, shuffled.
- Chosen questions (2 per question type, spread over difficulty/docs):

  - Q003: explanation, medium, D1
  - Q007: fact_retrieval, easy, D1
  - Q008: boundary_limitation, medium, D1
  - Q010: source_grounded_synthesis, hard, D1
  - Q017: fact_retrieval, medium, D2
  - Q020: boundary_limitation, hard, D2
  - Q025: comparison, medium, D3
  - Q034: explanation, medium, D4
  - Q036: source_grounded_synthesis, hard, D4
  - Q038: comparison, hard, D1+D2

## Stage 2 - AI-assisted review
- File: human_stage2_ai_assisted_180_2026-06-29.csv
- Remaining 30 questions x 6 codes = 180 answers, shuffled.
- AI second-rater scores shown as ai_draft_* columns; human fills human_* columns.

## Rules
- Complete Stage 1 BEFORE opening Stage 2.
- Never open the blind model key until all human scoring is done.
- Stage 1 human scores vs AI scores on the same 60 answers give the genuine
  human-AI agreement statistic (Spearman/kappa) reported in the dissertation.