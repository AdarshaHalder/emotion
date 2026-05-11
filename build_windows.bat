@echo off
echo === AI Voice Companion — Windows Build ===

:: 1. Install desktop deps
pip install -r requirements-desktop.txt
pip install pyinstaller

:: 2. Build .exe
pyinstaller EMOTION.spec --clean --noconfirm

:: 3. Optional: wrap in Inno Setup installer
where iscc >nul 2>&1
if %ERRORLEVEL% == 0 (
    iscc setup.iss
    echo Installer created.
) else (
    echo Distributable folder: dist\AIVoiceCompanion\
    echo Zip it up and share — users run AIVoiceCompanion.exe inside.
)

echo Done.
