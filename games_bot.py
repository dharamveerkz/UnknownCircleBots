import logging
import random

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

from telegram.request import HTTPXRequest

from config import GAMES_TOKEN

# =========================================================
# LOGGING
# =========================================================

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

# =========================================================
# STORAGE
# =========================================================

guess_number_games = {}

# =========================================================
# COMMANDS
# =========================================================


async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    keyboard = [
        [
            InlineKeyboardButton(
                "🎯 Guess Number",
                callback_data="guess"
            )
        ],
        [
            InlineKeyboardButton(
                "🪨📄✂️ Rock Paper Scissors",
                callback_data="rps"
            )
        ],
        [
            InlineKeyboardButton(
                "🏆 Leaderboard",
                callback_data="leaderboard"
            )
        ],
    ]

    await update.message.reply_text(
        "🎮 Choose a game:",
        reply_markup=InlineKeyboardMarkup(
            keyboard
        )
    )

# =========================================================
# CALLBACKS
# =========================================================


async def game_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()

    data = query.data

    # =====================================================
    # GUESS NUMBER
    # =====================================================

    if data == "guess":

        number = random.randint(1, 10)

        guess_number_games[
            query.from_user.id
        ] = number

        await query.edit_message_text(
            "🎯 Guess a number between 1-10\n\n"
            "Use:\n"
            "/guess <number>"
        )

    # =====================================================
    # ROCK PAPER SCISSORS
    # =====================================================

    elif data == "rps":

        keyboard = [
            [
                InlineKeyboardButton(
                    "🪨 Rock",
                    callback_data="rps_rock"
                )
            ],
            [
                InlineKeyboardButton(
                    "📄 Paper",
                    callback_data="rps_paper"
                )
            ],
            [
                InlineKeyboardButton(
                    "✂️ Scissors",
                    callback_data="rps_scissors"
                )
            ],
        ]

        await query.edit_message_text(
            "🪨📄✂️ Choose:",
            reply_markup=InlineKeyboardMarkup(
                keyboard
            )
        )

    # =====================================================
    # LEADERBOARD
    # =====================================================

    elif data == "leaderboard":

        await query.edit_message_text(
            "🏆 Leaderboard feature coming soon!"
        )

    # =====================================================
    # RPS LOGIC
    # =====================================================

    elif data.startswith("rps_"):

        choices = [
            "rock",
            "paper",
            "scissors",
        ]

        user_choice = data.split("_")[1]

        bot_choice = random.choice(choices)

        result = get_rps_result(
            user_choice,
            bot_choice
        )

        await query.edit_message_text(
            f"🧑 You: {user_choice}\n"
            f"🤖 Bot: {bot_choice}\n\n"
            f"🏆 Result: {result}"
        )

# =========================================================
# GUESS NUMBER COMMAND
# =========================================================


async def guess(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    user_id = update.effective_user.id

    if user_id not in guess_number_games:

        return await update.message.reply_text(
            "🎯 Start a game first using /start"
        )

    if not context.args:

        return await update.message.reply_text(
            "❌ Usage:\n"
            "/guess <number>"
        )

    try:

        user_guess = int(context.args[0])

    except ValueError:

        return await update.message.reply_text(
            "❌ Enter a valid number."
        )

    correct = guess_number_games[user_id]

    if user_guess == correct:

        del guess_number_games[user_id]

        await update.message.reply_text(
            "🎉 Correct! You won!"
        )

    else:

        await update.message.reply_text(
            "❌ Wrong guess. Try again!"
        )

# =========================================================
# HELPERS
# =========================================================


def get_rps_result(
    user_choice,
    bot_choice
):

    if user_choice == bot_choice:
        return "Draw"

    wins = {
        "rock": "scissors",
        "paper": "rock",
        "scissors": "paper",
    }

    if wins[user_choice] == bot_choice:
        return "You Win 🎉"

    return "Bot Wins 🤖"

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
        .token(GAMES_TOKEN)
        .request(request)
        .build()
    )

    app.add_handler(
        CommandHandler("start", start)
    )

    app.add_handler(
        CommandHandler("guess", guess)
    )

    app.add_handler(
        CallbackQueryHandler(game_callback)
    )

    return app
