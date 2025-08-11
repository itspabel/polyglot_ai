import requests
import asyncio

BASE_URL = "http://localhost:11434"

async def validate_and_list_models(api_key: str):
    try:
        url = f"{BASE_URL}/api/tags"
        resp = await asyncio.get_event_loop().run_in_executor(
            None, lambda: requests.get(url, timeout=6)
        )
        if resp.status_code != 200:
            return False, []
        models = [m["name"] for m in resp.json().get("models", [])]
        return True, models
    except Exception:
        return False, []

async def chat(api_key, model, messages):
    url = f"{BASE_URL}/api/chat"
    prompt = {
        "model": model,
        "messages": messages,
    }
    resp = await asyncio.get_event_loop().run_in_executor(
        None, lambda: requests.post(url, json=prompt, timeout=15)
    )
    try:
        return resp.json()["message"]["content"]
    except Exception:
        return "Error: Could not parse Ollama response."
