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
file_path = 'caminho_para_o_arquivo.tif'  # Substitua pelo caminho correto

# Abrir o arquivo .tif usando rasterio
with rasterio.open(file_path) as dataset:
    # Obter os dados de densidade populacional
    densidade = dataset.read(1)  # Lê a primeira banda (densidade populacional)
    
    # Obter as coordenadas de cada pixel
    transform = dataset.transform
    
    # Verificar informações básicas
    print("Dimensões da imagem (linha, coluna):", densidade.shape)
    print("Transformação de coordenadas:", transform)
    print("Primeiros valores de densidade populacional:", densidade[0:5, 0:5])



from rasterio.transform import rowcol

# Função para converter coordenadas geográficas para índice no raster
def coordenadas_para_indice(lon, lat, transform):
    col, row = ~transform * (lon, lat)
    return int(row), int(col)

# # Exemplo de uso: coordenadas de Brasília
# lon, lat = -47.9292, -15.7801  # Brasília

# # Converter coordenadas para índice no raster
# linha, coluna = coordenadas_para_indice(lon, lat, transform)
# print(f"Índice no raster para Brasília: ({linha}, {coluna})")
# print(f"Densidade populacional em Brasília: {densidade[linha, coluna]}")



from shapely.geometry import Point

# Função para verificar se um ponto está dentro de um círculo
def ponto_dentro_do_circulo(lon, lat, centro_circulo, raio):
    # Criar um ponto a partir das coordenadas (lon, lat)
    ponto = Point(lon, lat)
    # Criar um círculo a partir do centro e do raio
    circulo = Point(centro_circulo).buffer(raio)
    # Verificar se o ponto está dentro do círculo
    return ponto.within(circulo)

# Função para calcular a Bounding Box de um círculo
def calcular_bounding_box(centro_circulo, raio_km):
    # Aproximar 1 grau de latitude/longitude como 111 km
    raio_graus = raio_km / 111

    lon_centro, lat_centro = centro_circulo
    lon_min = lon_centro - raio_graus
    lon_max = lon_centro + raio_graus
    lat_min = lat_centro - raio_graus
    lat_max = lat_centro + raio_graus

    return lon_min, lon_max, lat_min, lat_max


def calcular_populacao_no_circulo(centro_circulo, raio_km, transform, densidade):
    # Raio do círculo em graus (aproximadamente, depende da latitude)
    raio_graus = raio_km / 111  # Aproximação de 111 km por grau de latitude

    populacao_total = 0
    
    # Iterar sobre as linhas e colunas da matriz de densidade
    for row in range(densidade.shape[0]):
        for col in range(densidade.shape[1]):
            # Converter o índice (linha, coluna) de volta para coordenadas geográficas
            lon, lat = transform * (col, row)
            
            # Verificar se o ponto está dentro do círculo
            if ponto_dentro_do_circulo(lon, lat, centro_circulo, raio_graus):
                # Adicionar a densidade dessa célula à população total
                populacao_total += densidade[row, col]
    
    return populacao_total

def calcular_populacao_no_circulo_rapido(centro_circulo, raio_km, transform, densidade):
    # Calcular a Bounding Box para o círculo
    lon_min, lon_max, lat_min, lat_max = calcular_bounding_box(centro_circulo, raio_km)
    
    # Converter as coordenadas da Bounding Box para índices no raster
    linha_min, coluna_min = coordenadas_para_indice(lon_min, lat_min, transform)
    linha_max, coluna_max = coordenadas_para_indice(lon_max, lat_max, transform)
    
    # Garantir que os índices estão na ordem correta
    linha_min, linha_max = min(linha_min, linha_max), max(linha_min, linha_max)
    coluna_min, coluna_max = min(coluna_min, coluna_max), max(coluna_min, coluna_max)
    
    populacao_total = 0

    # Iterar apenas sobre as células dentro da Bounding Box
    for row in range(linha_min, linha_max + 1):
        for col in range(coluna_min, coluna_max + 1):
            # Converter índice de volta para coordenadas geográficas
            lon, lat = transform * (col, row)
            
            # Verificar se o ponto está dentro do círculo
            if ponto_dentro_do_circulo(lon, lat, centro_circulo, raio_km / 111):
                # Adicionar a densidade da célula à população total
                populacao_total += densidade[row, col]
    
    return populacao_total


# # Exemplo de círculo em Brasília (-47.9292, -15.7801) com raio de 10 km
# centro_circulo = (-47.9292, -15.7801)
# raio_km = 10
# 
# populacao_estimada = calcular_populacao_no_circulo_rapido(centro_circulo, raio_km, transform, densidade)
# print(f"População estimada no círculo: {populacao_estimada:.0f}")




if __name__ == '__main__':
    app.run(debug=True)
