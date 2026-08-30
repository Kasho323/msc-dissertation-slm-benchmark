param(
    [Parameter(Mandatory = $true)]
    [ValidateSet("C1", "C2", "C3", "C4", "C5", "C6")]
    [string]$ModelConfigId,

    [int]$Repetitions = 3,
    [int]$Limit = 0,
    [int]$MaxTokens = 512,
    [int]$Seed = 42,
    [switch]$UploadCorpus,
    [switch]$StopOnError,
    [string]$TranscriptPath = ""
)

$ErrorActionPreference = "Stop"

$Root = "C:\Users\Crbd2\Desktop\Dissertation"
$Repo = Join-Path $Root "Jetson-Nano-RAG-LLM"
$Python = Join-Path $Repo "venv\Scripts\python.exe"
$Helper = Join-Path $Root "dissertation_project\benchmark_plan\run_benchmark_config.ps1"

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

$transcriptStarted = $false
if ($TranscriptPath) {
    New-Item -ItemType Directory -Force -Path (Split-Path -Parent $TranscriptPath) | Out-Null
    Start-Transcript -Path $TranscriptPath -Force
    $transcriptStarted = $true
}

$backend = $null
$startedBackend = $false

try {
    if (Test-BackendReady) {
        Write-Host "Using existing FastAPI backend on port 8000."
    }
    else {
        Write-Host "Starting temporary FastAPI backend on port 8000."
        $backend = Start-Process `
            -FilePath $Python `
            -ArgumentList @("-m", "uvicorn", "main:app", "--port", "8000") `
            -WorkingDirectory $Repo `
            -WindowStyle Hidden `
            -PassThru
        $startedBackend = $true
        Write-Host "Temporary backend PID: $($backend.Id)"
        Wait-BackendReady -BackendProcess $backend
    }

    $helperArgs = @(
        "-NoProfile",
        "-ExecutionPolicy", "Bypass",
        "-File", $Helper,
        "-ModelConfigId", $ModelConfigId,
        "-Repetitions", "$Repetitions",
        "-MaxTokens", "$MaxTokens",
        "-Seed", "$Seed"
    )

    if ($Limit -gt 0) {
        $helperArgs += @("-Limit", "$Limit")
    }
    if ($UploadCorpus) {
        $helperArgs += "-UploadCorpus"
    }
    if ($StopOnError) {
        $helperArgs += "-StopOnError"
    }

    Write-Host "Running full benchmark helper for $ModelConfigId."
    powershell.exe @helperArgs
    Write-Host "Benchmark helper finished for $ModelConfigId."
}
finally {
    if ($startedBackend -and $backend -and (Get-Process -Id $backend.Id -ErrorAction SilentlyContinue)) {
        Stop-Process -Id $backend.Id -Force
        Write-Host "Stopped temporary backend PID $($backend.Id)"
    }
    if ($transcriptStarted) {
        Stop-Transcript
    }
}
