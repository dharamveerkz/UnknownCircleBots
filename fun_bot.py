import logging
import random
import requests

from telegram import Update

from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)

from telegram.request import HTTPXRequest

from config import (
    FUN_TOKEN,
    MEME_SUBREDDITS,
)

# =========================================================
# LOGGING
# =========================================================

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

# =========================================================
# DATA
# =========================================================

quotes = [
    "✨ Stay consistent.",
    "🚀 Small steps every day.",
    "🔥 Discipline beats motivation.",
    "💡 Learn. Build. Improve.",
]

fortunes = [
    "🍀 Good luck is coming.",
    "⚡ Opportunity is near.",
    "🌟 You will achieve something big.",
    "🎯 Focus will bring success.",
]

# =========================================================
# COMMANDS
# =========================================================


async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    text = (
        "🎲 Fun Bot Activated!\n\n"
        "Commands:\n"
        "/joke\n"
        "/meme\n"
        "/8ball\n"
        "/dice\n"
        "/quote\n"
        "/fortune"
    )

    await update.message.reply_text(text)

# =========================================================
# JOKE
# =========================================================


async def joke(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    jokes = [
        (
            "Why do programmers prefer dark mode?\n"
            "Because light attracts bugs. 🐛"
        ),
        (
            "There are 10 types of people:\n"
            "Those who understand binary "
            "and those who don't."
        ),
        (
            "Why was the developer broke?\n"
            "Because he used up all his cache."
        ),
    ]

    await update.message.reply_text(
        f"😄 {random.choice(jokes)}"
    )

# =========================================================
# MEME
# =========================================================


async def meme(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    subreddit = random.choice(
        MEME_SUBREDDITS
    )

    try:

        url = (
            f"https://www.reddit.com/r/"
            f"{subreddit}/hot.json?limit=50"
        )

        headers = {
            "User-Agent": "UnknownCircleBot/1.0"
        }

        response = requests.get(
            url,
            headers=headers,
            timeout=10,
        )

        data = response.json()

        posts = data["data"]["children"]

        images = [
            post["data"]["url"]
            for post in posts
            if post["data"].get(
                "post_hint"
            ) == "image"
        ]

        if not images:

            return await update.message.reply_text(
                "😅 No memes found."
            )

        await update.message.reply_photo(
            random.choice(images)
        )

    except Exception as e:

        logger.error(e)

        await update.message.reply_text(
            "⚠️ Failed to fetch meme."
        )

# =========================================================
# 8BALL
# =========================================================


async def eight_ball(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    responses = [
        "✅ Yes",
        "❌ No",
        "🤔 Maybe",
        "⏳ Ask again later",
        "✨ Definitely",
        "😅 Unlikely",
    ]

    await update.message.reply_text(
        f"🎱 {random.choice(responses)}"
    )

# =========================================================
# DICE
# =========================================================


async def dice(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    value = random.randint(1, 6)

    await update.message.reply_text(
        f"🎲 You rolled: {value}"
    )

# =========================================================
# QUOTE
# =========================================================


async def quote(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    await update.message.reply_text(
        random.choice(quotes)
    )

# =========================================================
# FORTUNE
# =========================================================


async def fortune(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    await update.message.reply_text(
        random.choice(fortunes)
    )

# =========================================================
# CREATE APP
# =========================================================


def create_app():

    request = HTTPXRequest(
        connect_timeout=30,
        read_timeout=30,
        write_timeout=30,
        pool_timeout=30,
    )

    app = (
        Application.builder()
        .token(FUN_TOKEN)
        .request(request)
        .build()
    )

    app.add_handler(
        CommandHandler("start", start)
    )

    app.add_handler(
        CommandHandler("joke", joke)
    )

    app.add_handler(
        CommandHandler("meme", meme)
    )

    app.add_handler(
        CommandHandler("8ball", eight_ball)
    )

    app.add_handler(
        CommandHandler("dice", dice)
    )

    app.add_handler(
        CommandHandler("quote", quote)
    )

    app.add_handler(
        CommandHandler("fortune", fortune)
    )

    return app
