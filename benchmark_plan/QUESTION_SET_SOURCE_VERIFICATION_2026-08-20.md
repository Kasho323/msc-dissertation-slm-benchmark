# 40 题逐题来源核查记录

**执行日期:** 2026-08-20
**核查对象:** `benchmark_plan/question_set_template.csv`(冻结的 40 题问题集)
**比对来源:** `docs/final_benchmark_corpus/` 中的四份 PDF 原文

| ID | 文件 | 页数 | 抽取字符 |
|---|---|---:|---:|
| D1 | `D1_RAG_Lewis_2020.pdf` | 19 | 70,136 |
| D2 | `D2_llama_cpp_README.pdf` | 16 | 17,531 |
| D3 | `D3_NIST_AI_RMF_1_0.pdf` | 48 | 107,608 |
| D4 | `D4_ICO_AI_Data_Protection_Guidance.pdf` | 26 | 92,841 |

---

## ⚠️ 首要说明:本次核查**未修改任何题目**

问题集在实验前已冻结,并据此生成了全部 720 个输出、评分了 240 个唯一对。**现在修改任何 question text、expected-answer note 或 evidence location,都会使已生成的输出与已完成的评分失去对应关系,等于篡改实验数据。**

因此本记录的性质是:**核查 + 如实披露**,不是"修正"。Codex 指令中「报告哪些题目被修改」一项,答案是:**零题被修改**,理由如上。发现的问题以**披露**方式处理,不以回溯修改方式处理。

---

## 核查方法

分三步,避免用词频这种粗糙指标下结论:

**第一步 — 概念级覆盖率.** 从每题的 expected-answer note 抽取内容词,剔除三类噪声:
- 评分指导用语(`should`、`explain`、`mention`、`avoid overstating` 等)
- 项目专有词(`dissertation`、`benchmark`、`FastAPI`、`RAG`、`laptop` 等,这些本就不该出现在语料里)
- 停用词

余下的**实质概念词**再与 `source_id` 所指文档的全文比对,允许简单形态变化。

**第二步 — 拼写变体校正.** 论文用英式拼写,语料用美式。已确认 `quantisation`/`quantised` 在 D2 中以 `quantization` 出现(2 处),`memorised` 在 D1 中以 `memoriz*` 出现(1 处)。这类差异**不构成缺失**。

**第三步 — 人工逐项复核.** 对覆盖率偏低的题,回到原文逐句查证,并区分:
- **来源主张** —— 必须能在文档中定位
- **项目框架语** —— 说明该知识点对本研究为何相关,合理地不在来源中
- **评分指导语** —— 不是内容

---

## 总体结果

| 判定 | 题数 |
|---|---|
| **OK** —— 来源主张全部可在指定文档中定位 | **37** |
| **部分超出来源** —— 要点中部分具体项在指定文档中不存在 | **1**(Q035) |
| **元数据不一致** —— 证据位置引用了 `source_id` 之外的文档 | **2**(Q018、Q020) |
| **错配** —— 要点与来源不符 | **0** |
| **无法核验** | **0** |

**四份语料全部可读、可检索,证据位置所指的章节全部真实存在。**

---

## 发现一 · Q035 的要点部分超出 D4 的内容

**题干:** What kinds of local risks remain even if a model does not send data to a cloud API?
**证据位置:** D4 ICO security and data minimisation chapter; D4 privacy attacks section
**要点原文:**

> A good answer should mention **local storage, logs, vector databases, cached files, model outputs, access control, backups, device compromise, insecure dependencies**, and possible privacy attacks or leakage from models. It should not claim local equals fully private.

要点列举了十项。逐项对 D4 全文检索:

| 要点列举项 | D4 中是否存在 | 依据 |
|---|---|---|
| local storage | ✅ | `stored` 3 处 |
| **logs** | ❌ **不存在** | `\blogs?\b` 与 `\blogging\b` 均为 **0**。全文 11 处 "log" 全部是 `technolog*` / `terminolog*` |
| **vector databases** | ❌ **不存在** | `vector database` / `vector store` / `embedding` 均为 0 |
| **cached files** | ❌ **不存在** | `cache` / `cached` 均为 0 |
| model outputs | ✅ | `output` 10 处 |
| access control | ✅ | `unauthorised access` 1 处、`access to the` 5 处(短语 "access control" 本身为 0) |
| **backups** | ❌ **不存在** | `backup` / `back-up` 均为 0 |
| device compromise | ✅ | `compromise` 3、`attacker` 11、`adversar*` 11 |
| insecure dependencies | ✅ | `dependenc*` 1、`third-party` 2、`supply chain` 1、`external code` 1 |
| privacy attacks / leakage | ✅ | `privacy attack` 13、`model inversion` 13、`membership inference` 9。原文:「we focus on two kinds of these privacy attacks – 'model inversion' and 'membership inference'」 |

**判定:10 项中 6 项有来源支撑,4 项(logs、vector databases、cached files、backups)是作者针对本地 RAG 场景的自行扩展,D4 并未列举。**

**风险:** ICO 指南讨论的是 AI 系统的安全与数据最小化原则,不是本地 RAG 部署的具体文件类型。要点把作者的领域知识与来源内容混在了一起。

**这对结果有影响吗 —— 有限,且方向是保守的:**
- 该题是 40 题之一,权重 2.5%
- 六个配置**面对的是同一份要点**,所以偏差对所有配置一致,不改变相对比较
- 若模型答不出"日志、缓存、备份",它在 completeness 上会被扣分,而这几项本不在来源里 —— 这使评分对**所有**配置偏严,不偏袒任何一个

**建议处理(不改题目):** 在 §3.4 或 §6.6 增加一句披露,例如:

> One expected-answer note (Q035) enumerates local-deployment risks such as logs, caches and backups that reflect the local RAG setting rather than the wording of the source document. Because the same note was applied to all six configurations, this affects the absolute completeness scores on that question rather than the comparison between configurations.

---

## 发现二 · Q018 与 Q020 的证据位置引用了 `source_id` 之外的文档

| 题号 | `source_id` | `documents_needed` | 证据位置实际提到 |
|---|---|---|---|
| **Q018** | `D2` | `one_document` | `D2` **和 D4** ——「D2 README Description; **D4 ICO security/data minimisation for limitation context**」 |
| **Q020** | `D2` | `one_document` | `D2` **和 D4** ——「D2 README Description; D2 Quick start; **D4 ICO security/data minimisation context**」 |

**判定:元数据内部不一致。** 两题标为单文档题,但证据位置援引了第二份文档作为"限制语境"。

**核实:两题的主张本身没有问题。** Q018 的核心主张「computation can happen on the user's own machine rather than a remote cloud provider」在 D2 Description 中有直接支撑:

> "The main goal of llama.cpp is to enable LLM inference with minimal setup and state-of-the-art performance on a wide range of hardware — **locally and in the cloud**."

D4 只是被用来支持后半句"不要过度声称隐私"。

**这对论文有何影响:** §3.4 与 Appendix C 报告「3 题需要跨文档证据」(`documents_needed = multiple_documents` 的 Q038、Q039、Q040)。若把 Q018、Q020 也算上,跨文档题应为 5 题。**但这两题被冻结为单文档题,模型作答与评分都按单文档处理**,所以已报告的统计与实际执行一致。

**建议处理:** 不改元数据。可在 Appendix C 加一句脚注说明两题的证据位置援引了第二份文档作为语境,但实验中按单文档题处理。

---

## 发现三 · 部分要点含项目框架语(**正常,不是问题**)

多题的要点在陈述来源内容之后,补了一句"这对本研究为何重要"。例如:

- **Q012**:「…This makes it practical for a **laptop-based local benchmark**.」
- **Q016**:「…lets the **FastAPI backend** call a local model…reducing changes needed in the **RAG app**」(证据位置本身就写着 "project architecture context")
- **Q019**:「…for a laptop-based **dissertation** benchmark」

**判定:合理。** 这是评分指导笔记的正常写法 —— 前半句是来源主张(已逐条核实),后半句是研究者说明相关性。**不需要处理。**

---

## 逐题结果

覆盖率为"实质概念词命中率"。低于 100% 的差额已在第三步人工复核,确认为拼写变体、转述用词或项目框架语。

| 题号 | 来源 | 类型 | 难度 | 覆盖率 | 判定 |
|---|---|---|---|---:|---|
| Q001 | D1 | fact_retrieval | easy | 76% | OK |
| Q002 | D1 | explanation | medium | 94% | OK |
| Q003 | D1 | explanation | medium | 62% | OK — provenance 在 D1 有原文(「providing provenance for their decisions」) |
| Q004 | D1 | fact_retrieval | easy | 100% | OK |
| Q005 | D1 | explanation | medium | 88% | OK — `memorised` 对应 D1 的 `memoriz*` |
| Q006 | D1 | comparison | medium | 83% | OK |
| Q007 | D1 | fact_retrieval | easy | 100% | OK |
| Q008 | D1 | explanation | medium | 80% | OK |
| Q009 | D1 | boundary_limitation | hard | 84% | OK |
| Q010 | D1 | source_grounded_synthesis | medium | 93% | OK |
| Q011 | D2 | fact_retrieval | easy | 80% | OK |
| Q012 | D2 | explanation | medium | 77% | OK — 含项目框架语 |
| Q013 | D2 | fact_retrieval | easy | 91% | OK — `quantised` 对应 D2 的 `quantization` |
| Q014 | D2 | explanation | medium | 47% | **OK —— 要点几乎是 README 原句**:「1.5-bit, 2-bit, 3-bit, 4-bit, 5-bit, 6-bit, and 8-bit integer quantization **for faster inference and reduced memory use**」。低分纯属拼写变体造成 |
| Q015 | D2 | fact_retrieval | easy | 85% | OK |
| Q016 | D2 | explanation | medium | 79% | OK — 「OpenAI-compatible API server」与「Chat completion endpoint: /v1/chat/completions」均有原文 |
| Q017 | D2 | fact_retrieval | easy | 100% | OK |
| Q018 | D2 | explanation | medium | 31% | **元数据不一致(见发现二)**;主张本身有 D2 原文支撑 |
| Q019 | D2 | explanation | medium | 65% | OK — 含项目框架语 |
| Q020 | D2 | boundary_limitation | hard | 67% | **元数据不一致(见发现二)** |
| Q021 | D3 | fact_retrieval | easy | 91% | OK |
| Q022 | D3 | explanation | medium | 100% | OK |
| Q023 | D3 | explanation | medium | 100% | OK |
| Q024 | D3 | explanation | medium | 94% | OK |
| Q025 | D3 | comparison | medium | 79% | OK |
| Q026 | D3 | explanation | medium | 92% | OK |
| Q027 | D3 | boundary_limitation | hard | 93% | OK |
| Q028 | D3 | source_grounded_synthesis | hard | 72% | OK — 含项目框架语 |
| Q029 | D3 | boundary_limitation | hard | 75% | OK |
| Q030 | D4 | fact_retrieval | easy | 100% | OK |
| Q031 | D4 | explanation | medium | 100% | OK |
| Q032 | D4 | explanation | medium | 100% | OK |
| Q033 | D4 | explanation | medium | 100% | OK |
| Q034 | D4 | comparison | medium | 91% | OK |
| Q035 | D4 | boundary_limitation | hard | 65% | **部分超出来源(见发现一)** |
| Q036 | D4 | source_grounded_synthesis | hard | 95% | OK |
| Q037 | D4 | source_grounded_synthesis | hard | 91% | OK |
| Q038 | D1+D2 | source_grounded_synthesis | hard | 79% | OK |
| Q039 | D2+D4 | source_grounded_synthesis | hard | 83% | OK |
| Q040 | D1+D2+D3+D4 | source_grounded_synthesis | hard | 77% | OK |

---

## 结论与对 §3.11 措辞的影响

**Codex 提供的措辞现在可以使用,但需要一处修改。**

Codex 的原措辞:

> "AI assistance was used in the initial drafting and structuring of the question bank and expected-answer notes. I subsequently checked each question, expected-answer note and evidence location against the four source documents before the question set was frozen."

**问题在最后五个字:「before the question set was frozen」。**

本次核查是在 **2026-08-20** 完成的,而问题集在 **2026-06 实验前**就已冻结。写成"冻结前已核查"与事实不符。

**建议改为:**

> "AI assistance was used in the initial drafting and structuring of the question bank and expected-answer notes. Each question, expected-answer note and evidence location was subsequently checked against the four source documents; the check record is given in Appendix [X]. One note (Q035) was found to enumerate local-deployment risks that reflect the tested setting rather than the wording of the source document, and this is reported as a limitation rather than corrected, because the question set was frozen before any model output was generated."

这样三件事都如实交代:AI 参与过起草、核查确实做了、发现的问题以披露而非回溯修改处理。

---

## 本记录的归档位置

建议作为 **Appendix J**(或并入 Appendix C)纳入论文附录,使 §3.11 的"核查记录"有据可查。附录不计入正文字数。

**产出文件:**
- 本记录:`benchmark_plan/QUESTION_SET_SOURCE_VERIFICATION_2026-08-20.md`
- 逐题原始数据:核查脚本输出的 JSON(概念覆盖、未命中词、各来源分项),保存在临时工作区,如需归档可移入 `benchmark_plan/`
