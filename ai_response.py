"""
AI Response Module
Generate empathetic responses using OpenAI LLM
"""

from openai import OpenAI
from config import OPENAI_API_KEY, SYSTEM_PROMPT


# Unicode ranges → language, to pin the reply language to the user's *latest* message
_SCRIPT_RANGES = [
    ((0x0980, 0x09FF), "Bengali"),
    ((0x0900, 0x097F), "Hindi (or the Devanagari-script language they used)"),
    ((0x0B80, 0x0BFF), "Tamil"),
    ((0x0C00, 0x0C7F), "Telugu"),
    ((0x0A80, 0x0AFF), "Gujarati"),
    ((0x0A00, 0x0A7F), "Punjabi"),
    ((0x0600, 0x06FF), "Arabic"),
    ((0x0400, 0x04FF), "Russian"),
    ((0xAC00, 0xD7AF), "Korean"),
    ((0x3040, 0x30FF), "Japanese"),
    ((0x4E00, 0x9FFF), "Chinese"),
]


def _detect_reply_language(text):
    """Guess the language of `text` from its dominant script (Latin → English by default)."""
    counts = {}
    latin = 0
    for ch in text or "":
        cp = ord(ch)
        if ch.isascii():
            latin += ch.isalpha()
            continue
        for (lo, hi), name in _SCRIPT_RANGES:
            if lo <= cp <= hi:
                counts[name] = counts.get(name, 0) + 1
                break
    if counts:
        name, n = max(counts.items(), key=lambda kv: kv[1])
        if n >= latin:
            return name
    return "English (or the Latin-script language they actually used, e.g. Spanish/French)"


def generate_ai_response(user_message, conversation_history=None, mood=None, language="en", face_info=None):
    """
    Generate AI response using OpenAI API
    
    Args:
        user_message: user's current message
        conversation_history: list of previous messages (optional)
        mood: detected mood (optional)
        face_info: facial emotion dict from video_emotion (optional)
    
    Returns:
        AI response text
    """
    try:
        client = OpenAI(api_key=OPENAI_API_KEY)
        
        # Build conversation messages
        from config import SUPPORTED_LANGUAGES
        if not language or language == "auto":
            # Mirror whatever language the user actually spoke.
            system = SYSTEM_PROMPT + (
                "\n\nDetect the language of the user's message and reply ONLY in that "
                "same language, using its native script. If they wrote in Bengali, reply "
                "in Bengali; if Tamil, reply in Tamil; and so on. Never switch to English "
                "unless the user actually wrote in English. Keep it natural and "
                "grammatically correct."
            )
        else:
            lang_name = SUPPORTED_LANGUAGES.get(language, "English")
            system = SYSTEM_PROMPT + (
                f"\n\nALWAYS respond in {lang_name}. Even if the user writes in another "
                f"language, reply ONLY in natural, grammatically correct {lang_name} using "
                f"its native script. Never mix in English words or fall back to English."
            )

        # Inject mood-aware layer
        if mood == "negative":
            system += "\n\nRight now the person is struggling. Be especially soft and present. Don't rush to solutions — just be with them first."
        elif mood == "positive":
            system += "\n\nThe person is in a good place. Match their energy — be warm, light, and genuinely happy for them."

        # Inject what we can see on their face (video / camera input)
        if face_info and face_info.get("emotion") not in (None, "unknown"):
            system += (
                f"\n\nYou can also see the person on camera. Their face looks "
                f"{face_info['emotion']}"
                + (f" ({face_info['description']})" if face_info.get("description") else "")
                + ". Respond to what you see as a friend would — naturally, not like a "
                "report. If their face and their words don't match (e.g. smiling but "
                "saying they're fine while looking sad), gently notice it."
            )

        messages = [{"role": "system", "content": system}]

        # Add conversation history if provided
        if conversation_history:
            messages.extend(conversation_history)

        # In auto mode, pin the language to THIS message so earlier turns in another
        # language don't drag the reply along (placed last = strongest signal).
        if not language or language == "auto":
            reply_lang = _detect_reply_language(user_message)
            messages.append({
                "role": "system",
                "content": (
                    f"The user's latest message is in {reply_lang}. Reply ONLY in that "
                    "language, regardless of what language earlier messages were in."
                ),
            })

        # Add current user message
        messages.append({"role": "user", "content": user_message})

        # Generate response
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # far stronger at Tamil/Telugu & other non-English than gpt-3.5
            messages=messages,
            temperature=0.9,
            max_tokens=200
        )
        
        ai_message = response.choices[0].message.content
        return ai_message
    
    except Exception as e:
        print(f"Error generating AI response: {e}")
        return "I'm here for you. Could you tell me more about how you're feeling?"


def build_conversation_history(history_list):
    """
    Convert conversation history to OpenAI message format
    
    Args:
        history_list: list of tuples (role, message)
    
    Returns:
        list of message dicts
    """
    messages = []
    for role, content in history_list:
        messages.append({"role": role, "content": content})
    return messages
