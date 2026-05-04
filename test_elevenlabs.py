"""
Test ElevenLabs TTS - Verify voice output is working
"""

from voice_output import text_to_speech
from config import AVAILABLE_VOICES, ELEVENLABS_API_KEY
import os

print("🧪 Testing ElevenLabs Text-to-Speech\n")

# Check API key
if not ELEVENLABS_API_KEY or ELEVENLABS_API_KEY == "your-elevenlabs-api-key-here":
    print("❌ ERROR: ElevenLabs API key not configured!")
    print("Please add your API key to .env file")
    exit(1)

print(f"✅ API Key found: {ELEVENLABS_API_KEY[:10]}...")
print(f"\n📋 Available voices: {list(AVAILABLE_VOICES.keys())}\n")

# Test text
test_text = "Hello! This is a test of the text to speech system. Can you hear me?"

# Test each voice
for voice_name, voice_id in AVAILABLE_VOICES.items():
    print(f"\n🎤 Testing voice: {voice_name} (ID: {voice_id})")
    print(f"   Text: '{test_text}'")
    
    audio_file = text_to_speech(test_text, voice_id)
    
    if audio_file:
        file_size = os.path.getsize(audio_file)
        print(f"   ✅ SUCCESS! Audio generated: {file_size} bytes")
        print(f"   📁 File saved at: {audio_file}")
        print(f"   🔊 Play this file to test audio output")
        
        # Try to play using system command
        print(f"\n   Attempting to play audio...")
        os.system(f"afplay '{audio_file}'")  # macOS
        
        # Clean up
        os.remove(audio_file)
        print(f"   🗑️  Temp file cleaned up")
    else:
        print(f"   ❌ FAILED! Could not generate audio")

print("\n\n✅ Test complete!")
print("\nIf you heard audio playback, ElevenLabs is working correctly.")
print("If not, check:")
print("  1. Your API key is correct")
print("  2. You have API credits")
print("  3. Your speakers/volume are on")
