# modules/search_assistant.py
from modules.router import LLMRouter

def chat_seo(mensagens, api_keys, provider=None, model=None):
    router = LLMRouter(api_keys)
    return router.chat_completion(
        messages=mensagens,
        provider=provider,
        model=model,
        temperature=0.7,
        max_tokens=1000
    )