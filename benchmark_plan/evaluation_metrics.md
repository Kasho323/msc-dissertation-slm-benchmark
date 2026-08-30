# Evaluation Metrics

Every claim in the dissertation should be tied to a measurement or a clearly cited analytical comparison. This file defines the benchmark metrics.

## A. Quality Metrics

Use the same fixed question set for every model configuration. The recommended size is **30-40 questions**, with **50** as the upper limit if runtime is clearly manageable.

Each generated answer should be scored against the same rubric. A 0-5 scale is simple enough for manual checking and detailed enough for comparison:

- 0 = absent or unusable
- 1 = very poor
- 2 = weak
- 3 = acceptable
- 4 = good
- 5 = excellent

### A1. Relevance

Does the answer address the question that was asked?

### A2. Correctness

Is the answer factually correct when compared with the reference answer or source document?

### A3. Faithfulness to Source

Are the claims supported by the retrieved source context?

### A4. Completeness

Does the answer include the important parts of the expected answer, rather than only a fragment?

### A5. Hallucination Risk

Does the answer invent unsupported facts, details, citations, or explanations?

For scoring consistency, use the same 0-5 scale but interpret higher as better:

- 5 = no hallucination observed
- 0 = severe unsupported claims

### A6. Citation or Source Grounding

Does the answer clearly connect its claims to the retrieved source material?

This can be scored by checking whether the answer uses source-specific evidence, references the relevant passage, or stays visibly grounded in the provided context.

## B. Optional Automated Metrics

If the chosen dataset has reference answers, compute exact match or token-level F1 as a sanity check.

If RAGAS or a similar framework is used, treat it as a supporting automated evaluation rather than the whole quality story. The dissertation should still explain the rubric above, because answer quality must be concrete and inspectable.

## C. Human or Manual Validation

At minimum, manually inspect a stratified sample of answers across configurations.

Possible sample:

- 5-10 questions per configuration, or
- all answers if the final set is only 30 questions and time allows.

If only the student scores the answers, report this honestly as single-rater rubric scoring. Do not claim inter-rater reliability unless a second rater is actually used.

## D. System Metrics

Collect the same system metrics for every configuration.

### D1. Latency

Time from request submission to completed answer. If streaming is implemented, also record time-to-first-token.

Unit: milliseconds or seconds.

### D2. Throughput

Generated tokens per second.

### D3. Peak Memory

Peak resident memory used by the model-serving process during inference.

Unit: MiB or GiB.

### D4. Model Size

Size of the quantised model file on disk.

### D5. Deployment Notes

Record setup friction, runtime compatibility, crashes, context length limits, and any model-specific problems. These notes support the deployment-feasibility discussion.

## E. Privacy Analysis

Privacy should be treated as a structured analytical comparison, not a simple claim that local models are automatically safe.

Core statement:

> Local models avoid sending queries and documents to external cloud APIs, but privacy still depends on local storage, logs, access control, backups, and device security.

Use a table like this:

| Dimension | Local Model Workflow | Cloud LLM Workflow |
|---|---|---|
| Do questions leave the device? | Usually no external API transfer | Usually sent to provider API |
| Do source documents leave the device? | Usually remain local | May be uploaded or embedded by provider |
| Local storage risk | Vector DB, cached files, logs, and results need protection | Local copies may still exist, plus provider-side data |
| Logs and retention | Depends on app logging and OS backups | Depends on provider policy and account settings |
| Access control | Depends on laptop user accounts and file permissions | Depends on provider account, organisation controls, and API keys |
| Device compromise | Local compromise can expose all data and models | Cloud workflow still has local endpoint and credential risks |
| Offline use | Possible after setup | Usually requires network access |
| Regulatory discussion | Needs GDPR-aware handling of local personal data | Needs GDPR-aware handling of third-party processing |

Each row should be supported with literature, provider documentation, or a security/privacy framework.

## F. Reporting Format

Recommended final outputs:

- Table T1: quality rubric scores by configuration.
- Table T2: latency, throughput, peak memory, and model size by configuration.
- Table T3: Qwen2.5 1.5B Q2 vs Q4 vs Q8 comparison.
- Figure F1: quality vs speed or quality vs memory scatter plot.
- Table T4: privacy comparison matrix.

The conclusion should avoid absolute claims. A good final recommendation sounds like: "If the priority is X, choose Y; if the constraint is Z, choose W."
