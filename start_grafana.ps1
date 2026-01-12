# OptiRoute AI - Grafana Setup Script
Write-Host "Setting up Grafana for OptiRoute AI..." -ForegroundColor Cyan

$grafanaVersion = "10.2.2"
$grafanaUrl = "https://dl.grafana.com/oss/release/grafana-$grafanaVersion.windows-amd64.zip"
$downloadPath = "$PSScriptRoot\grafana.zip"
$extractPath = "$PSScriptRoot\grafana"

# Download Grafana
if (-Not (Test-Path $extractPath)) {
    Write-Host "Downloading Grafana $grafanaVersion..." -ForegroundColor Yellow
    Invoke-WebRequest -Uri $grafanaUrl -OutFile $downloadPath
    
    Write-Host "Extracting..." -ForegroundColor Yellow
    Expand-Archive -Path $downloadPath -DestinationPath $PSScriptRoot -Force
    Rename-Item -Path "$PSScriptRoot\grafana-$grafanaVersion" -NewName "grafana"
    Remove-Item $downloadPath
}

Write-Host "Starting Grafana on port 3000..." -ForegroundColor Green
Write-Host "Access Grafana at: http://localhost:3000" -ForegroundColor Cyan
Write-Host "Default credentials: admin / admin" -ForegroundColor Yellow
Write-Host "Press Ctrl+C to stop" -ForegroundColor Yellow

Set-Location "$extractPath\bin"
.\grafana-server.exe
