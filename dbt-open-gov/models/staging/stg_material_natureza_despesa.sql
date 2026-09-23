{{ config(materialized='view') }}

select
    cod_pdm,
    trim(cod_natureza_despesa) as cod_natureza_despesa,
    trim(nome_natureza_despesa) as nome_natureza_despesa,
    trim(status_natureza_despesa) as status_natureza_despesa,
    data_hora_carga
from {{ source('open_gov_staging', 'material_natureza_despesa') }}
