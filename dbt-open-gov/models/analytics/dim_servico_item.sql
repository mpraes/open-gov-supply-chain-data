{{ config(materialized='table') }}

select
    cod_servico,
    cod_subclasse,
    nome_servico,
    cod_cpc,
    is_exclusivo_central_compras,
    is_ativo,
    data_hora_atualizacao
from {{ ref('stg_servico_item') }}
