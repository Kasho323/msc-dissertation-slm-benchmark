"""
Stage 1 analysis (2026-06-30):
1. Validate the human-scored Stage 1 file (60 rows, all dimensions filled).
2. Describe the human score distribution (scale usage).
3. Compute human vs AI second-rater agreement on the same 60 answers:
   - Spearman rho on the average quality score
   - Spearman rho + quadratic-weighted kappa per dimension
   - mean absolute difference; largest disagreements listed
The blind model key is NOT read. Blind codes only.
"""

import csv
from pathlib import Path
from collections import Counter, defaultdict

from scipy.stats import spearmanr
from sklearn.metrics import cohen_kappa_score

BASE = Path(__file__).resolve().parent.parent / "benchmark_results"
HUMAN = Path(r"C:\Users\Crbd2\Downloads\human_stage1_independent_60_2026-06-29_HUMAN_SCORED.csv")
HUMAN_ARCHIVE = BASE / "human_stage1_independent_60_HUMAN_SCORED_archived.csv"
AI = BASE / "ai_second_rater_codex_gpt_C1_C6_2026-06-25.csv"
OUT = BASE / "stage1_agreement_report_2026-06-30.md"

DIMS = ["relevance", "correctness", "faithfulness_to_source",
        "completeness", "hallucination_risk", "source_grounding"]

def read_rows(path):
    with open(path, newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))

human = read_rows(HUMAN)
ai = {r["blind_answer_id"]: r for r in read_rows(AI)}

report = ["# Stage 1 Human Scoring - Validation and Human-AI Agreement",
          "", f"Generated: 2026-06-30. Human file: {HUMAN.name}", ""]

# ---------- 1. validation ----------
problems = []
if len(human) != 60:
    problems.append(f"Expected 60 rows, found {len(human)}")
for r in human:
    for d in DIMS:
        v = r.get(d, "")
        if v == "" or v is None:
            problems.append(f"{r['blind_answer_id']}: missing {d}")
        else:
            try:
                x = float(v)
                if not (0 <= x <= 5):
                    problems.append(f"{r['blind_answer_id']}: {d}={v} out of range")
            except ValueError:
                problems.append(f"{r['blind_answer_id']}: {d}='{v}' not numeric")
    if r["blind_answer_id"] not in ai:
        problems.append(f"{r['blind_answer_id']}: no matching AI rating")
    # average check
    try:
        vals = [float(r[d]) for d in DIMS]
        avg = sum(vals) / 6
        stated = float(r.get("average_quality_score") or 0)
        if abs(avg - stated) > 0.01:
            problems.append(f"{r['blind_answer_id']}: average mismatch (stated {stated}, computed {avg:.2f})")
    except ValueError:
        pass

low_no_note = [r["blind_answer_id"] for r in human
               if any(r.get(d) not in ("", None) and float(r[d]) <= 2 for d in DIMS)
               and not (r.get("scoring_notes") or "").strip()]

report.append("## 1. Validation / 文件校验")
report.append("")
if problems:
    report.append(f"**{len(problems)} problem(s) found:**")
    report += [f"- {p}" for p in problems[:30]]
else:
    report.append("- All 60 rows complete; every dimension 0-5; averages correct; all rows matched to AI ratings. PASS.")
if low_no_note:
    report.append(f"- Note: {len(low_no_note)} rows contain a score <=2 but have no scoring note: {', '.join(low_no_note[:10])}")
report.append("")

# ---------- 2. distribution ----------
report.append("## 2. Human score distribution / 打分分布")
report.append("")
allvals = Counter()
for r in human:
    for d in DIMS:
        allvals[int(float(r[d]))] += 1
total = sum(allvals.values())
report.append("| Score | Count | % |")
report.append("|---|---:|---:|")
for s in range(6):
    c = allvals.get(s, 0)
    report.append(f"| {s} | {c} | {100*c/total:.1f}% |")
report.append("")

hmeans = defaultdict(list)
for r in human:
    hmeans[r["blind_model_code"]].append(sum(float(r[d]) for d in DIMS) / 6)
report.append("| Blind code | n | Human mean | AI mean (from earlier report) |")
report.append("|---|---:|---:|---:|")
ai_means = {"A7": 3.575, "F3": 3.071, "K8": 2.683, "M4": 3.433, "R9": 3.446, "T2": 3.100}
for code in sorted(hmeans):
    hm = sum(hmeans[code]) / len(hmeans[code])
    report.append(f"| {code} | {len(hmeans[code])} | {hm:.3f} | {ai_means.get(code,'-')} |")
report.append("")
report.append("(AI means are over all 40 questions; human means are over the 10 Stage-1 questions, so levels are not directly comparable - ranking direction is the thing to watch.)")
report.append("")

# ---------- 3. agreement ----------
report.append("## 3. Human vs AI agreement on the same 60 answers / 人机一致性")
report.append("")
h_avg, a_avg = [], []
h_dim = {d: [] for d in DIMS}
a_dim = {d: [] for d in DIMS}
diffs = []
for r in human:
    arow = ai[r["blind_answer_id"]]
    hv = sum(float(r[d]) for d in DIMS) / 6
    av = sum(float(arow[d]) for d in DIMS) / 6
    h_avg.append(hv); a_avg.append(av)
    diffs.append((abs(hv - av), r["blind_answer_id"], hv, av, r["question_id"]))
    for d in DIMS:
        h_dim[d].append(int(float(r[d])))
        a_dim[d].append(int(float(arow[d])))

rho, p = spearmanr(h_avg, a_avg)
mad = sum(d[0] for d in diffs) / len(diffs)
report.append(f"- **Overall average score: Spearman rho = {rho:.3f}** (p = {p:.2g}), n = 60")
report.append(f"- Mean absolute difference between human and AI averages: {mad:.2f} points (0-5 scale)")
report.append("")
report.append("| Dimension | Spearman rho | Weighted kappa (quadratic) | Exact match % | Within +/-1 % |")
report.append("|---|---:|---:|---:|---:|")
for d in DIMS:
    hr, ar = h_dim[d], a_dim[d]
    try:
        dr, _ = spearmanr(hr, ar)
    except Exception:
        dr = float("nan")
    try:
        kap = cohen_kappa_score(hr, ar, weights="quadratic")
    except Exception:
        kap = float("nan")
    exact = sum(1 for x, y in zip(hr, ar) if x == y) / len(hr) * 100
    within1 = sum(1 for x, y in zip(hr, ar) if abs(x - y) <= 1) / len(hr) * 100
    report.append(f"| {d} | {dr:.3f} | {kap:.3f} | {exact:.0f}% | {within1:.0f}% |")
report.append("")

diffs.sort(reverse=True)
report.append("### Largest disagreements (top 8) / 分歧最大的答案")
report.append("")
report.append("| Blind ID | Question | Human avg | AI avg | |diff| |")
report.append("|---|---|---:|---:|---:|")
for dd, bid, hv, av, qid in diffs[:8]:
    report.append(f"| {bid} | {qid} | {hv:.2f} | {av:.2f} | {dd:.2f} |")
report.append("")
report.append("## Interpretation guide / 解读参考")
report.append("")
report.append("- Spearman rho: >0.7 strong, 0.5-0.7 moderate, <0.5 weak rank agreement.")
report.append("- Weighted kappa: >0.6 substantial, 0.4-0.6 moderate, <0.4 fair/poor.")
report.append("- If a dimension shows weak agreement, review that dimension manually in Stage 2 rather than trusting AI drafts for it.")

OUT.write_text("\n".join(report), encoding="utf-8")

# archive a copy of the human file next to the results
HUMAN_ARCHIVE.write_bytes(HUMAN.read_bytes())

print("PROBLEMS:", len(problems))
print("Overall Spearman rho:", round(rho, 3), "p:", p)
print("MAD:", round(mad, 3))
print("Report:", OUT.name)
