# Experiment Design

This is the concrete, runnable benchmark plan. It should be frozen into a protocol only after the supervisor confirms the model configurations, dataset, metrics, and hardware feasibility.

## 1. Hardware

| Item | Value | Notes |
|---|---|---|
| Machine | Student's personal laptop | To be specified before experiments |
| CPU | TBD | Record model, core count, and clock |
| RAM | TBD | Record total memory and free memory during inference |
| GPU | TBD | Record whether llama.cpp or Ollama uses it |
| OS | Windows | All runs on the same OS installation |
| Power profile | Plugged in, fixed Balanced plan | Use the same available Windows power plan for every run |

The benchmark is comparative. The absolute speed numbers only describe this laptop, but the model ranking is still meaningful because every configuration runs under the same conditions.

### Optional constrained-environment feasibility check

If practical, add a small Docker/container or otherwise constrained-runtime check to simulate a resource-limited on-device environment. This is a **methodology feasibility test**, not a core research contribution. Its purpose is to check whether the selected local setup remains usable under limited compute or memory conditions.

This check should only be included if it can be implemented without delaying the main benchmark. The main benchmark remains the comparison of local model configurations under a fixed RAG workflow.

## 2. Software Stack

| Component | Version | Source |
|---|---|---|
| Python | TBD | Record exact version |
| llama.cpp | TBD | Record commit or release |
| Ollama, if used | TBD | Record version |
| ChromaDB | TBD | Pin version |
| LangChain or direct pipeline code | TBD | Pin version |
| Evaluation scripts | project repository | Commit before final runs |

Everything used in the final benchmark should be recorded in a run manifest.

## 3. Pipeline

The previous Jetson-Nano-RAG-LLM project should be used as a **reference baseline or starting pipeline**, not as something that must be copied exactly.

Working pipeline:

```text
input question
  -> retrieve relevant chunks from vector DB
  -> optionally rerank retrieved chunks
  -> assemble prompt with context and question
  -> generate answer with local model
  -> record answer, retrieved sources, and system metrics
```

Once the pilot is complete, the retrieval settings should be fixed and reused for every model configuration. The dissertation contribution is the benchmark comparison, not a new RAG pipeline.

## 4. Conditions

Target size: **6 core configurations**, with at most **1 stretch configuration**.

| ID | Model | Quantisation | Pipeline | Purpose |
|---|---|---|---|---|
| C1 | Qwen2.5 0.5B Instruct | Q4_K_M | RAG | Smallest available lower-bound condition |
| C2 | Llama 3.2 1B Instruct | Q4_K_M | RAG | Available 1B model from a different family |
| C3 | Gemma 3 1B IT | Q4_K_M | RAG | Available 1B model from another family |
| C4 | Qwen2.5 1.5B Instruct | Q2_K | RAG | Strong model-size reduction condition |
| C5 | Qwen2.5 1.5B Instruct | Q4_K_M | RAG | Mid-level same-model quantisation condition |
| C6 | Qwen2.5 1.5B Instruct | Q8_0 | RAG | Higher-precision same-model quantisation condition |

C4-C6 form the controlled quantisation sensitivity study. Q1 is not a core condition because the official Qwen2.5 1.5B GGUF release starts at Q2_K. A Q1-class condition would require a different source or conversion procedure and would therefore introduce an additional variable.

Stretch choices, only if feasible:

- Qwen2.5 3B Q4_K_M as a larger same-family condition.
- TinyLlama 1.1B Q4_K_M as an extra very-small comparator.
- Phi-3.5-mini Q4_K_M as a stronger but heavier on-device model.
- A reproducibly generated Q1-class Qwen2.5 1.5B file as an extreme-compression feasibility boundary.
- A no-RAG control using the best model from the pilot.

## 5. Evaluation Question Set

Use one fixed evaluation question set for all configurations.

Target size: **30-40 questions**, with **50** as the upper limit if runtime is clearly manageable.

Current working decision:

- Use 3-5 open/public documents as the final benchmark source set.
- Current selected working sources are the RAG paper, llama.cpp README, NIST AI RMF, and ICO AI/data protection guidance.
- Keep model technical reports for literature/model background rather than final benchmark questions.
- Write hand-curated questions with expected-answer notes and source evidence.
- Use `Jackie_report.pdf` only for pipeline pilot testing, not as the final benchmark dataset.

The question set must be frozen before final runs. Each question should have:

- question text
- source document or passage
- expected answer or marking notes
- difficulty tag, if useful

See `evaluation_dataset_plan.md` and `question_set_template.csv`.

The upload-ready PDF corpus is stored in `docs/final_benchmark_corpus/` and has been validated with the same `PyPDFLoader` used by the backend. See `source_manifest.md` and `final_corpus_validation_2026-06-19.md`.

## 6. Repetitions and Randomisation

- Run each configuration on the same question set.
- Aim for **n = 3 repetitions** per configuration if runtime allows.
- Keep generation settings fixed across configurations.
- Record seed, temperature, context length, top-k, top-n, and max output tokens.
- Use generation seed `42` for final runs.
- Interleave configuration order where practical so that heat and background load do not favour one model.
- Keep one FastAPI backend and one uploaded in-memory vector store active while switching model configurations, so retrieved contexts remain comparable.

## 7. Procedure Per Configuration

1. Start the runtime with the selected model and quantisation.
2. Load or rebuild the same vector store.
3. Run 2-3 warm-up questions and discard those outputs.
4. For each evaluation question:
   - retrieve source chunks
   - generate the answer
   - record answer text and retrieved sources
   - record latency, throughput, and peak memory
5. Score each answer using the fixed quality rubric.
6. Export one CSV per configuration and run.

Use `run_manifest_template.csv`, `model_answer_log_template.csv`, and `answer_scoring_template.csv` as the working result-recording format. The schema is described in `benchmark_result_schema.md`.

Optional feasibility step:

- Repeat a small subset of the benchmark under a constrained Docker/container or constrained-runtime setup, if feasible.
- Use this only to discuss deployment feasibility under resource limits.
- Do not let this replace or delay the main laptop benchmark.

## 8. Analysis Plan

Primary outputs:

- table of quality scores by configuration
- table of speed and memory metrics by configuration
- Q2 vs Q4 vs Q8 comparison for Qwen2.5 1.5B
- cost-vs-quality scatter plot
- privacy comparison matrix

Because the question set is small, the analysis should emphasise clear descriptive statistics, paired comparisons on the same questions, confidence intervals where useful, and careful discussion rather than overclaiming statistical significance.

## 9. Privacy Analysis

Privacy is not simply "local equals private". The dissertation should state:

> Local models avoid sending queries and documents to external cloud APIs, but privacy still depends on local storage, logs, access control, backups, and device security.

This becomes a structured comparison between local and cloud workflows, supported by cited sources.

## 10. Pre-Registration

Before final experiments, freeze:

- model configurations
- dataset and question set
- retrieval settings
- generation settings
- quality rubric
- system metrics
- analysis plan

Any later change should be recorded as a dated protocol amendment.

## 11. Key Risks

| Risk | Mitigation |
|---|---|
| Additional Qwen2.5 1.5B files are unavailable or too slow | Complete a five-question feasibility pilot first and document any excluded configuration |
| Qwen2.5 3B or Phi-3.5-mini is too slow | Treat them as stretch only, not core conditions |
| Dataset takes too long to build | Use 30-40 questions, not 100-200; only go up to 50 if runtime is clearly manageable |
| Final source documents are too broad | Use 3-4 core open documents and keep model reports for literature only |
| Quality scoring is too vague | Use the six fixed rubric dimensions in `evaluation_metrics.md` |
| Privacy argument is too broad | Limit it to data flow, logs, storage, access control, and device security |
| Constrained-environment setup takes too long | Treat it as optional and report laptop-only results |
| Scope expands during July | Freeze the protocol before final runs |

## 12. Supervisor Decisions Needed

1. Confirm the 4-6 configuration scope.
2. Confirm the exact model list.
3. Confirm the 30-40 question evaluation set size, with 50 as the upper limit.
4. Confirm the quality rubric.
5. Confirm that privacy is an analytical comparison, not an empirical measurement.
