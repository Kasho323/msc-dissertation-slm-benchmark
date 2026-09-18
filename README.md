# Local Small Language Models: Dissertation Reproduction Repository

Supporting code and evidence for *Evaluating Local Small Language Models for an
On-Device AI Assistant with Privacy-Preserving Question Answering*, MSc Applied
Artificial Intelligence, ES9U9-60, WMG, University of Warwick.

This repository is prepared for public reviewer access. It contains the frozen
question set, benchmark harness, raw observations, retained ratings, analysis
scripts and instructions to reproduce preprocessing and run new experiments.
The submitted dissertation and personal university records are not published here.

## Start here: reproduce the reported numbers

With Python **3.10 or newer**, no third-party packages or model downloads are
needed for the main integrity and numerical checks:

```sh
git clone https://github.com/Kasho323/msc-dissertation-slm-benchmark.git
cd msc-dissertation-slm-benchmark
python reproduce.py
```

This verifies 1,347 retained evidence files, all 720 final raw responses, the
240 AI-rated answers and 30 independently human-rated answers. It recomputes
quality, speed, memory, truncation, rank association and the Q035 sensitivity
ordering. Outputs go into ignored `reproduction_output/`, never into the
original `benchmark_results/`.

To regenerate the original analysis tables, plots, agreement diagnostics,
20,000-resample intervals and Q2 truncation sensitivity report, use Python 3.10:

```sh
python -m venv .venv
# Windows PowerShell:
.venv/Scripts/python -m pip install -r requirements-analysis.txt
.venv/Scripts/python reproduce.py --full
# macOS/Linux: use .venv/bin/python instead.
```

The full command also checks that the regenerated system summary, blinding key
and quality table match the retained tables. It does not invoke an AI judge or
alter any scores. See [validation and provenance](reproduction/VALIDATION.md).

## Expected checks

| Configuration | Model | Quantisation | Mean quality (six decimals) | Throughput (tok/s) | Observed RSS (MiB) |
|---|---|---|---:|---:|---:|
| C1 | Qwen2.5 0.5B Instruct | Q4_K_M | 3.070833 | 103.42 | 568.37 |
| C2 | Llama 3.2 1B Instruct | Q4_K_M | 3.100000 | 76.07 | 1479.16 |
| C3 | Gemma 3 1B IT | Q4_K_M | 3.575000 | 67.15 | 1001.06 |
| C4 | Qwen2.5 1.5B Instruct | Q2_K | 2.683333 | 82.74 | 906.26 |
| C5 | Qwen2.5 1.5B Instruct | Q4_K_M | 3.433333 | 62.15 | 1793.69 |
| C6 | Qwen2.5 1.5B Instruct | Q8_0 | 3.445833 | 42.82 | 1829.38 |

Quality is the mean of six retained rating dimensions on a 0-5 scale. The table
above shows additional precision for reproducibility; it does not replace the
dissertation's rounded tables. The historical CSV field names use `mb`; the
harness divides bytes by 1024 squared, so these memory values are MiB.

Human-AI Spearman rho is **0.799266** (n=30): a rank-association result, not an
exact-agreement or ground-truth validation claim. Excluding Q035 gives C5
**3.448718**, C6 **3.435897**, reversing their very small full-set ordering.

## Reproduce preprocessing and run new experiments

Follow [the experiment guide](reproduction/EXPERIMENTS.md). It covers:

1. The pinned upstream RAG application and Windows Python environment.
2. Restoring the four exact corpus PDFs with SHA-256 checks.
3. Acquiring and verifying the six GGUF files using Appendix A metadata.
4. Installing the recorded CPU-only llama.cpp runtime.
5. A one-question smoke test, then the full 40 x 3 x 6 suite.

Re-running generation is separate from reproducing the existing statistics.
New measurements go into ignored `replication_runs/`. Runtime, hardware and
retrieval-model version differences can affect a new run. The guide records
known limitations rather than promising identical new measurements.

## Repository map

All paths below are relative to this repository root (the original local
`dissertation_project/` directory).

| Path | Purpose |
|---|---|
| `reproduce.py` | Supported entry point for retained-data checks and analysis |
| `reproduction/` | Current experiment setup, corpus/model verification and validation notes |
| `provenance/` | Input checksums, model metadata and revision information |
| `corpus/` | Licensed historical corpus snapshots, manifest and attribution |
| `benchmark_plan/` | Frozen protocol, 24 June amendment, 40 questions, harness and dated analyses |
| `benchmark_results/` | Immutable historical raw responses, logs, ratings, tables and sensitivity records |
| `literature/` | Retained written reference records, not redistributed source papers |
| `planning/wordcount_official.py` | Historical counting script; its name is not independent proof of a university rule |

The **final** raw run folders are `full_benchmark_C*_20260624_*` with start times
C1 211524, C2 213220, C3 215407, C4 221531, C5 223538 and C6 225248. Earlier
pilot, preliminary and aborted runs remain as evidence but are not selected by
`reproduce.py`. Fixed-seed repetitions produced identical answers within each
configuration-question group; quality scoring uses repetition 1 (240 answers).

## Submission snapshot and subsequent maintenance

The pre-publication repository state is commit
`9dfe890bf1fa9071bca3c7693a03fa75a533a4c4`, containing 1,403 tracked files.
That historical count is the one associated with the dissertation's repository
inventory; the maintained public version adds reproduction support files.
Post-submission maintenance changes access, documentation and execution paths,
not the submitted dissertation, frozen questions, experimental outputs or scores.
Historical documents may describe the repository as private at the time they
were written. The public repository makes reviewer invitations unnecessary.

Model weights, personal ethics certificates, supervision correspondence, private
university documents and the dissertation DOCX/PDF are not included. Third-party
materials retain their own rights; see [corpus attribution](corpus/README.md)
and [upstream application attribution](reproduction/EXPERIMENTS.md).
