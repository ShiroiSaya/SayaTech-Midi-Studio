# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_data_files, collect_dynamic_libs, collect_submodules

base_hiddenimports = collect_submodules('PySide6') + [
    'mido',
    'pydirectinput',
]
base_datas = [
    ('config.txt', '.'),
    ('config.example.txt', '.'),
    ('ui_settings.example.json', '.'),
    ('sayatech_modern/assets/background.png', 'sayatech_modern/assets'),
    ('sayatech_modern/assets/splash.png', 'sayatech_modern/assets'),
    ('sayatech_modern/assets/app_icon.png', 'sayatech_modern/assets'),
    ('sayatech_modern/assets/app.ico', 'sayatech_modern/assets'),
]
base_binaries = []

try:
    import torch  # noqa: F401
except Exception:
    torch_hiddenimports = []
    torch_datas = []
    torch_binaries = []
else:
    torch_hiddenimports = collect_submodules('torch')
    torch_datas = collect_data_files('torch')
    torch_binaries = collect_dynamic_libs('torch')

hiddenimports = base_hiddenimports + torch_hiddenimports
binaries = base_binaries + torch_binaries
datas = base_datas + torch_datas

a = Analysis(
    ['app.py'],
    pathex=[],
    binaries=binaries,
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
    a.binaries,
    a.datas,
    [],
    name='SayaTech_MIDI_Studio',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    icon='sayatech_modern/assets/app.ico',
)
