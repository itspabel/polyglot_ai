from telegram.ext import CommandHandler
from telegram import Update
from telegram.ext import ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome to Polyglot AI!\n"
        "I'm your gateway to top AIs using your own API keys. "
        "Your API keys are encrypted and never shared. "
        "Use /settings to get started.\n\n"
        "Commands:\n"
        "/settings - Manage AIs and keys\n"
        "/clear - Clear chat history\n"
        "/donate - Donate a star ⭐\n"
        "/leaderboard - Star leaderboard\n"
        "/help - Help info"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 Polyglot AI Bot Help\n\n"
        "• /settings — Manage your AI providers, API keys, and models\n"
        "• /clear — Clear current conversation history\n"
        "• /donate — Donate a star to support the project\n"
        "• /leaderboard — See top star donors\n"
        "• Just send a message to chat with your selected AI!"
    )

async def clear_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["history"] = []
    await update.message.reply_text("🧹 Conversation history cleared for the current AI.")

def register_command_handlers(application):
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("clear", clear_command))
