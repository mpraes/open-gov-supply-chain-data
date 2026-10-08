{{ config(materialized='table') }}

select
    origem,
    ni_fornecedor,
    sum(valor_total) as valor_total,
    min(mes) as mes_min,
    max(mes) as mes_max
from {{ ref('kpi_mes_fornecedor') }}
group by 1, 2
