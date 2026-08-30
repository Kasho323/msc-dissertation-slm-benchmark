# Protocol Amendment - Quantisation Sensitivity Study

**Date:** 2026-06-24  
**Reason:** Supervisor feedback received after review of the refined research plan  
**Status:** Adopted for the next pilot and final benchmark runs

## Supervisor Feedback

The supervisor recommended exploring stronger methods of reducing model size and examining how they affect the final output, specifically asking why the study included Q4 and Q8 but not Q1 or Q2.

## Amendment

The final benchmark is expanded from five to six model configurations:

| ID | Model | Quantisation | Purpose |
|---|---|---|---|
| C1 | Qwen2.5 0.5B Instruct | Q4_K_M | Small lower-bound configuration |
| C2 | Llama 3.2 1B Instruct | Q4_K_M | Cross-family 1B comparison |
| C3 | Gemma 3 1B IT | Q4_K_M | Cross-family 1B comparison |
| C4 | Qwen2.5 1.5B Instruct | Q2_K | Strong model-size reduction condition |
| C5 | Qwen2.5 1.5B Instruct | Q4_K_M | Mid-level quantisation condition |
| C6 | Qwen2.5 1.5B Instruct | Q8_0 | Higher-precision quantisation condition |

The C4-C6 comparison holds the model architecture and parameter count fixed. The RAG pipeline, corpus, 40-question set, retrieval settings, context length, temperature, output-token limit, and repetitions must also remain fixed.

## Why Q1 Is Not a Core Condition

The official `Qwen/Qwen2.5-1.5B-Instruct-GGUF` release provides Q2_K as its lowest standard quantisation and does not provide a Q1 file. Introducing a Q1 model from a different conversion source or using a different importance-matrix process would add a second uncontrolled variable. Q1 is therefore excluded from the core benchmark.

If a reliable Q1 variant can later be generated from the same source model using a documented and reproducible llama.cpp procedure, it may be tested on a small question subset as an optional feasibility boundary. It will not delay or replace the six core conditions.

## Updated Generation Setting

The initial C1-C3 runs used `max_tokens=200`. A raw-response audit found frequent `finish_reason=length`, so those runs remain preliminary system-validation evidence.

All final runs will use:

| Setting | Final value |
|---|---|
| retrieval k | 10 |
| rerank n | 3 |
| temperature | 0.2 |
| max output tokens | 512 |
| context length | 4096 |
| repetitions | 3 |

## Quantisation Analysis

For C4-C6, report:

- model file size;
- observed llama-server process RSS;
- answer latency;
- generated-token throughput;
- answer-quality scores;
- truncation and error rates;
- any loading, stability, or deployment problems.

The analysis will test whether the storage and memory savings from Q2_K are accompanied by measurable losses in correctness, completeness, faithfulness, or source grounding relative to Q4_K_M and Q8_0.

## Immediate Execution Order

1. Download the official Qwen2.5 1.5B Q2_K, Q4_K_M, and Q8_0 GGUF files.
2. Verify file sizes and that llama.cpp can load each file.
3. Run a five-question pilot for C4-C6 with `max_tokens=512`.
4. Check errors, output truncation, latency, memory, and retrieved-source logging.
5. Rerun C1-C3 and run C4-C6 on the frozen 40-question set.
6. Prepare a new blinded scoring file across all six configurations.
