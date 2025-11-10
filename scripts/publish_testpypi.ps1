# Publish script for TestPyPI
# This script uploads the package to TestPyPI for testing

Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "Publishing to TestPyPI" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""

# Check if dist directory exists
if (-not (Test-Path "dist")) {
    Write-Host "Error: dist directory not found!" -ForegroundColor Red
    Write-Host "Please run .\scripts\build.ps1 first" -ForegroundColor Yellow
    exit 1
}

Write-Host "Checking package with twine..." -ForegroundColor Yellow
python -m twine check dist/*
Write-Host ""

Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "Ready to upload to TestPyPI" -ForegroundColor Yellow
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "You will be prompted for your TestPyPI credentials:" -ForegroundColor White
Write-Host "  Username: __token__" -ForegroundColor Green
Write-Host "  Password: Your TestPyPI API token (starts with 'pypi-')" -ForegroundColor Green
Write-Host ""
Write-Host "To create a token:" -ForegroundColor Yellow
Write-Host "  1. Go to: https://test.pypi.org/manage/account/#api-tokens" -ForegroundColor White
Write-Host "  2. Click 'Add API token'" -ForegroundColor White
Write-Host "  3. Give it a name and copy the token" -ForegroundColor White
Write-Host ""

$confirm = Read-Host "Continue with upload? (y/n)"
if ($confirm -ne "y") {
    Write-Host "Upload cancelled." -ForegroundColor Yellow
    exit 0
}

Write-Host ""
Write-Host "Uploading to TestPyPI..." -ForegroundColor Yellow
python -m twine upload --repository testpypi dist/*

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "=====================================" -ForegroundColor Cyan
    Write-Host "Upload successful!" -ForegroundColor Green
    Write-Host "=====================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "View your package at:" -ForegroundColor Yellow
    Write-Host "  https://test.pypi.org/project/dshelper/" -ForegroundColor White
    Write-Host ""
    Write-Host "Test installation with:" -ForegroundColor Yellow
    Write-Host "  pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ dshelper" -ForegroundColor White
    Write-Host ""
    Write-Host "If everything works, you can publish to PyPI:" -ForegroundColor Cyan
    Write-Host "  .\scripts\publish_pypi.ps1" -ForegroundColor White
} else {
    Write-Host ""
    Write-Host "Upload failed! Please check the error messages above." -ForegroundColor Red
}
