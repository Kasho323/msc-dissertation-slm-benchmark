"""Recompute headline results from retained evidence; never re-run an AI judge.

Python 3.10+. The default check uses only the standard library.
--full additionally runs the original analyses (see requirements-analysis.txt).
"""
import argparse
from collections import Counter, defaultdict
import csv
import hashlib
import importlib.util
import json
import math
import os
from pathlib import Path
import statistics
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "benchmark_plan"))
from reproduction_paths import output_directory

RESULTS = ROOT / "benchmark_results"
DIMS = ["relevance", "correctness", "faithfulness_to_source", "completeness",
        "hallucination_risk", "source_grounding"]
RUNS = dict(zip([f"C{i}" for i in range(1, 7)],
               ["211524", "213220", "215407", "221531", "223538", "225248"]))


def read_csv(path):
    with path.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def require(condition, message):
    if not condition:
        raise ValueError(message)


def score(row):
    return sum(float(row[d]) for d in DIMS) / 6


def verify_retained_files():
    manifest = json.loads((ROOT / "provenance" / "retained_files_sha256.json").read_text())
    for name, expected in manifest.items():
        path = ROOT / name
        require(path.is_file(), f"Missing retained evidence: {name}")
        require(hashlib.sha256(path.read_bytes()).hexdigest() in expected,
                f"Retained evidence changed: {name}")
    return len(manifest)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--full", action="store_true")
    parser.add_argument("--output-dir", type=Path, default=ROOT / "reproduction_output")
    args = parser.parse_args()
    os.environ["REPRO_OUTPUT_DIR"] = str(args.output_dir.resolve())
    out = output_directory()
    checked = verify_retained_files()
    questions = read_csv(ROOT / "benchmark_plan" / "question_set_template.csv")
    qids = {q["question_id"] for q in questions}
    require(len(qids) == len(questions) == 40, "Expected frozen 40-question set")
    key = {r["blind_model_code"]: r["model_config_id"] for r in
           read_csv(RESULTS / "full_benchmark_blind_model_key_C1_C6_2026-06-24.csv")}
    ai = read_csv(RESULTS / "ai_second_rater_codex_gpt_C1_C6_2026-06-25.csv")
    human = read_csv(RESULTS / "human_independent_CLEAN_30_HUMAN_SCORED_2026-07-09.csv")
    require(len(ai) == 240 and len(human) == 30, "Wrong AI/human sample sizes")
    ai_by_id = {r["blind_answer_id"]: r for r in ai}
    require(len(ai_by_id) == 240, "Duplicate AI answer IDs")
    require(len({r['blind_answer_id'] for r in human}) == 30, "Duplicate human IDs")
    by_cfg = defaultdict(dict)
    for r in ai:
        require(all(0 <= float(r[d]) <= 5 for d in DIMS), "AI score outside scale")
        cfg = key[r["blind_model_code"]]
        require(r["question_id"] not in by_cfg[cfg], "Duplicate configuration/question")
        by_cfg[cfg][r["question_id"]] = r

    system = {r["model_config_id"]: r for r in
              read_csv(RESULTS / "full_benchmark_system_summary_C1_C6_2026-06-24.csv")}
    summary = {}
    total_raw = 0
    q2_reasons = {}
    for cfg, stamp in RUNS.items():
        folder = RESULTS / f"full_benchmark_{cfg}_20260624_{stamp}"
        rows = read_csv(folder / "model_answer_log.csv")
        manifest = read_csv(folder / "run_manifest.csv")[0]
        require(manifest['status'] == 'completed' and manifest['max_tokens'] == '512'
                and manifest['repetition_count'] == '3', f"Wrong final run: {cfg}")
        require(len(rows) == 120, f"Expected 120 answers: {cfg}")
        require(set(by_cfg[cfg]) == qids, f"Incomplete quality coverage: {cfg}")
        groups = defaultdict(list)
        for r in rows:
            require(not r["error_notes"], f"Experimental error: {cfg}/{r['question_id']}")
            groups[r['question_id']].append(r)
        require(set(groups) == qids, f"Incomplete run questions: {cfg}")
        for q, group in groups.items():
            require({r['repetition'] for r in group} == {'1','2','3'} and len(group) == 3,
                    f"Missing repetitions: {cfg}/{q}")
            require(len({r['generated_answer'] for r in group}) == 1,
                    f"Repetition text differs: {cfg}/{q}")
            if cfg == 'C4':
                require(len({r['finish_reason'] for r in group}) == 1, 'Q2 finish differs')
                q2_reasons[q] = group[0]['finish_reason']
        raw_json = list((folder / 'raw_responses').glob('*.json'))
        require(len(raw_json) == 120, f"Missing raw responses: {cfg}")
        for p in raw_json:
            json.loads(p.read_text(encoding='utf-8-sig'))
        total_raw += len(raw_json)
        means = {"latency_seconds": statistics.mean(float(r['latency_seconds']) for r in rows),
                 "tokens_per_second": statistics.mean(float(r['tokens_per_second']) for r in rows),
                 "rss_mib": statistics.mean(float(r['peak_memory_mb']) for r in rows)}
        for metric, field, precision in [('latency_seconds','mean_latency_seconds',4),
                                          ('tokens_per_second','mean_tokens_per_second',2),
                                          ('rss_mib','mean_observed_rss_mb',2)]:
            require(abs(means[metric]-float(system[cfg][field])) <= 0.5*10**(-precision)+1e-9,
                    f"System summary disagrees with raw logs: {cfg}/{metric}")
        truncated = sum(r['finish_reason'] == 'length' for r in rows)
        require(truncated == int(system[cfg]['finish_length']), f"Truncation mismatch: {cfg}")
        summary[cfg] = {"n_answers":40, "quality_mean": statistics.mean(score(r) for r in by_cfg[cfg].values()),
                        **means, "truncated_of_120": truncated}

    spec = importlib.util.spec_from_file_location('intervals', ROOT/'benchmark_plan'/'analyze_agreement_intervals_2026-08-23.py')
    intervals = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(intervals)
    for r in human:
        require(r['blind_answer_id'] in ai_by_id, 'Unmatched human answer')
        require(all(0 <= float(r[d]) <= 5 for d in DIMS), "Human score outside scale")
    h = [score(r) for r in human]
    a = [score(ai_by_id[r['blind_answer_id']]) for r in human]
    rho = intervals.spearman(h, a)
    require(math.isclose(rho,0.7992658480979864,abs_tol=1e-12), 'Human-AI rho changed')
    expected = [3.0708333333333333,3.1,3.575,2.683333333333333,3.433333333333333,3.445833333333333]
    for cfg, value in zip(RUNS, expected):
        require(math.isclose(summary[cfg]['quality_mean'],value,abs_tol=1e-12), f"Quality changed: {cfg}")
    natural = [q for q,r in q2_reasons.items() if r == 'stop']
    require(len(natural) == 32, "Q2 subset changed")
    q035 = {cfg: statistics.mean(score(r) for q,r in by_cfg[cfg].items() if q!='Q035')
            for cfg in ['C5','C6']}
    require(q035['C5'] > q035['C6'], 'Q035 ordering reversal not reproduced')
    report = {"retained_files_verified":checked, "raw_json_responses":total_raw,
              "ai_rated_answers":len(ai), "human_rated_answers":len(human),
              "configurations":summary, "human_ai_spearman":rho,
              "q035_excluded_quality":q035,
              "q2_natural_subset_n":len(natural),
              "q2_natural_subset_quality": {cfg:statistics.mean(score(by_cfg[cfg][q]) for q in natural)
                                             for cfg in ['C4','C5']}}
    (out/'headline_results.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(f'PASS: {checked} retained files, 720 raw answers, 240 AI scores, 30 human scores.')
    for cfg,r in summary.items():print(f"{cfg}: quality={r['quality_mean']:.6f}, tok/s={r['tokens_per_second']:.2f}, RSS MiB={r['rss_mib']:.2f}")
    print(f'Human-AI Spearman rho: {rho:.6f}; Q035 excluded: {q035}')
    if args.full:
        scripts = ['prepare_final_scoring_and_audits_2026_06_24.py',
                   'build_final_results_2026_07_09.py','analyze_clean30_agreement_2026_07_09.py',
                   'analyze_agreement_intervals_2026-08-23.py','analyze_q2_truncation_sensitivity_2026_07_23.py']
        for script in scripts:
            run = subprocess.run([sys.executable,str(ROOT/'benchmark_plan'/script)],
                                 cwd=ROOT, text=True, capture_output=True)
            (out/(script+'.log')).write_text(run.stdout+'\n'+run.stderr,encoding='utf-8')
            require(run.returncode == 0, f"{script} failed; see {out/(script+'.log')}")
            print(f'PASS: {script}')
        for name in ['full_benchmark_system_summary_C1_C6_2026-06-24.csv',
                     'full_benchmark_blind_model_key_C1_C6_2026-06-24.csv',
                     'final_quality_by_config_2026-07-09.csv']:
            require(read_csv(out/name) == read_csv(RESULTS/name), f'Regenerated table differs: {name}')
        print('PASS: regenerated system summary, blinding key and quality table match the archived tables.')
    verify_retained_files()
    print(f'Outputs: {out}; retained inputs unchanged.')


if __name__ == '__main__':
    main()
