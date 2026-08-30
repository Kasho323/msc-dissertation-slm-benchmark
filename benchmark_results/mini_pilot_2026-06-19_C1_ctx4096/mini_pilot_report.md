# Mini Pilot Report

**Run ID:** `MINI_C1_20260619_175319`
**Date:** 2026-06-19
**Model configuration:** C1 - Qwen2.5 0.5B Instruct Q4_K_M
**Questions:** Q001-Q005
**Repetitions:** 1
**Retrieval/generation:** k=10, n=3, temperature=0.2, max_tokens=200

## Result

- Completed questions: 5
- Average endpoint latency: 3.787 seconds
- Raw JSON responses saved in `raw_responses/`.
- Manual scoring is not completed yet; use `answer_scoring_mini_pilot.csv`.

## Answer Snippets

- **Q001:** Retrieval-augmented generation aims to address the problem of knowledge-intensive NLP tasks by retrieving and augmenting pre-trained language models with factual knowledge. This approach allows for the storage and retrieval of information from the models, whic
- **Q002:** RAG models combine parametric and non-parametric memory by leveraging two components:  1. A retriever component: This component returns (top-K truncated) distributions over text passages given a query. This allows the model to retrieve relevant information fro
- **Q003:**     Petr Baudi and Jan ediv`y. Modeling of the question answering task in the yodaqa system. In International Conference of the Cross-Language Evaluation Forum for European Languages, pages 222228. Springer, 2015. URL https://link.springer.com/chapter/10.1007%
- **Q004:** In a RAG pipeline, the retriever plays a crucial role. It is responsible for retrieving relevant information for the task at hand. To assess the effectiveness of the retrieval mechanism, the authors ran ablations where they froze the retriever during training.
- **Q005:** Retrieval can help a model access knowledge that is not stored in its parameters by leveraging the input sequences to retrieve text documents. This allows the model to update its knowledge as the world changes, using the input sequences to retrieve relevant do
