from telegram.ext import CommandHandler, CallbackQueryHandler
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from db import get_or_create_user, increment_stars, get_top_donors

async def donate_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = get_or_create_user(update.effective_user.id)
    keyboard = [[InlineKeyboardButton("⭐ Donate a Star", callback_data="donate_star")]]
    msg = f"🌟 You have donated {user.stars} stars!\nWant to support Polyglot AI? Press the button below to donate a star."
    await update.message.reply_text(msg, reply_markup=InlineKeyboardMarkup(keyboard))

async def donate_star_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user = get_or_create_user(query.from_user.id)
    increment_stars(user)
    await query.answer("Thank you for your star! ⭐")
    await query.edit_message_text(f"🌟 You have donated {user.stars} stars! Thank you for your support.")

async def leaderboard_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    top = get_top_donors()
    msg = "🏆 Star Donor Leaderboard:\n"
    for i, (uid, stars) in enumerate(top, 1):
        msg += f"{i}. {uid}: {stars}⭐\n"
    await update.message.reply_text(msg)

def register_donate_handlers(application):
    application.add_handler(CommandHandler("donate", donate_command))
    application.add_handler(CommandHandler("leaderboard", leaderboard_command))
    application.add_handler(CallbackQueryHandler(donate_star_callback, pattern="^donate_star$"))
