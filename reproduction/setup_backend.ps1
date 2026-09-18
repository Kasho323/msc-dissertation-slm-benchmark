param([string]$Python = "python", [string]$AppDir = "")
$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
if (-not $AppDir) { $AppDir = Join-Path $Root ".runtime\rag-app" }
$Commit = "e63300ab9514804889a27a71827041963b47b909"
& $Python -c "import sys; assert sys.version_info[:2] == (3,10), 'Use Python 3.10 for the recorded environment'"
if ($LASTEXITCODE -ne 0) { throw "Python 3.10 required" }
if (-not (Test-Path -LiteralPath $AppDir)) {
    git clone https://github.com/jackiewaang/Jetson-Nano-RAG-LLM.git $AppDir
    if ($LASTEXITCODE -ne 0) { throw "Backend clone failed" }
}
$Current = git -C $AppDir rev-parse HEAD
if ($Current -ne $Commit) {
    $Changes = git -C $AppDir status --porcelain
    if ($Changes) { throw "Existing backend has changes; use an empty AppDir instead" }
    git -C $AppDir checkout --detach $Commit
    if ($LASTEXITCODE -ne 0) { throw "Cannot select pinned backend commit" }
}
$VenvPython = Join-Path $AppDir "venv\Scripts\python.exe"
if (-not (Test-Path -LiteralPath $VenvPython)) {
    & $Python -m venv (Join-Path $AppDir "venv")
    if ($LASTEXITCODE -ne 0) { throw "Cannot create environment" }
}
& $VenvPython -m pip install -r (Join-Path $Root "requirements-experiment.txt")
if ($LASTEXITCODE -ne 0) { throw "Dependency installation failed" }
& $VenvPython -m pip check
if ($LASTEXITCODE -ne 0) { throw "Dependency conflicts; do not run the experiment" }
New-Item -ItemType Directory -Force -Path (Join-Path $AppDir "uploads") | Out-Null
New-Item -ItemType Directory -Force -Path (Join-Path $AppDir "models") | Out-Null
Write-Host "Pinned backend ready. Acquire models/runtime and check corpus before running the suite."
