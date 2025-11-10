# Build script for dshelper package
# This script builds the distribution packages

Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "Building DSHelper Package" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""

# Clean previous builds
Write-Host "Cleaning previous builds..." -ForegroundColor Yellow
if (Test-Path "dist") {
    Remove-Item -Recurse -Force dist
    Write-Host "✓ Removed dist directory" -ForegroundColor Green
}
if (Test-Path "build") {
    Remove-Item -Recurse -Force build
    Write-Host "✓ Removed build directory" -ForegroundColor Green
}
if (Test-Path "dshelper.egg-info") {
    Remove-Item -Recurse -Force dshelper.egg-info
    Write-Host "✓ Removed egg-info directory" -ForegroundColor Green
}
Write-Host ""

# Install/upgrade build tools
Write-Host "Installing/upgrading build tools..." -ForegroundColor Yellow
python -m pip install --upgrade pip
python -m pip install --upgrade build wheel twine
Write-Host "✓ Build tools ready" -ForegroundColor Green
Write-Host ""

# Build the package
Write-Host "Building distribution packages..." -ForegroundColor Yellow
python -m build
Write-Host ""

# Check if build was successful
if (Test-Path "dist") {
    Write-Host "=====================================" -ForegroundColor Cyan
    Write-Host "Build completed successfully!" -ForegroundColor Green
    Write-Host "=====================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Generated files:" -ForegroundColor Yellow
    Get-ChildItem dist | ForEach-Object { Write-Host "  - $_" -ForegroundColor White }
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Cyan
    Write-Host "  1. Test locally: pip install dist/dshelper-0.1.0-py3-none-any.whl" -ForegroundColor White
    Write-Host "  2. Upload to TestPyPI: .\scripts\publish_testpypi.ps1" -ForegroundColor White
    Write-Host "  3. Upload to PyPI: .\scripts\publish_pypi.ps1" -ForegroundColor White
} else {
    Write-Host "Build failed! Please check the error messages above." -ForegroundColor Red
    exit 1
}
