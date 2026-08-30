# Candidate Model Configurations

**Status:** Revised 2026-06-24 following supervisor feedback on lower-bit quantisation.

This project should compare **4-6 model configurations**, not necessarily 6 completely different model families. A configuration means a specific model plus a specific quantisation level and runtime setup. This keeps the dissertation achievable while still allowing a useful benchmark.

## Selection Criteria

A configuration should satisfy all of the following:

1. Open-weight and usable for academic research.
2. Instruction-tuned or chat-tuned.
3. Small enough to run locally on the student's laptop, with a target upper bound of about 3.8B parameters.
4. Available as GGUF or otherwise practical to serve through llama.cpp or Ollama.
5. Relevant to on-device or resource-constrained question answering.

## Final Core Set

| ID | Model | Quantisation | Why Include It | Status |
|---|---|---|---|---|
| C1 | Qwen2.5 0.5B Instruct | Q4_K_M | Smallest available model; fast lower-bound condition | Available |
| C2 | Llama 3.2 1B Instruct | Q4_K_M | Available 1B model from a different family | Available |
| C3 | Gemma 3 1B IT | Q4_K_M | Available 1B model from another model family | Available |
| C4 | Qwen2.5 1.5B Instruct | Q2_K | Strong model-size reduction condition requested after supervisor review | To prepare |
| C5 | Qwen2.5 1.5B Instruct | Q4_K_M | Mid-level quantisation condition | To prepare |
| C6 | Qwen2.5 1.5B Instruct | Q8_0 | Higher-precision comparison while holding model family and size fixed | To prepare |

This gives 6 configurations: three already-installed cross-family models plus a controlled Qwen2.5 1.5B Q2 vs Q4 vs Q8 quantisation comparison.

The official Qwen GGUF release provides Q2_K as its lowest standard quantisation and does not provide a Q1 file. Q1 is therefore excluded from the core benchmark to avoid introducing a differently sourced or differently produced model. It may be considered only as an optional feasibility boundary if a comparable and reproducible file can be produced later.

## Optional Stretch Configuration

Choose **one** stretch condition only if the laptop pilot shows the core set is manageable:

| Option | Model | Quantisation | Why It Might Be Useful |
|---|---|---|---|
| S1 | Qwen2.5 3B Instruct | Q4_K_M | Larger same-family model, but may be too slow |
| S2 | TinyLlama 1.1B Chat | Q4_K_M | Extra very-small comparator if needed |
| S3 | Phi-3.5-mini Instruct | Q4_K_M | Strong on-device framing, but may be slow or memory-heavy |
| S4 | Qwen2.5 1.5B Instruct | Q1-class, if reproducibly available | Optional extreme-compression feasibility boundary only |
| S5 | No-RAG control using the best-performing model | same as selected model | Shows how much the retrieval pipeline contributes |

## Relationship to the Previous Project

Do **not** describe Jackie/Wang's project as the single authoritative baseline. A more accurate wording is:

> Use the previous Jetson-Nano-RAG-LLM project as a reference baseline or starting pipeline.

The previous project is useful because it provides a RAG structure, model-serving pattern, and evaluation idea. However, its code, dependencies, and model choices may be outdated. This dissertation can borrow the architecture and reasoning without needing to replicate the old project exactly.

## Runtime Recommendation

Use **llama.cpp** as the primary runtime if practical, because it exposes GGUF quantisation choices clearly and is close to the previous project. Ollama can be discussed as a lower-friction deployment option, but it should not become a second full benchmark axis unless the supervisor explicitly asks for it.

## What to Confirm With the Supervisor

Supervisor feedback received on 2026-06-24 supports proceeding and asks the study to examine stronger size-reduction methods. The working response is to add Q2_K to the same-model quantisation comparison and explain why Q1 is not a core condition.
