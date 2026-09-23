{{ config(materialized='view') }}

select
    cod_servico,
    trim(cod_natureza_despesa) as cod_natureza_despesa,
    trim(nome_natureza_despesa) as nome_natureza_despesa,
    coalesce(status_natureza_despesa, false) as is_ativo,
    data_hora_carga
from {{ source('open_gov_staging', 'servico_natureza_despesa') }}
