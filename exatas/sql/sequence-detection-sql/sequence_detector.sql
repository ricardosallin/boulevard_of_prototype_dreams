WITH sequencias AS (
    SELECT 
        col, 
        col - ROW_NUMBER() OVER (ORDER BY col) AS grupo
    FROM tabela
),
agrupado AS (
    SELECT 
        MIN(col) AS ini,
        MAX(col) AS fim,
        COUNT(*) AS qtd,
        GROUP_CONCAT(col) AS todos
    FROM sequencias
    GROUP BY grupo
    HAVING COUNT(*) > 1
)
SELECT * FROM agrupado;
