{{ config(materialized='table') }}

select
    cod_divisao,
    cod_secao,
    nome_divisao,
    is_ativo,
    data_hora_atualizacao
from {{ ref('stg_servico_divisao') }}
