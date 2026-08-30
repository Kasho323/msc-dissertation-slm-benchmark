from __future__ import annotations

import csv
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
QUESTION_SET = ROOT / "dissertation_project" / "benchmark_plan" / "question_set_template.csv"
RESULTS_ROOT = ROOT / "dissertation_project" / "benchmark_results"

RUN_FOLDERS = {
    "C1": "full_benchmark_C1_20260619_224126",
    "C2": "full_benchmark_C2_20260619_225653",
    "C3": "full_benchmark_C3_20260619_231534",
}

OUTPUT_CSV = RESULTS_ROOT / "full_benchmark_scoring_review_C1_C2_C3_2026-06-19.csv"
OUTPUT_MD = RESULTS_ROOT / "full_benchmark_scoring_review_summary_2026-06-19.md"


FIELDS = [
    "model_config_id",
    "run_id",
    "question_id",
    "repetition",
    "source_id",
    "source_title",
    "question_type",
    "difficulty",
    "documents_needed",
    "question_text",
    "expected_answer_notes",
    "evidence_location",
    "generated_answer",
    "sources_returned",
    "latency_seconds",
    "tokens_generated",
    "tokens_per_second",
    "peak_memory_mb",
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


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in FIELDS})


def main() -> None:
    questions = {row["question_id"]: row for row in read_csv(QUESTION_SET)}
    rows: list[dict[str, Any]] = []
    counts: dict[str, int] = {}

    for model_config_id, folder_name in RUN_FOLDERS.items():
        answer_log = RESULTS_ROOT / folder_name / "model_answer_log.csv"
        if not answer_log.exists():
            raise FileNotFoundError(answer_log)

        count = 0
        for answer_row in read_csv(answer_log):
            question = questions[answer_row["question_id"]]
            rows.append(
                {
                    "model_config_id": model_config_id,
                    "run_id": answer_row["run_id"],
                    "question_id": answer_row["question_id"],
                    "repetition": answer_row["repetition"],
                    "source_id": question["source_id"],
                    "source_title": question["source_title"],
                    "question_type": question["question_type"],
                    "difficulty": question["difficulty"],
                    "documents_needed": question["documents_needed"],
                    "question_text": answer_row["question_text"],
                    "expected_answer_notes": question["expected_answer_notes"],
                    "evidence_location": question["evidence_location"],
                    "generated_answer": answer_row["generated_answer"],
                    "sources_returned": answer_row["sources_returned"],
                    "latency_seconds": answer_row["latency_seconds"],
                    "tokens_generated": answer_row["tokens_generated"],
                    "tokens_per_second": answer_row["tokens_per_second"],
                    "peak_memory_mb": answer_row["peak_memory_mb"],
                    "scored_by": "Cairenbading",
                }
            )
            count += 1
        counts[model_config_id] = count

    write_csv(OUTPUT_CSV, rows)

    summary_lines = [
        "# Full Benchmark Scoring Review Summary",
        "",
        "**Created:** 2026-06-19",
        "",
        "This file describes the combined scoring review sheet generated from the full C1/C2/C3 benchmark runs.",
        "",
        "## Output",
        "",
        f"- Review CSV: `{OUTPUT_CSV.name}`",
        f"- Total rows: {len(rows)}",
        "",
        "## Rows by Model",
        "",
        "| Model Config | Rows |",
        "|---|---:|",
    ]
    for model_config_id in RUN_FOLDERS:
        summary_lines.append(f"| {model_config_id} | {counts.get(model_config_id, 0)} |")

    summary_lines.extend(
        [
            "",
            "## How to Use",
            "",
            "Score each row using the six 0-5 quality dimensions:",
            "",
            "- relevance",
            "- correctness",
            "- faithfulness_to_source",
            "- completeness",
            "- hallucination_risk",
            "- source_grounding",
            "",
            "Then calculate `average_quality_score` as the mean of the six dimensions.",
            "",
            "The CSV includes the question, expected-answer notes, evidence location, generated answer, retrieved sources, and system metrics on the same row.",
            "",
        ]
    )
    OUTPUT_MD.write_text("\n".join(summary_lines), encoding="utf-8")

    print(f"Wrote {OUTPUT_CSV}")
    print(f"Wrote {OUTPUT_MD}")
    print(f"Rows: {len(rows)}")


if __name__ == "__main__":
    main()
