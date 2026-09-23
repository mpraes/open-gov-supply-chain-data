{{ config(materialized='view') }}

select
    cod_servico,
    cod_subclasse,
    cod_classe,
    cod_grupo,
    cod_divisao,
    cod_secao,
    trim(nome_servico) as nome_servico,
    cod_cpc,
    coalesce(exclusivo_central_compras, false) as is_exclusivo_central_compras,
    coalesce(status_servico, false) as is_ativo,
    data_hora_atualizacao,
    data_hora_carga
from {{ source('open_gov_staging', 'servico_item') }}
