# `config.py`

from dotenv import load_dotenv
from typing import Optional
import os

# Load .env variables
load_dotenv()


def _require_env(var: str) -> str:
    value = os.getenv(var)

    if not value or value.startswith("YOUR_"):
        raise ValueError(
            f"⚠️ Missing required env variable: {var}"
        )

    return value.strip()


# =========================================================
# BOT TOKENS
# =========================================================

MOD_TOKEN: str = _require_env("MOD_TOKEN")
GAMES_TOKEN: str = _require_env("GAMES_TOKEN")
AI_TOKEN: str = _require_env("AI_TOKEN")
FUN_TOKEN: str = _require_env("FUN_TOKEN")

# =========================================================
# GEMINI API
# =========================================================

GEMINI_API_KEY: str = _require_env("GEMINI_API_KEY")

# =========================================================
# OPTIONAL SETTINGS
# =========================================================

LOG_CHANNEL_ID: Optional[int] = (
    int(val)
    if (val := os.getenv("LOG_CHANNEL_ID"))
    and val.strip()
    else None
)

GROUP_CHAT_ID: Optional[int] = (
    int(val)
    if (val := os.getenv("GROUP_CHAT_ID"))
    and val.strip()
    else None
)

# =========================================================
# MODERATION SETTINGS
# =========================================================

CAPTCHA_TIMEOUT_SECONDS = 60

MAX_WARNINGS_BEFORE_BAN = 3

MUTE_DURATIONS = {
    "30m": 1800,
    "1h": 3600,
    "1d": 86400,
}

# =========================================================
# GAMES SETTINGS
# =========================================================

TRIVIA_TIMEOUT = 30
GAMES_COOLDOWN = 5

# =========================================================
# AI SETTINGS
# =========================================================

AI_RATE_LIMIT_PER_USER = 60
AI_MAX_RESPONSE_TOKENS = 512

# =========================================================
# FUN SETTINGS
# =========================================================

MEME_SUBREDDITS = [
    "memes",
    "dankmemes",
    "indiamemes",
]

JOKE_CATEGORIES = [
    "programming",
    "misc",
    "pun",
]

# =========================================================
# CONFIG VALIDATION
# =========================================================


def validate_config():

    tokens = [
        MOD_TOKEN,
        GAMES_TOKEN,
        AI_TOKEN,
        FUN_TOKEN,
    ]

    if len(set(tokens)) != len(tokens):
        raise ValueError(
            "❌ Duplicate bot tokens detected."
        )

    print("✅ Config validated successfully.")
