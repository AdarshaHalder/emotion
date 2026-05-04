"""
Voice Cloning Module
Allow users to clone voices from audio samples (Mom, Dad, Wife, etc.)
"""

import requests
from config import ELEVENLABS_API_KEY


def upload_voice_samples(name, description, audio_files):
    """
    Upload audio samples to create a cloned voice
    
    Args:
        name: Name for the cloned voice (e.g., "Mom", "Dad")
        description: Description of the voice
        audio_files: List of audio file paths (min 1, recommended 3-5)
    
    Returns:
        voice_id if successful, None otherwise
    """
    url = "https://api.elevenlabs.io/v1/voices/add"
    
    headers = {
        "xi-api-key": ELEVENLABS_API_KEY
    }
    
    # Prepare files for upload
    files = []
    for i, audio_file in enumerate(audio_files):
        with open(audio_file, 'rb') as f:
            files.append(('files', (f"sample_{i}.mp3", f.read(), 'audio/mpeg')))
    
    data = {
        'name': name,
        'description': description,
    }
    
    try:
        response = requests.post(url, headers=headers, data=data, files=files)

        if response.status_code == 200:
            result = response.json()
            voice_id = result.get('voice_id')
            print(f"✅ Voice '{name}' cloned successfully! Voice ID: {voice_id}")
            return voice_id, None
        else:
            body = response.json() if response.headers.get("content-type", "").startswith("application/json") else {}
            detail = body.get("detail", {})
            code = detail.get("code", "") if isinstance(detail, dict) else ""
            msg = detail.get("message", response.text) if isinstance(detail, dict) else str(detail)

            if code == "paid_plan_required":
                human_msg = "Voice cloning requires an ElevenLabs paid plan (Creator or above). Please upgrade at elevenlabs.io."
            else:
                human_msg = msg or f"ElevenLabs error {response.status_code}"

            print(f"❌ Error cloning voice: {response.status_code} — {human_msg}")
            return None, human_msg

    except Exception as e:
        print(f"❌ Error: {e}")
        return None, str(e)


def get_user_voices():
    """
    Get all voices (including cloned ones) from user's account
    
    Returns:
        List of voice dictionaries
    """
    url = "https://api.elevenlabs.io/v1/voices"
    headers = {"xi-api-key": ELEVENLABS_API_KEY}
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            return data.get("voices", [])
        return []
    except:
        return []


def delete_cloned_voice(voice_id):
    """
    Delete a cloned voice
    
    Args:
        voice_id: ID of the voice to delete
    
    Returns:
        True if successful, False otherwise
    """
    url = f"https://api.elevenlabs.io/v1/voices/{voice_id}"
    headers = {"xi-api-key": ELEVENLABS_API_KEY}
    
    try:
        response = requests.delete(url, headers=headers)
        return response.status_code == 200
    except:
        return False


def get_voice_info(voice_id):
    """
    Get detailed information about a voice
    
    Args:
        voice_id: ID of the voice
    
    Returns:
        Voice information dictionary
    """
    url = f"https://api.elevenlabs.io/v1/voices/{voice_id}"
    headers = {"xi-api-key": ELEVENLABS_API_KEY}
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        return None
    except:
        return None
