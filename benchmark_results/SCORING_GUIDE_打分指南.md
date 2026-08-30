# Human Scoring Guide / 人工打分操作指南

**Created / 创建:** 2026-06-29
**Total workload / 总工作量:** 240 answers = Stage 1 (60, from scratch) + Stage 2 (180, AI-assisted review)
**Estimated time / 预计耗时:** Stage 1 ≈ 2–2.5 h · Stage 2 ≈ 3–4 h · 分几天做,别一口气

---

## Why two stages / 为什么分两段

**Stage 1 (independent 独立):** you score 60 answers from scratch, without seeing any AI scores. These 60 are later compared with the AI's scores on the same answers → a genuine human–AI agreement statistic (Spearman correlation / weighted kappa) for the dissertation.

**第一段(独立):** 60 个答案你从零打分,完全不看 AI 的分。之后拿这 60 个和 AI 在同样答案上的分对比 → 得到真实的"人机一致性"统计量,写进论文。

**Stage 2 (AI-assisted AI辅助):** the remaining 180 answers show the AI's draft scores; you review, agree or correct. This saves time while the human stays the final authority.

**第二段(AI 辅助):** 剩下 180 个答案带着 AI 草稿分;你审核,同意或改掉。省时间,但人仍是最终裁决者。

**⚠️ Iron rules / 铁律:**
1. **先做完第一段,再打开第二段的文件。** Finish Stage 1 before opening the Stage 2 file.
2. **全部打完之前,绝不打开 blind model key 文件。** Never open the blind model key until all scoring is done.
3. 一旦发现自己想猜"这是哪个模型",停下来,只看答案本身。 If you catch yourself guessing which model it is, stop and judge only the answer text.

---

## Files / 文件

| Stage | File | Rows |
|---|---|---|
| 1 | `human_stage1_independent_60_2026-06-29.csv` | 60 |
| 2 | `human_stage2_ai_assisted_180_2026-06-29.csv` | 180 |
| split record | `two_stage_scoring_split_2026-06-29.md` | which questions are in which stage |

---

## How to score one answer / 单个答案怎么打(约 2 分钟)

For each row / 每一行:

1. **读题** — read `question_text`.
2. **读标准** — read `expected_answer_notes`(预期答案要点)and `evidence_location`(证据在哪份文档哪部分).
3. **读答案** — read `generated_answer`.
4. **打六个分**(each 0–5 / 每个 0-5 分):

| Dimension 维度 | Ask yourself 问自己 |
|---|---|
| relevance 相关性 | 它是在回答这道题吗?还是答非所问? |
| correctness 正确性 | 对照预期要点,它说的事实对吗? |
| faithfulness_to_source 忠实度 | 它的说法能在证据/来源里找到吗? |
| completeness 完整性 | 预期要点覆盖了多少?一半?全部? |
| hallucination_risk 幻觉 | 有没有编造?(5=完全没编,0=严重编造)注意:分越高越好 |
| source_grounding 来源依据 | 答案是否明显基于给它的材料,而非泛泛而谈? |

5. **average_quality_score** = 六个分的平均(Excel 里用公式 `=AVERAGE(...)` 拖一列即可)。
6. **scoring_notes** — 一句话即可,低分必写原因(如 "invented a fact about X" / "missed the second half of expected points")。
7. **scored_by** 填 `human`,**scored_date** 填当天日期。

**Scale anchor / 分数锚点:** 0=没答/不可用 1=很差 2=弱 3=可接受 4=好 5=优秀。**Use 3 as your center of gravity** — 别全打 4,那样区分不出模型。3 = 及格,4 = 确实好,5 = 挑不出毛病。

---

## Stage 2 extra rules / 第二段的额外规则

- Look at the answer FIRST, form your own impression, THEN look at `ai_draft_*` scores. 先看答案、心里有数,再看 AI 草稿分。
- If you agree / 同意:copy the draft into the `human_*` columns and set `review_status` = `Human reviewed - agreed`.
- If you disagree / 不同意:write your own scores in `human_*`, set `review_status` = `Human reviewed - changed`, and start `human_notes` with `Human review:` + 原因。
- Pay extra attention to / 重点盯:very low AI scores(≤2)、borderline(2.5-3.5)、and anything the AI called hallucination。

---

## Session plan / 分次计划(建议)

| Session | What | Time |
|---|---|---|
| 1 | Stage 1: 前 30 行 | ~1 h |
| 2 | Stage 1: 后 30 行 | ~1 h |
| 3 | Stage 2: 60 行 | ~1 h |
| 4 | Stage 2: 60 行 | ~1 h |
| 5 | Stage 2: 60 行 + 全表检查空格 | ~1.5 h |

Between sessions, save the file with the same name. 每次做完原名保存。
Consistency tip: before each session, re-read your last 5 scored rows to recalibrate. 每次开始前重看自己上一次打的最后 5 行,校准手感。

---

## After all scoring / 全部打完之后(顺序别乱)

1. 检查 240 行没有空分。
2. 计算 Stage-1 60 行的 human vs AI 一致性(这一步交给 Claude/Codex 算:Spearman + weighted kappa)。
3. **这时才打开 model key**,把盲码换回 C1-C6。
4. 合并质量分 + 系统指标 → 出结果表和图。
5. 写 Results / Discussion。
