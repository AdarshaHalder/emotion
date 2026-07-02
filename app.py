"""
AI Voice Companion - Main Streamlit App
"""

import streamlit as st
import time
import os
from voice_input import transcribe_audio_bytes, record_voice_sample
from mood_detection import detect_mood, get_mood_emoji, analyze_mood_with_details
from ai_response import generate_ai_response, build_conversation_history
from voice_output import text_to_speech, get_audio_duration
from voice_cloning import get_user_voices, upload_voice_samples, delete_cloned_voice
from config import AVAILABLE_VOICES, OPENAI_API_KEY, ELEVENLABS_API_KEY, SUPPORTED_LANGUAGES

def _is_desktop():
    """True when sounddevice is available (local/desktop), False on cloud."""
    try:
        import sounddevice  # noqa: F401
        return True
    except Exception:
        return False

IS_DESKTOP = _is_desktop()

# Page configuration
st.set_page_config(
    page_title="AI Voice Companion",
    page_icon="🎙️",
    layout="centered"
)

# Hide Streamlit / Community Cloud branding (toolbar, footer, creator/profile badge)
st.markdown(
    """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    [data-testid="stToolbar"] {display: none !important;}
    [data-testid="stDecoration"] {display: none !important;}
    [data-testid="stStatusWidget"] {display: none !important;}
    /* Bottom-right creator / profile badge (avatar + crown) and viewer badge */
    [data-testid="stAppViewerBadge"],
    [data-testid="stAppCreatorAvatar"],
    [class*="_profileContainer_"],
    [class*="_profileButton_"],
    [class*="_profilePreview_"],
    [class*="_profileImage_"],
    [class*="_viewerBadge_"],
    [class*="viewerBadge"],
    a[href*="share.streamlit.io/user"],
    a[href*="streamlit.io/cloud"] {display: none !important;}
    </style>
    """,
    unsafe_allow_html=True,
)

# Initialize session state
if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []

if "selected_voice" not in st.session_state:
    st.session_state.selected_voice = list(AVAILABLE_VOICES.keys())[0]

if "recording_duration" not in st.session_state:
    st.session_state.recording_duration = 5

if "live_voice_samples" not in st.session_state:
    st.session_state.live_voice_samples = []  # list of (label, file_path)

if "cloned_voices" not in st.session_state:
    st.session_state.cloned_voices = {}

if "language" not in st.session_state:
    st.session_state.language = "en"


# App header
st.title("🎙️ AI Voice Companion")
st.markdown("*Your supportive friend for emotional well-being*")
st.divider()

# Sidebar - Settings
with st.sidebar:
    st.header("⚙️ Settings")
    
    # Voice selection
    st.subheader("🎤 Voice Profile")
    
    # Get all available voices (premade + cloned)
    all_voices = get_user_voices()
    cloned_voices = {v['name']: v['voice_id'] for v in all_voices if v.get('category') == 'cloned'}
    
    # Combine premade and cloned voices
    combined_voices = {**AVAILABLE_VOICES, **cloned_voices}
    
    if cloned_voices:
        st.success(f"✅ {len(cloned_voices)} cloned voice(s) available")

    # Store cloned voices so the main flow can auto-switch on negative mood
    st.session_state.cloned_voices = cloned_voices

    selected_voice_name = st.selectbox(
        "Choose a voice:",
        options=list(combined_voices.keys()),
        key="voice_selector"
    )
    st.session_state.selected_voice = selected_voice_name
    st.session_state.voice_id = combined_voices[selected_voice_name]
    
    # Language selection
    st.subheader("🌐 Language")
    lang_names = list(SUPPORTED_LANGUAGES.values())
    lang_codes = list(SUPPORTED_LANGUAGES.keys())
    current_idx = lang_codes.index(st.session_state.language) if st.session_state.language in lang_codes else 0
    selected_lang_name = st.selectbox("Speak in:", lang_names, index=current_idx, key="lang_selector")
    st.session_state.language = lang_codes[lang_names.index(selected_lang_name)]

    # Recording duration
    st.subheader("Recording Settings")
    st.session_state.recording_duration = st.slider(
        "Recording duration (seconds):",
        min_value=3,
        max_value=15,
        value=5
    )
    
    # API status
    st.divider()
    st.subheader("🔌 API Status")
    
    if OPENAI_API_KEY:
        st.success("✓ OpenAI Connected")
    else:
        st.error("✗ OpenAI Key Missing")
    
    if ELEVENLABS_API_KEY:
        st.success("✓ ElevenLabs Connected")
    else:
        st.error("✗ ElevenLabs Key Missing")
    
    # Voice Cloning Section
    st.divider()
    st.subheader("🎙️ Clone a Voice")
    
    with st.expander("➕ Add Family Member Voice"):
        st.markdown("**Clone voices of loved ones** (Mom, Dad, Wife, etc.)")

        voice_name = st.text_input("Voice Name (e.g., 'Mom', 'Dad')", key="clone_name")
        voice_desc = st.text_input("Description (optional)", key="clone_desc")

        # --- Live mic recording (desktop only) ---
        if IS_DESKTOP:
            st.markdown("**🎙️ Record Live Samples**")
            live_duration = st.slider("Sample duration (seconds)", 5, 30, 10, key="live_sample_dur")

            if st.button("⏺️ Record from Mic", key="record_live_sample"):
                with st.spinner(f"Recording for {live_duration}s... speak now!"):
                    path = record_voice_sample(duration=live_duration)
                if path:
                    label = f"Live sample {len(st.session_state.live_voice_samples) + 1}"
                    st.session_state.live_voice_samples.append((label, path))
                    st.success(f"✅ {label} captured")
                else:
                    st.error("❌ Recording failed — check microphone permissions")
        else:
            st.info("💡 Live mic recording available in the desktop app. Upload files below.")

        if st.session_state.live_voice_samples:
            st.caption(f"{len(st.session_state.live_voice_samples)} live sample(s) recorded:")
            for i, (label, _) in enumerate(st.session_state.live_voice_samples):
                col_a, col_b = st.columns([4, 1])
                col_a.write(f"🎤 {label}")
                if col_b.button("✕", key=f"del_live_{i}"):
                    removed = st.session_state.live_voice_samples.pop(i)
                    if os.path.exists(removed[1]):
                        os.remove(removed[1])
                    st.rerun()

        # --- File upload ---
        st.markdown("**📁 Or Upload Audio Files**")
        uploaded_files = st.file_uploader(
            "MP3 / WAV (30 sec each recommended)",
            type=["mp3", "wav"],
            accept_multiple_files=True,
            key="audio_samples",
        )

        total_samples = len(st.session_state.live_voice_samples) + len(uploaded_files or [])
        can_clone = bool(voice_name) and total_samples > 0

        if st.button("🎨 Clone Voice", disabled=not can_clone):
            with st.spinner("🎨 Cloning voice... This may take 1-2 minutes"):
                import tempfile
                temp_files = []

                # Add live-recorded samples
                for _, path in st.session_state.live_voice_samples:
                    temp_files.append(path)

                # Save uploaded files to temp paths
                for uploaded_file in (uploaded_files or []):
                    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
                    tmp.write(uploaded_file.read())
                    tmp.close()
                    temp_files.append(tmp.name)

                voice_id, clone_error = upload_voice_samples(
                    voice_name,
                    voice_desc or f"Cloned voice of {voice_name}",
                    temp_files
                )

                # Clean up only the uploaded temp files (not live samples — they're in session)
                for path in temp_files:
                    if path not in [p for _, p in st.session_state.live_voice_samples]:
                        if os.path.exists(path):
                            os.remove(path)

                if voice_id:
                    for _, path in st.session_state.live_voice_samples:
                        if os.path.exists(path):
                            os.remove(path)
                    st.session_state.live_voice_samples = []
                    st.success(f"✅ Voice '{voice_name}' cloned successfully!")
                    st.balloons()
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error(f"❌ {clone_error}")
    
    # Manage cloned voices
    if cloned_voices:
        with st.expander("🗑️ Manage Cloned Voices"):
            for voice_name, voice_id in cloned_voices.items():
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f"🎤 {voice_name}")
                with col2:
                    if st.button("❌", key=f"delete_{voice_id}"):
                        if delete_cloned_voice(voice_id):
                            st.success(f"Deleted {voice_name}")
                            time.sleep(1)
                            st.rerun()
    
    # Clear conversation
    st.divider()
    if st.button("🗑️ Clear Conversation"):
        st.session_state.conversation_history = []
        st.rerun()

# Main interface
col1, col2 = st.columns([3, 1])

with col1:
    st.subheader("💬 Conversation")

with col2:
    # Show current mood if conversation exists
    if st.session_state.conversation_history:
        last_user_msg = None
        for role, msg, _ in reversed(st.session_state.conversation_history):
            if role == "user":
                last_user_msg = msg
                break
        
        if last_user_msg:
            mood = detect_mood(last_user_msg)
            emoji = get_mood_emoji(mood)
            st.metric("Mood", f"{emoji} {mood.capitalize()}")

# Display conversation history
if st.session_state.conversation_history:
    for role, message, mood in st.session_state.conversation_history:
        if role == "user":
            with st.chat_message("user"):
                st.write(message)
                if mood:
                    st.caption(f"Mood: {get_mood_emoji(mood)} {mood}")
        else:
            with st.chat_message("assistant"):
                st.write(message)
else:
    st.info("👋 Click the button below to start talking!")

st.divider()

# Voice input section
st.subheader("🎤 Voice Input")
st.caption("Click the mic button, speak, then click stop to send your message.")

audio_value = st.audio_input("🔴 Push to Talk", key=f"voice_input_{st.session_state.get('audio_key', 0)}")

def _process_turn(user_text):
    """Run mood → AI → TTS pipeline for a transcribed user message."""
    st.success(f"**You said:** {user_text}")

    with st.spinner("🧠 Analyzing mood..."):
        mood_info = analyze_mood_with_details(user_text)
        mood = mood_info["mood"]
        emoji = mood_info["emoji"]
        st.info(f"**Detected mood:** {emoji} {mood.capitalize()}")

        if mood == "negative":
            st.warning("⚠️ **Family members have been notified (simulation)**")
            cloned = st.session_state.get("cloned_voices", {})
            if cloned:
                first_name, first_id = next(iter(cloned.items()))
                st.session_state.voice_id = first_id
                st.info(f"🎙️ Switching to **{first_name}'s** voice for support")

    with st.spinner("💭 Thinking..."):
        history = build_conversation_history(
            [(role, msg) for role, msg, _ in st.session_state.conversation_history]
        )
        ai_text = generate_ai_response(user_text, history, mood, language=st.session_state.language)
        st.success(f"**AI:** {ai_text}")

    with st.spinner("🔊 Generating voice..."):
        audio_file = text_to_speech(ai_text, st.session_state.voice_id, mood, language=st.session_state.language)

        if audio_file:
            with open(audio_file, "rb") as f:
                resp_bytes = f.read()
            audio_duration = get_audio_duration(audio_file)
            os.remove(audio_file)

            st.success("🔊 **Playing audio response...**")
            st.audio(resp_bytes, format="audio/mp3", autoplay=True)
            st.download_button("📥 Download Response", data=resp_bytes,
                               file_name="ai_response.mp3", mime="audio/mp3")

            st.session_state.conversation_history.append(("user", user_text, mood))
            st.session_state.conversation_history.append(("assistant", ai_text, None))
            st.session_state["audio_key"] = st.session_state.get("audio_key", 0) + 1

            time.sleep(max(audio_duration + 1.0, 3.0))
            st.rerun()
        else:
            st.error("Failed to generate voice response")
            st.session_state.conversation_history.append(("user", user_text, mood))
            st.session_state.conversation_history.append(("assistant", ai_text, None))
            st.session_state["audio_key"] = st.session_state.get("audio_key", 0) + 1
            time.sleep(0.5)
            st.rerun()

if audio_value:
    if not OPENAI_API_KEY or not ELEVENLABS_API_KEY:
        st.error("⚠️ Please configure API keys in .env file")
    else:
        with st.spinner("🎤 Transcribing..."):
            try:
                user_text = transcribe_audio_bytes(audio_value.read(), language=st.session_state.language)
                if user_text:
                    _process_turn(user_text)
                else:
                    st.error("❌ Could not transcribe audio. Please try again.")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

# Footer
st.divider()
st.caption("🤖 AI Voice Companion PoC • Built with Streamlit, OpenAI & ElevenLabs")

# JS fallback: remove the Community Cloud creator/profile badge from the live DOM.
# st.markdown strips <script>, so we run it from a zero-height component iframe that
# reaches into the parent document (same-origin) and keeps it hidden across reruns.
import streamlit.components.v1 as components

components.html(
    """
    <script>
    const strip = () => {
      try {
        const doc = window.parent && window.parent.document;
        if (!doc) return;
        const sels = [
          '[data-testid="stAppViewerBadge"]',
          '[data-testid="stAppCreatorAvatar"]',
          '[class*="_profileContainer_"]',
          '[class*="_profileButton_"]',
          '[class*="_viewerBadge_"]',
          '[class*="viewerBadge"]',
          'a[href*="share.streamlit.io/user"]'
        ];
        sels.forEach(s => doc.querySelectorAll(s).forEach(el => {
          el.style.display = 'none';
          if (el.parentElement) el.parentElement.style.display = 'none';
        }));
      } catch (e) { /* cross-origin: ignore */ }
    };
    strip();
    setInterval(strip, 500);
    </script>
    """,
    height=0,
)
