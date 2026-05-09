import logging

from telegram import (
    Update,
    ChatPermissions,
)

from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)

from telegram.request import HTTPXRequest

from config import (
    MOD_TOKEN,
    MAX_WARNINGS_BEFORE_BAN,
)

# =========================================================
# LOGGING
# =========================================================

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

# =========================================================
# STORAGE
# =========================================================

# Temporary in-memory storage
# Use Redis or SQLite in production

warnings = {}

# =========================================================
# COMMANDS
# =========================================================


async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    await update.message.reply_text(
        "🛡️ Mod Bot Active!\n\n"
        "Available Commands:\n"
        "/warn\n"
        "/ban\n"
        "/mute\n"
        "/rules"
    )


async def rules(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    rules_text = """
📜 Group Rules

1️⃣ No spam or scams
2️⃣ Respect everyone
3️⃣ No NSFW content
4️⃣ No bot abuse
5️⃣ Admin decisions are final
"""

    await update.message.reply_text(rules_text)


async def warn(update, context):

    if not await is_admin(update):
        return await update.message.reply_text("❌ Admins only.")

    if not update.message.reply_to_message:
        return await update.message.reply_text("⚠️ Reply to user.")

    user = update.message.reply_to_message.from_user
    user_id = user.id

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT count FROM warnings WHERE user_id=?",
        (user_id,)
    )

    row = cursor.fetchone()

    count = row["count"] if row else 0
    count += 1

    cursor.execute("""
        INSERT INTO warnings (user_id, count)
        VALUES (?, ?)
        ON CONFLICT(user_id)
        DO UPDATE SET count=excluded.count
    """, (user_id, count))

    conn.commit()
    conn.close()

    await update.message.reply_text(
        f"⚠️ Warning given. Total: {count}"
    )

    if count >= 3:
        await update.effective_chat.ban_member(user_id)
        await update.message.reply_text("🔨 User banned.")


async def ban(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    if not await is_admin(update):
        return

    if not update.message.reply_to_message:
        return await update.message.reply_text(
            "⚠️ Reply to a user to ban."
        )

    user = update.message.reply_to_message.from_user

    try:

        await update.effective_chat.ban_member(
            user.id
        )

        await update.message.reply_text(
            f"🔨 {user.first_name} banned."
        )

    except Exception as e:

        logger.error(e)

        await update.message.reply_text(
            "⚠️ Failed to ban user."
        )


async def mute(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    if not await is_admin(update):
        return

    if not update.message.reply_to_message:
        return await update.message.reply_text(
            "⚠️ Reply to a user to mute."
        )

    user = update.message.reply_to_message.from_user

    try:

        permissions = ChatPermissions(
            can_send_messages=False
        )

        await update.effective_chat.restrict_member(
            user.id,
            permissions=permissions
        )

        await update.message.reply_text(
            f"🔇 {user.first_name} muted."
        )

    except Exception as e:

        logger.error(e)

        await update.message.reply_text(
            "⚠️ Failed to mute user."
        )

# =========================================================
# HELPERS
# =========================================================


async def is_admin(update: Update) -> bool:

    member = await update.effective_chat.get_member(
        update.effective_user.id
    )

    return member.status in [
        "administrator",
        "creator",
    ]

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
        .token(MOD_TOKEN)
        .request(request)
        .build()
    )

    app.add_handler(
        CommandHandler("start", start)
    )

    app.add_handler(
        CommandHandler("rules", rules)
    )

    app.add_handler(
        CommandHandler("warn", warn)
    )

    app.add_handler(
        CommandHandler("ban", ban)
    )

    app.add_handler(
        CommandHandler("mute", mute)
    )

    return app
