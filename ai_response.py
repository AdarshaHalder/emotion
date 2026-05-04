"""
AI Response Module
Generate empathetic responses using OpenAI LLM
"""

from openai import OpenAI
from config import OPENAI_API_KEY, SYSTEM_PROMPT


def generate_ai_response(user_message, conversation_history=None, mood=None, language="en"):
    """
    Generate AI response using OpenAI API
    
    Args:
        user_message: user's current message
        conversation_history: list of previous messages (optional)
        mood: detected mood (optional)
    
    Returns:
        AI response text
    """
    try:
        client = OpenAI(api_key=OPENAI_API_KEY)
        
        # Build conversation messages
        from config import SUPPORTED_LANGUAGES
        lang_name = SUPPORTED_LANGUAGES.get(language, "English")
        system = SYSTEM_PROMPT + f"\n\nALWAYS respond in {lang_name}. Even if the user writes in another language, reply in {lang_name}."

        # Inject mood-aware layer
        if mood == "negative":
            system += "\n\nRight now the person is struggling. Be especially soft and present. Don't rush to solutions — just be with them first."
        elif mood == "positive":
            system += "\n\nThe person is in a good place. Match their energy — be warm, light, and genuinely happy for them."

        messages = [{"role": "system", "content": system}]

        # Add conversation history if provided
        if conversation_history:
            messages.extend(conversation_history)

        # Add current user message
        messages.append({"role": "user", "content": user_message})

        # Generate response
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
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
