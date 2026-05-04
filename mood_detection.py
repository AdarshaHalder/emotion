"""
Mood Detection Module
Uses GPT for accurate mood classification with keyword fallback.
"""

from config import OPENAI_API_KEY, MOOD_KEYWORDS


def detect_mood(text):
    """
    Classify mood using GPT. Falls back to keyword matching if the API call fails.

    Returns:
        "positive", "neutral", or "negative"
    """
    if not text:
        return "neutral"

    try:
        from openai import OpenAI
        client = OpenAI(api_key=OPENAI_API_KEY)

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a mood classifier. Given a message, reply with exactly one word: "
                        "positive, negative, or neutral. "
                        "Consider the full meaning — negation, sarcasm, withdrawal, hopelessness. "
                        "When in doubt between neutral and negative, choose negative."
                    ),
                },
                {"role": "user", "content": text},
            ],
            temperature=0,
            max_tokens=5,
        )

        result = response.choices[0].message.content.strip().lower()
        if result in ("positive", "negative", "neutral"):
            return result
        return "neutral"

    except Exception:
        return _keyword_fallback(text)


def _keyword_fallback(text):
    """Simple keyword fallback if GPT call fails."""
    text_lower = text.lower()
    pos = sum(1 for kw in MOOD_KEYWORDS["positive"] if kw in text_lower)
    neg = sum(1 for kw in MOOD_KEYWORDS["negative"] if kw in text_lower)
    if neg > pos:
        return "negative"
    if pos > neg:
        return "positive"
    return "neutral"


def get_mood_emoji(mood):
    """
    Get emoji representation of mood
    
    Args:
        mood: "positive", "neutral", or "negative"
    
    Returns:
        emoji string
    """
    mood_emojis = {
        "positive": "😊",
        "neutral": "😐",
        "negative": "😔"
    }
    return mood_emojis.get(mood, "😐")


def analyze_mood_with_details(text):
    """
    Analyze mood and return detailed information
    
    Args:
        text: user's text input
    
    Returns:
        dict with mood, emoji, and matched keywords
    """
    mood = detect_mood(text)
    emoji = get_mood_emoji(mood)
    
    # Find matched keywords
    text_lower = text.lower() if text else ""
    matched_keywords = []
    
    for keyword in MOOD_KEYWORDS.get("positive", []) + MOOD_KEYWORDS.get("negative", []):
        if keyword in text_lower:
            matched_keywords.append(keyword)
    
    return {
        "mood": mood,
        "emoji": emoji,
        "keywords": matched_keywords
    }
