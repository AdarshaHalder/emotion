#!/bin/bash
set -e

echo "=== AI Voice Companion — Mac Build ==="

# 1. Install desktop deps
pip install -r requirements-desktop.txt
pip install pyinstaller

# 2. Build .app bundle
pyinstaller EMOTION.spec --clean --noconfirm

# 3. Package into .dmg
if command -v create-dmg &> /dev/null; then
    create-dmg \
        --volname "AI Voice Companion" \
        --window-pos 200 120 \
        --window-size 600 400 \
        --icon-size 100 \
        --icon "AIVoiceCompanion.app" 175 190 \
        --hide-extension "AIVoiceCompanion.app" \
        --app-drop-link 425 190 \
        "AIVoiceCompanion.dmg" \
        "dist/AIVoiceCompanion.app"
    echo "✅ AIVoiceCompanion.dmg created"
else
    # Fallback: plain hdiutil dmg (no fancy layout)
    hdiutil create -volname "AIVoiceCompanion" \
        -srcfolder dist/AIVoiceCompanion.app \
        -ov -format UDZO \
        AIVoiceCompanion.dmg
    echo "✅ AIVoiceCompanion.dmg created (install create-dmg for a nicer installer)"
fi
