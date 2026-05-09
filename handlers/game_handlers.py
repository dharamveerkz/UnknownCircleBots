import random

from telegram import Update

from telegram.ext import ContextTypes

# =========================================================
# TRIVIA QUESTIONS
# =========================================================

QUESTIONS = [
    {
        "question": "Capital of India?",
        "answer": "Delhi",
    },
    {
        "question": "2 + 2 = ?",
        "answer": "4",
    },
    {
        "question": "Python creator?",
        "answer": "Guido van Rossum",
    },
]

# =========================================================
# TRIVIA COMMAND
# =========================================================


async def trivia(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    q = random.choice(QUESTIONS)

    context.user_data["trivia_answer"] = (
        q["answer"]
    )

    await update.message.reply_text(
        f"🧠 Trivia Question:\n\n"
        f"{q['question']}"
    )

# =========================================================
# CHECK ANSWER
# =========================================================


async def check_trivia_answer(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    if "trivia_answer" not in context.user_data:
        return

    answer = (
        context.user_data["trivia_answer"]
    )

    user_answer = update.message.text

    if (
        user_answer.lower()
        == answer.lower()
    ):

        await update.message.reply_text(
            "✅ Correct answer!"
        )

    else:

        await update.message.reply_text(
            f"❌ Wrong answer.\n"
            f"Correct: {answer}"
        )

    del context.user_data["trivia_answer"]

# =========================================================
# RANDOM NUMBER GAME
# =========================================================


async def random_number_game(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    number = random.randint(1, 100)

    await update.message.reply_text(
        f"🎯 Random Number: {number}"
    )
