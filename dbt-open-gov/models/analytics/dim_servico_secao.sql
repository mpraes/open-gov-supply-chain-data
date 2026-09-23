{{ config(materialized='table') }}

select
    cod_secao,
    nome_secao,
    is_ativo,
    data_hora_atualizacao
from {{ ref('stg_servico_secao') }}
