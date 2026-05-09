import logging
import time

import google.generativeai as genai

from telegram import Update
from telegram.constants import ChatAction

from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)

from telegram.request import HTTPXRequest

from config import (
    AI_TOKEN,
    GEMINI_API_KEY,
    AI_RATE_LIMIT_PER_USER,
)

# =========================================================
# LOGGING
# =========================================================

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

# =========================================================
# GEMINI SETUP
# =========================================================

genai.configure(
    api_key=GEMINI_API_KEY
)

model = genai.GenerativeModel(
    "gemini-1.5-flash"
)

# =========================================================
# RATE LIMIT STORAGE
# =========================================================

user_last_ask = {}

# =========================================================
# COMMANDS
# =========================================================


async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    text = (
        "🤖 AI Bot Ready!\n\n"
        "Commands:\n"
        "/ask [question]\n"
        "/fact\n"
        "/roast\n"
        "/translate"
    )

    await update.message.reply_text(text)

# =========================================================
# ASK AI
# =========================================================


async def ask_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    user_id = update.effective_user.id

    # =====================================================
    # RATE LIMIT
    # =====================================================

    now = time.time()

    if user_id in user_last_ask:

        elapsed = (
            now - user_last_ask[user_id]
        )

        if elapsed < AI_RATE_LIMIT_PER_USER:

            remaining = int(
                AI_RATE_LIMIT_PER_USER - elapsed
            )

            return await update.message.reply_text(
                f"⏳ Wait {remaining}s "
                "before asking again."
            )

    # =====================================================
    # QUESTION
    # =====================================================

    question = " ".join(context.args)

    if not question:

        return await update.message.reply_text(
            "❌ Usage:\n"
            "/ask [question]"
        )

    user_last_ask[user_id] = now

    # =====================================================
    # GENERATE RESPONSE
    # =====================================================

    try:

        await context.bot.send_chat_action(
            chat_id=update.effective_chat.id,
            action=ChatAction.TYPING,
        )

        response = model.generate_content(
            question
        )

        text = response.text[:4000]

        await update.message.reply_text(
            f"💬 {text}"
        )

    except Exception as e:

        logger.error(
            f"Gemini Error: {e}"
        )

        await update.message.reply_text(
            "⚠️ AI service unavailable."
        )

# =========================================================
# FACT
# =========================================================


async def fact(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    facts = [
        "🧠 Honey never spoils.",
        "🌍 Earth rotates at 1670 km/h.",
        "⚡ Python was released in 1991.",
        "🚀 Space is completely silent.",
    ]

    import random

    await update.message.reply_text(
        random.choice(facts)
    )

# =========================================================
# ROAST
# =========================================================


async def roast(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    roasts = [
        "😂 You're proof that AI still needs humans.",
        "😅 Even WiFi disconnects less than your focus.",
        "🤖 Error 404: Common sense not found.",
    ]

    import random

    await update.message.reply_text(
        random.choice(roasts)
    )

# =========================================================
# TRANSLATE
# =========================================================


async def translate(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    if len(context.args) < 2:

        return await update.message.reply_text(
            "❌ Usage:\n"
            "/translate [language] [text]"
        )

    lang = context.args[0]

    text = " ".join(context.args[1:])

    prompt = (
        f"Translate this into {lang}:\n\n{text}"
    )

    try:

        response = model.generate_content(
            prompt
        )

        await update.message.reply_text(
            response.text[:4000]
        )

    except Exception as e:

        logger.error(e)

        await update.message.reply_text(
            "⚠️ Translation failed."
        )

# =========================================================
# CREATE APP
# =========================================================


def create_app():

    request = HTTPXRequest(
        connect_timeout=30,
        read_timeout=60,
        write_timeout=60,
        pool_timeout=30,
    )

    app = (
        Application.builder()
        .token(AI_TOKEN)
        .request(request)
        .build()
    )

    app.add_handler(
        CommandHandler("start", start)
    )

    app.add_handler(
        CommandHandler("ask", ask_handler)
    )

    app.add_handler(
        CommandHandler("fact", fact)
    )

    app.add_handler(
        CommandHandler("roast", roast)
    )

    app.add_handler(
        CommandHandler("translate", translate)
    )

    return app
