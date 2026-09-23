{{ config(materialized='table') }}

select
    cod_subclasse,
    cod_classe,
    nome_subclasse,
    is_ativo,
    data_hora_atualizacao
from {{ ref('stg_servico_subclasse') }}
