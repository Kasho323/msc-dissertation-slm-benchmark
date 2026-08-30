# Final Corpus Validation

**Date:** 2026-06-19  
**Corpus folder:** `docs/final_benchmark_corpus/`

## Purpose

This check confirms that the final benchmark corpus is upload-ready for the existing RAG app, which only accepts PDF files and loads them with `PyPDFLoader`.

## Files

| Source ID | PDF | Pages Loaded by PyPDFLoader | Extracted Characters |
|---|---|---:|---:|
| D1 | `D1_RAG_Lewis_2020.pdf` | 19 | 69080 |
| D2 | `D2_llama_cpp_README.pdf` | 16 | 17089 |
| D3 | `D3_NIST_AI_RMF_1_0.pdf` | 48 | 106449 |
| D4 | `D4_ICO_AI_Data_Protection_Guidance.pdf` | 26 | 91781 |

## Result

All four PDFs loaded successfully with the same Python environment used by `Jetson-Nano-RAG-LLM`.

The corpus is ready for upload into the RAG backend after the backend is started.

## Backend Upload Smoke Test

After starting the local RAG stack with `start_all.ps1`, the four PDFs were uploaded to:

`http://127.0.0.1:8000/upload`

Backend response:

```json
{"message":"4 PDFs uploaded and processed."}
```

A smoke-test question was then sent to the RAG endpoint:

> What problem does retrieval-augmented generation try to address in knowledge-intensive NLP tasks?

The endpoint returned a non-empty answer and cited:

`./uploads/D1_RAG_Lewis_2020.pdf`

This confirms that the final corpus can be uploaded, embedded, retrieved, and used for generation by the existing backend.

## Notes

- `Jackie_report.pdf` remains a pilot document only.
- D2 and D4 were generated from public Markdown/HTML sources because the existing app only accepts PDFs.
- Raw source HTML/Markdown is stored in `docs/final_benchmark_corpus/raw/`.
- Visual previews were generated for D2 and D4 to confirm the generated PDFs are readable.
