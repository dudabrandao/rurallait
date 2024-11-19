from flask import Flask, jsonify, request
from fireBase import Firebase
from fpdf import FPDF
import os
from datetime import datetime

app = Flask(__name__)
db = Firebase()

@app.route('/', methods=['GET'])
def home():
    return "AAAAA"

@app.route('/getConfig', methods=['POST'])
def getConfig():
    uid = request.json.get('id')
    result = db.getConfig(uid)
    return jsonify({'status': 'success', 'data': result})

@app.route('/postSensor', methods=['POST'])
def postSensor():
    uid = request.json.get('id')
    data = request.json.get('data')
    if db.auth(uid):
        db.insertSensor(uid, data)
        return jsonify({'status': 'success', 'data': data})
    else:
        return jsonify({'status': 'error', 'message': 'Invalid user'})

# Diretório para salvar PDFs
PDF_DIR = 'static/pdfs'
os.makedirs(PDF_DIR, exist_ok=True)

@app.route('/gerar-relatorio/<int:id>', methods=['POST'])
def gerar_relatorio(id):
    # Simulação de dados do banco
    info = buscar_informacoes_no_banco(id)
    if not info:
        return jsonify({'error': 'Informações não encontradas.'}), 404

    # Gera o nome do arquivo PDF
    timestamp = datetime.now().strftime("%d-%m-%Y")
    pdf_filename = f"{id}-relatorio-{timestamp}.pdf"
    pdf_path = os.path.join(PDF_DIR, pdf_filename)

    # Criação do PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Relatório para ID: {id}", ln=True)
    pdf.cell(200, 10, txt=f"Informações: {info}", ln=True)
    pdf.output(pdf_path)

    # Retorna o link do PDF
    return jsonify({'link': f'static/pdfs/{pdf_filename}'})

def buscar_informacoes_no_banco(id):
    # Simulação de dados do banco
    dados = {
        1: "Dados do usuário 1",
        2: "Dados do usuário 2",
        3: "Dados do usuário 3"
    }
    return dados.get(id)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)
