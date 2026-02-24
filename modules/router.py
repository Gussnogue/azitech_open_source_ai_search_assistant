# modules/router.py
import time
from typing import List, Dict, Any, Optional
import openai
from groq import Groq
import fireworks.client
import together

# Dicionário de modelos disponíveis por provedor (pode expandir)
MODELS_BY_PROVIDER = {
    "groq": [
        "llama3-70b-8192",
        "llama3-8b-8192",
        "mixtral-8x7b-32768",
        "gemma2-9b-it",
        "openai/gpt-oss-120b"
    ],
    "fireworks": [
        "accounts/fireworks/models/llama-v3-70b-instruct",
        "accounts/fireworks/models/llama-v3-8b-instruct",
        "accounts/fireworks/models/mixtral-8x7b-instruct"
    ],
    "together": [
        "meta-llama/Llama-3-70b-chat-hf",
        "meta-llama/Llama-3-8b-chat-hf",
        "mistralai/Mixtral-8x7B-Instruct-v0.1"
    ],
    "replicate": [
        "meta/meta-llama-3-70b-instruct",
        "meta/meta-llama-3-8b-instruct",
        "mistralai/mistral-7b-instruct-v0.2"
    ]
}

class LLMRouter:
    def __init__(self, api_keys: Dict[str, str]):
        self.api_keys = api_keys
        self.providers = self._init_providers()

    def _init_providers(self):
        providers = {}
        if self.api_keys.get("groq"):
            providers["groq"] = {
                "client": Groq(api_key=self.api_keys["groq"]),
                "chat": self._chat_groq
            }
        if self.api_keys.get("fireworks"):
            fireworks.client.api_key = self.api_keys["fireworks"]
            providers["fireworks"] = {
                "client": fireworks.client,
                "chat": self._chat_fireworks
            }
        if self.api_keys.get("together"):
            together.api_key = self.api_keys["together"]
            providers["together"] = {
                "client": together,
                "chat": self._chat_together
            }
        if self.api_keys.get("replicate"):
            providers["replicate"] = {
                "client": None,
                "chat": self._chat_replicate
            }
        return providers

    def _chat_groq(self, client, messages, model, temperature, max_tokens):
        return client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens
        ).choices[0].message.content

    def _chat_fireworks(self, client, messages, model, temperature, max_tokens):
        resp = client.ChatCompletion.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens
        )
        return resp.choices[0].message.content

    def _chat_together(self, client, messages, model, temperature, max_tokens):
        resp = client.ChatCompletion.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens
        )
        return resp.choices[0].message.content

    def _chat_replicate(self, client, messages, model, temperature, max_tokens):
        import replicate
        prompt = "\n".join([f"{m['role']}: {m['content']}" for m in messages])
        output = replicate.run(
            model,
            input={"prompt": prompt, "temperature": temperature, "max_tokens": max_tokens}
        )
        return "".join(output)

    def chat_completion(self, messages: List[Dict], provider: Optional[str] = None,
                        model: Optional[str] = None, temperature=0.7, max_tokens=1000) -> str:
        """
        Se provider for None, tenta todos em ordem.
        Se provider for especificado, tenta apenas aquele.
        Se model for None, usa o primeiro da lista do provedor.
        """
        if provider and provider not in self.providers:
            return f"❌ Provedor '{provider}' não configurado ou chave inválida."

        # Caso específico: provedor escolhido
        if provider:
            prov = self.providers[provider]
            # Se modelo não especificado, pega o primeiro da lista
            if model is None:
                model = MODELS_BY_PROVIDER[provider][0]
            try:
                print(f"🔄 Usando {provider} com modelo {model}...")
                return prov["chat"](prov["client"], messages, model, temperature, max_tokens)
            except Exception as e:
                return f"❌ Erro no provedor {provider}: {e}"

        # Fallback: tenta todos em ordem (Groq, Fireworks, Together, Replicate)
        ordem = ["groq", "fireworks", "together", "replicate"]
        for prov_name in ordem:
            if prov_name in self.providers:
                try:
                    model_uso = MODELS_BY_PROVIDER[prov_name][0]
                    print(f"🔄 Tentando fallback {prov_name}...")
                    resp = self.providers[prov_name]["chat"](
                        self.providers[prov_name]["client"],
                        messages, model_uso, temperature, max_tokens
                    )
                    return resp
                except Exception as e:
                    print(f"⚠️ Fallback {prov_name} falhou: {e}")
                    continue
        return "❌ Todos os provedores falharam. Verifique suas chaves e cotas."
    
    