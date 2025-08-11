from . import openai
from . import gemini
from . import anthropic
from . import grok
from . import cohere
from . import mistral
from . import ollama

PROVIDERS = {
    "OpenAI": openai,
    "Google Gemini": gemini,
    "Anthropic": anthropic,
    "Grok": grok,
    "Cohere": cohere,
    "Mistral": mistral,
    "Ollama": ollama,
}
