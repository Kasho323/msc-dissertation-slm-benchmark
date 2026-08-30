# Research Gap

This note gives the short gap statement that can later be used in the Introduction and Literature Review.

## Gap in One Paragraph

Large language models are widely benchmarked, but small local language models are less often evaluated under a realistic question-answering workflow that also measures answer quality, speed, memory use, deployment practicality, and privacy implications together. Existing work often focuses either on general capability benchmarks or on showing that a local RAG system can run. There is still room for a compact, controlled dissertation benchmark asking which local model configuration is most suitable for an on-device question-answering assistant.

## Relationship to Wang 2025

Wang's Jetson-Nano-RAG-LLM project is best treated as a **reference baseline or starting pipeline**. It demonstrated that a local RAG assistant can run on edge/laptop hardware, but it does not need to be replicated exactly. The present dissertation can borrow its RAG structure and evaluation motivation while updating the model choices, simplifying the scope, and using a clearer quality rubric.

## Specific Gap This Dissertation Addresses

This dissertation addresses:

- limited model-configuration comparison for local small models
- limited evidence on model size and quantisation trade-offs
- vague or overly broad answer-quality scoring
- privacy claims that need more nuance than "local equals private"
- lack of practical laptop-focused deployment recommendations

## Boundaries

This dissertation does not claim to solve:

- edge-device deployment on Jetson Nano
- fine-tuning or LoRA adaptation
- multilingual or multimodal question answering
- production-grade assistant design
- empirical cloud API benchmarking

## Fit With Research Questions

| Gap Area | Dissertation Response |
|---|---|
| Which local model configuration works best? | Compare 4-6 configurations on the same question set |
| Is answer quality good enough? | Score relevance, correctness, faithfulness, completeness, hallucination risk, and source grounding |
| What does better quality cost? | Record latency, throughput, memory, and model size |
| Does quantisation matter? | Compare Qwen2.5 1.5B Q4 against Q8, with Q5 optional |
| Is local deployment private? | Analyse data flow, logs, local storage, access control, backups, and device security |

## Working Claim

The expected contribution is not "this model is universally best". The expected contribution is a conditional recommendation:

> If the priority is speed, choose one configuration; if the priority is answer quality, choose another; if privacy is the motivation, local deployment helps but still requires local data protection.
