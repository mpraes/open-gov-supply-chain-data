-- Covering indexes for leftover fact scans. Run outside a transaction.
-- CREATE INDEX CONCURRENTLY cannot run inside BEGIN/COMMIT.
SET statement_timeout = 0;
SET maintenance_work_mem = '256MB';

CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_fct_preco_material_data_compra_valor
  ON analytics.fct_preco_material (data_compra)
  INCLUDE (valor_total_homologado);

CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_fct_preco_material_ni_fornecedor_valor
  ON analytics.fct_preco_material (ni_fornecedor)
  INCLUDE (valor_total_homologado);

CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_fct_preco_material_codigo_uasg_valor
  ON analytics.fct_preco_material (codigo_uasg)
  INCLUDE (valor_total_homologado);

CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_fct_preco_material_cod_item_valor
  ON analytics.fct_preco_material (cod_item)
  INCLUDE (valor_total_homologado);

CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_fct_preco_servico_data_compra_valor
  ON analytics.fct_preco_servico (data_compra)
  INCLUDE (valor_total_homologado);

CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_fct_preco_servico_ni_fornecedor_valor
  ON analytics.fct_preco_servico (ni_fornecedor)
  INCLUDE (valor_total_homologado);

CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_fct_preco_servico_codigo_uasg_valor
  ON analytics.fct_preco_servico (codigo_uasg)
  INCLUDE (valor_total_homologado);

CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_fct_preco_servico_cod_servico_valor
  ON analytics.fct_preco_servico (cod_servico)
  INCLUDE (valor_total_homologado);
