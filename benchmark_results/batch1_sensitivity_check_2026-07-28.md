# Batch-1 sensitivity check on human–AI agreement

**Created:** 2026-07-28. Verifies that the batch-1 rating incident (initial 30 answers unintentionally routed to Xiaomi MiMo, quarantined, then rescored by the Codex rater in the same session used to diagnose the problem) does not materially affect the human–AI agreement result.

## Data sources

- AI scores (all 240): `ai_second_rater_codex_gpt_C1_C6_2026-06-25.csv`
- Independent human scores (30): `human_independent_CLEAN_30_HUMAN_SCORED_2026-07-09.csv`
- Batch-1 (rescored) IDs: `ai_second_rater_batches_2026-06-25/batch_01_codex_gpt_ratings.json`
- Quarantined MiMo ratings (never merged): `ai_second_rater_batches_2026-06-25/batch_01_mimo_v2.5_pro_ratings_QUARANTINED.json`

Overall score per answer = unweighted mean of the six rubric dimensions (relevance, correctness, faithfulness_to_source, completeness, hallucination_risk, source_grounding).

## Overlap

3 of the 30 human-validation answers fall in batch 1 (the batch that cannot be described as completely uninfluenced by prior AI ratings):

`F3-Q038-R1`, `T2-Q003-R1`, `T2-Q017-R1`

## Result

| Sample | n | Spearman ρ | MAD (0–5) |
|--------|---:|-----------:|----------:|
| All matched answers | 30 | 0.799 | 0.761 |
| Batch-1 overlaps removed | 27 | 0.807 | 0.772 |

Human mean overall = 2.05; AI mean overall = 2.60 (human 0.55 lower on average, i.e. generally stricter).

## Conclusion

Removing the three possibly-influenced batch-1 answers changes Spearman's ρ from 0.799 to 0.807 and the mean absolute difference from 0.76 to 0.77 — essentially unchanged. The human–AI agreement result is therefore robust to the batch-1 rating incident, and the incident does not materially affect the validation of the AI rating method. The quarantined MiMo ratings were never merged into the analysed dataset.

This is a rank-order association check on a 30-answer sample; it does not measure absolute agreement, remove the systematic offset between raters, or independently validate the final model ranking.
