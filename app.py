import os
import openai  # A importação permanece a mesma
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Inicializa a chave da API
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

# Texto fixo que será sempre incluído
texto_fixo = """Analise o dataset a seguir e me responda as seguintes informações: 
1. Quem é o cliente? Formato de retorno: Cliente: nome da pessoa
2. O orçamento é referente a qual obra/lugar? Formato de retorno: Obra: nome da obra
3. O orçamento é em qual lugar? Formato de retorno: Lugar: localização
4. A arquitetura/projeto arquitetonico foi realizado por quem? Formato de retorno: Arquiteto: nome do arquiteto/empresa de arquitetura
5. Quais as formas de pagamento? 
6. Detalhe resumidamente as atividades orçadas com seus respectivos valores em Reais (Brasil), separados por linhas. 
7. Qual o valor total dos serviços descritos?. Formato de retorno: Valor total do orçamento: valor total
Observações: 
1. Caso a informação não for encontrada, retorne 'Informação não foi encontrada'. 
2. Retorne os valores monetarios no padrao R$000.000.000,00
3. Não retorne o numero de indice da pergunta na resposta.
4. Corrija gramaticamente
Retorne as respostas separadas por linhas. 
Dataset: 
"""

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
        # Requisição usando o método correto da API
        response = openai.ChatCompletion.create(
            model="gpt-4",  # Modelo desejado
            messages=[
                {"role": "user", "content": texto_completo}
            ]
        )

        # Acessando a resposta corretamente
        texto_processado = response['choices'][0]['message']['content'].strip()
        print(texto_processado)

        # Retorna o texto processado como resposta
        return jsonify({"mensagem": "Texto processado com sucesso!", "texto_corrigido": texto_processado})

    except Exception as e:
        print(f"Erro ao processar a requisição: {e}")
        return jsonify({"error": f"Erro ao processar a requisição: {e}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)
