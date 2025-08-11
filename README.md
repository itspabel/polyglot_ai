# Polyglot AI Telegram Bot

Universal AI gateway bot for Telegram (BYOK, supports OpenAI, Google Gemini, Anthropic Claude, Grok, Cohere, Mistral, Ollama, and more).
Includes a star donation system for users to show support!

## Features

- Bring-Your-Own-Key (BYOK) for all supported AI providers
- Secure API key storage (encrypted at rest)
- Easy model selection & switching
- Chat with any configured AI
- Star donation system & leaderboard
- Simple setup: SQLite for storage
- Extensible provider adapters

## Setup

1. Clone this repo
2. `pip install -r requirements.txt`
3. Export environment variables:
   - `TELEGRAM_BOT_TOKEN=...`
   - `FERNET_KEY=$(python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())")`
4. `python bot.py`

## Extending

Add new AI providers in `ai_providers/` and register them in `ai_providers/__init__.py`.
