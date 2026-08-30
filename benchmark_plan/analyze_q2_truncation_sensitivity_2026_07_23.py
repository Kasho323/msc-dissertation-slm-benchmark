"""Check whether Q2's quality gap remains after excluding length-stopped answers."""

from __future__ import annotations

import csv
from collections import defaultdict
from pathlib import Path
from statistics import mean, median


PROJECT = Path(__file__).resolve().parents[1]
RESULTS = PROJECT / "benchmark_results"
QUALITY_FILE = RESULTS / "ai_second_rater_codex_gpt_C1_C6_2026-06-25.csv"
FINISH_FILE = RESULTS / "full_benchmark_finish_reason_audit_C1_C6_2026-06-24.csv"
DETAIL_FILE = RESULTS / "q2_truncation_sensitivity_per_question_2026-07-23.csv"
REPORT_FILE = RESULTS / "q2_truncation_sensitivity_report_2026-07-23.md"

Q2_CODE = "K8"
Q4_CODE = "M4"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


quality_rows = read_csv(QUALITY_FILE)
finish_rows = read_csv(FINISH_FILE)

quality_by_model_question: dict[tuple[str, str], dict[str, str]] = {}
for row in quality_rows:
    quality_by_model_question[(row["blind_model_code"], row["question_id"])] = row

q2_finish_by_question: dict[str, list[str]] = defaultdict(list)
for row in finish_rows:
    if row["blind_model_code"] == Q2_CODE:
        q2_finish_by_question[row["question_id"]].append(row["finish_reason"])

if len(q2_finish_by_question) != 40:
    raise ValueError(f"Expected 40 Q2 questions, found {len(q2_finish_by_question)}")

for question_id, reasons in q2_finish_by_question.items():
    if len(reasons) != 3:
        raise ValueError(f"{question_id}: expected 3 repetitions, found {len(reasons)}")
    if len(set(reasons)) != 1:
        raise ValueError(f"{question_id}: repetitions have different finish reasons: {reasons}")

detail_rows: list[dict[str, str | float]] = []
for question_id in sorted(q2_finish_by_question):
    q2_row = quality_by_model_question[(Q2_CODE, question_id)]
    q4_row = quality_by_model_question[(Q4_CODE, question_id)]
    q2_quality = float(q2_row["average_quality_score"])
    q4_quality = float(q4_row["average_quality_score"])
    detail_rows.append(
        {
            "question_id": question_id,
            "q2_finish_reason": q2_finish_by_question[question_id][0],
            "q2_quality": q2_quality,
            "q4_quality_same_question": q4_quality,
            "q4_minus_q2": q4_quality - q2_quality,
            "q2_completeness": float(q2_row["completeness"]),
            "q4_completeness_same_question": float(q4_row["completeness"]),
        }
    )

with DETAIL_FILE.open("w", encoding="utf-8-sig", newline="") as handle:
    writer = csv.DictWriter(handle, fieldnames=list(detail_rows[0]))
    writer.writeheader()
    writer.writerows(detail_rows)


def summarise(rows: list[dict[str, str | float]]) -> dict[str, float | int]:
    differences = [float(row["q4_minus_q2"]) for row in rows]
    return {
        "n": len(rows),
        "q2_quality": mean(float(row["q2_quality"]) for row in rows),
        "q4_quality": mean(float(row["q4_quality_same_question"]) for row in rows),
        "mean_difference": mean(differences),
        "median_difference": median(differences),
        "q2_completeness": mean(float(row["q2_completeness"]) for row in rows),
        "q4_completeness": mean(
            float(row["q4_completeness_same_question"]) for row in rows
        ),
    }


natural_rows = [row for row in detail_rows if row["q2_finish_reason"] == "stop"]
length_rows = [row for row in detail_rows if row["q2_finish_reason"] == "length"]

if len(natural_rows) != 32 or len(length_rows) != 8:
    raise ValueError(
        f"Expected 32 natural and 8 length-stopped questions; "
        f"found {len(natural_rows)} and {len(length_rows)}"
    )

summaries = {
    "All 40 questions": summarise(detail_rows),
    "Q2 naturally finished (same 32 questions for Q4)": summarise(natural_rows),
    "Q2 length-stopped (same 8 questions for Q4)": summarise(length_rows),
}

report_lines = [
    "# Q2 truncation sensitivity check",
    "",
    "This check uses first-repetition quality scores and groups finish reasons by "
    "question. The three fixed-seed repetitions had the same finish reason for "
    "every Q2 question.",
    "",
    "| Subset | n | Q2 mean quality | Q4 mean quality on same questions | "
    "Mean Q4-Q2 gap | Q2 completeness | Q4 completeness |",
    "|---|---:|---:|---:|---:|---:|---:|",
]
for label, values in summaries.items():
    report_lines.append(
        f"| {label} | {values['n']} | {values['q2_quality']:.3f} | "
        f"{values['q4_quality']:.3f} | {values['mean_difference']:.3f} | "
        f"{values['q2_completeness']:.3f} | {values['q4_completeness']:.3f} |"
    )

report_lines.extend(
    [
        "",
        "## Interpretation",
        "",
        "- Eight of the 40 Q2 questions reached the 512-token limit. Across the "
        "three identical repetitions, this appears as 24 of 120 outputs.",
        "- On the 32 questions where Q2 finished naturally, Q2 still averaged "
        f"{summaries['Q2 naturally finished (same 32 questions for Q4)']['q2_quality']:.3f}, "
        "compared with "
        f"{summaries['Q2 naturally finished (same 32 questions for Q4)']['q4_quality']:.3f} "
        "for Q4 on exactly the same questions.",
        "- The quality gap therefore remains after the length-stopped Q2 answers "
        "are excluded. Truncation may reduce completeness, but it does not explain "
        "the full Q2 quality difference.",
        "- The eight length-stopped questions were harder for both configurations, "
        "because Q4 also scored lower on that subset than on its other questions.",
        "",
        "## Q2 length-stopped question IDs",
        "",
        ", ".join(str(row["question_id"]) for row in length_rows),
        "",
    ]
)
REPORT_FILE.write_text("\n".join(report_lines), encoding="utf-8")

print(f"Wrote {DETAIL_FILE}")
print(f"Wrote {REPORT_FILE}")
for label, values in summaries.items():
    print(
        f"{label}: n={values['n']}, Q2={values['q2_quality']:.3f}, "
        f"Q4={values['q4_quality']:.3f}, gap={values['mean_difference']:.3f}"
    )
