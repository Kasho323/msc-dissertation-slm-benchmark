# Benchmark Plan - Overview

The empirical core of the dissertation is a compact benchmark of local small language model configurations for question answering.

## What Is Being Compared

The benchmark compares **4-6 model configurations** on the same laptop, using the same RAG-style pipeline and the same evaluation question set.

A model configuration means:

- model family and size
- quantisation level
- runtime setup

This is more manageable than comparing many entirely different models, and it still produces a meaningful dissertation benchmark.

## Relationship to the Previous Project

The previous Jetson-Nano-RAG-LLM project should be described as a **reference baseline or starting pipeline**.

It provides useful ideas:

- local RAG architecture
- retrieval and reranking structure
- local GGUF model serving
- quality and system metric categories

But the dissertation does not need to replicate it exactly. The old code and models may be outdated, so this project can adapt the structure while keeping the benchmark controlled.

## Benchmark Outputs

For each configuration:

- answer quality scores
- latency or time-to-first-token
- throughput
- peak memory use
- model size on disk
- deployment notes

For the dissertation:

- comparison table across configurations
- Q2 vs Q4 vs Q8 controlled quantisation comparison
- quality-vs-cost plot
- structured privacy comparison matrix
- final recommendation such as "if the priority is speed, choose X; if the priority is answer quality, choose Y"

## Recommended Scale

| Item | Recommended Scope |
|---|---|
| Model configurations | 4-6 |
| Evaluation questions | 30-40, with 50 as the upper limit |
| Repetitions | Aim for 3 per configuration if runtime allows |
| Pipeline variants | 1 fixed pipeline |
| Hardware | Student laptop only |

## Working Phases

| Phase | Outcome |
|---|---|
| Phase 1 | Confirm model list, dataset/question set, and rubric |
| Phase 2 | Build or adapt benchmark runner and run a small pilot |
| Phase 3 | Freeze protocol and run final benchmark |
| Phase 4 | Analyse data and write Results/Discussion |
| Phase 5 | Finish full dissertation and submission materials |

## Hard Constraints

- Do not expand into a large system-building project.
- Do not treat local deployment as automatically private.
- Do not test too many models.
- Do not change the question set between models.
- Do not change retrieval settings after the protocol is frozen.

## Current Quantisation Decision

- The supervisor approved the overall direction on 2026-06-24 and requested investigation of stronger model-size reduction.
- The final working set contains six configurations.
- Qwen2.5 1.5B Q2_K, Q4_K_M, and Q8_0 form the controlled quantisation study.
- Q1 is excluded from the core comparison because it is not provided in the official Qwen GGUF release.
- Any Q1-class test is optional and must not delay the core benchmark.
