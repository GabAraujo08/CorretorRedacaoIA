from flask import Flask, render_template, request
import requests
import json
import os

app = Flask(__name__)
app.config['TEMPLATE_FOLDER'] = os.path.join(os.getcwd(), 'api/templates')

API_KEY = "#" #Coloque sua chave de API aqui
OPENAI_LINK = "https://api.openai.com/v1/chat/completions"
ID_MODELO = "gpt-3.5-turbo"

import requests

def get_openai_response(content):
    """
    Get a response from the OpenAI API.

    Args:
        content (str): The content of the message to send to the API.

    Returns:
        dict: The JSON response from the API.

    Raises:
        requests.exceptions.RequestException: If an error occurred while making the request.
        ValueError: If the response does not contain the expected data.
    """
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    body = {
        "model": ID_MODELO,
        "messages": [{"role": "system", "content": content}]
    }

    response = requests.post(OPENAI_LINK, headers=headers, json=body)

    if response.status_code != 200:
        raise ValueError(f"Request to OpenAI API failed with status code {response.status_code}: {response.text}")

    response_json = response.json()

    if 'choices' not in response_json:
        raise ValueError(f"Unexpected response format: {response_json}")

    return response_json

    """
    Get a response from the OpenAI API.

    Args:
        content (str): The content of the message to send to the API.

    Returns:
        dict: The JSON response from the API.

    Raises:
        requests.exceptions.RequestException: If an error occurred while making the request.
    """
    # Set the headers for the request
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    # Create the request body
    body = {
        "model": ID_MODELO,
        "messages": [{"role": "system", "content": content}]
    }

    # Send the request to the OpenAI API
    response = requests.post(OPENAI_LINK, headers=headers, json=body)

    # Return the JSON response
    return response.json()

def correcao_redacao(tema: str, redacao: str) -> str:
    """
    This function takes a theme and an essay as input and returns a formatted correction response.

    Args:
        tema (str): The theme of the essay.
        redacao (str): The essay content.

    Returns:
        str: The formatted correction response.
    """
    correcao_content = (
        f"Aja como um corretor de redações do ENEM, avalie segundo as competências do Enem "
        f"e detalhe como foi o desempenho do candidato em cada competência, ao final atribua "
        f"sua pontuação a redação, identifique também os pontos importantes da redação, tais "
        f"como a tese da redação, os argumentos, a proposta de intervenção, veja se eles são "
        f"coerentes e embasados e faça sua atribuição quanto a isso, seja ela positiva ou negativa. "
        f"Tema: {tema} Redação: {redacao}"
    )

    try:
        correcao_response = get_openai_response(correcao_content)
        resposta = correcao_response["choices"][0]["message"]["content"]
        resposta_formatada = "<br>".join(resposta.strip().split("\n"))
    except ValueError as e:
        resposta_formatada = f"Erro ao obter resposta da API: {e}"
    except KeyError as e:
        resposta_formatada = f"Erro no formato da resposta da API: {e}"

    return resposta_formatada

    """
    This function takes a theme and an essay as input and returns a formatted correction response.

    Args:
        tema (str): The theme of the essay.
        redacao (str): The essay content.

    Returns:
        str: The formatted correction response.
    """
    # Create the correction content by formatting the theme and essay
    correcao_content = (
        f"Aja como um corretor de redações do ENEM, avalie segundo as competências do Enem "
        f"e detalhe como foi o desempenho do candidato em cada competência, ao final atribua "
        f"sua pontuação a redação, identifique também os pontos importantes da redação, tais "
        f"como a tese da redação, os argumentos, a proposta de intervenção, veja se eles são "
        f"coerentes e embasados e faça sua atribuição quanto a isso, seja ela positiva ou negativa. "
        f"Tema: {tema} Redação: {redacao}"
    )

    # Get the correction response from OpenAI API
    correcao_response = get_openai_response(correcao_content)

    # Extract the message content from the response
    resposta = correcao_response["choices"][0]["message"]["content"]

    # Format the response with line breaks
    resposta_formatada = "<br>".join(resposta.strip().split("\n"))

    return resposta_formatada

def redacao_chat(tema, redacao):
    content = f"Reescreva essa redação da forma que você julgar mais adequada seguindo os preceitos de correção da redação do ENEM. Tema: {tema} Redação: {redacao}"
    
    try:
        response = get_openai_response(content)
        return response['choices'][0]['message']['content']
    except ValueError as e:
        return f"Erro ao obter resposta da API: {e}"
    except KeyError as e:
        return f"Erro no formato da resposta da API: {e}"

    content = f"Reescreva essa redação da forma que você julgar mais adequada seguindo os preceitos de correção da redação do ENEM. Tema: {tema} Redação: {redacao}"
    response = get_openai_response(content)
    return response['choices'][0]['message']['content']
    

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        tema_redacao = request.form['temaRedacao']
        redacao = request.form['redacao']

        correcao_api = correcao_redacao(tema_redacao, redacao)
        redacao_chat_api = redacao_chat(tema_redacao, redacao)

        return render_template('resposta.html',
                               correcao=correcao_api,
                               redacaoChat=redacao_chat_api,
                               redacao=redacao)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
