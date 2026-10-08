{{ config(materialized='table') }}

select
    origem,
    codigo_uasg,
    sum(valor_total) as valor_total,
    min(mes) as mes_min,
    max(mes) as mes_max
from {{ ref('kpi_mes_uasg') }}
group by 1, 2
