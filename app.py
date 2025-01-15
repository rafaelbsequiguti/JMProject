import os
from openai import OpenAI
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Inicializa o cliente OpenAI
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

app = Flask(__name__)

# Texto fixo que será sempre incluído
texto_fixo = "Analise o dataset a seguir e me responda as seguintes informações: \n 1. Quem é o cliente?  \n 2. O orçamento é referente a qual obra/lugar? \n 3. A arquitetura/projeto arquitetonico foi realizado por quem? \n 4. Quais as formas de pagamento? \n 5. Detalhe resumidamente as atividades orçadas com seus respectivos valores em Reais brasileiros, separados por linhas. \n 6. Qual o valor total dos serviços descritos? \n Observações: 1. Caso a informação não for encontrada, retorne 'Informação não foi encontrada'. \n Retorne as respostas separadas por linhas. \n Dataset: \n"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/processar', methods=['POST'])
def processar():
    texto_usuario = request.form.get('texto')
    
    if not texto_usuario:
        return jsonify({"error": "Texto do orçamento é obrigatório"}), 400
    
    # Concatenando o texto fixo com o texto do usuário
    texto_completo = texto_fixo + "\n" + texto_usuario

    print(texto_completo)
    
    try:
        # Envia a requisição para a OpenAI usando o novo cliente
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "user", "content": texto_completo}
            ],
            model="gpt-4"  # Modelo desejado (por exemplo, gpt-4)
        )

        # Convertendo o objeto para dicionário e acessando os dados
        chat_completion_dict = chat_completion.to_dict()

        # Acessando a resposta corretamente
        texto_processado = chat_completion_dict['choices'][0]['message']['content'].strip()
        print(texto_processado)

        # Retorna o texto processado como resposta
        return jsonify({"mensagem": "Texto processado com sucesso!", "texto_corrigido": texto_processado})

    except Exception as e:
        print(f"Erro ao processar a requisição: {e}")
        return jsonify({"error": f"Erro ao processar a requisição: {e}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)

