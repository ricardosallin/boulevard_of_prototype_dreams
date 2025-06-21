from flask import Flask, request, jsonify
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

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

    # Criar o ponto central do círculo
    center = Point(lng, lat)

    # Simular o cálculo de população dentro do círculo (faremos algo mais complexo depois)
    # Por enquanto, apenas estimamos a população com base no raio
    estimated_population = int(radius / 1000)  # Simulando que a cada 1000 metros tem 'x' pessoas

    print(f"Recebido: Latitude: {lat}, Longitude: {lng}, Raio: {radius}")
    return jsonify({
        'status': 'success',
        'message': 'Dados recebidos com sucesso!',
        'estimated_population': estimated_population
    })

if __name__ == '__main__':
    app.run(debug=True)
