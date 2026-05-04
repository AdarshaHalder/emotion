"""
Test Voice Cloning Feature
This script demonstrates how to clone a voice
"""

from voice_cloning import upload_voice_samples, get_user_voices
import os

print("🎙️ Voice Cloning Demo\n")

print("=" * 60)
print("HOW VOICE CLONING WORKS:")
print("=" * 60)
print("""
1. **Collect Audio Samples**
   - Record 3-5 audio clips of the person
   - Each clip: 30 seconds - 2 minutes
   - Clear audio, no background noise
   - Different sentences (natural speech)

2. **Upload & Clone**
   - Provide samples to ElevenLabs
   - AI analyzes voice characteristics
   - Creates unique voice ID
   - Takes 1-2 minutes

3. **Use Cloned Voice**
   - Select cloned voice from dropdown
   - AI speaks in that person's voice
   - Natural intonation preserved

EXAMPLES:
- Mom's comforting voice
- Dad's encouraging voice  
- Spouse's loving voice
- Grandparent's wisdom
""")

print("\n" + "=" * 60)
print("YOUR CURRENT VOICES:")
print("=" * 60 + "\n")

voices = get_user_voices()

premade = [v for v in voices if v.get('category') == 'premade']
cloned = [v for v in voices if v.get('category') == 'cloned']

print(f"📢 Premade Voices: {len(premade)}")
for voice in premade[:5]:
    print(f"   - {voice.get('name')}")

print(f"\n🎤 Cloned Voices: {len(cloned)}")
if cloned:
    for voice in cloned:
        print(f"   - {voice.get('name')} (ID: {voice.get('voice_id')})")
else:
    print("   (No cloned voices yet)")

print("\n" + "=" * 60)
print("HOW TO CLONE A VOICE:")
print("=" * 60)
print("""
1. Open the desktop app
2. Go to sidebar → "Clone a Voice"
3. Enter voice name (e.g., "Mom")
4. Upload 1-5 audio samples
5. Click "Clone Voice"
6. Wait 1-2 minutes
7. Select from dropdown!

TIP: Use voice memos, video clips, or phone recordings
""")

print("\n✅ Voice cloning is ready to use in the app!")
