// Configurações do Projeto
Project catalogo_servicos {
  database_type: 'PostgreSQL'
  Note: 'Modelagem Dimensional do Catálogo de Serviços (analytics)'
}

// ----------------------------------------------------
// Dimensões Hierárquicas
// ----------------------------------------------------

Table dim_servico_secao {
  cod_secao int8 [pk, note: 'Identificador único da Seção']
  nome_secao varchar(200) [not null]
  is_ativo boolean [not null]
  data_hora_atualizacao timestamp
}

Table dim_servico_divisao {
  cod_divisao int8 [pk, note: 'Identificador único da Divisão']
  cod_secao int8 [not null]
  nome_divisao varchar(200) [not null]
  is_ativo boolean [not null]
  data_hora_atualizacao timestamp
}

Table dim_servico_grupo {
  cod_grupo int8 [pk, note: 'Identificador único do Grupo']
  cod_divisao int8 [not null]
  nome_grupo varchar(200) [not null]
  is_ativo boolean [not null]
  data_hora_atualizacao timestamp
}

Table dim_servico_classe {
  cod_classe int8 [pk, note: 'Identificador único da Classe']
  cod_grupo int8 [not null]
  nome_classe varchar(200) [not null]
  is_ativo boolean [not null]
  data_hora_atualizacao timestamp
}

Table dim_servico_subclasse {
  cod_subclasse int8 [pk, note: 'Identificador único da Subclasse']
  cod_classe int8 [not null]
  nome_subclasse varchar(200) [not null]
  is_ativo boolean [not null]
  data_hora_atualizacao timestamp
}

Table dim_servico_item {
  cod_servico int8 [pk, note: 'Identificador único do Item de Serviço']
  cod_subclasse int8 [not null]
  nome_servico varchar(500) [not null]
  cod_cpc int8
  is_exclusivo_central_compras boolean [not null]
  is_ativo boolean [not null]
  data_hora_atualizacao timestamp
}

// ----------------------------------------------------
// Tabelas de Ligação (Bridges / N:M)
// ----------------------------------------------------

Table bridge_servico_unidade_medida {
  cod_servico int8 [not null]
  sigla_unidade_medida varchar(50) [not null]
  nome_unidade_medida varchar(200)
  is_ativo boolean [not null]
  data_hora_carga timestamptz

  indexes {
    (cod_servico, sigla_unidade_medida) [pk]
  }
}

Table bridge_servico_natureza_despesa {
  cod_servico int8 [not null]
  cod_natureza_despesa varchar(50) [not null]
  nome_natureza_despesa varchar(200)
  is_ativo boolean [not null]
  data_hora_carga timestamptz

  indexes {
    (cod_servico, cod_natureza_despesa) [pk]
  }
}

// ----------------------------------------------------
// Relacionamentos (Foreign Keys)
// ----------------------------------------------------

Ref: dim_servico_divisao.cod_secao > dim_servico_secao.cod_secao
Ref: dim_servico_grupo.cod_divisao > dim_servico_divisao.cod_divisao
Ref: dim_servico_classe.cod_grupo > dim_servico_grupo.cod_grupo
Ref: dim_servico_subclasse.cod_classe > dim_servico_classe.cod_classe
Ref: dim_servico_item.cod_subclasse > dim_servico_subclasse.cod_subclasse

Ref: bridge_servico_unidade_medida.cod_servico > dim_servico_item.cod_servico
Ref: bridge_servico_natureza_despesa.cod_servico > dim_servico_item.cod_servico
