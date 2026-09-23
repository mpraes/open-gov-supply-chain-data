{{ config(
    materialized='incremental',
    unique_key='id_preco_material_fato'
) }}

with base as (
    select
        md5(cast(id_compra as text) || '-' || cast(id_item_compra as text)) as id_preco_material_fato,
        id_compra,
        id_item_compra,
        numero_item_compra,
        cod_item,
        cod_pdm,
        cod_classe,
        nullif(trim(regexp_replace(coalesce(ni_fornecedor, ''), '[.\-/]', '', 'g')), '') as ni_fornecedor_raw,
        codigo_uasg,
        forma_compra,
        cod_modalidade,
        criterio_julgamento,
        sigla_unidade_medida,
        sigla_unidade_fornecimento,
        nome_unidade_fornecimento,
        capacidade_unidade_fornecimento,
        marca_material,
        quantidade,
        preco_unitario,
        round(cast(quantidade * preco_unitario as numeric), 2) as valor_total_homologado,
        percentual_maior_desconto,
        data_compra,
        data_resultado,
        objeto_compra,
        descricao_detalhada_item,
        data_referencia_fato,
        data_hora_carga
    from {{ ref('stg_preco_material') }}

    {% if is_incremental() %}
        where data_referencia_fato > (select max(data_referencia_fato) from {{ this }})
    {% endif %}
)

select
    b.id_preco_material_fato,
    b.id_compra,
    b.id_item_compra,
    b.numero_item_compra,
    b.cod_item,
    b.cod_pdm,
    b.cod_classe,
    -- Garante que se a chave não existir na dimensão, o valor é nulo e não viola a FK:
    f.ni_fornecedor,
    b.codigo_uasg,
    b.forma_compra,
    b.cod_modalidade,
    b.criterio_julgamento,
    b.sigla_unidade_medida,
    b.sigla_unidade_fornecimento,
    b.nome_unidade_fornecimento,
    b.capacidade_unidade_fornecimento,
    b.marca_material,
    b.quantidade,
    b.preco_unitario,
    b.valor_total_homologado,
    b.percentual_maior_desconto,
    b.data_compra,
    b.data_resultado,
    b.objeto_compra,
    b.descricao_detalhada_item,
    b.data_referencia_fato,
    b.data_hora_carga
from base b
left join {{ ref('dim_fornecedor') }} f
    on b.ni_fornecedor_raw = f.ni_fornecedor
