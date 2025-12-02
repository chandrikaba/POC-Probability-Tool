# Build Docker Images - PowerShell Script
# Run this script after installing Docker Desktop

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Deal Win Probability Tool - Docker Build" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Docker is installed
try {
    docker --version | Out-Null
    Write-Host "✓ Docker is installed" -ForegroundColor Green
} catch {
    Write-Host "✗ Docker is not installed!" -ForegroundColor Red
    Write-Host "Please install Docker Desktop from: https://www.docker.com/products/docker-desktop" -ForegroundColor Yellow
    exit 1
}

# Navigate to project root
$projectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $projectRoot

Write-Host ""
Write-Host "Building Docker images..." -ForegroundColor Yellow
Write-Host ""

# Build Streamlit UI
Write-Host "1. Building Streamlit UI image..." -ForegroundColor Cyan
docker build -f docker/Dockerfile.streamlit -t deal-win-probability-ui:latest .
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Streamlit UI image built successfully" -ForegroundColor Green
} else {
    Write-Host "✗ Failed to build Streamlit UI image" -ForegroundColor Red
    exit 1
}

Write-Host ""

# Build FastAPI
Write-Host "2. Building FastAPI image..." -ForegroundColor Cyan
docker build -f docker/Dockerfile.api -t deal-win-probability-api:latest .
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ FastAPI image built successfully" -ForegroundColor Green
} else {
    Write-Host "✗ Failed to build FastAPI image" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Build Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Available images:" -ForegroundColor Yellow
docker images | Select-String "deal-win"

Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "  1. Run with docker-compose: cd docker && docker-compose up -d" -ForegroundColor White
Write-Host "  2. Or run individually:" -ForegroundColor White
Write-Host "     - Streamlit: docker run -p 8501:8501 deal-win-probability-ui" -ForegroundColor White
Write-Host "     - API: docker run -p 8000:8000 deal-win-probability-api" -ForegroundColor White
Write-Host ""
Write-Host "Access the application:" -ForegroundColor Yellow
Write-Host "  - Streamlit UI: http://localhost:8501" -ForegroundColor White
Write-Host "  - FastAPI: http://localhost:8000" -ForegroundColor White
Write-Host "  - API Docs: http://localhost:8000/docs" -ForegroundColor White
