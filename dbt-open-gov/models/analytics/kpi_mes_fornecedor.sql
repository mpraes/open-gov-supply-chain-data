{{ config(materialized='table') }}

select
    'material'::text as origem,
    date_trunc('month', data_compra)::date as mes,
    ni_fornecedor,
    sum(valor_total_homologado) as valor_total
from {{ ref('fct_preco_material') }}
where data_compra is not null
group by 2, 3

union all

select
    'servico',
    date_trunc('month', data_compra)::date,
    ni_fornecedor,
    sum(valor_total_homologado)
from {{ ref('fct_preco_servico') }}
where data_compra is not null
group by 2, 3
