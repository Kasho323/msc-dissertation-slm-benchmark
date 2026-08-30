# Benchmark Result Schema

**Created:** 2026-06-19  
**Status:** Working schema. To be frozen with the experimental protocol.

This file defines what should be recorded when the benchmark is run. The goal is to make every final claim traceable to either a model output, a quality score, a system metric, or a documented setup note.

## Files

| File | Purpose |
|---|---|
| `question_set_template.csv` | Frozen question set with expected-answer notes and evidence locations |
| `run_manifest_template.csv` | One row per model configuration and benchmark run |
| `model_answer_log_template.csv` | One row per generated answer |
| `answer_scoring_template.csv` | One row per scored answer |

## Run Manifest

Use `run_manifest_template.csv` to record model and runtime setup before each run.

Key fields:

- run_id
- model_config_id
- model_name
- quantisation
- model_file
- runtime
- hardware notes
- retrieval settings
- generation settings
- start and end time
- run status

## Model Answer Log

Use `model_answer_log_template.csv` to store raw benchmark outputs.

Key fields:

- run_id
- question_id
- repetition
- prompt
- generated_answer
- sources_returned
- latency_seconds
- tokens_generated
- tokens_per_second
- peak_memory_mb
- error_notes

This file should not be edited after the run except to add clearly marked error notes.

## Answer Scoring

Use `answer_scoring_template.csv` to score each generated answer.

Quality dimensions use the 0-5 scale in `evaluation_metrics.md`:

- relevance
- correctness
- faithfulness_to_source
- completeness
- hallucination_risk
- source_grounding

The average quality score can be calculated after scoring. The scoring notes should briefly explain why the score was given, especially for low or borderline answers.

## Analysis Tables

The final dissertation can derive:

- quality mean by model configuration
- quality by question type
- latency and throughput by model configuration
- peak memory by model configuration
- Q2 vs Q4 vs Q8 comparison for Qwen2.5 1.5B
- qualitative failure examples

## Rule

Do not change the question wording, retrieval settings, or generation settings after final runs begin. If a change is unavoidable, record it as a protocol amendment before continuing.
