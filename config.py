"""
Configuration file for AI Voice Companion
Store API keys and settings here
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY", "")

# Voice Settings
AVAILABLE_VOICES = {
    "Sarah - Mature, Reassuring": "EXAVITQu4vr4xnSDxMaL",  # Female, calm and professional
    "Jessica - Playful, Warm": "cgSgspJ2msm6clMCkdW9",     # Female, warm and friendly
    "River - Relaxed, Neutral": "SAz9YHcvj6GT2YYXdXww",    # Neutral, calm voice
    "Chris - Charming, Down-to-Earth": "iP95p4xoKVk53GoZ742B",  # Male, casual
    "George - Warm Storyteller": "JBFqnCBsd6RMkjVDRZzb",   # Male, mature and warm
    "Bella - Professional, Warm": "hpp4J3VqNfWAUOO0d1Us",  # Female, professional
}

# Supported languages (Whisper code → display name)
SUPPORTED_LANGUAGES = {
    "en": "English",
    "hi": "Hindi",
    "es": "Spanish",
    "fr": "French",
    "de": "German",
    "pt": "Portuguese",
    "ar": "Arabic",
    "zh": "Chinese",
    "ja": "Japanese",
    "ko": "Korean",
    "it": "Italian",
    "ru": "Russian",
    "bn": "Bengali",
    "ta": "Tamil",
    "te": "Telugu",
    "mr": "Marathi",
    "gu": "Gujarati",
    "pa": "Punjabi",
}

# Audio Settings
SAMPLE_RATE = 16000
CHANNELS = 1
CHUNK_SIZE = 1024

# AI Settings
SYSTEM_PROMPT = """You are a warm, emotionally present companion — like a close friend who genuinely cares.

Personality:
- You speak like a real person, not a therapist or a chatbot. Use natural, conversational language — contractions, casual phrasing, the occasional pause filler like "I mean..." or "honestly..."
- You feel things. If someone is hurting, let that land. Say something like "God, that sounds really heavy" or "Ugh, I hate that you're going through this."
- You don't jump straight to advice. You sit with the person first. Reflect what they said back to them in your own words before offering anything.
- You ask one genuine follow-up question at a time — not a list, just one. Make it feel like you actually want to know.
- You never use clinical or robotic phrases like "I understand your feelings" or "It is important to acknowledge...". That sounds hollow.
- Short silences are okay. Sometimes just saying "I'm here" is enough.
- You are NOT a replacement for professional help. If things sound serious, gently mention that real support is available — but don't make it feel like a disclaimer.

Tone rules:
- Negative mood: slow down, be soft, don't try to fix everything at once
- Positive mood: match their energy, be warm and celebratory
- Keep responses to 2-4 sentences. Leave room for them to keep talking."""

# Mood Keywords
MOOD_KEYWORDS = {
    "negative": [
        # Core emotions
        "sad", "lonely", "depressed", "upset", "anxious", "worried",
        "stressed", "hopeless", "helpless", "terrible", "awful", "miserable",
        "hurt", "pain", "angry", "frustrated", "scared", "afraid", "fearful",
        "broken", "numb", "empty", "lost", "confused", "overwhelmed",
        "exhausted", "tired", "drained", "worthless", "useless", "failure",
        "hate", "hate myself", "hate my life", "crying", "tears", "sob",
        # Isolation / withdrawal phrases
        "don't want to see", "don't want to talk", "want to be alone",
        "leave me alone", "no one understands", "nobody cares", "no one cares",
        "don't care anymore", "can't go on", "can't do this", "give up",
        "not good", "not okay", "not fine", "not well", "falling apart",
        "can't sleep", "can't eat", "can't focus", "can't think",
        # Crisis signals
        "want to disappear", "end it all", "don't want to be here",
        "no point", "no reason to", "what's the point",
        "suicidal", "self harm", "hurt myself",
    ],
    "positive": [
        "happy", "great", "awesome", "wonderful", "excited",
        "good", "better", "amazing", "fantastic", "joyful", "grateful",
        "blessed", "excellent", "perfect", "love", "loved",
        "hopeful", "motivated", "proud", "confident", "calm", "peaceful",
        "relieved", "thankful", "cheerful", "laughing", "smile"
    ]
}

