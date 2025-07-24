

# 🗺️ Detecção de Sequências no SQL

**Resumo:**  
Uma ideia com SQL avançado: dada uma sequência de números esparsos, queremos encontrar os casos de números sequenciais dentro dela. É o tipo de coisa que um programador recém-formado faria no C++ ou Java (abordagem estruturada) sem maiores problemas, mas se tiver que fazer em SQL (abordagem de conjuntos) provavelmente vai engasgar.

Conforme:
- https://chatgpt.com/c/67eca281-0974-800d-a830-e9f9cb8293df (SqlExpert)
- https://chatgpt.com/c/67ec9eb8-34a0-800d-9cfe-d73911eb3113 (GPT)

---

## 🧠 Motivação

> No Projeto Pizzarias do Mundo, os competidores recebem "medalhas" por determinados padrões e/ou comportamentos com os folhetos entregues. Uma delas é a sequência de meses com entrega: o competidor ganha a medalha de Prata ao entregar folhetos (mesmo que só 1) em 6 meses seguidos, e a de Ouro ao completar 12 meses diferentes.

Para descobrir os ganhadores dessa medalha (existem várias outras!), dada uma sequência de meses desde o início do projeto, sendo abr/2012 o mês 1, mai/12 o mês 2 e assim por diante, a ideia era encontrar pessoas que entregaram folhetos em meses seguidos.

---

## ⚙️ O que a query faz

- Dada uma coluna X numérica sequencial esparsa:
	- Identifica os grupos usando row_number() ou equivalente
	- **Números sequenciais terão valores iguais para (X - rownumber)** --> esta é a Sacada Genial™!!

---

## 🤖 Como o GPT ajudou

- Teve a Sacada Genial™
- Gerou o código inicial para sequências de 1 em 1
- Só depois o Sallin teve a ideia de localizar sequências com outros passos
- Ele ajustou a abordagem mas mantendo a Sacada Genial™
- Mas não trouxe exatamente o resultado esperado: repete sequências parciais
- Sallin fez este ajuste manualmente


---

## 🧪 Exemplo de uso

Considerando uma coluna numérica COL com os seguintes valores:
35, 41, 49, 51, 58, 71, 75, 79, 80, 83, 84, 111, 115, 125, 144, 145, 146, 147, 192, 193

Para passo=1 ele retorna:

| ini | fim | qtd | todos |
| --- | --- | --- | ------ |
| 79 | 80 | 2 | 79,80 |
| 83 | 84 | 2 | 83,84 |
| 144 | 147 | 4 | 144,145,146,147 |
| 192 | 193 | 2 | 192,193 |


Para passo=4:
| ini | fim | qtd | todos |
| --- | --- | --- | ------ |
| 71 | 83 | 4 | 71,75,79,83 |
| 80 | 84 | 2 | 80,84 |
| 111 | 115 | 2 | 111,115 |


---
