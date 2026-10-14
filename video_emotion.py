"""
Video Emotion Module
Detects facial emotion from video frames / camera snapshots using GPT-4o-mini vision,
transcribes the speech in a video via Whisper, and fuses face + speech into one mood.
"""

import base64
import json
import os
import tempfile

from openai import OpenAI
from config import OPENAI_API_KEY
from voice_input import speech_to_text

# Facial emotion → coarse mood used by the rest of the pipeline
EMOTION_TO_MOOD = {
    "happy": "positive",
    "surprised": "neutral",
    "neutral": "neutral",
    "sad": "negative",
    "angry": "negative",
    "fearful": "negative",
    "disgusted": "negative",
}

EMOTION_EMOJIS = {
    "happy": "😄",
    "surprised": "😮",
    "neutral": "😐",
    "sad": "😢",
    "angry": "😠",
    "fearful": "😨",
    "disgusted": "🤢",
}

WHISPER_MAX_BYTES = 25 * 1024 * 1024


def extract_frames(video_path, num_frames=4, max_side=512):
    """
    Sample evenly spaced frames from a video and return them as JPEG bytes.
    Frames are downscaled so the longest side is at most `max_side` px.
    """
    import cv2

    cap = cv2.VideoCapture(video_path)
    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) or 0
    # Skip the very first/last frames (often blank or motion-blurred)
    if total > 0:
        indices = [int(total * (i + 1) / (num_frames + 1)) for i in range(num_frames)]
    else:
        indices = []

    frames = []
    for idx in indices:
        cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
        ok, frame = cap.read()
        if not ok:
            continue
        h, w = frame.shape[:2]
        scale = max_side / max(h, w)
        if scale < 1:
            frame = cv2.resize(frame, (int(w * scale), int(h * scale)))
        ok, buf = cv2.imencode(".jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, 85])
        if ok:
            frames.append(buf.tobytes())

    # Some containers don't report a frame count — fall back to reading sequentially
    if not frames:
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        ok, frame = cap.read()
        if ok:
            ok, buf = cv2.imencode(".jpg", frame)
            if ok:
                frames.append(buf.tobytes())

    cap.release()
    return frames


def detect_facial_emotion(images):
    """
    Classify the facial emotion shown across one or more images (JPEG/PNG bytes).

    Returns:
        dict with emotion, mood, emoji, confidence, description
        (emotion is "unknown" if no face is visible or the call fails)
    """
    if not images:
        return _unknown("No frames could be read.")

    content = [{
        "type": "text",
        "text": (
            "These are frames of one person from a short video or camera snapshot. "
            "Read their facial expression and body language across all frames. Reply with JSON only: "
            '{"face_visible": true|false, '
            '"emotion": "happy|sad|angry|fearful|surprised|disgusted|neutral", '
            '"confidence": 0.0-1.0, '
            '"description": "one short sentence on the visible cues, e.g. teary eyes, forced smile"}. '
            "Look for subtle signs (downcast eyes, tension, masked sadness behind a smile)."
        ),
    }]
    for img in images:
        b64 = base64.b64encode(img).decode()
        content.append({
            "type": "image_url",
            "image_url": {"url": f"data:image/jpeg;base64,{b64}", "detail": "low"},
        })

    try:
        client = OpenAI(api_key=OPENAI_API_KEY)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": content}],
            response_format={"type": "json_object"},
            temperature=0,
            max_tokens=120,
        )
        data = json.loads(response.choices[0].message.content)
    except Exception as e:
        print(f"Error detecting facial emotion: {e}")
        return _unknown("Facial analysis failed.")

    if not data.get("face_visible", True):
        return _unknown("No face visible.")

    emotion = str(data.get("emotion", "neutral")).lower()
    if emotion not in EMOTION_TO_MOOD:
        emotion = "neutral"
    return {
        "emotion": emotion,
        "mood": EMOTION_TO_MOOD[emotion],
        "emoji": EMOTION_EMOJIS[emotion],
        "confidence": float(data.get("confidence", 0.5) or 0.5),
        "description": data.get("description", ""),
    }


def _unknown(reason):
    return {
        "emotion": "unknown",
        "mood": None,
        "emoji": "❔",
        "confidence": 0.0,
        "description": reason,
    }


def transcribe_video(video_path, language="auto"):
    """
    Transcribe the speech track of a video with Whisper.
    Whisper accepts mp4/webm/m4a directly; for larger files the audio is
    extracted to mp3 first (requires ffmpeg via pydub).

    Returns:
        transcribed text or None
    """
    path = video_path
    if os.path.getsize(video_path) > WHISPER_MAX_BYTES:
        try:
            from pydub import AudioSegment
            audio = AudioSegment.from_file(video_path).set_channels(1)
            tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
            tmp.close()
            audio.export(tmp.name, format="mp3", bitrate="64k")
            path = tmp.name
        except Exception as e:
            print(f"Error extracting audio from video: {e}")
            return None
    else:
        # speech_to_text deletes the file it reads, so hand it a copy
        ext = ".webm" if video_path.lower().endswith(".webm") else ".mp4"
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=ext)
        with open(video_path, "rb") as src:
            tmp.write(src.read())
        tmp.close()
        path = tmp.name

    return speech_to_text(path, language=language)


def analyze_video_bytes(video_bytes, filename="video.mp4", language="auto", num_frames=4):
    """
    Full video pipeline: save → sample frames → facial emotion → transcribe speech.

    Returns:
        (face_info dict, transcript str or None)
    """
    suffix = os.path.splitext(filename)[1].lower() or ".mp4"
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    tmp.write(video_bytes)
    tmp.close()
    try:
        frames = extract_frames(tmp.name, num_frames=num_frames)
        face_info = detect_facial_emotion(frames)
        transcript = transcribe_video(tmp.name, language=language)
        return face_info, (transcript or "").strip() or None
    finally:
        if os.path.exists(tmp.name):
            os.remove(tmp.name)


def fuse_moods(text_mood, face_mood):
    """
    Combine speech mood and facial mood. Negative from either side wins
    (people often mask distress in one channel), then positive, then neutral.
    """
    moods = {m for m in (text_mood, face_mood) if m}
    if "negative" in moods:
        return "negative"
    if "positive" in moods:
        return "positive"
    return "neutral"
