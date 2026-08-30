param(
    [Parameter(Mandatory = $true)]
    [ValidateSet("C1", "C2", "C3", "C4", "C5", "C6")]
    [string]$ModelConfigId,

    [int]$Repetitions = 3,
    [int]$Limit = 0,
    [int]$MaxTokens = 512,
    [int]$Seed = 42,
    [switch]$UploadCorpus,
    [switch]$StopOnError
)

$ErrorActionPreference = "Stop"

$Root = "C:\Users\Crbd2\Desktop\Dissertation"
$Repo = Join-Path $Root "Jetson-Nano-RAG-LLM"
$Python = Join-Path $Repo "venv\Scripts\python.exe"
$LlamaDir = Join-Path $Root "llama.cpp"
$LlamaServer = Join-Path $LlamaDir "llama-server.exe"
$Runner = Join-Path $Root "dissertation_project\benchmark_plan\run_full_benchmark.py"
$LogDir = Join-Path $Root "dissertation_project\benchmark_results\service_logs"

$Models = @{
    C1 = @{
        Name = "Qwen2.5 0.5B Instruct"
        Quantisation = "Q4_K_M"
        File = "models/qwen2.5-0.5b-instruct-q4_k_m.gguf"
        Path = Join-Path $Repo "models\qwen2.5-0.5b-instruct-q4_k_m.gguf"
    }
    C2 = @{
        Name = "Llama 3.2 1B Instruct"
        Quantisation = "Q4_K_M"
        File = "models/Llama-3.2-1B-Instruct.Q4_K_M.gguf"
        Path = Join-Path $Repo "models\Llama-3.2-1B-Instruct.Q4_K_M.gguf"
    }
    C3 = @{
        Name = "Gemma 3 1B IT"
        Quantisation = "Q4_K_M"
        File = "models/gemma-3-1b-it.Q4_K_M.gguf"
        Path = Join-Path $Repo "models\gemma-3-1b-it.Q4_K_M.gguf"
    }
    C4 = @{
        Name = "Qwen2.5 1.5B Instruct"
        Quantisation = "Q2_K"
        File = "models/qwen2.5-1.5b-instruct-q2_k.gguf"
        Path = Join-Path $Repo "models\qwen2.5-1.5b-instruct-q2_k.gguf"
    }
    C5 = @{
        Name = "Qwen2.5 1.5B Instruct"
        Quantisation = "Q4_K_M"
        File = "models/qwen2.5-1.5b-instruct-q4_k_m.gguf"
        Path = Join-Path $Repo "models\qwen2.5-1.5b-instruct-q4_k_m.gguf"
    }
    C6 = @{
        Name = "Qwen2.5 1.5B Instruct"
        Quantisation = "Q8_0"
        File = "models/qwen2.5-1.5b-instruct-q8_0.gguf"
        Path = Join-Path $Repo "models\qwen2.5-1.5b-instruct-q8_0.gguf"
    }
}

function Assert-FileExists {
    param([string]$Path)

    if (-not (Test-Path -LiteralPath $Path)) {
        throw "Missing required file: $Path"
    }
}

function Assert-PortFree {
    param([int]$Port)

    $listeners = Get-NetTCPConnection -State Listen -LocalPort $Port -ErrorAction SilentlyContinue
    if ($listeners) {
        $listeners | ForEach-Object {
            $process = Get-Process -Id $_.OwningProcess -ErrorAction SilentlyContinue
            Write-Host "Port $Port is already in use by PID $($_.OwningProcess) $($process.ProcessName) $($process.Path)"
        }
        throw "Port $Port is already in use. Stop the conflicting process before running this benchmark helper."
    }
}

Assert-FileExists $Python
Assert-FileExists $LlamaServer
Assert-FileExists $Runner

$config = $Models[$ModelConfigId]
Assert-FileExists $config.Path

try {
    $backend = Invoke-WebRequest -UseBasicParsing -Uri "http://127.0.0.1:8000/docs" -TimeoutSec 5
    Write-Host "Backend is reachable: HTTP $($backend.StatusCode)"
}
catch {
    throw "FastAPI backend is not reachable at http://127.0.0.1:8000. Start it before running this helper."
}

Assert-PortFree 8080

New-Item -ItemType Directory -Force -Path $LogDir | Out-Null
$stamp = Get-Date -Format "yyyyMMdd_HHmmss"
$logFile = Join-Path $LogDir "llama_${ModelConfigId}_full_${stamp}.log"

$llamaArgs = @(
    "-m", $config.Path,
    "--port", "8080",
    "--ctx-size", "4096",
    "--parallel", "1",
    "--cache-ram", "0",
    "--no-cache-prompt",
    "--ctx-checkpoints", "0",
    "--seed", "$Seed",
    "--log-file", $logFile
)

$llama = Start-Process `
    -FilePath $LlamaServer `
    -ArgumentList $llamaArgs `
    -WorkingDirectory $LlamaDir `
    -WindowStyle Hidden `
    -PassThru

try {
    Write-Host "Started llama-server for $ModelConfigId with PID $($llama.Id)"

    $ready = $false
    foreach ($i in 1..30) {
        Start-Sleep -Seconds 2
        try {
            $health = Invoke-WebRequest -UseBasicParsing -Uri "http://127.0.0.1:8080/health" -TimeoutSec 3
            if ($health.Content -match "ok") {
                Write-Host "llama-server health OK after $($i * 2)s"
                $ready = $true
                break
            }
        }
        catch {
            if (-not (Get-Process -Id $llama.Id -ErrorAction SilentlyContinue)) {
                throw "llama-server exited before becoming healthy. Check log: $logFile"
            }
        }
    }

    if (-not $ready) {
        throw "llama-server did not become healthy. Check log: $logFile"
    }

    $runnerArgs = @(
        $Runner,
        "--model-config-id", $ModelConfigId,
        "--model-name", $config.Name,
        "--quantisation", $config.Quantisation,
        "--model-file", $config.File,
        "--repetitions", "$Repetitions",
        "--max-tokens", "$MaxTokens",
        "--seed", "$Seed",
        "--context-length", "4096"
    )

    if ($UploadCorpus) {
        $runnerArgs += "--upload-corpus"
    }
    if ($Limit -gt 0) {
        $runnerArgs += @("--limit", "$Limit")
    }
    if ($StopOnError) {
        $runnerArgs += "--stop-on-error"
    }

    & $Python @runnerArgs
}
finally {
    if (Get-Process -Id $llama.Id -ErrorAction SilentlyContinue) {
        Stop-Process -Id $llama.Id -Force
        Write-Host "Stopped llama-server PID $($llama.Id)"
    }
}
