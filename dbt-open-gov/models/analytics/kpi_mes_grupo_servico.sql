{{ config(materialized='table') }}

select
    date_trunc('month', f.data_compra)::date as mes,
    coalesce(g.nome_grupo, cast(i.cod_grupo as text)) as nome_grupo,
    sum(f.valor_total_homologado) as valor_total
from {{ ref('fct_preco_servico') }} f
join {{ ref('stg_servico_item') }} i on i.cod_servico = f.cod_servico
left join {{ ref('dim_servico_grupo') }} g on g.cod_grupo = i.cod_grupo
where f.data_compra is not null
group by 1, 2
