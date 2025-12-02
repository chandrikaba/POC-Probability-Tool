# Project Cleanup Script
# This script removes unwanted files and folders from the project

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Project Cleanup - Deal Win Probability Tool" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$projectRoot = "c:\Users\chand\OneDrive\Documents\Chandrika\Makers Lab\AI Based Deal Win Probability\POC - Probability Tool"
Set-Location $projectRoot

# Items to remove
$itemsToRemove = @(
    # Duplicate/old files in root
    "Dockerfile",                    # Moved to docker/ folder
    "docker-compose.yml",            # Moved to docker/ folder
    "main.py",                       # Unused file
    "verify_structure.py",           # Temporary verification script
    "MODULARIZATION_SUMMARY.md",     # Old documentation
    "RESTRUCTURING_GUIDE.md",        # Old documentation
    
    # Duplicate backend folder (we use api.py directly)
    "backend",
    
    # Old base-data folder
    "base-data",
    
    # Cache folders
    "__pycache__",
    "data\cache",
    
    # Old prediction files (keep only latest and synthetic data)
    "data\output\predictions.xlsx",
    "data\output\predictions_1764250939.xlsx",
    "data\output\predictions_1764251397.xlsx",
    "data\output\predictions_20251127_212731.xlsx",
    "data\output\predictions_20251128_092416.xlsx",
    "data\output\predictions_20251128_092420.xlsx",
    "data\output\predictions_20251128_101325.xlsx",
    "data\output\predictions_20251128_105300.xlsx",
    "data\output\predictions_20251128_110706.xlsx",
    "data\output\predictions_20251128_113242.xlsx",
    "data\output\predictions_20251128_115037.xlsx",
    "data\output\predictions_20251128_115048.xlsx",
    "data\output\predictions_20251128_115052.xlsx",
    "data\output\predictions_20251128_120047.xlsx",
    "data\output\synthetic_deals_backup.xlsx"
)

Write-Host "Files and folders to be removed:" -ForegroundColor Yellow
Write-Host ""

$totalSize = 0
$itemCount = 0

foreach ($item in $itemsToRemove) {
    $fullPath = Join-Path $projectRoot $item
    if (Test-Path $fullPath) {
        $itemCount++
        if (Test-Path $fullPath -PathType Container) {
            $size = (Get-ChildItem $fullPath -Recurse -File | Measure-Object -Property Length -Sum).Sum
            Write-Host "  [FOLDER] $item" -ForegroundColor Red
        }
        else {
            $size = (Get-Item $fullPath).Length
            Write-Host "  [FILE]   $item" -ForegroundColor Red
        }
        $totalSize += $size
    }
}

Write-Host ""
Write-Host "Total items to remove: $itemCount" -ForegroundColor Yellow
Write-Host "Total size to free: $([math]::Round($totalSize / 1MB, 2)) MB" -ForegroundColor Yellow
Write-Host ""

# Ask for confirmation
$confirmation = Read-Host "Do you want to proceed with cleanup? (yes/no)"

if ($confirmation -eq "yes") {
    Write-Host ""
    Write-Host "Starting cleanup..." -ForegroundColor Green
    Write-Host ""
    
    $removedCount = 0
    $failedCount = 0
    
    foreach ($item in $itemsToRemove) {
        $fullPath = Join-Path $projectRoot $item
        if (Test-Path $fullPath) {
            try {
                Remove-Item -Path $fullPath -Recurse -Force
                Write-Host "  ✓ Removed: $item" -ForegroundColor Green
                $removedCount++
            }
            catch {
                Write-Host "  ✗ Failed to remove: $item" -ForegroundColor Red
                Write-Host "    Error: $($_.Exception.Message)" -ForegroundColor Red
                $failedCount++
            }
        }
    }
    
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host "Cleanup Complete!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host "  Items removed: $removedCount" -ForegroundColor Green
    Write-Host "  Items failed: $failedCount" -ForegroundColor $(if ($failedCount -gt 0) { "Red" } else { "Green" })
    Write-Host ""
    Write-Host "Remaining project structure:" -ForegroundColor Yellow
    Write-Host ""
    
    # Show clean directory structure
    tree /F /A
    
}
else {
    Write-Host ""
    Write-Host "Cleanup cancelled." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Note: The following essential files and folders are preserved:" -ForegroundColor Cyan
Write-Host "  • app.py, api.py - Main application files" -ForegroundColor White
Write-Host "  • src/ - Core scripts (generate, train, predict)" -ForegroundColor White
Write-Host "  • models/ - Trained models" -ForegroundColor White
Write-Host "  • data/output/synthetic_deals.xlsx - Training data" -ForegroundColor White
Write-Host "  • data/output/predictions_20251128_144345.xlsx - Latest prediction" -ForegroundColor White
Write-Host "  • docker/ - Docker deployment files" -ForegroundColor White
Write-Host "  • docs/ - Documentation" -ForegroundColor White
Write-Host "  • requirements.txt - Dependencies" -ForegroundColor White
Write-Host ""
