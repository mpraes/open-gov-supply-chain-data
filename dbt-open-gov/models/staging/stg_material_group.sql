{{ config(materialized='view') }}

select
    cod_grupo,
    trim(nome_grupo) as nome_grupo,
    coalesce(status_grupo, false) as is_ativo,
    data_hora_atualizacao,
    data_hora_carga
from {{ source('open_gov_staging', 'material_group') }}
