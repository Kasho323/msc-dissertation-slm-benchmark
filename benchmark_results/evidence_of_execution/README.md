# Evidence of execution

The supervisor asked on 27 August 2026 for evidence in the appendix that the
retained code runs, so that the second examiner can confirm the work was
carried out. This folder holds that evidence. It supports Appendix K.4.

Nothing here is reconstructed, re-drawn or edited. The three images are screen
captures taken by the author while the system was running; the two logs are the
unmodified console output of the two server processes.

## The captured session, 2 September 2026

Three processes were started in order, on the machine described in Section 3.7:

    llama-server.exe -m models/gemma-3-1b-it.Q4_K_M.gguf --port 8080
        --ctx-size 4096 --parallel 1 --cache-ram 0 --no-cache-prompt
        --ctx-checkpoints 0 --seed 42

    python -m uvicorn main:app --host 127.0.0.1 --port 8000

    python -m streamlit run app.py

The four corpus documents D1-D4 were then indexed through the interface and
question Q001 of the frozen question set was submitted. Retrieval and generation
settings were set to the values recorded in the 24 June 2026 C3 run manifest:
k = 10, n = 3, max_tokens = 512, temperature 0.2.

| File | What it is |
|---|---|
| `K1_settings_and_corpus.png` | The interface after the four corpus documents were indexed, showing the settings in force |
| `K2_answer_and_provenance.png` | The answer to Q001 with its retrieved sources and page numbers |
| `K3_backend_console.png` | The retrieval backend console for the same request |

## Retained from an earlier run, 30 August 2026

These three files come from a separate run of the same flow on 30 August 2026,
kept because they are machine-written rather than photographed.

| File | What it is |
|---|---|
| `llama_server_console.log` | Console output of the generation server |
| `backend_console.log` | Console output of the retrieval backend |
| `rag_response.json` | The unmodified API response from that run |

## What this does and does not show

It shows that the retained system loads its models from local files, indexes
the corpus, retrieves passages, reranks them, and returns an answer with
page-level provenance.

It is **not** a second measurement of the performance reported in Chapter 4:
one query on one question is not the mean over forty questions and three
repetitions under the controlled protocol of Section 3.7. The two quantities
that can be compared are nonetheless close. Throughput in the 2 September
session was 67.65 tokens per second against the 67.15 reported for C3 in
Table 4.3, and process memory 0.98 GB against 1001.06 MiB. The 30 August run,
made while other work was on the machine, gave 43.85 tokens per second and the
same 0.98 GB, which is the expected pattern: memory is stable, throughput
follows machine load.

## Two things worth noting

**The runtime is the same build as the original experiment.** Both runs record
`system_fingerprint: b9587-d2e22ed97`, which is the `runtime_version` in the
24 June 2026 C3 run manifest.

**Retrieval is deterministic.** Six runs across 30 August and 2 September 2026,
through both the HTTP interface and the browser and at temperatures 0.0 and
0.2, all returned the same three passages for Q001: chunks 0, 148 and 75 of
D1_RAG_Lewis_2020.pdf, on pages 1, 17 and 8. This is the property that allows
retrieval to be held constant while only the generation model varies, which is
the design stated in Section 3.2.
