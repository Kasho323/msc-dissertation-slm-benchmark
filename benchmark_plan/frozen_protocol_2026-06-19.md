# Proposed Frozen Experimental Protocol

**Created:** 2026-06-19  
**Status:** Supervisor approved direction on 2026-06-24; amended to include Q2_K and `max_tokens=512`  
**Project:** Evaluating Local Small Language Models for an On-Device AI Assistant with Privacy-Preserving Question Answering

## 1. Purpose

This protocol defines the experimental setup before final benchmark runs. Its purpose is to prevent scope drift and make the benchmark repeatable.

The benchmark answers the main research question:

> Which local small language model configuration offers the best trade-off between answer quality, computational efficiency, deployment practicality, and privacy for an on-device question-answering assistant?

## 2. Fixed RAG Pipeline

The previous `Jetson-Nano-RAG-LLM` project is used as a reference baseline or starting pipeline.

Pipeline:

```text
PDF corpus
  -> PyPDFLoader
  -> chunking / embedding
  -> vector retrieval
  -> reranking
  -> prompt assembly
  -> local llama.cpp chat completion
  -> answer + sources + timing data
```

The pipeline itself is not the research contribution. The contribution is the controlled comparison of model configurations under the same workflow.

## 3. Fixed Source Corpus

Only the following four PDF files should be uploaded for the final benchmark:

| Source ID | Local PDF | Role |
|---|---|---|
| D1 | `docs/final_benchmark_corpus/D1_RAG_Lewis_2020.pdf` | RAG concepts and grounding |
| D2 | `docs/final_benchmark_corpus/D2_llama_cpp_README.pdf` | Local inference, GGUF, quantisation, server setup |
| D3 | `docs/final_benchmark_corpus/D3_NIST_AI_RMF_1_0.pdf` | AI risk, trustworthiness, deployment practicality |
| D4 | `docs/final_benchmark_corpus/D4_ICO_AI_Data_Protection_Guidance.pdf` | Privacy, data protection, lawfulness, transparency, security |

`Jackie_report.pdf` is a pilot document only and must not be used as part of the final benchmark corpus.

Model technical reports, including Qwen2.5, Gemma, and Llama documentation, are literature/background sources only. They should not be uploaded into the final benchmark vector store.

## 4. Fixed Evaluation Question Set

Use:

`dissertation_project/benchmark_plan/question_set_template.csv`

The question set contains 40 questions:

- D1 RAG paper: 10 questions
- D2 llama.cpp README: 10 questions
- D3 NIST AI RMF: 9 questions
- D4 ICO AI/data protection: 8 questions
- Cross-document synthesis: 3 questions

Each question has:

- question ID
- source ID
- question type
- question text
- expected-answer notes
- evidence location
- difficulty
- one-document or multiple-document tag

Question wording must not be changed after final runs begin.

## 5. Model Configurations

Core configurations:

| ID | Model | Quantisation | Status | Purpose |
|---|---|---|---|---|
| C1 | Qwen2.5 0.5B Instruct | Q4_K_M | Available | Smallest lower-bound condition |
| C2 | Llama 3.2 1B Instruct | Q4_K_M | Available | 1B model from a different family |
| C3 | Gemma 3 1B IT | Q4_K_M | Available | Another 1B model family |
| C4 | Qwen2.5 1.5B Instruct | Q2_K | To prepare | Strong model-size reduction condition |
| C5 | Qwen2.5 1.5B Instruct | Q4_K_M | To prepare | Mid-level quantisation condition |
| C6 | Qwen2.5 1.5B Instruct | Q8_0 | To prepare | Higher-precision quantisation condition |

The controlled quantisation study is C4-C6: Q2_K vs Q4_K_M vs Q8_0 with the same base model and pipeline. The official Qwen GGUF release does not provide a Q1 file, so Q1 is excluded from the core comparison. See `protocol_amendment_2026-06-24.md`.

Optional stretch configurations must not be added unless the core benchmark is complete and the supervisor agrees:

- Qwen2.5 3B Q4_K_M
- TinyLlama 1.1B Q4_K_M
- Phi-3.5-mini Q4_K_M
- Qwen2.5 1.5B Q5_K_M
- no-RAG control

## 6. Runtime Setup

Primary runtime:

- llama.cpp `llama-server.exe`
- local OpenAI-compatible endpoint: `http://127.0.0.1:8080/v1/chat/completions`
- FastAPI backend: `http://127.0.0.1:8000`
- Streamlit frontend: `http://127.0.0.1:8501`

Use:

`start_all.ps1`

The backend uses an in-memory ChromaDB store, so PDFs must be re-uploaded after every backend restart.

## 7. Retrieval and Generation Settings

Default final-run settings:

| Setting | Value |
|---|---|
| retrieval k | 10 |
| rerank n | 3 |
| temperature | 0.2 |
| generation seed | 42 |
| max output tokens | 512 |
| llama.cpp context length | 4096 |
| llama.cpp parallel slots | 1 |
| repetitions | aim for 3 per configuration |
| warm-up questions | 2-3, discarded |

If runtime is too slow, reduce repetitions only after documenting the reason as a protocol amendment.

Recommended llama-server flags for comparable runs:

```powershell
--ctx-size 4096 --parallel 1 --cache-ram 0 --no-cache-prompt --ctx-checkpoints 0 --seed 42
```

For the final suite, start the FastAPI backend once, upload the corpus once, and keep the same in-memory vector store while switching llama.cpp model configurations. This controls retrieved context across models more reliably than rebuilding the vector store for every configuration.

## 8. Recorded Outputs

Use these templates:

| File | Purpose |
|---|---|
| `run_manifest_template.csv` | one row per model configuration and run |
| `model_answer_log_template.csv` | raw generated answers and system metrics |
| `answer_scoring_template.csv` | manual quality scores |

Record at minimum:

- model configuration ID
- question ID
- repetition
- generated answer
- retrieved source files/pages/chunks
- latency
- tokens generated
- tokens per second, if available
- peak memory, if measurable
- errors or crashes

## 9. Quality Scoring

Each answer is scored from 0 to 5 on six dimensions:

| Dimension | Meaning |
|---|---|
| relevance | answers the question asked |
| correctness | factually matches expected answer/source |
| faithfulness to source | claims are supported by retrieved source context |
| completeness | covers the important expected points |
| hallucination risk | higher score means fewer unsupported claims |
| source grounding | answer is clearly tied to retrieved material |

The primary scoring reference is:

`dissertation_project/benchmark_plan/evaluation_metrics.md`

Single-rater manual scoring is acceptable if reported honestly. Do not claim inter-rater reliability unless a second rater is actually used.

## 10. System Metrics

Record:

- latency
- time-to-first-token, if available
- generated tokens
- tokens per second
- peak memory use
- model file size
- setup/runtime problems

If a metric cannot be collected reliably, document it and avoid overclaiming in Results.

## 11. Analysis Plan

Primary outputs:

- quality score table by model configuration
- latency / throughput / memory table by configuration
- Qwen2.5 1.5B Q2 vs Q4 vs Q8 comparison
- quality-vs-speed or quality-vs-memory plot
- privacy comparison matrix

The final recommendation should be conditional:

> If the priority is speed, choose X; if answer quality matters more, choose Y; if privacy is the motivation, local deployment helps but still requires local data protection.

## 12. Privacy Analysis

Privacy is analytical, not an empirical privacy experiment.

Core statement:

> Local models avoid sending queries and documents to external cloud APIs, but privacy still depends on local storage, logs, access control, backups, and device security.

Use D3 and D4 to support the privacy and risk discussion.

## 13. Optional Constrained-Environment Check

A Docker/container or otherwise constrained-runtime check may be included only as a feasibility test method.

It is not a core research contribution.

If it delays the benchmark, skip it and report laptop-only results.

## 14. Amendment Rule

After this protocol is frozen, changes must be recorded below before continuing.

Examples requiring amendment:

- changing the model list
- changing the question wording
- adding or removing corpus documents
- changing retrieval or generation settings
- changing number of repetitions
- changing scoring criteria

## 15. Protocol Amendments

| Date | Change | Reason | Approved by |
|---|---|---|---|
| 2026-06-24 | Add Qwen2.5 1.5B Q2_K as C4; renumber Q4_K_M and Q8_0 as C5-C6 | Supervisor requested investigation of stronger model-size reduction and asked why Q1/Q2 were not included | Supervisor feedback; implementation decision documented |
| 2026-06-24 | Increase `max_tokens` from 200 to 512 for all final runs | Initial raw-response audit found frequent `finish_reason=length` | Methodological correction before final scoring |

## 16. Supervisor Confirmation Needed

The supervisor confirmed that the direction and details looked good on 2026-06-24 and asked the project to proceed, with an additional recommendation to investigate lower-bit quantisation. The protocol now records the resulting Q2/Q4/Q8 comparison.

## 17. Mini Pilot Evidence

A first mini pilot was completed on 2026-06-19 using C1 Qwen2.5 0.5B Q4_K_M and questions Q001-Q005.

A controlled C1/C2/C3 mini pilot was then completed using the same five questions and the same llama-server flags:

```powershell
--ctx-size 4096 --parallel 1 --cache-ram 0 --no-cache-prompt --ctx-checkpoints 0
```

Controlled pilot files:

- `dissertation_project/benchmark_results/mini_pilot_2026-06-19_C1_ctx4096/`
- `dissertation_project/benchmark_results/mini_pilot_2026-06-19_C2/`
- `dissertation_project/benchmark_results/mini_pilot_2026-06-19_C3/`
- `dissertation_project/benchmark_results/mini_pilot_comparison_C1_C2_C3_2026-06-19.md`

Controlled pilot findings:

- The pipeline works technically: answers, sources, latency, token counts, and memory estimates were recorded.
- The scoring rubric is usable.
- C1 was fastest and lightest but failed Q003.
- C2 was slower and showed terminology/conceptual errors.
- C3 had the best five-question quality score but was slowest.
- These are pilot findings only; final claims require the full frozen 40-question benchmark.
