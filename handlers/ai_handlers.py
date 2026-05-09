import google.generativeai as genai

from telegram import Update

from telegram.ext import ContextTypes

from config import GEMINI_API_KEY

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
# AI CHAT
# =========================================================


async def ai_chat(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    text = update.message.text

    if not text:
        return

    try:

        response = model.generate_content(
            text
        )

        await update.message.reply_text(
            response.text[:4000]
        )

    except Exception:

        await update.message.reply_text(
            "⚠️ AI error occurred."
        )

# =========================================================
# AI SUMMARY
# =========================================================


async def summarize_text(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    text = " ".join(context.args)

    if not text:

        return await update.message.reply_text(
            "❌ Usage:\n"
            "/summary [text]"
        )

    prompt = (
        "Summarize this text:\n\n"
        f"{text}"
    )

    try:

        response = model.generate_content(
            prompt
        )

        await update.message.reply_text(
            response.text[:4000]
        )

    except Exception:

        await update.message.reply_text(
            "⚠️ Summary failed."
        )
