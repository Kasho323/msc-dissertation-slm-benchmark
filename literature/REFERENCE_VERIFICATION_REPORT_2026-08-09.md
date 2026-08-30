# Reference verification report

**Date:** 2026-08-09
**Scope:** all 63 non-thesis entries (S01–S63) in `MASTER_REFERENCE_PLAN.md`. The five example theses (S64–S68) were excluded: they are public repository records used for presentation study, not cited sources.

**Why this was done:** WMG's guidance on AI in assessment states that generative AI "produces fake citations and references". Every candidate source was therefore checked against the publisher's own record before any of it enters the dissertation's reference list.

**Method:** each source's primary link was fetched and compared with the publisher-deposited metadata (`citation_title`, `citation_author`, `citation_date`, or the page title). Where the publisher blocked automated access (Cloudflare, IEEE, OpenReview, Sage) or served a PDF with no HTML metadata, the record was re-checked through the Crossref REST API, the arXiv API, or an HTTP status check on the file itself.

## Headline result

**All 63 sources are real, existing publications or official documents. No fabricated reference was found.**

| Outcome | Count |
|---|---:|
| Title, authors and year confirmed against the publisher record | 63 |
| Fabricated or non-existent | 0 |
| Metadata details still to settle before the final reference list | 4 |

## Items still to settle (metadata only — all four sources are real)

| ID | Source | Issue | Action |
|----|--------|-------|--------|
| S04 | Malkov and Yashunin, HNSW | The plan records **2018**; Crossref gives the IEEE TPAMI issue year as **2020** (the DOI carries 2018 because that was the acceptance/early-access year) | Decide which version is being cited and use that year consistently |
| S53 | OWASP LLM Top 10 | The page now resolves to the **OWASP Gen AI Security Project**; the project and document have been renamed since earlier editions | Record the exact document title, edition and year of the version actually used |
| S51 | GDPR, Regulation (EU) 2016/679 | The EUR-Lex link returns a bot-challenge response rather than the document; the CELEX identifier itself is correct | Use the stable ELI permalink `https://eur-lex.europa.eu/eli/reg/2016/679/oj` |
| S48 | NIST Privacy Framework | Crossref returns the title truncated as "NIST PRIVACY FRAMEWORK:" | Use the full official title from the document itself |

## Not defects

- **S16, S20, S25** — the plan's years (2024, 2024, 2016) are the years of the *published* versions; the arXiv preprints are earlier (2023, 2023, 2015). Citing the published version is correct, so no change is needed. The same applies to S10 (arXiv 2023, ICLR 2024).
- **S34, S35, S38, S41, S42, S44, S45, S53** — these are official documentation, model cards and technical reports. Their web-page titles differ from the descriptive names used in the plan (for example `sentence-transformers/all-MiniLM-L6-v2 · Hugging Face` versus "all-MiniLM-L6-v2 Model Card"). The links resolve to the correct resources.
- **S41, S47** — direct PDF links; both confirmed reachable and served as PDFs (3.7 MB and 1.2 MB respectively).

## Sources confirmed through a secondary authority

These publishers blocked automated access, so the record was confirmed through Crossref or arXiv instead:

| ID | Confirmed via | Publisher record |
|----|---------------|------------------|
| S03 | Crossref | Robertson and Zaragoza, 2009, *Foundations and Trends in Information Retrieval* |
| S04 | Crossref | Malkov and Yashunin, IEEE TPAMI (see note above) |
| S10 | arXiv 2310.11511 | Asai, Wu, Wang, Sil — Self-RAG |
| S46 | Crossref | Tabassi, 2023, NIST report |
| S48 | Crossref | NIST, 2020, report |
| S56 | Crossref | Wang and Chau, 2024, ACM SIGIR proceedings |
| S59 | Crossref | Cohen, 1960, *Educational and Psychological Measurement* |
| S61 | Crossref | Artstein and Poesio, 2008, *Computational Linguistics* |
| S63 | Crossref | Gundersen and Kjensmo, 2018, AAAI (DOI 10.1609/aaai.v32i1.11503) |

## What this report does and does not establish

It establishes that each candidate source **exists** and that the recorded title, authors and year match the publisher's record. It does **not** establish that a source supports any particular claim in the dissertation: that still requires reading the source and is recorded separately in `literature_matrix.md`. A source should be cited only once it has been read closely enough to identify the exact claim it supports.
