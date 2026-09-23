{{ config(materialized='table') }}

select
    cod_grupo,
    nome_grupo,
    is_ativo,
    data_hora_atualizacao
from {{ ref('stg_material_group') }}
