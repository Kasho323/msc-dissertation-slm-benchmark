from __future__ import annotations

import csv
import json
import random
from collections import Counter, defaultdict
from pathlib import Path
from reproduction_paths import output_directory
OUTPUT = output_directory()
from statistics import mean, median
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
QUESTION_SET = ROOT / "benchmark_plan" / "question_set_template.csv"
RESULTS_ROOT = ROOT / "benchmark_results"

RUN_FOLDERS = {
    "C1": "full_benchmark_C1_20260624_211524",
    "C2": "full_benchmark_C2_20260624_213220",
    "C3": "full_benchmark_C3_20260624_215407",
    "C4": "full_benchmark_C4_20260624_221531",
    "C5": "full_benchmark_C5_20260624_223538",
    "C6": "full_benchmark_C6_20260624_225248",
}

OUTPUT_STEM = "C1_C6_2026-06-24"
RANDOM_SEED = 20260624
BLIND_CODES = ["A7", "F3", "K8", "M4", "R9", "T2"]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, Any]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def normalise_sources(sources_json: str) -> str:
    sources = json.loads(sources_json or "{}")
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


def percentile(values: list[float], fraction: float) -> float:
    ordered = sorted(values)
    if not ordered:
        return 0.0
    index = round((len(ordered) - 1) * fraction)
    return ordered[index]


def main() -> None:
    rng = random.Random(RANDOM_SEED)
    questions = {row["question_id"]: row for row in read_csv(QUESTION_SET)}
    model_ids = list(RUN_FOLDERS)

    shuffled_codes = BLIND_CODES[:]
    rng.shuffle(shuffled_codes)
    blind_code_by_model = dict(zip(model_ids, shuffled_codes, strict=True))

    blind_rows: list[dict[str, Any]] = []
    finish_rows: list[dict[str, Any]] = []
    source_rows: list[dict[str, Any]] = []
    memory_rows: list[dict[str, Any]] = []
    system_rows: list[dict[str, Any]] = []
    repetition_rows: list[dict[str, Any]] = []

    source_signatures: dict[str, set[str]] = defaultdict(set)
    source_signatures_by_model: dict[str, dict[str, set[str]]] = defaultdict(lambda: defaultdict(set))
    answers_by_model_question: dict[str, dict[str, list[str]]] = defaultdict(lambda: defaultdict(list))

    for model_id, folder_name in RUN_FOLDERS.items():
        folder = RESULTS_ROOT / folder_name
        answer_rows = read_csv(folder / "model_answer_log.csv")
        manifest = read_csv(folder / "run_manifest.csv")[0]

        latencies: list[float] = []
        throughputs: list[float] = []
        memories: list[float] = []
        output_tokens: list[float] = []
        finish_counts: Counter[str] = Counter()
        error_count = 0

        for row in answer_rows:
            question = questions[row["question_id"]]
            finish_reason = row.get("finish_reason", "")
            finish_counts[finish_reason] += 1
            error_count += bool(row.get("error_notes", "").strip())

            if row.get("latency_seconds"):
                latencies.append(float(row["latency_seconds"]))
            if row.get("tokens_per_second"):
                throughputs.append(float(row["tokens_per_second"]))
            if row.get("peak_memory_mb"):
                memories.append(float(row["peak_memory_mb"]))
            if row.get("tokens_generated"):
                output_tokens.append(float(row["tokens_generated"]))

            blind_rows.append(
                {
                    "blind_answer_id": (
                        f"{blind_code_by_model[model_id]}-{row['question_id']}-R{row['repetition']}"
                    ),
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
                    "generated_answer": row["generated_answer"],
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
                    "prompt_tokens": row.get("prompt_tokens", ""),
                    "completion_tokens": row.get("tokens_generated", ""),
                    "generated_answer_chars": len(row["generated_answer"]),
                    "generated_answer_words_approx": len(row["generated_answer"].split()),
                    "error_notes": row.get("error_notes", ""),
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
                    "tokens_generated": row.get("tokens_generated", ""),
                }
            )

            signature = normalise_sources(row["sources_returned"])
            source_signatures[row["question_id"]].add(signature)
            source_signatures_by_model[row["question_id"]][model_id].add(signature)
            source_rows.append(
                {
                    "model_config_id": model_id,
                    "blind_model_code": blind_code_by_model[model_id],
                    "question_id": row["question_id"],
                    "repetition": row["repetition"],
                    "source_signature": signature,
                    "sources_used": row["sources_returned"],
                }
            )
            answers_by_model_question[model_id][row["question_id"]].append(
                row["generated_answer"].strip()
            )

        system_rows.append(
            {
                "model_config_id": model_id,
                "model_name": manifest["model_name"],
                "quantisation": manifest["quantisation"],
                "model_file_size_mb": manifest["model_file_size_mb"],
                "answers": len(answer_rows),
                "errors": error_count,
                "finish_stop": finish_counts.get("stop", 0),
                "finish_length": finish_counts.get("length", 0),
                "mean_latency_seconds": round(mean(latencies), 4),
                "median_latency_seconds": round(median(latencies), 4),
                "p95_latency_seconds": round(percentile(latencies, 0.95), 4),
                "mean_tokens_per_second": round(mean(throughputs), 2),
                "mean_observed_rss_mb": round(mean(memories), 2),
                "min_observed_rss_mb": round(min(memories), 2),
                "max_observed_rss_mb": round(max(memories), 2),
                "mean_output_tokens": round(mean(output_tokens), 2),
                "seed": manifest["seed"],
                "max_tokens": manifest["max_tokens"],
                "power_profile": manifest["power_profile"],
            }
        )

    for model_id in model_ids:
        for question_id, answers in sorted(answers_by_model_question[model_id].items()):
            unique_answers = len(set(answers))
            repetition_rows.append(
                {
                    "model_config_id": model_id,
                    "blind_model_code": blind_code_by_model[model_id],
                    "question_id": question_id,
                    "repetitions": len(answers),
                    "unique_exact_answers": unique_answers,
                    "all_repetitions_exactly_identical": str(unique_answers == 1),
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
        "prompt_tokens",
        "completion_tokens",
        "generated_answer_chars",
        "generated_answer_words_approx",
        "error_notes",
    ]
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
        "tokens_generated",
    ]
    system_fields = list(system_rows[0])
    repetition_fields = list(repetition_rows[0])

    blind_csv = OUTPUT / f"full_benchmark_blind_scoring_{OUTPUT_STEM}.csv"
    blind_rep1_csv = OUTPUT / f"full_benchmark_blind_scoring_rep1_only_{OUTPUT_STEM}.csv"
    key_csv = OUTPUT / f"full_benchmark_blind_model_key_{OUTPUT_STEM}.csv"
    finish_csv = OUTPUT / f"full_benchmark_finish_reason_audit_{OUTPUT_STEM}.csv"
    source_csv = OUTPUT / f"full_benchmark_source_consistency_audit_{OUTPUT_STEM}.csv"
    source_summary_csv = OUTPUT / f"full_benchmark_source_consistency_summary_{OUTPUT_STEM}.csv"
    memory_csv = OUTPUT / f"full_benchmark_memory_audit_{OUTPUT_STEM}.csv"
    repetition_csv = OUTPUT / f"full_benchmark_repetition_consistency_{OUTPUT_STEM}.csv"
    system_csv = OUTPUT / f"full_benchmark_system_summary_{OUTPUT_STEM}.csv"

    write_csv(blind_csv, blind_fields, blind_rows)
    write_csv(
        blind_rep1_csv,
        blind_fields,
        [row for row in blind_rows if row["repetition"] == "1"],
    )
    write_csv(
        key_csv,
        ["blind_model_code", "model_config_id", "run_folder", "note"],
        [
            {
                "blind_model_code": blind_code_by_model[model_id],
                "model_config_id": model_id,
                "run_folder": RUN_FOLDERS[model_id],
                "note": "Do not open this key until blind scoring is complete.",
            }
            for model_id in model_ids
        ],
    )
    write_csv(finish_csv, finish_fields, finish_rows)
    write_csv(source_csv, source_fields, source_rows)
    write_csv(memory_csv, memory_fields, memory_rows)
    write_csv(repetition_csv, repetition_fields, repetition_rows)
    write_csv(system_csv, system_fields, system_rows)

    source_summary_rows = []
    inconsistent_questions = []
    for question_id in sorted(source_signatures):
        consistent = len(source_signatures[question_id]) == 1
        if not consistent:
            inconsistent_questions.append(question_id)
        row: dict[str, Any] = {
            "question_id": question_id,
            "consistent_all_models_and_repetitions": str(consistent),
            "unique_source_signatures_all_runs": len(source_signatures[question_id]),
        }
        for model_id in model_ids:
            row[f"unique_source_signatures_{model_id}"] = len(
                source_signatures_by_model[question_id][model_id]
            )
        source_summary_rows.append(row)
    write_csv(source_summary_csv, list(source_summary_rows[0]), source_summary_rows)

    identical_repetition_groups = sum(
        row["all_repetitions_exactly_identical"] == "True" for row in repetition_rows
    )
    total_repetition_groups = len(repetition_rows)

    summary_md = OUTPUT / f"full_benchmark_audit_summary_{OUTPUT_STEM}.md"
    lines = [
        "# Final C1-C6 Benchmark Audit Summary",
        "",
        "**Created:** 2026-06-24",
        f"**Blind randomisation seed:** `{RANDOM_SEED}`",
        "**Generation seed:** `42`",
        "**Generation limit:** `max_tokens=512`",
        "",
        "## Scope",
        "",
        f"- Configurations: {len(model_ids)}",
        "- Questions per configuration: 40",
        "- Repetitions per question: 3",
        f"- Total generated answers: {len(finish_rows)}",
        f"- Rep-1 blind-scoring rows: {sum(row['repetition'] == '1' for row in blind_rows)}",
        "",
        "## System Summary",
        "",
        "| Config | Quant | Size MiB | Mean latency s | P95 latency s | Tokens/s | Mean RSS MiB | Mean output tokens | stop | length | errors |",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for row in system_rows:
        lines.append(
            f"| {row['model_config_id']} | {row['quantisation']} | "
            f"{float(row['model_file_size_mb']):.1f} | {row['mean_latency_seconds']:.3f} | "
            f"{row['p95_latency_seconds']:.3f} | {row['mean_tokens_per_second']:.2f} | "
            f"{row['mean_observed_rss_mb']:.2f} | {row['mean_output_tokens']:.2f} | "
            f"{row['finish_stop']} | {row['finish_length']} | {row['errors']} |"
        )

    lines.extend(
        [
            "",
            "## Retrieval Fairness",
            "",
            f"- Questions checked: {len(source_summary_rows)}",
            f"- Questions with inconsistent source signatures: {len(inconsistent_questions)}",
        ]
    )
    if inconsistent_questions:
        lines.append(f"- Inconsistent IDs: {', '.join(inconsistent_questions)}")
    else:
        lines.append(
            "- Every question used the same retrieved source signature across all six models and repetitions."
        )

    lines.extend(
        [
            "",
            "## Repetition Consistency",
            "",
            f"- Model-question groups checked: {total_repetition_groups}",
            (
                "- Groups with exactly identical answers across all three repetitions: "
                f"{identical_repetition_groups}"
            ),
            (
                "- Because the generation seed was fixed, exact repetition agreement is expected. "
                "Score repetition 1 for answer quality and retain all three repetitions for system-metric variability."
            ),
            "",
            "## Scoring Files",
            "",
            f"- Primary human scoring file: `{blind_rep1_csv.name}`",
            f"- All repetitions: `{blind_csv.name}`",
            f"- Hidden model key: `{key_csv.name}`",
            "- Do not open the model key before human scoring is complete.",
            "",
            "## Interpretation Rules",
            "",
            "- System metrics are now final-run measurements, but answer-quality conclusions remain pending scoring.",
            "- `observed_llama_server_rss_mb` is process RSS after requests, not a profiler-derived true peak.",
            "- Compare latency alongside output length and throughput; longer answers can increase latency.",
            "- Do not select a best model until the blinded quality scores have been combined with system metrics.",
        ]
    )
    summary_md.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"Wrote {blind_rep1_csv}")
    print(f"Wrote {blind_csv}")
    print(f"Wrote {key_csv}")
    print(f"Wrote {finish_csv}")
    print(f"Wrote {source_summary_csv}")
    print(f"Wrote {repetition_csv}")
    print(f"Wrote {system_csv}")
    print(f"Wrote {summary_md}")


if __name__ == "__main__":
    main()
