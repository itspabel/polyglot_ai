import openai
import asyncio

async def validate_and_list_models(api_key: str):
    try:
        client = openai.OpenAI(api_key=api_key)
        resp = await asyncio.get_event_loop().run_in_executor(None, client.models.list)
        models = [m.id for m in resp.data if "gpt" in m.id]
        return True, models
    except Exception:
        return False, []

async def chat(api_key, model, messages):
    client = openai.OpenAI(api_key=api_key)
    completion = await asyncio.get_event_loop().run_in_executor(
        None,
        lambda: client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.7
        )
    )
    return completion.choices[0].message.content
