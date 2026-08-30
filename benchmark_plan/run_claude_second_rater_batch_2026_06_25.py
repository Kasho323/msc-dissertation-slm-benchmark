from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
BATCH_DIR = (
    ROOT
    / "dissertation_project"
    / "benchmark_results"
    / "ai_second_rater_batches_2026-06-25"
)
CLAUDE = Path(r"C:\Users\Crbd2\AppData\Roaming\npm\claude.cmd")

SCHEMA = {
    "type": "object",
    "properties": {
        "ratings": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "blind_answer_id": {"type": "string"},
                    "relevance": {"type": "integer", "minimum": 0, "maximum": 5},
                    "correctness": {"type": "integer", "minimum": 0, "maximum": 5},
                    "faithfulness_to_source": {
                        "type": "integer",
                        "minimum": 0,
                        "maximum": 5,
                    },
                    "completeness": {"type": "integer", "minimum": 0, "maximum": 5},
                    "hallucination_risk": {
                        "type": "integer",
                        "minimum": 0,
                        "maximum": 5,
                    },
                    "source_grounding": {
                        "type": "integer",
                        "minimum": 0,
                        "maximum": 5,
                    },
                    "scoring_notes": {"type": "string", "maxLength": 300},
                },
                "required": [
                    "blind_answer_id",
                    "relevance",
                    "correctness",
                    "faithfulness_to_source",
                    "completeness",
                    "hallucination_risk",
                    "source_grounding",
                    "scoring_notes",
                ],
                "additionalProperties": False,
            },
        }
    },
    "required": ["ratings"],
    "additionalProperties": False,
}

RUBRIC = """
You are the independent AI second rater for an MSc dissertation benchmark.

The model identities are hidden. Do not infer or mention model identity. Score each
generated answer only against its question, expected-answer notes, and evidence
location.

Use integer scores from 0 to 5:
0 absent/unusable; 1 very poor; 2 weak; 3 acceptable; 4 good; 5 excellent.

Dimensions:
- relevance: directly addresses the question.
- correctness: factually agrees with expected-answer notes and evidence.
- faithfulness_to_source: claims are supported by the supplied evidence description.
- completeness: covers the important expected points.
- hallucination_risk: higher is better; 5 means no unsupported claims observed.
- source_grounding: answer is clearly tied to the supplied material.

Rules:
- Do not reward length.
- Penalise repetition, wrong terminology, unsupported detail, vagueness, and missing points.
- If the answer cuts off mid-sentence, lower completeness and mention truncation.
- A concise refusal can be faithful but may score poorly for relevance/completeness.
- Apply the rubric consistently across all rows.
- Return exactly one rating for every input blind_answer_id, in input order.
- Keep scoring_notes under 45 words and explain the main reason for the scores.
""".strip()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("batch_number", type=int)
    args = parser.parse_args()

    input_path = BATCH_DIR / f"batch_{args.batch_number:02d}.json"
    output_path = BATCH_DIR / f"batch_{args.batch_number:02d}_ratings.json"
    raw_path = BATCH_DIR / f"batch_{args.batch_number:02d}_claude_raw.json"

    rows = json.loads(input_path.read_text(encoding="utf-8"))
    prompt = (
        RUBRIC
        + "\n\nRate the following blind rows:\n"
        + json.dumps(rows, ensure_ascii=False)
    )

    command = [
        str(CLAUDE),
        "--print",
        "--safe-mode",
        "--tools",
        "",
        "--no-session-persistence",
        "--model",
        "sonnet",
        "--effort",
        "medium",
        "--output-format",
        "json",
        "--json-schema",
        json.dumps(SCHEMA, separators=(",", ":")),
    ]
    completed = subprocess.run(
        command,
        input=prompt,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        timeout=1800,
        check=False,
    )
    if completed.returncode != 0:
        raise RuntimeError(
            f"Claude exited with {completed.returncode}:\n{completed.stderr}"
        )

    raw_path.write_text(completed.stdout, encoding="utf-8")
    envelope = json.loads(completed.stdout)
    ratings_object = envelope.get("structured_output")
    if ratings_object is None:
        result = envelope.get("result")
        if isinstance(result, str):
            ratings_object = json.loads(result)
    if not isinstance(ratings_object, dict):
        raise ValueError("Claude response did not contain structured ratings.")

    ratings = ratings_object.get("ratings", [])
    expected_ids = [row["blind_answer_id"] for row in rows]
    returned_ids = [row["blind_answer_id"] for row in ratings]
    if returned_ids != expected_ids:
        raise ValueError("Returned answer IDs do not exactly match input order.")

    model_usage = envelope.get("modelUsage", {})
    actual_models = list(model_usage)
    actual_model = ", ".join(actual_models) if actual_models else "unknown"

    for rating in ratings:
        scores = [
            rating["relevance"],
            rating["correctness"],
            rating["faithfulness_to_source"],
            rating["completeness"],
            rating["hallucination_risk"],
            rating["source_grounding"],
        ]
        rating["average_quality_score"] = round(sum(scores) / len(scores), 3)
        rating["rated_by"] = f"{actual_model} via Claude Code 2.1.178"
        rating["rated_date"] = "2026-06-25"

    output_path.write_text(
        json.dumps(ratings, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"Wrote {len(ratings)} ratings to {output_path}")


if __name__ == "__main__":
    main()
