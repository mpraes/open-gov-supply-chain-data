{{ config(materialized='view') }}

select
    cod_classe,
    cod_grupo,
    trim(nome_classe) as nome_classe,
    coalesce(status_classe, false) as is_ativo,
    data_hora_atualizacao,
    data_hora_carga
from {{ source('open_gov_staging', 'material_class') }}
