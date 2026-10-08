{{ config(materialized='table') }}

select
    'material'::text as origem,
    date_trunc('month', data_compra)::date as mes,
    sum(valor_total_homologado) as valor_total,
    count(distinct ni_fornecedor) as n_fornecedor,
    count(distinct cod_item) as n_item,
    count(distinct codigo_uasg) as n_uasg
from {{ ref('fct_preco_material') }}
where data_compra is not null
group by 2

union all

select
    'servico',
    date_trunc('month', data_compra)::date,
    sum(valor_total_homologado),
    count(distinct ni_fornecedor),
    count(distinct cod_servico),
    count(distinct codigo_uasg)
from {{ ref('fct_preco_servico') }}
where data_compra is not null
group by 2
