# AUTOCLICK Error Detection Script Runner
Write-Host "Running AUTOCLICK Error Detection Script..." -ForegroundColor Cyan

# Run the Python script with any passed arguments
python detect_errors.py $args

# Check the exit code
if ($LASTEXITCODE -ne 0) {
    Write-Host "`n=====================================================================" -ForegroundColor Red
    Write-Host "ERROR: Issues were found in the codebase. Please fix them before running the app." -ForegroundColor Red
    Write-Host "=====================================================================" -ForegroundColor Red
    Write-Host "`nTo automatically fix merge conflicts, run: .\detect_errors.ps1 --fix" -ForegroundColor Yellow
    Write-Host "`nPress any key to continue..."
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    exit 1
} else {
    Write-Host "`n=====================================================================" -ForegroundColor Green
    Write-Host "SUCCESS: No critical issues found. The app should run correctly." -ForegroundColor Green
    Write-Host "=====================================================================" -ForegroundColor Green
    Write-Host "`nPress any key to continue..."
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
}
