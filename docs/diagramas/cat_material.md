// Use DBML to define your database structure
// Docs: https://dbml.dbdiagram.io/docs

Table dim_material_grupo {
  cod_grupo int8 [pk, note: 'Código identificador do grupo']
  nome_grupo varchar(200) [not null]
  is_ativo boolean
  data_hora_atualizacao timestamp
}

Table dim_material_classe {
  cod_classe int8 [pk, note: 'Código identificador da classe']
  cod_grupo int8 [not null, note: 'FK para dim_material_grupo']
  nome_classe varchar(200) [not null]
  is_ativo boolean
  data_hora_atualizacao timestamp
}

Table dim_material_pdm {
  cod_pdm int8 [pk, note: 'Padrão Descritivo de Material']
  cod_classe int8 [not null, note: 'FK para dim_material_classe']
  cod_grupo int8 [not null, note: 'Redundância útil de hierarquia']
  nome_pdm varchar(200) [not null]
  is_ativo boolean
  data_hora_atualizacao timestamp
}

Table dim_material_item {
  cod_item int8 [pk, note: 'Item individual de material']
  cod_pdm int8 [not null, note: 'FK para dim_material_pdm']
  descricao_item text [not null]
  is_ativo boolean
  is_sustentavel boolean
  codigo_ncm varchar(20)
  descricao_ncm text
  aplica_margem_preferencia boolean
  data_hora_atualizacao timestamp
}

Table dim_material_unidade_fornecimento {
  cod_pdm int8 [not null, note: 'FK para dim_material_pdm']
  numero_sequencial_unidade_fornecimento int8 [not null]
  sigla_unidade_fornecimento varchar(50) [not null]
  nome_unidade_fornecimento varchar(200)
  descricao_unidade_fornecimento text
  sigla_unidade_medida varchar(50)
  capacidade_unidade_fornecimento numeric
  is_ativo_pdm boolean
  is_ativo_unidade boolean
  data_hora_atualizacao timestamp

  indexes {
    (cod_pdm, numero_sequencial_unidade_fornecimento) [pk]
  }
}

Table bridge_material_pdm_natureza_despesa {
  cod_pdm int8 [not null, note: 'FK para dim_material_pdm']
  cod_natureza_despesa varchar(50) [not null]
  nome_natureza_despesa varchar(200)
  status_natureza_despesa varchar(50)

  indexes {
    (cod_pdm, cod_natureza_despesa) [pk]
  }
}

Table dim_material_caracteristica {
  cod_item int8 [not null, note: 'FK para dim_material_item']
  numero_caracteristica int4 [not null]
  codigo_caracteristica varchar(50)
  nome_caracteristica varchar(200)
  is_ativo_caracteristica boolean
  codigo_valor_caracteristica varchar(50)
  nome_valor_caracteristica text
  is_ativo_valor_caracteristica boolean
  sigla_unidade_medida varchar(50)
  data_hora_atualizacao timestamp

  indexes {
    (cod_item, numero_caracteristica) [pk]
  }
}

// Relacionamentos Hierárquicos
Ref: dim_material_grupo.cod_grupo < dim_material_classe.cod_grupo
Ref: dim_material_classe.cod_classe < dim_material_pdm.cod_classe
Ref: dim_material_pdm.cod_pdm < dim_material_item.cod_pdm

// Desdobramentos do PDM
Ref: dim_material_pdm.cod_pdm < dim_material_unidade_fornecimento.cod_pdm
Ref: dim_material_pdm.cod_pdm < bridge_material_pdm_natureza_despesa.cod_pdm

// Características do Item de Material
Ref: dim_material_item.cod_item < dim_material_caracteristica.cod_item
