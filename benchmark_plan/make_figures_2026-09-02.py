# -*- coding: utf-8 -*-
"""Redraw Figures 3.1 and 4.1 in monochrome.

Both figures previously used blue and beige fills. A dissertation that will be
read and possibly printed in black and white reads better, and more formally,
without colour, so both are redrawn in greys. Nothing about the content
changes: the same boxes, labels, settings, data points and non-dominated sets
as before, taken from the same sections and tables.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

plt.rcParams["font.family"] = "Calibri"

OUT = (r"C:\Users\Crbd2\Desktop\Dissertation\dissertation_project\benchmark_results"
       r"\fig_%s_2026-09-02.png")

INK = "#000000"
LINE = "#444444"
EDGE = "#333333"
FILL_MAIN = "#F2F2F2"
FILL_EVAL = "#E0E0E0"
FILL_VAR = "#DCDCDC"

# ---------------------------------------------------------------- Figure 3.1
fig, ax = plt.subplots(figsize=(6.4, 7.8))
ax.set_xlim(0, 100); ax.set_ylim(2, 118); ax.axis("off")


def box(x, y, w, h, title, sub=None, fill=FILL_MAIN, edge=EDGE):
    ax.add_patch(FancyBboxPatch((x, y), w, h,
                                boxstyle="round,pad=0.35,rounding_size=1.2",
                                linewidth=0.9, edgecolor=edge, facecolor=fill))
    if sub:
        ax.text(x + w / 2, y + h * 0.63, title, ha="center", va="center",
                fontsize=8.8, color=INK)
        ax.text(x + w / 2, y + h * 0.27, sub, ha="center", va="center",
                fontsize=7.6, color=LINE, style="italic")
    else:
        ax.text(x + w / 2, y + h / 2, title, ha="center", va="center",
                fontsize=8.8, color=INK)


def arrow(x1, y1, x2, y2):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>",
                                 mutation_scale=11, linewidth=0.9,
                                 color=LINE, shrinkA=0, shrinkB=0))


CX, W, H = 12, 56, 8.6
STEPS = [
    (108, "Four public source documents", "D1\u2013D4"),
    (96,  "Loading and segmentation", "512-character chunks, 100-character overlap"),
    (84,  "Embedding and indexing", "all-MiniLM-L6-v2; in-memory ChromaDB"),
    (72,  "Retrieval", "k = 10"),
    (60,  "Reranking", "ms-marco-MiniLM-L6-v2; n = 3"),
    (48,  "Prompt assembly", "question and the three retained passages"),
    (36,  "Local generation", "llama.cpp server, CPU-only"),
    (24,  "Generated answer and source record", None),
]
for y, t, s in STEPS:
    box(CX, y, W, H, t, s)
for i in range(len(STEPS) - 1):
    arrow(CX + W / 2, STEPS[i][0], CX + W / 2, STEPS[i + 1][0] + H)

box(74, 36, 24, 8.6, "Configuration", "C1\u2013C6", fill=FILL_VAR)
arrow(74, 40.3, CX + W, 40.3)
box(4, 8, 44, 9.4, "Answer quality", "six-dimension 0\u20135 rubric", fill=FILL_EVAL)
box(54, 8, 44, 9.4, "System performance",
    "latency, throughput, memory, file size", fill=FILL_EVAL)
arrow(28, 24, 26, 17.4)
arrow(52, 24, 76, 17.4)

fig.savefig(OUT % "methodology_overview", dpi=400, bbox_inches="tight",
            facecolor="white", pad_inches=0.1)
plt.close(fig)
print("Figure 3.1 redrawn")

# ---------------------------------------------------------------- Figure 4.1
Q = {"C1": 3.071, "C2": 3.100, "C3": 3.575, "C4": 2.683, "C5": 3.433, "C6": 3.446}
TP = {"C1": 103.42, "C2": 76.07, "C3": 67.15, "C4": 82.74, "C5": 62.15, "C6": 42.82}
RSS = {"C1": 568.37, "C2": 1479.16, "C3": 1001.06, "C4": 906.26, "C5": 1793.69,
       "C6": 1829.38}
ND_TP = ["C1", "C2", "C3"]
ND_RSS = ["C1", "C3"]

GRID = "#D0D0D0"
ND_FILL = "#333333"
D_FILL = "#FFFFFF"
D_EDGE = "#777777"

fig, axes = plt.subplots(1, 2, figsize=(7.2, 3.5))
PANELS = [
    (axes[0], TP, ND_TP, "Throughput (tokens per second)",
     "(a) quality against throughput", False),
    (axes[1], RSS, ND_RSS, "Observed process RSS (MiB)",
     "(b) quality against memory", True),
]
for ax, cost, nd, xlabel, title, invert in PANELS:
    ax.set_axisbelow(True)
    ax.grid(True, linewidth=0.6, color=GRID)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color("#777777"); ax.spines[s].set_linewidth(0.8)
    pts = sorted(((cost[c], Q[c]) for c in nd))
    ax.plot([p[0] for p in pts], [p[1] for p in pts],
            linewidth=1.0, color=ND_FILL, alpha=0.45, zorder=1)
    for c in Q:
        on = c in nd
        ax.scatter(cost[c], Q[c], s=54, zorder=3,
                   facecolor=ND_FILL if on else D_FILL,
                   edgecolor=ND_FILL if on else D_EDGE, linewidth=1.1)
        off = (0, 9)
        if invert and c == "C5":
            off = (14, -4)
        elif invert and c == "C6":
            off = (-2, 10)
        ax.annotate(c, (cost[c], Q[c]), textcoords="offset points",
                    xytext=off, ha="center", fontsize=8.4, color=INK)
    ax.set_xlabel(xlabel, fontsize=8.6, color=INK)
    ax.set_title(title, fontsize=9.0, color=INK, pad=8)
    ax.tick_params(labelsize=8.0, colors="#333333", length=3)
    if invert:
        ax.invert_xaxis()
    lo, hi = min(Q.values()), max(Q.values())
    ax.set_ylim(lo - 0.16, hi + 0.20)

axes[0].set_ylabel("Overall answer quality (0\u20135)", fontsize=8.6, color=INK)
axes[1].tick_params(labelleft=False)
axes[0].scatter([], [], s=54, facecolor=ND_FILL, edgecolor=ND_FILL, label="non-dominated")
axes[0].scatter([], [], s=54, facecolor=D_FILL, edgecolor=D_EDGE, label="dominated")
axes[0].legend(loc="lower left", fontsize=7.8, frameon=False, handletextpad=0.4)
fig.tight_layout()
fig.savefig(OUT % "quality_cost_tradeoff", dpi=400, bbox_inches="tight",
            facecolor="white", pad_inches=0.08)
plt.close(fig)
print("Figure 4.1 redrawn")
