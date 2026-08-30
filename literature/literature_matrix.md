# Literature Matrix

A structured table to track every paper read. The matrix forces a one-line "so what" per paper so that, when the literature review chapter is written, each paper has a defined role rather than being cited as filler.

**How to use:**
- Add a new row each time you read a paper.
- Keep "Why it matters here" to one sentence; if you can't, you haven't finished reading.
- Tag each paper to the sub-RQ(s) it supports.
- Update the *Status* column: `to read`, `reading`, `done`, `dropped`.

---

## Matrix

| # | Author (year) | Short title | Venue | Theme | Sub-RQ | Why it matters here | Status |
|---|---|---|---|---|---|---|---|
| 1 | Lewis et al. (2020) | Retrieval-Augmented Generation for Knowledge-Intensive NLP | NeurIPS | RAG foundations | RQ1 | Defines the RAG architecture used throughout the dissertation | to read |
| 2 | Es et al. (2023) | RAGAS | arXiv / EACL 2024 | RAG evaluation | RQ1 | Defines the faithfulness / answer relevance / context utilisation triad used as the primary quality metric | to read |
| 3 | Saad-Falcon et al. (2024) | ARES | NAACL | RAG evaluation | RQ1 | Alternative RAG evaluation framework 鈥?justifies choice of RAGAS vs ARES | to read |
| 4 | Chen et al. (2024) | RGB benchmark | AAAI | RAG benchmark dataset | RQ1 | Candidate evaluation dataset for the empirical core | to read |
| 5 | Zheng et al. (2023) | LLM-as-a-Judge / MT-Bench | NeurIPS | Evaluation methodology | RQ1 | Documents known biases in LLM-as-judge 鈥?justifies the human-rubric validation step | to read |
| 6 | Qwen Team (2024) | Qwen 2.5 Technical Report | arXiv | Model | RQ1, RQ2 | Source for Qwen 2.5 model claims (0.5B, 1.5B variants) | to read |
| 7 | Meta Llama Team (2024) | The Llama 3 Herd of Models | arXiv | Model | RQ1, RQ2 | Source for Llama 3.2 1B model claims | to read |
| 8 | Gemma Team (2025) | Gemma 3 Technical Report | DeepMind | Model | RQ1, RQ2 | Source for Gemma 3 1B model claims | to read |
| 9 | Abdin et al. (2024) | Phi-3 Technical Report | arXiv | Model | RQ1, RQ2 | On-device framing aligns directly with this dissertation's motivation | to read |
| 10 | Allal et al. (2025) | SmolLM2 | arXiv | Model | RQ1, RQ2 | Data-centric small-model training 鈥?different design philosophy than Qwen / Llama | to read |
| 11 | Frantar et al. (2023) | GPTQ | ICLR | Quantisation | RQ1, RQ2 | Foundational PTQ reference for the quantisation sub-study | to read |
| 12 | Dettmers & Zettlemoyer (2023) | k-bit Inference Scaling Laws | ICML | Quantisation | RQ1, RQ2 | Justifies why 4-bit is the default sweet spot | to read |
| 13 | ggerganov / ggml-org (n.d.) | llama.cpp / GGUF K-Quants docs | GitHub | Local inference / quantisation | RQ2 | Defines the local runtime and quantisation context used in the benchmark source set | selected source |
| 14 | Liu et al. (2024) | MobileLLM | ICML | On-device LLMs | RQ2, RQ3 | Architectural design for sub-billion models 鈥?context for the small-model framing | to read |
| 15 | Xu et al. (2024) | Resource-Efficient Foundation Models survey | arXiv | Survey | RQ1, RQ2 | Broad map of efficient deployment techniques | to read |
| 16 | Wang, J. (2025) | Jetson-Nano-RAG-LLM project report | WMG internal | Baseline | all | The direct predecessor 鈥?must be discussed in lit review | partly done |
| 17 | NIST (2023) | AI Risk Management Framework | NIST | AI risk / governance | RQ2, RQ3 | Frames risk, trustworthiness, and deployment practicality beyond raw model accuracy | selected source |
| 18 | ICO (2023/2024) | Guidance on AI and Data Protection | ICO | Privacy / data protection | RQ3 | Anchor source for GDPR-aware discussion of transparency, lawfulness, security, and data minimisation | selected source |
| 19 | OWASP (2025) | Top 10 for LLM Applications | OWASP | LLM security | RQ3 | Optional support for application-level risks such as data leakage, logging, and access control | to read |

---

## How to keep this matrix honest

- A paper is *dropped* if it does not support a sub-RQ. Recording the drop is more useful than silently ignoring it.
- Forward + backward citation walking is the most efficient way to grow the matrix. Start from #2 (RAGAS), #5 (Zheng), and #4 (RGB).
- A target of around 30 papers for the final lit review chapter is reasonable for an MSc dissertation; quality of engagement matters more than quantity.

## Caveat on the seed list

The exact year, venue, and authorship strings above were drafted from memory. **Verify each citation against the actual paper** (arXiv ID, DOI) before using it in the dissertation. Treat this matrix as the current literature-tracking file.
