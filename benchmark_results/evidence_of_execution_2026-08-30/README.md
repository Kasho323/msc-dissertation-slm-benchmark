# Evidence of execution — 30 August 2026

The supervisor asked on 27 August 2026 for evidence in the appendix that the
retained code runs, so that the second examiner can confirm the work was
carried out. This folder holds that evidence.

Everything here was produced in a **single continuous session** on 30 August
2026 on the machine described in Section 3.7. Nothing is reconstructed,
re-drawn or edited; the two images are screen captures of the live application
taken by a real browser, and the two logs are the unmodified console output of
the two server processes.

## What was run

Three processes, in this order:

    llama-server.exe -m models/gemma-3-1b-it.Q4_K_M.gguf --port 8080
        --ctx-size 4096 --parallel 1 --cache-ram 0 --no-cache-prompt
        --ctx-checkpoints 0 --seed 42

    python -m uvicorn main:app --host 127.0.0.1 --port 8000

    python -m streamlit run app.py

The four corpus documents D1-D4 were then uploaded through the interface and
question Q001 of the frozen question set was submitted. Retrieval and
generation settings were set to the values recorded in the 24 June 2026 C3 run
manifest: k = 10, n = 3, max_tokens = 512, temperature = 0.2.

## Files

| File | What it is |
|---|---|
| `K1_settings_and_corpus.png` | The interface after the four corpus documents were indexed, showing the settings in force |
| `K2_answer_and_provenance.png` | The answer to Q001 with its retrieved sources and page numbers |
| `llama_server_console.log` | Console output of the generation server |
| `backend_console.log` | Console output of the retrieval backend |
| `rag_response.json` | The unmodified API response behind the second image |

## What this does and does not show

It shows that the retained system loads its models locally, indexes the corpus,
retrieves passages, and returns an answer with page-level provenance.

It is **not** a re-measurement of the performance reported in Chapter 4. The
throughput printed here (43.9 tokens per second) comes from one ad-hoc query on
a machine running other work; the 67.15 tokens per second reported for C3 in
Table 4.3 is the mean over 40 questions and three repetitions under the
controlled protocol of Section 3.7. Process memory, which is far less sensitive
to load, does agree: 0.97 GB here against 1001.06 MiB in Table 4.3.

## Two things worth noting

**The runtime is the same build as the original experiment.** The response
records `system_fingerprint: b9587-d2e22ed97`, which is the `runtime_version`
recorded in the 24 June 2026 C3 run manifest.

**Retrieval is deterministic.** Five independent runs on 30 August 2026 — one
through the HTTP API and four through the interface, at temperatures 0.0 and 0.2
— all returned the same three passages for Q001: chunks 0, 148 and 75 of
D1_RAG_Lewis_2020.pdf, on pages 1, 17 and 8. This is the property that allows
retrieval to be held constant while only the generation model varies, which is
the design stated in Section 3.2.
