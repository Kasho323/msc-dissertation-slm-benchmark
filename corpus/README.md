# Frozen retrieval corpus

These are the four inputs used in the final 24 June 2026 benchmark, not an
updated collection of web pages. `manifest.json` records their exact SHA-256
checksums and original URLs. Run `python reproduction/prepare_corpus.py` from
the repository root. It downloads D1 and verifies all four files, refusing any
checksum mismatch. No certificate-verification bypass is used.

- **D1:** Lewis et al., *Retrieval-Augmented Generation for Knowledge-Intensive
  NLP Tasks*. Not redistributed here. The arXiv **v4** PDF was downloaded on
  18 September 2026 and matched the retained benchmark PDF byte for byte.
- **D2:** A text-only rendering of the retained llama.cpp README snapshot.
  Distributed with the ggml authors' MIT notice in `llama.cpp-LICENSE.txt`.
  This is the historical PDF, not a rendering of today's `master` README.
  [Licence source](https://github.com/ggml-org/llama.cpp/blob/d2e22ed97/LICENSE).
- **D3:** NIST, *Artificial Intelligence Risk Management Framework (AI RMF
  1.0)*, January 2023, NIST AI 100-1, DOI 10.6028/NIST.AI.100-1. Unmodified
  retained publication. The official download returned HTTP 403 during the
  release check, so the retained copy is included. NIST permits copying and
  distribution of its public information unless marked otherwise:
  [NIST copyright notice](https://www.nist.gov/copyrights-disclaimers).
  No NIST endorsement is implied.
- **D4:** Information Commissioner's Office, *Guidance on AI and Data
  Protection — Selected Chapters*, publication date not reliably established;
  text snapshot retained before the 24 June 2026 benchmark, licensed under the
  [Open Government Licence v3.0](https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/).
  This is a research-generated text-only PDF, not an ICO-issued publication.
  The five underlying official URLs are recorded in `manifest.json`.
  [ICO reuse terms](https://ico.org.uk/global/copyright-and-re-use-of-materials/),
  checked 18 September 2026. No ICO logos/images are included. No endorsement
  is implied. The snapshot is historical evidence, not current legal guidance.

The original acquisition/conversion code is retained as
`benchmark_plan/prepare_final_corpus.py` for provenance. That dated script
fetches dynamic sources and is **not** the restoration entry point: running
it today would produce a different corpus. Use the checksum-verified PDFs
above for replication. PDF-to-text cleaning and splitting are performed by
the pinned upstream `rag_pipeline.py` as documented in the reproduction guide.
