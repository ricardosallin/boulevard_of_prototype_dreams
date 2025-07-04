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
  JOIN tabela as t
    ON t.col = s.col + s.passo
),
-- Pega apenas a sequência final (com maior qtd) para cada raiz
maximas AS (
  SELECT *
  FROM sequencias s1
  WHERE NOT EXISTS (
    SELECT 1 FROM sequencias s2
    WHERE (s1.col = s2.col or s1.raiz = s2.raiz) AND s1.qtd < s2.qtd
  )
)
SELECT 
  raiz AS ini,
  col AS fim,
  qtd,
  lista AS todos
FROM maximas
WHERE qtd >= 2
ORDER BY ini;
