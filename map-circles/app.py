from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_circle', methods=['POST'])
def process_circle():
    data = request.json
    lat = data['lat']
    lng = data['lng']
    radius = data['radius']

    # Para agora, vamos apenas imprimir e retornar uma mensagem simples
    print(f"Recebido: Latitude: {lat}, Longitude: {lng}, Raio: {radius}")
    return jsonify({'status': 'success', 'message': 'Dados recebidos com sucesso!'})

if __name__ == '__main__':
    app.run(debug=True)
