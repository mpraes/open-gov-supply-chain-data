// Configurações do Projeto
Project open_gov_supply_chain {
  database_type: 'PostgreSQL'
  Note: 'Star Schema Analítico de Compras e Preços Públicos'
}

// --- DIMENSÕES TRANSVERSAIS ---
Table dim_fornecedor {
  ni_fornecedor varchar(20) [pk]
  nome_razao_social varchar(200)
  is_ativo boolean
  cnpj varchar(20)
  cpf varchar(20)
  is_habilitado_licitar boolean
  codigo_cnae varchar(20)
  nome_cnae varchar(200)
  cod_natureza_juridica varchar(20)
  nome_natureza_juridica varchar(200)
  cod_porte_empresa varchar(20)
  nome_porte_empresa varchar(200)
  nome_municipio varchar(200)
  sigla_uf varchar(2)
}

Table dim_uasg {
  codigo_uasg varchar(20) [pk]
  nome_uasg varchar(200)
  is_ativo boolean
  is_uso_sisg boolean
  is_adesao_siasg boolean
  sigla_uf varchar(2)
  codigo_municipio_ibge int8
  nome_municipio_ibge varchar(200)
  codigo_orgao int8
  cnpj_cpf_orgao varchar(20)
  codigo_siorg varchar(32)
}

// --- DIMENSÕES DO CATÁLOGO ---
Table dim_material_item {
  cod_item int8 [pk]
  cod_pdm int8 [not null]
  descricao_item text
  is_ativo boolean
}

Table dim_servico_item {
  cod_servico int8 [pk]
  cod_subclasse int8 [not null]
  nome_servico text
  is_ativo boolean
}

// --- FATOS DE PREÇOS HOMOLOGADOS ---
Table fct_preco_material {
  id_preco_material_fato varchar(32) [pk, note: 'MD5(id_compra + id_item_compra)']
  id_compra text [not null]
  id_item_compra int8 [not null]
  numero_item_compra int8
  cod_item int8 [not null]
  cod_pdm int8
  cod_classe int8
  ni_fornecedor varchar(20)
  codigo_uasg varchar(20)
  forma_compra varchar(200)
  cod_modalidade int8
  criterio_julgamento varchar(200)
  sigla_unidade_medida varchar(50)
  sigla_unidade_fornecimento varchar(50)
  marca_material varchar(200)
  quantidade numeric
  preco_unitario numeric
  valor_total_homologado numeric
  percentual_maior_desconto numeric
  data_compra date
  data_resultado date
  data_referencia_fato timestamp
}

Table fct_preco_servico {
  id_preco_servico_fato varchar(32) [pk, note: 'MD5(id_compra + id_item_compra)']
  id_compra text [not null]
  id_item_compra int8 [not null]
  numero_item_compra int8
  cod_servico int8 [not null]
  ni_fornecedor varchar(20)
  codigo_uasg varchar(20)
  forma_compra varchar(200)
  cod_modalidade int8
  criterio_julgamento varchar(200)
  sigla_unidade_medida varchar(50)
  quantidade numeric
  preco_unitario numeric
  valor_total_homologado numeric
  percentual_maior_desconto numeric
  data_compra date
  data_resultado date
  data_referencia_fato timestamp
}

// Relacionamentos da Fato de Material
Ref: fct_preco_material.cod_item > dim_material_item.cod_item
Ref: fct_preco_material.ni_fornecedor > dim_fornecedor.ni_fornecedor
Ref: fct_preco_material.codigo_uasg > dim_uasg.codigo_uasg

// Relacionamentos da Fato de Serviço
Ref: fct_preco_servico.cod_servico > dim_servico_item.cod_servico
Ref: fct_preco_servico.ni_fornecedor > dim_fornecedor.ni_fornecedor
Ref: fct_preco_servico.codigo_uasg > dim_uasg.codigo_uasg
