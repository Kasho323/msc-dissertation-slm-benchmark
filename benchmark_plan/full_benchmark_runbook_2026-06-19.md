# Full Benchmark Runbook

**Created:** 2026-06-19  
**Purpose:** Commands for running the frozen 40-question benchmark.

## Files

| File | Purpose |
|---|---|
| `run_full_benchmark.py` | Runs the selected question set against the already-running backend/model server and writes benchmark outputs. |
| `run_benchmark_config.ps1` | Starts one llama.cpp model configuration, runs `run_full_benchmark.py`, then stops that model server. |
| `run_full_benchmark_with_backend.ps1` | Starts a temporary backend if needed, calls `run_benchmark_config.ps1`, then stops only the backend it started. |

The helper currently supports the locally available model configurations:

- C1: Qwen2.5 0.5B Instruct Q4_K_M
- C2: Llama 3.2 1B Instruct Q4_K_M
- C3: Gemma 3 1B IT Q4_K_M

## Before Running

For benchmark runs, do not start the full `start_all.ps1` stack first. The benchmark helper starts and stops `llama-server` on port 8080 for each model configuration, so port 8080 must be free.

Start the FastAPI backend from the RAG repo root:

```powershell
cd C:\Users\Crbd2\Desktop\Dissertation\Jetson-Nano-RAG-LLM
.\venv\Scripts\python.exe -m uvicorn main:app --port 8000
```

The backend uses in-memory ChromaDB. If the backend was restarted, use `-UploadCorpus` on the first benchmark helper command.

## Dry Run

Validate that the runner sees the frozen 40-question set:

```powershell
.\Jetson-Nano-RAG-LLM\venv\Scripts\python.exe .\dissertation_project\benchmark_plan\run_full_benchmark.py --model-config-id C1 --model-name "Qwen2.5 0.5B Instruct" --quantisation Q4_K_M --model-file "models/qwen2.5-0.5b-instruct-q4_k_m.gguf" --dry-run
```

Expected dry-run result:

- 40 selected questions
- 3 repetitions
- 120 planned answer rows

## Smoke Test

Run one question once:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\dissertation_project\benchmark_plan\run_benchmark_config.ps1 -ModelConfigId C1 -Limit 1 -Repetitions 1 -UploadCorpus -StopOnError
```

This was validated on 2026-06-19 and produced:

`dissertation_project/benchmark_results/full_benchmark_C1_20260619_223429/`

## Full Runs

Run C1:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\dissertation_project\benchmark_plan\run_benchmark_config.ps1 -ModelConfigId C1 -Repetitions 3 -UploadCorpus
```

If the backend is not already running, use the wrapper:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\dissertation_project\benchmark_plan\run_full_benchmark_with_backend.ps1 -ModelConfigId C1 -Repetitions 3 -UploadCorpus
```

## Max Tokens Amendment Option

The 2026-06-20 finish-reason audit found many `finish_reason=length` outputs with `max_tokens=200`. If the protocol is amended to use a higher output limit, run with `-MaxTokens 512`, for example:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\dissertation_project\benchmark_plan\run_full_benchmark_with_backend.ps1 -ModelConfigId C1 -Repetitions 3 -UploadCorpus -MaxTokens 512
```

Use the same `-MaxTokens` value for every model configuration in the final benchmark.

Run C2:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\dissertation_project\benchmark_plan\run_benchmark_config.ps1 -ModelConfigId C2 -Repetitions 3
```

Run C3:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\dissertation_project\benchmark_plan\run_benchmark_config.ps1 -ModelConfigId C3 -Repetitions 3
```

Use `-UploadCorpus` again only if the backend has been restarted since the previous upload.

## Output Files

Each full run creates:

- `run_manifest.csv`
- `model_answer_log.csv`
- `answer_scoring.csv`
- `benchmark_run_report.md`
- `raw_responses/`

Manual scoring should be entered into `answer_scoring.csv` after the run. Do not edit `model_answer_log.csv` except for clearly marked error notes.

## Runtime Estimate

Based on the five-question controlled mini pilot:

- C1 should be the fastest.
- C2 should be slower and use more memory.
- C3 should be slowest but may provide better quality.

Each 40-question, 3-repetition run produces 120 answers. Run one model configuration at a time.
