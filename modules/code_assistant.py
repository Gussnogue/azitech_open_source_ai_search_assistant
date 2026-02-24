# modules/code_assistant.py
from modules.router import LLMRouter, MODELS_BY_PROVIDER

SYSTEM_PROMPT = """
Você é um assistente especializado em gerar código Python a partir de descrições de usuários.
Sua resposta deve seguir exatamente este formato:

1. **Explicação**: Descreva o que o código faz, de forma clara e concisa.

2. **Código Python**: Forneça o código em um bloco markdown com a linguagem especificada (python). O código deve ser funcional e bem comentado.

3. **Exemplo com números inteiros/reais simples.Pequenos e de preferência inteiros**: Gere números aleatórios apropriados para testar o código (use a biblioteca random ou numpy) e mostre o resultado da execução. Apresente o exemplo de forma didática, mostrando os valores de entrada e o resultado.

Não inclua nenhum texto adicional fora dessas seções.
"""

def generate_code(user_request, api_keys, provider=None, model=None):
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_request}
    ]
    router = LLMRouter(api_keys)
    return router.chat_completion(
        messages=messages,
        provider=provider,
        model=model,
        temperature=0.3,
        max_tokens=1500
    )
