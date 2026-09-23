{{ config(materialized='view') }}

select
    cod_divisao,
    cod_secao,
    trim(nome_divisao) as nome_divisao,
    coalesce(status_divisao, false) as is_ativo,
    data_hora_atualizacao,
    data_hora_carga
from {{ source('open_gov_staging', 'servico_divisao') }}
