# -*- mode: python ; coding: utf-8 -*-

from pathlib import Path

project_root = Path.cwd()
entry_script = project_root / "src" / "gpsimagestomap" / "__main__.py"
templates_dir = project_root / "src" / "gpsimagestomap" / "templates"


a = Analysis(
    [str(entry_script)],
    pathex=[str(project_root / "src")],
    binaries=[],
    datas=[
        (str(templates_dir), "gpsimagestomap/templates"),
    ],
    hiddenimports=[
        "pillow_heif",
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
    name='flightphotomapper',
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='flightphotomapper',
)
