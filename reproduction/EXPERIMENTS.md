# Re-running the experiments

## Scope and fixed evidence

`python reproduce.py --full` recomputes statistics from the retained observations
and ratings. It does not regenerate model answers or AI/human ratings. A fresh
generation run is a **replication**, with its own timestamps and measurements.
Do not expect identical speed or memory measurements on different hardware.
The frozen 40-question bank and all original scores remain unchanged.

The tested experiment platform was Windows 11, Intel Core Ultra 9 275HX,
31.43 GiB reported RAM, Balanced power plan, CPU-only llama.cpp. The benchmark
uses k=10, n=3, temperature=0.2, seed=42, max_tokens=512, context=4096 and three
repetitions. C1-C3 compare complete configurations; only C4-C6 hold the base
model fixed for the quantisation comparison.

## 1. Backend and Python environment

Install Git and Python **3.10** for the experiment scripts. From this repository:

```powershell
powershell -NoProfile -ExecutionPolicy RemoteSigned -File reproduction/setup_backend.ps1 -Python python
```

This clones [Jackie Wang's RAG application](https://github.com/jackiewaang/Jetson-Nano-RAG-LLM)
to `.runtime/rag-app` at commit `e63300ab9514804889a27a71827041963b47b909`.
It is an external dependency; its implementation is not claimed as original
dissertation code. No licence was found in that upstream checkout, so its
source is not vendored or relicensed here. The setup script pins the code and
checks package consistency. `requirements-experiment.txt` captures the working
Windows environment inspected on 18 September 2026; it is not a retroactive
claim that every transitive package was recorded in June. The old root
`requirements.txt` is retained as a historical partial dependency list.

The current setup does not need Unix-only uvloop. Start the backend only on
loopback; the upstream API is a research prototype, not a public web service.

## 2. Corpus and models

```powershell
python reproduction/prepare_corpus.py
```

The three licensed corpus snapshots are included; the fourth downloads from
arXiv at a verified version. All four SHA-256 values must pass. See
[`corpus/README.md`](../corpus/README.md) for provenance and reuse notices.

Download each GGUF from the exact revision URL in
[`provenance/models.json`](../provenance/models.json), respecting the source
model's licence/access terms, into `.runtime/rag-app/models/`. These six
revision IDs and file hashes were transcribed from the **current dissertation's
Appendix A**, without changing the dissertation. Then run:

```powershell
python reproduction/check_models.py
```

The RAG backend also needs `sentence-transformers/all-MiniLM-L6-v2` and
`cross-encoder/ms-marco-MiniLM-L6-v2`. Put their complete model directories at
`.runtime/rag-app/models/all-MiniLM-L6-v2` and
`.runtime/rag-app/models/ms-marco-MiniLM-L6-v2`, respectively. The upstream
backend otherwise attempts to download them. For offline operation provision
both first. `provenance/retrieval_models_sha256.json` records the retained local
file hashes inspected for this release. The June run manifests did not record
their Hugging Face revision IDs; do not assume that an unpinned current download
is necessarily identical. This is a recorded replication limitation.

## 3. Generation runtime

Use the CPU-only Windows x64 llama.cpp **b9587** release, commit prefix
`d2e22ed97`, from [the official release](https://github.com/ggml-org/llama.cpp/releases/tag/b9587).
Extract the executable and companion DLLs into `.runtime/llama.cpp/` and check
`.runtime/llama.cpp/llama-server.exe --version`. Do not silently use the newest
runtime. The original cache, context and seed flags are preserved by the runner.

## 4. Smoke test and full suite

```powershell
powershell -NoProfile -ExecutionPolicy RemoteSigned -File benchmark_plan/run_benchmark_suite.ps1 -ModelConfigIds C1 -Repetitions 1 -Limit 1
powershell -NoProfile -ExecutionPolicy RemoteSigned -File benchmark_plan/run_benchmark_suite.ps1
```

The second command runs all six configurations, 40 questions, three repetitions.
It can take hours. The script launches one shared FastAPI backend, uploads the
corpus once and then runs each GGUF in sequence. Ports 8000 and 8080 must be free.
It stops only the processes it launches. The app performs PDF loading, whitespace
and non-ASCII cleaning, 512-character splitting with 100-character overlap,
embedding/indexing, retrieval and reranking. Each run retains raw responses,
retrieved sources, answer logs, measurements, and a run manifest.

New runs and service logs go into ignored `replication_runs/`; existing run
directories cannot be overwritten. You may supply `-AppDir`, `-LlamaDir` and
`-CorpusDir` for another installation. There are no author-specific paths in
this supported entry point.

For a non-generating selection check:

```powershell
python benchmark_plan/run_full_benchmark.py --model-config-id C1 --model-name "Qwen2.5 0.5B Instruct" --quantisation Q4_K_M --model-file models/qwen2.5-0.5b-instruct-q4_k_m.gguf --dry-run
```

## 5. Scoring and interpretation

The retained AI scores cover the 240 first-repetition answers; 30 independent
human ratings support the reported agreement analysis. A new run requires a
new, separately documented scoring exercise; an external judge may change over
time and is not made deterministic by the generation seed. No API key or paid
service is required to reproduce the **existing** statistics.

Historical runbooks/scripts are retained for auditability. Some contain the
original author's local paths or early 200-token settings. Use this guide and
the 24 June protocol amendment for a final-benchmark replication, not the
19 June preliminary runs. Historical notes are not new claims or current
university submission guidance.
