{{ config(materialized='view') }}

select
    cod_item,
    cod_pdm,
    cod_classe,
    cod_grupo,
    trim(descricao_item) as descricao_item,
    coalesce(status_item, false) as is_ativo,
    coalesce(item_sustentavel, false) as is_sustentavel,
    nullif(trim(codigo_ncm), '') as codigo_ncm,
    nullif(trim(descricao_ncm), '') as descricao_ncm,
    coalesce(aplica_margem_preferencia, false) as aplica_margem_preferencia,
    data_hora_atualizacao,
    data_hora_carga
from {{ source('open_gov_staging', 'material_item') }}
