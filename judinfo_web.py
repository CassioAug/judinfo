from flask import Flask, render_template, request, jsonify
from judinfo_cli import DataJudSimple, get_all_courts_categorized

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/courts')
def courts():
    return jsonify(get_all_courts_categorized())

@app.route('/search', methods=['POST'])
def search():
    data = request.get_json()
    numero = data.get('numero')
    tribunais = data.get('tribunais')

    client = DataJudSimple()
    resultados = []

    for tribunal in tribunais:
        resultado = client.consultar_processo(numero, tribunal)
        if resultado:
            resultados.append(resultado)

    return jsonify(resultados)

@app.route('/status', methods=['POST'])
def status():
    data = request.get_json()
    tribunais = data.get('tribunais')

    client = DataJudSimple()
    resultados = {}

    for tribunal in tribunais:
        resultado = client.verificar_tribunal(tribunal)
        resultados[tribunal] = resultado

    return jsonify(resultados)

if __name__ == '__main__':
    app.run()
