# Chapter 2 Reading and Writing Plan

Date: 11 August 2026  
Status: active control file for the Literature Review  
Target length: 2,800-3,400 words

## 1. Purpose

This file controls the next stage of Chapter 2. The existence check in `REFERENCE_VERIFICATION_REPORT_2026-08-09.md` confirmed that all 63 non-thesis candidate sources are real. That check does not establish that every source supports a particular sentence in the dissertation. A source may only be cited after its relevant section has been read and its support for the claim has been recorded.

The Literature Review must be a thematic and critical synthesis. It must not become a sequence of one-paper summaries, and the five example dissertations must not be used as evidence for technical claims.

## 2. Non-negotiable rules

1. Prefer original research papers, official model documentation and authoritative institutional guidance.
2. Record the exact page, section, table or passage supporting each retained claim.
3. Separate what a source directly reports from what is inferred for this dissertation.
4. Compare sources within each theme: agreements, differences in method, limits and relevance to this project.
5. Do not use phrases such as "no one has studied" or "all existing work" unless a systematic search can support them.
6. Use cautious gap language such as "limited evidence is available", "few reviewed studies jointly examine", or "this combination remains underexplored".
7. Build the Harvard reference entry only after deciding that the source is actually cited.
8. The final Reference List contains only works cited in the dissertation. Candidate count is not a target to be padded.
9. Sources S64-S68 are for presentation and structure study only; they do not establish technical facts.
10. The baseline repository P01 is a project artefact, not a peer-reviewed academic source.

## 3. Proposed Chapter 2 structure

| Section | Working title | Main purpose | Target words |
|---|---|---|---:|
| 2.1 | Chapter introduction | Define the review scope and the five connected themes | about 150 |
| 2.2 | RAG and retrieval for document question answering | Explain retrieval, grounding, embeddings and reranking; establish what is fixed in this study | 450-550 |
| 2.3 | Evaluating RAG answers and using LLMs as judges | Compare RAG evaluation frameworks, rubric scoring, human validation and known rater biases | 550-650 |
| 2.4 | Quantisation and controlled precision trade-offs | Compare post-training quantisation approaches and explain why Q2/Q4/Q8 must be tested rather than assumed | 550-650 |
| 2.5 | Small models and on-device deployment | Review practical local inference, compact models, llama.cpp and ordinary-device constraints | 350-450 |
| 2.6 | Privacy and security in local and cloud RAG workflows | Distinguish reduced external transmission from complete security; compare data-flow and residual risks | 500-600 |
| 2.7 | Synthesis, applied research gap and chapter summary | Join the themes, state the bounded gap and lead into the Methodology | 250-350 |
|  | Total |  | 2,800-3,400 |

The section numbers are provisional until they are placed in the official dissertation document. The thematic order is the controlling structure.

## 4. Core argument by section

### 2.1 Chapter introduction

Establish that the review connects five bodies of work: RAG, answer evaluation, quantisation, on-device inference, and privacy/security. State that the purpose is to derive the benchmark design and identify the applied gap, not to catalogue every local language model.

### 2.2 RAG and retrieval for document question answering

Questions to answer:

- What problem does RAG address, and how does retrieved context ground generation?
- What roles do embeddings and reranking play in document retrieval?
- Which parts of a RAG pipeline can affect answer quality independently of the generator?
- Why must retrieval be held fixed when generator configurations are compared?

Core sources: S01, S05, S06, S08 and S09.  
Supporting implementation source: S33 only where the runtime implementation is discussed.

Critical synthesis required:

- Compare foundational RAG with later taxonomies rather than repeating definitions.
- Distinguish retrieval quality from generation quality.
- End by explaining why this dissertation reuses one fixed retrieval pipeline across all six configurations.

### 2.3 Evaluating RAG answers and using LLMs as judges

Questions to answer:

- Which answer properties are measured by RAG evaluation frameworks?
- What is gained and lost when an LLM performs rubric-based evaluation?
- Why is an independently scored human sample useful?
- Which known position, verbosity, self-preference or judgement biases limit an AI rater?
- Why does agreement with a human sample support the scoring procedure without proving the final model ranking?

Core sources: S13, S14, S15, S18, S19, S20 and S21.  
Supporting benchmark source: S16.

Critical synthesis required:

- Compare automated evaluation frameworks by their inputs, dimensions, validation data and limitations.
- Do not present RAGAS dimensions as identical to this dissertation's six-dimension rubric; identify what was borrowed and what was adapted.
- Use the bias literature to justify blinding and independent human validation.
- Keep Spearman and agreement-statistic details mainly in Methodology; Chapter 2 only establishes why validation is needed.

### 2.4 Quantisation and controlled precision trade-offs

Questions to answer:

- How does post-training quantisation reduce model storage and memory requirements?
- What accuracy or output-quality risks can lower precision introduce?
- Why is four-bit precision often practical but not guaranteed to be best for every model and task?
- How do existing methods differ from the llama.cpp Q2_K, Q4_K_M and Q8_0 comparison used here?

Core sources: S27, S28, S29, S30 and S31.  
Implementation terminology: S34 and S35.

Critical synthesis required:

- Compare methods, hardware assumptions, model scales and evaluation tasks.
- Do not transfer GPU results on large models directly to a small CPU-based RAG system without stating the limitation.
- Distinguish general quantisation evidence from the exact GGUF quantisation types tested in this project.
- Lead to the controlled Qwen2.5 1.5B sub-study, where model, questions, retrieval and generation settings remain fixed.

### 2.5 Small models and on-device deployment

Questions to answer:

- What evidence supports the feasibility of compact models on personal or mobile hardware?
- What practical constraints remain, including model size, memory, speed and runtime support?
- How does this dissertation's laptop setting differ from mobile-device or GPU studies?

Core sources: S30, S33, S35, S36 and S56.  
Model-specific sources S37-S42 should be used only for exact model facts, not broad claims about on-device AI.

Critical synthesis required:

- Separate feasibility from suitability: running locally does not establish acceptable answer quality.
- Compare the hardware and task settings used by prior work with the single-laptop RAG benchmark in this dissertation.

### 2.6 Privacy and security in local and cloud RAG workflows

Questions to answer:

- Which privacy risks arise when questions, documents, embeddings or logs are handled by an external provider?
- Which external data transfers are avoided by the tested local workflow?
- Which risks remain locally, including device compromise, insecure dependencies, prompt injection, retrieval-store leakage and backups?
- Why is local processing a data-flow advantage rather than proof of complete security?

Core sources: S46, S47, S48, S49, S50, S51, S53, S54, S55, S56 and S57.

Critical synthesis required:

- Separate legal/data-protection principles from empirical security research.
- Distinguish cloud-provider guidance from measurements made in this study; no cloud service was empirically benchmarked.
- Contrast client-side retrieval motivation with attacks that remain possible in RAG systems.
- End with the dimensions used by the structured privacy comparison in Chapters 3 and 4.

### 2.7 Synthesis, applied research gap and chapter summary

The synthesis should connect the themes rather than introduce new literature. A cautious working formulation is:

> The reviewed literature provides separate evidence on RAG design, automated answer evaluation, model quantisation, on-device inference and privacy risk. However, limited evidence jointly examines these factors under one fixed RAG workflow on an ordinary laptop, while combining a controlled Q2/Q4/Q8 comparison with answer-quality, latency, throughput, observed process RSS and model-file-size measurements. This combination remains underexplored and motivates the benchmark developed in this dissertation.

This wording remains provisional until the core reading notes confirm each part. The final paragraph should connect the gap directly to the research question and Methodology.

## 4a. Time budget and realistic depth of reading

Submission is 12:00 on 2 September 2026, and Chapters 5, 6 and 7 are still unwritten. Reading every candidate source to the depth of the full evidence-note template would take longer than the time available, so depth is allocated by how much argumentative weight a source carries:

| Depth | Which sources | What is read | Note produced |
|---|---|---|---|
| **Full note** | The six Wave 1 anchors, plus any source used to justify a design decision (roughly 12–15 in total) | Abstract, method, the specific result relied on, and the stated limitations | Complete evidence-note template |
| **Targeted note** | Most Wave 2 sources | Abstract plus only the section containing the claim being cited | Claim, exact location, one-line paraphrase, keep/drop |
| **Fact check only** | Model cards, official documentation, standards and legal texts (S33–S35, S37–S53) | The specific figure, setting or clause being cited | The value cited and where it appears |

A source that cannot be given at least a targeted note should not be cited. It is better to cite thirty sources that have genuinely been read than sixty that have not.

**Suggested pacing:** Wave 1 in one working session; each theme in Section 2.2–2.6 in one session (reading and drafting together, theme by theme); Section 2.7 last. This keeps Chapter 2 to roughly a week and protects the time needed for Chapters 5–7.

## 4b. Relationship to the rest of the dissertation

- The target of 55–70 references is for the **whole dissertation**, not for Chapter 2 alone. Chapter 2 carries the largest share, but Chapters 1, 3, 5 and 6 also cite. At 2,800–3,400 words, Chapter 2 can support roughly 30–45 sources discussed with real substance; the remainder appear elsewhere. Do not compress extra citations into Chapter 2 to reach a number.
- Wave 2 reading on evaluation, quantisation and privacy also supplies **Chapter 6 (Discussion)**, where findings are related back to previous research. Notes should therefore record which chapter each claim is intended for, as the evidence-note template already provides.

## 4c. Resolving the existing [CITE] markers

Chapters 1, 3 and 4 already contain 20 `[CITE:Sxx]` markers, and the supervisor draft states that every reference is being verified before the final reference list is built. Each marker must be closed out as part of this stage, not left to the end:

1. Read the source section that the marker points to.
2. Confirm it supports the sentence it is attached to; if it does not, change the source or soften the sentence.
3. Replace the marker with the Harvard in-text citation.
4. Add the entry to the reference list only at that point.

Markers to close: Chapter 1 (S08, S13, S14, S28, S29, S30, S49, S50, S56 and the research-methods source still to be chosen for the research-philosophy section), Chapter 3 (P01, S01, S06, S13, S18, S33, S44, S45, S46, S49, and the model sources S37–S42), Chapter 4 (S49, S50, S51, S53, S54, S55, S57).

## 5. Reading waves

### Wave 1: six anchor sources

Read these first and complete a full evidence note for each before drafting prose:

1. S01 Lewis et al. (2020): foundational RAG mechanism and motivation.
2. S13 Es et al. (2024): RAGAS dimensions and automated RAG evaluation.
3. S18 Zheng et al. (2023): LLM-as-a-judge method and known biases.
4. S29 Dettmers and Zettlemoyer (2023): four-bit precision trade-off.
5. S30 Lin et al. (2024): activation-aware low-bit quantisation and deployment trade-offs.
6. S56 Wang and Chau (2024): client-side retrieval and privacy motivation.

Deliverable: six completed evidence notes and a one-page cross-source comparison. No final Chapter 2 prose is written before this deliverable is checked.

### Wave 2: complete each theme

Read selectively but directly from the original sources:

- RAG and retrieval: S05, S06, S08, S09.
- Evaluation: S14, S15, S16, S19, S20, S21.
- Quantisation and local inference: S27, S28, S31, S33, S34, S35, S36.
- Privacy and security: S46, S47, S48, S49, S50, S51, S53, S54, S55, S57.

Deliverable: a claim-evidence map for Sections 2.2-2.6 and a keep/drop decision for every read source.

### Wave 3: targeted factual and methodological support

- S37-S45: exact model, embedding and reranker facts; primarily Methodology.
- S58-S63: statistics, agreement and reproducibility; primarily Methodology and limitations.
- P01: baseline code provenance; project artefact, not literature evidence.
- Remaining medium/optional sources: read only when they fill a documented gap in the argument.

## 6. Evidence-note template

Create one note per source using this structure:

```text
S-code:
Verified Harvard metadata:
Permanent URL or DOI:
Date accessed (web sources only):
Section/page/table read:
Research problem:
Method, data and hardware:
Finding directly reported by the source:
Limitation stated by the source:
Limitation identified for this dissertation's setting:
Exact claim this source can support:
Safe paraphrase in my own words:
Planned dissertation section:
Comparison or disagreement with another source:
Keep / background only / drop:
```

Do not record only the abstract. For a retained source, read the method, relevant result and limitations sections needed for the intended claim.

## 7. Claim-evidence control

Before drafting each subsection, build a small table with these columns:

| Claim ID | Planned claim | Supporting S-code(s) | Exact location checked | Agreement/contrast | Safe to draft? |
|---|---|---|---|---|---|

A claim is safe to draft only when the supporting location has been checked. An existing `[CITE:Sxx]` marker is a pointer to investigate, not proof that the citation is suitable.

## 8. Critical synthesis pattern

Use paragraphs that compare evidence:

1. Topic sentence stating the issue.
2. Evidence from two or more relevant sources.
3. Comparison of methods, assumptions or findings.
4. Limitation for this dissertation's hardware, model scale or task.
5. Design implication or transition to the applied gap.

Useful pattern:

> Source A establishes [...], while Source B extends this by [...]. However, both evaluate [...], which limits direct transfer to [...]. This dissertation therefore fixes/records/compares [...] in order to [...].

Avoid a catalogue pattern such as "A says..., B says..., C says...".

## 9. Metadata decisions still open

These do not block Wave 1 reading, but they must be resolved before the final Harvard Reference List:

1. S04 HNSW: use one consistent publication year, distinguishing 2018 early access from the 2020 formal issue if necessary.
2. S53 OWASP: record the exact title, version and year of the guidance actually used.
3. S51 GDPR: use the permanent ELI link `https://eur-lex.europa.eu/eli/reg/2016/679/oj`.
4. S48 NIST Privacy Framework: use the complete official document title.

## 10. Wave 1 completion record and immediate next action

Wave 1 was completed on 11 August 2026. The original publication pages and PDFs for S01, S13, S18, S29, S30 and S56 were checked, their relevant methods, findings and limitations were read, and a full evidence note was completed for each source.

The controlled outputs are:

1. `wave1_sources/WAVE1_EVIDENCE_NOTES_2026-08-11.md` - six complete evidence notes with verified metadata, exact locations, safe paraphrases, limitations and claim boundaries.
2. `wave1_sources/WAVE1_CLAIM_EVIDENCE_MAP_2026-08-11.md` - fifteen controlled claims, seven unsupported overclaims, and four cross-source synthesis blocks.
3. `wave1_sources/*.pdf` - the six local source PDFs used for the evidence notes.

The provisional applied gap remains intentionally cautious. The six anchors show that RAG, RAG evaluation, LLM judging, low-bit quantisation and client-side retrieval have all been studied, but they do not jointly evaluate the complete combination used in this dissertation. Wave 2 must check closer work before the final gap wording is frozen.

The next working session starts Section 2.2 and proceeds theme by theme. For each theme, read the relevant Wave 2 sources at the depth specified in Section 4a, draft a critical synthesis rather than a paper-by-paper catalogue, and close the matching `[CITE]` markers in Chapters 1, 3 and 4. Use the claim-evidence map as a boundary: claims marked provisional must not be written as established conclusions.
