# Publish script for PyPI
# This script uploads the package to the official PyPI

Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "Publishing to PyPI (Production)" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""

# Check if dist directory exists
if (-not (Test-Path "dist")) {
    Write-Host "Error: dist directory not found!" -ForegroundColor Red
    Write-Host "Please run .\scripts\build.ps1 first" -ForegroundColor Yellow
    exit 1
}

Write-Host "IMPORTANT: This will publish to the PRODUCTION PyPI!" -ForegroundColor Red
Write-Host "Make sure you have:" -ForegroundColor Yellow
Write-Host "  ✓ Tested on TestPyPI" -ForegroundColor White
Write-Host "  ✓ Updated version number if re-publishing" -ForegroundColor White
Write-Host "  ✓ Updated CHANGELOG.md" -ForegroundColor White
Write-Host "  ✓ All tests passing" -ForegroundColor White
Write-Host ""

$confirm1 = Read-Host "Have you tested on TestPyPI? (y/n)"
if ($confirm1 -ne "y") {
    Write-Host "Please test on TestPyPI first: .\scripts\publish_testpypi.ps1" -ForegroundColor Yellow
    exit 0
}

Write-Host ""
Write-Host "Checking package with twine..." -ForegroundColor Yellow
python -m twine check dist/*
Write-Host ""

Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "Ready to upload to PyPI" -ForegroundColor Yellow
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "You will be prompted for your PyPI credentials:" -ForegroundColor White
Write-Host "  Username: __token__" -ForegroundColor Green
Write-Host "  Password: Your PyPI API token (starts with 'pypi-')" -ForegroundColor Green
Write-Host ""
Write-Host "To create a token:" -ForegroundColor Yellow
Write-Host "  1. Go to: https://pypi.org/manage/account/#api-tokens" -ForegroundColor White
Write-Host "  2. Click 'Add API token'" -ForegroundColor White
Write-Host "  3. Give it a name and copy the token" -ForegroundColor White
Write-Host ""

$confirm2 = Read-Host "Are you absolutely sure you want to publish to PyPI? (yes/no)"
if ($confirm2 -ne "yes") {
    Write-Host "Upload cancelled." -ForegroundColor Yellow
    exit 0
}

Write-Host ""
Write-Host "Uploading to PyPI..." -ForegroundColor Yellow
python -m twine upload dist/*

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "=====================================" -ForegroundColor Cyan
    Write-Host "Upload successful!" -ForegroundColor Green
    Write-Host "=====================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Your package is now live!" -ForegroundColor Green
    Write-Host ""
    Write-Host "View your package at:" -ForegroundColor Yellow
    Write-Host "  https://pypi.org/project/dshelper/" -ForegroundColor White
    Write-Host ""
    Write-Host "Anyone can now install it with:" -ForegroundColor Yellow
    Write-Host "  pip install dshelper" -ForegroundColor White
    Write-Host ""
    Write-Host "Congratulations! 🎉" -ForegroundColor Green
} else {
    Write-Host ""
    Write-Host "Upload failed! Please check the error messages above." -ForegroundColor Red
}
