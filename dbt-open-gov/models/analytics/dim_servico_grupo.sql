{{ config(materialized='table') }}

select
    cod_grupo,
    cod_divisao,
    nome_grupo,
    is_ativo,
    data_hora_atualizacao
from {{ ref('stg_servico_grupo') }}
