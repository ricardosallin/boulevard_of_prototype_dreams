from flask import Flask, render_template, request, jsonify
import rasterio

app = Flask(__name__)

# Carregar o arquivo de densidade populacional e o objeto transform
with rasterio.open('path/para/seu/arquivo.tif') as src:
    densidade = src.read(1)  # Lê os dados da primeira banda
    transform = src.transform

# Função para calcular a Bounding Box do círculo
def calcular_bounding_box(centro_circulo, raio_km):
    raio_graus = raio_km / 111  # Aproximar 1 grau = 111 km
    lon_centro, lat_centro = centro_circulo
    lon_min = lon_centro - raio_graus
    lon_max = lon_centro + raio_graus
    lat_min = lat_centro - raio_graus
    lat_max = lat_centro + raio_graus
    return lon_min, lon_max, lat_min, lat_max

# Função para converter coordenadas para índices da matriz de densidade
def coordenadas_para_indice(lon, lat, transform):
    col, row = ~transform * (lon, lat)
    return int(row), int(col)

# Função para verificar se um ponto está dentro do círculo
def ponto_dentro_do_circulo(lon, lat, centro_circulo, raio_graus):
    lon_centro, lat_centro = centro_circulo
    return ((lon - lon_centro)**2 + (lat - lat_centro)**2) ** 0.5 <= raio_graus

# Função para calcular a população dentro do círculo
def calcular_populacao_no_circulo(centro_circulo, raio_km, transform, densidade):
    lon_min, lon_max, lat_min, lat_max = calcular_bounding_box(centro_circulo, raio_km)
    linha_min, coluna_min = coordenadas_para_indice(lon_min, lat_min, transform)
    linha_max, coluna_max = coordenadas_para_indice(lon_max, lat_max, transform)

    # Verificar os limites da matriz
    linha_min, linha_max = max(0, min(linha_min, linha_max)), min(densidade.shape[0] - 1, max(linha_min, linha_max))
    coluna_min, coluna_max = max(0, min(coluna_min, coluna_max)), min(densidade.shape[1] - 1, max(coluna_min, coluna_max))

    populacao_total = 0

    # Iterar sobre as células na bounding box e calcular a população
    for row in range(linha_min, linha_max + 1):
        for col in range(coluna_min, coluna_max + 1):
            lon, lat = transform * (col, row)
            if ponto_dentro_do_circulo(lon, lat, centro_circulo, raio_km / 111):
                valor_densidade = densidade[row, col]

                # Ignorar células sem dados ou com valores inválidos
                if valor_densidade > 0:  # Considerar apenas valores positivos
                    populacao_total += valor_densidade

    return populacao_total


# Rota principal para servir o arquivo HTML
@app.route('/')
def index():
    return render_template('index.html')

# Rota para calcular a população
@app.route('/process_circle', methods=['POST'])
def process_circle():
    dados = request.json
    centro = dados.get('centro')  # Coordenadas [lon, lat]
    raio_km = dados.get('raio')   # Raio em km

    populacao_estimada = calcular_populacao_no_circulo(centro, raio_km, transform, densidade)

    return jsonify({"estimated_population": populacao_estimada})

if __name__ == '__main__':
    app.run(debug=True)
