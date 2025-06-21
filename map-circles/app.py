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

import rasterio
import numpy as np

# Carregue o arquivo .tif
file_path = 'caminho_para_o_arquivo.tif'

# Abrir o arquivo .tif usando rasterio
with rasterio.open(file_path) as dataset:
    # Obter os dados de densidade populacional
    densidade = dataset.read(1)  # Lê a primeira banda (a densidade populacional)
    
    # Obter as coordenadas de cada pixel
    transform = dataset.transform
    
    # Verificar informações básicas
    print("Dimensões:", densidade.shape)
    print("Transform:", transform)
    print("Primeiros valores de densidade:", densidade[0:5, 0:5])


from rasterio.transform import rowcol
from shapely.geometry import Point

# Converter coordenadas geográficas para índice no raster
def coordenadas_para_indice(lon, lat, transform):
    # Usar a transformação do dataset para converter para índice de linha/coluna
    col, row = ~transform * (lon, lat)
    return int(row), int(col)

# # Exemplo de uso com coordenadas de um ponto
# lon, lat = -47.9292, -15.7801  # Exemplo: Brasília
# linha, coluna = coordenadas_para_indice(lon, lat, transform)
# print("Índice no raster:", linha, coluna)
# print("Densidade populacional nesse ponto:", densidade[linha, coluna])


if __name__ == '__main__':
    app.run(debug=True)
