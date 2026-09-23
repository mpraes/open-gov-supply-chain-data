{{ config(materialized='view') }}

select
    cod_servico,
    trim(sigla_unidade_medida) as sigla_unidade_medida,
    trim(nome_unidade_medida) as nome_unidade_medida,
    coalesce(status_unidade_medida, false) as is_ativo,
    data_hora_carga
from {{ source('open_gov_staging', 'servico_unidade_medida') }}
