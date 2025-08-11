import requests
import asyncio

API_URL = "https://generativelanguage.googleapis.com/v1beta/models"

async def validate_and_list_models(api_key: str):
    try:
        url = f"{API_URL}?key={api_key}"
        resp = await asyncio.get_event_loop().run_in_executor(
            None, lambda: requests.get(url, timeout=8)
        )
        if resp.status_code != 200:
            return False, []
        models = [m["name"].split("/")[-1] for m in resp.json().get("models", [])]
        return True, models
    except Exception:
        return False, []

async def chat(api_key, model, messages):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
    prompt = {
        "contents": [{"parts": [{"text": m["content"]}]} for m in messages]
    }
    resp = await asyncio.get_event_loop().run_in_executor(
        None, lambda: requests.post(url, json=prompt, timeout=10)
    )
    try:
        return resp.json()["candidates"][0]["content"]["parts"][0]["text"]
    except Exception:
        return "Error: Could not parse Gemini response."
