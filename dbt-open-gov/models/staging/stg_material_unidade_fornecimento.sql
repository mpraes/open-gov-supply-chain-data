{{ config(materialized='view') }}

select
    cod_pdm,
    numero_sequencial_unidade_fornecimento,
    trim(sigla_unidade_fornecimento) as sigla_unidade_fornecimento,
    trim(nome_unidade_fornecimento) as nome_unidade_fornecimento,
    trim(descricao_unidade_fornecimento) as descricao_unidade_fornecimento,
    trim(sigla_unidade_medida) as sigla_unidade_medida,
    capacidade_unidade_fornecimento,
    coalesce(status_unidade_fornecimento_pdm, false) as is_ativo_pdm,
    coalesce(status_unidade_fornecimento, false) as is_ativo_unidade,
    data_hora_atualizacao,
    data_hora_carga
from {{ source('open_gov_staging', 'material_unidade_fornecimento') }}
