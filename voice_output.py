"""
Voice Output Module
Convert text to speech using ElevenLabs API
"""

import os
import tempfile
import requests
from config import ELEVENLABS_API_KEY


# Voice settings tuned per mood for natural, human-sounding delivery
# stability: lower = more expressive/varied pitch (less robotic)
# style: higher = more emotional delivery (0–1, v2 models only)
_VOICE_SETTINGS = {
    "negative": {
        "stability": 0.25,       # soft, gentle, slightly hesitant
        "similarity_boost": 0.80,
        "style": 0.45,           # emotional warmth
        "use_speaker_boost": True,
    },
    "positive": {
        "stability": 0.30,       # upbeat, varied intonation
        "similarity_boost": 0.75,
        "style": 0.50,           # lively
        "use_speaker_boost": True,
    },
    "neutral": {
        "stability": 0.35,       # natural conversational tone
        "similarity_boost": 0.75,
        "style": 0.30,
        "use_speaker_boost": True,
    },
}


# Languages NOT officially covered by eleven_multilingual_v2 → use the broader
# eleven_turbo_v2_5 model so pronunciation is correct instead of garbled.
_EXTENDED_LANGS = {"te", "bn", "mr", "gu", "pa"}


def text_to_speech(text, voice_id, mood="neutral", language="en"):
    """
    Convert text to speech using ElevenLabs API.

    Args:
        text: text to speak
        voice_id: ElevenLabs voice ID
        mood: "positive", "negative", or "neutral" — tunes expressiveness
        language: ISO-639-1 code — selects the best-fitting TTS model

    Returns:
        path to MP3 file, or None on failure
    """
    try:
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"

        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": ELEVENLABS_API_KEY,
        }

        settings = _VOICE_SETTINGS.get(mood, _VOICE_SETTINGS["neutral"])

        # eleven_multilingual_v2 = highest quality for its supported languages;
        # extended Indian languages need turbo_v2_5 for correct pronunciation.
        model_id = "eleven_turbo_v2_5" if language in _EXTENDED_LANGS else "eleven_multilingual_v2"

        data = {
            "text": text,
            "model_id": model_id,
            "voice_settings": settings,
        }

        print(f"🔊 TTS [{mood}] → {text[:60]}...")
        response = requests.post(url, json=data, headers=headers, timeout=40)

        if response.status_code == 200:
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
            temp_file.write(response.content)
            temp_file.close()
            print(f"✅ Audio ready: {os.path.getsize(temp_file.name)} bytes")
            return temp_file.name
        else:
            print(f"❌ ElevenLabs {response.status_code}: {response.text}")
            return None

    except Exception as e:
        print(f"❌ TTS error: {e}")
        import traceback
        traceback.print_exc()
        return None


def get_audio_duration(audio_file_path):
    """
    Get duration of audio file. Falls back to file-size estimation if ffmpeg is absent.

    Returns:
        duration in seconds
    """
    try:
        from pydub import AudioSegment
        audio = AudioSegment.from_mp3(audio_file_path)
        return len(audio) / 1000.0
    except Exception:
        pass

    # Fallback: ElevenLabs encodes at ~128 kbps → ~16000 bytes/sec
    try:
        size = os.path.getsize(audio_file_path)
        return size / 16000.0
    except Exception:
        return 0
