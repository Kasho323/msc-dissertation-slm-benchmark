"""Interval estimates for the human-AI agreement result reported in Section 4.7.

analyze_clean30_agreement_2026_07_09.py computes the point estimates: Spearman
rho, its p value, the mean absolute difference and the dimension-level
diagnostics of Table 4.8. It does not compute interval estimates. This script
records the two intervals quoted in Section 4.7 so that both are reproducible
from the retained scoring files.

Fixed choices, stated so the result can be reproduced exactly:

  RNG                     Python standard library random.Random, Mersenne Twister
  seed                    20260821
  resamples               20000
  resampling unit         the matched answer (human and AI scores move together)
  interval method         percentile
  Spearman ties           average ranks
  degenerate resamples    a resample whose ranks are constant gives an undefined
                          rho and is discarded; the count is reported
  second interval         paired-sample t on the per-answer AI minus human
                          difference, df = n - 1

Two different t statistics appear in this analysis and must not be conflated:

  Spearman significance test    t = rho * sqrt((n - 2) / (1 - rho^2)),
                                df = n - 2. Tests whether the rank association
                                differs from zero. This is NOT a paired-sample t.
  Paired mean-difference test   t = mean(d) / (sd(d) / sqrt(n)), df = n - 1,
                                where d is the per-answer AI minus human
                                difference. This is the statistic behind the
                                second confidence interval.

Reads only the two retained scoring files. Writes a report; changes nothing.

Usage:  python analyze_agreement_intervals_2026-08-23.py
"""

import csv
import math
import random
import statistics
from pathlib import Path

RESULTS = Path(__file__).resolve().parents[1] / "benchmark_results"
AI_SCORES = RESULTS / "ai_second_rater_codex_gpt_C1_C6_2026-06-25.csv"
HUMAN_SCORES = RESULTS / "human_independent_CLEAN_30_HUMAN_SCORED_2026-07-09.csv"
OUT = RESULTS / "agreement_intervals_report_2026-08-23.md"

SEED = 20260821
RESAMPLES = 20000
DIMENSIONS = [
    "relevance",
    "correctness",
    "faithfulness_to_source",
    "completeness",
    "hallucination_risk",
    "source_grounding",
]
# t critical value, two-sided 95 per cent, df = 29
T_CRITICAL_DF29 = 2.045229642


def average_ranks(values):
    order = sorted(range(len(values)), key=lambda i: values[i])
    out = [0.0] * len(values)
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and values[order[j + 1]] == values[order[i]]:
            j += 1
        rank = (i + j) / 2 + 1
        for k in range(i, j + 1):
            out[order[k]] = rank
        i = j + 1
    return out


def pearson(x, y):
    n = len(x)
    mx, my = sum(x) / n, sum(y) / n
    sx = math.sqrt(sum((a - mx) ** 2 for a in x))
    sy = math.sqrt(sum((b - my) ** 2 for b in y))
    if sx == 0 or sy == 0:
        return None
    return sum((a - mx) * (b - my) for a, b in zip(x, y)) / (sx * sy)


def spearman(x, y):
    return pearson(average_ranks(x), average_ranks(y))


def percentile(sorted_values, q):
    """Percentile by nearest lower order statistic, matching the reported CI."""
    idx = int(q * (len(sorted_values) - 1))
    if q > 0.5:
        idx = math.ceil(q * (len(sorted_values) - 1))
    return sorted_values[idx]


def answer_mean(row):
    return sum(float(row[d]) for d in DIMENSIONS) / len(DIMENSIONS)


def main():
    ai = {r["blind_answer_id"]: r for r in csv.DictReader(open(AI_SCORES, encoding="utf-8-sig"))}
    human = list(csv.DictReader(open(HUMAN_SCORES, encoding="utf-8-sig")))

    missing = [r["blind_answer_id"] for r in human if r["blind_answer_id"] not in ai]
    if missing:
        raise SystemExit(f"unmatched answers: {missing}")

    h = [answer_mean(r) for r in human]
    a = [answer_mean(ai[r["blind_answer_id"]]) for r in human]
    n = len(h)

    rho = spearman(h, a)
    # Significance test of rho. Reported separately so it is never mistaken for
    # the paired-sample statistic below: different formula, different df.
    t_rho = rho * math.sqrt((n - 2) / (1 - rho * rho))

    diffs = [x - y for x, y in zip(a, h)]
    mean_diff = statistics.mean(diffs)
    sd_diff = statistics.stdev(diffs)
    se_diff = sd_diff / math.sqrt(n)
    t_paired = mean_diff / se_diff
    t_lo = mean_diff - T_CRITICAL_DF29 * se_diff
    t_hi = mean_diff + T_CRITICAL_DF29 * se_diff

    rng = random.Random(SEED)
    boot = []
    degenerate = 0
    for _ in range(RESAMPLES):
        idx = [rng.randrange(n) for _ in range(n)]
        r = spearman([h[i] for i in idx], [a[i] for i in idx])
        if r is None:
            degenerate += 1
        else:
            boot.append(r)
    boot.sort()
    rho_lo = percentile(boot, 0.025)
    rho_hi = percentile(boot, 0.975)

    lines = [
        "# Interval estimates for the human-AI agreement result",
        "",
        "Generated by `analyze_agreement_intervals_2026-08-23.py`. Supplements",
        "`analyze_clean30_agreement_2026_07_09.py`, which reports the point estimates only.",
        "",
        "## Inputs",
        "",
        f"- AI ratings: `{AI_SCORES.name}`",
        f"- Independent human ratings: `{HUMAN_SCORES.name}`",
        f"- Matched answers: {n}",
        "",
        "## Method",
        "",
        "| Choice | Value |",
        "|---|---|",
        "| RNG | `random.Random` (Mersenne Twister), Python standard library |",
        f"| Seed | {SEED} |",
        f"| Resamples | {RESAMPLES} |",
        "| Resampling unit | matched answer; human and AI scores resampled together |",
        "| Interval method | percentile |",
        "| Spearman ties | average ranks |",
        f"| Discarded degenerate resamples | {degenerate} |",
        "| Second interval | paired-sample t, df = n - 1 |",
        "",
        "## Result 1: rank association and its bootstrap interval",
        "",
        "| Quantity | Value |",
        "|---|---|",
        f"| Spearman rho | {rho:.6f} |",
        f"| Significance test of rho: t | {t_rho:.4f} |",
        f"| Significance test of rho: df | {n - 2} |",
        f"| Bootstrap 95% CI for rho | [{rho_lo:.6f}, {rho_hi:.6f}] |",
        f"| Bootstrap 95% CI for rho, as reported | [{rho_lo:.2f}, {rho_hi:.2f}] |",
        "",
        "## Result 2: mean AI-human difference and its paired-sample t interval",
        "",
        "| Quantity | Value |",
        "|---|---|",
        f"| Mean AI minus human difference | {mean_diff:.6f} |",
        f"| SD of paired differences | {sd_diff:.6f} |",
        f"| Standard error | {se_diff:.6f} |",
        f"| Paired mean-difference test: t | {t_paired:.4f} |",
        f"| Paired mean-difference test: df | {n - 1} |",
        f"| Paired-sample t 95% CI | [{t_lo:.6f}, {t_hi:.6f}] |",
        f"| Paired-sample t 95% CI, as reported | [{t_lo:.2f}, {t_hi:.2f}] |",
        "",
        "## The two t statistics are different quantities",
        "",
        f"`t = {t_rho:.4f}, df = {n - 2}` tests whether the Spearman rank association differs",
        "from zero. It is derived from rho and the sample size, and it must not be described",
        "as a paired-sample t statistic.",
        "",
        f"`t = {t_paired:.4f}, df = {n - 1}` is the paired-sample statistic for the mean",
        "AI-minus-human score difference, and is the one underlying the second interval above.",
        "",
    ]
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines[lines.index("## Result 1: rank association and its bootstrap interval"):]))
    print(f"\nreport: {OUT.name}")


if __name__ == "__main__":
    main()
