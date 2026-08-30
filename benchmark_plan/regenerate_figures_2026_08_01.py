# -*- coding: utf-8 -*-
"""Regenerate the two quality-vs-cost scatter figures with corrected labels.

Fixes three presentation defects in the 2026-07-09 figures (data unchanged):
  1. Point labels dropped the model family name, because the original code used
     CFG_LABEL[c].split(' ', 1)[1] -- e.g. "Gemma 3 1B Q4_K_M" rendered as
     "3 1B Q4_K_M" and "Llama 3.2 1B Q4_K_M" as "3.2 1B Q4_K_M".
  2. The topmost label (C3) collided with the chart title.
  3. The memory axis was labelled MB while the dissertation reports MiB
     (the harness divides by 1024**2).

Reads the same source CSVs as build_final_results_2026_07_09.py and recomputes
the plotted values from them; it does not read or alter any table output.
Writes NEW dated filenames so the 2026-07-09 figures remain as evidence.
"""
import csv
from pathlib import Path
from statistics import mean
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

BASE = Path(__file__).resolve().parent.parent / "benchmark_results"
AI  = BASE / "ai_second_rater_codex_gpt_C1_C6_2026-06-25.csv"
KEY = BASE / "full_benchmark_blind_model_key_C1_C6_2026-06-24.csv"
SYS = BASE / "full_benchmark_system_summary_C1_C6_2026-06-24.csv"

DIMS = ["relevance", "correctness", "faithfulness_to_source",
        "completeness", "hallucination_risk", "source_grounding"]
ORDER = ["C1", "C2", "C3", "C4", "C5", "C6"]
CFG_LABEL = {
    "C1": "Qwen2.5 0.5B Q4_K_M", "C2": "Llama 3.2 1B Q4_K_M",
    "C3": "Gemma 3 1B Q4_K_M",   "C4": "Qwen2.5 1.5B Q2_K",
    "C5": "Qwen2.5 1.5B Q4_K_M", "C6": "Qwen2.5 1.5B Q8_0"}

# Per-point label placement: (dx, dy in points, horizontal alignment).
# Tuned so no label overlaps a marker, the title, another label, or the axes
# edge. Presentation only -- no effect on the plotted data.
OFFSETS = {
    "speed":  {"C1": (-10, -16, "right"), "C2": (9, 6, "left"),
               "C3": (9, 0, "left"),      "C4": (9, 6, "left"),
               "C5": (9, 6, "left"),      "C6": (9, 6, "left")},
    # C5 and C6 sit almost on top of each other (their observed RSS differs by
    # only 35.69 MiB), so their labels are stacked above and below the markers.
    "memory": {"C1": (-10, -16, "right"), "C2": (9, 6, "left"),
               "C3": (9, 0, "left"),      "C4": (9, 6, "left"),
               "C5": (0, -22, "center"),  "C6": (0, 13, "center")},
}

def rd(p):
    with open(p, newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))

code2cfg = {r["blind_model_code"]: r["model_config_id"] for r in rd(KEY)}
sysrows = {r["model_config_id"]: r for r in rd(SYS)}
overall = {c: [] for c in ORDER}
for r in rd(AI):
    cfg = code2cfg[r["blind_model_code"]]
    overall[cfg].append(sum(float(r[d]) for d in DIMS) / len(DIMS))

def scatter(xkey, xlabel, title, fname, which, invert=False):
    fig, ax = plt.subplots(figsize=(7.6, 5.2))
    xs, ys = [], []
    for c in ORDER:
        x = float(sysrows[c][xkey]); y = mean(overall[c])
        xs.append(x); ys.append(y)
        ax.scatter(x, y, s=90, zorder=3)
        dx, dy, ha = OFFSETS[which][c]
        ax.annotate(f"{c}  {CFG_LABEL[c]}", (x, y), textcoords="offset points",
                    xytext=(dx, dy), fontsize=8, zorder=4, ha=ha)
    # headroom so the highest label cannot reach the title
    ymin, ymax = min(ys), max(ys)
    pad = (ymax - ymin) * 0.22
    ax.set_ylim(ymin - pad, ymax + pad)
    xmin, xmax = min(xs), max(xs)
    xpad = (xmax - xmin) * 0.16
    ax.set_xlim(xmin - xpad, xmax + xpad)
    ax.set_xlabel(xlabel); ax.set_ylabel("Overall answer quality (0-5)")
    ax.set_title(title); ax.grid(True, alpha=.3)
    if invert:
        ax.invert_xaxis()
    fig.tight_layout()
    fig.savefig(BASE / fname, dpi=150)
    plt.close(fig)
    print("wrote", fname)
    for c in ORDER:
        print(f"   {c} {CFG_LABEL[c]:22s} x={float(sysrows[c][xkey]):9.2f} "
              f"y={mean(overall[c]):.3f}")

scatter("mean_tokens_per_second", "Throughput (tokens/s)",
        "Quality vs throughput", "fig_quality_vs_speed_2026-08-01.png", "speed")
scatter("mean_observed_rss_mb", "Observed process RSS (MiB)",
        "Quality vs observed process RSS", "fig_quality_vs_memory_2026-08-01.png",
        "memory", invert=True)
