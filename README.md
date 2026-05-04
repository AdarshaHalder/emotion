# 🎙️ AI Voice Companion - Emotional Support PoC

A complete working prototype of an AI-powered voice companion that provides emotional support through natural conversation.

## 🎯 Features

- ✅ **Voice Input**: Push-to-talk recording with speech-to-text
- ✅ **Mood Detection**: Rule-based keyword detection (positive/neutral/negative)
- ✅ **AI Response**: Empathetic responses using GPT-3.5
- ✅ **Voice Output**: Natural-sounding voice using ElevenLabs
- ✅ **Voice Selection**: Choose from multiple voice profiles
- ✅ **Voice Cloning**: Clone voices of loved ones (Mom, Dad, Wife, etc.) 🌟
- ✅ **Alert Simulation**: Notification when negative mood is detected
- ✅ **Conversation History**: Track the full conversation
- ✅ **Clean UI**: Simple Streamlit interface
- ✅ **Desktop App**: Native desktop application (PyWebView)

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Setup API Keys

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Edit `.env` and add your API keys:

```env
OPENAI_API_KEY=sk-your-openai-api-key-here
ELEVENLABS_API_KEY=your-elevenlabs-api-key-here
```

**Get your API keys:**
- OpenAI: https://platform.openai.com/api-keys
- ElevenLabs: https://elevenlabs.io/app/settings/api-keys

### 3. Run the App

**Option A: Desktop App (Recommended)**

```bash
# macOS/Linux
chmod +x run_desktop.sh
./run_desktop.sh

# Windows
run_desktop.bat
```

**Option B: Web Browser**

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## 📁 Project Structure

```
/EMOTION
├── app.py                 # Main Streamlit application
├── desktop_app.py         # Desktop app launcher (PyWebView)
├── voice_input.py         # Audio recording & speech-to-text
├── mood_detection.py      # Rule-based mood classification
├── ai_response.py         # LLM response generation
├── voice_output.py        # Text-to-speech conversion
├── config.py             # Configuration & settings
├── requirements.txt      # Python dependencies
├── run_desktop.sh        # Desktop launcher (macOS/Linux)
├── run_desktop.bat       # Desktop launcher (Windows)
├── .env.example         # Example environment file
└── README.md            # This file
```

## 🎮 How to Use

1. **Start the app**: `./run_desktop.sh` or `streamlit run app.py`
2. **Select a voice**: Choose from the sidebar dropdown
3. **Click "Push to Talk"**: Record your message (default 5 seconds)
4. **Wait for response**: AI will analyze, respond, and speak
5. **View mood**: Check detected mood in the conversation
6. **Continue talking**: Build a natural conversation

### 🎙️ Clone Family Voices (New!)

Want AI to speak in Mom's or Dad's voice?

1. **Prepare audio samples**: 1-5 recordings (30 sec each)
2. **Go to sidebar** → "Clone a Voice"
3. **Upload samples**: MP3/WAV files
4. **Click "Clone Voice"**: Wait 1-2 minutes
5. **Select cloned voice**: Choose from dropdown!

See [VOICE_CLONING_GUIDE.md](VOICE_CLONING_GUIDE.md) for detailed instructions.

## 🧠 How It Works

### Voice Input Flow
```
Microphone → Audio Recording → Whisper API → Text
```

### Mood Detection
Simple keyword matching:
- **Negative**: sad, lonely, depressed, upset, anxious...
- **Positive**: happy, great, awesome, excited...
- **Neutral**: Everything else

### AI Response
```
User Text + Mood + History → GPT-3.5 → Empathetic Response
```

### Voice Output
```
AI Text → ElevenLabs API → Audio File → Play in Browser
```

## ⚙️ Configuration

Edit `config.py` to customize:

- **Voices**: Add more ElevenLabs voice IDs
- **Recording duration**: Change default recording time
- **Mood keywords**: Modify keyword lists
- **System prompt**: Adjust AI personality

## 🔧 Troubleshooting

### No audio input detected
- Check microphone permissions
- Test with: `python -c "import sounddevice; print(sounddevice.query_devices())"`

### API errors
- Verify API keys are correct in `.env`
- Check API credit balance
- Ensure internet connection

### Module not found
- Run: `pip install -r requirements.txt`
- Use Python 3.8+

## 🎨 Customization Ideas

1. **Add more voices**: Get voice IDs from ElevenLabs and add to `config.py`
2. **Better mood detection**: Use sentiment analysis library
3. **Export conversation**: Add button to save chat history
4. **Multiple languages**: Change Whisper language parameter
5. **Custom triggers**: Add more alert conditions

## 📝 API Costs (Estimate)

- **OpenAI Whisper**: ~$0.006 per minute of audio
- **OpenAI GPT-3.5**: ~$0.002 per conversation
- **ElevenLabs**: Varies by plan (free tier: 10k characters/month)

**For 1 week PoC**: ~$5-10 total

## ⚠️ Important Notes

- This is a **PROTOTYPE** for demonstration only
- NOT for production use
- NOT a replacement for professional mental health support
- Alert system is **simulated** (no real notifications)

## 🤝 Contributing

This is a PoC. Feel free to:
- Fork and experiment
- Add features
- Improve UI
- Share feedback

## 📄 License

MIT License - Free to use and modify

## 🙏 Acknowledgments

- OpenAI for Whisper & GPT
- ElevenLabs for voice synthesis
- Streamlit for the UI framework

---

**Built with ❤️ as a 1-week PoC**

**Questions?** Check the code comments or API documentation.
