$ErrorActionPreference = "Stop"

$ProjectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ProjectRoot

foreach ($Path in @(
    "build",
    "dist",
    "installer\Output"
)) {
    if (Test-Path $Path) {
        Remove-Item $Path -Recurse -Force
        Write-Host "Removed $Path"
    }
}

Write-Host "Release build folders cleaned."
