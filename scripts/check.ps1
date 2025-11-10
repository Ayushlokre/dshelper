# Check script for dshelper package
# Runs code quality checks (linting, type checking)

Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "Running Code Quality Checks" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""

# Install checking tools
Write-Host "Installing checking tools..." -ForegroundColor Yellow
python -m pip install black flake8 mypy -q
Write-Host "✓ Tools ready" -ForegroundColor Green
Write-Host ""

# Check code formatting with black
Write-Host "Checking code formatting (Black)..." -ForegroundColor Yellow
python -m black --check dshelper/ tests/
$black_exit = $LASTEXITCODE
Write-Host ""

# Lint with flake8
Write-Host "Linting code (Flake8)..." -ForegroundColor Yellow
python -m flake8 dshelper/ --max-line-length=100 --ignore=E203,W503
$flake8_exit = $LASTEXITCODE
Write-Host ""

# Type checking with mypy
Write-Host "Type checking (MyPy)..." -ForegroundColor Yellow
python -m mypy dshelper/ --ignore-missing-imports
$mypy_exit = $LASTEXITCODE
Write-Host ""

# Summary
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "Summary" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan

if ($black_exit -eq 0) {
    Write-Host "✓ Black (formatting): PASSED" -ForegroundColor Green
} else {
    Write-Host "✗ Black (formatting): FAILED" -ForegroundColor Red
    Write-Host "  Run: python -m black dshelper/ tests/" -ForegroundColor Yellow
}

if ($flake8_exit -eq 0) {
    Write-Host "✓ Flake8 (linting): PASSED" -ForegroundColor Green
} else {
    Write-Host "✗ Flake8 (linting): FAILED" -ForegroundColor Red
}

if ($mypy_exit -eq 0) {
    Write-Host "✓ MyPy (type checking): PASSED" -ForegroundColor Green
} else {
    Write-Host "✗ MyPy (type checking): FAILED" -ForegroundColor Red
}

Write-Host ""

if (($black_exit -eq 0) -and ($flake8_exit -eq 0) -and ($mypy_exit -eq 0)) {
    Write-Host "All checks passed! Code is ready for publishing." -ForegroundColor Green
    exit 0
} else {
    Write-Host "Some checks failed. Please fix the issues before publishing." -ForegroundColor Red
    exit 1
}
