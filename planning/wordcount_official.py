# -*- coding: utf-8 -*-
"""WMG official count. Counted: body prose, headings, tables, captions, abstract.
Not counted: drafting notes, planning scaffolding, status lines, [CITE]/[FILL]
placeholders (these become Harvard citations later), markdown pipes/markup."""
import sys, re
from pathlib import Path

SKIP = ("planned sections","verified material available","cautions carried forward",
        "material to place elsewhere","drafting notes","working notes")
FILES = [("Abstract","abstract_draft_2026-07-26.md"),
         ("Ch1 Introduction","introduction_draft_2026-07-26.md"),
         ("Ch2 Literature","literature_review_draft_2026-08-11.md"),
         ("Ch3 Methodology","methodology_draft_2026-07-27.md"),
         ("Ch4 Results","results_draft_2026-07-28.md"),
         ("Ch5 Analysis","analysis_draft_2026-08-12.md"),
         ("Ch6 Discussion","discussion_chapter_2026-08-13.md"),
         ("Ch7 Conclusion","conclusion_draft.md")]

def count(path):
    if not path.exists(): return None
    lines = path.read_text(encoding="utf-8").splitlines()
    # everything between the file title and the first horizontal rule is the
    # drafting header, not dissertation text (same rule as the docx builder)
    div = next((i for i, l in enumerate(lines[1:], 1) if l.strip() == "---"), None)
    if div is not None:
        lines = [lines[0]] + lines[div + 1:]
    n=0; skipping=False
    for line in lines:
        s=line.strip()
        if s.startswith("# "): skipping=False; continue          # file title
        if s.startswith("##"):
            skipping = any(s.lstrip("#").strip().lower().startswith(k) for k in SKIP)
        if skipping or not s: continue
        if s.startswith("---"): continue
        if s.startswith(">"):                                     # note vs real quotation
            rest = s.lstrip(">").strip()
            if rest.startswith(("Note (", "Optional addition", "Optional:", "Planned topics",
                                "Specifically:", "**PENDING", "PENDING —")): continue
            s = rest
        if s.startswith("[FILL") or s.startswith("[PENDING"): continue
        if s.startswith("**Status:**"): continue                  # file metadata
        if re.fullmatch(r"[-|: ]+", s): continue                  # table separator row
        s = re.sub(r"\[CITE[^\]]*\]", " ", s)                     # placeholder, not yet text
        s = s.replace("|"," ").replace("*"," ").replace("#"," ")
        n += len(s.split())
    return n

base = Path(sys.argv[1]); tot=0
print(f"{'':20s}{'words':>7}")
for label, fn in FILES:
    c = count(base/fn)
    if c is None: print(f"{label:20s}{'—':>7}   (not written)"); continue
    tot+=c; print(f"{label:20s}{c:7d}")
print(f"{'-'*27}\n{'BODY TOTAL':20s}{tot:7d}")
