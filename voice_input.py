"""
Voice Input Module
Records audio and converts speech to text using Whisper
"""

import os
import tempfile
from openai import OpenAI
from config import OPENAI_API_KEY, SAMPLE_RATE, CHANNELS


def record_audio(duration=5):
    """Record audio from microphone (desktop only — requires sounddevice)."""
    import sounddevice as sd
    import numpy as np
    print(f"Recording for {duration} seconds...")
    audio_data = sd.rec(
        int(duration * SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        channels=CHANNELS,
        dtype=np.int16
    )
    sd.wait()
    print("Recording complete!")
    return audio_data


def save_audio_temp(audio_data):
    """Save numpy audio array to a temp WAV file. Returns file path."""
    import soundfile as sf
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    sf.write(temp_file.name, audio_data, SAMPLE_RATE)
    return temp_file.name


def speech_to_text(audio_file_path, language="en"):
    """
    Transcribe an audio file path via Whisper.

    Args:
        audio_file_path: path to WAV/MP3 file
        language: ISO-639-1 code

    Returns:
        transcribed text or None
    """
    try:
        client = OpenAI(api_key=OPENAI_API_KEY)
        with open(audio_file_path, "rb") as audio_file:
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                language=language,
            )
        return transcript.text
    except Exception as e:
        print(f"Error in speech-to-text: {e}")
        return None
    finally:
        if os.path.exists(audio_file_path):
            os.remove(audio_file_path)


def transcribe_audio_bytes(audio_bytes, language="en"):
    """
    Transcribe raw audio bytes from st.audio_input() via Whisper.
    Works on both cloud and desktop.

    Args:
        audio_bytes: bytes-like object (e.g. from st.audio_input().read())
        language: ISO-639-1 code

    Returns:
        transcribed text or None
    """
    try:
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
        tmp.write(audio_bytes)
        tmp.close()
        return speech_to_text(tmp.name, language=language)
    except Exception as e:
        print(f"Error transcribing audio bytes: {e}")
        return None


def record_voice_sample(duration=5):
    """
    Record a voice sample for cloning. Desktop only.

    Returns:
        path to WAV file (caller must delete), or None on error
    """
    try:
        audio_data = record_audio(duration)
        return save_audio_temp(audio_data)
    except Exception as e:
        print(f"Error recording sample: {e}")
        return None


def process_voice_input(duration=5, language="en"):
    """
    Full desktop pipeline: record → save → transcribe. Desktop only.

    Returns:
        transcribed text
    """
    audio_data = record_audio(duration)
    temp_file = save_audio_temp(audio_data)
    return speech_to_text(temp_file, language=language)
