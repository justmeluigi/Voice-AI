# 🎙️ Voice AI - Speech to Text & Kokoro Text-to-Speech

A high-performance AI voice platform featuring **OpenAI Whisper** for high-accuracy audio transcription & word-level timing, and **Kokoro-82M** for natural, lifelike text-to-speech with 26 expressive preset voices.

---

## ✨ Features

### 🎙️ 1. Speech to Text (Whisper STT)
- **Multi-Format Audio & Video Support**:
  - Drag & drop or browse files: MP3, WAV, M4A, FLAC, OGG, AAC, WEBM, MP4, WMA.
- **Live Microphone Recording**:
  - Real-time frequency waveform visualizer via HTML5 Web Audio API.
  - Recording timer, pause, resume, and preview playback before transcribing.
- **Model Selection & In-Memory Caching**:
  - Choose between Whisper **Tiny** (39M), **Base** (74M), **Small** (244M), and **Medium** (769M).
  - Models are cached in memory for zero re-load delay on subsequent requests.
- **Word-by-Word Timestamps & Karaoke Highlighting**:
  - Millisecond-accurate start and end times for every single word spoken.
  - Interactive **Word Timestamps** tab displaying word tokens, durations (e.g. `450ms`), and confidence probabilities.
  - Real-time karaoke-style word highlighting as the audio plays.
  - Click any word to instantly jump audio playback directly to that word.
  - Export word-level data as **CSV (`.csv`)** and **JSON (`.json`)**.
- **Interactive Segmented Timestamps**:
  - Synchronized audio player: clicking any segment jumps audio playback directly to that timestamp.
  - Active segment highlights in real-time as the audio plays.
- **Direct Bridge to Kokoro**:
  - One-click "Speak Text with Kokoro TTS" button immediately transfers transcribed text to speech synthesis.
- **Export Formats**:
  - **Plain Text (`.txt`)**
  - **Word Timestamps CSV (`.csv`)**
  - **SubRip Subtitles (`.srt`)**
  - **WebVTT Subtitles (`.vtt`)**
  - **Full Structured Data (`.json`)**

---

### 🔊 2. Text to Speech (Kokoro TTS)
- **Ultra-Natural Kokoro-82M Neural Model**:
  - Generates human-like, expressive speech at 24kHz audio quality.
  - Ultra-fast synthesis with in-memory pipeline caching.
- **26 Preset Voice Profiles**:
  - **🇺🇸 American Female**:
    - `af_heart` (Heart - Warm & Natural ⭐ Flagship)
    - `af_bella` (Bella - Cheerful & Vibrant)
    - `af_nicole` (Nicole - Calm & Narrative)
    - `af_aoede` (Aoede - Smooth & Melodic)
    - `af_kore` (Kore - Gentle & Soft)
    - `af_sarah` (Sarah - Articulate & Professional)
    - `af_sky` (Sky - Bright & Upbeat)
    - `af_alloy` (Alloy - Neutral & Clear)
    - `af_jessica` (Jessica - Expressive)
    - `af_river` (River - Conversational)
  - **🇺🇸 American Male**:
    - `am_adam` (Adam - Deep & Authoritative)
    - `am_michael` (Michael - Friendly & Professional)
    - `am_echo` (Echo - Warm & Resonant)
    - `am_eric` (Eric - Conversational & Crisp)
    - `am_fenrir` (Fenrir - Deep & Cinematic)
    - `am_liam` (Liam - Youthful & Energetic)
    - `am_onyx` (Onyx - Rich & Deep)
    - `am_puck` (Puck - Lively & Animated)
  - **🇬🇧 British Female**:
    - `bf_emma` (Emma - Classic British RP)
    - `bf_isabella` (Isabella - Soft & Elegant)
    - `bf_alice` (Alice - Refined & Articulate)
    - `bf_lily` (Lily - Warm & Expressive)
  - **🇬🇧 British Male**:
    - `bm_george` (George - Refined British Gentleman)
    - `bm_fable` (Fable - Audiobook Narrator)
    - `bm_lewis` (Lewis - Intellectual & Calm)
    - `bm_daniel` (Daniel - Modern British)
- **Controls & Features**:
  - Real-time voice category filtering (All, 🇺🇸 American, 🇬🇧 British, Female, Male).
  - Speaking speed slider (0.5x to 2.0x).
  - Character & word counter.
  - One-click sample prompts (Greeting, Story, Assistant).
  - In-browser 24kHz audio player with real-time waveform.
  - Direct `.WAV` audio download.

---

## 🖥️ Desktop Application (Native Rust)

**Voice AI** is packaged as a high-performance **native Rust desktop application** (`voice-ai.exe`) powered by **Tao** (native windowing) and **Wry / WebView2** (hardware-accelerated Webview).

### ✨ Desktop App Highlights:
- **Standalone `.exe`**: Compiled directly with Rust 2021 edition and MSVC.
- **Zero-Configuration Daemon Lifecycle**:
  - Automatically launches the Python AI backend silently in the background (no ugly black command prompt windows).
  - Waits until Whisper & Kokoro APIs are healthy.
  - Automatically terminates backend worker processes when you close the desktop app window.
- **Hardware-Accelerated UI**: Native 60+ FPS smooth rendering, dark theme background with zero white-flash on startup.

### 🚀 Running the Desktop App:
- **Option 1**: Double-click **[`voice-ai.exe`](file:///d:/Whisper%20Audio%20Transcription/voice-ai.exe)** in the project folder.
- **Option 2**: Run **[`launch-desktop.bat`](file:///d:/Whisper%20Audio%20Transcription/launch-desktop.bat)**.
- **Option 3**: In terminal:
  ```powershell
  .\voice-ai.exe
  ```

---

## 🚀 Running via Web Browser (Alternative)

If you prefer using your standard browser instead of the desktop window:
```powershell
python app.py
```
Or double-click `run.bat` and visit:
👉 **[http://127.0.0.1:8000](http://127.0.0.1:8000)**

---

## 🛠️ API Reference

- `GET /api/info`: System hardware, loaded models, and voice statistics.
- `GET /api/languages`: 99 supported Whisper languages.
- `POST /api/transcribe`: Audio transcription & translation with word timestamps.
- `GET /api/tts/voices`: List of all 26 Kokoro preset voices with metadata.
- `POST /api/tts/synthesize`: Synthesize text to speech (`{ "text": "...", "voice": "af_heart", "speed": 1.0 }`).
- `GET /api/tts/audio/{filename}`: Stream or download generated audio.
