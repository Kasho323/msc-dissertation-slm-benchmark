"""
Make a CLEAN blank 30-answer independent human-scoring subset (2026-07-07).
- 5 answers per blind code x 6 codes = 30.
- Fresh filename so the scoring tool's saved progress does NOT carry over the
  earlier (AI-derived) scores.
- All score columns blank. No AI data anywhere in this file.
"""
import csv, random
from collections import defaultdict
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent / "benchmark_results"
SRC = BASE / "human_stage1_independent_60_2026-06-29.csv"   # blank original 60
OUT = BASE / "human_independent_CLEAN_30_2026-07-07.csv"

DIMS = ["relevance","correctness","faithfulness_to_source",
        "completeness","hallucination_risk","source_grounding"]

with open(SRC, newline="", encoding="utf-8-sig") as f:
    rows = list(csv.DictReader(f))

by_code = defaultdict(list)
for r in rows:
    by_code[r["blind_model_code"]].append(r)

rng = random.Random(20260707)
picked = []
for code in sorted(by_code):
    items = by_code[code][:]
    rng.shuffle(items)
    picked.extend(items[:5])
rng.shuffle(picked)

fields = ["blind_answer_id","blind_model_code","question_id","source_id",
          "source_title","question_type","difficulty","documents_needed",
          "question_text","expected_answer_notes","evidence_location",
          "generated_answer",
          *DIMS,"average_quality_score","scoring_notes","scored_by","scored_date"]

with open(OUT,"w",newline="",encoding="utf-8-sig") as f:
    w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
    w.writeheader()
    for r in picked:
        row = {k: r.get(k,"") for k in fields}
        for d in DIMS: row[d] = ""          # ensure blank
        row["average_quality_score"] = ""
        row["scoring_notes"] = ""; row["scored_by"] = ""; row["scored_date"] = ""
        w.writerow(row)

print("Wrote", OUT.name, "-", len(picked), "blank rows")
print("Per code:", {c: sum(1 for p in picked if p['blind_model_code']==c) for c in sorted(by_code)})
