# 🚀 QUICK START GUIDE - AI Voice Companion Desktop App

## ✅ What's Installed:
- Python environment with all dependencies
- Streamlit web app
- **PyWebView desktop wrapper**
- API keys configured

---

## 🖥️ Run Desktop App (Native Window)

```bash
./run_desktop.sh
```

**What happens:**
- Native desktop window opens
- No browser tabs needed
- Runs like a real desktop app
- Auto-starts Streamlit in background

---

## 🌐 Run Web Version (Browser)

```bash
source venv/bin/activate
streamlit run app.py
```

Then open: http://localhost:8501

---

## 📱 Desktop App Features:

✅ **Native Window** - Feels like a real desktop app  
✅ **No Browser** - Runs standalone  
✅ **Resizable** - Min size 800x600  
✅ **Auto-Start** - Streamlit starts automatically  
✅ **Clean UI** - No browser chrome/toolbars  

---

## 🎯 How to Use:

1. **Launch**: `./run_desktop.sh`
2. **Wait 3 seconds**: Window opens automatically
3. **Select voice**: Choose from sidebar
4. **Click "Push to Talk"**: Record your message
5. **Listen**: AI responds with voice

---

## 🛠️ Troubleshooting:

### Port already in use:
```bash
# Kill existing Streamlit process
pkill -f streamlit
```

### Desktop window doesn't open:
```bash
# Check if Streamlit is running
lsof -i :8501

# Try web version
streamlit run app.py
```

### Permission denied:
```bash
chmod +x run_desktop.sh
```

---

## 📊 Comparison:

| Feature | Desktop App | Web Version |
|---------|-------------|-------------|
| Window | Native | Browser Tab |
| Start | Double-click | Terminal command |
| UI | Clean | Browser chrome |
| Feel | Desktop app | Website |

---

## 💡 Tips:

- **Desktop app** is recommended for daily use
- **Web version** is good for development/testing
- Both use the same backend code
- Desktop app uses less resources (no full browser)

---

## 🎊 Your App is Ready!

Just run: `./run_desktop.sh`

Enjoy your AI Voice Companion! 🎙️
