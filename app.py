import os
import time
import shutil
import tempfile
import threading
import uuid
from typing import Optional, List, Dict, Any
from pathlib import Path

from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import numpy as np
import soundfile as sf
import torch
import whisper
from kokoro import KPipeline

app = FastAPI(title="Voice AI - Speech to Text & Kokoro TTS", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"
STATIC_DIR.mkdir(exist_ok=True)

AUDIO_OUT_DIR = BASE_DIR / "generated_audio"
AUDIO_OUT_DIR.mkdir(exist_ok=True)

COMPRESSED_AUDIO_DIR = BASE_DIR / "compressed_audio"
COMPRESSED_AUDIO_DIR.mkdir(exist_ok=True)

MIME_TYPES = {
    "mp3": "audio/mpeg",
    "m4a": "audio/mp4",
    "aac": "audio/aac",
    "ogg": "audio/ogg",
    "opus": "audio/ogg",
    "wav": "audio/wav",
    "flac": "audio/flac",
    "webm": "audio/webm",
}

# Hardware Detection
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
DEVICE_NAME = torch.cuda.get_device_name(0) if torch.cuda.is_available() else "CPU"

# Whisper Models
AVAILABLE_MODELS = {
    "tiny": {
        "name": "Tiny",
        "parameters": "39 M",
        "vram": "~1 GB",
        "speed": "Ultra Fast (~32x)",
        "description": "Fastest model, low resource usage. Good for quick drafts."
    },
    "base": {
        "name": "Base",
        "parameters": "74 M",
        "vram": "~1 GB",
        "speed": "Fast (~16x)",
        "description": "Great balance between speed and accuracy for general speech."
    },
    "small": {
        "name": "Small",
        "parameters": "244 M",
        "vram": "~2 GB",
        "speed": "Moderate (~6x)",
        "description": "High accuracy, very good at accents and technical terms."
    },
    "medium": {
        "name": "Medium",
        "parameters": "769 M",
        "vram": "~5 GB",
        "speed": "Slow (~2x)",
        "description": "Maximum accuracy for complex audio, multilingual, or noisy inputs."
    }
}

_whisper_models: Dict[str, Any] = {}
_whisper_lock = threading.Lock()
_current_loaded_whisper: Optional[str] = None

import json

CUSTOM_VOICES_FILE = BASE_DIR / "custom_voices.json"

# Kokoro Preset & Community Voices
KOKORO_PRESET_VOICES = [
    # ====================================================
    # OFFICIAL AMERICAN FEMALE (11)
    # ====================================================
    {"id": "af_heart", "name": "Heart", "category": "official", "gender": "Female", "accent": "American", "flag": "🇺🇸", "trait": "Warm & Natural", "recommended": True, "avatar": "❤️"},
    {"id": "af_nova", "name": "Nova", "category": "official", "gender": "Female", "accent": "American", "flag": "🇺🇸", "trait": "Crisp & Modern Studio", "recommended": True, "avatar": "🌟"},
    {"id": "af_bella", "name": "Bella", "category": "official", "gender": "Female", "accent": "American", "flag": "🇺🇸", "trait": "Cheerful & Vibrant", "avatar": "🌸"},
    {"id": "af_nicole", "name": "Nicole", "category": "official", "gender": "Female", "accent": "American", "flag": "🇺🇸", "trait": "Calm & Narrative", "avatar": "🎙️"},
    {"id": "af_aoede", "name": "Aoede", "category": "official", "gender": "Female", "accent": "American", "flag": "🇺🇸", "trait": "Smooth & Melodic", "avatar": "🎵"},
    {"id": "af_kore", "name": "Kore", "category": "official", "gender": "Female", "accent": "American", "flag": "🇺🇸", "trait": "Gentle & Soft", "avatar": "🌿"},
    {"id": "af_sarah", "name": "Sarah", "category": "official", "gender": "Female", "accent": "American", "flag": "🇺🇸", "trait": "Articulate & Professional", "avatar": "💼"},
    {"id": "af_sky", "name": "Sky", "category": "official", "gender": "Female", "accent": "American", "flag": "🇺🇸", "trait": "Bright & Upbeat", "avatar": "☀️"},
    {"id": "af_alloy", "name": "Alloy", "category": "official", "gender": "Female", "accent": "American", "flag": "🇺🇸", "trait": "Neutral & Clear", "avatar": "🤖"},
    {"id": "af_jessica", "name": "Jessica", "category": "official", "gender": "Female", "accent": "American", "flag": "🇺🇸", "trait": "Expressive & Dynamic", "avatar": "✨"},
    {"id": "af_river", "name": "River", "category": "official", "gender": "Female", "accent": "American", "flag": "🇺🇸", "trait": "Relaxed & Conversational", "avatar": "🌊"},

    # ====================================================
    # OFFICIAL AMERICAN MALE (9)
    # ====================================================
    {"id": "am_adam", "name": "Adam", "category": "official", "gender": "Male", "accent": "American", "flag": "🇺🇸", "trait": "Deep & Authoritative", "avatar": "👑"},
    {"id": "am_michael", "name": "Michael", "category": "official", "gender": "Male", "accent": "American", "flag": "🇺🇸", "trait": "Friendly & Professional", "recommended": True, "avatar": "🤝"},
    {"id": "am_fenrir", "name": "Fenrir", "category": "official", "gender": "Male", "accent": "American", "flag": "🇺🇸", "trait": "Deep & Cinematic", "avatar": "🐺"},
    {"id": "am_echo", "name": "Echo", "category": "official", "gender": "Male", "accent": "American", "flag": "🇺🇸", "trait": "Warm & Resonant", "avatar": "📻"},
    {"id": "am_eric", "name": "Eric", "category": "official", "gender": "Male", "accent": "American", "flag": "🇺🇸", "trait": "Conversational & Crisp", "avatar": "☕"},
    {"id": "am_liam", "name": "Liam", "category": "official", "gender": "Male", "accent": "American", "flag": "🇺🇸", "trait": "Youthful & Energetic", "avatar": "⚡"},
    {"id": "am_onyx", "name": "Onyx", "category": "official", "gender": "Male", "accent": "American", "flag": "🇺🇸", "trait": "Rich & Deep", "avatar": "💎"},
    {"id": "am_puck", "name": "Puck", "category": "official", "gender": "Male", "accent": "American", "flag": "🇺🇸", "trait": "Lively & Animated", "avatar": "🎭"},
    {"id": "am_santa", "name": "Santa", "category": "official", "gender": "Male", "accent": "American", "flag": "🇺🇸", "trait": "Jolly & Booming Storyteller", "avatar": "🎅"},

    # ====================================================
    # OFFICIAL BRITISH FEMALE & MALE (8)
    # ====================================================
    {"id": "bf_emma", "name": "Emma", "category": "official", "gender": "Female", "accent": "British", "flag": "🇬🇧", "trait": "Classic British RP", "recommended": True, "avatar": "☕"},
    {"id": "bf_isabella", "name": "Isabella", "category": "official", "gender": "Female", "accent": "British", "flag": "🇬🇧", "trait": "Soft & Elegant", "avatar": "🌹"},
    {"id": "bf_alice", "name": "Alice", "category": "official", "gender": "Female", "accent": "British", "flag": "🇬🇧", "trait": "Refined & Articulate", "avatar": "📖"},
    {"id": "bf_lily", "name": "Lily", "category": "official", "gender": "Female", "accent": "British", "flag": "🇬🇧", "trait": "Warm & Expressive", "avatar": "🌷"},
    {"id": "bm_george", "name": "George", "category": "official", "gender": "Male", "accent": "British", "flag": "🇬🇧", "trait": "Refined British Gentleman", "avatar": "🎩"},
    {"id": "bm_fable", "name": "Fable", "category": "official", "gender": "Male", "accent": "British", "flag": "🇬🇧", "trait": "Audiobook Narrator", "recommended": True, "avatar": "📚"},
    {"id": "bm_lewis", "name": "Lewis", "category": "official", "gender": "Male", "accent": "British", "flag": "🇬🇧", "trait": "Intellectual & Calm", "avatar": "🧐"},
    {"id": "bm_daniel", "name": "Daniel", "category": "official", "gender": "Male", "accent": "British", "flag": "🇬🇧", "trait": "Modern British", "avatar": "🏙️"},

    # ====================================================
    # CURATED COMMUNITY VOICE BLENDS (24)
    # ====================================================
    {
        "id": "comm_velvet_noir", "name": "Velvet Noir", "category": "community", "gender": "Female",
        "accent": "American", "flag": "🇺🇸", "trait": "Sultry Late-Night Radio & ASMR", "avatar": "🌙",
        "recommended": True, "community": True, "blend_label": "60% Nicole + 40% Heart",
        "recipe": {"af_nicole": 0.60, "af_heart": 0.40}
    },
    {
        "id": "comm_aurora", "name": "Aurora", "category": "community", "gender": "Female",
        "accent": "American", "flag": "🇺🇸", "trait": "Radiant & Empathetic AI Companion", "avatar": "🌌",
        "recommended": True, "community": True, "blend_label": "55% Heart + 45% Sky",
        "recipe": {"af_heart": 0.55, "af_sky": 0.45}
    },
    {
        "id": "comm_titan_trailer", "name": "Titan Trailer", "category": "community", "gender": "Male",
        "accent": "American", "flag": "🇺🇸", "trait": "Epic Movie Trailer & Promo Voice", "avatar": "🎬",
        "recommended": True, "community": True, "blend_label": "65% Fenrir + 35% Onyx",
        "recipe": {"am_fenrir": 0.65, "am_onyx": 0.35}
    },
    {
        "id": "comm_lord_ashcroft", "name": "Lord Ashcroft", "category": "community", "gender": "Male",
        "accent": "British", "flag": "🇬🇧", "trait": "Master Fantasy & History Narrator", "avatar": "🏰",
        "recommended": True, "community": True, "blend_label": "55% George + 45% Fable",
        "recipe": {"bm_george": 0.55, "bm_fable": 0.45}
    },
    {
        "id": "comm_celeste", "name": "Celeste", "category": "community", "gender": "Female",
        "accent": "Transatlantic", "flag": "🌊", "trait": "Mid-Atlantic Prestige Documentary", "avatar": "🥂",
        "recommended": True, "community": True, "blend_label": "50% Emma + 50% Heart",
        "recipe": {"bf_emma": 0.50, "af_heart": 0.50}
    },
    {
        "id": "comm_sterling", "name": "Sterling", "category": "community", "gender": "Male",
        "accent": "Transatlantic", "flag": "🌍", "trait": "Global Broadcast & News Anchor", "avatar": "🎙️",
        "community": True, "blend_label": "50% Adam + 50% Lewis",
        "recipe": {"am_adam": 0.50, "bm_lewis": 0.50}
    },
    {
        "id": "comm_fireside", "name": "Fireside", "category": "community", "gender": "Male",
        "accent": "British", "flag": "🇬🇧", "trait": "Cozy Audiobook & Bedtime Storyteller", "avatar": "🔥",
        "community": True, "blend_label": "60% Fable + 40% Echo",
        "recipe": {"bm_fable": 0.60, "am_echo": 0.40}
    },
    {
        "id": "comm_nexus_ai", "name": "Nexus OS", "category": "community", "gender": "Female",
        "accent": "American", "flag": "🇺🇸", "trait": "Futuristic Starship & Sci-Fi AI", "avatar": "🛸",
        "community": True, "blend_label": "55% Alloy + 45% Kore",
        "recipe": {"af_alloy": 0.55, "af_kore": 0.45}
    },
    {
        "id": "comm_maverick", "name": "Maverick", "category": "community", "gender": "Male",
        "accent": "American", "flag": "🇺🇸", "trait": "Dynamic Tech & Startup Podcaster", "avatar": "🎧",
        "community": True, "blend_label": "55% Michael + 45% Puck",
        "recipe": {"am_michael": 0.55, "am_puck": 0.45}
    },
    {
        "id": "comm_seraphina", "name": "Seraphina", "category": "community", "gender": "Female",
        "accent": "Transatlantic", "flag": "✨", "trait": "Poetic, Ethereal & Dreamy Muse", "avatar": "🦋",
        "community": True, "blend_label": "50% Aoede + 50% Isabella",
        "recipe": {"af_aoede": 0.50, "bf_isabella": 0.50}
    },
    {
        "id": "comm_callahan", "name": "Callahan", "category": "community", "gender": "Male",
        "accent": "American", "flag": "🇺🇸", "trait": "Gritty Hardboiled Noir Detective", "avatar": "🕵️",
        "community": True, "blend_label": "60% Onyx + 40% Adam",
        "recipe": {"am_onyx": 0.60, "am_adam": 0.40}
    },
    {
        "id": "comm_duchess", "name": "Duchess", "category": "community", "gender": "Female",
        "accent": "British", "flag": "🇬🇧", "trait": "Aristocratic Period Drama Lead", "avatar": "💎",
        "community": True, "blend_label": "60% Alice + 40% Isabella",
        "recipe": {"bf_alice": 0.60, "bf_isabella": 0.40}
    },
    {
        "id": "comm_pixie", "name": "Pixie", "category": "community", "gender": "Female",
        "accent": "American", "flag": "🇺🇸", "trait": "High-Energy Creator & Story Vlogger", "avatar": "⚡",
        "community": True, "blend_label": "55% Bella + 45% Jessica",
        "recipe": {"af_bella": 0.55, "af_jessica": 0.45}
    },
    {
        "id": "comm_bodhi", "name": "Bodhi", "category": "community", "gender": "Female",
        "accent": "American", "flag": "🇺🇸", "trait": "Serene Mindfulness & Meditation Guide", "avatar": "🧘",
        "community": True, "blend_label": "60% Kore + 40% River",
        "recipe": {"af_kore": 0.60, "af_river": 0.40}
    },
    {
        "id": "comm_oxford_prof", "name": "Prof. Arthur", "category": "community", "gender": "Male",
        "accent": "British", "flag": "🇬🇧", "trait": "Oxford Scholar & Science Lecturer", "avatar": "📜",
        "community": True, "blend_label": "60% Lewis + 40% George",
        "recipe": {"bm_lewis": 0.60, "bm_george": 0.40}
    },
    {
        "id": "comm_victoria", "name": "Victoria", "category": "community", "gender": "Female",
        "accent": "American", "flag": "🇺🇸", "trait": "Keynote Speaker & Executive Briefer", "avatar": "📈",
        "community": True, "blend_label": "55% Sarah + 45% Nova",
        "recipe": {"af_sarah": 0.55, "af_nova": 0.45}
    },
    {
        "id": "comm_clementine", "name": "Clementine", "category": "community", "gender": "Female",
        "accent": "British", "flag": "🇬🇧", "trait": "Warm Indie RPG Character Voice", "avatar": "🍂",
        "community": True, "blend_label": "55% Lily + 45% Aoede",
        "recipe": {"bf_lily": 0.55, "af_aoede": 0.45}
    },
    {
        "id": "comm_blitz", "name": "Blitz", "category": "community", "gender": "Male",
        "accent": "American", "flag": "🇺🇸", "trait": "Fast-Paced Esports & Hype Caster", "avatar": "🏆",
        "community": True, "blend_label": "60% Liam + 40% Puck",
        "recipe": {"am_liam": 0.60, "am_puck": 0.40}
    },
    {
        "id": "comm_midnight_fm", "name": "Midnight FM", "category": "community", "gender": "Male",
        "accent": "Transatlantic", "flag": "🎷", "trait": "Smooth Jazz & Late-Night Radio DJ", "avatar": "🎷",
        "community": True, "blend_label": "60% Echo + 40% Daniel",
        "recipe": {"am_echo": 0.60, "bm_daniel": 0.40}
    },
    {
        "id": "comm_rosalind", "name": "Rosalind", "category": "community", "gender": "Female",
        "accent": "British", "flag": "🇬🇧", "trait": "Whimsical Children's Storybook", "avatar": "🧚",
        "community": True, "blend_label": "55% Lily + 45% Emma",
        "recipe": {"bf_lily": 0.55, "bf_emma": 0.45}
    },
    {
        "id": "comm_vanguard", "name": "Vanguard", "category": "community", "gender": "Male",
        "accent": "American", "flag": "🇺🇸", "trait": "Tactical Commander & Action Lead", "avatar": "🛡️",
        "community": True, "blend_label": "55% Eric + 45% Fenrir",
        "recipe": {"am_eric": 0.55, "am_fenrir": 0.45}
    },
    {
        "id": "comm_obsidian", "name": "Obsidian", "category": "community", "gender": "Male",
        "accent": "Transatlantic", "flag": "⌚", "trait": "Velvet Baritone Luxury Commercial", "avatar": "🖤",
        "community": True, "blend_label": "50% Onyx + 50% George",
        "recipe": {"am_onyx": 0.50, "bm_george": 0.50}
    },
    {
        "id": "comm_lyra", "name": "Lyra", "category": "community", "gender": "Female",
        "accent": "American", "flag": "🇺🇸", "trait": "Sweet Acoustic & Gentle Storyteller", "avatar": "🎶",
        "community": True, "blend_label": "50% Bella + 50% Kore",
        "recipe": {"af_bella": 0.50, "af_kore": 0.50}
    },
    {
        "id": "comm_archivist", "name": "The Archivist", "category": "community", "gender": "Male",
        "accent": "British", "flag": "🇬🇧", "trait": "Ancient Lorekeeper & Wise Mentor", "avatar": "🧙",
        "community": True, "blend_label": "55% Fable + 45% Santa",
        "recipe": {"bm_fable": 0.55, "am_santa": 0.45}
    },

    # ====================================================
    # INTERNATIONAL / GLOBAL TIMBRE VOICES (13)
    # ====================================================
    {"id": "ff_siwis", "name": "Siwis", "category": "international", "gender": "Female", "accent": "French", "flag": "🇫🇷", "trait": "Parisian Chic & Soft Cadence", "avatar": "🥐"},
    {"id": "if_sara", "name": "Sara", "category": "international", "gender": "Female", "accent": "Italian", "flag": "🇮🇹", "trait": "Melodic Milanese Expressive", "avatar": "🎭"},
    {"id": "im_nicola", "name": "Nicola", "category": "international", "gender": "Male", "accent": "Italian", "flag": "🇮🇹", "trait": "Warm Roman Baritone", "avatar": "🍷"},
    {"id": "ef_dora", "name": "Dora", "category": "international", "gender": "Female", "accent": "Spanish", "flag": "🇪🇸", "trait": "Warm Iberian Storyteller", "avatar": "💃"},
    {"id": "em_alex", "name": "Alex", "category": "international", "gender": "Male", "accent": "Spanish", "flag": "🇪🇸", "trait": "Clear Madrid Narrator", "avatar": "🎸"},
    {"id": "pf_dora", "name": "Clara", "category": "international", "gender": "Female", "accent": "Portuguese", "flag": "🇧🇷", "trait": "Smooth Bossa Nova Warmth", "avatar": "🌴"},
    {"id": "pm_alex", "name": "Mateus", "category": "international", "gender": "Male", "accent": "Portuguese", "flag": "🇧🇷", "trait": "Friendly São Paulo Studio", "avatar": "⚽"},
    {"id": "jf_alpha", "name": "Sakura", "category": "international", "gender": "Female", "accent": "Japanese", "flag": "🇯🇵", "trait": "Crisp Tokyo Anime & Narrator", "avatar": "🌸"},
    {"id": "jm_kumo", "name": "Kumo", "category": "international", "gender": "Male", "accent": "Japanese", "flag": "🇯🇵", "trait": "Calm Kyoto Storyteller", "avatar": "⛩️"},
    {"id": "zf_xiaoxiao", "name": "Xiaoxiao", "category": "international", "gender": "Female", "accent": "Mandarin", "flag": "🇨🇳", "trait": "Sweet & Articulate Studio", "avatar": "🏮"},
    {"id": "zm_yunyang", "name": "Yunyang", "category": "international", "gender": "Male", "accent": "Mandarin", "flag": "🇨🇳", "trait": "Broadcast Anchor Timbre", "avatar": "🐉"},
    {"id": "hf_alpha", "name": "Ananya", "category": "international", "gender": "Female", "accent": "Hindi", "flag": "🇮🇳", "trait": "Warm & Clear Expressive", "avatar": "🪷"},
    {"id": "hm_omega", "name": "Rohan", "category": "international", "gender": "Male", "accent": "Hindi", "flag": "🇮🇳", "trait": "Deep & Articulate Studio", "avatar": "🕌"}
]

_kokoro_pipelines: Dict[str, Any] = {}
_kokoro_lock = threading.Lock()


def load_custom_voices() -> List[Dict[str, Any]]:
    if not CUSTOM_VOICES_FILE.exists():
        return []
    try:
        with open(CUSTOM_VOICES_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except Exception as e:
        print(f"Warning: could not load custom_voices.json: {e}")
        return []


def save_custom_voices(voices: List[Dict[str, Any]]) -> None:
    try:
        with open(CUSTOM_VOICES_FILE, "w", encoding="utf-8") as f:
            json.dump(voices, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"Warning: could not save custom_voices.json: {e}")


def get_all_kokoro_voices() -> List[Dict[str, Any]]:
    custom = load_custom_voices()
    return custom + KOKORO_PRESET_VOICES


def get_whisper_model(model_name: str):
    global _current_loaded_whisper
    if model_name not in AVAILABLE_MODELS:
        raise HTTPException(status_code=400, detail=f"Invalid model name '{model_name}'. Choose from: {list(AVAILABLE_MODELS.keys())}")
    
    with _whisper_lock:
        if model_name not in _whisper_models:
            print(f"Loading Whisper model '{model_name}' on {DEVICE}...")
            model = whisper.load_model(model_name, device=DEVICE)
            _whisper_models[model_name] = model
            _current_loaded_whisper = model_name
            print(f"Model '{model_name}' loaded successfully.")
        else:
            _current_loaded_whisper = model_name
        return _whisper_models[model_name]


def get_kokoro_pipeline(lang_code: str):
    with _kokoro_lock:
        if lang_code not in _kokoro_pipelines:
            print(f"Initializing Kokoro KPipeline for lang_code='{lang_code}' on {DEVICE}...")
            _kokoro_pipelines[lang_code] = KPipeline(lang_code=lang_code, device=DEVICE)
            print(f"Kokoro KPipeline '{lang_code}' ready.")
        return _kokoro_pipelines[lang_code]


def resolve_voice_tensor_and_lang(voice_id: str, custom_recipe: Optional[Dict[str, float]] = None):
    """
    Resolve a voice ID (official, community blend, custom blend, or comma-separated recipe)
    into (lang_code, voice_or_tensor, voice_meta).
    """
    all_voices = get_all_kokoro_voices()
    voice_meta = next((v for v in all_voices if v["id"] == voice_id), None)

    recipe = custom_recipe or (voice_meta.get("recipe") if voice_meta else None)

    # Support inline 'af_heart:60,af_bella:40' syntax if passed directly
    if not recipe and ("," in voice_id or ":" in voice_id):
        parsed_recipe: Dict[str, float] = {}
        for part in voice_id.split(","):
            part = part.strip()
            if not part:
                continue
            if ":" in part:
                k, w = part.split(":", 1)
                try:
                    parsed_recipe[k.strip()] = float(w.strip())
                except ValueError:
                    parsed_recipe[k.strip()] = 1.0
            else:
                parsed_recipe[part] = 1.0
        if parsed_recipe:
            recipe = parsed_recipe

    if recipe:
        # Determine primary language pipeline ('b' if top component is British, else 'a')
        top_voice = max(recipe.items(), key=lambda kv: kv[1])[0]
        lang_code = "b" if top_voice.startswith("b") else "a"
        pipeline = get_kokoro_pipeline(lang_code)

        blended_tensor = None
        total_w = sum(float(w) for w in recipe.values()) or 1.0
        for comp_id, weight in recipe.items():
            single_pack = pipeline.load_single_voice(comp_id)
            w = float(weight) / total_w
            blended_tensor = (single_pack * w) if blended_tensor is None else (blended_tensor + single_pack * w)

        return lang_code, blended_tensor, voice_meta

    # Single voice fallback
    if not voice_meta:
        voice_id = "af_heart"
        voice_meta = next((v for v in all_voices if v["id"] == "af_heart"), None)

    lang_code = "b" if voice_id.startswith("b") else "a"
    return lang_code, voice_id, voice_meta


def format_timestamp_srt(seconds: float) -> str:
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int(round((seconds - int(seconds)) * 1000))
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"


def format_timestamp_vtt(seconds: float) -> str:
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int(round((seconds - int(seconds)) * 1000))
    return f"{hours:02d}:{minutes:02d}:{secs:02d}.{millis:03d}"


def generate_srt(segments: List[Dict[str, Any]]) -> str:
    lines = []
    for idx, seg in enumerate(segments, start=1):
        start = format_timestamp_srt(seg["start"])
        end = format_timestamp_srt(seg["end"])
        text = seg["text"].strip()
        lines.append(f"{idx}\n{start} --> {end}\n{text}\n")
    return "\n".join(lines)


def generate_vtt(segments: List[Dict[str, Any]]) -> str:
    lines = ["WEBVTT\n"]
    for idx, seg in enumerate(segments, start=1):
        start = format_timestamp_vtt(seg["start"])
        end = format_timestamp_vtt(seg["end"])
        text = seg["text"].strip()
        lines.append(f"{idx}\n{start} --> {end}\n{text}\n")
    return "\n".join(lines)


# Pydantic models for TTS requests
class SynthesizeRequest(BaseModel):
    text: str
    voice: str = "af_heart"
    speed: float = 1.0
    recipe: Optional[Dict[str, float]] = None


class CreateCustomVoiceRequest(BaseModel):
    name: str
    voice_a: str
    voice_b: str
    weight_a: int = 50
    trait: Optional[str] = None
    avatar: Optional[str] = "🧪"


@app.get("/api/info")
async def get_system_info():
    """Return hardware specs, supported Whisper models, and active cache"""
    all_v = get_all_kokoro_voices()
    return {
        "app_name": "Voice AI",
        "device": DEVICE,
        "device_name": DEVICE_NAME,
        "whisper_models": AVAILABLE_MODELS,
        "active_whisper": _current_loaded_whisper,
        "kokoro_voices_count": len(all_v)
    }


@app.get("/api/languages")
async def get_supported_languages():
    """Return dictionary of supported Whisper languages"""
    langs = []
    for code, name in whisper.tokenizer.LANGUAGES.items():
        langs.append({"code": code, "name": name.title()})
    langs.sort(key=lambda x: x["name"])
    return langs


@app.post("/api/transcribe")
async def transcribe_audio(
    file: UploadFile = File(...),
    model_name: str = Form("base"),
    language: Optional[str] = Form(None),
    task: str = Form("transcribe"),
    word_timestamps: bool = Form(False),
    temperature: float = Form(0.0),
    initial_prompt: Optional[str] = Form(None)
):
    """
    Transcribe or translate an uploaded audio file using Whisper.
    """
    if task not in ["transcribe", "translate"]:
        raise HTTPException(status_code=400, detail="Task must be 'transcribe' or 'translate'")
    
    lang = language.strip().lower() if language and language.strip() and language.strip().lower() != "auto" else None
    prompt = initial_prompt.strip() if initial_prompt and initial_prompt.strip() else None

    suffix = Path(file.filename or "audio.wav").suffix or ".wav"
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    temp_path = temp_file.name

    try:
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        temp_file.close()

        start_time = time.perf_counter()
        model = get_whisper_model(model_name)

        transcribe_args: Dict[str, Any] = {
            "fp16": (DEVICE == "cuda"),
            "task": task,
            "temperature": temperature,
        }

        if lang:
            transcribe_args["language"] = lang
        if prompt:
            transcribe_args["initial_prompt"] = prompt
        if word_timestamps:
            transcribe_args["word_timestamps"] = True

        result = model.transcribe(temp_path, **transcribe_args)
        elapsed_time = round(time.perf_counter() - start_time, 2)

        segments = []
        raw_segments = result.get("segments", [])
        total_duration = 0.0

        for s in raw_segments:
            seg_start = round(float(s.get("start", 0.0)), 2)
            seg_end = round(float(s.get("end", 0.0)), 2)
            if seg_end > total_duration:
                total_duration = seg_end

            seg_data = {
                "id": s.get("id", len(segments)),
                "start": seg_start,
                "end": seg_end,
                "text": s.get("text", "").strip()
            }

            if word_timestamps and "words" in s:
                seg_data["words"] = [
                    {
                        "word": w.get("word", "").strip(),
                        "start": round(float(w.get("start", 0.0)), 2),
                        "end": round(float(w.get("end", 0.0)), 2),
                        "probability": round(float(w.get("probability", 1.0)), 3)
                    }
                    for w in s.get("words", [])
                ]
            segments.append(seg_data)

        detected_lang = result.get("language", lang or "unknown")
        detected_lang_name = whisper.tokenizer.LANGUAGES.get(detected_lang, detected_lang).title()
        speed_factor = round(total_duration / max(elapsed_time, 0.001), 1) if total_duration > 0 else 1.0

        srt_content = generate_srt(segments)
        vtt_content = generate_vtt(segments)

        all_words = []
        for s in segments:
            if "words" in s and s["words"]:
                all_words.extend(s["words"])

        return {
            "success": True,
            "text": result.get("text", "").strip(),
            "segments": segments,
            "words": all_words,
            "has_word_timestamps": bool(all_words),
            "language": detected_lang,
            "language_name": detected_lang_name,
            "task": task,
            "duration": round(total_duration, 2),
            "processing_time": elapsed_time,
            "speed_factor": speed_factor,
            "model_used": model_name,
            "srt": srt_content,
            "vtt": vtt_content,
            "filename": file.filename or "recording.wav"
        }

    except Exception as e:
        print(f"Error during transcription: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except Exception:
                pass


# ----------------------------------------------------
# Kokoro TTS Endpoints
# ----------------------------------------------------
@app.get("/api/tts/voices")
async def get_kokoro_voices():
    """Return all preset, community blend, international, and user-created voices for Kokoro TTS"""
    return get_all_kokoro_voices()


@app.post("/api/tts/voices/custom")
async def create_custom_community_voice(req: CreateCustomVoiceRequest):
    """Create and persist a user-crafted community voice blend"""
    name = req.name.strip()
    if not name:
        raise HTTPException(status_code=400, detail="Voice name is required.")

    base_map = {v["id"]: v for v in KOKORO_PRESET_VOICES if v.get("category") in ("official", "international")}
    if req.voice_a not in base_map or req.voice_b not in base_map:
        raise HTTPException(status_code=400, detail="Please select valid base Kokoro voices to blend.")

    if req.voice_a == req.voice_b:
        raise HTTPException(status_code=400, detail="Please choose two different base voices to blend.")

    w_a = max(10, min(90, int(req.weight_a)))
    w_b = 100 - w_a

    va = base_map[req.voice_a]
    vb = base_map[req.voice_b]

    gender = va["gender"] if va["gender"] == vb["gender"] else "Hybrid"
    accent = va["accent"] if va["accent"] == vb["accent"] else f"{va['accent']} · {vb['accent']}"
    flag = va["flag"] if va["flag"] == vb["flag"] else f"{va['flag']}{vb['flag']}"
    blend_label = f"{w_a}% {va['name']} + {w_b}% {vb['name']}"
    trait = (req.trait or "").strip() or f"Custom Blend ({blend_label})"
    avatar = (req.avatar or "🧪").strip()[:4] or "🧪"

    new_voice = {
        "id": f"custom_{uuid.uuid4().hex[:8]}",
        "name": name,
        "category": "community",
        "gender": gender,
        "accent": accent,
        "flag": flag,
        "trait": trait,
        "avatar": avatar,
        "community": True,
        "custom": True,
        "blend_label": blend_label,
        "recipe": {
            req.voice_a: round(w_a / 100.0, 2),
            req.voice_b: round(w_b / 100.0, 2)
        }
    }

    custom_list = load_custom_voices()
    custom_list.insert(0, new_voice)
    save_custom_voices(custom_list)
    return {"success": True, "voice": new_voice, "voices": get_all_kokoro_voices()}


@app.delete("/api/tts/voices/custom/{voice_id}")
async def delete_custom_community_voice(voice_id: str):
    """Delete a user-created custom community voice"""
    custom_list = load_custom_voices()
    updated = [v for v in custom_list if v.get("id") != voice_id]
    if len(updated) == len(custom_list):
        raise HTTPException(status_code=404, detail="Custom voice not found.")
    save_custom_voices(updated)
    return {"success": True, "voices": get_all_kokoro_voices()}


@app.post("/api/tts/synthesize")
async def synthesize_speech(req: SynthesizeRequest):
    """
    Synthesize text into natural speech using Kokoro-82M.
    Supports official voices, curated community blends, international voices, and custom recipes.
    """
    clean_text = req.text.strip()
    if not clean_text:
        raise HTTPException(status_code=400, detail="Text cannot be empty.")

    voice = req.voice.strip()
    speed = max(0.5, min(req.speed, 2.0))

    try:
        start_time = time.perf_counter()
        lang_code, voice_or_tensor, voice_meta = resolve_voice_tensor_and_lang(voice, req.recipe)
        pipeline = get_kokoro_pipeline(lang_code)

        # Generate audio segments
        generator = pipeline(clean_text, voice=voice_or_tensor, speed=speed, split_pattern=r'\n+')
        audio_pieces = []

        for _, _, audio in generator:
            if hasattr(audio, "numpy"):
                audio_pieces.append(audio.numpy())
            elif isinstance(audio, np.ndarray):
                audio_pieces.append(audio)
            else:
                audio_pieces.append(np.array(audio))

        if not audio_pieces:
            raise HTTPException(status_code=500, detail="Kokoro did not generate any audio.")

        combined_audio = np.concatenate(audio_pieces)
        duration = round(len(combined_audio) / 24000.0, 2)
        elapsed_time = round(time.perf_counter() - start_time, 2)

        # Save audio file to generated_audio directory
        audio_id = f"kokoro_{uuid.uuid4().hex[:12]}"
        audio_filename = f"{audio_id}.wav"
        output_path = AUDIO_OUT_DIR / audio_filename
        sf.write(str(output_path), combined_audio, 24000)

        return {
            "success": True,
            "audio_url": f"/api/tts/audio/{audio_filename}",
            "filename": audio_filename,
            "duration": duration,
            "processing_time": elapsed_time,
            "speed_ratio": round(duration / max(elapsed_time, 0.001), 1) if duration > 0 else 1.0,
            "voice": voice,
            "voice_info": voice_meta,
            "text": clean_text,
            "characters": len(clean_text)
        }

    except Exception as e:
        print(f"Error during Kokoro TTS synthesis: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/tts/audio/{filename}")
async def get_generated_audio(filename: str):
    """Serve synthesized audio WAV file"""
    file_path = AUDIO_OUT_DIR / filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Audio file not found")
    return FileResponse(file_path, media_type="audio/wav")


# ----------------------------------------------------
# Audio Compressor & DSP Endpoints
# ----------------------------------------------------
import subprocess

def probe_audio_file(file_path: Path) -> Dict[str, Any]:
    """Inspect audio file properties using ffprobe"""
    cmd = [
        "ffprobe",
        "-v", "quiet",
        "-print_format", "json",
        "-show_format",
        "-show_streams",
        str(file_path)
    ]
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, check=True)
        data = json.loads(proc.stdout)
        fmt = data.get("format", {})
        streams = data.get("streams", [])
        audio_stream = next((s for s in streams if s.get("codec_type") == "audio"), {})

        duration = float(fmt.get("duration", audio_stream.get("duration", 0.0) or 0.0))
        bitrate = int(fmt.get("bit_rate", audio_stream.get("bit_rate", 0) or 0))
        sample_rate = int(audio_stream.get("sample_rate", 0) or 0)
        channels = int(audio_stream.get("channels", 0) or 0)
        codec_name = audio_stream.get("codec_name", "")

        return {
            "duration": round(duration, 2),
            "bitrate": bitrate,
            "sample_rate": sample_rate,
            "channels": channels,
            "codec_name": codec_name
        }
    except Exception as e:
        print(f"Warning during ffprobe probe: {e}")
        return {
            "duration": 0.0,
            "bitrate": 0,
            "sample_rate": 0,
            "channels": 0,
            "codec_name": ""
        }


@app.post("/api/compress")
async def compress_audio_endpoint(
    file: UploadFile = File(...),
    target_format: str = Form("mp3"),
    bitrate: str = Form("64k"),
    sample_rate: str = Form("auto"),
    channels: str = Form("auto"),
    enable_dsp: bool = Form(False),
    threshold: float = Form(-20.0),
    ratio: float = Form(4.0),
    attack: float = Form(20.0),
    release: float = Form(250.0),
    makeup_gain: float = Form(2.0),
    normalize: bool = Form(True),
    target_lufs: float = Form(-16.0)
):
    """
    Compress file size and optionally apply dynamic range compression / loudness normalization.
    """
    suffix = Path(file.filename or "audio.wav").suffix or ".wav"
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    temp_in_path = temp_file.name

    try:
        with open(temp_in_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        temp_file.close()

        start_time = time.perf_counter()
        orig_size = os.path.getsize(temp_in_path)
        orig_meta = probe_audio_file(Path(temp_in_path))

        # Output extension & destination
        clean_fmt = target_format.lower().strip()
        if clean_fmt not in ("mp3", "m4a", "aac", "ogg", "opus", "wav", "flac"):
            clean_fmt = "mp3"

        out_ext = ".m4a" if clean_fmt in ("m4a", "aac") else f".{clean_fmt}"
        out_id = f"compressed_{uuid.uuid4().hex[:12]}"
        out_filename = f"{out_id}{out_ext}"
        out_path = COMPRESSED_AUDIO_DIR / out_filename

        # Construct FFmpeg command
        cmd = ["ffmpeg", "-y", "-i", temp_in_path]

        # Audio filters pipeline
        filters = []
        if enable_dsp:
            filters.append(
                f"acompressor=threshold={threshold}dB:ratio={ratio}:attack={attack}:release={release}:makeup={makeup_gain}"
            )
        if normalize:
            # EBU R128 integrated loudness normalization
            filters.append(f"loudnorm=I={target_lufs}:TP=-1.5:LRA=11")

        if filters:
            cmd.extend(["-af", ",".join(filters)])

        # Codec & Bitrate mapping
        if clean_fmt == "mp3":
            cmd.extend(["-c:a", "libmp3lame"])
            if bitrate and bitrate != "auto":
                br = bitrate if bitrate.endswith("k") else f"{bitrate}k"
                cmd.extend(["-b:a", br])
        elif clean_fmt in ("m4a", "aac"):
            cmd.extend(["-c:a", "aac"])
            if bitrate and bitrate != "auto":
                br = bitrate if bitrate.endswith("k") else f"{bitrate}k"
                cmd.extend(["-b:a", br])
        elif clean_fmt in ("ogg", "opus"):
            cmd.extend(["-c:a", "libopus"])
            if bitrate and bitrate != "auto":
                br = bitrate if bitrate.endswith("k") else f"{bitrate}k"
                cmd.extend(["-b:a", br])
        elif clean_fmt == "flac":
            cmd.extend(["-c:a", "flac"])
        elif clean_fmt == "wav":
            cmd.extend(["-c:a", "pcm_s16le"])
        else:
            cmd.extend(["-c:a", "libmp3lame", "-b:a", "64k"])

        # Channels downmix
        if str(channels) in ("1", "mono"):
            cmd.extend(["-ac", "1"])
        elif str(channels) in ("2", "stereo"):
            cmd.extend(["-ac", "2"])

        # Sample rate
        if sample_rate and sample_rate != "auto":
            cmd.extend(["-ar", str(sample_rate)])

        # Fast execution flags & destination
        cmd.extend(["-vn", str(out_path)])

        proc = subprocess.run(cmd, capture_output=True, text=True)
        if proc.returncode != 0:
            print(f"FFmpeg error: {proc.stderr}")
            raise HTTPException(status_code=500, detail=f"Audio compression failed: {proc.stderr[:400]}")

        elapsed_time = round(time.perf_counter() - start_time, 2)
        comp_size = os.path.getsize(out_path)
        comp_meta = probe_audio_file(out_path)

        saved_bytes = max(0, orig_size - comp_size)
        saved_percent = round((saved_bytes / max(orig_size, 1)) * 100, 1) if orig_size > 0 else 0.0

        return {
            "success": True,
            "filename": out_filename,
            "original_filename": file.filename or "audio.wav",
            "audio_url": f"/api/compress/audio/{out_filename}",
            "original_size": orig_size,
            "compressed_size": comp_size,
            "saved_bytes": saved_bytes,
            "saved_percent": saved_percent,
            "duration": comp_meta.get("duration") or orig_meta.get("duration", 0.0),
            "original_meta": orig_meta,
            "compressed_meta": comp_meta,
            "format": clean_fmt,
            "bitrate": bitrate,
            "channels": comp_meta.get("channels", 2),
            "sample_rate": comp_meta.get("sample_rate", 44100),
            "processing_time": elapsed_time,
            "dsp_applied": enable_dsp or normalize
        }

    except Exception as e:
        print(f"Error during audio compression: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if os.path.exists(temp_in_path):
            try:
                os.remove(temp_in_path)
            except Exception:
                pass


@app.get("/api/compress/audio/{filename}")
async def get_compressed_audio(filename: str):
    """Serve compressed audio file"""
    file_path = COMPRESSED_AUDIO_DIR / filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Audio file not found")
    ext = file_path.suffix.lstrip(".").lower()
    media_type = MIME_TYPES.get(ext, "audio/mpeg")
    return FileResponse(file_path, media_type=media_type)


# Serve static assets
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

@app.get("/")
async def root():
    index_file = STATIC_DIR / "index.html"
    if index_file.exists():
        return FileResponse(index_file)
    return {"message": "Voice AI API is running."}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
