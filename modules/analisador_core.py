# -*- coding: utf-8 -*-
"""
ANALISADOR MULTIFUNCIONAL
Opções:
1. Análise de texto (sentimento, keywords, etc.)
2. Análise de PDF (extrai texto e analisa)
3. Extrair todas as tags de heading (H1 a H6) de uma URL (com contagem)
4. Extrair metadados e links de uma URL (sem limites)
5. Sair
"""

import re
import math
import os
from collections import Counter

# ==================== BIBLIOTECAS OPCIONAIS ====================
try:
    import PyPDF2
    PDF_SUPPORT = True
except ImportError:
    PDF_SUPPORT = False

try:
    import requests
    from bs4 import BeautifulSoup
    WEB_SUPPORT = True
except ImportError:
    WEB_SUPPORT = False

# ==================== CONSTANTES DE ANÁLISE DE TEXTO ====================
MAX_CHARS = 500000

COMMON_WORDS = {
    "o", "a", "os", "as", "um", "uma", "uns", "umas",
    "de", "do", "da", "dos", "das", "em", "no", "na",
    "nos", "nas", "por", "para", "com", "sem", "sob",
    "sobre", "entre", "que", "e", "ou", "mas", "se",
    "porque", "como", "quando", "onde", "qual", "quais",
    "este", "esta", "esse", "essa", "aquele", "aquela",
    "isto", "isso", "aquilo", "meu", "minha", "seu", "sua",
    "nosso", "nossa", "deles", "delas", "já", "ainda", "agora",
    "depois", "antes", "sempre", "nunca", "aqui", "ali", "lá",
}

COMMON_ERRORS = {
    "concerteza": "com certeza", "menas": "menos", "fazem": "faz",
    "houveram": "houve", "imformação": "informação", "advinhar": "adivinhar",
    "envia-lo": "enviá-lo", "provalvelmente": "provavelmente", "excessão": "exceção",
    "entregar-mos": "entregarmos", "a gente": "nós", "pra": "para",
}

AI_INDICATORS = [
    "além disso", "dessa forma", "por outro lado", "é importante destacar",
    "vale ressaltar", "convém mencionar", "nesse contexto", "de acordo com",
    "como mencionado", "conforme visto", "em suma", "portanto",
    "entretanto", "contudo", "todavia", "assim sendo",
    "deste modo", "em outras palavras", "ou seja", "isto é",
    "podemos observar", "nota-se que", "é fundamental", "é crucial",
]

POSITIVE_WORDS = {
    "bom", "boa", "ótimo", "excelente", "maravilhoso", "incrível",
    "gosto", "amo", "adoro", "feliz", "alegre", "contento",
    "sucesso", "vitória", "conquista", "progresso", "evolução",
    "bonito", "lindo", "perfeito", "ideal", "fantástico", "espetacular",
    "magnífico", "adorável", "abençoado", "gratidão", "obrigado",
    "prazer", "divertido", "emocionante", "inesquecível",
}

NEGATIVE_WORDS = {
    "ruim", "péssimo", "horrível", "terrível", "ódio", "detesto",
    "triste", "deprimido", "angustiado", "preocupado", "medo",
    "fracasso", "derrota", "problema", "dificuldade", "erro",
    "feio", "horroroso", "desastre", "catástrofe", "pior",
    "lamentável", "nojento", "repugnante", "raiva", "inveja",
    "ciúmes", "dor", "sofrimento", "chateado", "aborrecido", "cansado",
}

# ==================== FUNÇÕES DE ANÁLISE DE TEXTO ====================

def extrair_palavras(texto):
    texto_limpo = re.sub(r'[^a-zA-Záéíóúâêîôûãõç\s]', ' ', texto.lower())
    return texto_limpo.split()

def analisar_palavras_chave(palavras):
    total = len(palavras)
    if total == 0:
        return []
    freq = Counter(palavras)
    palavras_filtradas = {p: c for p, c in freq.items() if len(p) > 3 and p not in COMMON_WORDS}
    densidades = [(p, (c / total) * 100) for p, c in palavras_filtradas.items()]
    densidades = [(p, d) for p, d in densidades if d > 1.0]
    densidades.sort(key=lambda x: x[1], reverse=True)
    return densidades[:10]

def palavras_repetidas(palavras):
    freq = Counter(palavras)
    palavras_filtradas = {p: c for p, c in freq.items() if len(p) > 3 and p not in COMMON_WORDS}
    ordenadas = sorted(palavras_filtradas.items(), key=lambda x: x[1], reverse=True)
    return ordenadas[:10]

def verificar_erros_ortograficos(palavras):
    erros = []
    for palavra in palavras:
        if palavra in COMMON_ERRORS:
            erros.append(f"'{palavra}' → '{COMMON_ERRORS[palavra]}'")
    return erros

def detectar_ia(texto, palavras):
    texto_lower = texto.lower()
    score = 0.0
    matches = 0
    for ind in AI_INDICATORS:
        if ind in texto_lower:
            matches += 1
    if AI_INDICATORS:
        score += (matches / len(AI_INDICATORS)) * 50
    sentencas = re.split(r'[.!?]', texto)
    if len(sentencas) > 2:
        comprimento_medio = len(texto) / len(sentencas)
        if comprimento_medio > 120:
            score += 15
    rep_count = len([p for p, c in Counter(palavras).items() if c > 5])
    if rep_count > 5:
        score += 10
    formais = ["portanto", "entretanto", "contudo", "todavia"]
    for f in formais:
        if f in texto_lower:
            score += 5
    return min(score, 100.0)

def calcular_legibilidade(texto, num_palavras):
    if num_palavras == 0:
        return 0.0
    sentencas = [s for s in re.split(r'[.!?]', texto) if s.strip()]
    num_sentencas = max(len(sentencas), 1)
    comprimento_medio_frase = num_palavras / num_sentencas
    palavras_longas = sum(1 for p in texto.split() if len(p) > 6)
    proporcao_longas = palavras_longas / num_palavras
    score = 100.0
    if comprimento_medio_frase > 25:
        score -= (comprimento_medio_frase - 25) * 2
    if proporcao_longas > 0.2:
        score -= (proporcao_longas - 0.2) * 100
    if 15 <= comprimento_medio_frase <= 20:
        score += 10
    return max(0, min(100, score))

def analisar_sentimento(texto):
    palavras = texto.lower().split()
    pos = neg = total = 0
    for p in palavras:
        p_clean = re.sub(r'[^a-záéíóúâêîôãç]', '', p)
        if p_clean in POSITIVE_WORDS:
            pos += 1
            total += 1
        elif p_clean in NEGATIVE_WORDS:
            neg += 1
            total += 1
    if total == 0:
        return 50.0
    return (pos / total) * 100

def gerar_resumo(texto, keywords):
    sentencas = re.split(r'[.!?]', texto)
    sentencas = [s.strip() for s in sentencas if s.strip()]
    if not sentencas:
        return "Texto muito curto para resumo."
    melhor_frase = sentencas[0]
    melhor_score = 0
    for frase in sentencas:
        palavras_frase = set(re.findall(r'\b[a-z]+\b', frase.lower()))
        score = sum(1 for kw, _ in keywords if kw in palavras_frase)
        if score > melhor_score:
            melhor_score = score
            melhor_frase = frase
    if len(melhor_frase) > 150:
        melhor_frase = melhor_frase[:147] + "..."
    return melhor_frase

def analisar_texto(texto):
    palavras = extrair_palavras(texto)
    num_palavras = len(palavras)
    num_caracteres = len(texto)
    keywords = analisar_palavras_chave(palavras)
    repetidas = palavras_repetidas(palavras)
    erros = verificar_erros_ortograficos(palavras)
    ia_prob = detectar_ia(texto, palavras)
    legibilidade = calcular_legibilidade(texto, num_palavras)
    sentimento = analisar_sentimento(texto)
    resumo = gerar_resumo(texto, keywords)
    return {
        'palavras': num_palavras,
        'caracteres': num_caracteres,
        'keywords': keywords,
        'repetidas': repetidas,
        'erros': erros,
        'ia_prob': ia_prob,
        'legibilidade': legibilidade,
        'sentimento': sentimento,
        'resumo': resumo
    }

def exibir_analise_texto(analise):
    print("\n📊 RESULTADOS DA ANÁLISE")
    print("─" * 40)
    print("📝 Estatísticas Básicas:")
    print(f"   • Palavras: {analise['palavras']}")
    print(f"   • Caracteres: {analise['caracteres']}")
    print("\n🎯 Palavras-chave Principais:")
    if not analise['keywords']:
        print("   Nenhuma palavra-chave significativa encontrada")
    else:
        for i, (kw, dens) in enumerate(analise['keywords'][:5], 1):
            print(f"   {i}. {kw} ({dens:.1f}%)")
    print("\n🔁 Palavras mais repetidas:")
    if not analise['repetidas']:
        print("   Nenhuma repetição significativa")
    else:
        for palavra, contagem in analise['repetidas'][:5]:
            print(f"   • {palavra}: {contagem} vezes")
    print("\n🔍 Qualidade do Texto:")
    print(f"   • Legibilidade: {analise['legibilidade']:.1f}%")
    if analise['legibilidade'] < 50:
        print("     ⚠️  Difícil de entender")
    elif analise['legibilidade'] < 70:
        print("     ✅ Nível moderado")
    elif analise['legibilidade'] < 85:
        print("     ✅ Bom entendimento")
    else:
        print("     🎉 Excelente clareza")
    print("\n😊 Análise de Sentimento:")
    print(f"   • Score: {analise['sentimento']:.1f}%")
    if analise['sentimento'] < 30:
        print("     😞 Negativo")
    elif analise['sentimento'] < 45:
        print("     😐 Levemente negativo")
    elif analise['sentimento'] < 56:
        print("     😐 Neutro")
    elif analise['sentimento'] < 71:
        print("     🙂 Levemente positivo")
    else:
        print("     😊 Positivo")
    print("\n🤖 Detecção de IA:")
    print(f"   • Probabilidade: {analise['ia_prob']:.1f}%")
    if analise['ia_prob'] <= 30:
        print("     👤 Provavelmente humano")
    elif analise['ia_prob'] <= 60:
        print("     🤔 Inconclusivo")
    elif analise['ia_prob'] <= 80:
        print("     ⚠️  Possível IA")
    else:
        print("     🤖 Provavelmente IA")
    print("\n✏️  Erros Ortográficos:")
    if not analise['erros']:
        print("   ✅ Nenhum erro comum detectado")
    else:
        for erro in analise['erros']:
            print(f"   • {erro}")
    print("\n📋 Resumo:")
    print(f"   \"{analise['resumo']}\"")

# ==================== FUNÇÕES DE PDF ====================

def extrair_texto_pdf(caminho):
    if not PDF_SUPPORT:
        return None
    try:
        with open(caminho, 'rb') as arquivo:
            leitor = PyPDF2.PdfReader(arquivo)
            texto = ''
            for pagina in leitor.pages:
                texto += pagina.extract_text() + '\n'
            return texto
    except Exception as e:
        print(f"❌ Erro ao ler PDF: {e}")
        return None

# ==================== FUNÇÕES DE WEB (HEADINGS) ====================

def extrair_headings_completos(url):
    """
    Extrai todas as tags de heading de H1 a H6 de uma URL e retorna um dicionário
    com a contagem e a lista de cada heading (sem truncamento).
    """
    if not WEB_SUPPORT:
        print("❌ Suporte web não disponível. Instale requests e beautifulsoup4.")
        return None
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        resposta = requests.get(url, timeout=10, headers=headers)
        if resposta.status_code != 200:
            print(f"❌ Erro HTTP {resposta.status_code}")
            return None
        soup = BeautifulSoup(resposta.text, 'html.parser')
        
        headings = {}
        for nivel in range(1, 7):
            tag = f'h{nivel}'
            elementos = soup.find_all(tag)
            textos = [el.get_text(strip=True) for el in elementos if el.get_text(strip=True)]
            headings[f'H{nivel}'] = {
                'quantidade': len(textos),
                'textos': textos
            }
        
        titulo = soup.title.string.strip() if soup.title else 'Sem título'
        
        return {
            'url': url,
            'titulo': titulo,
            'headings': headings
        }
    except Exception as e:
        print(f"❌ Erro na requisição: {e}")
        return None

def exibir_headings_completos(dados):
    print("\n🌐 HEADINGS DA PÁGINA (H1 a H6)")
    print("─" * 60)
    print(f"URL: {dados['url']}")
    print(f"Título: {dados['titulo']}\n")
    
    for nivel in range(1, 7):
        key = f'H{nivel}'
        info = dados['headings'][key]
        print(f"{key}: {info['quantidade']} ocorrência(s)")
        if info['textos']:
            for i, texto in enumerate(info['textos'], 1):
                print(f"   {i}. {texto}")  # sem truncamento
        else:
            print("   (nenhum)")
        print()

# ==================== FUNÇÕES DE WEB (METADADOS E LINKS) ====================

def extrair_metadados_e_links(url):
    """
    Extrai metadados comuns e todos os links (internos, externos, especiais) de uma URL.
    """
    if not WEB_SUPPORT:
        print("❌ Suporte web não disponível. Instale requests e beautifulsoup4.")
        return None
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        resposta = requests.get(url, timeout=10, headers=headers)
        if resposta.status_code != 200:
            print(f"❌ Erro HTTP {resposta.status_code}")
            return None
        soup = BeautifulSoup(resposta.text, 'html.parser')
        
        # Metadados
        metadados = {
            'title': soup.title.string.strip() if soup.title else None,
            'description': None,
            'keywords': None,
            'author': None,
            'viewport': None,
            'robots': None,
            'og:title': None,
            'og:description': None,
            'og:image': None,
            'twitter:card': None,
            'canonical': None,
            'language': None,
            'charset': None,
        }
        
        for meta in soup.find_all('meta'):
            name = meta.get('name', '').lower()
            prop = meta.get('property', '').lower()
            content = meta.get('content', '')
            if name == 'description':
                metadados['description'] = content
            elif name == 'keywords':
                metadados['keywords'] = content
            elif name == 'author':
                metadados['author'] = content
            elif name == 'viewport':
                metadados['viewport'] = content
            elif name == 'robots':
                metadados['robots'] = content
            elif prop == 'og:title':
                metadados['og:title'] = content
            elif prop == 'og:description':
                metadados['og:description'] = content
            elif prop == 'og:image':
                metadados['og:image'] = content
            elif prop == 'twitter:card':
                metadados['twitter:card'] = content
        
        canonical = soup.find('link', rel='canonical')
        if canonical and canonical.get('href'):
            metadados['canonical'] = canonical['href']
        
        html = soup.find('html')
        if html and html.get('lang'):
            metadados['language'] = html['lang']
        
        charset = soup.find('meta', charset=True)
        if charset and charset.get('charset'):
            metadados['charset'] = charset['charset']
        
        # Extração de links (sem limites)
        links = {
            'internos': [],
            'externos': [],
            'especiais': []
        }
        
        dominio_base = re.match(r'https?://([^/]+)', url).group(1) if url else ''
        
        for a in soup.find_all('a', href=True):
            href = a['href'].strip()
            texto = a.get_text(strip=True) or '[sem texto]'
            if href.startswith(('http://', 'https://')):
                if dominio_base in href:
                    links['internos'].append({'url': href, 'texto': texto})
                else:
                    links['externos'].append({'url': href, 'texto': texto})
            elif href.startswith('/') or href.startswith('?'):
                links['internos'].append({'url': href, 'texto': texto})
            elif href.startswith(('mailto:', 'tel:', 'javascript:')):
                links['especiais'].append({'url': href, 'texto': texto})
            else:
                links['internos'].append({'url': href, 'texto': texto})
        
        return {
            'url': url,
            'metadados': metadados,
            'links': links,
            'total_links': len(links['internos']) + len(links['externos']) + len(links['especiais'])
        }
    except Exception as e:
        print(f"❌ Erro na requisição: {e}")
        return None

def exibir_metadados_e_links(dados):
    print("\n🌐 METADADOS E LINKS DA PÁGINA")
    print("─" * 60)
    print(f"URL: {dados['url']}\n")
    
    print("📋 METADADOS:")
    m = dados['metadados']
    for chave, valor in m.items():
        if valor:
            print(f"   {chave}: {valor}")
    
    print("\n🔗 LINKS:")
    print(f"Total de links encontrados: {dados['total_links']}")
    
    if dados['links']['internos']:
        print(f"\n   ▶ Internos ({len(dados['links']['internos'])}):")
        for i, link in enumerate(dados['links']['internos'], 1):
            print(f"      {i}. {link['texto']} -> {link['url']}")
    
    if dados['links']['externos']:
        print(f"\n   ▶ Externos ({len(dados['links']['externos'])}):")
        for i, link in enumerate(dados['links']['externos'], 1):
            print(f"      {i}. {link['texto']} -> {link['url']}")
    
    if dados['links']['especiais']:
        print(f"\n   ▶ Especiais ({len(dados['links']['especiais'])}):")
        for i, link in enumerate(dados['links']['especiais'], 1):
            print(f"      {i}. {link['texto']} -> {link['url']}")

# ==================== MENU PRINCIPAL ====================

def menu():
    print("=" * 60)
    print("           ANALISADOR MULTIFUNCIONAL")
    print("=" * 60)
    print("1. Analisar texto (sentimento, keywords, etc.)")
    print("2. Analisar PDF (extrai texto e analisa)")
    print("3. Extrair headings completos (H1 a H6) de uma URL")
    print("4. Extrair metadados e links de uma URL (sem limites)")
    print("5. Sair")
    print("-" * 60)
    opcao = input("Escolha uma opção (1-5): ").strip()
    return opcao

def main():
    while True:
        opcao = menu()
        if opcao == '5':
            print("👋 Encerrando...")
            break

        elif opcao == '1':
            print("\nDigite ou cole o texto para análise:")
            print("─" * 40)
            texto = input().strip()
            if not texto:
                print("❌ Texto vazio.")
                continue
            if len(texto) > MAX_CHARS:
                print(f"⚠️  Texto muito longo. Analisando primeiros {MAX_CHARS} caracteres.")
                texto = texto[:MAX_CHARS]
            analise = analisar_texto(texto)
            exibir_analise_texto(analise)

        elif opcao == '2':
            if not PDF_SUPPORT:
                print("❌ Suporte a PDF não disponível. Instale PyPDF2.")
                continue
            caminho = input("Caminho do arquivo PDF: ").strip().strip('"').strip("'")
            if not os.path.exists(caminho):
                print("❌ Arquivo não encontrado.")
                continue
            print("\n🔄 Extraindo texto do PDF...")
            texto = extrair_texto_pdf(caminho)
            if texto is None:
                continue
            print(f"✅ Texto extraído: {len(texto)} caracteres.")
            if len(texto) > MAX_CHARS:
                print(f"⚠️  Texto muito longo. Analisando primeiros {MAX_CHARS} caracteres.")
                texto = texto[:MAX_CHARS]
            analise = analisar_texto(texto)
            exibir_analise_texto(analise)

        elif opcao == '3':
            if not WEB_SUPPORT:
                print("❌ Suporte web não disponível. Instale requests e beautifulsoup4.")
                continue
            url = input("URL: ").strip()
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
            print("\n🔄 Buscando página...")
            dados = extrair_headings_completos(url)
            if dados:
                exibir_headings_completos(dados)

        elif opcao == '4':
            if not WEB_SUPPORT:
                print("❌ Suporte web não disponível. Instale requests e beautifulsoup4.")
                continue
            url = input("URL: ").strip()
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
            print("\n🔄 Buscando página...")
            dados = extrair_metadados_e_links(url)
            if dados:
                exibir_metadados_e_links(dados)

        else:
            print("❌ Opção inválida.")

        input("\nPressione Enter para continuar...")

if __name__ == "__main__":
    main()

    