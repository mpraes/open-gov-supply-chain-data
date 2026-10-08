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

ANALYZE analytics.kpi_fornecedor_total;
ANALYZE analytics.kpi_item_material_total;
ANALYZE analytics.kpi_item_servico_total;
ANALYZE analytics.kpi_uasg_total;
ANALYZE analytics.kpi_catalog_fornecedor;
ANALYZE analytics.kpi_catalog_material;
