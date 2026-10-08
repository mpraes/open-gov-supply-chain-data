{{ config(materialized='table') }}

select
    cod_item,
    sum(valor_total) as valor_total,
    min(mes) as mes_min,
    max(mes) as mes_max
from {{ ref('kpi_mes_item_material') }}
group by 1
