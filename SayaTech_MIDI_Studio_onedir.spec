# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_data_files

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

# CPU 版显式排除整套 PyTorch / TorchVision / 构建工具链，避免装进几 GB 的依赖
cpu_excludes = [
    'torch', 'torch._C', 'torchvision', 'torchaudio', 'torchgen', 'functorch', 'triton',
    'pip', 'setuptools', 'wheel', 'pkg_resources',
]

datas = list(base_datas)
try:
    datas += collect_data_files('shiboken6')
except Exception:
    pass

a = Analysis(
    ['app.py'],
    pathex=[],
    binaries=base_binaries,
    datas=datas,
    hiddenimports=base_hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=cpu_excludes,
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
    name='SayaTech_MIDI_Studio_CPU',
)
