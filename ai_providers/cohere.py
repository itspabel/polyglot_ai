import cohere
import asyncio

async def validate_and_list_models(api_key: str):
    try:
        client = cohere.Client(api_key)
        resp = await asyncio.get_event_loop().run_in_executor(None, client.models)
        models = [m.name for m in resp]
        return True, models
    except Exception:
        return False, []

async def chat(api_key, model, messages):
    client = cohere.Client(api_key)
    prompt = "\n".join([f"{m['role']}: {m['content']}" for m in messages])
    resp = await asyncio.get_event_loop().run_in_executor(
        None,
        lambda: client.chat(model=model, message=prompt)
    )
    try:
        return resp.text
    except Exception:
        return "Error: Could not parse Cohere response."
