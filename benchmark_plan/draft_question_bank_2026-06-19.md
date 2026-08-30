# Draft Evaluation Question Bank

**Created:** 2026-06-19  
**Status:** Draft only. These questions are not frozen and still need expected-answer notes after the source documents are finalised.

## D1 - RAG Paper

1. What problem does retrieval-augmented generation try to address in knowledge-intensive NLP tasks?
2. How does RAG combine parametric memory and non-parametric memory?
3. Why is provenance important in a question-answering system?
4. What is the role of the retriever in a RAG pipeline?
5. How can retrieval help a model update or access knowledge that is not stored in its parameters?
6. What is the difference between generating from model parameters alone and generating with retrieved passages?
7. According to the paper, what kinds of tasks are considered knowledge-intensive?
8. What limitation of large pre-trained models motivates the use of retrieval?

9. Why is grounding an answer in retrieved evidence useful for reducing unsupported claims?
10. What does RAG add to a standard language generation system?

## D2 - llama.cpp

11. What is the main purpose of llama.cpp?
12. Why is llama.cpp relevant for local or on-device language model deployment?
13. What does GGUF enable in local model serving?
14. How does quantisation support faster inference or lower memory use?
15. What is the purpose of running `llama-server` rather than only a command-line model?
16. Why is an OpenAI-compatible endpoint useful for this project?
17. What hardware or backend options are described as relevant to llama.cpp deployment?
18. What does local inference change about where model computation happens?
19. Why might a lightweight runtime matter for a laptop-based dissertation benchmark?
20. What deployment limitation might still remain even if the runtime supports local inference?

## D3 - NIST AI Risk Management Framework

21. What is the purpose of the NIST AI Risk Management Framework?
22. Why does AI risk management matter when deploying AI systems?
23. What does it mean to consider trustworthiness in AI design and evaluation?
24. How can an AI risk framework support evaluation beyond accuracy alone?
25. Why should risks to individuals, organisations, and society be considered separately?
26. How could the AI RMF support the privacy discussion in this dissertation?
27. Why should an AI system be evaluated for limitations as well as capabilities?
28. How does risk management help frame deployment practicality?
29. Why is it useful to separate technical performance from broader trust and governance concerns?

## D4 - ICO AI and Data Protection Guidance

30. What data protection principles are relevant to AI systems?
31. Why are transparency and explainability important for AI systems that process personal data?
32. What does lawfulness mean in the context of AI and data protection?
33. Why are accuracy and statistical accuracy relevant to AI outputs?
34. How do security and data minimisation relate to AI deployment?
35. What kinds of local risks remain even if a model does not send data to a cloud API?
36. How can local deployment reduce some privacy risks while leaving other data protection responsibilities in place?
37. Why does keeping processing local not remove all data protection responsibilities?

## Cross-Document Questions

38. How do RAG and local deployment address different parts of the question-answering problem?
39. How do technical deployment choices connect to privacy and data protection concerns?
40. Based on the source documents, why should the dissertation conclusion be a conditional recommendation rather than a single universal winner?
