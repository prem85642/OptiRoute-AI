# OptiRoute AI - Prometheus Setup Script
Write-Host "Setting up Prometheus for OptiRoute AI..." -ForegroundColor Cyan

$prometheusVersion = "2.47.0"
$prometheusUrl = "https://github.com/prometheus/prometheus/releases/download/v$prometheusVersion/prometheus-$prometheusVersion.windows-amd64.zip"
$downloadPath = "$PSScriptRoot\prometheus.zip"
$extractPath = "$PSScriptRoot\prometheus"

# Download Prometheus
if (-Not (Test-Path $extractPath)) {
    Write-Host "Downloading Prometheus $prometheusVersion..." -ForegroundColor Yellow
    Invoke-WebRequest -Uri $prometheusUrl -OutFile $downloadPath
    
    Write-Host "Extracting..." -ForegroundColor Yellow
    Expand-Archive -Path $downloadPath -DestinationPath $PSScriptRoot -Force
    Rename-Item -Path "$PSScriptRoot\prometheus-$prometheusVersion.windows-amd64" -NewName "prometheus"
    Remove-Item $downloadPath
}

Write-Host "Starting Prometheus on port 9090..." -ForegroundColor Green
Write-Host "Access Prometheus at: http://localhost:9090" -ForegroundColor Cyan
Write-Host "Press Ctrl+C to stop" -ForegroundColor Yellow

Set-Location $extractPath
.\prometheus.exe --config.file="..\prometheus.yml" --storage.tsdb.path=".\data"
