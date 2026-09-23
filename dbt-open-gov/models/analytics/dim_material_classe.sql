{{ config(materialized='table') }}

select
    cod_classe,
    cod_grupo,
    nome_classe,
    is_ativo,
    data_hora_atualizacao
from {{ ref('stg_material_class') }}
