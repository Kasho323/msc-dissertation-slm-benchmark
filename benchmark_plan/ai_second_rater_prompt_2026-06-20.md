# AI Second Rater Prompt

Use this prompt with Claude, Gemini, or GPT when asking for an AI-assisted second quality rating.

## Prompt

You are acting as a second rater for an MSc dissertation benchmark of local small language models in a RAG-based question-answering pipeline.

You will receive rows from a blind scoring CSV. The model identity is hidden behind random blind codes. Do not try to infer which model produced the answer. Score only the generated answer against the question, expected-answer notes, and evidence location.

Use a 0-5 scale for each dimension:

- 0 = absent or unusable
- 1 = very poor
- 2 = weak
- 3 = acceptable
- 4 = good
- 5 = excellent

Score these six dimensions:

1. relevance: Does the answer address the question asked?
2. correctness: Is the answer factually correct compared with the expected-answer notes and source evidence?
3. faithfulness_to_source: Are the claims supported by the source/evidence?
4. completeness: Does the answer cover the important expected points?
5. hallucination_risk: Higher is better. 5 means no unsupported claims observed; 0 means severe unsupported/invented claims.
6. source_grounding: Is the answer clearly grounded in the provided source material?

Then calculate:

average_quality_score = mean of the six dimension scores

For each row, return the same identifying columns and add:

- relevance
- correctness
- faithfulness_to_source
- completeness
- hallucination_risk
- source_grounding
- average_quality_score
- scoring_notes

Keep scoring_notes concise but specific. Mention if the answer is truncated, off-topic, unsupported, too vague, or missing important expected points.

Important:

- Do not use latency, memory, throughput, or model identity when scoring.
- Do not reward an answer just because it is long.
- Penalise answers that use wrong terminology or invent unsupported details.
- If an answer appears cut off mid-sentence, score completeness lower and mention truncation in scoring_notes.
- Be consistent across rows.

## Recommended Workflow

Use the rep-1-only blind scoring file first:

`full_benchmark_blind_scoring_rep1_only_C1_C2_C3_2026-06-20.csv`

This gives 120 rows for C1-C3. After checking consistency and workload, decide whether to score all 360 rows.

