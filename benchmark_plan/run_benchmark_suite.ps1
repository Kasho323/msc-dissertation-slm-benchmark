param(
    [string]$ModelConfigIds = "C1,C2,C3,C4,C5,C6",

    [string]$AppDir = "",
    [string]$LlamaDir = "",
    [string]$CorpusDir = "",
    [int]$Repetitions = 3,
    [int]$Limit = 0,
    [int]$MaxTokens = 512,
    [int]$Seed = 42,
    [switch]$StopOnError,
    [string]$TranscriptPath = ""
)

$ErrorActionPreference = "Stop"

$Root = Split-Path -Parent $PSScriptRoot
if (-not $AppDir) { $AppDir = Join-Path $Root ".runtime\rag-app" }
if (-not $LlamaDir) { $LlamaDir = Join-Path $Root ".runtime\llama.cpp" }
if (-not $CorpusDir) { $CorpusDir = Join-Path $Root "corpus" }
$Repo = $AppDir
$Python = Join-Path $Repo "venv\Scripts\python.exe"
$Helper = Join-Path $Root "benchmark_plan\run_benchmark_config.ps1"
$LogDir = Join-Path $Root "replication_runs\service_logs"
$AllowedConfigIds = @("C1", "C2", "C3", "C4", "C5", "C6")
$SelectedConfigIds = @(
    $ModelConfigIds.Split(",") |
        ForEach-Object { $_.Trim().ToUpperInvariant() } |
        Where-Object { $_ }
)

if (-not $SelectedConfigIds.Count) {
    throw "At least one model configuration must be selected."
}

foreach ($configId in $SelectedConfigIds) {
    if ($configId -notin $AllowedConfigIds) {
        throw "Unsupported model configuration: $configId"
    }
}

$transcriptStarted = $false
if ($TranscriptPath) {
    New-Item -ItemType Directory -Force -Path (Split-Path -Parent $TranscriptPath) | Out-Null
    Start-Transcript -Path $TranscriptPath -Force
    $transcriptStarted = $true
}

function Test-BackendReady {
    try {
        $response = Invoke-WebRequest -UseBasicParsing -Uri "http://127.0.0.1:8000/docs" -TimeoutSec 5
        return $response.StatusCode -eq 200
    }
    catch {
        return $false
    }
}

function Wait-BackendReady {
    param([System.Diagnostics.Process]$BackendProcess)

    foreach ($i in 1..120) {
        Start-Sleep -Seconds 2
        if (Test-BackendReady) {
            Write-Host "Backend ready after $($i * 2)s"
            return
        }
        if (-not (Get-Process -Id $BackendProcess.Id -ErrorAction SilentlyContinue)) {
            throw "Backend exited before becoming ready."
        }
        if ($i % 10 -eq 0) {
            Write-Host "Waiting for backend... $($i * 2)s"
        }
    }
    throw "Backend did not become ready."
}

if (Test-BackendReady) {
    throw "Port 8000 already has a reachable backend. Stop it before running the controlled suite."
}

New-Item -ItemType Directory -Force -Path $LogDir | Out-Null
New-Item -ItemType Directory -Force -Path (Join-Path $Repo "uploads") | Out-Null

$backend = Start-Process `
    -FilePath $Python `
    -ArgumentList @("-m", "uvicorn", "main:app", "--port", "8000") `
    -WorkingDirectory $Repo `
    -WindowStyle Hidden `
    -PassThru

try {
    Write-Host "Started shared FastAPI backend PID $($backend.Id)"
    Wait-BackendReady -BackendProcess $backend

    for ($i = 0; $i -lt $SelectedConfigIds.Count; $i++) {
        $configId = $SelectedConfigIds[$i]
        $helperArgs = @(
            "-NoProfile",
            "-ExecutionPolicy", "Bypass",
            "-File", $Helper,
            "-ModelConfigId", $configId,
            "-AppDir", $Repo,
            "-LlamaDir", $LlamaDir,
            "-CorpusDir", $CorpusDir,
            "-Repetitions", "$Repetitions",
            "-MaxTokens", "$MaxTokens",
            "-Seed", "$Seed"
        )

        if ($Limit -gt 0) {
            $helperArgs += @("-Limit", "$Limit")
        }
        if ($i -eq 0) {
            $helperArgs += "-UploadCorpus"
        }
        if ($StopOnError) {
            $helperArgs += "-StopOnError"
        }

        Write-Host "Running $configId ($($i + 1)/$($SelectedConfigIds.Count)) with the shared vector store."
        powershell.exe @helperArgs
        if ($LASTEXITCODE -ne 0) {
            throw "Benchmark helper failed for $configId with exit code $LASTEXITCODE"
        }
    }

    Write-Host "Controlled benchmark suite completed."
}
finally {
    if (Get-Process -Id $backend.Id -ErrorAction SilentlyContinue) {
        Stop-Process -Id $backend.Id -Force
        Write-Host "Stopped shared FastAPI backend PID $($backend.Id)"
    }
    if ($transcriptStarted) {
        Stop-Transcript
    }
}
