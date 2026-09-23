{{ config(materialized='view') }}

select
    cod_subclasse,
    cod_classe,
    trim(nome_subclasse) as nome_subclasse,
    coalesce(status_subclasse, false) as is_ativo,
    data_hora_atualizacao,
    data_hora_carga
from {{ source('open_gov_staging', 'servico_subclasse') }}
