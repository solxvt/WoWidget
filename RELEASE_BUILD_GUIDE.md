# WoWidget Windows Release Build

## Before the first public release

Confirm the repository remains configured as `solxvt/WoWidget` and verify the
release version in:


```text
wowidget/version.py
version_info.txt
WoWidget.spec
installer/WoWidget.iss
```

## Build the standalone application

From the project root in PowerShell:

```powershell
.\build_release.ps1
```

The application will be created at:

```text
dist\WoWidget\WoWidget.exe
```

This is an onedir build. Keep the complete `dist\WoWidget` folder
together while testing.

## Test the packaged build

Fully exit the development version from the system tray, then run:

```powershell
.\dist\WoWidget\WoWidget.exe
```

Test:

- first-run setup
- character search
- portrait generation and saving
- Cloudflare upload
- Discord widget update
- automatic scheduler
- settings
- launch with Windows
- start minimized
- system tray
- GitHub update check

## Build the installer

Install Inno Setup 6, then run:

```powershell
.\installer\build_installer.ps1
```

The installer will be created under:

```text
installer\Output
```

## GitHub release workflow

1. Commit and push the release source.
2. Create a GitHub release tag such as `v1.0.0`.
3. Upload the generated installer as a release asset.
4. Publish the release.
5. Confirm **Check for Updates** reports that the installed version is
   current.
6. For a later test release, publish a higher semantic version and
   confirm the update dialog appears.
