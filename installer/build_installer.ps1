$ErrorActionPreference = "Stop"

$InstallerRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = Split-Path -Parent $InstallerRoot

Set-Location $ProjectRoot

if (-not (Test-Path "dist\WoWidget\WoWidget.exe")) {
    throw (
        "Build the PyInstaller application first by running " +
        ".\build_release.ps1"
    )
}

$PossibleCompilers = @(
    "${env:LOCALAPPDATA}\Programs\Inno Setup 6\ISCC.exe",
    "${env:ProgramFiles(x86)}\Inno Setup 6\ISCC.exe",
    "${env:ProgramFiles}\Inno Setup 6\ISCC.exe"
)

$Compiler = $PossibleCompilers |
    Where-Object { Test-Path $_ } |
    Select-Object -First 1

if (-not $Compiler) {
    throw (
        "Inno Setup 6 was not found. Install it, then run " +
        "this script again."
    )
}

& $Compiler "installer\WoWidget.iss"

Write-Host ""
Write-Host "Installer build completed." -ForegroundColor Green
Write-Host (
    "Output: " +
    "$ProjectRoot\installer\Output"
)
