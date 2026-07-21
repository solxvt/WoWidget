# -*- mode: python ; coding: utf-8 -*-

from pathlib import Path

import certifi


project_root = Path(SPECPATH)

datas = [
    (
        str(
            project_root
            / "wowidget"
            / "assets"
        ),
        "wowidget/assets",
    ),
    (
        certifi.where(),
        "certifi",
    ),
]

hiddenimports = [
    "PIL._tkinter_finder",
    "keyring.backends.Windows",
]

analysis = Analysis(
    ["main.py"],
    pathex=[
        str(
            project_root
        ),
    ],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        "tkinter",
        "matplotlib",
        "numpy",
        "pandas",
    ],
    noarchive=False,
    optimize=1,
)

pyz = PYZ(
    analysis.pure
)

exe = EXE(
    pyz,
    analysis.scripts,
    [],
    exclude_binaries=True,
    name="WoWidget",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=(
        "wowidget/assets/icons/wowidget.ico"
    ),
    version="version_info.txt",
)

collection = COLLECT(
    exe,
    analysis.binaries,
    analysis.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name="WoWidget",
)
