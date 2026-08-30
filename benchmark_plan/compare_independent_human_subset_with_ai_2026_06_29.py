from __future__ import annotations

import argparse
import csv
import math
from collections import defaultdict
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


def is_scored(row: dict[str, str]) -> bool:
    return all(row.get(dimension, "").strip() != "" for dimension in DIMENSIONS)


def score(row: dict[str, str], dimension: str) -> float:
    value = row.get(dimension, "").strip()
    if value == "":
        raise ValueError(f"{row.get('blind_answer_id')} has no {dimension} score")
    parsed = float(value)
    if parsed < 0 or parsed > 5:
        raise ValueError(
            f"{row.get('blind_answer_id')} has invalid {dimension} score: {value}"
        )
    return parsed


def average_score(row: dict[str, str]) -> float:
    return mean(score(row, dimension) for dimension in DIMENSIONS)


def ranks(values: list[float]) -> list[float]:
    indexed = sorted(enumerate(values), key=lambda item: item[1])
    result = [0.0] * len(values)
    i = 0
    while i < len(indexed):
        j = i
        while j + 1 < len(indexed) and indexed[j + 1][1] == indexed[i][1]:
            j += 1
        avg_rank = (i + j + 2) / 2
        for k in range(i, j + 1):
            result[indexed[k][0]] = avg_rank
        i = j + 1
    return result


def pearson(xs: list[float], ys: list[float]) -> float | None:
    if len(xs) < 2:
        return None
    x_mean = mean(xs)
    y_mean = mean(ys)
    num = sum((x - x_mean) * (y - y_mean) for x, y in zip(xs, ys))
    den_x = math.sqrt(sum((x - x_mean) ** 2 for x in xs))
    den_y = math.sqrt(sum((y - y_mean) ** 2 for y in ys))
    if den_x == 0 or den_y == 0:
        return None
    return num / (den_x * den_y)


def spearman(xs: list[float], ys: list[float]) -> float | None:
    return pearson(ranks(xs), ranks(ys))


def quadratic_weighted_kappa(human: list[int], ai: list[int]) -> float | None:
    if len(human) != len(ai) or not human:
        return None

    n_categories = 6
    observed = [[0 for _ in range(n_categories)] for _ in range(n_categories)]
    human_counts = [0 for _ in range(n_categories)]
    ai_counts = [0 for _ in range(n_categories)]

    for h, a in zip(human, ai):
        observed[h][a] += 1
        human_counts[h] += 1
        ai_counts[a] += 1

    n = len(human)
    observed_weighted = 0.0
    expected_weighted = 0.0
    max_distance = (n_categories - 1) ** 2

    for i in range(n_categories):
        for j in range(n_categories):
            weight = ((i - j) ** 2) / max_distance
            observed_weighted += weight * observed[i][j] / n
            expected = (human_counts[i] * ai_counts[j]) / n
            expected_weighted += weight * expected / n

    if expected_weighted == 0:
        return None
    return 1 - (observed_weighted / expected_weighted)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("human_subset_csv", type=Path)
    args = parser.parse_args()

    human_rows = [row for row in read_csv(args.human_subset_csv) if is_scored(row)]
    ai_rows = read_csv(AI_FILE)

    human_by_id = {row["blind_answer_id"]: row for row in human_rows}
    ai_by_id = {row["blind_answer_id"]: row for row in ai_rows}

    missing_ai = sorted(set(human_by_id) - set(ai_by_id))
    if missing_ai:
        raise ValueError(f"AI CSV is missing {len(missing_ai)} answer IDs")

    comparison_rows: list[dict[str, object]] = []
    by_dimension_abs_diff: dict[str, list[float]] = defaultdict(list)

    for answer_id in sorted(human_by_id):
        human = human_by_id[answer_id]
        ai = ai_by_id[answer_id]
        row: dict[str, object] = {
            "blind_answer_id": answer_id,
            "blind_model_code": human["blind_model_code"],
            "question_id": human["question_id"],
        }
        human_scores = []
        ai_scores = []
        for dimension in DIMENSIONS:
            h = score(human, dimension)
            a = score(ai, dimension)
            row[f"human_{dimension}"] = h
            row[f"ai_{dimension}"] = a
            row[f"difference_{dimension}"] = h - a
            human_scores.append(h)
            ai_scores.append(a)
            by_dimension_abs_diff[dimension].append(abs(h - a))

        human_avg = mean(human_scores)
        ai_avg = mean(ai_scores)
        row["human_average"] = round(human_avg, 3)
        row["ai_average"] = round(ai_avg, 3)
        row["average_difference"] = round(human_avg - ai_avg, 3)
        row["absolute_average_difference"] = round(abs(human_avg - ai_avg), 3)
        row["requires_review"] = abs(human_avg - ai_avg) >= 1.0
        comparison_rows.append(row)

    if not comparison_rows:
        raise ValueError("No fully scored human rows were found.")

    suffix = "independent_subset_2026-06-29"
    comparison_path = RESULTS / f"human_vs_codex_ai_comparison_{suffix}.csv"
    with comparison_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=list(comparison_rows[0]))
        writer.writeheader()
        writer.writerows(comparison_rows)

    disagreement_rows = [row for row in comparison_rows if row["requires_review"]]
    disagreement_path = RESULTS / f"human_vs_codex_ai_disagreement_review_{suffix}.csv"
    with disagreement_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=list(comparison_rows[0]))
        writer.writeheader()
        writer.writerows(disagreement_rows)

    human_averages = [float(row["human_average"]) for row in comparison_rows]
    ai_averages = [float(row["ai_average"]) for row in comparison_rows]
    avg_spearman = spearman(human_averages, ai_averages)

    summary_lines = [
        "# Independent Human Subset vs Codex/GPT AI Rating Summary",
        "",
        f"- Human subset rows compared: {len(comparison_rows)}",
        f"- Questions represented: {len(set(row['question_id'] for row in comparison_rows))}",
        f"- Rows requiring review (mean difference >= 1.0): {len(disagreement_rows)}",
        f"- Average-score Spearman correlation: {avg_spearman:.3f}" if avg_spearman is not None else "- Average-score Spearman correlation: not defined",
        "",
        "| Dimension | Mean absolute difference | Spearman | Quadratic weighted kappa |",
        "|---|---:|---:|---:|",
    ]

    for dimension in DIMENSIONS:
        human_dimension = [int(score(row, dimension)) for row in human_rows]
        ai_dimension = [int(score(ai_by_id[row["blind_answer_id"]], dimension)) for row in human_rows]
        dim_spearman = spearman(
            [float(value) for value in human_dimension],
            [float(value) for value in ai_dimension],
        )
        dim_kappa = quadratic_weighted_kappa(human_dimension, ai_dimension)
        summary_lines.append(
            "| {dimension} | {mad:.3f} | {rho} | {kappa} |".format(
                dimension=dimension,
                mad=mean(by_dimension_abs_diff[dimension]),
                rho=f"{dim_spearman:.3f}" if dim_spearman is not None else "n/a",
                kappa=f"{dim_kappa:.3f}" if dim_kappa is not None else "n/a",
            )
        )

    summary_lines.extend(
        [
            "",
            "## Method Note",
            "",
            "This comparison should be used only for the independently scored human subset. It is suitable for checking human-AI agreement because the human scorer should complete these rows without seeing the AI draft scores.",
            "",
            "The remaining rows may still be handled as AI-assisted draft scoring with human review, but they should not be used as independent evidence of human-AI agreement if the human reviewer saw the AI-prefilled scores.",
        ]
    )

    summary_path = RESULTS / f"human_vs_codex_ai_summary_{suffix}.md"
    summary_path.write_text("\n".join(summary_lines) + "\n", encoding="utf-8")

    print(f"Wrote {comparison_path}")
    print(f"Wrote {disagreement_path}")
    print(f"Wrote {summary_path}")


if __name__ == "__main__":
    main()
