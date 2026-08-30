from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SOURCE = (
    ROOT
    / "dissertation_project"
    / "benchmark_results"
    / "full_benchmark_blind_scoring_rep1_only_C1_C6_2026-06-24.csv"
)
OUTPUT_DIR = (
    ROOT
    / "dissertation_project"
    / "benchmark_results"
    / "ai_second_rater_batches_2026-06-25"
)
BATCH_SIZE = 30

INPUT_FIELDS = [
    "blind_answer_id",
    "question_id",
    "source_id",
    "question_type",
    "difficulty",
    "question_text",
    "expected_answer_notes",
    "evidence_location",
    "generated_answer",
]


def main() -> None:
    with SOURCE.open(newline="", encoding="utf-8") as file:
        rows = list(csv.DictReader(file))

    if len(rows) != 240:
        raise ValueError(f"Expected 240 rep-1 blind rows, found {len(rows)}")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    manifest = []
    for start in range(0, len(rows), BATCH_SIZE):
        batch_number = start // BATCH_SIZE + 1
        selected = [
            {field: row[field] for field in INPUT_FIELDS}
            for row in rows[start : start + BATCH_SIZE]
        ]
        batch_path = OUTPUT_DIR / f"batch_{batch_number:02d}.json"
        batch_path.write_text(
            json.dumps(selected, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        manifest.append(
            {
                "batch_number": batch_number,
                "input_file": batch_path.name,
                "rows": len(selected),
                "first_answer_id": selected[0]["blind_answer_id"],
                "last_answer_id": selected[-1]["blind_answer_id"],
                "status": "prepared",
            }
        )

    with (OUTPUT_DIR / "manifest.csv").open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=list(manifest[0]))
        writer.writeheader()
        writer.writerows(manifest)

    print(f"Prepared {len(manifest)} batches in {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
