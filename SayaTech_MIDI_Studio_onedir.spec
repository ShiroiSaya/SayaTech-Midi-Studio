# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_submodules

hiddenimports = collect_submodules('PySide6') + [
    'mido',
    'pydirectinput',
]

datas = [
    ('config.txt', '.'),
    ('sayatech_modern/assets/background.png', 'sayatech_modern/assets'),
    ('sayatech_modern/assets/splash.png', 'sayatech_modern/assets'),
    ('sayatech_modern/assets/app_icon.png', 'sayatech_modern/assets'),
    ('sayatech_modern/assets/app.ico', 'sayatech_modern/assets'),
]

a = Analysis(
    ['app.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
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
    [],
    exclude_binaries=True,
    name='SayaTech_MIDI_Studio',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    icon='sayatech_modern/assets/app.ico',
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='SayaTech_MIDI_Studio',
)
