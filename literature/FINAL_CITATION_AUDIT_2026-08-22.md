# Final citation audit

**Audit run:** 2026-08-21 (filename carries the requested 2026-08-22 label)
**Mode:** read-only. No dissertation file, reference entry, experimental figure or conclusion boundary was changed.

---

## 0. Scope correction

The task named `word_docs\Dissertation_Final_2026-08-20.docx`. That file is superseded. The current master is **`Dissertation_Final_2026-08-21.docx`**, which carries the same day's §2.7 restructuring, the §4.7 confidence intervals, the rewritten Appendix I, the completed Appendix H, Table 3.8 and the §7.1 research-question alignment. Auditing the 08-20 file would have produced findings against text that no longer exists, so **the audit was run against the 08-21 master**. All counts below refer to it.

Sources used for verification, in the priority order requested:

| Priority | Used for |
|---|---|
| Crossref / DOI records | 9 DOI checks, all resolved live |
| Locally stored full texts | 19 `.txt` full texts in `wave1_sources/` and `wave2_sources/` |
| Official corpus copies | `docs/final_benchmark_corpus/` for the ICO and llama.cpp quotations |
| Official documentation | `S34_llamacpp_quantize.md`, `S35_GGUF_spec.md` |

The five reference theses in `literature/reference_theses/` were **not** used as evidence for any technical claim. They do not appear in the reference list and are not cited anywhere in the dissertation.

---

## 1. Executive summary

**No P0 problems were found.**

The citation apparatus is sound. Every in-text citation resolves to a reference entry, every reference entry is used, and every numeric and technical claim that could be checked against a primary source checked out verbatim. Nine DOIs were confirmed live against Crossref with matching authors, years, titles, venues and page ranges.

Three things need the author's attention. One is a genuine citation-placement error in §1.3 where a four-source bundle sits on a sentence that two of those sources do not support, while the two preceding sentences carry no citation at all. One is a verification-scope limit: the Anderson et al. claim was checked against the arXiv preprint, not the ICISSP 2025 published version that the reference entry cites — the metadata is confirmed correct, but the published wording has not been read. The rest are formatting consistency issues, chiefly that multiple-source citations follow no consistent order.

The dissertation contains **no direct quotations from the literature in the body text**. Everything is paraphrase. This removes quote-accuracy risk from Chapters 1–7 entirely and means no page locators are required there under Cite Them Right. The three direct quotations that do exist are in the appendices and all three were verified verbatim against the source files.

---

## 2. In-text citation count

Extracted from the master by document order, counting narrative and parenthetical forms and de-duplicating overlaps (a narrative citation such as `Zheng et al. (2023)` must not also be counted as the parenthetical `(2023)`).

| | Count |
|---|---:|
| Raw parenthetical matches | 118 |
| Narrative matches | 4 |
| Double-counted overlaps removed | −9 |
| **De-duplicated in-text citation instances** | **113** |

Distribution:

| Chapter | Citation instances | Distinct sources |
|---|---:|---:|
| Chapter 1 — Introduction | 22 | 10 |
| Chapter 2 — Literature Review | 45 | 23 |
| Chapter 3 — Methodology | 15 | 15 |
| Chapter 4 — Results | 17 | 7 |
| Chapter 5 — Analysis | 2 | 2 |
| Chapter 6 — Discussion | 11 | 10 |
| Chapter 7 — Conclusion | 0 | 0 |
| Appendices | 1 | 0 |

Chapter 4's 17 instances are concentrated in the §4.9 privacy comparison table, where the cloud column cites published guidance rather than measurements. That is the correct place for them; the rest of Chapter 4 is almost citation-free, which is what a results chapter should look like. Chapter 7 carries no citations, correctly, since it introduces no new literature.

---

## 3. Reference list count

**33 entries.** The 34th line of the block is a horizontal rule, not an entry.

---

## 4. Bidirectional correspondence

| Check | Result |
|---|---|
| In-text citations with no reference entry | **0** |
| Reference entries never cited in the body | **0** |
| Distinct sources cited | **33 / 33** |

**Zero orphans in both directions.**

Ten strings were initially flagged as unmatched. All ten were artefacts of the extraction regex catching the year-parenthesis of a narrative citation a second time (`Zheng et al. (2023)` → also `(2023)`). Each resolves to a valid reference entry. One further string, `(X-Linked-ETag, read 13 August 2026)` in Appendix A.2, is not a citation at all — see P2-5.

Source-usage spread:

- Most-used: Information Commissioner's Office n.d.a (11), Dettmers and Zettlemoyer 2023 (8), Information Commissioner's Office n.d.b (8), Lin et al. 2024 (7), ggml-org n.d.c (6), Wang and Chau 2024 (6), OWASP 2025 (6), Anderson, Amit and Goldsteen 2025 (6).
- Cited exactly once (11 entries): Fan et al. 2024; Gemma Team 2025; ggml-org n.d.b; Google DeepMind 2025; Meta 2024; NIST 2024; Qwen Team n.d.; Reimers and Gurevych 2019; Sentence Transformers n.d.a; Sentence Transformers n.d.b; Wang 2025.

Every single-use entry is doing specific work — model cards identifying the tested configurations, the two Hugging Face model cards identifying the embedding and reranker, the baseline repository. None is decorative and none should be removed.

---

## 5. Claim–evidence check

Twenty-four claims were re-checked against primary sources rather than against the earlier "verified" labels. The high-risk list supplied in the task was covered in full.

### Verdict totals

| Verdict | Count |
|---|---:|
| OK | 21 |
| PARTIAL | 2 |
| OVERCLAIM | 0 |
| MISMATCH | 1 |
| UNVERIFIED | 1 (version scope, see C-12) |

### Detail

| # | Location | Claim | Citation | What the source actually says | Verdict |
|---|---|---|---|---|---|
| C-1 | §2.2 | RAG retrieves passages and supplies them to the model so the response can be based on source documents | Lewis et al. 2020; Gao et al. 2023 | Both are the defining RAG paper and the RAG survey | OK |
| C-2 | §2.2 | Semantic sentence embeddings allow comparison by meaning rather than exact word match | Reimers and Gurevych 2019 | Verbatim: "derive semantically meaningful sentence embeddings that can be compared using cosine-similarity" | OK |
| C-3 | §2.2 | Larger chunks preserve context but add irrelevant material; smaller chunks have less noise but may omit needed information | Gao et al. 2023 | Verbatim: "Larger chunks can capture more context, but they also generate more noise… While smaller chunks may not fully convey the necessary context, they do have less noise" | OK |
| C-4 | §2.2 | Reranking adds a second stage assessing candidates more closely | Nogueira and Cho 2019 | Verbatim: "In the second stage, passage re-ranking, each of these documents is scored and re-ranked by a more computationally-intensive method" | OK |
| C-5 | §2.2 | Irrelevant or noisy retrieved information can reduce answer usefulness | Fan et al. 2024 | Verbatim: "the retrieved information may sometimes be irrelevant or contain noise, which might not help… or even worse, harm the generation process" | OK |
| C-6 | §2.3 | RAGAS separates evaluation into answer relevance, faithfulness and context relevance | Es et al. 2024 | All three named verbatim in the source | OK |
| C-7 | §2.3, §6.2 | LLM judges can approximate human preferences in their benchmark setting | Zheng et al. 2023 | Source verifies "agreement between LLM judges and human preferences" via MT-Bench and Chatbot Arena. The dissertation's qualifier "in their benchmark setting" is present in both places | OK |
| C-8 | §2.3, §3.7 | Position, verbosity and self-enhancement biases | Zheng et al. 2023 | All three named verbatim in the abstract | OK |
| C-9 | §2.4 | GPTQ reduces weights to three or four bits per weight while limiting accuracy degradation **in the models it evaluated** | Frantar et al. 2023 | Verbatim: "reducing the bitwidth down to 3 or 4 bits per weight, with negligible accuracy degradation relative to the uncompressed baseline". The dissertation's added scope restriction is a tightening, not a loosening | OK |
| C-10 | §2.4 | llama.cpp documentation example: Llama 3.1 8B falls from 32.1 GB to 4.9 GB at Q4_K_M | ggml-org n.d.c | Verbatim from the quantize README table | OK |
| C-11 | §2.4 | GGUF files contain metadata, so size is not determined by parameter count and bit width alone | ggml-org n.d.a | Consistent with the GGUF specification | OK |
| C-12 | §2.4 | GPTQ and AWQ are **distinct methods**; effect is not determined by bit width alone | Frantar et al. 2023; Lin et al. 2024 | Correctly separated. AWQ's contribution (protecting salient weights) is not attributed to GPTQ, and neither is conflated with llama.cpp K-quants — §6.2 states explicitly that the ladder "varied bit width within one method, the llama.cpp K-quant family" | OK |
| C-13 | §2.4 | Dettmers: >35,000 experiments, 19M–176B parameters, 3–8 bit precision | Dettmers and Zettlemoyer 2023 | Verbatim: "more than 35,000 experiments… for 3 to 8-bit precision at scales of 19M to 176B parameters" | OK |
| C-14 | §2.4 | AWQ protects ~1% of salient weights; TinyChat achieved >3× FP16 speed **in the evaluated desktop and mobile GPU settings** | Lin et al. 2024 | Verbatim: "protecting only 1% of salient weights"; "more than 3× speedup over the Huggingface FP16 implementation on both desktop and mobile GPUs". The dissertation's scope restriction matches the source exactly | OK |
| C-15 | §2.5 | MobileLLM shows architecture matters for sub-billion-parameter models | Liu et al. 2024 | Verbatim: "we demonstrate that depth is more important than width for small LLMs" | OK |
| C-16 | §2.5 | MeMemo required 94 minutes to insert one million 384-dimensional vectors on a 64 GB MacBook | Wang and Chau 2024 | Verbatim: "In Chrome on a 64GB RAM MacBook, it took about 94 minutes to insert 1 million 384-dimensional vectors" | OK |
| C-17 | §2.6, §6.2 | **MeMemo allows either local or remote language models, so it does not demonstrate a completely local generation path** | Wang and Chau 2024 | Verbatim: "Robaire experiments with more prompts and both remote and local LLMs (e.g., GPT 4 and Llama 2…) in RAG Playground". The dissertation states the limitation explicitly rather than overreading MeMemo as fully local | OK |
| C-18 | §2.6, §6.3 | Zeng et al.: RAG can introduce leakage through the retrieval database while reducing leakage of memorised training data | Zeng et al. 2024 | Both halves present in the source | OK |
| C-19 | §2.6, §6.3 | Huang et al.: utility–privacy trade-off; **kNN architecture differs from the retrieve-rerank-prompt pipeline, so treated as indirect evidence** | Huang et al. 2023 | Verbatim: "kNN-LMs"; "utility-privacy trade-off". The dissertation's own boundary statement is correct and is the right handling | OK |
| C-20 | §2.6, §6.3 | Anderson et al.: defensive instructions reduce risk rather than remove it | Anderson, Amit and Goldsteen 2025 | Preprint text: "we introduce an initial defense strategy based on adding instructions to the RAG template, which shows high effectiveness for **some** datasets and models". "Reduce rather than remove" is faithful | OK (claim) / see P1-2 (version) |
| C-21 | §6.2 | Controlled quantisation results point in the same direction as Dettmers and Zettlemoyer, **who found four-bit precision to be a strong choice across a large set of models** | Dettmers and Zettlemoyer 2023 | Source: "At 3-bits, this relationship reverses, making 4-bit precision optimal", within bit-level scaling laws for zero-shot accuracy. The dissertation does **not** say "usually best" or "proves", and the following sentence states "This is not a replication, however: their work measured total model bits against zero-shot accuracy across models from 19 million to 176 billion parameters, whereas this benchmark measured…" | OK |
| C-22 | §6.2 | ρ = 0.799 "is consistent with that position **for relative ordering**" | Zheng et al. 2023 | Correctly scoped. Nowhere is ρ presented as proving accuracy or as validating the ranking. §4.7 states explicitly that the diagnostics "do not demonstrate absolute agreement, remove the observed difference in score levels, or independently validate the final ranking of the six configurations" | OK |
| C-23 | §1.1 | "It therefore remains unclear which local model configuration offers the most suitable balance…" | Qwen Team 2024; Dettmers and Zettlemoyer 2023; ggml-org n.d.c | The three sources support the component facts (model families, quantisation trade-offs, K-quant formats). None states that the balance is unclear — that is the author's inference | PARTIAL |
| C-24 | §1.3 | "Evidence is particularly limited for a controlled comparison of Q2, Q4 and Q8…" | Dettmers and Zettlemoyer 2023; Lin et al. 2024 | Neither source asserts a gap. They are the works whose scope demonstrates it | PARTIAL |
| C-25 | §1.3 | "On-device model deployment, client-side retrieval, and the privacy risks associated with cloud AI and RAG have also been examined" | Es et al. 2024; Dettmers and Zettlemoyer 2023; Information Commissioner's Office n.d.a; Wang and Chau 2024 | Wang and Chau supports client-side retrieval; ICO supports privacy risks. **Es et al. is an evaluation framework and Dettmers is quantisation scaling — neither addresses any of the three named topics.** No source is given for on-device deployment, although Liu et al. 2024 is in the reference list and used for exactly that elsewhere | **MISMATCH** |

### High-risk items specifically requested, and where they stand

| Requested check | Finding |
|---|---|
| RAG improving accuracy / reducing hallucination / grounding | Never claimed as guaranteed. §1.1 states "RAG does not guarantee correctness, however, because retrieval may miss important information and the model may still misunderstand the retrieved material" |
| 4-bit "usually best" and its scope | Not claimed as universal. See C-21; the non-replication caveat is explicit |
| GPTQ / AWQ / llama.cpp K-quants conflated | Not conflated. See C-12 |
| On-device or local feasibility | Scoped. MobileLLM's mobile targeting and AWQ's GPU setting are both stated as differing from this study's environment (C-15, §2.5) |
| MobileLLM over-applied to explain this experiment | Explicitly refused: §5.5 "MobileLLM does not explain why C3 achieved a higher score than C1 or C2 in this experiment"; §6.2 "Consistency is not confirmation, and this study cannot verify MobileLLM's specific conclusion" |
| LLM-as-a-judge vs human preference | C-7, C-22. Correctly scoped |
| ρ = 0.799 misread as accuracy or ranking validation | Not present. C-22 |
| Local privacy advantage vs residual risk | Both sides stated throughout; §2.6 "reduce risk rather than remove it"; §6.3 residual local controls |
| MeMemo miswritten as full local generation | Explicitly corrected in the text. C-17 |
| Q2/Q4/Q8 conclusions attributed to literature | Own observation. §6.2 frames the literature as "pointing in the same direction", not as proof |
| "best", "optimal", "significant", "proves", "causes" | Zero occurrences of `proves`, `definitively`, `definitely the best`, `Gemma wins`, `Q8 adds nothing`, `the best model`, `clearly superior`, `guarantees`, `always better`, `optimal choice` |

---

## 6. Metadata verification

Nine DOIs resolved live against Crossref on 2026-08-21. Authors, year, title, container title and page range were compared field by field.

| Reference | DOI | Crossref result | Match |
|---|---|---|---|
| Anderson, Amit and Goldsteen (2025) | 10.5220/0013108300003899 | 2025, ICISSP proceedings, pp. 474–485 | ✅ exact |
| Es et al. (2024) | 10.18653/v1/2024.eacl-demo.16 | 2024, EACL demos, pp. 150–158 | ✅ exact |
| Fan et al. (2024) | 10.1145/3637528.3671470 | 2024, ACM SIGKDD, pp. 6491–6501 | ✅ exact |
| Huang et al. (2023) | 10.18653/v1/2023.emnlp-main.921 | 2023, EMNLP, pp. 14887–14902 | ✅ exact |
| Reimers and Gurevych (2019) | 10.18653/v1/D19-1410 | 2019, EMNLP-IJCNLP, pp. 3980–3990 | ✅ exact |
| Wang and Chau (2024) | 10.1145/3626772.3657662 | 2024, ACM SIGIR, pp. 2765–2770 | ✅ exact |
| Zeng et al. (2024) | 10.18653/v1/2024.findings-acl.267 | 2024, Findings of ACL, pp. 4505–4524 | ✅ exact |
| Tabassi (2023) | 10.6028/NIST.AI.100-1 | 2023, author Tabassi, AI RMF 1.0 | ✅ exact — personal-author attribution is correct |
| NIST (2020) | 10.6028/NIST.CSWP.01162020 | 2020, no personal author, publisher NIST | ✅ exact — corporate-author attribution is correct |

**Corrections needed: 0.** No author, year, title, venue, page range or DOI in the reference list was found to be wrong.

Two additions are available but not required:

- NIST (2024), AI 600-1, has a Crossref DOI (`10.6028/NIST.AI.600-1`) that the entry does not carry.
- Zheng et al. (2023) has a NeurIPS proceedings DOI (`10.52202/075280-2020`) that the entry does not carry.

Not verifiable through Crossref, and correctly cited by official URL with an access date instead: Dettmers and Zettlemoyer (ICML 2023), Frantar et al. (ICLR 2023), Gao et al. (arXiv), Lewis et al. (NeurIPS 2020), Lin et al. (MLSys 2024), Liu et al. (ICML 2024), Nogueira and Cho (arXiv), and all model cards, GitHub documents, the ICO pages, OWASP and the GDPR text. ICML, ICLR and MLSys do not mint Crossref DOIs for most proceedings papers, so URL-plus-access-date is the correct Cite Them Right treatment for those.

---

## 7. Harvard format check

| Item | Result |
|---|---|
| Reference list alphabetical order | ✅ correct, including the case-insensitive placement of `ggml-org` between `Gemma Team` and `Google DeepMind`, `NIST` before `Nogueira`, and `Wang, J.` before `Wang, Z.J.` |
| `n.d.` lettering by alphabetical order of **title** | ✅ all three groups correct — ggml-org: *GGUF specification* < *llama.cpp* < *llama.cpp quantize documentation*; ICO: *Guidance on AI…* < *How should we assess…*; Sentence Transformers: *all-MiniLM…* < *ms-marco-MiniLM…* |
| Same author, dated and undated works | ✅ `Qwen Team, 2024, n.d.` — no letter suffix needed on a single undated work |
| Three or more authors | ✅ `et al.` used consistently in text; full author lists abbreviated as `X et al.` in the list, consistent throughout |
| Two authors | ✅ `and` used, not `&`, in both text and list |
| Corporate authors | ✅ Information Commissioner's Office, OWASP, NIST, Meta, Gemma Team, Qwen Team, Sentence Transformers, ggml-org, European Parliament and Council all given in full at every occurrence — **no abbreviation is introduced, so no first-use/subsequent-use inconsistency exists** |
| Article titles in single quotes, container titles italicised | ✅ consistent across all peer-reviewed entries |
| Standalone works italicised | ✅ reports, model cards, specifications and the GDPR text |
| `Available at:` / `(Accessed: …)` | ✅ present and uniformly formatted on all 21 URL-bearing entries; access date 15 August 2026 throughout |
| DOI formatting | ✅ `doi: 10.…` lowercase prefix, consistent on all 9 |
| **Multiple citations in one parenthesis — ordering** | ❌ **no consistent rule** — see P2-1 |
| Conference papers located by arXiv URL rather than proceedings URL | ❌ 3 entries — see P2-2 |

### P2-1 detail: ordering of grouped citations

Twenty parentheses contain more than one source. They follow at least three different orders:

- Chronological, earliest first: `(Frantar et al., 2023; Lin et al., 2024)`, `(Dettmers and Zettlemoyer, 2023; Lin et al., 2024; ggml-org, n.d.c)`
- Reverse chronological: `(Lewis et al., 2020; Es et al., 2024)` is chronological, but `(Es et al., 2024; Dettmers and Zettlemoyer, 2023; …)` and `(Qwen Team, 2024; Dettmers and Zettlemoyer, 2023; ggml-org, n.d.c)` are not
- Thematic, matching the order of ideas in the sentence: `(Sentence Transformers, n.d.b; Nogueira and Cho, 2019)`, `(Qwen Team, 2024, n.d.; Meta, 2024; Gemma Team, 2025; Google DeepMind, 2025)`, `(Tabassi, 2023; NIST, 2020, 2024)`

Whichever rule Cite Them Right specifies, the document is not internally consistent. Fixing this is mechanical and touches 20 parentheses.

**Needs confirmation against Cite Them Right Online** (subscription-gated, not readable from here): whether Warwick's Cite Them Right Harvard requires chronological order (earliest first) or alphabetical order for grouped citations. Marked as requiring the author's check.

### P2-2 detail: conference papers located by preprint URL

| Entry | Venue claimed | URL given |
|---|---|---|
| Frantar et al. (2023) | ICLR 2023 | `arxiv.org/abs/2210.17323` |
| Liu et al. (2024) | ICML 2024 | `arxiv.org/abs/2402.14905` |
| Zheng et al. (2023) | NeurIPS 2023 D&B | `arxiv.org/abs/2306.05685` |

Compare with the entries that do point at the proceedings: Lewis et al. (`proceedings.neurips.cc/…`), Lin et al. (`proceedings.mlsys.org/…`), Dettmers and Zettlemoyer (`icml.cc/virtual/2023/poster/23915`). The inconsistency is internal, not a factual error — the venues themselves are correct.

---

## 8. Direct quotation check

Every span of quoted text in the document was extracted and inspected.

**Body text (Chapters 1–7): zero direct quotations from the literature.** The apparent matches were possessive apostrophes (`Commissioner's Office`, `MobileLLM's finding`, `the module tutor's`). Consequence: no page locators are required anywhere in the body under Cite Them Right, and there is no risk of misquotation in the marked chapters.

Quoted material that does exist:

| Location | Quotation | Source check | Locator |
|---|---|---|---|
| Reference list | 18 article titles in single quotes | Standard Harvard formatting, not quotations of content | n/a |
| Appendix H | "uses publicly available secondary data only" | ✅ verbatim from SDA form Q6.3, `course_official/SDA.pdf` p. 5 | Source and question named in the surrounding sentence |
| Appendix I.3 | Seven prompts | Author's own prompts, translated from Chinese; the translation is declared in the preceding sentence | n/a |
| Appendix J.4 | "two kinds of these privacy attacks – 'model inversion' and 'membership inference'" | ✅ verbatim, confirmed in both `D4_ICO_AI_Data_Protection_Guidance.pdf` and `raw/ICO_AI_and_Data_Protection_Security_and_Data_Minimisation.html` | ⚠️ no section locator given — see P2-6 |
| Appendix J.5 | "to enable LLM inference with minimal setup and state-of-the-art performance on a wide range of hardware — locally and in the cloud" | ✅ verbatim, `raw/D2_llama_cpp_README.md` line 62 | ⚠️ no section locator given — see P2-6 |

No paraphrase is presented as a direct quotation. No ellipsis or square-bracket alteration appears anywhere. No quotation is over-long.

---

## 9. Tables, captions and appendix citations

| Check | Result |
|---|---|
| Every table named in the body text | ✅ **15 / 15**, each referenced 2–5 times |
| Table numbering consistent with captions and list of tables | ✅ 15 captions, 15 static list entries, page numbers verified against the render |
| Tables built from this study's own data carrying invented external sources | ✅ none — Tables 3.1, 3.5, 3.7, 3.8, 4.1–4.10 and 6.1 carry no external attribution, correctly |
| Table 4.10 (privacy comparison) sourcing | ✅ the cloud column cites ICO, GDPR Art. 5, OWASP, Zeng, Huang and Anderson in the cells; the local column is described in the surrounding text as the observed architecture. The distinction between measured and published is stated explicitly in §4.9 |
| Table 3.7, Table 4.9 in-text pointers added earlier | ✅ still present: Table 3.7 referenced 3 times, Table 4.9 referenced 3 times |
| Appendices A–J each referenced from the body | ✅ **10 / 10** |
| Appendix citations also present in the reference list | ✅ Appendix B names Lewis et al. (2020), ggml-org (n.d.b), Tabassi (2023) and Information Commissioner's Office (n.d.a) — all four are in the list |
| Appendix E/F rubric and rater instructions | ✅ authored for this study; §3.6.1 states the rubric was "informed by RAG evaluation literature, including RAGAS, but this study used its own transparent 0–5 rubric rather than calculating RAGAS scores directly" — the boundary is correct |
| Appendix A model manifest | ✅ model cards cited in §3.3; SHA-256 provenance is this study's own verification, correctly not attributed to an external source |

---

## 10. Citation density and source quality by chapter

| Chapter | Density | Assessment |
|---|---|---|
| Ch 1 | 22 instances, 10 sources | Appropriate for a background and gap chapter. Two of the three gap sentences carry the PARTIAL pattern (C-23, C-24) and one carries the MISMATCH (C-25) |
| Ch 2 | 45 instances, 23 sources | Highest density, correctly. **This is critical synthesis, not a paper-by-paper summary.** §2.7 organises the field into three strands, then states specifically what is missing — wrong hardware class, wrong metric (total model bits and zero-shot accuracy), no joint evaluation — rather than resting on "these topics are usually studied separately". Multiple sections state explicitly where a source does not transfer to a CPU-based pipeline. No single source or institution dominates: the largest share is the ICO's two documents at 19 of 113 instances, and those carry the data-protection strand alone |
| Ch 3 | 15 instances, **15 sources** | One citation per source — every citation identifies a specific artefact (model card, embedding, reranker, corpus document, baseline repository, rubric provenance). No source is carrying multiple unrelated claims |
| Ch 4 | 17 instances, 7 sources | Concentrated in §4.9. Correct: this is the only part of the results chapter that reports something not measured in this study, and it says so |
| Ch 5 | 2 instances, 2 sources | Low by design. Chapter 5 interprets this study's own results; the literature link is Chapter 6's job. The two citations present (MobileLLM, llama.cpp) are both used to mark a boundary rather than to support a finding. **This is defensible but is the one place a marker might expect more** — see "author decisions" |
| Ch 6 | 11 instances, 10 sources | Correct shape for a discussion chapter: nearly one source per claim, each used to relate a finding to prior work and then bounded |
| Ch 7 | 0 | Correct — no new literature in the conclusion |

**Unsupported external factual claims:** none found. Paragraphs stating facts about the world outside this experiment carry citations; paragraphs stating this study's observations do not, which is the correct division.

**One source carrying too many different claims:** none. The most-used source, ICO n.d.a, carries a single strand (data-protection obligations around data flow, storage, access control and retention) across its 11 uses.

**Sources that should be swapped for the original paper:** none. Where a survey is cited (Gao et al. 2023, Fan et al. 2024) it is cited for a survey-level statement, and the primary papers (Lewis, Reimers, Nogueira, Frantar, Lin, Liu, Dettmers) are cited directly for their own findings.

---

## 11. Issues by severity

### P0 — none

No fabricated source, no mismatched reference entry, no missing entry, and no key conclusion resting on an unsupported citation.

### P1

**P1-1 — Citation placement error in §1.3.** A four-source bundle sits at the end of a three-sentence block and attaches grammatically to the third sentence only. Es et al. (2024) and Dettmers and Zettlemoyer (2023) do not support "on-device model deployment, client-side retrieval, and the privacy risks associated with cloud AI and RAG". The two preceding sentences — one about RAG evaluation, one about quantisation — carry no citation at all, and those are exactly the sentences the two misplaced sources do support. No source is given for on-device deployment even though Liu et al. (2024) is in the list and used for that purpose in §2.5.

**P1-2 — Anderson et al. verified against the preprint, not the cited version.** The reference entry cites ICISSP 2025, pp. 474–485, DOI `10.5220/0013108300003899`, and Crossref confirms every field. However the locally stored full text (`wave2_sources/S57_Anderson_2024_RAG_Membership_Inference.txt`) contains no occurrence of "ICISSP" or "SciTePress" and is the earlier preprint. The claim drawn from it ("defensive instructions reduce risk rather than remove it") is supported by the preprint wording. Whether the published version words it identically is **UNVERIFIED**. This is the only reference in the list where the version read differs from the version cited.

### P2

**P2-1 — Grouped citations follow no consistent order.** 20 parentheses, at least three different orders in use. Rule to be confirmed against Cite Them Right Online.

**P2-2 — Three conference papers located by arXiv URL** while three comparable entries use the official proceedings URL.

**P2-3 — NIST (2024) AI 600-1 has a Crossref DOI** (`10.6028/NIST.AI.600-1`) not carried in the entry.

**P2-4 — Zheng et al. (2023) has a NeurIPS proceedings DOI** (`10.52202/075280-2020`) not carried in the entry.

**P2-5 — Appendix A.2 contains `(X-Linked-ETag, read 13 August 2026)`**, which reads like a Harvard citation but is a technical note about an HTTP header. Recasting it as prose would remove the ambiguity.

**P2-6 — Two appendix quotations lack a locator.** The ICO and llama.cpp quotations are verbatim and the documents are named, but neither gives a section heading. Both sources are HTML/Markdown without page numbers, so Cite Them Right expects a section or paragraph locator: the ICO passage sits under "How should we assess security and data minimisation in AI?"; the llama.cpp passage is the opening line of the README's description section.

**P2-7 — NIST documents split between personal and corporate author.** `Tabassi, E. (2023)` for AI RMF 1.0 and `NIST (2020)` / `NIST (2024)` for the other two. **Both are correct** — Crossref shows a personal author for the first and none for the others — but a reader looking for the AI RMF under "N" will not find it, and §2.6 makes the split visible in one parenthesis: `(Tabassi, 2023; NIST, 2020, 2024)`.

---

## 12. Suggested changes

Nothing here has been applied. Each is the minimum edit that resolves the finding.

| # | Where | Change | Words |
|---|---|---|---:|
| 1 | §1.3 sentences 1–3 | Distribute the bundle: put `(Lewis et al., 2020; Es et al., 2024)` on the RAG-evaluation sentence, `(Frantar et al., 2023; Dettmers and Zettlemoyer, 2023)` on the quantisation sentence, and leave `(Liu et al., 2024; Wang and Chau, 2024; Information Commissioner's Office, n.d.a)` on the third | ≈ +8 |
| 2 | §1.1, §1.3 | Optional: reword the two PARTIAL gap sentences so the citation supports the premise rather than the inference — e.g. "…which those sources examine separately" instead of citing them for the gap itself | ≈ +6 |
| 3 | 20 parentheses | Apply one ordering rule throughout, once the Cite Them Right rule is confirmed | 0 |
| 4 | Frantar, Liu, Zheng entries | Replace the arXiv URLs with the OpenReview / PMLR / NeurIPS proceedings URLs | 0 |
| 5 | NIST (2024), Zheng (2023) | Add the two available DOIs | ≈ +6 |
| 6 | Appendix A.2 | Recast the `(X-Linked-ETag, read 13 August 2026)` parenthesis as prose | ≈ +4 |
| 7 | Appendix J.4, J.5 | Add a section locator to each quotation | ≈ +12 |
| 8 | Reference list | Optional: add a see-reference from NIST to Tabassi for AI RMF 1.0, or leave as is | ≈ +8 |

Total if all applied: about +44 words to the body (items 1, 2, 5) and the rest in the appendices, which are not counted. Current body count is 16,461 against a 16,000 limit; the penalty threshold is more than 10% over, i.e. 17,600.

---

## 13. Items needing the author or supervisor to decide

1. **The Cite Them Right rule for ordering grouped citations.** Cite Them Right Online is subscription-gated and could not be read from here. The author has Warwick access. Until confirmed, item 3 above cannot be applied correctly.
2. **Whether to obtain the published Anderson et al. (2025) text.** The metadata is confirmed. Reading the SciTePress version would convert P1-2 from UNVERIFIED to verified. If it cannot be obtained, the honest position is that the claim rests on the preprint, and that should be stated nowhere in the body — it changes nothing about the claim's accuracy.
3. **Whether Chapter 5's two citations are enough.** The division of labour (Chapter 5 interprets own results, Chapter 6 relates to literature) is deliberate and defensible. A second marker may still expect more. This is a judgement about presentation, not a citation error.
4. **Whether to switch NIST AI RMF 1.0 to a corporate author** for consistency with the other two NIST entries, at the cost of departing from the record's own attribution.
5. **The 2024/25 marking grid applies to a 2025/26 submission.** Criterion 3, "Critically evaluate the context of the research, synthesising ideas from a referenced review of relevant source material", carries 20%. The audit finds Chapter 2 meets it. If the 2025/26 grid differs, that assessment should be rechecked.

---

## 14. Statements this audit can make

- No source in the reference list was fabricated. All 33 were traced to a primary record.
- No page number, DOI, publication place, version or access date was invented during this audit, and none in the reference list was found to be wrong.
- No GitHub project is described as peer-reviewed research. `Wang (2025)` and the three `ggml-org` entries are labelled *GitHub repository*; §3.2 describes the baseline as a repository that was adapted, not as a study.
- No observation from this experiment is presented as a conclusion from the literature.
- No general finding from the literature is extended to this study's Windows laptop, CPU-only inference and fixed RAG pipeline without an explicit boundary statement.
- The five reference theses were used for structure and expression only and appear nowhere in the citation apparatus.
