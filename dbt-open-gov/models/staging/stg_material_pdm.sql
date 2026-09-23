{{ config(materialized='view') }}

select
    cod_pdm,
    cod_classe,
    cod_grupo,
    trim(nome_pdm) as nome_pdm,
    coalesce(status_pdm, false) as is_ativo,
    data_hora_atualizacao,
    data_hora_carga
from {{ source('open_gov_staging', 'material_pdm') }}
