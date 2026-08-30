"""
Analyse the CLEAN 30 independent human scoring (2026-07-09).
Validate completeness, describe distribution, and compute genuine human-vs-AI
agreement (these human scores were produced with NO AI scores visible).
Blind model key is NOT read.
"""
import csv
from pathlib import Path
from collections import Counter, defaultdict
from scipy.stats import spearmanr
from sklearn.metrics import cohen_kappa_score

BASE = Path(__file__).resolve().parent.parent / "benchmark_results"
HUMAN = Path(r"C:\Users\Crbd2\Downloads\human_independent_CLEAN_30_2026-07-07_HUMAN_SCORED.csv")
HUMAN_ARCHIVE = BASE / "human_independent_CLEAN_30_HUMAN_SCORED_2026-07-09.csv"
AI = BASE / "ai_second_rater_codex_gpt_C1_C6_2026-06-25.csv"
OUT = BASE / "clean30_agreement_report_2026-07-09.md"

DIMS = ["relevance","correctness","faithfulness_to_source",
        "completeness","hallucination_risk","source_grounding"]

def rd(p):
    with open(p, newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))

human = rd(HUMAN)
ai = {r["blind_answer_id"]: r for r in rd(AI)}

rep = ["# CLEAN 30 Independent Human Scoring - Validation and Human-AI Agreement",
       "", "Generated 2026-07-09. Human scores produced with NO AI scores visible (independent).", ""]

# validation
problems = []
if len(human) != 30: problems.append(f"expected 30 rows, got {len(human)}")
for r in human:
    for d in DIMS:
        try:
            x = float(r[d])
            if not 0 <= x <= 5: problems.append(f"{r['blind_answer_id']}: {d}={r[d]} out of range")
        except (ValueError, KeyError):
            problems.append(f"{r['blind_answer_id']}: {d} missing/non-numeric")
    if r["blind_answer_id"] not in ai:
        problems.append(f"{r['blind_answer_id']}: no AI match")

rep.append("## 1. Validation")
rep.append("- " + ("All 30 rows complete, every dimension 0-5, all matched to AI ratings. PASS." if not problems else f"{len(problems)} problems"))
for p in problems[:20]: rep.append(f"  - {p}")
rep.append("")

# distribution
cnt = Counter()
for r in human:
    for d in DIMS: cnt[int(float(r[d]))] += 1
tot = sum(cnt.values())
rep.append("## 2. Human score distribution (scale usage)")
rep.append("| Score | Count | % |"); rep.append("|---|---:|---:|")
for s in range(6): rep.append(f"| {s} | {cnt.get(s,0)} | {100*cnt.get(s,0)/tot:.0f}% |")
rep.append("")

# per-blind-code means
hm = defaultdict(list); am = defaultdict(list)
for r in human:
    hv = sum(float(r[d]) for d in DIMS)/6
    av = sum(float(ai[r['blind_answer_id']][d]) for d in DIMS)/6
    hm[r["blind_model_code"]].append(hv); am[r["blind_model_code"]].append(av)
rep.append("## 3. Mean quality by blind code (still anonymised)")
rep.append("| Blind code | n | Human mean | AI mean |"); rep.append("|---|---:|---:|---:|")
for c in sorted(hm):
    rep.append(f"| {c} | {len(hm[c])} | {sum(hm[c])/len(hm[c]):.2f} | {sum(am[c])/len(am[c]):.2f} |")
rep.append("")

# agreement
h_avg=[]; a_avg=[]; hd={d:[] for d in DIMS}; ad={d:[] for d in DIMS}; diffs=[]
for r in human:
    a=ai[r["blind_answer_id"]]
    hv=sum(float(r[d]) for d in DIMS)/6; av=sum(float(a[d]) for d in DIMS)/6
    h_avg.append(hv); a_avg.append(av); diffs.append((abs(hv-av), r["blind_answer_id"], hv, av))
    for d in DIMS: hd[d].append(int(float(r[d]))); ad[d].append(int(float(a[d])))
rho,p = spearmanr(h_avg,a_avg)
mad = sum(d[0] for d in diffs)/len(diffs)
rep.append("## 4. Human vs AI agreement (n=30)")
rep.append(f"- **Overall average score: Spearman rho = {rho:.3f}** (p={p:.2g})")
rep.append(f"- Mean absolute difference of averages: {mad:.2f} points on the 0-5 scale")
rep.append("")
rep.append("| Dimension | Spearman rho | Weighted kappa | Exact % | Within +/-1 % |")
rep.append("|---|---:|---:|---:|---:|")
for d in DIMS:
    try: dr,_=spearmanr(hd[d],ad[d])
    except: dr=float('nan')
    try: k=cohen_kappa_score(hd[d],ad[d],weights="quadratic")
    except: k=float('nan')
    ex=sum(1 for x,y in zip(hd[d],ad[d]) if x==y)/len(hd[d])*100
    w1=sum(1 for x,y in zip(hd[d],ad[d]) if abs(x-y)<=1)/len(hd[d])*100
    rep.append(f"| {d} | {dr:.2f} | {k:.2f} | {ex:.0f}% | {w1:.0f}% |")
rep.append("")
diffs.sort(reverse=True)
rep.append("## 5. Largest human-AI disagreements")
rep.append("| Blind ID | Human avg | AI avg | diff |"); rep.append("|---|---:|---:|---:|")
for dd,bid,hv,av in diffs[:6]: rep.append(f"| {bid} | {hv:.2f} | {av:.2f} | {dd:.2f} |")
rep.append("")
rep.append("Guide: Spearman >0.7 strong, 0.5-0.7 moderate. Weighted kappa >0.6 substantial, 0.4-0.6 moderate.")

OUT.write_text("\n".join(rep), encoding="utf-8")
HUMAN_ARCHIVE.write_bytes(HUMAN.read_bytes())
print("problems:", len(problems))
print("overall Spearman rho:", round(rho,3), "MAD:", round(mad,3))
print("report:", OUT.name)
