# Evaluating Local Small Language Models for an On-Device AI Assistant with Privacy-Preserving Question Answering

Supporting material for an MSc Applied Artificial Intelligence dissertation
(module ES9U9-60, WMG, University of Warwick).

The study benchmarks six local small language model configurations on a consumer laptop
under a single fixed retrieval-augmented generation pipeline, measuring answer quality and
computational cost together, and includes a controlled comparison of three quantisation
levels applied to one base model.

This repository holds the reproducibility inventory listed in Appendix G of the
dissertation. It is not a software product and is not intended to be installed as one.

## What is here

| Path | Contents |
|---|---|
| `dissertation_project/benchmark_plan/` | The protocol frozen on 19 June 2026 and its 24 June amendment, the benchmark runbook and harness, the frozen 40-question set, and the analysis scripts |
| `dissertation_project/benchmark_results/` | Raw model outputs, per-run manifests and answer logs, retrieved-source records, the blinding key, both raters' scores, audit summaries and sensitivity analyses |
| `dissertation_project/literature/` | Reference verification records, the final Harvard reference list, and the link and date verification log |
| `dissertation_project/planning/wordcount_official.py` | The word-count script used for the submission |
| `docs/final_benchmark_corpus/` | The four public source documents used as the retrieval corpus, with their manifest |

## Experimental record

Six configurations answered the same 40 questions three times under fixed settings,
producing 720 generated outputs on one laptop. Every output, together with the sources it
retrieved and the system measurements taken at the time, is retained under
`dissertation_project/benchmark_results/full_benchmark_C*_20260624_*/`.

| Setting | Value |
|---|---|
| Runtime | llama.cpp build `b9587-d2e22ed97`, CPU-only |
| Operating system | Windows 11 25H2 build 26200.8655 |
| Processor | Intel Core Ultra 9 275HX |
| Retrieval | k = 10, reranked to n = 3 |
| Generation | temperature 0.2, seed 42, max 512 tokens, 4096-token context |
| Repetitions | 3 per question |

Because generation used a fixed seed at temperature 0.2, all three repetitions produced
identical text in all 240 configuration–question groups, so quality scoring was applied to
the 240 unique first-repetition answers.

## What is not here

Model weights are not stored in this repository. The six GGUF files are published releases;
their source repositories and SHA-256 checksums are recorded in Appendix A of the
dissertation, which is sufficient to obtain and verify the exact files used.

The retrieval application was adapted from a previous student project rather than written
for this study, and is available separately at
<https://github.com/jackiewaang/Jetson-Nano-RAG-LLM>. The llama.cpp runtime is obtained
from <https://github.com/ggml-org/llama.cpp>.

Downloaded copies of cited papers and example theses are excluded because they are subject
to third-party copyright. Personal ethics-training certificates and supervision records are
excluded as personal data.

## Reproducing the analysis

The analysis scripts read only the retained result files and can be run without re-executing
any model.

```
pip install -r requirements.txt
cd dissertation_project/benchmark_plan
python analyze_clean30_agreement_2026_07_09.py
python analyze_agreement_intervals_2026-08-23.py
python analyze_q2_truncation_sensitivity_2026_07_23.py
```

Re-running the 720 generations is a separate matter. Any such run produces a new replication
dataset and must be stored separately; it does not replace the 24 June 2026 record, which is
the dataset the dissertation reports.

## Status

This repository is private while the dissertation is under assessment.
