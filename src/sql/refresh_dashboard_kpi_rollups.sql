-- Rebuild monthly KPI rollups from analytics facts.
-- One slim scan per fact table, then cheap GROUP BYs. statement_timeout off.
SET statement_timeout = 0;
SET work_mem = '64MB';

DROP TABLE IF EXISTS analytics._kpi_mat_slim;
CREATE UNLOGGED TABLE analytics._kpi_mat_slim AS
SELECT date_trunc('month', data_compra)::date AS mes,
       ni_fornecedor,
       codigo_uasg,
       cod_item,
       valor_total_homologado AS valor_total
FROM analytics.fct_preco_material
WHERE data_compra IS NOT NULL;

DROP TABLE IF EXISTS analytics._kpi_srv_slim;
CREATE UNLOGGED TABLE analytics._kpi_srv_slim AS
SELECT date_trunc('month', data_compra)::date AS mes,
       ni_fornecedor,
       codigo_uasg,
       cod_servico,
       valor_total_homologado AS valor_total
FROM analytics.fct_preco_servico
WHERE data_compra IS NOT NULL;

DROP TABLE IF EXISTS analytics.kpi_mes_origem;
CREATE TABLE analytics.kpi_mes_origem AS
SELECT 'material'::text AS origem,
       mes,
       SUM(valor_total) AS valor_total,
       COUNT(DISTINCT ni_fornecedor) AS n_fornecedor,
       COUNT(DISTINCT cod_item) AS n_item,
       COUNT(DISTINCT codigo_uasg) AS n_uasg
FROM analytics._kpi_mat_slim
GROUP BY mes
UNION ALL
SELECT 'servico',
       mes,
       SUM(valor_total),
       COUNT(DISTINCT ni_fornecedor),
       COUNT(DISTINCT cod_servico),
       COUNT(DISTINCT codigo_uasg)
FROM analytics._kpi_srv_slim
GROUP BY mes;

DROP TABLE IF EXISTS analytics.kpi_mes_fornecedor;
CREATE TABLE analytics.kpi_mes_fornecedor AS
SELECT 'material'::text AS origem, mes, ni_fornecedor, SUM(valor_total) AS valor_total
FROM analytics._kpi_mat_slim
GROUP BY mes, ni_fornecedor
UNION ALL
SELECT 'servico', mes, ni_fornecedor, SUM(valor_total)
FROM analytics._kpi_srv_slim
GROUP BY mes, ni_fornecedor;

DROP TABLE IF EXISTS analytics.kpi_mes_uasg;
CREATE TABLE analytics.kpi_mes_uasg AS
SELECT 'material'::text AS origem, mes, codigo_uasg, SUM(valor_total) AS valor_total
FROM analytics._kpi_mat_slim
GROUP BY mes, codigo_uasg
UNION ALL
SELECT 'servico', mes, codigo_uasg, SUM(valor_total)
FROM analytics._kpi_srv_slim
GROUP BY mes, codigo_uasg;

DROP TABLE IF EXISTS analytics.kpi_mes_item_material;
CREATE TABLE analytics.kpi_mes_item_material AS
SELECT mes, cod_item, SUM(valor_total) AS valor_total
FROM analytics._kpi_mat_slim
GROUP BY mes, cod_item;

DROP TABLE IF EXISTS analytics.kpi_mes_item_servico;
CREATE TABLE analytics.kpi_mes_item_servico AS
SELECT mes, cod_servico, SUM(valor_total) AS valor_total
FROM analytics._kpi_srv_slim
GROUP BY mes, cod_servico;

DROP TABLE IF EXISTS analytics.kpi_mes_grupo_material;
CREATE TABLE analytics.kpi_mes_grupo_material AS
SELECT s.mes, g.nome_grupo, SUM(s.valor_total) AS valor_total
FROM analytics._kpi_mat_slim s
JOIN analytics.dim_material_item i ON i.cod_item = s.cod_item
JOIN analytics.dim_material_pdm p ON p.cod_pdm = i.cod_pdm
JOIN analytics.dim_material_classe c ON c.cod_classe = p.cod_classe
JOIN analytics.dim_material_grupo g ON g.cod_grupo = c.cod_grupo
GROUP BY 1, 2;

DROP TABLE IF EXISTS analytics.kpi_mes_grupo_servico;
CREATE TABLE analytics.kpi_mes_grupo_servico AS
SELECT s.mes,
       COALESCE(g.nome_grupo, CAST(i.cod_grupo AS text)) AS nome_grupo,
       SUM(s.valor_total) AS valor_total
FROM analytics._kpi_srv_slim s
JOIN analytics.stg_servico_item i ON i.cod_servico = s.cod_servico
LEFT JOIN analytics.dim_servico_grupo g ON g.cod_grupo = i.cod_grupo
GROUP BY 1, 2;

DROP TABLE IF EXISTS analytics._kpi_mat_slim;
DROP TABLE IF EXISTS analytics._kpi_srv_slim;

CREATE INDEX IF NOT EXISTS idx_kpi_mes_origem_origem_mes
  ON analytics.kpi_mes_origem (origem, mes);
CREATE INDEX IF NOT EXISTS idx_kpi_mes_fornecedor_mes
  ON analytics.kpi_mes_fornecedor (mes, origem);
CREATE INDEX IF NOT EXISTS idx_kpi_mes_uasg_mes
  ON analytics.kpi_mes_uasg (mes);
CREATE INDEX IF NOT EXISTS idx_kpi_mes_item_material_mes
  ON analytics.kpi_mes_item_material (mes);
CREATE INDEX IF NOT EXISTS idx_kpi_mes_item_servico_mes
  ON analytics.kpi_mes_item_servico (mes);
CREATE INDEX IF NOT EXISTS idx_kpi_mes_grupo_material_mes
  ON analytics.kpi_mes_grupo_material (mes);
CREATE INDEX IF NOT EXISTS idx_kpi_mes_grupo_servico_mes
  ON analytics.kpi_mes_grupo_servico (mes);

ANALYZE analytics.kpi_mes_origem;
ANALYZE analytics.kpi_mes_fornecedor;
ANALYZE analytics.kpi_mes_uasg;
ANALYZE analytics.kpi_mes_item_material;
ANALYZE analytics.kpi_mes_item_servico;
ANALYZE analytics.kpi_mes_grupo_material;
ANALYZE analytics.kpi_mes_grupo_servico;

DROP TABLE IF EXISTS analytics.kpi_fornecedor_total;
CREATE TABLE analytics.kpi_fornecedor_total AS
SELECT origem, ni_fornecedor, SUM(valor_total) AS valor_total,
       MIN(mes) AS mes_min, MAX(mes) AS mes_max
FROM analytics.kpi_mes_fornecedor
GROUP BY 1, 2;

DROP TABLE IF EXISTS analytics.kpi_item_material_total;
CREATE TABLE analytics.kpi_item_material_total AS
SELECT cod_item, SUM(valor_total) AS valor_total,
       MIN(mes) AS mes_min, MAX(mes) AS mes_max
FROM analytics.kpi_mes_item_material
GROUP BY 1;

DROP TABLE IF EXISTS analytics.kpi_item_servico_total;
CREATE TABLE analytics.kpi_item_servico_total AS
SELECT cod_servico, SUM(valor_total) AS valor_total,
       MIN(mes) AS mes_min, MAX(mes) AS mes_max
FROM analytics.kpi_mes_item_servico
GROUP BY 1;

DROP TABLE IF EXISTS analytics.kpi_uasg_total;
CREATE TABLE analytics.kpi_uasg_total AS
SELECT origem, codigo_uasg, SUM(valor_total) AS valor_total,
       MIN(mes) AS mes_min, MAX(mes) AS mes_max
FROM analytics.kpi_mes_uasg
GROUP BY 1, 2;

DROP TABLE IF EXISTS analytics.kpi_catalog_fornecedor;
CREATE TABLE analytics.kpi_catalog_fornecedor AS
SELECT COUNT(*)::bigint AS total,
       COUNT(*) FILTER (WHERE is_ativo)::bigint AS ativos,
       COUNT(*) FILTER (WHERE is_habilitado_licitar)::bigint AS habilitados,
       COUNT(*) FILTER (
           WHERE nome_razao_social = 'FORNECEDOR NÃO CADASTRADO NO CADASTRO GERAL'
       )::bigint AS missing
FROM analytics.dim_fornecedor;

DROP TABLE IF EXISTS analytics.kpi_fornecedor_uf;
CREATE TABLE analytics.kpi_fornecedor_uf AS
SELECT COALESCE(sigla_uf, '(sem UF)') AS label, COUNT(*)::bigint AS n
FROM analytics.dim_fornecedor
GROUP BY 1;

DROP TABLE IF EXISTS analytics.kpi_fornecedor_porte;
CREATE TABLE analytics.kpi_fornecedor_porte AS
SELECT COALESCE(NULLIF(TRIM(nome_porte_empresa), ''), '(sem porte)') AS label,
       COUNT(*)::bigint AS n
FROM analytics.dim_fornecedor
GROUP BY 1;

DROP TABLE IF EXISTS analytics.kpi_fornecedor_cnae;
CREATE TABLE analytics.kpi_fornecedor_cnae AS
SELECT COALESCE(NULLIF(TRIM(nome_cnae), ''), '(sem CNAE)') AS label,
       COUNT(*)::bigint AS n
FROM analytics.dim_fornecedor
GROUP BY 1;

DROP TABLE IF EXISTS analytics.kpi_catalog_material;
CREATE TABLE analytics.kpi_catalog_material AS
SELECT COUNT(*)::bigint AS total,
       COUNT(*) FILTER (WHERE is_ativo)::bigint AS ativos,
       COUNT(*) FILTER (WHERE is_sustentavel)::bigint AS sustentaveis,
       COUNT(*) FILTER (WHERE aplica_margem_preferencia)::bigint AS margem
FROM analytics.dim_material_item;

DROP TABLE IF EXISTS analytics.kpi_material_grupo_count;
CREATE TABLE analytics.kpi_material_grupo_count AS
SELECT g.nome_grupo AS label, COUNT(*)::bigint AS n
FROM analytics.dim_material_item i
JOIN analytics.dim_material_pdm p ON p.cod_pdm = i.cod_pdm
JOIN analytics.dim_material_classe c ON c.cod_classe = p.cod_classe
JOIN analytics.dim_material_grupo g ON g.cod_grupo = c.cod_grupo
GROUP BY 1;

CREATE INDEX IF NOT EXISTS idx_kpi_fornecedor_total_mes_max
  ON analytics.kpi_fornecedor_total (mes_max);
CREATE INDEX IF NOT EXISTS idx_kpi_item_material_total_mes_max
  ON analytics.kpi_item_material_total (mes_max);
CREATE INDEX IF NOT EXISTS idx_kpi_item_servico_total_mes_max
  ON analytics.kpi_item_servico_total (mes_max);
CREATE INDEX IF NOT EXISTS idx_kpi_uasg_total_mes_max
  ON analytics.kpi_uasg_total (mes_max);

DROP TABLE IF EXISTS analytics.kpi_catalog_servico;
CREATE TABLE analytics.kpi_catalog_servico AS
SELECT COUNT(*)::bigint AS total,
       COUNT(*) FILTER (WHERE i.is_ativo)::bigint AS ativos,
       COUNT(*) FILTER (WHERE i.is_exclusivo_central_compras)::bigint AS exclusivo,
       CASE
           WHEN COUNT(*) = 0 THEN 0::numeric
           ELSE COUNT(*) FILTER (WHERE sc.cod_subclasse IS NOT NULL)::numeric
                / COUNT(*)
       END AS cobertura
FROM analytics.dim_servico_item i
LEFT JOIN analytics.dim_servico_subclasse sc
  ON sc.cod_subclasse = i.cod_subclasse;

DROP TABLE IF EXISTS analytics.kpi_servico_secao;
CREATE TABLE analytics.kpi_servico_secao AS
SELECT COALESCE(s.nome_secao, CAST(i.cod_secao AS text)) AS label,
       COUNT(*)::bigint AS n
FROM analytics.stg_servico_item i
LEFT JOIN analytics.dim_servico_secao s ON s.cod_secao = i.cod_secao
GROUP BY 1;

DROP TABLE IF EXISTS analytics.kpi_catalog_uasg;
CREATE TABLE analytics.kpi_catalog_uasg AS
SELECT COUNT(*)::bigint AS total,
       COUNT(*) FILTER (WHERE is_ativo)::bigint AS ativas,
       COUNT(*) FILTER (WHERE is_uso_sisg)::bigint AS sisg,
       COUNT(*) FILTER (WHERE is_adesao_siasg)::bigint AS siasg,
       COUNT(DISTINCT codigo_orgao)::bigint AS orgaos
FROM analytics.dim_uasg;

DROP TABLE IF EXISTS analytics.kpi_uasg_uf;
CREATE TABLE analytics.kpi_uasg_uf AS
SELECT COALESCE(sigla_uf, '(sem UF)') AS label, COUNT(*)::bigint AS n
FROM analytics.dim_uasg
GROUP BY 1;

DROP TABLE IF EXISTS analytics.kpi_catalog_overview;
CREATE TABLE analytics.kpi_catalog_overview AS
SELECT (SELECT total FROM analytics.kpi_catalog_fornecedor) AS fornecedores,
       (SELECT total FROM analytics.kpi_catalog_material) AS materiais,
       (SELECT total FROM analytics.kpi_catalog_servico) AS servicos,
       (SELECT total FROM analytics.kpi_catalog_uasg) AS uasgs;

-- Distinct priced keys per window, so the request path does not COUNT DISTINCT.
DROP TABLE IF EXISTS analytics.kpi_priced_counts;
CREATE TABLE analytics.kpi_priced_counts AS
SELECT 'all'::text AS janela,
       (SELECT COUNT(DISTINCT ni_fornecedor) FROM analytics.kpi_fornecedor_total)
           AS n_fornecedor,
       (SELECT COUNT(*) FROM analytics.kpi_item_material_total) AS n_item_material,
       (SELECT COUNT(*) FROM analytics.kpi_item_servico_total) AS n_item_servico
UNION ALL
SELECT '12m',
       (SELECT COUNT(DISTINCT ni_fornecedor) FROM analytics.kpi_fornecedor_total
        WHERE mes_max >= (CURRENT_DATE - INTERVAL '12 months')),
       (SELECT COUNT(*) FROM analytics.kpi_item_material_total
        WHERE mes_max >= (CURRENT_DATE - INTERVAL '12 months')),
       (SELECT COUNT(*) FROM analytics.kpi_item_servico_total
        WHERE mes_max >= (CURRENT_DATE - INTERVAL '12 months'));

-- Top 8 spend rows per tabela/janela/origem. 12m sums the monthly grain.
DROP TABLE IF EXISTS analytics.kpi_top_spend;
CREATE TABLE analytics.kpi_top_spend AS
SELECT 'item_material'::text AS tabela, 'all'::text AS janela, 'all'::text AS origem,
       COALESCE(d.descricao_item, CAST(s.cod_item AS text)) AS label,
       CAST(s.cod_item AS text) AS key, s.valor_total
FROM (
    SELECT cod_item, valor_total FROM analytics.kpi_item_material_total
    ORDER BY valor_total DESC LIMIT 8
) s
LEFT JOIN analytics.dim_material_item d ON d.cod_item = s.cod_item
UNION ALL
SELECT 'item_material', '12m', 'all',
       COALESCE(d.descricao_item, CAST(s.cod_item AS text)),
       CAST(s.cod_item AS text), s.valor_total
FROM (
    SELECT cod_item, SUM(valor_total) AS valor_total
    FROM analytics.kpi_mes_item_material
    WHERE mes >= (CURRENT_DATE - INTERVAL '12 months')
    GROUP BY 1 ORDER BY 2 DESC LIMIT 8
) s
LEFT JOIN analytics.dim_material_item d ON d.cod_item = s.cod_item
UNION ALL
SELECT 'item_servico', 'all', 'all',
       COALESCE(d.nome_servico, CAST(s.cod_servico AS text)),
       CAST(s.cod_servico AS text), s.valor_total
FROM (
    SELECT cod_servico, valor_total FROM analytics.kpi_item_servico_total
    ORDER BY valor_total DESC LIMIT 8
) s
LEFT JOIN analytics.dim_servico_item d ON d.cod_servico = s.cod_servico
UNION ALL
SELECT 'item_servico', '12m', 'all',
       COALESCE(d.nome_servico, CAST(s.cod_servico AS text)),
       CAST(s.cod_servico AS text), s.valor_total
FROM (
    SELECT cod_servico, SUM(valor_total) AS valor_total
    FROM analytics.kpi_mes_item_servico
    WHERE mes >= (CURRENT_DATE - INTERVAL '12 months')
    GROUP BY 1 ORDER BY 2 DESC LIMIT 8
) s
LEFT JOIN analytics.dim_servico_item d ON d.cod_servico = s.cod_servico
UNION ALL
SELECT 'fornecedor', 'all', 'all',
       COALESCE(d.nome_razao_social, s.ni_fornecedor), s.ni_fornecedor, s.valor_total
FROM (
    SELECT ni_fornecedor, SUM(valor_total) AS valor_total
    FROM analytics.kpi_fornecedor_total
    GROUP BY 1 ORDER BY 2 DESC LIMIT 8
) s
LEFT JOIN analytics.dim_fornecedor d ON d.ni_fornecedor = s.ni_fornecedor
UNION ALL
SELECT 'fornecedor', '12m', 'all',
       COALESCE(d.nome_razao_social, s.ni_fornecedor), s.ni_fornecedor, s.valor_total
FROM (
    SELECT ni_fornecedor, SUM(valor_total) AS valor_total
    FROM analytics.kpi_mes_fornecedor
    WHERE mes >= (CURRENT_DATE - INTERVAL '12 months')
    GROUP BY 1 ORDER BY 2 DESC LIMIT 8
) s
LEFT JOIN analytics.dim_fornecedor d ON d.ni_fornecedor = s.ni_fornecedor
UNION ALL
SELECT 'fornecedor', 'all', origem,
       COALESCE(d.nome_razao_social, s.ni_fornecedor), s.ni_fornecedor, s.valor_total
FROM (
    SELECT origem, ni_fornecedor, valor_total
    FROM (
        SELECT origem, ni_fornecedor, valor_total,
               row_number() OVER (PARTITION BY origem ORDER BY valor_total DESC) AS rn
        FROM analytics.kpi_fornecedor_total
    ) ranked
    WHERE rn <= 8
) s
LEFT JOIN analytics.dim_fornecedor d ON d.ni_fornecedor = s.ni_fornecedor
UNION ALL
SELECT 'fornecedor', '12m', origem,
       COALESCE(d.nome_razao_social, s.ni_fornecedor), s.ni_fornecedor, s.valor_total
FROM (
    SELECT origem, ni_fornecedor, valor_total
    FROM (
        SELECT origem, ni_fornecedor, SUM(valor_total) AS valor_total,
               row_number() OVER (
                   PARTITION BY origem ORDER BY SUM(valor_total) DESC
               ) AS rn
        FROM analytics.kpi_mes_fornecedor
        WHERE mes >= (CURRENT_DATE - INTERVAL '12 months')
        GROUP BY origem, ni_fornecedor
    ) ranked
    WHERE rn <= 8
) s
LEFT JOIN analytics.dim_fornecedor d ON d.ni_fornecedor = s.ni_fornecedor
UNION ALL
SELECT 'uasg', 'all', 'all',
       COALESCE(d.nome_uasg, CAST(s.codigo_uasg AS text)),
       CAST(s.codigo_uasg AS text), s.valor_total
FROM (
    SELECT codigo_uasg, SUM(valor_total) AS valor_total
    FROM analytics.kpi_uasg_total
    GROUP BY 1 ORDER BY 2 DESC LIMIT 8
) s
LEFT JOIN analytics.dim_uasg d ON d.codigo_uasg = s.codigo_uasg
UNION ALL
SELECT 'uasg', '12m', 'all',
       COALESCE(d.nome_uasg, CAST(s.codigo_uasg AS text)),
       CAST(s.codigo_uasg AS text), s.valor_total
FROM (
    SELECT codigo_uasg, SUM(valor_total) AS valor_total
    FROM analytics.kpi_mes_uasg
    WHERE mes >= (CURRENT_DATE - INTERVAL '12 months')
    GROUP BY 1 ORDER BY 2 DESC LIMIT 8
) s
LEFT JOIN analytics.dim_uasg d ON d.codigo_uasg = s.codigo_uasg
UNION ALL
SELECT 'orgao', 'all', 'all',
       COALESCE(CAST(g.codigo_orgao AS text), '(sem órgão)'),
       CAST(g.codigo_orgao AS text), g.valor_total
FROM (
    SELECT u.codigo_orgao, SUM(t.valor_total) AS valor_total
    FROM analytics.kpi_uasg_total t
    JOIN analytics.dim_uasg u ON u.codigo_uasg = t.codigo_uasg
    GROUP BY 1 ORDER BY 2 DESC LIMIT 8
) g
UNION ALL
SELECT 'orgao', '12m', 'all',
       COALESCE(CAST(g.codigo_orgao AS text), '(sem órgão)'),
       CAST(g.codigo_orgao AS text), g.valor_total
FROM (
    SELECT u.codigo_orgao, SUM(s.valor_total) AS valor_total
    FROM analytics.kpi_mes_uasg s
    JOIN analytics.dim_uasg u ON u.codigo_uasg = s.codigo_uasg
    WHERE s.mes >= (CURRENT_DATE - INTERVAL '12 months')
    GROUP BY 1 ORDER BY 2 DESC LIMIT 8
) g;

CREATE INDEX IF NOT EXISTS idx_kpi_priced_counts_janela
  ON analytics.kpi_priced_counts (janela);
CREATE INDEX IF NOT EXISTS idx_kpi_top_spend_slice
  ON analytics.kpi_top_spend (tabela, janela, origem);

ANALYZE analytics.kpi_fornecedor_total;
ANALYZE analytics.kpi_item_material_total;
ANALYZE analytics.kpi_item_servico_total;
ANALYZE analytics.kpi_uasg_total;
ANALYZE analytics.kpi_catalog_fornecedor;
ANALYZE analytics.kpi_catalog_material;
ANALYZE analytics.kpi_catalog_servico;
ANALYZE analytics.kpi_catalog_uasg;
ANALYZE analytics.kpi_catalog_overview;
ANALYZE analytics.kpi_priced_counts;
ANALYZE analytics.kpi_top_spend;
