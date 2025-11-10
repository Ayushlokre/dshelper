# Test script for dshelper package
# Runs all tests with coverage

Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "Running DSHelper Tests" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""

# Check if pytest is installed
Write-Host "Checking test dependencies..." -ForegroundColor Yellow
python -m pip install pytest pytest-cov -q
Write-Host "✓ Test dependencies ready" -ForegroundColor Green
Write-Host ""

# Run tests
Write-Host "Running tests with coverage..." -ForegroundColor Yellow
Write-Host ""
python -m pytest tests/ -v --cov=dshelper --cov-report=term-missing --cov-report=html

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "=====================================" -ForegroundColor Cyan
    Write-Host "All tests passed!" -ForegroundColor Green
    Write-Host "=====================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Coverage report saved to: htmlcov/index.html" -ForegroundColor Yellow
    Write-Host "Open it in your browser to see detailed coverage." -ForegroundColor White
} else {
    Write-Host ""
    Write-Host "Some tests failed. Please fix them before publishing." -ForegroundColor Red
    exit 1
}
