from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    CallbackQueryHandler, CommandHandler, MessageHandler, filters, ContextTypes
)
from db import (
    get_user_keys, set_active_ai, remove_ai, get_or_create_user
)
from ai_providers import PROVIDERS

async def settings_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Add New AI", callback_data="add_ai")],
        [InlineKeyboardButton("Switch Active AI", callback_data="switch_ai")],
        [InlineKeyboardButton("My AIs & Usage", callback_data="my_ais")],
        [InlineKeyboardButton("Remove AI", callback_data="remove_ai")]
    ]
    await update.message.reply_text(
        "⚙️ Settings panel. Manage AI providers and models:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def settings_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "add_ai":
        keyboard = [
            [InlineKeyboardButton(name, callback_data=f"provider_{name}")]
            for name in PROVIDERS
        ]
        await query.edit_message_text(
            "Select an AI provider to add:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    elif data.startswith("provider_"):
        provider = data.split("_", 1)[1]
        context.user_data["pending_provider"] = provider
        await query.edit_message_text(
            f"Paste your {provider} API key. (This message will be deleted for your security.)"
        )
        context.user_data["awaiting_api_key"] = True
    elif data == "switch_ai":
        keys = get_user_keys(query.from_user.id)
        keyboard = [
            [InlineKeyboardButton(f"{k.provider_name}: {k.selected_model}", callback_data=f"activate_{k.provider_name}")]
            for k in keys
        ] or [[InlineKeyboardButton("No AIs Configured", callback_data="none")]]
        await query.edit_message_text("Choose AI to activate:", reply_markup=InlineKeyboardMarkup(keyboard))
    elif data.startswith("activate_"):
        provider = data.split("_", 1)[1]
        context.user_data["active_ai"] = provider
        await query.edit_message_text(f"✅ {provider} is now your active AI.")
    elif data == "my_ais":
        keys = get_user_keys(query.from_user.id)
        if not keys:
            msg = "No AI providers configured yet."
        else:
            msg = "Your configured AIs:\n"
            for k in keys:
                msg += f"• {k.provider_name}: {k.selected_model}\n"
        await query.edit_message_text(msg)
    elif data == "remove_ai":
        keys = get_user_keys(query.from_user.id)
        keyboard = [
            [InlineKeyboardButton(f"{k.provider_name}", callback_data=f"remove_{k.provider_name}")]
            for k in keys
        ] or [[InlineKeyboardButton("No AIs Configured", callback_data="none")]]
        await query.edit_message_text("Select an AI to remove:", reply_markup=InlineKeyboardMarkup(keyboard))
    elif data.startswith("remove_"):
        provider = data.split("_", 1)[1]
        remove_ai(query.from_user.id, provider)
        await query.edit_message_text(f"❌ Removed {provider} from your configuration.")
    else:
        await query.edit_message_text("Unknown option.")

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get("awaiting_api_key"):
        provider = context.user_data["pending_provider"]
        api_key = update.message.text.strip()
        prov_mod = PROVIDERS[provider]
        valid, models = await prov_mod.validate_and_list_models(api_key)
        await update.message.delete()
        if valid:
            context.user_data["pending_api_key"] = api_key
            context.user_data["available_models"] = models
            keyboard = [
                [InlineKeyboardButton(model, callback_data=f"selectmodel_{model}")]
                for model in models
            ]
            await update.message.reply_text(
                "API key valid! Choose a model:",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
        else:
            await update.message.reply_text(
                "❌ API key invalid. Please try again in /settings."
            )
        context.user_data["awaiting_api_key"] = False
    elif update.message.text.startswith("/"):
        return
    else:
        pass  # Let chat handler handle

async def select_model_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    model = query.data.split("_", 1)[1]
    provider = context.user_data["pending_provider"]
    api_key = context.user_data["pending_api_key"]
    set_active_ai(query.from_user.id, provider, model, api_key)
    context.user_data["active_ai"] = provider
    await query.edit_message_text(
        f"✅ Success! {provider} ({model}) is now your active chat model."
    )
    context.user_data.pop("pending_provider", None)
    context.user_data.pop("pending_api_key", None)
    context.user_data.pop("available_models", None)

def register_settings_handlers(application):
    application.add_handler(CommandHandler("settings", settings_command))
    application.add_handler(CallbackQueryHandler(settings_callback, pattern="^(add_ai|provider_|switch_ai|activate_|my_ais|remove_ai|remove_)"))
    application.add_handler(CallbackQueryHandler(select_model_callback, pattern="^selectmodel_"))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))
