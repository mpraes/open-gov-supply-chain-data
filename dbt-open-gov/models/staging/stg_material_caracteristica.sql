{{ config(materialized='view') }}

select
    cod_item,
    numero_caracteristica,
    trim(codigo_caracteristica) as codigo_caracteristica,
    trim(nome_caracteristica) as nome_caracteristica,
    coalesce(status_caracteristica, false) as is_ativo_caracteristica,
    nullif(trim(codigo_valor_caracteristica), '') as codigo_valor_caracteristica,
    trim(nome_valor_caracteristica) as nome_valor_caracteristica,
    coalesce(status_valor_caracteristica, false) as is_ativo_valor_caracteristica,
    nullif(trim(sigla_unidade_medida), '') as sigla_unidade_medida,
    data_hora_atualizacao,
    data_hora_carga
from {{ source('open_gov_staging', 'material_caracteristica') }}
