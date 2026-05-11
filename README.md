# AI Voice Companion

An AI-powered voice companion that listens, understands your emotions, and responds in a natural human voice — including the cloned voice of a family member.

---

## What It Does

- Records your voice and transcribes it using OpenAI Whisper
- Detects your emotional mood (positive / neutral / negative) using GPT
- Replies with an empathetic, human-sounding AI response
- Speaks the response aloud using ElevenLabs voice synthesis
- Automatically switches to a cloned family member's voice when you're feeling low
- Supports 18 languages including Hindi, Tamil, Telugu, Bengali, and more

---

## Requirements

Before you begin, make sure you have the following installed on your machine:

- **Python 3.10 or higher** — [Download here](https://www.python.org/downloads/)
- **Git** — [Download here](https://git-scm.com/downloads)
- A **microphone** connected to your computer

You will also need API keys for:

- **OpenAI** — [Get your key here](https://platform.openai.com/api-keys)
- **ElevenLabs** — [Get your key here](https://elevenlabs.io/app/settings/api-keys)

---

## Setup Instructions

### Step 1 — Clone the Repository

Open your terminal and run:

```bash
git clone https://github.com/AdarshaHalder/emotion.git
cd emotion
```

---

### Step 2 — Create a Virtual Environment

```bash
# macOS / Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

---

### Step 3 — Install Dependencies

**For web / browser use:**
```bash
pip install -r requirements.txt
```

**For desktop use (with full microphone support for voice cloning):**
```bash
pip install -r requirements-desktop.txt
```

---

### Step 4 — Configure API Keys

Copy the example environment file:

```bash
cp .env.example .env
```

Open the `.env` file in any text editor and fill in your keys:

```env
OPENAI_API_KEY=sk-your-openai-key-here
ELEVENLABS_API_KEY=your-elevenlabs-key-here
```

Save the file.

---

### Step 5 — Run the App

```bash
streamlit run app.py
```

The app will open automatically in your browser at `http://localhost:8501`

---

## How to Use

### Starting a Conversation

1. Open the app in your browser
2. Click the **microphone button** under "Voice Input"
3. Speak your message, then click **stop**
4. The app will transcribe, detect your mood, generate a response, and speak it back to you

### Changing the Voice

In the left sidebar, use the **"Choose a voice"** dropdown to select from several built-in voices.

### Changing the Language

In the left sidebar, select your preferred language from the **"Language"** dropdown. The app will transcribe and respond in that language.

### Cloning a Family Member's Voice

You can make the AI respond in the voice of someone you know (e.g., Mom, Dad):

1. In the sidebar, click **"Add Family Member Voice"**
2. Enter a name (e.g., `Mom`)
3. Upload 1–5 audio recordings of that person (MP3 or WAV, 30 seconds each recommended)
4. Click **"Clone Voice"**
5. The cloned voice will appear in the voice dropdown

> Note: Voice cloning requires an ElevenLabs paid plan (Starter or above).

When a negative mood is detected, the app automatically switches to the cloned voice for emotional support.

---

## Running as a Desktop App (macOS)

If you received a `.dmg` file:

1. Double-click `AIVoiceCompanion.dmg`
2. Drag `AIVoiceCompanion` into your **Applications** folder
3. Open the app from Applications

No Python installation required for the desktop version.

---

## Online Version

The app is also accessible online (no installation needed):

> [https://emotion-scriptures.streamlit.app](https://emotion-scriptures.streamlit.app)

> Note: The online version uses your browser's microphone. The voice cloning live-recording feature is only available in the desktop app.

---

## Project Structure

```
emotion/
├── app.py                  # Main Streamlit application
├── config.py               # API keys and settings
├── ai_response.py          # GPT response generation
├── mood_detection.py       # GPT-based mood classification
├── voice_input.py          # Audio recording and transcription
├── voice_output.py         # ElevenLabs text-to-speech
├── voice_cloning.py        # Voice cloning via ElevenLabs
├── desktop_app.py          # Desktop launcher (PyWebView)
├── requirements.txt        # Dependencies for web/cloud
├── requirements-desktop.txt# Dependencies for desktop
├── build_mac.sh            # Build script for macOS .dmg
├── build_windows.bat       # Build script for Windows .exe
├── EMOTION.spec            # PyInstaller configuration
└── .env.example            # Environment variable template
```

---

## Troubleshooting

**Microphone not working**
- Make sure your browser has microphone permission enabled
- On macOS, go to System Settings → Privacy & Security → Microphone

**API errors**
- Double-check your API keys in the `.env` file
- Make sure you have credits/quota available on OpenAI and ElevenLabs

**Module not found**
- Make sure your virtual environment is activated before running
- Re-run `pip install -r requirements.txt`

**App not opening**
- Make sure port 8501 is not in use
- Try: `streamlit run app.py --server.port 8502`

---

## API Cost Estimate (for reference)

| Service | Usage | Approx. Cost |
|---|---|---|
| OpenAI Whisper | Per voice message | ~$0.006 / minute |
| OpenAI GPT-3.5 | Per response | ~$0.002 / conversation |
| ElevenLabs TTS | Per response | Free tier: 10k chars/month |

For a 1-week demo: approximately **$5–10 total**.

---

## Support

For any issues, contact the development team or raise an issue on GitHub:
[https://github.com/AdarshaHalder/emotion/issues](https://github.com/AdarshaHalder/emotion/issues)
