# Link and date verification

**Date:** 2026-08-30
**Scope:** all 33 entries in the final reference list (`REFERENCES_HARVARD_2026-08-13.md`).
**Reason:** supervisor comments of 25 August 2026 on the annotated draft:

> #118 "This has a date on their website. Please check and verify. This guidance was updated on 15 March 2023."
> #119 "Was the entire literature review conducted in one day?"
> #120 "Please re-verify those links."
> #53 "Pick the website update date or access date."

## Method

Every URL was requested with `curl` using a desktop browser user-agent, following
redirects. Entries that returned a non-2xx status on the first pass were re-checked with a
full GET, and where the host blocks automated access the record was confirmed through the
Crossref REST API instead. Update dates were taken from the host's own metadata: the GitHub
commit API for repository files, the Hugging Face model API `lastModified` field, and the
page text itself for the ICO guidance.

## Result: all 33 links resolve

| Outcome | Count |
|---|---:|
| Resolved with a 2xx status | 31 |
| Host blocked automation; record confirmed through Crossref | 1 |
| Redirect to the canonical host, confirmed reachable | 1 |
| Dead, moved without redirect, or not found | **0** |

### The two entries that needed a second pass

| Entry | First pass | Resolution |
|---|---|---|
| Fan et al. (2024) | `403` from `dl.acm.org` | Cloudflare blocks automated requests. The Crossref record for `10.1145/3637528.3671470` returns the title, *Proceedings of the 30th ACM SIGKDD Conference on Knowledge Discovery and Data Mining*, pp. 6491–6501, publisher ACM, first authors Fan, Ding, Ning. All match the reference entry. A second ACM DOI in the list (Wang and Chau) returned `200`, so the block is intermittent rather than a broken link. |
| Reimers and Gurevych (2019) | `301` from `doi.org` | Permanent redirect to `aclanthology.org/D19-1410`. Both the trailing-slash and no-slash forms return `200`. |

The two ICO pages returned `405` when probed with `HEAD` because the host does not allow
that method; both return `200` under `GET`.

## Dates established for previously undated web sources

Comment #53 asked for either the website update date or the access date. The reference list
already carried access dates, so the update date was established from each host's own record
and used as the publication year. Nothing was inferred where a host did not state a date.

| Source | Evidence | Year used |
|---|---|---|
| ICO, *Guidance on AI and data protection* | The page body states "This guidance was updated on 15 March 2023." | 2023a |
| ICO, *How should we assess security and data minimisation in AI?* | A section of the same guidance; the parent page carries the update statement above. The sub-page itself states no separate date. | 2023b |
| ggml-org, *GGUF specification* | GitHub commit API, `repos/ggml-org/ggml/commits?path=docs/gguf.md` → last commit 2026-07-09 | 2026a |
| ggml-org, *llama.cpp* | GitHub repository API → last push 2026-08-28; the repository is under continuous development | 2026b |
| ggml-org, *llama.cpp quantize documentation* | GitHub commit API, `repos/ggml-org/llama.cpp/commits?path=tools/quantize/README.md` → last commit 2026-06-05 | 2026c |
| Qwen Team, *Qwen2.5-1.5B-Instruct model card* | Hugging Face model API → `lastModified` 2024-09-25 | 2024b |
| Sentence Transformers, *all-MiniLM-L6-v2 model card* | Hugging Face model API → `lastModified` 2026-06-01 | 2026a |
| Sentence Transformers, *ms-marco-MiniLM-L6-v2 cross-encoder model card* | Hugging Face model API → `lastModified` 2026-08-09 | 2026b |

The DC.Date metadata on the two ICO pages (2026-01-21 and 2025-08-26) records when the
content-management system last republished the page, not the version date of the guidance,
so it was **not** used.

After this change the reference list contains no undated entry.

## Note on the access dates (comment #119)

Twenty-one entries carry the access date 15 August 2026. This is not a sign that the reading
was done in one day. The access date records when the URL was last retrieved, which was done
as a batch verification step, not when each source was read. The reading is recorded
separately in `literature_matrix.md`, and the source-existence check carried out on
2026-08-09 is recorded in `REFERENCE_VERIFICATION_REPORT_2026-08-09.md`, which covered all 63
candidate sources against publisher metadata.

The access dates were therefore left unchanged. Assigning differentiated dates that were not
actually recorded would misrepresent the process.
