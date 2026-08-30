# Search Keywords and Strategy

Concrete search strings to use in Google Scholar, arXiv, ACL Anthology, and Semantic Scholar. Logging the keywords used means the literature review is reproducible 鈥?somebody else (including the supervisor) can run the same searches and check that nothing important was missed.

## Time window

Prioritise **2023 onward**. Anything older than 2022 is cited only for foundational context (RAG itself, transformer fundamentals). Local small LMs evolve too quickly to rely on older empirical findings.

## Core keyword clusters

### Cluster 1 鈥?Small language models

- `"small language model" survey`
- `"small language models" benchmark`
- `"sub-billion" OR "1B parameter" language model evaluation`
- `compact language model on-device`
- `efficient language model survey 2024..2026`

### Cluster 2 鈥?RAG evaluation

- `RAGAS faithfulness "answer relevance"`
- `ARES retrieval-augmented evaluation`
- `RAG benchmark "ground truth"`
- `"retrieval-augmented generation" evaluation framework`
- `RAG faithfulness metric limitations`

### Cluster 3 鈥?Local / on-device inference

- `local LLM inference llama.cpp`
- `Ollama local model deployment`
- `on-device LLM privacy`
- `edge LLM inference benchmark`
- `consumer hardware LLM evaluation`

### Cluster 4 鈥?Quantisation

- `LLM quantization 4-bit accuracy`
- `GPTQ AWQ comparison`
- `GGUF quantization quality`
- `"Q4_K_M" OR "K-quants" evaluation`
- `post-training quantization small model`

### Cluster 5 鈥?LLM-as-judge

- `"LLM-as-a-judge" bias`
- `"LLM judge" agreement human rater`
- `automated evaluation LLM faithfulness`
- `LLM evaluator self-preference verbosity`

### Cluster 6 鈥?Privacy and threat modelling

- `LLM privacy threat model`
- `prompt leakage user data LLM`
- `local-first AI privacy GDPR`
- `on-device AI data sovereignty`
- `NIST AI Risk Management Framework trustworthy AI risk`
- `ICO AI data protection guidance transparency lawfulness security data minimisation`
- `STRIDE LLM application` *(STRIDE is a Microsoft threat-modelling framework 鈥?possible structure for RQ3)*

## Citation graph walking

For high-value anchor papers, also do:

- **Forward citations:** "cited by" on Google Scholar to find newer work that builds on them. Most useful for RAGAS, ARES, RGB, Zheng 2023, Phi-3.
- **Backward citations:** read the related-work section of the anchor paper and follow the most-cited references. Most useful for newer model technical reports.

## Source priority

1. Peer-reviewed venues (ACL, EMNLP, NAACL, NeurIPS, ICML, ICLR, AAAI, EACL).
2. arXiv preprints from major labs (Google DeepMind, Meta AI, Microsoft Research, Hugging Face).
3. Reproducible benchmark leaderboards (Hugging Face Open LLM Leaderboard, MTEB, MMLU-Pro) 鈥?cite as data sources, not as papers.
4. Reputable industry blogs (Hugging Face, Anthropic, OpenAI) 鈥?cite only when they are the canonical source for a specific claim (e.g. GGUF format specification).

## What to *not* cite

- LinkedIn posts, Medium articles, YouTube videos 鈥?never as primary sources.
- Older small-model work (pre-2022) 鈥?out of date.
- Cloud-API-only evaluations (e.g. OpenAI vs. Anthropic comparisons) 鈥?out of scope.
- Fine-tuning or LoRA work 鈥?out of scope.

## Search log

Append each search session here with date, keywords used, and a one-line outcome ("found 3 useful papers", "duplicate of previous results", "no relevant results"). This becomes evidence of reading depth for the supervisor and for the dissertation's methodology chapter.

| Date | Cluster(s) | Keywords used | Outcome |
|---|---|---|---|
| | | | |
