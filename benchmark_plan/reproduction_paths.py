"""Separate derived outputs from the retained dissertation evidence."""
import os
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[1]
RESULTS = PROJECT / "benchmark_results"


def output_directory():
    path = Path(os.environ.get("REPRO_OUTPUT_DIR", str(PROJECT / "reproduction_output"))).resolve()
    for protected in (RESULTS, PROJECT / "benchmark_plan", PROJECT / "provenance"):
        if path == protected or protected in path.parents:
            raise ValueError(f"Output must not overwrite retained evidence: {path}")
    path.mkdir(parents=True, exist_ok=True)
    return path
