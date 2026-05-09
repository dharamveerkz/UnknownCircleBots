import asyncio
import logging

from config import validate_config
from utils.db import init_db
from mod_bot import create_app as mod_app
from games_bot import create_app as games_app
from ai_bot import create_app as ai_app
from fun_bot import create_app as fun_app

# =========================================================
# LOGGING
# =========================================================

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

logger = logging.getLogger(__name__)

# =========================================================
# START SINGLE BOT
# =========================================================


async def start_bot(name, app):

    try:

        logger.info(f"🚀 Starting {name} Bot...")

        await app.initialize()

        await app.start()

        if app.updater:
            await app.updater.start_polling(
                drop_pending_updates=True
            )

        logger.info(
            f"✅ {name} Bot started successfully!"
        )

    except Exception as e:

        logger.error(
            f"❌ Failed to start {name} Bot: {e}"
        )

# =========================================================
# MAIN
# =========================================================


async def main():

    validate_config()
    init_db()
    # Validate config

    validate_config()

    logger.info(
        "🚀 Launching UnknownCircle bot suite..."
    )

    # Create all apps
    apps = [
        ("🛡️ Mod", mod_app()),
        ("🎮 Games", games_app()),
        ("🤖 AI", ai_app()),
        ("🎲 Fun", fun_app()),
    ]

    # Start all bots concurrently
    await asyncio.gather(
        *(start_bot(name, app) for name, app in apps)
    )

    logger.info("✨ All bots running!")

    # Keep alive
    try:

        while True:
            await asyncio.sleep(3600)

    except KeyboardInterrupt:

        logger.info("🛑 Shutting down...")

        for _, app in apps:

            try:

                await app.stop()

                await app.shutdown()

            except Exception as e:

                logger.error(
                    f"Shutdown error: {e}"
                )

# =========================================================
# ENTRY
# =========================================================

if __name__ == "__main__":

    asyncio.run(main())
