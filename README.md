# 🧠 Azitech Open Source AI Search Assistant

**Central de Soluções Digitais com IA Multi-Provedor**  
Desenvolvido por [Gustavo Nogueira](https://azitech.com.br), CEO da AZITech.

Sistema modular que integra **múltiplos provedores de IA** (Groq, Fireworks, Together, Replicate, Vercel AI Gateway) em uma única interface Streamlit. Oferece desde análise de texto local até geração de código em Python, Rust, C++, consultas SEO e etimologia.

🔗 **Acesse o site oficial:** [azitech.com.br](https://azitech.com.br)

---

## 📋 Índice
- [Visão Geral](#visão-geral)
- [Arquitetura do Sistema](#arquitetura-do-sistema)
- [Módulos Disponíveis](#módulos-disponíveis)
- [Tecnologias Utilizadas](#tecnologias-utilizadas)
- [Pré-requisitos](#pré-requisitos)
- [Instalação e Execução](#instalação-e-execução)
- [Como Obter Chaves de API](#como-obter-chaves-de-api)
- [Estrutura de Pastas](#estrutura-de-pastas)
- [Créditos e Agradecimentos](#créditos-e-agradecimentos)
- [Contribuição](#contribuição)
- [Licença](#licença)

---

## 🚀 Visão Geral

O **Azitech AI Search Assistant** é uma plataforma unificada que permite acessar dezenas de modelos de IA através de um único ponto de entrada, com fallback automático entre provedores. Ideal para:

- Profissionais de **SEO** que precisam de auditorias técnicas e sugestões de otimização.
- **Desenvolvedores** que desejam gerar código em múltiplas linguagens.
- **Pesquisadores** e **curiosos** que querem explorar etimologia e cálculos.
- Empresas que buscam **independência de provedor** e otimização de custos.

---

## 🏗️ Arquitetura do Sistema

O sistema é composto por:

1. **Router Inteligente (`router.py`)**  
   Gerencia chamadas para múltiplos provedores (Groq, Fireworks, Together, Replicate, Vercel) com fallback automático. Se um provedor falhar (cota excedida, instabilidade), a requisição é redirecionada para o próximo disponível.

2. **Módulos Especializados**  
   Cada funcionalidade é isolada em um módulo independente dentro da pasta `modules/`. Todos utilizam o router para comunicação com a IA.

3. **Interface Streamlit (`app.py`)**  
   Interface gráfica moderna, responsiva e totalmente personalizada com a identidade visual da AZITech.

4. **Analisador Core (`analisador_core.py`)**  
   Funcionalidades locais sem IA: extração de headings, metadados, análise de sentimento, palavras-chave, leitura de PDF, etc.

---

## 📦 Módulos Disponíveis

| Módulo | Arquivo | Descrição |
|--------|---------|-----------|
| **Analisador Core** | `analisador_core.py` | Análise de texto, PDF, headings e metadados (totalmente local, sem IA). |
| **Assistente SEO** | `search_assistant.py` | Chat especializado em SEO, estratégias de ranqueamento e otimização de conteúdo. Baseado nas diretrizes oficiais do Google Search Central. |
| **Código Python** | `code_assistant.py` | Gera código Python a partir de descrições, com explicação, exemplo e LaTeX. |
| **Rust (Cálculo)** | `rust_calc_assistant.py` | Gera código Rust para problemas matemáticos e numéricos, com exemplos usando números inteiros (prova real). |
| **C++ (Cálculo)** | `cpp_calc_assistant.py` | Gera código C++ para cálculos, com exemplos usando números inteiros (prova real). |
| **Etimologia** | `etimologia.py` | Consulta a origem de palavras em latim, grego, sânscrito, hebraico, etc. Baseado em dicionários etimológicos e referências acadêmicas. |

---

## 🛠️ Tecnologias Utilizadas

- **Linguagem:** Python 3.10+
- **Framework Web:** [Streamlit](https://streamlit.io)
- **Provedores de IA:**
  - [Groq](https://groq.com)
  - [Fireworks AI](https://fireworks.ai)
  - [Together AI](https://together.ai)
  - [Replicate](https://replicate.com)
  - [Vercel AI Gateway](https://vercel.com/ai-gateway) (compatível com OpenAI)
- **Bibliotecas principais:**
  - `PyPDF2` – extração de texto de PDFs
  - `requests` + `beautifulsoup4` – scraping de headings e metadados
  - `openai` – cliente base para APIs compatíveis
  - `groq`, `fireworks-ai`, `together`, `replicate` – SDKs oficiais
  - `python-dotenv` – gerenciamento de variáveis de ambiente

---

## ✅ Pré-requisitos

- **Python 3.10 ou superior** instalado.
- **Git** (para clonar o repositório).
- **Chaves de API** de pelo menos um dos provedores suportados (recomenda-se ter várias para fallback).

---

## 🔧 Instalação e Execução

### 1. Clone o repositório

```bash
git clone https://github.com/Gussnogue/azitech_open_source_ai_search_assistant.git
cd azitech_open_source_ai_search_assistant

2. Crie e ative um ambiente virtual (recomendado)

Windows:

bash
python -m venv venv
venv\Scripts\activate

Linux/macOS:

bash
python3 -m venv venv
source venv/bin/activate

3. Instale as dependências

bash
pip install -r requirements.txt

4. Configure as chaves de API (opcional)

Você pode criar um arquivo .env na raiz do projeto com suas chaves:

env
GROQ_API_KEY=sua_chave
FIREWORKS_API_KEY=sua_chave
TOGETHER_API_KEY=sua_chave
REPLICATE_API_TOKEN=sua_chave
VERCEL_AI_GATEWAY_KEY=sua_chave

Ou inserir as chaves diretamente na interface do Streamlit após executar o app.

5. Execute o aplicativo

bash
streamlit run app.py

O aplicativo abrirá automaticamente no navegador em http://localhost:8501.

🔑 Como Obter Chaves de API
Provedor	URL para cadastro	Plano gratuito
Groq	console.groq.com	✅ Sim (30 req/min)
Fireworks AI	fireworks.ai	✅ Sim (créditos iniciais)
Together AI	together.ai	✅ Sim (créditos iniciais)
Replicate	replicate.com	✅ Sim (créditos iniciais)
Vercel AI Gateway	vercel.com/ai-gateway	✅ Sim ($5/mês grátis)
Recomenda-se cadastrar-se em todos para aproveitar as cotas gratuitas e garantir alta disponibilidade.

📁 Estrutura de Pastas

text
azitech_open_source_ai_search_assistant/
├── app.py                     # Interface Streamlit (frontend principal)
├── requirements.txt           # Dependências do projeto
├── README.md                  # Documentação
├── .env.example               # Exemplo de arquivo de ambiente
├── .gitignore                 # Arquivos ignorados pelo Git
└── modules/
    ├── __init__.py            # Torna a pasta um pacote Python
    ├── analisador_core.py     # Módulo local (sem IA)
    ├── search_assistant.py    # Assistente SEO
    ├── code_assistant.py      # Assistente Python
    ├── rust_calc_assistant.py # Assistente Rust
    ├── cpp_calc_assistant.py  # Assistente C++
    ├── etimologia.py          # Consulta etimológica
    └── router.py              # Roteador inteligente multi-provedor

🙏 Créditos e Agradecimentos
Este projeto utiliza documentações e recursos oficiais das seguintes tecnologias e provedores:

Tecnologia	Documentação Oficial	Ícone
Python	docs.python.org/3	https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white
Streamlit	docs.streamlit.io	https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white
Groq	console.groq.com/docs	https://img.shields.io/badge/Groq-00A67E?style=flat&logo=groq&logoColor=white
Fireworks AI	readme.fireworks.ai	https://img.shields.io/badge/Fireworks_AI-FF6F00?style=flat
Together AI	docs.together.ai	https://img.shields.io/badge/Together_AI-5A2B77?style=flat
Replicate	replicate.com/docs	https://img.shields.io/badge/Replicate-003D74?style=flat
Vercel AI Gateway	vercel.com/docs/ai	https://img.shields.io/badge/Vercel-000000?style=flat&logo=vercel&logoColor=white
PyPDF2	pypdf2.readthedocs.io	https://img.shields.io/badge/PyPDF2-FFD43B?style=flat&logo=python&logoColor=blue
Beautiful Soup	crummy.com/software/BeautifulSoup	https://img.shields.io/badge/Beautiful_Soup-4B8BBE?style=flat
Agradecimentos especiais às comunidades open-source que tornaram este projeto possível.

🤝 Contribuição

Contribuições são bem-vindas! Se você deseja:

Adicionar um novo provedor de IA.
Criar um novo módulo especializado.
Corrigir bugs ou melhorar a interface.

Siga os passos:

Faça um fork do projeto.
Crie uma branch para sua feature (git checkout -b feature/nova-funcionalidade).
Commit suas mudanças (git commit -m 'Adiciona nova funcionalidade').
Push para a branch (git push origin feature/nova-funcionalidade).
Abra um Pull Request.

📄 Licença
Este projeto está licenciado sob a MIT License.

© 2026 AZITech – Central de Soluções Digitais.
Desenvolvido por Gustavo Silva Nogueira.
📍 Teófilo Otoni - MG • 📧 azitech.oficial@gmail.com
🌐 azitech.com.br • 📱 @azi.tech.math (Instagram, LinkedIn, Twitter)
