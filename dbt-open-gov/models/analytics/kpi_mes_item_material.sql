{{ config(materialized='table') }}

select
    date_trunc('month', data_compra)::date as mes,
    cod_item,
    sum(valor_total_homologado) as valor_total
from {{ ref('fct_preco_material') }}
where data_compra is not null
group by 1, 2
