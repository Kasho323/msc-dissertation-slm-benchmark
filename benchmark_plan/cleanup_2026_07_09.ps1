# Cleanup 2026-07-09: move superseded/aborted/contaminated files to _archive_superseded.
# Nothing is hard-deleted except __pycache__. Final data (6/24 runs, AI ratings,
# CLEAN_30 human scores, audits, final results) is untouched.

$base = "C:\Users\Crbd2\Desktop\Dissertation\dissertation_project"
$res  = Join-Path $base "benchmark_results"
$plan = Join-Path $base "benchmark_plan"
$arc  = Join-Path $base "_archive_superseded"
New-Item -ItemType Directory -Force -Path $arc | Out-Null

function MoveSafe($path) {
  if (Test-Path $path) { Move-Item -Force $path $arc; Write-Output ("archived: " + (Split-Path $path -Leaf)) }
}

# 1. aborted C1 runs (6/19, only 1 question each)
MoveSafe (Join-Path $res "full_benchmark_C1_20260619_223429")
MoveSafe (Join-Path $res "full_benchmark_C1_20260619_224035")

# 2. superseded 6/19 full runs (max_tokens=200, replaced by 6/24 512 runs)
MoveSafe (Join-Path $res "full_benchmark_C1_20260619_224126")
MoveSafe (Join-Path $res "full_benchmark_C2_20260619_225653")
MoveSafe (Join-Path $res "full_benchmark_C3_20260619_231534")
"full_benchmark_system_summary_C1_C2_C3_2026-06-19.csv",
"full_benchmark_system_summary_C1_C2_C3_2026-06-19.md",
"full_benchmark_scoring_review_C1_C2_C3_2026-06-19.csv",
"full_benchmark_scoring_review_summary_2026-06-19.md",
"full_benchmark_blind_scoring_C1_C2_C3_2026-06-20.csv",
"full_benchmark_blind_scoring_rep1_only_C1_C2_C3_2026-06-20.csv",
"full_benchmark_finish_reason_audit_C1_C2_C3_2026-06-20.csv",
"full_benchmark_blind_model_key_C1_C2_C3_2026-06-20.csv",
"full_benchmark_source_consistency_audit_C1_C2_C3_2026-06-20.csv",
"full_benchmark_source_consistency_summary_C1_C2_C3_2026-06-20.csv",
"full_benchmark_memory_sanity_audit_C1_C2_C3_2026-06-20.csv",
"full_benchmark_audit_summary_C1_C2_C3_2026-06-20.md" | ForEach-Object { MoveSafe (Join-Path $res $_) }

# 3. aborted/pilot 6/24 run folders (finals are C1_211524 C2_213220 C3_215407 C4_221531 C5_223538 C6_225248)
"full_benchmark_C4_20260624_205901","full_benchmark_C5_20260624_210016","full_benchmark_C6_20260624_210126",
"full_benchmark_C4_20260624_210711","full_benchmark_C5_20260624_210813","full_benchmark_C6_20260624_210903" |
  ForEach-Object { MoveSafe (Join-Path $res $_) }

# 4. CONTAMINATED fake-human file + its misleading agreement report -> rename with warning
if (Test-Path (Join-Path $res "human_stage1_independent_60_HUMAN_SCORED_archived.csv")) {
  Move-Item -Force (Join-Path $res "human_stage1_independent_60_HUMAN_SCORED_archived.csv") (Join-Path $arc "VOID_DO_NOT_USE_ai_copied_not_human_60.csv")
  Write-Output "archived+renamed: VOID_DO_NOT_USE_ai_copied_not_human_60.csv"
}
MoveSafe (Join-Path $res "stage1_agreement_report_2026-06-30.md")

# 5. unused two-stage files (superseded by CLEAN_30 + Design A)
MoveSafe (Join-Path $res "human_stage1_independent_60_2026-06-29.csv")
MoveSafe (Join-Path $res "human_stage2_ai_assisted_180_2026-06-29.csv")
MoveSafe (Join-Path $res "two_stage_scoring_split_2026-06-29.md")

# 6. superseded analysis scripts (keep for audit trail, out of the way)
"analyze_stage1_agreement_2026_06_30.py","prepare_two_stage_human_scoring_2026_06_29.py",
"compare_human_and_ai_scores_2026_06_25.py","compare_independent_human_subset_with_ai_2026_06_29.py" |
  ForEach-Object { MoveSafe (Join-Path $plan $_) }

# 7. hard-delete python cache only
if (Test-Path (Join-Path $plan "__pycache__")) {
  Remove-Item -Recurse -Force (Join-Path $plan "__pycache__")
  Write-Output "deleted: __pycache__"
}

Write-Output ""
Write-Output ("Done. Archive folder: " + $arc)
