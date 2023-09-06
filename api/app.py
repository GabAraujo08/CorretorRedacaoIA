from flask import Flask, render_template, request
import requests
import json
import os

app = Flask(__name__)
app.config['TEMPLATE_FOLDER'] = os.path.join(os.getcwd(), 'api/templates')

API_KEY = "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"
OPENAI_LINK = "https://api.openai.com/v1/chat/completions"
ID_MODELO = "gpt-3.5-turbo"

def get_openai_response(content):
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    body = {
        "model": ID_MODELO,
        "messages": [{"role": "system", "content": content}]
    }
    response = requests.post(OPENAI_LINK, headers=headers, json=body)
    return response.json()

def correcao_redacao(tema, redacao):
    correcao_content = f"""Aja como um corretor de redações do ENEM, avalie segundo as competências do Enem e detalhe como foi o desempenho do candidato em cada competência, ao final atribua sua pontuação a redação, identifique também os pontos importantes da redação, tais como a tese da redação, os argumentos, a proposta de intervenção, veja se eles são coerentes e embasados e faça sua atribuição quanto a isso, seja ela positiva ou negativa. Tema: {tema} Redação: {redacao}"""
    correcao_response = get_openai_response(correcao_content)

    # Processar a resposta dividindo em linhas
    resposta = correcao_response['choices'][0]['message']['content']
    linhas = resposta.strip().split('\n')

    # Formatando as linhas para o HTML
    resposta_formatada = '<br>'.join(linhas)

    return resposta_formatada

def redacao_chat(tema, redacao):
    redacao_chat_content = f"""Reescreva essa redação da forma que você julgar mais adequada seguindo os preceitos de correção da redação do ENEM. Tema: {tema} Redação: {redacao}"""
    redacao_chat_response = get_openai_response(redacao_chat_content)
    return redacao_chat_response['choices'][0]['message']['content']

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        tema_redacao = request.form['temaRedacao']
        redacao = request.form['redacao']

        correcao_api = correcao_redacao(tema_redacao, redacao)
        redacao_chat_api = redacao_chat(tema_redacao, redacao)

        return render_template('resposta.html', correcao=correcao_api, redacaoChat=redacao_chat_api, redacao=redacao)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
