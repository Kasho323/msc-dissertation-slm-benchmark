from __future__ import annotations

import argparse
import csv
import json
import platform
import re
import subprocess
import time
import winreg
from datetime import datetime
from pathlib import Path
from typing import Any

import psutil
import requests


ROOT = Path(__file__).resolve().parents[1]
QUESTION_SET = ROOT / "benchmark_plan" / "question_set_template.csv"
CORPUS_DIR = ROOT / "corpus"
OUTPUT_ROOT = ROOT / "replication_runs"
BACKEND_URL = "http://127.0.0.1:8000"


ANSWER_LOG_FIELDS = [
    "run_id",
    "model_config_id",
    "question_id",
    "repetition",
    "question_text",
    "generated_answer",
    "sources_returned",
    "finish_reason",
    "prompt_tokens",
    "latency_seconds",
    "time_to_first_token_seconds",
    "tokens_generated",
    "tokens_per_second",
    "peak_memory_mb",
    "error_notes",
]

SCORING_FIELDS = [
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
]

RUN_MANIFEST_FIELDS = [
    "run_id",
    "model_config_id",
    "model_name",
    "quantisation",
    "model_file",
    "model_file_size_mb",
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
    "seed",
    "max_tokens",
    "context_length",
    "repetition_count",
    "start_time",
    "end_time",
    "status",
    "notes",
]


def read_questions(question_ids: list[str] | None, limit: int | None) -> list[dict[str, str]]:
    with QUESTION_SET.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    if question_ids:
        wanted = set(question_ids)
        rows = [row for row in rows if row["question_id"] in wanted]

    if limit is not None:
        rows = rows[:limit]

    if not rows:
        raise ValueError("No questions selected.")

    return rows


def upload_corpus() -> str:
    pdfs = sorted(CORPUS_DIR.glob("D*.pdf"))
    if not pdfs:
        raise FileNotFoundError(f"No corpus PDFs found in {CORPUS_DIR}")

    files = []
    try:
        for pdf in pdfs:
            files.append(("files", (pdf.name, pdf.open("rb"), "application/pdf")))
        response = requests.post(f"{BACKEND_URL}/upload", files=files, timeout=600)
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


def post_question(args: argparse.Namespace, question: str) -> tuple[dict[str, Any], float]:
    payload = {
        "prompt": question,
        "max_tokens": args.max_tokens,
        "temperature": args.temperature,
        "k": args.k,
        "n": args.n,
    }
    started = time.perf_counter()
    response = requests.post(f"{BACKEND_URL}/", json=payload, timeout=args.timeout_seconds)
    latency = time.perf_counter() - started
    response.raise_for_status()
    return response.json(), latency


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, Any]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def safe_average(values: list[float]) -> float | None:
    if not values:
        return None
    return sum(values) / len(values)


def parse_question_ids(value: str) -> list[str]:
    return [item.strip() for item in value.split(",") if item.strip()]


def registry_value(path: str, name: str, default: str = "") -> str:
    try:
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, path) as key:
            value, _ = winreg.QueryValueEx(key, name)
            return str(value)
    except OSError:
        return default


def system_metadata() -> dict[str, str]:
    cpu = registry_value(
        r"HARDWARE\DESCRIPTION\System\CentralProcessor\0",
        "ProcessorNameString",
        platform.processor(),
    ).strip()
    display_version = registry_value(
        r"SOFTWARE\Microsoft\Windows NT\CurrentVersion",
        "DisplayVersion",
    )
    build = registry_value(
        r"SOFTWARE\Microsoft\Windows NT\CurrentVersion",
        "CurrentBuildNumber",
    )
    ubr = registry_value(
        r"SOFTWARE\Microsoft\Windows NT\CurrentVersion",
        "UBR",
    )
    build_label = f"{build}.{ubr}" if build and ubr else build
    os_label = f"Windows 11 {display_version} build {build_label}".strip()

    try:
        power_output = subprocess.check_output(["powercfg", "/GETACTIVESCHEME"])
        power_text = power_output.decode("ascii", errors="ignore")
        guid_match = re.search(
            r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}",
            power_text,
        )
        power_guid = guid_match.group(0).lower() if guid_match else ""
        known_schemes = {
            "381b4222-f694-41f0-9685-ff5bb260df2e": "Balanced",
            "8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c": "High performance",
            "a1841308-3541-4fab-bc81-f71556f20b4a": "Power saver",
            "e9a42b02-d5df-448d-aa00-03f14749eb61": "Ultimate performance",
        }
        power_profile = f"{known_schemes.get(power_guid, 'Unknown')} ({power_guid})"
    except (OSError, subprocess.SubprocessError):
        power_profile = "unavailable"

    return {
        "cpu": cpu,
        "ram_gb": str(round(psutil.virtual_memory().total / (1024**3), 2)),
        "os": os_label,
        "gpu": "Not used; CPU-only llama.cpp build",
        "power_profile": power_profile,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    global CORPUS_DIR, OUTPUT_ROOT
    parser.add_argument("--corpus-dir", type=Path, default=CORPUS_DIR)
    parser.add_argument("--output-root", type=Path, default=OUTPUT_ROOT)
    parser.add_argument("--app-dir", type=Path, default=ROOT / ".runtime" / "rag-app")
    parser.add_argument("--upload-corpus", action="store_true", help="Upload final corpus before running.")
    parser.add_argument("--model-config-id", required=True)
    parser.add_argument("--model-name", required=True)
    parser.add_argument("--quantisation", required=True)
    parser.add_argument("--model-file", required=True)
    parser.add_argument("--output-dir", default="")
    parser.add_argument("--repetitions", type=int, default=3)
    parser.add_argument("--question-ids", default="", help="Comma-separated question IDs, for example Q001,Q002.")
    parser.add_argument("--limit", type=int, default=None, help="Run only the first N selected questions.")
    parser.add_argument("--k", type=int, default=10)
    parser.add_argument("--n", type=int, default=3)
    parser.add_argument("--temperature", type=float, default=0.2)
    parser.add_argument("--max-tokens", type=int, default=512)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--context-length", default="4096")
    parser.add_argument("--timeout-seconds", type=int, default=600)
    parser.add_argument("--scored-by", default="Cairenbading")
    parser.add_argument("--stop-on-error", action="store_true")
    parser.add_argument("--dry-run", action="store_true", help="Validate selection and print planned run only.")
    args = parser.parse_args()
    CORPUS_DIR = args.corpus_dir.resolve()
    OUTPUT_ROOT = args.output_root.resolve()

    if args.repetitions < 1:
        raise ValueError("--repetitions must be at least 1.")

    question_ids = parse_question_ids(args.question_ids) if args.question_ids else None
    questions = read_questions(question_ids=question_ids, limit=args.limit)

    if args.dry_run:
        print("Full benchmark dry run")
        print(f"Model: {args.model_config_id} - {args.model_name} {args.quantisation}")
        print(f"Questions selected: {len(questions)}")
        print(f"Repetitions: {args.repetitions}")
        print(f"Planned answer rows: {len(questions) * args.repetitions}")
        print("First questions:")
        for row in questions[:5]:
            print(f"- {row['question_id']}: {row['question_text']}")
        return

    run_stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    run_id = f"FULL_{args.model_config_id}_{run_stamp}"
    output_dir_name = args.output_dir or f"full_benchmark_{args.model_config_id}_{run_stamp}"
    output_dir = OUTPUT_ROOT / output_dir_name
    raw_dir = output_dir / "raw_responses"
    output_dir = output_dir.resolve()
    protected = (ROOT / "benchmark_results").resolve()
    if output_dir == protected or protected in output_dir.parents:
        raise ValueError("Cannot write a replication into the retained benchmark_results.")
    output_dir.mkdir(parents=True, exist_ok=False)
    raw_dir.mkdir(parents=True, exist_ok=True)

    upload_response = ""
    if args.upload_corpus:
        print("Uploading final benchmark corpus...", flush=True)
        upload_response = upload_corpus()
        print(f"Upload response: {upload_response}", flush=True)

    answer_rows: list[dict[str, Any]] = []
    scoring_rows: list[dict[str, Any]] = []
    model_name = ""
    system_fingerprint = ""
    errors: list[str] = []

    total = len(questions) * args.repetitions
    completed = 0
    started_iso = datetime.now().isoformat(timespec="seconds")

    for repetition in range(1, args.repetitions + 1):
        for row in questions:
            question_id = row["question_id"]
            completed += 1
            print(
                f"[{args.model_config_id}] {completed}/{total} posting {question_id} rep {repetition}...",
                flush=True,
            )

            response_json: dict[str, Any] = {}
            latency: float | str = ""
            answer = ""
            sources: Any = {}
            tokens_generated: Any = ""
            prompt_tokens: Any = ""
            tokens_per_second: Any = ""
            finish_reason = ""
            error_notes = ""

            try:
                response_json, measured_latency = post_question(args, row["question_text"])
                latency = round(measured_latency, 4)
                choice = response_json.get("choices", [{}])[0]
                message = choice.get("message", {})
                answer = message.get("content", "")
                finish_reason = choice.get("finish_reason", "")
                usage = response_json.get("usage", {})
                timings = response_json.get("timings", {})
                sources = response_json.get("sources_used", {})
                model_name = response_json.get("model", model_name)
                system_fingerprint = response_json.get("system_fingerprint", system_fingerprint)
                tokens_generated = usage.get("completion_tokens") or timings.get("predicted_n", "")
                prompt_tokens = usage.get("prompt_tokens", "")
                tokens_per_second = timings.get("predicted_per_second", "")
                print(
                    f"[{args.model_config_id}] completed {question_id} rep {repetition} in {measured_latency:.2f}s",
                    flush=True,
                )
            except Exception as exc:  # noqa: BLE001 - keep benchmark moving and record the failure.
                error_notes = f"{type(exc).__name__}: {exc}"
                errors.append(f"{question_id} rep {repetition}: {error_notes}")
                print(f"[{args.model_config_id}] ERROR {question_id} rep {repetition}: {error_notes}", flush=True)
                response_json = {"error": error_notes}
                if args.stop_on_error:
                    raise

            raw_path = raw_dir / f"{question_id}_rep{repetition}.json"
            raw_path.write_text(json.dumps(response_json, ensure_ascii=False, indent=2), encoding="utf-8")

            answer_rows.append(
                {
                    "run_id": run_id,
                    "model_config_id": args.model_config_id,
                    "question_id": question_id,
                    "repetition": repetition,
                    "question_text": row["question_text"],
                    "generated_answer": answer,
                    "sources_returned": json.dumps(sources, ensure_ascii=False),
                    "finish_reason": finish_reason,
                    "prompt_tokens": prompt_tokens,
                    "latency_seconds": latency,
                    "time_to_first_token_seconds": "",
                    "tokens_generated": tokens_generated,
                    "tokens_per_second": tokens_per_second,
                    "peak_memory_mb": llama_memory_mb() or "",
                    "error_notes": error_notes,
                }
            )
            scoring_rows.append(
                {
                    "run_id": run_id,
                    "model_config_id": args.model_config_id,
                    "question_id": question_id,
                    "repetition": repetition,
                    "relevance": "",
                    "correctness": "",
                    "faithfulness_to_source": "",
                    "completeness": "",
                    "hallucination_risk": "",
                    "source_grounding": "",
                    "average_quality_score": "",
                    "scoring_notes": "",
                    "scored_by": args.scored_by,
                    "scored_date": "",
                }
            )

    status = "completed_with_errors" if errors else "completed"
    ended_iso = datetime.now().isoformat(timespec="seconds")
    hardware = system_metadata()
    manifest_rows = [
        {
            "run_id": run_id,
            "model_config_id": args.model_config_id,
            "model_name": args.model_name,
            "quantisation": args.quantisation,
            "model_file": args.model_file,
            "model_file_size_mb": round(
                (args.app_dir / args.model_file).stat().st_size / (1024 * 1024),
                2,
            ),
            "runtime": "llama.cpp",
            "runtime_version": system_fingerprint,
            "python_version": "venv Python",
            "os": hardware["os"],
            "cpu": hardware["cpu"],
            "ram_gb": hardware["ram_gb"],
            "gpu": hardware["gpu"],
            "power_profile": hardware["power_profile"],
            "retrieval_k": args.k,
            "rerank_n": args.n,
            "temperature": args.temperature,
            "seed": args.seed,
            "max_tokens": args.max_tokens,
            "context_length": args.context_length,
            "repetition_count": args.repetitions,
            "start_time": started_iso,
            "end_time": ended_iso,
            "status": status,
            "notes": (
                f"Full benchmark run. Questions={len(questions)}. "
                f"Backend model response model={model_name}. Corpus upload response={upload_response}. "
                f"Errors={len(errors)}."
            ),
        }
    ]

    write_csv(output_dir / "model_answer_log.csv", ANSWER_LOG_FIELDS, answer_rows)
    write_csv(output_dir / "answer_scoring.csv", SCORING_FIELDS, scoring_rows)
    write_csv(output_dir / "run_manifest.csv", RUN_MANIFEST_FIELDS, manifest_rows)

    latency_values = [float(row["latency_seconds"]) for row in answer_rows if row["latency_seconds"] != ""]
    memory_values = [float(row["peak_memory_mb"]) for row in answer_rows if row["peak_memory_mb"] != ""]
    tps_values = [float(row["tokens_per_second"]) for row in answer_rows if row["tokens_per_second"] != ""]

    avg_latency = safe_average(latency_values)
    avg_memory = safe_average(memory_values)
    avg_tps = safe_average(tps_values)

    report_lines = [
        "# Full Benchmark Run Report",
        "",
        f"**Run ID:** `{run_id}`",
        f"**Model configuration:** {args.model_config_id} - {args.model_name} {args.quantisation}",
        f"**Questions:** {len(questions)}",
        f"**Repetitions:** {args.repetitions}",
        f"**Total attempted answers:** {len(answer_rows)}",
        f"**Status:** {status}",
        "",
        "## Settings",
        "",
        f"- retrieval k: {args.k}",
        f"- rerank n: {args.n}",
        f"- temperature: {args.temperature}",
        f"- seed: {args.seed}",
        f"- max_tokens: {args.max_tokens}",
        f"- context_length: {args.context_length}",
        "",
        "## System Metrics",
        "",
        f"- Mean latency: {avg_latency:.3f} seconds" if avg_latency is not None else "- Mean latency: unavailable",
        f"- Mean peak memory estimate: {avg_memory:.2f} MiB" if avg_memory is not None else "- Mean peak memory estimate: unavailable",
        f"- Mean tokens/s: {avg_tps:.2f}" if avg_tps is not None else "- Mean tokens/s: unavailable",
        "",
        "## Files",
        "",
        "- `run_manifest.csv`",
        "- `model_answer_log.csv`",
        "- `answer_scoring.csv`",
        "- `raw_responses/`",
        "",
        "## Errors",
        "",
    ]
    if errors:
        report_lines.extend(f"- {error}" for error in errors)
    else:
        report_lines.append("- None")

    (output_dir / "benchmark_run_report.md").write_text("\n".join(report_lines) + "\n", encoding="utf-8")

    print(f"Full benchmark run complete: {output_dir}")
    print(f"Status: {status}")


if __name__ == "__main__":
    main()
