#!/bin/bash

# Desktop App Launcher Script for macOS/Linux

echo "🚀 Starting AI Voice Companion Desktop App..."

# Navigate to project directory
cd "$(dirname "$0")"

# Activate virtual environment
source venv/bin/activate

# Run desktop app
python desktop_app.py
