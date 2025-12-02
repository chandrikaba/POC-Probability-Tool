# Run Docker Containers - PowerShell Script

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Deal Win Probability Tool - Docker Run" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Docker is running
try {
    docker ps | Out-Null
    Write-Host "✓ Docker is running" -ForegroundColor Green
} catch {
    Write-Host "✗ Docker is not running!" -ForegroundColor Red
    Write-Host "Please start Docker Desktop" -ForegroundColor Yellow
    exit 1
}

# Navigate to docker directory
$dockerDir = $PSScriptRoot
Set-Location $dockerDir

Write-Host ""
Write-Host "Starting containers with docker-compose..." -ForegroundColor Yellow
Write-Host ""

# Run docker-compose
docker-compose up -d

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host "Containers Started Successfully!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host ""
    
    # Show running containers
    Write-Host "Running containers:" -ForegroundColor Yellow
    docker-compose ps
    
    Write-Host ""
    Write-Host "Access the application:" -ForegroundColor Yellow
    Write-Host "  - Streamlit UI: http://localhost:8501" -ForegroundColor Green
    Write-Host "  - FastAPI: http://localhost:8000" -ForegroundColor Green
    Write-Host "  - API Docs: http://localhost:8000/docs" -ForegroundColor Green
    
    Write-Host ""
    Write-Host "Useful commands:" -ForegroundColor Yellow
    Write-Host "  - View logs: docker-compose logs -f" -ForegroundColor White
    Write-Host "  - Stop: docker-compose stop" -ForegroundColor White
    Write-Host "  - Stop and remove: docker-compose down" -ForegroundColor White
    Write-Host "  - Restart: docker-compose restart" -ForegroundColor White
} else {
    Write-Host ""
    Write-Host "✗ Failed to start containers" -ForegroundColor Red
    Write-Host "Check the error messages above" -ForegroundColor Yellow
    exit 1
}
