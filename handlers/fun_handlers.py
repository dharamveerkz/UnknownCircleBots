import random

from telegram import Update

from telegram.ext import ContextTypes

# =========================================================
# QUOTES
# =========================================================

QUOTES = [
    "🔥 Never stop learning.",
    "🚀 Keep building.",
    "💡 Creativity changes everything.",
    "⚡ Stay focused.",
]

# =========================================================
# FACTS
# =========================================================

FACTS = [
    "🧠 Honey never spoils.",
    "🌍 Earth is slightly oval.",
    "⚡ Lightning is hotter than the sun.",
]

# =========================================================
# QUOTE COMMAND
# =========================================================


async def random_quote(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    await update.message.reply_text(
        random.choice(QUOTES)
    )

# =========================================================
# FACT COMMAND
# =========================================================


async def random_fact(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    await update.message.reply_text(
        random.choice(FACTS)
    )

# =========================================================
# ROAST COMMAND
# =========================================================


async def roast_user(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    roasts = [
        "😂 Even Google can't understand you.",
        "🤖 Your logic needs an update.",
        "😅 Loading intelligence... failed.",
    ]

    await update.message.reply_text(
        random.choice(roasts)
    )

# =========================================================
# FORTUNE COMMAND
# =========================================================


async def fortune(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    fortunes = [
        "🍀 Luck is on your side.",
        "✨ A new opportunity is coming.",
        "🚀 Success is near.",
    ]

    await update.message.reply_text(
        random.choice(fortunes)
    )
