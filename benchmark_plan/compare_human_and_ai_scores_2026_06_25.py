from __future__ import annotations

import argparse
import csv
from pathlib import Path
from statistics import mean


ROOT = Path(__file__).resolve().parents[2]
AI_FILE = (
    ROOT
    / "dissertation_project"
    / "benchmark_results"
    / "ai_second_rater_codex_gpt_C1_C6_2026-06-25.csv"
)
RESULTS = ROOT / "dissertation_project" / "benchmark_results"
DIMENSIONS = [
    "relevance",
    "correctness",
    "faithfulness_to_source",
    "completeness",
    "hallucination_risk",
    "source_grounding",
]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as file:
        return list(csv.DictReader(file))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("human_csv", type=Path)
    args = parser.parse_args()

    human_rows = read_csv(args.human_csv)
    ai_rows = read_csv(AI_FILE)
    human_by_id = {row["blind_answer_id"]: row for row in human_rows}
    ai_by_id = {row["blind_answer_id"]: row for row in ai_rows}

    missing = sorted(set(ai_by_id) - set(human_by_id))
    if missing:
        raise ValueError(f"Human CSV is missing {len(missing)} answer IDs.")

    comparison_rows = []
    dimension_differences: dict[str, list[float]] = {
        dimension: [] for dimension in DIMENSIONS
    }

    for answer_id in sorted(ai_by_id):
        human = human_by_id[answer_id]
        ai = ai_by_id[answer_id]
        row = {
            "blind_answer_id": answer_id,
            "blind_model_code": ai["blind_model_code"],
            "question_id": ai["question_id"],
        }
        human_scores = []
        ai_scores = []
        for dimension in DIMENSIONS:
            if human.get(dimension, "") == "":
                raise ValueError(f"{answer_id} has no human {dimension} score.")
            human_score = float(human[dimension])
            ai_score = float(ai[dimension])
            difference = human_score - ai_score
            row[f"human_{dimension}"] = human_score
            row[f"ai_{dimension}"] = ai_score
            row[f"difference_{dimension}"] = difference
            human_scores.append(human_score)
            ai_scores.append(ai_score)
            dimension_differences[dimension].append(abs(difference))

        human_average = mean(human_scores)
        ai_average = mean(ai_scores)
        row["human_average"] = round(human_average, 3)
        row["ai_average"] = round(ai_average, 3)
        row["average_difference"] = round(human_average - ai_average, 3)
        row["absolute_average_difference"] = round(
            abs(human_average - ai_average), 3
        )
        row["requires_review"] = abs(human_average - ai_average) >= 1.0
        comparison_rows.append(row)

    comparison_path = RESULTS / "human_vs_codex_ai_comparison_2026-06-25.csv"
    with comparison_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=list(comparison_rows[0]))
        writer.writeheader()
        writer.writerows(comparison_rows)

    review_rows = [
        row for row in comparison_rows if row["requires_review"]
    ]
    review_path = RESULTS / "human_vs_codex_ai_disagreement_review_2026-06-25.csv"
    with review_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=list(comparison_rows[0]))
        writer.writeheader()
        writer.writerows(review_rows)

    summary_path = RESULTS / "human_vs_codex_ai_summary_2026-06-25.md"
    lines = [
        "# Human vs Codex/GPT Rating Summary",
        "",
        f"- Answers compared: {len(comparison_rows)}",
        f"- Answers requiring review (mean difference >= 1.0): {len(review_rows)}",
        "",
        "| Dimension | Mean absolute difference |",
        "|---|---:|",
    ]
    for dimension in DIMENSIONS:
        lines.append(
            f"| {dimension} | {mean(dimension_differences[dimension]):.3f} |"
        )
    summary_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"Wrote {comparison_path}")
    print(f"Wrote {review_path}")
    print(f"Wrote {summary_path}")


if __name__ == "__main__":
    main()
