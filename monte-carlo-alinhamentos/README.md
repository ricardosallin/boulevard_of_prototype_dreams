# 🎯 Monte Carlo dos Alinhamentos
(conforme https://chatgpt.com/c/6818eba4-6c9c-800d-8d1c-6616e779e0e8)

**Resumo:**  
Simulação feita para estimar a probabilidade de que, dentre `N` pontos aleatórios em um plano cartesiano, `K` estejam alinhados e/ou igualmente espaçados. O objetivo foi testar critérios como tolerância angular e regularidade de distância entre pontos.

---

## 🧠 Motivação

A curiosidade começou com uma pergunta:  
> *"Dado um conjunto de pontos aleatórios, com que frequência alguns deles formam padrões reconhecíveis — como estarem em linha ou igualmente espaçados?"*

---

## ⚙️ O que ele faz

- Gera `N` pontos aleatórios em um plano 2D
- Verifica subconjuntos que estejam alinhados (com tolerância ajustável)
- Opcional: verifica se estão igualmente espaçados
- Usa simulação de Monte Carlo para estimar frequência

---

## 🤖 Como o GPT ajudou

O ChatGPT contribuiu com:
- Geração do esqueleto do código
- Lógica para detecção de alinhamento com tolerância angular
- Ideia de decompor o problema em filtros geométricos

---

## 🧪 Exemplos de execução

```bash
python simula_alinhamentos.py --pontos 100 --min_alinhados 3 --tolerancia 0.01
```

---

## 🧭 Próximos passos?
- Adicionar visualização com Matplotlib
- Implementar detecção de espaçamento regular
- Interface Tkinter para usuários ajustarem parâmetros

---

## 📝 Notas finais
Um exercício que mistura geometria, estatística e observação de padrões — algo entre ciência e pareidolia.
