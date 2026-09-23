{{ config(materialized='table') }}

select
    cod_pdm,
    cod_classe,
    cod_grupo,
    nome_pdm,
    is_ativo,
    data_hora_atualizacao
from {{ ref('stg_material_pdm') }}
