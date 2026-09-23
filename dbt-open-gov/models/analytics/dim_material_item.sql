{{ config(materialized='table') }}

select
    cod_item,
    cod_pdm,
    descricao_item,
    codigo_ncm,
    descricao_ncm,
    is_ativo,
    is_sustentavel,
    aplica_margem_preferencia,
    data_hora_atualizacao
from {{ ref('stg_material_item') }}
