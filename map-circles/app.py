from flask import Flask, request, jsonify
import rasterio

app = Flask(__name__)

# Carregar o arquivo de densidade populacional e o objeto transform
with rasterio.open('path/para/seu/arquivo.tif') as src:
    densidade = src.read(1)  # Lê os dados da primeira banda
    transform = src.transform

# Funções de cálculo da população
def calcular_bounding_box(centro_circulo, raio_km):
    raio_graus = raio_km / 111
    lon_centro, lat_centro = centro_circulo
    lon_min = lon_centro - raio_graus
    lon_max = lon_centro + raio_graus
    lat_min = lat_centro - raio_graus
    lat_max = lat_centro + raio_graus
    return lon_min, lon_max, lat_min, lat_max

def coordenadas_para_indice(lon, lat, transform):
    col, row = ~transform * (lon, lat)
    return int(row), int(col)

def ponto_dentro_do_circulo(lon, lat, centro_circulo, raio_graus):
    lon_centro, lat_centro = centro_circulo
    return ((lon - lon_centro)**2 + (lat - lat_centro)**2) ** 0.5 <= raio_graus

def calcular_populacao_no_circulo_rapido(centro_circulo, raio_km, transform, densidade):
    lon_min, lon_max, lat_min, lat_max = calcular_bounding_box(centro_circulo, raio_km)
    linha_min, coluna_min = coordenadas_para_indice(lon_min, lat_min, transform)
    linha_max, coluna_max = coordenadas_para_indice(lon_max, lat_max, transform)
    
    linha_min, linha_max = min(linha_min, linha_max), max(linha_min, linha_max)
    coluna_min, coluna_max = min(coluna_min, coluna_max), max(coluna_min, coluna_max)

    populacao_total = 0

    for row in range(linha_min, linha_max + 1):
        for col in range(coluna_min, coluna_max + 1):
            lon, lat = transform * (col, row)
            if ponto_dentro_do_circulo(lon, lat, centro_circulo, raio_km / 111):
                populacao_total += densidade[row, col]

    return populacao_total

# Rota para calcular a população dentro de um círculo
@app.route('/calcular_populacao', methods=['POST'])
def calcular_populacao():
    dados = request.json
    centro = dados.get('centro')  # [lon, lat]
    raio_km = dados.get('raio')  # Raio em km

    populacao_estimada = calcular_populacao_no_circulo_rapido(centro, raio_km, transform, densidade)
    
    return jsonify({"populacao": populacao_estimada})

if __name__ == '__main__':
    app.run(debug=True)
