import requests
import asyncio

API_URL = "https://api.anthropic.com/v1/models"

async def validate_and_list_models(api_key: str):
    headers = {
        "x-api-key": api_key,
        "anthropic-version": "2023-06-01",
    }
    try:
        resp = await asyncio.get_event_loop().run_in_executor(
            None, lambda: requests.get(API_URL, headers=headers, timeout=8)
        )
        if resp.status_code != 200:
            return False, []
        models = [m["id"] for m in resp.json().get("models", [])]
        return True, models
    except Exception:
        return False, []

async def chat(api_key, model, messages):
    url = "https://api.anthropic.com/v1/messages"
    headers = {
        "x-api-key": api_key,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json",
    }
    prompt = {
        "model": model,
        "max_tokens": 1024,
        "messages": [{"role": m["role"], "content": m["content"]} for m in messages],
    }
    resp = await asyncio.get_event_loop().run_in_executor(
        None, lambda: requests.post(url, headers=headers, json=prompt, timeout=15)
    )
    try:
        return resp.json()["content"][0]["text"]
    except Exception:
        return "Error: Could not parse Claude response."
