# 🗺️ Círculos no Mapa

**Resumo:**  
Este experimento visualiza círculos geográficos em um mapa, com centro em coordenadas definidas e raio especificado em quilômetros.  
O objetivo foi entender como representar áreas de alcance (ex: zonas de influência, distância máxima de cobertura) respeitando a curvatura da Terra e a escala do mapa.
Conforme https://chatgpt.com/c/6716dc7d-dc60-800d-92fe-eae42f53a177

---

## 🧠 Motivação

> "E se eu quisesse marcar, num mapa, todos os pontos que estão até X km de um ponto central? Como isso se representa em coordenadas geográficas?"

A ideia nasceu de uma curiosidade prática: traçar áreas de influência em mapas — algo comum em estudos urbanos, marketing, logística e epidemiologia.

---

## ⚙️ O que ele faz

- Dado um ponto central (latitude, longitude) e um raio em km:
  - Calcula os pontos de contorno que formam um círculo geográfico ao redor
  - Gera um arquivo GeoJSON ou exibe em um mapa interativo com `folium`
- Pode adicionar múltiplos círculos, sobrepor camadas, ajustar cores e opacidade

---

## 🤖 Como o GPT ajudou

- Geração de código para cálculo de pontos ao redor de um centro usando `geopy`
- Integração com `folium` para visualização
- Explicações sobre distorção de escala em mapas (especialmente em altas latitudes)

---

## 🧪 Exemplo de uso

```python
# Define ponto central
centro = (-23.5505, -46.6333)  # São Paulo, SP

# Gera círculo de 10 km
circulo = gerar_circulo(centro, raio_km=10)

# Visualiza no mapa
exibir_mapa_com_circulo(centro, circulo)
```

Visualização gerada:

---

## 📦 Requisitos

- geopy
- folium
- numpy
- flask
- geopandas
- shapely

Instale com:

```bash
pip install geopy folium numpy
```

---

## 🧭 Próximos passos

- Adicionar suporte a múltiplos círculos com diferentes raios
- Exportar para arquivos .geojson ou .kml
- Marcar interseções entre círculos

---

## 📝 Notas finais

Embora mapas pareçam planos, círculos reais no mundo seguem geodésicas — e esse projeto ajuda a traduzir esse conceito de maneira visual e concreta.

---
