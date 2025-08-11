import requests
import asyncio

API_URL = "https://api.mistral.ai/v1/models"

async def validate_and_list_models(api_key: str):
    headers = {"Authorization": f"Bearer {api_key}"}
    try:
        resp = await asyncio.get_event_loop().run_in_executor(
            None, lambda: requests.get(API_URL, headers=headers, timeout=8)
        )
        if resp.status_code != 200:
            return False, []
        models = [m["id"] for m in resp.json().get("data", [])]
        return True, models
    except Exception:
        return False, []

async def chat(api_key, model, messages):
    url = "https://api.mistral.ai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    prompt = {
        "model": model,
        "messages": messages,
        "max_tokens": 1024,
    }
    resp = await asyncio.get_event_loop().run_in_executor(
        None, lambda: requests.post(url, headers=headers, json=prompt, timeout=15)
    )
    try:
        return resp.json()["choices"][0]["message"]["content"]
    except Exception:
        return "Error: Could not parse Mistral response."
