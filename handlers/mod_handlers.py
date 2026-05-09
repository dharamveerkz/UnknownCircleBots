from telegram import Update
from telegram.ext import ContextTypes

# =========================================================
# WELCOME MESSAGE
# =========================================================


async def welcome_user(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    if not update.message.new_chat_members:
        return

    for user in update.message.new_chat_members:

        await update.message.reply_text(
            f"👋 Welcome {user.first_name}!\n"
            "Please read the group rules."
        )

# =========================================================
# GOODBYE MESSAGE
# =========================================================


async def goodbye_user(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    if not update.message.left_chat_member:
        return

    user = update.message.left_chat_member

    await update.message.reply_text(
        f"👋 Goodbye {user.first_name}"
    )

# =========================================================
# BAD WORD FILTER
# =========================================================

BAD_WORDS = [
    "spam",
    "scam",
    "badword",
]


async def bad_word_filter(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    if not update.message.text:
        return

    text = update.message.text.lower()

    for word in BAD_WORDS:

        if word in text:

            try:

                await update.message.delete()

                await update.message.reply_text(
                    "🚫 Bad words are not allowed."
                )

            except Exception:
                pass

            break
