# evony_tool.spec
# PyInstaller build configuration for Evony Gear Optimizer v1.3.0
#
# BUILD COMMAND (run from the evony_tool folder):
#   py -3.11 -m PyInstaller evony_tool.spec --clean

import os
import sys
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

block_cipher = None

# Resolve the spec file's own directory so paths work regardless of
# where PyInstaller is called from
SPEC_DIR = os.path.dirname(os.path.abspath(SPEC))

webview_datas   = collect_data_files('webview')
webview_hidimps = collect_submodules('webview')

a = Analysis(
    [os.path.join(SPEC_DIR, 'app.py')],
    pathex=[SPEC_DIR],
    binaries=[],
    datas=[
        (os.path.join(SPEC_DIR, 'templates'),            'templates'),
        (os.path.join(SPEC_DIR, 'static'),               'static'),
        (os.path.join(SPEC_DIR, 'evony_data.xlsx'), '.'),
        (os.path.join(SPEC_DIR, 'splash.py'), '.'),
    ] + webview_datas,
    hiddenimports=[
        'tkinter',
        'tkinter.font',
        'openpyxl',
        'openpyxl.styles',
        'openpyxl.styles.fills',
        'openpyxl.utils',
        'flask',
        'jinja2',
        'werkzeug',
        'werkzeug.serving',
        'werkzeug.routing',
        'webview',
        'webview.platforms',
        'webview.platforms.winforms',
    ] + webview_hidimps,
    hookspath=[],
    runtime_hooks=[],
    excludes=['tkinter', 'matplotlib', 'numpy', 'pandas', 'PIL'],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='EvonyGearOptimizer',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,
    icon=os.path.join(SPEC_DIR, 'icon.ico'),
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name='EvonyGearOptimizer',
)
