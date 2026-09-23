{{ config(materialized='view') }}

select
    cod_secao,
    trim(nome_secao) as nome_secao,
    coalesce(status_secao, false) as is_ativo,
    data_hora_atualizacao,
    data_hora_carga
from {{ source('open_gov_staging', 'servico_secao') }}
