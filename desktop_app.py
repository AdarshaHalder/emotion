"""
Desktop App Launcher
Wraps Streamlit app in a native desktop window using PyWebView
"""

import webview
import threading
import time
import subprocess
import sys
import os
from pathlib import Path

# Get the project directory
PROJECT_DIR = Path(__file__).parent


def run_streamlit():
    """Run Streamlit server in background"""
    # Activate venv and run streamlit
    if sys.platform == "win32":
        python_exec = PROJECT_DIR / "venv" / "Scripts" / "python.exe"
        streamlit_exec = PROJECT_DIR / "venv" / "Scripts" / "streamlit.exe"
    else:  # macOS/Linux
        python_exec = PROJECT_DIR / "venv" / "bin" / "python"
        streamlit_exec = PROJECT_DIR / "venv" / "bin" / "streamlit"
    
    # Run streamlit
    cmd = [
        str(streamlit_exec),
        "run",
        str(PROJECT_DIR / "app.py"),
        "--server.headless=true",
        "--server.port=8501",
        "--browser.gatherUsageStats=false"
    ]
    
    subprocess.Popen(
        cmd,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )


def create_window():
    """Create desktop window"""
    # Wait for Streamlit to start
    time.sleep(3)
    
    # Create window
    window = webview.create_window(
        title="AI Voice Companion",
        url="http://localhost:8501",
        width=1000,
        height=800,
        resizable=True,
        fullscreen=False,
        min_size=(800, 600),
    )
    
    webview.start()


def main():
    """Main entry point"""
    print("🚀 Starting AI Voice Companion...")
    print("⏳ Loading application...")
    
    # Start Streamlit in background thread
    streamlit_thread = threading.Thread(target=run_streamlit, daemon=True)
    streamlit_thread.start()
    
    # Create and show window
    create_window()


if __name__ == "__main__":
    main()
