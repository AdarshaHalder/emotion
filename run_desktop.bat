@echo off
REM Desktop App Launcher Script for Windows

echo Starting AI Voice Companion Desktop App...

REM Navigate to project directory
cd /d "%~dp0"

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Run desktop app
python desktop_app.py

pause
