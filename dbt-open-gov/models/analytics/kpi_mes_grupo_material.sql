{{ config(materialized='table') }}

select
    date_trunc('month', f.data_compra)::date as mes,
    g.nome_grupo,
    sum(f.valor_total_homologado) as valor_total
from {{ ref('fct_preco_material') }} f
join {{ ref('dim_material_item') }} i on i.cod_item = f.cod_item
join {{ ref('dim_material_pdm') }} p on p.cod_pdm = i.cod_pdm
join {{ ref('dim_material_classe') }} c on c.cod_classe = p.cod_classe
join {{ ref('dim_material_grupo') }} g on g.cod_grupo = c.cod_grupo
where f.data_compra is not null
group by 1, 2
