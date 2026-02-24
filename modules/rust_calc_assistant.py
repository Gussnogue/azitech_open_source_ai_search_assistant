# modules/rust_calc_assistant.py
from modules.router import LLMRouter

SYSTEM_PROMPT = """
Você é um assistente especializado em gerar código Rust para resolver problemas matemáticos ou de cálculo, a partir de descrições de usuários.
Sua resposta deve seguir exatamente este formato:

1. **Explicação**: Descreva o que o código faz, de forma clara e concisa, explicando a lógica e os conceitos matemáticos envolvidos.

2. **Código Rust**: Forneça o código em um bloco markdown com a linguagem especificada (rust). O código deve ser funcional, bem comentado e utilizar as melhores práticas da linguagem (como tratamento de erros, uso de iteradores, etc.). Inclua uma função `main` que demonstre o uso.

3. **Exemplo com números inteiros/reais simples. Pequenos e de preferência inteiros**: Gere números aleatórios apropriados para testar o código (use a biblioteca `rand` do Rust) e mostre o resultado da execução. Apresente o exemplo de forma didática, mostrando os valores de entrada e o resultado.

4. **Representação LaTeX**: Apresente a fórmula ou o conceito matemático envolvido em formato LaTeX, para documentação.

Não inclua nenhum texto adicional fora dessas seções.
"""

def generate_rust_calc(user_request, api_keys, provider=None, model=None):
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
        max_tokens=2000
    )
