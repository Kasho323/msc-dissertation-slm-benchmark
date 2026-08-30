from __future__ import annotations

import csv
import json
from collections import defaultdict
from pathlib import Path
from statistics import mean


ROOT = Path(__file__).resolve().parents[2]
RESULTS = ROOT / "dissertation_project" / "benchmark_results"
BATCH_DIR = RESULTS / "ai_second_rater_batches_2026-06-25"
SOURCE = RESULTS / "full_benchmark_blind_scoring_rep1_only_C1_C6_2026-06-24.csv"
OUTPUT = RESULTS / "ai_second_rater_codex_gpt_C1_C6_2026-06-25.csv"
SUMMARY = RESULTS / "ai_second_rater_codex_gpt_summary_2026-06-25.md"

SCORE_FIELDS = [
    "relevance",
    "correctness",
    "faithfulness_to_source",
    "completeness",
    "hallucination_risk",
    "source_grounding",
]


def main() -> None:
    with SOURCE.open(newline="", encoding="utf-8") as file:
        source_rows = list(csv.DictReader(file))
    source_by_id = {row["blind_answer_id"]: row for row in source_rows}

    ratings = []
    for batch_number in range(1, 9):
        path = BATCH_DIR / f"batch_{batch_number:02d}_codex_gpt_ratings.json"
        rows = json.loads(path.read_text(encoding="utf-8"))
        if len(rows) != 30:
            raise ValueError(f"{path.name}: expected 30 rows, found {len(rows)}")
        for row in rows:
            row["batch_number"] = batch_number
        ratings.extend(rows)

    ids = [row["blind_answer_id"] for row in ratings]
    if len(ids) != 240 or len(set(ids)) != 240:
        raise ValueError("Ratings must contain exactly 240 unique IDs.")
    if set(ids) != set(source_by_id):
        missing = sorted(set(source_by_id) - set(ids))
        extra = sorted(set(ids) - set(source_by_id))
        raise ValueError(f"ID mismatch. Missing={missing}; extra={extra}")

    output_rows = []
    batch_averages: dict[int, list[float]] = defaultdict(list)
    code_averages: dict[str, list[float]] = defaultdict(list)

    for rating in ratings:
        scores = []
        for field in SCORE_FIELDS:
            value = rating[field]
            if not isinstance(value, int) or not 0 <= value <= 5:
                raise ValueError(
                    f"{rating['blind_answer_id']} invalid {field}: {value}"
                )
            scores.append(value)

        calculated = round(sum(scores) / 6, 3)
        if abs(calculated - float(rating["average_quality_score"])) > 0.001:
            raise ValueError(
                f"{rating['blind_answer_id']} average mismatch: "
                f"{rating['average_quality_score']} vs {calculated}"
            )

        source = source_by_id[rating["blind_answer_id"]]
        output_row = {
            "blind_answer_id": rating["blind_answer_id"],
            "blind_model_code": source["blind_model_code"],
            "question_id": source["question_id"],
            "repetition": source["repetition"],
            "source_id": source["source_id"],
            "question_type": source["question_type"],
            "difficulty": source["difficulty"],
            **{field: rating[field] for field in SCORE_FIELDS},
            "average_quality_score": calculated,
            "scoring_notes": rating["scoring_notes"],
            "rated_by": rating["rated_by"],
            "rated_date": rating["rated_date"],
            "batch_number": rating["batch_number"],
        }
        output_rows.append(output_row)
        batch_averages[rating["batch_number"]].append(calculated)
        code_averages[source["blind_model_code"]].append(calculated)

    output_rows.sort(key=lambda row: row["blind_answer_id"])
    with OUTPUT.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=list(output_rows[0]))
        writer.writeheader()
        writer.writerows(output_rows)

    batch_means = {batch: mean(values) for batch, values in batch_averages.items()}
    max_batch_drift = max(batch_means.values()) - min(batch_means.values())

    lines = [
        "# Codex/GPT AI Second-Rater Summary",
        "",
        "**Date:** 2026-06-25",
        "**Rows:** 240",
        "**Model identities:** blinded",
        "",
        "## Validation",
        "",
        "- 240 unique blind answer IDs matched the rep-1 scoring source.",
        "- Every dimension is an integer from 0 to 5.",
        "- Every average was independently recalculated and matched.",
        "- No model identity key was read or merged.",
        "- The quarantined MiMo files were excluded.",
        "",
        "## Batch Calibration",
        "",
        "| Batch | Rows | Mean score |",
        "|---:|---:|---:|",
    ]
    for batch in sorted(batch_means):
        lines.append(f"| {batch} | {len(batch_averages[batch])} | {batch_means[batch]:.3f} |")

    lines.extend(
        [
            "",
            f"Maximum difference between batch means: **{max_batch_drift:.3f}**.",
            "",
            "## Blind-Code Results",
            "",
            "These remain anonymous until human scoring is complete.",
            "",
            "| Blind code | Answers | Mean AI score |",
            "|---|---:|---:|",
        ]
    )
    for code in sorted(code_averages):
        lines.append(f"| {code} | {len(code_averages[code])} | {mean(code_averages[code]):.3f} |")

    lines.extend(
        [
            "",
            "## Method Limitation",
            "",
            "Batch 01 was rescored from the original blind answers, but the current session had previously inspected quarantined MiMo ratings while diagnosing provider routing. Batches 02-08 had no prior external AI ratings.",
            "",
            "Human scoring remains the primary evaluation. Do not open the blind model key until the human scores are complete.",
        ]
    )
    SUMMARY.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"Wrote {OUTPUT}")
    print(f"Wrote {SUMMARY}")


if __name__ == "__main__":
    main()
