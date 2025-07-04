WITH sequencias AS (
    SELECT 
        col,
        col - ROW_NUMBER() OVER (ORDER BY col) AS grupo
    FROM tabela
)
SELECT 
    MIN(col) AS ini,
    MAX(col) AS fim,
    COUNT(*) AS qtd,
    STRING_AGG(col::TEXT, ',') AS todos
FROM sequencias
GROUP BY grupo
HAVING COUNT(*) > 1
ORDER BY ini;
