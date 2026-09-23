{{ config(materialized='view') }}

select
    cod_grupo,
    cod_divisao,
    trim(nome_grupo) as nome_grupo,
    coalesce(status_grupo, false) as is_ativo,
    data_hora_atualizacao,
    data_hora_carga
from {{ source('open_gov_staging', 'servico_grupo') }}
