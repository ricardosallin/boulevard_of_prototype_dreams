WITH RECURSIVE sequencias(col, raiz, passo, lista, qtd) AS (
  -- Começa cada valor como uma nova sequência
  SELECT 
    col,
    col AS raiz,
    :passo AS passo,
    CAST(col AS TEXT) AS lista,
    1 AS qtd
  FROM tabela

  UNION ALL

  -- Tenta estender a sequência procurando o próximo valor com o passo desejado
  SELECT 
    t.col,
    s.raiz,
    s.passo,
    s.lista || ',' || t.col,
    s.qtd + 1
  FROM sequencias s
  JOIN tabela t
    ON t.col = s.col + s.passo
)
SELECT 
  MIN(raiz) AS ini,
  MAX(col) AS fim,
  qtd,
  lista AS todos
FROM sequencias
WHERE qtd >= 2
GROUP BY raiz
ORDER BY ini;
