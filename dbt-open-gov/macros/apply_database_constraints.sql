{% macro apply_database_constraints() %}

{% set sql %}
-- ============================================================================
-- 1. CHAVES PRIMÁRIAS (PRIMARY KEYS)
-- ============================================================================

-- 1.1 Dimensões Transversais
ALTER TABLE analytics.dim_fornecedor 
  DROP CONSTRAINT IF EXISTS pk_dim_fornecedor CASCADE;
ALTER TABLE analytics.dim_fornecedor 
  ADD CONSTRAINT pk_dim_fornecedor PRIMARY KEY (ni_fornecedor);

ALTER TABLE analytics.dim_uasg 
  DROP CONSTRAINT IF EXISTS pk_dim_uasg CASCADE;
ALTER TABLE analytics.dim_uasg 
  ADD CONSTRAINT pk_dim_uasg PRIMARY KEY (codigo_uasg);

-- 1.2 Catálogo de Materiais
ALTER TABLE analytics.dim_material_grupo 
  DROP CONSTRAINT IF EXISTS pk_dim_material_grupo CASCADE;
ALTER TABLE analytics.dim_material_grupo 
  ADD CONSTRAINT pk_dim_material_grupo PRIMARY KEY (cod_grupo);

ALTER TABLE analytics.dim_material_classe 
  DROP CONSTRAINT IF EXISTS pk_dim_material_classe CASCADE;
ALTER TABLE analytics.dim_material_classe 
  ADD CONSTRAINT pk_dim_material_classe PRIMARY KEY (cod_classe);

ALTER TABLE analytics.dim_material_pdm 
  DROP CONSTRAINT IF EXISTS pk_dim_material_pdm CASCADE;
ALTER TABLE analytics.dim_material_pdm 
  ADD CONSTRAINT pk_dim_material_pdm PRIMARY KEY (cod_pdm);

ALTER TABLE analytics.dim_material_item 
  DROP CONSTRAINT IF EXISTS pk_dim_material_item CASCADE;
ALTER TABLE analytics.dim_material_item 
  ADD CONSTRAINT pk_dim_material_item PRIMARY KEY (cod_item);

ALTER TABLE analytics.dim_material_caracteristica 
  DROP CONSTRAINT IF EXISTS pk_dim_material_caracteristica CASCADE;
ALTER TABLE analytics.dim_material_caracteristica 
  ADD CONSTRAINT pk_dim_material_caracteristica PRIMARY KEY (id_material_caracteristica);

ALTER TABLE analytics.dim_material_unidade_fornecimento 
  DROP CONSTRAINT IF EXISTS pk_dim_material_unidade_fornecimento CASCADE;
ALTER TABLE analytics.dim_material_unidade_fornecimento 
  ADD CONSTRAINT pk_dim_material_unidade_fornecimento PRIMARY KEY (id_unidade_fornecimento);

ALTER TABLE analytics.bridge_material_pdm_natureza_despesa 
  DROP CONSTRAINT IF EXISTS pk_bridge_material_natureza CASCADE;
ALTER TABLE analytics.bridge_material_pdm_natureza_despesa 
  ADD CONSTRAINT pk_bridge_material_natureza PRIMARY KEY (id_pdm_natureza_despesa);

-- 1.3 Catálogo de Serviços
ALTER TABLE analytics.dim_servico_secao 
  DROP CONSTRAINT IF EXISTS pk_dim_servico_secao CASCADE;
ALTER TABLE analytics.dim_servico_secao 
  ADD CONSTRAINT pk_dim_servico_secao PRIMARY KEY (cod_secao);

ALTER TABLE analytics.dim_servico_divisao 
  DROP CONSTRAINT IF EXISTS pk_dim_servico_divisao CASCADE;
ALTER TABLE analytics.dim_servico_divisao 
  ADD CONSTRAINT pk_dim_servico_divisao PRIMARY KEY (cod_divisao);

ALTER TABLE analytics.dim_servico_grupo 
  DROP CONSTRAINT IF EXISTS pk_dim_servico_grupo CASCADE;
ALTER TABLE analytics.dim_servico_grupo 
  ADD CONSTRAINT pk_dim_servico_grupo PRIMARY KEY (cod_grupo);

ALTER TABLE analytics.dim_servico_classe 
  DROP CONSTRAINT IF EXISTS pk_dim_servico_classe CASCADE;
ALTER TABLE analytics.dim_servico_classe 
  ADD CONSTRAINT pk_dim_servico_classe PRIMARY KEY (cod_classe);

ALTER TABLE analytics.dim_servico_subclasse 
  DROP CONSTRAINT IF EXISTS pk_dim_servico_subclasse CASCADE;
ALTER TABLE analytics.dim_servico_subclasse 
  ADD CONSTRAINT pk_dim_servico_subclasse PRIMARY KEY (cod_subclasse);

ALTER TABLE analytics.dim_servico_item 
  DROP CONSTRAINT IF EXISTS pk_dim_servico_item CASCADE;
ALTER TABLE analytics.dim_servico_item 
  ADD CONSTRAINT pk_dim_servico_item PRIMARY KEY (cod_servico);

ALTER TABLE analytics.bridge_servico_unidade_medida 
  DROP CONSTRAINT IF EXISTS pk_bridge_servico_unidade CASCADE;
ALTER TABLE analytics.bridge_servico_unidade_medida 
  ADD CONSTRAINT pk_bridge_servico_unidade PRIMARY KEY (id_servico_unidade_medida);

ALTER TABLE analytics.bridge_servico_natureza_despesa 
  DROP CONSTRAINT IF EXISTS pk_bridge_servico_natureza CASCADE;
ALTER TABLE analytics.bridge_servico_natureza_despesa 
  ADD CONSTRAINT pk_bridge_servico_natureza PRIMARY KEY (id_servico_natureza_despesa);

-- 1.4 Tabelas Fato
ALTER TABLE analytics.fct_preco_material 
  DROP CONSTRAINT IF EXISTS pk_fct_preco_material CASCADE;
ALTER TABLE analytics.fct_preco_material 
  ADD CONSTRAINT pk_fct_preco_material PRIMARY KEY (id_preco_material_fato);

ALTER TABLE analytics.fct_preco_servico 
  DROP CONSTRAINT IF EXISTS pk_fct_preco_servico CASCADE;
ALTER TABLE analytics.fct_preco_servico 
  ADD CONSTRAINT pk_fct_preco_servico PRIMARY KEY (id_preco_servico_fato);

-- ============================================================================
-- 2. CHAVES ESTRANGEIRAS (FOREIGN KEYS)
-- ============================================================================

-- Materiais
ALTER TABLE analytics.dim_material_classe 
  DROP CONSTRAINT IF EXISTS fk_classe_grupo CASCADE;
ALTER TABLE analytics.dim_material_classe 
  ADD CONSTRAINT fk_classe_grupo 
  FOREIGN KEY (cod_grupo) REFERENCES analytics.dim_material_grupo (cod_grupo);

ALTER TABLE analytics.dim_material_pdm 
  DROP CONSTRAINT IF EXISTS fk_pdm_classe CASCADE;
ALTER TABLE analytics.dim_material_pdm 
  ADD CONSTRAINT fk_pdm_classe 
  FOREIGN KEY (cod_classe) REFERENCES analytics.dim_material_classe (cod_classe);

ALTER TABLE analytics.dim_material_item 
  DROP CONSTRAINT IF EXISTS fk_item_pdm CASCADE;
ALTER TABLE analytics.dim_material_item 
  ADD CONSTRAINT fk_item_pdm 
  FOREIGN KEY (cod_pdm) REFERENCES analytics.dim_material_pdm (cod_pdm);

ALTER TABLE analytics.dim_material_caracteristica 
  DROP CONSTRAINT IF EXISTS fk_caracteristica_item CASCADE;
ALTER TABLE analytics.dim_material_caracteristica 
  ADD CONSTRAINT fk_caracteristica_item 
  FOREIGN KEY (cod_item) REFERENCES analytics.dim_material_item (cod_item);

ALTER TABLE analytics.dim_material_unidade_fornecimento 
  DROP CONSTRAINT IF EXISTS fk_unidade_pdm CASCADE;
ALTER TABLE analytics.dim_material_unidade_fornecimento 
  ADD CONSTRAINT fk_unidade_pdm 
  FOREIGN KEY (cod_pdm) REFERENCES analytics.dim_material_pdm (cod_pdm);

ALTER TABLE analytics.bridge_material_pdm_natureza_despesa 
  DROP CONSTRAINT IF EXISTS fk_natureza_pdm CASCADE;
ALTER TABLE analytics.bridge_material_pdm_natureza_despesa 
  ADD CONSTRAINT fk_natureza_pdm 
  FOREIGN KEY (cod_pdm) REFERENCES analytics.dim_material_pdm (cod_pdm);

-- Serviços
ALTER TABLE analytics.dim_servico_divisao 
  DROP CONSTRAINT IF EXISTS fk_divisao_secao CASCADE;
ALTER TABLE analytics.dim_servico_divisao 
  ADD CONSTRAINT fk_divisao_secao 
  FOREIGN KEY (cod_secao) REFERENCES analytics.dim_servico_secao (cod_secao);

ALTER TABLE analytics.dim_servico_grupo 
  DROP CONSTRAINT IF EXISTS fk_grupo_divisao CASCADE;
ALTER TABLE analytics.dim_servico_grupo 
  ADD CONSTRAINT fk_grupo_divisao 
  FOREIGN KEY (cod_divisao) REFERENCES analytics.dim_servico_divisao (cod_divisao);

ALTER TABLE analytics.dim_servico_classe 
  DROP CONSTRAINT IF EXISTS fk_serv_classe_grupo CASCADE;
ALTER TABLE analytics.dim_servico_classe 
  ADD CONSTRAINT fk_serv_classe_grupo 
  FOREIGN KEY (cod_grupo) REFERENCES analytics.dim_servico_grupo (cod_grupo);

ALTER TABLE analytics.dim_servico_subclasse 
  DROP CONSTRAINT IF EXISTS fk_subclasse_classe CASCADE;
ALTER TABLE analytics.dim_servico_subclasse 
  ADD CONSTRAINT fk_subclasse_classe 
  FOREIGN KEY (cod_classe) REFERENCES analytics.dim_servico_classe (cod_classe);

ALTER TABLE analytics.dim_servico_item 
  DROP CONSTRAINT IF EXISTS fk_item_subclasse CASCADE;
ALTER TABLE analytics.dim_servico_item 
  ADD CONSTRAINT fk_item_subclasse 
  FOREIGN KEY (cod_subclasse) REFERENCES analytics.dim_servico_subclasse (cod_subclasse);

ALTER TABLE analytics.bridge_servico_unidade_medida 
  DROP CONSTRAINT IF EXISTS fk_unidade_servico CASCADE;
ALTER TABLE analytics.bridge_servico_unidade_medida 
  ADD CONSTRAINT fk_unidade_servico 
  FOREIGN KEY (cod_servico) REFERENCES analytics.dim_servico_item (cod_servico);

ALTER TABLE analytics.bridge_servico_natureza_despesa 
  DROP CONSTRAINT IF EXISTS fk_natureza_servico CASCADE;
ALTER TABLE analytics.bridge_servico_natureza_despesa 
  ADD CONSTRAINT fk_natureza_servico 
  FOREIGN KEY (cod_servico) REFERENCES analytics.dim_servico_item (cod_servico);

-- Fato Material
ALTER TABLE analytics.fct_preco_material 
  DROP CONSTRAINT IF EXISTS fk_fct_mat_item CASCADE;
ALTER TABLE analytics.fct_preco_material 
  ADD CONSTRAINT fk_fct_mat_item 
  FOREIGN KEY (cod_item) REFERENCES analytics.dim_material_item (cod_item);

ALTER TABLE analytics.fct_preco_material 
  DROP CONSTRAINT IF EXISTS fk_fct_mat_uasg CASCADE;
ALTER TABLE analytics.fct_preco_material 
  ADD CONSTRAINT fk_fct_mat_uasg 
  FOREIGN KEY (codigo_uasg) REFERENCES analytics.dim_uasg (codigo_uasg);

-- Fato Serviço
ALTER TABLE analytics.fct_preco_servico 
  DROP CONSTRAINT IF EXISTS fk_fct_serv_item CASCADE;
ALTER TABLE analytics.fct_preco_servico 
  ADD CONSTRAINT fk_fct_serv_item 
  FOREIGN KEY (cod_servico) REFERENCES analytics.dim_servico_item (cod_servico);

ALTER TABLE analytics.fct_preco_servico 
  DROP CONSTRAINT IF EXISTS fk_fct_serv_uasg CASCADE;
ALTER TABLE analytics.fct_preco_servico 
  ADD CONSTRAINT fk_fct_serv_uasg 
  FOREIGN KEY (codigo_uasg) REFERENCES analytics.dim_uasg (codigo_uasg);

-- ============================================================================
-- 3. SANITIZAÇÃO DE FORNECEDORES ÓRFÃOS E FKs DE FORNECEDOR
-- ============================================================================
-- Garante que se houver novo CNPJ na fato sem cadastro na dim_fornecedor,
-- ele seja registrado previamente antes de subir a foreign key:
INSERT INTO analytics.dim_fornecedor (ni_fornecedor, nome_razao_social, is_ativo, is_habilitado_licitar, data_hora_carga)
SELECT DISTINCT f.ni_fornecedor, 'FORNECEDOR NÃO LOCALIZADO NA DIMENSÃO', false, false, now()
FROM (
    SELECT ni_fornecedor FROM analytics.fct_preco_servico WHERE ni_fornecedor IS NOT NULL
    UNION
    SELECT ni_fornecedor FROM analytics.fct_preco_material WHERE ni_fornecedor IS NOT NULL
) f
LEFT JOIN analytics.dim_fornecedor d ON f.ni_fornecedor = d.ni_fornecedor
WHERE d.ni_fornecedor IS NULL;

ALTER TABLE analytics.fct_preco_material 
  DROP CONSTRAINT IF EXISTS fk_fct_mat_fornecedor CASCADE;
ALTER TABLE analytics.fct_preco_material 
  ADD CONSTRAINT fk_fct_mat_fornecedor 
  FOREIGN KEY (ni_fornecedor) REFERENCES analytics.dim_fornecedor (ni_fornecedor);

ALTER TABLE analytics.fct_preco_servico 
  DROP CONSTRAINT IF EXISTS fk_fct_serv_fornecedor CASCADE;
ALTER TABLE analytics.fct_preco_servico 
  ADD CONSTRAINT fk_fct_serv_fornecedor 
  FOREIGN KEY (ni_fornecedor) REFERENCES analytics.dim_fornecedor (ni_fornecedor);
{% endset %}

{% do run_query(sql) %}
{{ log("Constraints físicas e integridade relacional aplicadas com sucesso no schema analytics.", info=True) }}

{% endmacro %}
