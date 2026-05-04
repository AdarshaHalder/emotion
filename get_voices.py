"""
Get Available ElevenLabs Voices
This will show you which voices you can use with your API key
"""

import requests
from config import ELEVENLABS_API_KEY

print("🎤 Fetching your available ElevenLabs voices...\n")

url = "https://api.elevenlabs.io/v1/voices"
headers = {
    "xi-api-key": ELEVENLABS_API_KEY
}

try:
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        voices = data.get("voices", [])
        
        print(f"✅ Found {len(voices)} available voices:\n")
        
        for voice in voices:
            name = voice.get("name", "Unknown")
            voice_id = voice.get("voice_id", "")
            category = voice.get("category", "unknown")
            labels = voice.get("labels", {})
            
            print(f"📢 {name}")
            print(f"   ID: {voice_id}")
            print(f"   Category: {category}")
            print(f"   Labels: {labels}")
            print()
        
        print("\n" + "="*60)
        print("💡 Copy these voice IDs to config.py:")
        print("="*60 + "\n")
        
        print("AVAILABLE_VOICES = {")
        for i, voice in enumerate(voices[:5]):  # Show first 5
            name = voice.get("name", "Unknown")
            voice_id = voice.get("voice_id", "")
            print(f'    "{name}": "{voice_id}",')
        print("}")
        
    else:
        print(f"❌ Error: {response.status_code}")
        print(f"Response: {response.text}")

except Exception as e:
    print(f"❌ Error: {e}")
