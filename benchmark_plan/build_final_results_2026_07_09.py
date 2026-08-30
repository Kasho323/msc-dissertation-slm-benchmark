"""
Build final Results tables + figure (2026-07-09).
Design A: AI second-rater = primary quality score for all 240 answers,
validated by the 30-answer independent human subset (Spearman rho = 0.80).

Outputs (in benchmark_results/):
- final_results_tables_2026-07-09.md   (T1 quality, T2 system, T3 quantisation, per-question-type)
- final_quality_by_config_2026-07-09.csv
- fig_quality_vs_speed_2026-07-09.png
- fig_quality_vs_memory_2026-07-09.png
"""
import csv
from pathlib import Path
from collections import defaultdict
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

BASE = Path(__file__).resolve().parent.parent / "benchmark_results"
AI = BASE / "ai_second_rater_codex_gpt_C1_C6_2026-06-25.csv"
KEY = BASE / "full_benchmark_blind_model_key_C1_C6_2026-06-24.csv"
SYS = BASE / "full_benchmark_system_summary_C1_C6_2026-06-24.csv"
OUT_MD = BASE / "final_results_tables_2026-07-09.md"
OUT_CSV = BASE / "final_quality_by_config_2026-07-09.csv"

DIMS = ["relevance","correctness","faithfulness_to_source",
        "completeness","hallucination_risk","source_grounding"]

def rd(p):
    with open(p, newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))

code2cfg = {r["blind_model_code"]: r["model_config_id"] for r in rd(KEY)}
ai = rd(AI)
sysrows = {r["model_config_id"]: r for r in rd(SYS)}

CFG_LABEL = {
    "C1":"Qwen2.5 0.5B Q4_K_M","C2":"Llama 3.2 1B Q4_K_M","C3":"Gemma 3 1B Q4_K_M",
    "C4":"Qwen2.5 1.5B Q2_K","C5":"Qwen2.5 1.5B Q4_K_M","C6":"Qwen2.5 1.5B Q8_0"}
ORDER = ["C1","C2","C3","C4","C5","C6"]

# ---- aggregate quality per config (all 240) ----
qual = defaultdict(lambda: defaultdict(list))   # cfg -> dim -> [scores]
overall = defaultdict(list)
bytype = defaultdict(lambda: defaultdict(list))  # cfg -> qtype -> [avg]
n_by_cfg = defaultdict(int)
for r in ai:
    cfg = code2cfg[r["blind_model_code"]]
    n_by_cfg[cfg] += 1
    for d in DIMS:
        qual[cfg][d].append(float(r[d]))
    ov = sum(float(r[d]) for d in DIMS)/6
    overall[cfg].append(ov)
    bytype[cfg][r["question_type"]].append(ov)

def mean(xs): return sum(xs)/len(xs) if xs else float("nan")

# ---- write CSV ----
with open(OUT_CSV,"w",newline="",encoding="utf-8-sig") as f:
    w = csv.writer(f)
    w.writerow(["config","model","n_answers",*DIMS,"overall_quality"])
    for c in ORDER:
        w.writerow([c, CFG_LABEL[c], n_by_cfg[c],
                    *[f"{mean(qual[c][d]):.2f}" for d in DIMS],
                    f"{mean(overall[c]):.2f}"])

# ---- markdown ----
L = ["# Final Results (2026-07-09)","",
     "Quality = AI second-rater (LLM-as-judge) over all 240 answers (rep 1 x 6 configs x 40 questions).",
     "Validated on a 30-answer independent human subset: Spearman rho = 0.80, human systematically stricter.",
     "System metrics from the final max_tokens=512 run, seed 42, same laptop, Balanced power plan.",""]

# T1 quality
L += ["## Table T1 - Answer quality by configuration (0-5)","",
      "| Config | Model | Relevance | Correct. | Faithful. | Complete. | Halluc.(hi=good) | Grounding | Overall |",
      "|---|---|---:|---:|---:|---:|---:|---:|---:|"]
for c in ORDER:
    L.append("| {} | {} | {:.2f} | {:.2f} | {:.2f} | {:.2f} | {:.2f} | {:.2f} | **{:.2f}** |".format(
        c, CFG_LABEL[c], *[mean(qual[c][d]) for d in DIMS], mean(overall[c])))
L.append("")

# T2 system
L += ["## Table T2 - System metrics by configuration","",
      "| Config | Model | Size (MB) | Mean latency (s) | P95 latency (s) | Tokens/s | Mean RSS (MB) | Truncated (of 120) |",
      "|---|---|---:|---:|---:|---:|---:|---:|"]
for c in ORDER:
    s = sysrows[c]
    L.append("| {} | {} | {} | {} | {} | {} | {} | {} |".format(
        c, CFG_LABEL[c], s["model_file_size_mb"], s["mean_latency_seconds"],
        s["p95_latency_seconds"], s["mean_tokens_per_second"], s["mean_observed_rss_mb"], s["finish_length"]))
L.append("")

# T3 quantisation ladder (C4/C5/C6 same model)
L += ["## Table T3 - Quantisation sensitivity, Qwen2.5 1.5B (same model, only precision changes)","",
      "| Quant | Overall quality | Size (MB) | Mean latency (s) | Tokens/s | Mean RSS (MB) | Truncated |",
      "|---|---:|---:|---:|---:|---:|---:|"]
for c,q in [("C4","Q2_K"),("C5","Q4_K_M"),("C6","Q8_0")]:
    s = sysrows[c]
    L.append("| {} | {:.2f} | {} | {} | {} | {} | {} |".format(
        q, mean(overall[c]), s["model_file_size_mb"], s["mean_latency_seconds"],
        s["mean_tokens_per_second"], s["mean_observed_rss_mb"], s["finish_length"]))
L.append("")

# per question type overall quality
qtypes = sorted({t for c in ORDER for t in bytype[c]})
L += ["## Table T4 - Overall quality by question type","",
      "| Config | " + " | ".join(qtypes) + " |",
      "|---|" + "---:|"*len(qtypes)]
for c in ORDER:
    L.append("| {} | ".format(c) + " | ".join(f"{mean(bytype[c][t]):.2f}" if bytype[c][t] else "-" for t in qtypes) + " |")
L.append("")

L += ["## Notes for writing","",
      "- Quality is AI-rated; treat as indicative and cite the human-validation rho=0.80.",
      "- Memory is observed llama-server RSS, not profiler peak.",
      "- Q2_K shows the most truncation (24/120) and lowest quality - a clear over-compression finding.",
      "- Conditional recommendation style: 'If priority is X, choose Y.'"]
OUT_MD.write_text("\n".join(L), encoding="utf-8")

# ---- figures ----
def scatter(xkey, xlabel, fname, invert=False):
    fig, ax = plt.subplots(figsize=(7,5))
    for c in ORDER:
        x = float(sysrows[c][xkey]); y = mean(overall[c])
        ax.scatter(x, y, s=90)
        ax.annotate(f"{c}\n{CFG_LABEL[c].split(' ',1)[1] if ' ' in CFG_LABEL[c] else c}",
                    (x,y), textcoords="offset points", xytext=(8,4), fontsize=8)
    ax.set_xlabel(xlabel); ax.set_ylabel("Overall answer quality (0-5)")
    ax.set_title("Quality vs "+xlabel); ax.grid(True, alpha=.3)
    if invert: ax.invert_xaxis()
    fig.tight_layout(); fig.savefig(BASE/fname, dpi=150); plt.close(fig)

scatter("mean_tokens_per_second","Throughput (tokens/s)","fig_quality_vs_speed_2026-07-09.png")
scatter("mean_observed_rss_mb","Memory RSS (MB)","fig_quality_vs_memory_2026-07-09.png", invert=True)

print("Quality (overall) by config:")
for c in ORDER: print(f"  {c} {CFG_LABEL[c]:26s} {mean(overall[c]):.2f}  (n={n_by_cfg[c]})")
print("Wrote:", OUT_MD.name, OUT_CSV.name, "+ 2 figures")
