param(
    [switch]$Force
)

$ErrorActionPreference = "Stop"

$Root = "C:\Users\Crbd2\Desktop\Dissertation"
$ModelDir = Join-Path $Root "Jetson-Nano-RAG-LLM\models"

$Files = @(
    @{
        Name = "qwen2.5-1.5b-instruct-q2_k.gguf"
        Url = "https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct-GGUF/resolve/main/qwen2.5-1.5b-instruct-q2_k.gguf?download=true"
        MinimumBytes = 700MB
    },
    @{
        Name = "qwen2.5-1.5b-instruct-q4_k_m.gguf"
        Url = "https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct-GGUF/resolve/main/qwen2.5-1.5b-instruct-q4_k_m.gguf?download=true"
        MinimumBytes = 1GB
    },
    @{
        Name = "qwen2.5-1.5b-instruct-q8_0.gguf"
        Url = "https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct-GGUF/resolve/main/qwen2.5-1.5b-instruct-q8_0.gguf?download=true"
        MinimumBytes = 1.7GB
    }
)

New-Item -ItemType Directory -Force -Path $ModelDir | Out-Null

foreach ($file in $Files) {
    $destination = Join-Path $ModelDir $file.Name

    if ((Test-Path -LiteralPath $destination) -and -not $Force) {
        $existing = Get-Item -LiteralPath $destination
        if ($existing.Length -ge $file.MinimumBytes) {
            Write-Host "Already present: $($file.Name) ($([math]::Round($existing.Length / 1MB, 1)) MiB)"
            continue
        }
        Write-Host "Existing file is incomplete; resuming: $($file.Name)"
    }

    Write-Host "Downloading official Qwen file: $($file.Name)"
    & curl.exe `
        --fail `
        --location `
        --retry 5 `
        --retry-delay 3 `
        --continue-at - `
        --output $destination `
        $file.Url

    if ($LASTEXITCODE -ne 0) {
        throw "Download failed for $($file.Name) with curl exit code $LASTEXITCODE"
    }

    $downloaded = Get-Item -LiteralPath $destination
    if ($downloaded.Length -lt $file.MinimumBytes) {
        throw "Downloaded file is unexpectedly small: $destination"
    }

    Write-Host "Verified size: $($file.Name) ($([math]::Round($downloaded.Length / 1MB, 1)) MiB)"
}

Write-Host "All Qwen2.5 1.5B quantisation files are present."
