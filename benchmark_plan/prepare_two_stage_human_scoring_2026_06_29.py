"""
Prepare the two-stage human scoring workflow (2026-06-29).

Stage 1 (independent): 10 stratified questions x 6 blind codes = 60 answers.
  -> human scores these FROM SCRATCH, no AI scores visible.
  -> used later for a genuine human-vs-AI agreement statistic.

Stage 2 (AI-assisted review): remaining 30 questions x 6 codes = 180 answers.
  -> AI second-rater scores shown as DRAFT columns; human reviews/edits.

Design notes:
- The same 10 questions are used for every blind code (paired design).
- Stratified: 2 questions per question_type, spread across difficulty and source docs.
- Deterministic (seed 20260629) so the split is reproducible.
- The blind model key is never read. Blind codes only.
"""

import csv
import random
from collections import defaultdict
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent / "benchmark_results"
BLIND = BASE / "full_benchmark_blind_scoring_rep1_only_C1_C6_2026-06-24.csv"
AI = BASE / "ai_second_rater_codex_gpt_C1_C6_2026-06-25.csv"

OUT_STAGE1 = BASE / "human_stage1_independent_60_2026-06-29.csv"
OUT_STAGE2 = BASE / "human_stage2_ai_assisted_180_2026-06-29.csv"
OUT_PLAN = BASE / "two_stage_scoring_split_2026-06-29.md"

SEED = 20260629
DIMS = ["relevance", "correctness", "faithfulness_to_source",
        "completeness", "hallucination_risk", "source_grounding"]

def read_rows(path):
    with open(path, newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))

blind_rows = read_rows(BLIND)
ai_rows = read_rows(AI)
assert len(blind_rows) == 240, f"expected 240 blind rows, got {len(blind_rows)}"
assert len(ai_rows) == 240, f"expected 240 AI rows, got {len(ai_rows)}"

ai_by_id = {r["blind_answer_id"]: r for r in ai_rows}
missing = [r["blind_answer_id"] for r in blind_rows if r["blind_answer_id"] not in ai_by_id]
assert not missing, f"AI ratings missing for: {missing[:5]}"

# --- choose 10 stratified questions (2 per question_type) ---
q_meta = {}
for r in blind_rows:
    q_meta[r["question_id"]] = {
        "question_type": r["question_type"],
        "difficulty": r["difficulty"],
        "source_id": r["source_id"],
    }

by_type = defaultdict(list)
for qid, m in sorted(q_meta.items()):
    by_type[m["question_type"]].append(qid)

rng = random.Random(SEED)
stage1_questions = []
for qtype in sorted(by_type):
    qids = by_type[qtype]
    # prefer spreading across difficulty and source docs
    rng.shuffle(qids)
    qids.sort(key=lambda q: (q_meta[q]["difficulty"], q_meta[q]["source_id"]))
    # take first and last after sort -> spreads difficulty/doc
    picks = [qids[0], qids[-1]] if len(qids) >= 2 else qids[:1]
    stage1_questions.extend(picks)

stage1_set = set(stage1_questions)
assert len(stage1_set) == 10, f"expected 10 stage-1 questions, got {len(stage1_set)}"

stage1 = [r for r in blind_rows if r["question_id"] in stage1_set]
stage2 = [r for r in blind_rows if r["question_id"] not in stage1_set]
assert len(stage1) == 60 and len(stage2) == 180

rng.shuffle(stage1)
rng.shuffle(stage2)

# --- Stage 1 file: blank human columns, NO AI data ---
stage1_fields = [
    "blind_answer_id", "blind_model_code", "question_id", "source_id",
    "source_title", "question_type", "difficulty", "documents_needed",
    "question_text", "expected_answer_notes", "evidence_location",
    "generated_answer",
    *DIMS, "average_quality_score", "scoring_notes", "scored_by", "scored_date",
]
with open(OUT_STAGE1, "w", newline="", encoding="utf-8-sig") as f:
    w = csv.DictWriter(f, fieldnames=stage1_fields, extrasaction="ignore")
    w.writeheader()
    for r in stage1:
        w.writerow(r)

# --- Stage 2 file: AI draft columns + blank human columns ---
stage2_fields = [
    "blind_answer_id", "blind_model_code", "question_id", "source_id",
    "source_title", "question_type", "difficulty", "documents_needed",
    "question_text", "expected_answer_notes", "evidence_location",
    "generated_answer",
    *[f"ai_draft_{d}" for d in DIMS], "ai_draft_average", "ai_draft_notes",
    *[f"human_{d}" for d in DIMS], "human_average", "review_status",
    "human_notes", "scored_by", "scored_date",
]
with open(OUT_STAGE2, "w", newline="", encoding="utf-8-sig") as f:
    w = csv.DictWriter(f, fieldnames=stage2_fields, extrasaction="ignore")
    w.writeheader()
    for r in stage2:
        ai = ai_by_id[r["blind_answer_id"]]
        row = {k: r.get(k, "") for k in stage2_fields if not k.startswith(("ai_", "human_")) and k not in ("review_status",)}
        for d in DIMS:
            row[f"ai_draft_{d}"] = ai[d]
        row["ai_draft_average"] = ai["average_quality_score"]
        row["ai_draft_notes"] = ai.get("scoring_notes", "")
        row["review_status"] = "AI draft - needs human review"
        w.writerow(row)

# --- split record ---
lines = ["# Two-Stage Human Scoring Split (2026-06-29)", "",
         f"Random seed: {SEED} (deterministic, reproducible)", "",
         "## Stage 1 - independent human scoring (no AI shown)",
         f"- File: {OUT_STAGE1.name}",
         "- 10 questions x 6 blind codes = 60 answers, shuffled.",
         "- Chosen questions (2 per question type, spread over difficulty/docs):", ""]
for qid in sorted(stage1_set):
    m = q_meta[qid]
    lines.append(f"  - {qid}: {m['question_type']}, {m['difficulty']}, {m['source_id']}")
lines += ["", "## Stage 2 - AI-assisted review",
          f"- File: {OUT_STAGE2.name}",
          "- Remaining 30 questions x 6 codes = 180 answers, shuffled.",
          "- AI second-rater scores shown as ai_draft_* columns; human fills human_* columns.",
          "", "## Rules",
          "- Complete Stage 1 BEFORE opening Stage 2.",
          "- Never open the blind model key until all human scoring is done.",
          "- Stage 1 human scores vs AI scores on the same 60 answers give the genuine",
          "  human-AI agreement statistic (Spearman/kappa) reported in the dissertation."]
OUT_PLAN.write_text("\n".join(lines), encoding="utf-8")

print("Stage 1:", OUT_STAGE1.name, "-", len(stage1), "rows")
print("Stage 2:", OUT_STAGE2.name, "-", len(stage2), "rows")
print("Stage-1 questions:", ", ".join(sorted(stage1_set)))
