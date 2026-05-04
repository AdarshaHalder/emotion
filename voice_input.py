"""
Voice Input Module
Records audio and converts speech to text using Whisper
"""

import os
import tempfile
import sounddevice as sd
import soundfile as sf
import numpy as np
from openai import OpenAI
from config import OPENAI_API_KEY, SAMPLE_RATE, CHANNELS


def record_audio(duration=5):
    """
    Record audio from microphone
    
    Args:
        duration: Recording duration in seconds
    
    Returns:
        numpy array of audio data
    """
    print(f"Recording for {duration} seconds...")
    audio_data = sd.rec(
        int(duration * SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        channels=CHANNELS,
        dtype=np.int16
    )
    sd.wait()  # Wait until recording is finished
    print("Recording complete!")
    return audio_data


def save_audio_temp(audio_data):
    """
    Save audio data to temporary file
    
    Args:
        audio_data: numpy array of audio
    
    Returns:
        path to temporary file
    """
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    sf.write(temp_file.name, audio_data, SAMPLE_RATE)
    return temp_file.name


def speech_to_text(audio_file_path, language="en"):
    """
    Convert speech to text using OpenAI Whisper API

    Args:
        audio_file_path: path to audio file
        language: ISO-639-1 language code (e.g. "hi", "es", "fr")

    Returns:
        transcribed text
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
        # Clean up temp file
        if os.path.exists(audio_file_path):
            os.remove(audio_file_path)


def record_voice_sample(duration=5):
    """
    Record a voice sample and return the saved file path (caller must delete).

    Returns:
        path to WAV file, or None on error
    """
    try:
        audio_data = record_audio(duration)
        return save_audio_temp(audio_data)
    except Exception as e:
        print(f"Error recording sample: {e}")
        return None


def process_voice_input(duration=5, language="en"):
    """
    Complete pipeline: record → save → transcribe

    Args:
        duration: recording duration in seconds
        language: ISO-639-1 language code

    Returns:
        transcribed text
    """
    audio_data = record_audio(duration)
    temp_file = save_audio_temp(audio_data)
    text = speech_to_text(temp_file, language=language)
    return text
