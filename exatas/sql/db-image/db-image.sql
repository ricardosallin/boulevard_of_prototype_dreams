-- modelo de dados

CREATE TABLE imagem_pixels (
    img TEXT,
    x INT,
    y INT,
    r INT,
    g INT,
    b INT,
    PRIMARY KEY (img, x, y)
);

-- A chave composta garante unicidade do pixel.
-- X e Y podem começar em 1 ou 0, dependendo da convenção (bibliotecas de imagem geralmente usam 0-index).
-- A tabela representa uma imagem como uma matriz esparsa (caso de imagens com transparência ou regiões sem interesse, por exemplo, você poderia nem guardar tudo).

  /****************/
 /* CASOS DE USO */
/****************/

-- analise de cores dominantes

SELECT r, g, b, COUNT(*) as freq
FROM imagem_pixels
WHERE img = 'minha_imagem'
GROUP BY r, g, b
ORDER BY freq DESC;

-- Mapeamento de calor de uma cor específica
-- Exemplo: todos os pixels com r > 200 (regiões vermelhas intensas).

-- Inversão de cores com um UPDATE:
UPDATE imagem_pixels
SET r = 255 - r, g = 255 - g, b = 255 - b
WHERE img = 'imagem_teste';


-- Filtro seletivo, por exemplo, deixar só tons de azul:
UPDATE imagem_pixels
SET r = 0, g = 0
WHERE img = 'imagem_teste' AND b > r AND b > g;



-- Edição geométrica com SQL:

-- Mover blocos:
UPDATE imagem_pixels
SET x = x + 10, y = y + 5
WHERE img = 'imagem_teste' AND x BETWEEN 50 AND 100 AND y BETWEEN 50 AND 100;


-- Cortar margens:
DELETE FROM imagem_pixels
WHERE img = 'imagem_teste' AND (x < 10 OR y < 10);


🧩 Reconhecimento básico:
-- Detecção de blocos com mesma cor (útil pra OCR rudimentar ou sprite detection).
-- Tracking de padrões de cor em quadros de animação (se img for um frame ID).
-- Compressão via clustering de cores (ex: K-means simplificado em SQL).

