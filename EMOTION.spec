# -*- mode: python ; coding: utf-8 -*-
import sys
import os
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

block_cipher = None

# Collect all streamlit data files
streamlit_data = collect_data_files("streamlit")

a = Analysis(
    ["desktop_app.py"],
    pathex=["."],
    binaries=[],
    datas=[
        ("app.py", "."),
        ("config.py", "."),
        ("ai_response.py", "."),
        ("mood_detection.py", "."),
        ("voice_input.py", "."),
        ("voice_output.py", "."),
        ("voice_cloning.py", "."),
        (".env.example", "."),
        *streamlit_data,
    ],
    hiddenimports=[
        "streamlit",
        "streamlit.web.cli",
        "streamlit.runtime.scriptrunner.magic_funcs",
        "openai",
        "sounddevice",
        "soundfile",
        "numpy",
        "requests",
        "dotenv",
        "pydub",
        "webview",
        *collect_submodules("streamlit"),
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
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
    name="AIVoiceCompanion",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    icon="icon.ico" if sys.platform == "win32" else "icon.icns",
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name="AIVoiceCompanion",
)

# macOS .app bundle
if sys.platform == "darwin":
    app = BUNDLE(
        coll,
        name="AIVoiceCompanion.app",
        icon="icon.icns",
        bundle_identifier="com.scripturesllp.aivoicecompanion",
        info_plist={
            "NSMicrophoneUsageDescription": "AI Voice Companion needs microphone access to record your voice.",
            "CFBundleShortVersionString": "1.0.0",
        },
    )
