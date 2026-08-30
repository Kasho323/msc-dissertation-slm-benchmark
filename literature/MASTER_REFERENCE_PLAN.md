# Master Reference Plan

## Status and purpose

This is the shared source-acquisition plan for Codex, Claude, and the student. It is not yet the final Harvard reference list.

The final dissertation should contain approximately **55-70 unique, relevant references**. This target is based on five related theses, whose reference counts were 39, 116, 18, 19, and 103. The target reflects the breadth of this project without copying the scale of a systematic review.

Rules:

1. A source is cited only if it supports a claim actually made in the dissertation.
2. Technical facts should use primary papers or official technical documentation.
3. Privacy and governance claims should use authoritative sources such as NIST, ICO, OWASP, legislation, or the original security research.
4. The five example theses are mainly writing examples. They must not be used to avoid reading an available original source.
5. Final metadata, access dates, capitalisation, and Harvard formatting must be checked before submission.
6. A source marked `metadata-check` must not enter the final bibliography until its bibliographic record has been verified.

## Status labels

- `verified-primary`: a primary publication page or official proceedings record has been checked.
- `official`: an official model, software, standards, regulator, or legal source.
- `metadata-check`: a relevant candidate whose final bibliographic details still need checking.
- `example-only`: a thesis used primarily to study presentation and argument structure.
- `project-artifact`: a code repository or project report used to document the baseline or implementation history; it is not treated as a peer-reviewed academic source.

## A. RAG foundations and retrieval

| ID | Source | Priority | Planned use | Status | Primary/official link |
|---|---|---|---|---|---|
| S01 | Lewis et al. (2020), *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks* | Must | Define RAG and parametric/non-parametric memory | verified-primary | https://proceedings.neurips.cc/paper/2020/hash/6b493230205f780e1bc26945df7481e5-Abstract.html |
| S02 | Karpukhin et al. (2020), *Dense Passage Retrieval for Open-Domain Question Answering* | High | Dense retrieval background | verified-primary | https://aclanthology.org/2020.emnlp-main.550/ |
| S03 | Robertson and Zaragoza (2009), *The Probabilistic Relevance Framework: BM25 and Beyond* | Medium | Sparse-retrieval comparison and terminology | metadata-check | https://doi.org/10.1561/1500000019 |
| S04 | Malkov and Yashunin (2018), *Efficient and Robust Approximate Nearest Neighbor Search Using Hierarchical Navigable Small World Graphs* | Medium | Vector-index background | metadata-check | https://doi.org/10.1109/TPAMI.2018.2889473 |
| S05 | Reimers and Gurevych (2019), *Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks* | Must | Embedding and semantic retrieval rationale | verified-primary | https://aclanthology.org/D19-1410/ |
| S06 | Nogueira and Cho (2019), *Passage Re-ranking with BERT* | Must | Cross-encoder reranking rationale | verified-primary | https://arxiv.org/abs/1901.04085 |
| S07 | Izacard and Grave (2021), *Leveraging Passage Retrieval with Generative Models for Open Domain Question Answering* | Medium | Multi-passage generation context | metadata-check | https://aclanthology.org/2021.eacl-main.74/ |
| S08 | Fan et al. (2024), *A Survey on RAG Meeting LLMs: Towards Retrieval-Augmented Large Language Models* | High | Literature map and RAG taxonomy | verified-primary | https://doi.org/10.1145/3637528.3671470 |
| S09 | Gao et al. (2023), *Retrieval-Augmented Generation for Large Language Models: A Survey* | High | Naive, advanced, and modular RAG terminology | metadata-check | https://arxiv.org/abs/2312.10997 |
| S10 | Asai et al. (2024), *Self-RAG: Learning to Retrieve, Generate, and Critique through Self-Reflection* | Medium | Context for adaptive/advanced RAG; contrast with fixed pipeline | metadata-check | https://openreview.net/forum?id=hSyW5go0v8 |
| S11 | Yan et al. (2024), *Corrective Retrieval Augmented Generation* | Optional | Context for retrieval correction; contrast with fixed pipeline | metadata-check | https://arxiv.org/abs/2401.15884 |
| S12 | Vaswani et al. (2017), *Attention Is All You Need* | Medium | Minimal transformer background only | metadata-check | https://arxiv.org/abs/1706.03762 |

## B. RAG evaluation, answer quality, and LLM-as-a-judge

| ID | Source | Priority | Planned use | Status | Primary/official link |
|---|---|---|---|---|---|
| S13 | Es et al. (2024), *RAGAs: Automated Evaluation of Retrieval Augmented Generation* | Must | Relevance and faithfulness dimensions | verified-primary | https://aclanthology.org/2024.eacl-demo.16/ |
| S14 | Saad-Falcon et al. (2024), *ARES: An Automated Evaluation Framework for Retrieval-Augmented Generation Systems* | High | Human-labelled subset and automated RAG evaluation context | verified-primary | https://aclanthology.org/2024.naacl-long.20/ |
| S15 | Ru et al. (2024), *RAGChecker: A Fine-grained Framework for Diagnosing Retrieval-Augmented Generation* | High | Fine-grained error diagnosis and limits of aggregate scores | metadata-check | https://arxiv.org/abs/2408.08067 |
| S16 | Chen et al. (2024), *Benchmarking Large Language Models in Retrieval-Augmented Generation* | High | RAG robustness and benchmark design | metadata-check | https://arxiv.org/abs/2309.01431 |
| S17 | Lyu et al. (2024), *CRUD-RAG: A Comprehensive Chinese Benchmark for Retrieval-Augmented Generation of Large Language Models* | Optional | RAG task taxonomy and evaluation breadth | metadata-check | https://arxiv.org/abs/2401.17043 |
| S18 | Zheng et al. (2023), *Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena* | Must | Position, verbosity, and self-enhancement biases | verified-primary | https://arxiv.org/abs/2306.05685 |
| S19 | Liu et al. (2023), *G-Eval: NLG Evaluation using GPT-4 with Better Human Alignment* | High | LLM-based rubric scoring context | metadata-check | https://arxiv.org/abs/2303.16634 |
| S20 | Wang et al. (2024), *Large Language Models are not Fair Evaluators* | High | Evaluator bias and calibration limits | metadata-check | https://arxiv.org/abs/2305.17926 |
| S21 | Chen et al. (2024), *Humans or LLMs as the Judge? A Study on Judgement Biases* | High | Bias can affect both human and AI raters | verified-primary | https://arxiv.org/abs/2402.10669 |
| S22 | Fabbri et al. (2021), *SummEval: Re-evaluating Summarization Evaluation* | Medium | Multi-dimensional rubric and human/automatic metric comparison | metadata-check | https://aclanthology.org/2021.tacl-1.24/ |
| S23 | Lin, Hilton and Evans (2022), *TruthfulQA: Measuring How Models Mimic Human Falsehoods* | Medium | Factuality and unsupported-answer context | metadata-check | https://aclanthology.org/2022.acl-long.229/ |
| S24 | Li et al. (2023), *HaluEval: A Large-Scale Hallucination Evaluation Benchmark for Large Language Models* | Medium | Hallucination definition and evaluation context | metadata-check | https://aclanthology.org/2023.emnlp-main.397/ |

Metadata note for S13: the arXiv preprint was first submitted in 2023, but the final citable publication is the EACL 2024 System Demonstrations paper. The final Harvard reference should use Es et al. (2024), pages 150-158, DOI: 10.18653/v1/2024.eacl-demo.16.

## C. Quantisation and local/on-device inference

| ID | Source | Priority | Planned use | Status | Primary/official link |
|---|---|---|---|---|---|
| S25 | Han, Mao and Dally (2016), *Deep Compression* | Medium | General model-compression background | metadata-check | https://arxiv.org/abs/1510.00149 |
| S26 | Jacob et al. (2018), *Quantization and Training of Neural Networks for Efficient Integer-Arithmetic-Only Inference* | Medium | General integer quantisation background | metadata-check | https://openaccess.thecvf.com/content_cvpr_2018/html/Jacob_Quantization_and_Training_CVPR_2018_paper.html |
| S27 | Dettmers et al. (2022), *LLM.int8(): 8-bit Matrix Multiplication for Transformers at Scale* | High | Eight-bit inference and memory reduction context | verified-primary | https://papers.neurips.cc/paper_files/paper/2022/hash/c3ba4962c05c49636d4c6206a97e9c8a-Abstract-Conference.html |
| S28 | Frantar et al. (2023), *GPTQ: Accurate Post-Training Quantization for Generative Pre-trained Transformers* | Must | Post-training low-bit quantisation context | verified-primary | https://arxiv.org/abs/2210.17323 |
| S29 | Dettmers and Zettlemoyer (2023), *The Case for 4-bit Precision: k-bit Inference Scaling Laws* | Must | Explain why 4-bit is a strong controlled condition, without assuming it will always win | verified-primary | https://icml.cc/virtual/2023/poster/23915 |
| S30 | Lin et al. (2024), *AWQ: Activation-aware Weight Quantization for On-Device LLM Compression and Acceleration* | High | Low-bit on-device deployment and accuracy/efficiency trade-off | verified-primary | https://proceedings.mlsys.org/paper_files/paper/2024/hash/42a452cbafa9dd64e9ba4aa95cc1ef21-Abstract-Conference.html |
| S31 | Xiao et al. (2023), *SmoothQuant: Accurate and Efficient Post-Training Quantization for Large Language Models* | Medium | Alternative post-training quantisation method | metadata-check | https://proceedings.mlr.press/v202/xiao23c.html |
| S32 | Dettmers et al. (2023), *QLoRA: Efficient Finetuning of Quantized LLMs* | Optional | Distinguish quantised fine-tuning from this inference-only study | metadata-check | https://arxiv.org/abs/2305.14314 |
| S33 | ggml-org (n.d.), *llama.cpp* | Must | Runtime, local serving, supported backends, and OpenAI-compatible server | official | https://github.com/ggml-org/llama.cpp |
| S34 | ggml-org (n.d.), *llama.cpp Quantize Documentation* | Must | Q2_K, Q4_K_M, Q8_0 terminology and quantisation workflow | official | https://github.com/ggml-org/llama.cpp/blob/master/tools/quantize/README.md |
| S35 | ggml-org (n.d.), *GGUF Specification* | High | GGUF role and format definition | official | https://github.com/ggml-org/ggml/blob/master/docs/gguf.md |
| S36 | Liu et al. (2024), *MobileLLM: Optimizing Sub-billion Parameter Language Models for On-Device Use Cases* | High | Small-model and on-device deployment motivation | metadata-check | https://arxiv.org/abs/2402.14905 |

Metadata note for S30: the final MLSys 2024 proceedings title includes "On-Device". The arXiv preprint title omits that phrase. Use the proceedings title and publication record in the final Harvard reference.

## D. Tested models, embedding model, and reranker

| ID | Source | Priority | Planned use | Status | Primary/official link |
|---|---|---|---|---|---|
| S37 | Qwen Team (2024), *Qwen2.5 Technical Report* | Must | Qwen2.5 family and size variants | verified-primary | https://arxiv.org/abs/2412.15115 |
| S38 | Qwen Team (n.d.), *Qwen2.5-1.5B-Instruct Model Card* | Must | Exact tested model metadata and intended use | official | https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct |
| S39 | Dubey et al. (2024), *The Llama 3 Herd of Models* | High | Llama family technical background | metadata-check | https://arxiv.org/abs/2407.21783 |
| S40 | Meta (2024), *Llama 3.2 Model Card* | Must | Exact Llama 3.2 1B metadata, limitations, and licence | official | https://github.com/meta-llama/llama-models/blob/main/models/llama3_2/MODEL_CARD.md |
| S41 | Gemma Team (2025), *Gemma 3 Technical Report* | Must | Gemma 3 architecture and 1B-family technical context | verified-primary | https://storage.googleapis.com/deepmind-media/gemma/Gemma3Report.pdf |
| S42 | Google DeepMind (2025), *Gemma 3 Model Card* | Must | Exact tested-model capabilities, limitations, and responsible-use context | official | https://ai.google.dev/gemma/docs/core/model_card_3 |
| S43 | Wang et al. (2020), *MiniLM: Deep Self-Attention Distillation for Task-Agnostic Compression of Pre-Trained Transformers* | High | MiniLM architecture used by local retrieval components | verified-primary | https://papers.neurips.cc/paper_files/paper/2020/hash/3f5ee243547dee91fbd053c1c4a845aa-Abstract.html |
| S44 | Sentence Transformers (n.d.), *all-MiniLM-L6-v2 Model Card* | Must | Exact local embedding model implementation details | official | https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2 |
| S45 | Sentence Transformers (n.d.), *ms-marco-MiniLM-L6-v2 Cross-Encoder Model Card* | Must | Exact local reranker implementation details | official | https://huggingface.co/cross-encoder/ms-marco-MiniLM-L6-v2 |

## E. Privacy, security, and governance

| ID | Source | Priority | Planned use | Status | Primary/official link |
|---|---|---|---|---|---|
| S46 | Tabassi (2023), *Artificial Intelligence Risk Management Framework (AI RMF 1.0)* | Must | Trustworthiness and lifecycle risk framing | official | https://doi.org/10.6028/NIST.AI.100-1 |
| S47 | NIST (2024), *Artificial Intelligence Risk Management Framework: Generative Artificial Intelligence Profile* | Must | Generative-AI-specific risk discussion | official | https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf |
| S48 | NIST (2020), *Privacy Framework: A Tool for Improving Privacy through Enterprise Risk Management, Version 1.0* | High | Distinguish privacy risk management from security controls | official | https://doi.org/10.6028/NIST.CSWP.01162020 |
| S49 | Information Commissioner's Office (n.d.), *Guidance on AI and Data Protection* | Must | UK data-protection principles and AI lifecycle | official | https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/artificial-intelligence/guidance-on-ai-and-data-protection/ |
| S50 | Information Commissioner's Office (n.d.), *How Should We Assess Security and Data Minimisation in AI?* | Must | Data minimisation and the limits of technical privacy measures | official | https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/artificial-intelligence/guidance-on-ai-and-data-protection/how-should-we-assess-security-and-data-minimisation-in-ai/ |
| S51 | European Parliament and Council (2016), *Regulation (EU) 2016/679, Article 5* | High | Data minimisation, integrity, and confidentiality principles | official | https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32016R0679 |
| S52 | UK Parliament (2018), *Data Protection Act 2018* | High | UK legal context; cite only where directly relevant | official | https://www.legislation.gov.uk/ukpga/2018/12/contents |
| S53 | OWASP (2025), *Top 10 for LLMs and Generative AI Applications* | High | Prompt injection, information disclosure, and vector/embedding weaknesses | official | https://genai.owasp.org/llm-top-10/ |
| S54 | Zeng et al. (2024), *The Good and the Bad: Exploring Privacy Issues in Retrieval-Augmented Generation* | High | RAG-specific privacy threats | metadata-check | https://arxiv.org/abs/2402.16893 |
| S55 | Huang et al. (2023), *Privacy Implications of Retrieval-Based Language Models* | High | Privacy leakage from retrieval-based language models | metadata-check | https://arxiv.org/abs/2305.14888 |
| S56 | Wang and Chau (2024), *MeMemo: On-device Retrieval Augmentation for Private and Personalized Text Generation* | Must | Direct precedent for client-side retrieval and privacy motivation | verified-primary | https://doi.org/10.1145/3626772.3657662 |
| S57 | Anderson, Amit and Goldsteen (2024), *Is My Data in Your Retrieval Database? Membership Inference Attacks Against Retrieval Augmented Generation* | Medium | Show that RAG privacy risks extend beyond cloud transmission | metadata-check | https://arxiv.org/abs/2405.20446 |

## F. Statistics, agreement, and reproducibility

| ID | Source | Priority | Planned use | Status | Primary/official link |
|---|---|---|---|---|---|
| S58 | Spearman (1904), *The Proof and Measurement of Association between Two Things* | Must | Original basis for Spearman's rank correlation | metadata-check | https://doi.org/10.2307/1412159 |
| S59 | Cohen (1960), *A Coefficient of Agreement for Nominal Scales* | Optional | Explain why kappa is not the selected statistic for the present ordinal/continuous summary | metadata-check | https://doi.org/10.1177/001316446002000104 |
| S60 | Krippendorff (2018), *Content Analysis: An Introduction to Its Methodology*, 4th ed. | Medium | Reliability and coding-design background | metadata-check | https://us.sagepub.com/en-us/nam/content-analysis/book258450 |
| S61 | Artstein and Poesio (2008), *Inter-Coder Agreement for Computational Linguistics* | High | Agreement measures and interpretation | metadata-check | https://doi.org/10.1162/coli.07-034-R2 |
| S62 | Pineau et al. (2021), *Improving Reproducibility in Machine Learning Research* | High | Protocol freezing, artefact retention, and reproducibility | metadata-check | https://jmlr.org/papers/v22/20-303.html |
| S63 | Gundersen and Kjensmo (2018), *State of the Art: Reproducibility in Artificial Intelligence* | Medium | Reproducibility terminology and reporting | metadata-check | https://ojs.aaai.org/index.php/AAAI/article/view/11503 |

## G. Related theses used for presentation study

These five sources do not automatically belong in the final bibliography. Cite them only if they support a genuine related-work claim.

| ID | Source | Priority | Planned use | Status | Public record |
|---|---|---|---|---|---|
| S64 | Ahmad (2025), local-model RAG evaluation | Optional | Related empirical student work; model-comparison presentation | example-only | https://aaltodoc.aalto.fi/items/a4950788-a775-4fbb-9ee1-04ab10138cbb |
| S65 | Hamalainen (2025), RAG and LLM-as-a-judge | Optional | Related evaluation student work; chapter organisation | example-only | https://aaltodoc.aalto.fi/items/f0676611-4e7a-4fbb-8a26-8bed2b3911e2 |
| S66 | Henriksson and Grattan (2025), quantised local RAG | Optional | Short bachelor comparison; table clarity only | example-only | https://www.diva-portal.org/smash/get/diva2%3A1970376/FULLTEXT01.pdf |
| S67 | Yu and Tang (2026), llama.cpp bottlenecks | Optional | Hardware-conditioned systems argument | example-only | https://odr.chalmers.se/items/1d688f36-7a13-45d1-82d3-76dd1520581d |
| S68 | Bodea (2025), RAG privacy | Optional | Privacy taxonomy and discussion structure | example-only | https://www.cs.cit.tum.de/en/sebis/student-theses-guided-research/completed-theses-guided-research/2025/masters-thesis-andreea-bodea/ |

## H. Project artefacts and baseline code

Items in this section document implementation provenance and the starting pipeline. They are tracked separately from the 68 academic, official, and example candidates above.

| ID | Artefact | Planned use | Status | Repository |
|---|---|---|---|---|
| P01 | Wang, J. (2025), *Jetson-Nano-RAG-LLM* | Reference implementation and starting RAG pipeline | project-artifact | https://github.com/jackiewaang/Jetson-Nano-RAG-LLM |

Harvard-style working reference for P01: Wang, J. (2025) *Jetson-Nano-RAG-LLM*. GitHub repository. Available at: https://github.com/jackiewaang/Jetson-Nano-RAG-LLM (Accessed: 27 July 2026).

## Selection target

This plan contains 68 candidates:

- 57 technical, empirical, official, or governance sources (S01-S57);
- 6 statistics/reproducibility sources (S58-S63);
- 5 related theses used mainly as writing examples (S64-S68).

P01 is a separately tracked project artefact and does not increase the 68-source candidate count.

The expected final bibliography is not required to include all 68. A sensible final selection is:

- retain most of S01-S57 where the corresponding claim appears;
- retain 3-5 of S58-S63 according to the final statistical wording;
- cite no more than 1-3 of S64-S68 unless the Literature Review genuinely compares related dissertation work;
- add a source only when a new factual claim or scholarly comparison needs it.

## Next verification work

- [ ] Verify every `metadata-check` record against Crossref, the publisher, ACL Anthology, proceedings, or the official repository.
- [ ] Record the exact Harvard reference and access date for every web source.
- [ ] Mark each source `read`, `partly read`, `cited`, or `dropped`.
- [ ] Add page/section notes for sources used in close factual claims.
- [ ] Map each retained source to Introduction, Literature Review, Methodology, Results, or Discussion.
- [ ] Check that every in-text citation has one reference-list entry and every reference-list entry is cited in the text.
- [ ] Run a final source-quality audit: primary source preferred, no citation laundering, no padding.
