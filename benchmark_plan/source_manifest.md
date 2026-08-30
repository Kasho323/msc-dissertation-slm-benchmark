# Source Manifest for Evaluation Dataset

**Created:** 2026-06-19  
**Status:** Working source manifest. To be frozen with the experimental protocol.

## Core Benchmark Sources

| Source ID | Short Name | Full Source | URL | Benchmark Role |
|---|---|---|---|---|
| D1 | RAG Paper | Lewis et al. (2020), *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks* | https://arxiv.org/abs/2005.11401 | Tests RAG concepts, retrieval grounding, provenance, and factuality |
| D2 | llama.cpp README | ggml-org, *llama.cpp* official repository README | https://github.com/ggml-org/llama.cpp | Tests local inference, runtime practicality, GGUF, server use, and quantisation |
| D3 | NIST AI RMF | NIST, *AI Risk Management Framework* | https://www.nist.gov/itl/ai-risk-management-framework | Tests risk, trustworthiness, evaluation beyond accuracy, and deployment framing |
| D4 | ICO AI/Data Protection | ICO, *Guidance on AI and Data Protection* | https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/artificial-intelligence/guidance-on-ai-and-data-protection/ | Tests privacy, data protection, transparency, lawfulness, security, and data minimisation |

## Background-Only Sources

| Source | URL | Use |
|---|---|---|
| Qwen2.5 Technical Report | https://arxiv.org/abs/2412.15115 | Literature review and model-selection justification only |
| Gemma 3 Technical Report | https://arxiv.org/abs/2503.19786 | Literature review and model-selection justification only |
| Llama model documentation/report | TBD | Literature review and model-selection justification only |

## Rule

Only D1-D4 should be uploaded into the final benchmark vector store unless the protocol is amended. Background-only sources may be cited in the dissertation, but they should not generate final benchmark questions.

## Local Corpus Files

The upload-ready PDF corpus is stored in:

`docs/final_benchmark_corpus/`

| Source ID | Local PDF |
|---|---|
| D1 | `docs/final_benchmark_corpus/D1_RAG_Lewis_2020.pdf` |
| D2 | `docs/final_benchmark_corpus/D2_llama_cpp_README.pdf` |
| D3 | `docs/final_benchmark_corpus/D3_NIST_AI_RMF_1_0.pdf` |
| D4 | `docs/final_benchmark_corpus/D4_ICO_AI_Data_Protection_Guidance.pdf` |

`docs/final_benchmark_corpus/corpus_manifest.csv` records the download URLs and generated filenames.
