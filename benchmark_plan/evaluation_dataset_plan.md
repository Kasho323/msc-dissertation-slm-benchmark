# Evaluation Dataset Plan

**Created:** 2026-06-19  
**Status:** Working plan. Not frozen until supervisor confirmation.

## Decision

The final benchmark should use a fixed question set built from open/public documents.

`Jackie_report.pdf` should be used for pilot testing only. It is useful for checking that upload, retrieval, generation, and source citation work, but it should not be treated as the final dissertation benchmark dataset.

## Rationale

Using open/public documents is cleaner for the dissertation because:

- the source material can be cited and described transparently
- the evaluation questions can be shared in an appendix
- the dataset is not tied too closely to one previous student project
- every model receives the same retrieved source context
- the method fits the ethics scope: secondary data and public/open documents only

## Selected Working Source Set

Use 4 core documents. The final set should be small enough to inspect manually, but broad enough to test factual retrieval, comparison, explanation, and source-grounded synthesis.

| ID | Source | URL | Purpose in Dataset | Status |
|---|---|---|---|
| D1 | Lewis et al. (2020), Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks | https://arxiv.org/abs/2005.11401 | RAG concepts, retrieval plus generation, provenance, factuality | Core benchmark source |
| D2 | llama.cpp official repository README | https://github.com/ggml-org/llama.cpp | Local inference, GGUF, quantisation, runtime practicality | Core benchmark source |
| D3 | NIST AI Risk Management Framework | https://www.nist.gov/itl/ai-risk-management-framework | AI risk, trustworthiness, risk management framing | Core benchmark source |
| D4 | ICO Guidance on AI and Data Protection | https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/artificial-intelligence/guidance-on-ai-and-data-protection/ | Data protection, transparency, lawfulness, fairness, security, data minimisation | Core benchmark source |

The Qwen2.5 Technical Report should be kept for literature review and model-background justification, not for the final benchmark question set. This avoids making the evaluation set too closely tied to one of the tested model families.

## Question Set Size

Target: **30-40 questions**.

Do not exceed 50 questions unless the benchmark runner is already stable and runtime is clearly manageable.

Recommended distribution:

| Question Type | Target Count | Purpose |
|---|---:|---|
| Fact retrieval | 10-12 | Can the model extract specific facts from retrieved context? |
| Explanation | 8-10 | Can the model explain a concept using the source? |
| Comparison | 6-8 | Can the model compare ideas across sections or documents? |
| Source-grounded synthesis | 6-8 | Can the model combine evidence without hallucinating? |
| Boundary/limitation questions | 4-6 | Can the model avoid overclaiming beyond the source? |

## Question Record Format

Each question must have:

- question ID
- source document ID
- question text
- question type
- expected answer or marking notes
- evidence location or source passage note
- difficulty: easy, medium, or hard
- whether the question requires one document or multiple documents

Use `question_set_template.csv` as the working format.

## Drafting Rules

1. Every question must be answerable from the source documents.
2. Avoid questions that require outside knowledge.
3. Avoid yes/no questions unless the explanation is the important part.
4. Include some questions where the answer is limited or conditional.
5. Keep wording identical for every model run.
6. Freeze the final question set before final experiments.
7. If a question is changed after freezing, record it as a protocol amendment.

## Pilot vs Final Use

| Stage | Documents | Purpose |
|---|---|---|
| Pipeline pilot | `docs/Jackie_report.pdf` | Check RAG upload, retrieval, answer generation, and source citation |
| Dataset pilot | 5-8 questions from open documents | Check question difficulty and answer format |
| Final benchmark | 30-40 frozen questions from open documents | Compare all model configurations |

## Supervisor Confirmation Needed

1. Is it acceptable to use a hand-curated open-document QA set?
2. Is 30-40 questions enough, with 50 as the upper limit?
3. Is it acceptable to keep model technical reports as literature/background rather than benchmark source documents?
4. Is the selected source mix suitable: RAG, local inference, AI risk management, and AI data protection?
