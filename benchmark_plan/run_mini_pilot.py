from __future__ import annotations

import argparse
import csv
import json
import time
from datetime import datetime
from pathlib import Path
from typing import Any

import psutil
import requests


ROOT = Path(__file__).resolve().parents[2]
QUESTION_SET = ROOT / "dissertation_project" / "benchmark_plan" / "question_set_template.csv"
CORPUS_DIR = ROOT / "docs" / "final_benchmark_corpus"
OUTPUT_ROOT = ROOT / "dissertation_project" / "benchmark_results"
BACKEND_URL = "http://127.0.0.1:8000"


PILOT_QUESTION_IDS = ["Q001", "Q002", "Q003", "Q004", "Q005"]


def read_questions() -> list[dict[str, str]]:
    with QUESTION_SET.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    wanted = set(PILOT_QUESTION_IDS)
    return [row for row in rows if row["question_id"] in wanted]


def upload_corpus() -> str:
    pdfs = sorted(CORPUS_DIR.glob("D*.pdf"))
    if not pdfs:
        raise FileNotFoundError(f"No corpus PDFs found in {CORPUS_DIR}")

    files = []
    try:
        for pdf in pdfs:
            files.append(("files", (pdf.name, pdf.open("rb"), "application/pdf")))
        response = requests.post(f"{BACKEND_URL}/upload", files=files, timeout=300)
        response.raise_for_status()
        return response.text
    finally:
        for _, file_tuple in files:
            file_tuple[1].close()


def llama_memory_mb() -> float | None:
    total = 0
    found = False
    for proc in psutil.process_iter(["name", "memory_info"]):
        try:
            name = (proc.info["name"] or "").lower()
            if "llama-server" in name:
                found = True
                total += proc.info["memory_info"].rss
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    if not found:
        return None
    return round(total / (1024 * 1024), 2)


def post_question(question: str) -> tuple[dict[str, Any], float]:
    payload = {
        "prompt": question,
        "max_tokens": 200,
        "temperature": 0.2,
        "k": 10,
        "n": 3,
    }
    started = time.perf_counter()
    response = requests.post(f"{BACKEND_URL}/", json=payload, timeout=300)
    latency = time.perf_counter() - started
    response.raise_for_status()
    return response.json(), latency


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, Any]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--upload-corpus", action="store_true", help="Upload final corpus before running the pilot.")
    parser.add_argument("--model-config-id", default="C1")
    parser.add_argument("--model-name", default="Qwen2.5 0.5B Instruct")
    parser.add_argument("--quantisation", default="Q4_K_M")
    parser.add_argument("--model-file", default="models/qwen2.5-0.5b-instruct-q4_k_m.gguf")
    parser.add_argument("--output-dir", default="mini_pilot_2026-06-19")
    args = parser.parse_args()

    run_stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    run_id = f"MINI_{args.model_config_id}_{run_stamp}"
    output_dir = OUTPUT_ROOT / args.output_dir
    raw_dir = output_dir / "raw_responses"
    output_dir.mkdir(parents=True, exist_ok=True)
    raw_dir.mkdir(parents=True, exist_ok=True)

    upload_response = ""
    if args.upload_corpus:
        upload_response = upload_corpus()

    questions = read_questions()
    answer_rows: list[dict[str, Any]] = []
    scoring_rows: list[dict[str, Any]] = []
    snippets: list[str] = []
    model_name = ""
    system_fingerprint = ""

    for row in questions:
        question_id = row["question_id"]
        print(f"[{args.model_config_id}] Posting {question_id}...", flush=True)
        response_json, latency = post_question(row["question_text"])
        print(f"[{args.model_config_id}] Completed {question_id} in {latency:.2f}s", flush=True)
        raw_path = raw_dir / f"{question_id}.json"
        raw_path.write_text(json.dumps(response_json, ensure_ascii=False, indent=2), encoding="utf-8")

        choice = response_json.get("choices", [{}])[0]
        message = choice.get("message", {})
        answer = message.get("content", "")
        usage = response_json.get("usage", {})
        timings = response_json.get("timings", {})
        sources = response_json.get("sources_used", {})

        model_name = response_json.get("model", model_name)
        system_fingerprint = response_json.get("system_fingerprint", system_fingerprint)
        tokens_generated = usage.get("completion_tokens") or timings.get("predicted_n", "")
        tokens_per_second = timings.get("predicted_per_second", "")

        answer_rows.append(
            {
                "run_id": run_id,
                "model_config_id": args.model_config_id,
                "question_id": question_id,
                "repetition": 1,
                "question_text": row["question_text"],
                "generated_answer": answer,
                "sources_returned": json.dumps(sources, ensure_ascii=False),
                "latency_seconds": round(latency, 4),
                "time_to_first_token_seconds": "",
                "tokens_generated": tokens_generated,
                "tokens_per_second": tokens_per_second,
                "peak_memory_mb": llama_memory_mb() or "",
                "error_notes": "",
            }
        )
        scoring_rows.append(
            {
                "run_id": run_id,
                "model_config_id": args.model_config_id,
                "question_id": question_id,
                "repetition": 1,
                "relevance": "",
                "correctness": "",
                "faithfulness_to_source": "",
                "completeness": "",
                "hallucination_risk": "",
                "source_grounding": "",
                "average_quality_score": "",
                "scoring_notes": "",
                "scored_by": "Cairenbading",
                "scored_date": "",
            }
        )
        snippets.append(f"- **{question_id}:** {answer[:260].replace(chr(10), ' ')}")

    run_manifest_rows = [
        {
            "run_id": run_id,
            "model_config_id": args.model_config_id,
            "model_name": args.model_name,
            "quantisation": args.quantisation,
            "model_file": args.model_file,
            "runtime": "llama.cpp",
            "runtime_version": system_fingerprint,
            "python_version": "venv Python",
            "os": "Windows",
            "cpu": "TBD",
            "ram_gb": "TBD",
            "gpu": "TBD",
            "power_profile": "plugged_in_high_performance",
            "retrieval_k": 10,
            "rerank_n": 3,
            "temperature": 0.2,
            "max_tokens": 200,
            "context_length": "",
            "repetition_count": 1,
            "start_time": run_stamp,
            "end_time": datetime.now().isoformat(timespec="seconds"),
            "status": "completed",
            "notes": f"Mini pilot on first five questions. Backend model response model={model_name}. Corpus upload response={upload_response}",
        }
    ]

    write_csv(
        output_dir / "model_answer_log_mini_pilot.csv",
        [
            "run_id",
            "model_config_id",
            "question_id",
            "repetition",
            "question_text",
            "generated_answer",
            "sources_returned",
            "latency_seconds",
            "time_to_first_token_seconds",
            "tokens_generated",
            "tokens_per_second",
            "peak_memory_mb",
            "error_notes",
        ],
        answer_rows,
    )
    write_csv(
        output_dir / "answer_scoring_mini_pilot.csv",
        [
            "run_id",
            "model_config_id",
            "question_id",
            "repetition",
            "relevance",
            "correctness",
            "faithfulness_to_source",
            "completeness",
            "hallucination_risk",
            "source_grounding",
            "average_quality_score",
            "scoring_notes",
            "scored_by",
            "scored_date",
        ],
        scoring_rows,
    )
    write_csv(
        output_dir / "run_manifest_mini_pilot.csv",
        [
            "run_id",
            "model_config_id",
            "model_name",
            "quantisation",
            "model_file",
            "runtime",
            "runtime_version",
            "python_version",
            "os",
            "cpu",
            "ram_gb",
            "gpu",
            "power_profile",
            "retrieval_k",
            "rerank_n",
            "temperature",
            "max_tokens",
            "context_length",
            "repetition_count",
            "start_time",
            "end_time",
            "status",
            "notes",
        ],
        run_manifest_rows,
    )

    report = output_dir / "mini_pilot_report.md"
    avg_latency = sum(float(row["latency_seconds"]) for row in answer_rows) / len(answer_rows)
    report.write_text(
        "\n".join(
            [
                "# Mini Pilot Report",
                "",
                f"**Run ID:** `{run_id}`",
                "**Date:** 2026-06-19",
                f"**Model configuration:** {args.model_config_id} - {args.model_name} {args.quantisation}",
                "**Questions:** Q001-Q005",
                "**Repetitions:** 1",
                "**Retrieval/generation:** k=10, n=3, temperature=0.2, max_tokens=200",
                "",
                "## Result",
                "",
                f"- Completed questions: {len(answer_rows)}",
                f"- Average endpoint latency: {avg_latency:.3f} seconds",
                "- Raw JSON responses saved in `raw_responses/`.",
                "- Manual scoring is not completed yet; use `answer_scoring_mini_pilot.csv`.",
                "",
                "## Answer Snippets",
                "",
                *snippets,
                "",
            ]
        ),
        encoding="utf-8",
    )

    print(f"Mini pilot complete: {output_dir}")


if __name__ == "__main__":
    main()
