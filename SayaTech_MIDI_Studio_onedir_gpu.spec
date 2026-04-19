# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_data_files, collect_dynamic_libs, collect_submodules

base_hiddenimports = [
    'PySide6.QtCore',
    'PySide6.QtGui',
    'PySide6.QtWidgets',
    'mido',
    'pydirectinput',
]
base_datas = [
    ('config.txt', '.'),
    ('config.example.txt', '.'),
    ('ui_settings.example.json', '.'),
    ('sayatech_modern/assets/background.png', 'sayatech_modern/assets'),
    ('sayatech_modern/assets/splash.png', 'sayatech_modern/assets'),
    ('sayatech_modern/assets/app.ico', 'sayatech_modern/assets'),
]
base_binaries = []

torch_hiddenimports = collect_submodules('torch')
torch_datas = collect_data_files('torch')
torch_binaries = collect_dynamic_libs('torch')

hiddenimports = base_hiddenimports + torch_hiddenimports
datas = base_datas + torch_datas
binaries = base_binaries + torch_binaries
try:
    datas += collect_data_files('shiboken6')
except Exception:
    pass

a = Analysis(
    ['app.py'],
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['pip', 'setuptools', 'wheel', 'pkg_resources'],
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
    upx=False,
    console=False,
    disable_windowed_traceback=False,
    icon='sayatech_modern/assets/app.ico',
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name='SayaTech_MIDI_Studio_GPU',
)
