import os
import logging
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    CallbackQueryHandler, filters
)
from handlers.commands import register_command_handlers
from handlers.settings import register_settings_handlers
from handlers.ai_chat import register_chat_handler
from handlers.donate import register_donate_handlers
from db import init_db

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

def main():
    token = os.environ["TELEGRAM_BOT_TOKEN"]
    init_db()
    application = ApplicationBuilder().token(token).build()
    register_command_handlers(application)
    register_settings_handlers(application)
    register_chat_handler(application)
    register_donate_handlers(application)
    application.run_polling()

if __name__ == "__main__":
    main()
