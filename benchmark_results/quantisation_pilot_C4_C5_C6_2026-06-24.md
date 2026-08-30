# Qwen2.5 1.5B Quantisation Pilot

**Date:** 2026-06-24  
**Status:** Preliminary five-question feasibility pilot, not final answer-quality evidence

## Purpose

This pilot responds to supervisor feedback asking why only Q4 and Q8 were proposed and whether stronger model-size reduction such as Q1 or Q2 could be explored.

The official Qwen2.5 1.5B GGUF release provides Q2_K, Q4_K_M, and Q8_0. It does not provide a standard Q1 file. The controlled pilot therefore compares:

- C4: Qwen2.5 1.5B Instruct Q2_K
- C5: Qwen2.5 1.5B Instruct Q4_K_M
- C6: Qwen2.5 1.5B Instruct Q8_0

## Controlled Settings

- same Qwen2.5 1.5B base model;
- same four-document corpus;
- same questions Q001-Q005;
- same FastAPI backend and in-memory vector store;
- same retrieved chunks for all 5 questions across C4-C6;
- retrieval `k=10`;
- rerank `n=3`;
- temperature `0.2`;
- `max_tokens=512`;
- context length `4096`;
- llama.cpp seed `42`;
- one repetition for feasibility checking.

## Preliminary System Results

| Config | Quantisation | File size (MiB) | Mean latency (s) | Mean tokens/s | Observed mean llama-server RSS (MiB) | Mean output tokens | Errors | Length stops |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| C4 | Q2_K | 718.0 | 6.580 | 67.52 | 890.10 | 216.2 | 0 | 0 |
| C5 | Q4_K_M | 1065.6 | 5.184 | 54.23 | 1776.42 | 117.4 | 0 | 0 |
| C6 | Q8_0 | 1806.8 | 5.987 | 39.28 | 1810.09 | 86.2 | 0 | 0 |

Q2_K is approximately 60.3% smaller on disk than Q8_0. In this pilot, its observed llama-server RSS was approximately 50.8% lower than Q8_0.

The latency means must not be interpreted as final speed rankings because output lengths differed substantially. Throughput, latency, and answer quality must be analysed together in the full repeated benchmark.

## Preliminary Output Observations

- All 15 requests completed successfully with `finish_reason=stop`.
- No answer reached the 512-token limit.
- Q2_K produced much longer answers on average and showed visible repetition and less controlled synthesis in some examples.
- Q4_K_M was more concise but declined to answer Q003 because the context did not directly cover the question.
- Q8_0 produced concise answers overall, but its Q003 response drifted into loosely related evaluation details.
- These observations justify the full blinded quality evaluation; they are not sufficient for a quality conclusion.

## Retrieval Fairness Check

An earlier pilot restarted and rebuilt the backend for every model and produced different retrieved chunk signatures for Q003 and Q005. The controlled suite was therefore changed to:

1. start FastAPI once;
2. upload and index the corpus once;
3. keep the same vector store active;
4. switch only the llama.cpp model between configurations.

After this correction, the retrieved source signatures were identical across C4-C6 for all five pilot questions.

## Model File Verification

| Quantisation | SHA-256 |
|---|---|
| Q2_K | `5EDE348E91CE1E7A330926EC5B202C27B864D065149DC463257FDE1F98865B3A` |
| Q4_K_M | `6A1A2EB6D15622BF3C96857206351BA97E1AF16C30D7A74EE38970E434E9407E` |
| Q8_0 | `D7EFB072E7724D25048A4FDA0A3E10B04BDEF5D06B1403A1C93BD9F1240A63C8` |

## Environment

- CPU: Intel Core Ultra 9 275HX
- logical processors: 24
- RAM: 31.43 GiB
- GPU present: NVIDIA GeForce RTX 5070 Laptop GPU
- inference runtime: CPU-only llama.cpp build; GPU not used
- OS: Windows 11 25H2, build 26200.8655
- active power plan during this pilot: Balanced
- Python: 3.10.11
- llama.cpp: build 9587 (`d2e22ed97`)

## Next Action

Before the final 40-question, three-repetition runs:

1. choose and keep one power plan for every configuration;
2. use `run_benchmark_suite.ps1` so all configurations share one vector store;
3. rerun C1-C3 with `max_tokens=512` and seed `42`;
4. run C4-C6 under the same protocol;
5. regenerate the blinded scoring dataset for all six configurations.
