# app.py
import streamlit as st
import os
import tempfile
from modules import analisador_core, search_assistant, code_assistant
from modules import rust_calc_assistant, cpp_calc_assistant, etimologia
from modules.router import MODELS_BY_PROVIDER

# ==================== CONFIGURAÇÃO DA PÁGINA ====================
st.set_page_config(
    page_title="AZITech Open Source AI Search Assistant",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== ESTILOS CSS PERSONALIZADOS ====================
st.markdown("""
<style>
    /* Cabeçalho principal */
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        margin-bottom: 2rem;
        text-align: center;
    }
    .main-header h1 {
        margin: 0;
        font-size: 2.5rem;
        font-weight: 700;
    }
    .main-header p {
        margin: 0.5rem 0 0;
        font-size: 1.2rem;
        opacity: 0.95;
    }
    /* Rodapé */
    .footer {
        margin-top: 3rem;
        padding: 1.5rem;
        background-color: #f8f9fa;
        border-radius: 10px;
        text-align: center;
        color: #6c757d;
        border-top: 1px solid #dee2e6;
    }
    .footer a {
        color: #667eea;
        text-decoration: none;
        font-weight: 500;
    }
    .footer a:hover {
        text-decoration: underline;
    }
    /* Cartões de contato na sidebar */
    .contact-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 4px solid #667eea;
    }
    .contact-card h4 {
        margin: 0 0 0.5rem 0;
        color: #333;
    }
    .contact-card p {
        margin: 0.25rem 0;
        color: #666;
    }
    /* Badge de status */
    .status-badge {
        background-color: #28a745;
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        display: inline-block;
        margin-bottom: 1rem;
    }
    /* Títulos das seções */
    .section-title {
        color: #333;
        font-weight: 600;
        margin-bottom: 1.5rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #667eea;
    }
</style>
""", unsafe_allow_html=True)

# ==================== CABEÇALHO PRINCIPAL ====================
st.markdown("""
<div class="main-header">
    <h1>🧠 AZITech Open Source AI Search Assistant</h1>
    <p>Central de Soluções Digitais • SEO Técnico • Desenvolvimento • IA Multi-Provedor</p>
</div>
""", unsafe_allow_html=True)

# ==================== SIDEBAR PROFISSIONAL ====================
with st.sidebar:
    # Logo e título da empresa
    st.markdown("## 🚀 **AZITech**")
    st.markdown("*Central de Soluções Digitais*")
    st.markdown("---")

    # Status online
    st.markdown('<div class="status-badge">🟢 Sistema Online</div>', unsafe_allow_html=True)

    # Chaves dos provedores
    st.markdown("### 🔑 Chaves dos Provedores")
    st.markdown("Insira suas chaves. Quanto mais provedores, mais opções e resiliência.")

    # Inicializa chaves na sessão
    if "api_keys" not in st.session_state:
        st.session_state.api_keys = {}

    groq_key = st.text_input("Groq API Key", type="password", value=st.session_state.api_keys.get("groq", ""))
    fireworks_key = st.text_input("Fireworks API Key", type="password", value=st.session_state.api_keys.get("fireworks", ""))
    together_key = st.text_input("Together API Key", type="password", value=st.session_state.api_keys.get("together", ""))
    replicate_key = st.text_input("Replicate API Token", type="password", value=st.session_state.api_keys.get("replicate", ""))
    vercel_key = st.text_input("Vercel AI Gateway API Key", type="password", value=st.session_state.api_keys.get("vercel", ""))

    if st.button("💾 Salvar Chaves", use_container_width=True):
        st.session_state.api_keys = {
            "groq": groq_key,
            "fireworks": fireworks_key,
            "together": together_key,
            "replicate": replicate_key,
            "vercel": vercel_key,
        }
        st.success("Chaves salvas com sucesso!")

    st.markdown("---")

    # Configuração de provedor/modelo
    st.markdown("### ⚙️ Configuração dos Assistentes")

    if "selected_provider" not in st.session_state:
        st.session_state.selected_provider = "auto"
    if "selected_model" not in st.session_state:
        st.session_state.selected_model = "auto"

    provider_options = ["auto"] + [p for p in MODELS_BY_PROVIDER.keys() if st.session_state.api_keys.get(p)]
    selected_provider = st.selectbox(
        "Provedor (auto = fallback automático)",
        provider_options,
        index=provider_options.index(st.session_state.selected_provider) if st.session_state.selected_provider in provider_options else 0
    )

    model_options = ["auto"]
    if selected_provider != "auto" and selected_provider in MODELS_BY_PROVIDER:
        model_options.extend(MODELS_BY_PROVIDER[selected_provider])

    selected_model = st.selectbox(
        "Modelo (auto = primeiro da lista do provedor)",
        model_options,
        index=model_options.index(st.session_state.selected_model) if st.session_state.selected_model in model_options else 0
    )

    st.session_state.selected_provider = selected_provider
    st.session_state.selected_model = selected_model

    st.markdown("---")

    # Informações de contato
    st.markdown("### 📍 **Teófilo Otoni - MG**")
    st.markdown("""
    <div class="contact-card">
        <h4>📞 Contato</h4>
        <p><strong>Site:</strong> <a href="https://azitech.com.br" target="_blank">azitech.com.br</a></p>
        <p><strong>E-mail:</strong> azitech.oficial@gmail.com</p>
        <p><strong>Redes:</strong> @azi.tech (Instagram, LinkedIn, Twitter)</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.caption("© 2026 AZITech • Open Source AI Search Assistant")

# ==================== MENU PRINCIPAL ====================
st.markdown('<h2 class="section-title">📋 Módulos Disponíveis</h2>', unsafe_allow_html=True)

menu = st.selectbox(
    "Escolha o módulo desejado",
    [
        "Analisador Core (local)",
        "Assistente SEO",
        "Assistente de Código Python",
        "Assistente Rust (Cálculo)",
        "Assistente C++ (Cálculo)",
        "Etimologia"
    ]
)

# ==================== MÓDULO 1: ANALISADOR CORE ====================
if menu == "Analisador Core (local)":
    st.header("📊 Analisador Core (sem IA)")
    st.info("Este módulo funciona **sem necessidade de chaves de API**. Análise local de textos, PDFs e URLs.")

    opcao = st.radio("Tipo de entrada", ["Texto", "PDF", "URL (headings)", "URL (metadados)"], horizontal=True)

    if opcao == "Texto":
        texto = st.text_area("Cole o texto para análise", height=200)
        if st.button("🔍 Analisar texto", use_container_width=True):
            with st.spinner("Analisando..."):
                res = analisador_core.analisar_texto(texto)
            st.json(res)

    elif opcao == "PDF":
        arquivo = st.file_uploader("Envie um arquivo PDF", type=["pdf"])
        if arquivo and st.button("📄 Analisar PDF", use_container_width=True):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                tmp.write(arquivo.read())
                tmp_path = tmp.name
            with st.spinner("Extraindo e analisando..."):
                texto = analisador_core.extrair_texto_pdf(tmp_path)
                res = analisador_core.analisar_texto(texto)
            os.unlink(tmp_path)
            st.json(res)

    elif opcao == "URL (headings)":
        url = st.text_input("URL do site", placeholder="https://exemplo.com")
        if url and st.button("🔗 Extrair headings", use_container_width=True):
            with st.spinner("Buscando..."):
                res = analisador_core.extrair_headings_completos(url)
            st.json(res)

    else:  # metadados
        url = st.text_input("URL do site", placeholder="https://exemplo.com")
        if url and st.button("🔗 Extrair metadados e links", use_container_width=True):
            with st.spinner("Buscando..."):
                res = analisador_core.extrair_metadados_e_links(url)
            st.json(res)

# ==================== MÓDULO 2: ASSISTENTE SEO ====================
elif menu == "Assistente SEO":
    st.header("🔍 Assistente SEO")
    if not any(st.session_state.api_keys.values()):
        st.error("❌ **É necessário inserir pelo menos uma chave de API na barra lateral para usar este módulo.**")
    else:
        if "messages_seo" not in st.session_state:
            st.session_state.messages_seo = [{"role": "system", "content": "Você é um consultor especialista em SEO."}]

        for msg in st.session_state.messages_seo:
            if msg["role"] != "system":
                with st.chat_message(msg["role"]):
                    st.markdown(msg["content"])

        prompt = st.chat_input("Faça sua pergunta sobre SEO...")
        if prompt:
            st.session_state.messages_seo.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                provider = None if st.session_state.selected_provider == "auto" else st.session_state.selected_provider
                model = None if st.session_state.selected_model == "auto" else st.session_state.selected_model
                with st.spinner("Pensando..."):
                    resposta = search_assistant.chat_seo(
                        st.session_state.messages_seo,
                        st.session_state.api_keys,
                        provider=provider,
                        model=model
                    )
                st.markdown(resposta)

            st.session_state.messages_seo.append({"role": "assistant", "content": resposta})

# ==================== MÓDULO 3: CÓDIGO PYTHON ====================
elif menu == "Assistente de Código Python":
    st.header("🐍 Assistente de Código Python (código editável)")
    if not any(st.session_state.api_keys.values()):
        st.error("❌ **É necessário inserir pelo menos uma chave de API na barra lateral para usar este módulo.**")
    else:
        st.markdown("""
        **Descreva o que você quer que o código faça.** Exemplos:
        - *"quero uma função que calcule a média de uma lista de números"*
        - *"quero transforme em código um valor constante 6 que some mais n e divida por m. n é o número de visitantes extras e m é quantidade de kg de carne a cada 2 pessoas."*
        """)

        user_request = st.text_area("Sua solicitação:", height=150)
        if st.button("🚀 Gerar Código", use_container_width=True):
            if user_request.strip():
                provider = None if st.session_state.selected_provider == "auto" else st.session_state.selected_provider
                model = None if st.session_state.selected_model == "auto" else st.session_state.selected_model
                with st.spinner("Gerando código..."):
                    resposta_raw = code_assistant.generate_code(
                        user_request,
                        st.session_state.api_keys,
                        provider=provider,
                        model=model
                    )

                st.markdown("### 📝 Resposta (editável)")
                edited_code = st.text_area("Edite o código gerado se desejar:", resposta_raw, height=400)
                st.code(edited_code, language="python")
            else:
                st.warning("Digite uma solicitação.")

# ==================== MÓDULO 4: RUST CÁLCULO ====================
elif menu == "Assistente Rust (Cálculo)":
    st.header("🦀 Assistente Rust para Cálculos")
    if not any(st.session_state.api_keys.values()):
        st.error("❌ **É necessário inserir pelo menos uma chave de API na barra lateral para usar este módulo.**")
    else:
        st.markdown("""
        **Descreva o problema matemático ou cálculo que você quer resolver em Rust.** Exemplos:
        - *"quero uma função que calcule o fatorial de um número"*
        - *"quero calcular a integral numérica de f(x) = x^2 no intervalo [0,1] usando o método de Simpson"*
        """)

        user_request = st.text_area("Sua solicitação:", height=150)

        col1, col2 = st.columns(2)
        with col1:
            provider_choice = st.selectbox(
                "Provedor (opcional)",
                ["auto"] + [p for p in MODELS_BY_PROVIDER.keys() if st.session_state.api_keys.get(p)],
                key="rust_provider"
            )
        with col2:
            model_choice = st.text_input("Modelo (opcional)", key="rust_model")

        if st.button("🦀 Gerar Código Rust", use_container_width=True):
            if user_request.strip():
                provider = None if provider_choice == "auto" else provider_choice
                model = model_choice.strip() or None

                with st.spinner("Gerando código Rust..."):
                    resposta_raw = rust_calc_assistant.generate_rust_calc(
                        user_request,
                        st.session_state.api_keys,
                        provider=provider,
                        model=model
                    )

                st.markdown("### 📝 Resposta")
                st.markdown(resposta_raw)
            else:
                st.warning("Digite uma solicitação.")

# ==================== MÓDULO 5: C++ CÁLCULO ====================
elif menu == "Assistente C++ (Cálculo)":
    st.header("⚙️ Assistente C++ para Cálculos")
    if not any(st.session_state.api_keys.values()):
        st.error("❌ **É necessário inserir pelo menos uma chave de API na barra lateral para usar este módulo.**")
    else:
        st.markdown("""
        **Descreva o problema matemático ou cálculo que você quer resolver em C++.** Exemplos:
        - *"quero uma função que calcule a raiz quadrada usando o método de Newton"*
        - *"quero calcular o produto escalar de dois vetores"*
        """)

        user_request = st.text_area("Sua solicitação:", height=150)

        col1, col2 = st.columns(2)
        with col1:
            provider_choice = st.selectbox(
                "Provedor (opcional)",
                ["auto"] + [p for p in MODELS_BY_PROVIDER.keys() if st.session_state.api_keys.get(p)],
                key="cpp_provider"
            )
        with col2:
            model_choice = st.text_input("Modelo (opcional)", key="cpp_model")

        if st.button("⚙️ Gerar Código C++", use_container_width=True):
            if user_request.strip():
                provider = None if provider_choice == "auto" else provider_choice
                model = model_choice.strip() or None

                with st.spinner("Gerando código C++..."):
                    resposta_raw = cpp_calc_assistant.generate_cpp_calc(
                        user_request,
                        st.session_state.api_keys,
                        provider=provider,
                        model=model
                    )

                st.markdown("### 📝 Resposta")
                st.markdown(resposta_raw)
            else:
                st.warning("Digite uma solicitação.")

# ==================== MÓDULO 6: ETIMOLOGIA ====================
elif menu == "Etimologia":
    st.header("📖 Consulta Etimológica")
    if not any(st.session_state.api_keys.values()):
        st.error("❌ **É necessário inserir pelo menos uma chave de API na barra lateral para usar este módulo.**")
    else:
        st.markdown("""
        **Descubra a origem das palavras em latim, grego, sânscrito, hebraico e outras línguas.** Exemplos:
        - filosofia
        - karma
        - sábado
        - alfabeto
        - cavalo
        - amor
        - direito
        """)

        palavra = st.text_input("Digite uma palavra:", placeholder="Ex: filosofia")

        col1, col2 = st.columns(2)
        with col1:
            provider_choice = st.selectbox(
                "Provedor (opcional)",
                ["auto"] + [p for p in MODELS_BY_PROVIDER.keys() if st.session_state.api_keys.get(p)],
                key="etimologia_provider"
            )
        with col2:
            model_choice = st.text_input("Modelo (opcional)", key="etimologia_model")

        if st.button("📜 Consultar Etimologia", use_container_width=True):
            if palavra.strip():
                provider = None if provider_choice == "auto" else provider_choice
                model = model_choice.strip() or None

                with st.spinner("Consultando origens..."):
                    resposta = etimologia.consultar_etimologia(
                        palavra.strip(),
                        st.session_state.api_keys,
                        provider=provider,
                        model=model
                    )

                st.markdown("### 📜 Resultado")
                st.markdown(resposta)
            else:
                st.warning("Digite uma palavra.")

# ==================== RODAPÉ ====================
st.markdown("""
<div class="footer">
    <p><strong>AZITech Open Source AI Search Assistant</strong> — desenvolvido por <a href="https://azitech.com.br" target="_blank">Gustavo Nogueira, CEO da AZITech</a></p>
    <p>📍 Teófilo Otoni - MG • 📧 azitech.oficial@gmail.com • 🌐 <a href="https://azitech.com.br" target="_blank">azitech.com.br</a></p>
    <p>📱 Redes: @azi.tech (Instagram, LinkedIn, Twitter)</p>
    <p style="margin-top:1rem; font-size:0.9rem;">© 2026 AZITech — Central de Soluções Digitais. Open Source AI Search Assistant.</p>
</div>
""", unsafe_allow_html=True)

