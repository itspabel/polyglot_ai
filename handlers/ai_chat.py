from telegram.ext import MessageHandler, filters
from db import get_user_keys
from ai_providers import PROVIDERS

HISTORY_LEN = 10

async def chat_message(update, context):
    if update.message.text.startswith("/"):
        return  # Let commands handle
    user_id = update.effective_user.id
    active_ai = context.user_data.get("active_ai")
    if not active_ai:
        await update.message.reply_text("❗ No AI selected. Use /settings to add and activate an AI.")
        return
    keys = {k.provider_name: k for k in get_user_keys(user_id)}
    if active_ai not in keys:
        await update.message.reply_text("❗ Selected AI not found. Use /settings.")
        return
    keyobj = keys[active_ai]
    from db import decrypt_key
    api_key = decrypt_key(keyobj.encrypted_api_key)
    model = keyobj.selected_model
    history = context.user_data.setdefault("history", [])
    history.append({"role": "user", "content": update.message.text})
    if len(history) > HISTORY_LEN:
        history = history[-HISTORY_LEN:]
        context.user_data["history"] = history
    messages = [{"role": h["role"], "content": h["content"]} for h in history]
    try:
        prov_mod = PROVIDERS[active_ai]
        response = await prov_mod.chat(api_key, model, messages)
        await update.message.reply_text(response)
        history.append({"role": "assistant", "content": response})
        if len(history) > HISTORY_LEN:
            context.user_data["history"] = history[-HISTORY_LEN:]
    except Exception as e:
        await update.message.reply_text("⚠️ AI error: " + str(e))

def register_chat_handler(application):
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat_message))
