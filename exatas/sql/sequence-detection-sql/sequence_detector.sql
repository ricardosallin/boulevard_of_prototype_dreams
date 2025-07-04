WITH numerada AS (
    SELECT 
        col,
        ROW_NUMBER() OVER (ORDER BY col) AS rn
    FROM tabela
),
sequencias AS (
    SELECT
        col,
        (:passo * rn) - col AS grupo
    FROM numerada
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
