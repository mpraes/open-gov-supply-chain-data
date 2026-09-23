{{ config(materialized='view') }}

select
    trim(id_compra) as id_compra,
    id_item_compra,
    numero_item_compra,
    codigo_item_catalogo as cod_servico,
    trim(forma) as forma_compra,
    modalidade as cod_modalidade,
    trim(criterio_julgamento) as criterio_julgamento,
    trim(descricao_item) as descricao_item,
    trim(sigla_unidade_medida) as sigla_unidade_medida,
    quantidade,
    preco_unitario,
    percentual_maior_desconto,
    nullif(trim(ni_fornecedor), '') as ni_fornecedor,
    nullif(trim(codigo_uasg), '') as codigo_uasg,
    case 
        when data_compra ~ '^\d{4}-\d{2}-\d{2}' then cast(substring(data_compra from 1 for 10) as date)
        else null 
    end as data_compra,
    case 
        when data_resultado ~ '^\d{4}-\d{2}-\d{2}' then cast(substring(data_resultado from 1 for 10) as date)
        else null 
    end as data_resultado,
    objeto_compra,
    descricao_detalhada_item,
    coalesce(data_atualizacao_fato, data_hora_carga) as data_referencia_fato,
    data_hora_carga
from {{ source('open_gov_staging', 'preco_servico') }}
