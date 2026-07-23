$ErrorActionPreference = "Stop"

$ProjectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ProjectRoot

Write-Host ""
Write-Host "Building WoWidget 1.0.1..." -ForegroundColor Cyan
Write-Host ""

if (-not (Test-Path ".venv\Scripts\python.exe")) {
    throw (
        "The project virtual environment was not found at " +
        ".venv\Scripts\python.exe"
    )
}

$Python = ".venv\Scripts\python.exe"

& $Python -m pip install --upgrade pip
& $Python -m pip install -r requirements-release.txt

if (Test-Path "build") {
    Remove-Item "build" -Recurse -Force
}

if (Test-Path "dist") {
    Remove-Item "dist" -Recurse -Force
}

& $Python -m PyInstaller `
    --noconfirm `
    --clean `
    "WoWidget.spec"

if (-not (Test-Path "dist\WoWidget\WoWidget.exe")) {
    throw "PyInstaller finished without producing WoWidget.exe."
}

Write-Host ""
Write-Host "Build completed successfully." -ForegroundColor Green
Write-Host (
    "Executable: " +
    "$ProjectRoot\dist\WoWidget\WoWidget.exe"
)
Write-Host ""
