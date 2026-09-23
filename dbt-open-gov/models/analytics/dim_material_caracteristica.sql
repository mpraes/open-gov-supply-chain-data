{{ config(
    materialized='incremental',
    unique_key='id_material_caracteristica'
) }}

with deduplicado as (
    select
        md5(
            cast(cod_item as text) || '-' ||
            cast(numero_caracteristica as text) || '-' ||
            coalesce(trim(codigo_caracteristica), '') || '-' ||
            coalesce(trim(codigo_valor_caracteristica), '') || '-' ||
            coalesce(trim(nome_caracteristica), '') || '-' ||
            coalesce(trim(nome_valor_caracteristica), '') || '-' ||
            coalesce(trim(sigla_unidade_medida), '')
        ) as id_material_caracteristica,
        cod_item,
        numero_caracteristica,
        codigo_caracteristica,
        nome_caracteristica,
        is_ativo_caracteristica,
        codigo_valor_caracteristica,
        nome_valor_caracteristica,
        is_ativo_valor_caracteristica,
        sigla_unidade_medida,
        data_hora_atualizacao,
        row_number() over (
            partition by 
                cod_item, 
                numero_caracteristica, 
                coalesce(trim(codigo_caracteristica), ''), 
                coalesce(trim(codigo_valor_caracteristica), ''),
                coalesce(trim(nome_caracteristica), ''),
                coalesce(trim(nome_valor_caracteristica), '')
            order by data_hora_atualizacao desc nulls last, data_hora_carga desc nulls last
        ) as rn
    from {{ ref('stg_material_caracteristica') }}

    {% if is_incremental() %}
        where data_hora_atualizacao > (select max(data_hora_atualizacao) from {{ this }})
    {% endif %}
)

select
    id_material_caracteristica,
    cod_item,
    numero_caracteristica,
    codigo_caracteristica,
    nome_caracteristica,
    is_ativo_caracteristica,
    codigo_valor_caracteristica,
    nome_valor_caracteristica,
    is_ativo_valor_caracteristica,
    sigla_unidade_medida,
    data_hora_atualizacao
from deduplicado
where rn = 1
