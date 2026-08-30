from __future__ import annotations

import csv
import json
import random
from collections import Counter, defaultdict
from pathlib import Path
from statistics import mean
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
QUESTION_SET = ROOT / "dissertation_project" / "benchmark_plan" / "question_set_template.csv"
RESULTS_ROOT = ROOT / "dissertation_project" / "benchmark_results"

RUN_FOLDERS = {
    "C1": "full_benchmark_C1_20260619_224126",
    "C2": "full_benchmark_C2_20260619_225653",
    "C3": "full_benchmark_C3_20260619_231534",
}

OUTPUT_STEM = "C1_C2_C3_2026-06-20"
RANDOM_SEED = 20260620
BLIND_CODES = ["K7", "A4", "F9", "M2", "R6", "T1", "X5", "Q8"]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, Any]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def normalise_sources(sources: Any) -> str:
    if not isinstance(sources, dict):
        return json.dumps(sources, sort_keys=True, ensure_ascii=False)
    detailed = sources.get("detailed_sources", [])
    simplified = [
        {
            "source": item.get("source", ""),
            "page": item.get("page", ""),
            "chunk_id": item.get("chunk_id", ""),
        }
        for item in detailed
    ]
    return json.dumps(simplified, sort_keys=True, ensure_ascii=False)


def answer_key(row: dict[str, str]) -> str:
    return f"{row['question_id']}_rep{row['repetition']}"


def main() -> None:
    rng = random.Random(RANDOM_SEED)
    questions = {row["question_id"]: row for row in read_csv(QUESTION_SET)}

    model_ids = list(RUN_FOLDERS)
    shuffled_codes = BLIND_CODES[:]
    rng.shuffle(shuffled_codes)
    blind_code_by_model = {model_id: shuffled_codes[index] for index, model_id in enumerate(model_ids)}

    blind_rows: list[dict[str, Any]] = []
    finish_rows: list[dict[str, Any]] = []
    memory_rows: list[dict[str, Any]] = []
    source_rows: list[dict[str, Any]] = []
    all_source_signatures: dict[str, dict[str, set[str]]] = defaultdict(lambda: defaultdict(set))

    for model_id, folder_name in RUN_FOLDERS.items():
        folder = RESULTS_ROOT / folder_name
        answer_rows = read_csv(folder / "model_answer_log.csv")

        for row in answer_rows:
            question = questions[row["question_id"]]
            raw_path = folder / "raw_responses" / f"{answer_key(row)}.json"
            raw = load_json(raw_path)
            choice = (raw.get("choices") or [{}])[0]
            finish_reason = choice.get("finish_reason", "")
            usage = raw.get("usage", {})
            timings = raw.get("timings", {})
            sources = raw.get("sources_used", {})
            generated_answer = row["generated_answer"]
            answer_id = f"{blind_code_by_model[model_id]}-{row['question_id']}-R{row['repetition']}"

            blind_rows.append(
                {
                    "blind_answer_id": answer_id,
                    "blind_model_code": blind_code_by_model[model_id],
                    "question_id": row["question_id"],
                    "repetition": row["repetition"],
                    "source_id": question["source_id"],
                    "source_title": question["source_title"],
                    "question_type": question["question_type"],
                    "difficulty": question["difficulty"],
                    "documents_needed": question["documents_needed"],
                    "question_text": row["question_text"],
                    "expected_answer_notes": question["expected_answer_notes"],
                    "evidence_location": question["evidence_location"],
                    "generated_answer": generated_answer,
                    "relevance": "",
                    "correctness": "",
                    "faithfulness_to_source": "",
                    "completeness": "",
                    "hallucination_risk": "",
                    "source_grounding": "",
                    "average_quality_score": "",
                    "scoring_notes": "",
                    "scored_by": "",
                    "scored_date": "",
                }
            )

            finish_rows.append(
                {
                    "model_config_id": model_id,
                    "blind_model_code": blind_code_by_model[model_id],
                    "question_id": row["question_id"],
                    "repetition": row["repetition"],
                    "finish_reason": finish_reason,
                    "completion_tokens": usage.get("completion_tokens", ""),
                    "predicted_tokens": timings.get("predicted_n", ""),
                    "generated_answer_chars": len(generated_answer),
                    "generated_answer_words_approx": len(generated_answer.split()),
                    "raw_json": str(raw_path.relative_to(ROOT)),
                }
            )

            memory_rows.append(
                {
                    "model_config_id": model_id,
                    "blind_model_code": blind_code_by_model[model_id],
                    "question_id": row["question_id"],
                    "repetition": row["repetition"],
                    "observed_llama_server_rss_mb": row.get("peak_memory_mb", ""),
                    "latency_seconds": row.get("latency_seconds", ""),
                    "tokens_per_second": row.get("tokens_per_second", ""),
                }
            )

            source_signature = normalise_sources(sources)
            all_source_signatures[row["question_id"]][model_id].add(source_signature)
            source_rows.append(
                {
                    "model_config_id": model_id,
                    "blind_model_code": blind_code_by_model[model_id],
                    "question_id": row["question_id"],
                    "repetition": row["repetition"],
                    "source_signature": source_signature,
                    "sources_used": json.dumps(sources, ensure_ascii=False, sort_keys=True),
                }
            )

    rng.shuffle(blind_rows)

    blind_fields = [
        "blind_answer_id",
        "blind_model_code",
        "question_id",
        "repetition",
        "source_id",
        "source_title",
        "question_type",
        "difficulty",
        "documents_needed",
        "question_text",
        "expected_answer_notes",
        "evidence_location",
        "generated_answer",
        "relevance",
        "correctness",
        "faithfulness_to_source",
        "completeness",
        "hallucination_risk",
        "source_grounding",
        "average_quality_score",
        "scoring_notes",
        "scored_by",
        "scored_date",
    ]
    finish_fields = [
        "model_config_id",
        "blind_model_code",
        "question_id",
        "repetition",
        "finish_reason",
        "completion_tokens",
        "predicted_tokens",
        "generated_answer_chars",
        "generated_answer_words_approx",
        "raw_json",
    ]
    key_fields = ["blind_model_code", "model_config_id", "run_folder", "note"]
    source_fields = [
        "model_config_id",
        "blind_model_code",
        "question_id",
        "repetition",
        "source_signature",
        "sources_used",
    ]
    memory_fields = [
        "model_config_id",
        "blind_model_code",
        "question_id",
        "repetition",
        "observed_llama_server_rss_mb",
        "latency_seconds",
        "tokens_per_second",
    ]

    blind_csv = RESULTS_ROOT / f"full_benchmark_blind_scoring_{OUTPUT_STEM}.csv"
    blind_rep1_csv = RESULTS_ROOT / f"full_benchmark_blind_scoring_rep1_only_{OUTPUT_STEM}.csv"
    finish_csv = RESULTS_ROOT / f"full_benchmark_finish_reason_audit_{OUTPUT_STEM}.csv"
    key_csv = RESULTS_ROOT / f"full_benchmark_blind_model_key_{OUTPUT_STEM}.csv"
    source_csv = RESULTS_ROOT / f"full_benchmark_source_consistency_audit_{OUTPUT_STEM}.csv"
    source_summary_csv = RESULTS_ROOT / f"full_benchmark_source_consistency_summary_{OUTPUT_STEM}.csv"
    memory_csv = RESULTS_ROOT / f"full_benchmark_memory_sanity_audit_{OUTPUT_STEM}.csv"

    write_csv(blind_csv, blind_fields, blind_rows)
    write_csv(blind_rep1_csv, blind_fields, [row for row in blind_rows if row["repetition"] == "1"])
    write_csv(finish_csv, finish_fields, finish_rows)
    write_csv(
        key_csv,
        key_fields,
        [
            {
                "blind_model_code": blind_code_by_model[model_id],
                "model_config_id": model_id,
                "run_folder": RUN_FOLDERS[model_id],
                "note": "Do not open this key during blind scoring.",
            }
            for model_id in model_ids
        ],
    )
    write_csv(source_csv, source_fields, source_rows)
    write_csv(memory_csv, memory_fields, memory_rows)

    finish_summary: dict[str, Counter[str]] = defaultdict(Counter)
    for row in finish_rows:
        finish_summary[row["model_config_id"]][row["finish_reason"]] += 1

    source_question_summaries = []
    inconsistent_questions = []
    for question_id, by_model in sorted(all_source_signatures.items()):
        all_signatures = set()
        per_model_counts = {}
        for model_id, signatures in by_model.items():
            all_signatures.update(signatures)
            per_model_counts[model_id] = len(signatures)
        is_consistent = len(all_signatures) == 1
        if not is_consistent:
            inconsistent_questions.append(question_id)
        source_question_summaries.append((question_id, is_consistent, per_model_counts, len(all_signatures)))

    write_csv(
        source_summary_csv,
        [
            "question_id",
            "consistent_all_runs",
            "unique_source_signatures_all_models",
            "unique_source_signatures_C1",
            "unique_source_signatures_C2",
            "unique_source_signatures_C3",
        ],
        [
            {
                "question_id": question_id,
                "consistent_all_runs": str(is_consistent),
                "unique_source_signatures_all_models": total_unique,
                "unique_source_signatures_C1": per_model_counts.get("C1", 0),
                "unique_source_signatures_C2": per_model_counts.get("C2", 0),
                "unique_source_signatures_C3": per_model_counts.get("C3", 0),
            }
            for question_id, is_consistent, per_model_counts, total_unique in source_question_summaries
        ],
    )

    memory_by_model: dict[str, list[float]] = defaultdict(list)
    for row in memory_rows:
        value = row["observed_llama_server_rss_mb"]
        if value != "":
            memory_by_model[row["model_config_id"]].append(float(value))

    summary_md = RESULTS_ROOT / f"full_benchmark_audit_summary_{OUTPUT_STEM}.md"
    lines = [
        "# Full Benchmark Blind Scoring and Audit Summary",
        "",
        "**Created:** 2026-06-20",
        f"**Randomisation seed:** `{RANDOM_SEED}`",
        "",
        "## Generated Files",
        "",
        f"- Blind scoring CSV: `{blind_csv.name}`",
        f"- Rep-1-only blind scoring CSV: `{blind_rep1_csv.name}`",
        f"- Blind model key: `{key_csv.name}`",
        f"- Finish reason audit: `{finish_csv.name}`",
        f"- Source consistency audit: `{source_csv.name}`",
        f"- Source consistency summary: `{source_summary_csv.name}`",
        f"- Memory sanity audit: `{memory_csv.name}`",
        "",
        "## Blind Scoring",
        "",
        f"- Rows: {len(blind_rows)}",
        f"- Rep-1-only rows: {sum(1 for row in blind_rows if row['repetition'] == '1')}",
        "- Model identifiers are hidden behind random blind codes.",
        "- Row order is shuffled.",
        "- Latency, memory, and throughput are excluded from the blind scoring sheet to reduce scoring bias.",
        "- Do not open the blind model key until after scoring is completed.",
        "",
        "## Finish Reason Audit",
        "",
        "| Model | stop | length | other/blank | total |",
        "|---|---:|---:|---:|---:|",
    ]
    for model_id in model_ids:
        counts = finish_summary[model_id]
        stop_count = counts.get("stop", 0)
        length_count = counts.get("length", 0)
        total = sum(counts.values())
        other = total - stop_count - length_count
        lines.append(f"| {model_id} | {stop_count} | {length_count} | {other} | {total} |")

    lines.extend(
        [
            "",
            "## Source Consistency Audit",
            "",
            f"- Questions checked: {len(source_question_summaries)}",
            f"- Questions with inconsistent retrieved source signatures: {len(inconsistent_questions)}",
        ]
    )
    if inconsistent_questions:
        lines.append(f"- Inconsistent question IDs: {', '.join(inconsistent_questions)}")
    else:
        lines.append("- Retrieved source signatures were consistent for every question across C1-C3 and repetitions.")

    lines.extend(
        [
            "",
            "## Memory Sanity Note",
            "",
            "The existing `peak_memory_mb` field should be interpreted as an observed llama-server process RSS estimate after each request, not as a true peak-memory profiler measurement.",
            "",
            "| Model | Mean observed RSS MiB | Min | Max | Rows |",
            "|---|---:|---:|---:|---:|",
        ]
    )
    for model_id in model_ids:
        values = memory_by_model[model_id]
        lines.append(
            f"| {model_id} | {mean(values):.2f} | {min(values):.2f} | {max(values):.2f} | {len(values)} |"
        )

    lines.extend(
        [
            "",
            "## Seed and Reproducibility Note",
            "",
            "The C1-C3 full benchmark runs did not specify an explicit generation seed in llama.cpp. This should be reported as `seed not specified`. The three repetitions per question still provide repeated observations under the same temperature and prompt settings, but the runs are not bit-level reproducible from a recorded seed.",
            "",
            "For C4/C5, use the same seed policy as C1-C3 unless the protocol is explicitly amended and the earlier models are rerun.",
            "",
        ]
    )
    summary_md.write_text("\n".join(lines), encoding="utf-8")

    print(f"Wrote {blind_csv}")
    print(f"Wrote {blind_rep1_csv}")
    print(f"Wrote {key_csv}")
    print(f"Wrote {finish_csv}")
    print(f"Wrote {source_csv}")
    print(f"Wrote {source_summary_csv}")
    print(f"Wrote {memory_csv}")
    print(f"Wrote {summary_md}")


if __name__ == "__main__":
    main()
