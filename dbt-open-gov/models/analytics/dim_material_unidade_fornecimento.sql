{{ config(
	materialized='incremental',
	unique_key='id_unidade_fornecimento'
)}}

select
    md5(cast(cod_pdm as text) || '-' || cast(numero_sequencial_unidade_fornecimento as text)) as id_unidade_fornecimento,
    cod_pdm,
    numero_sequencial_unidade_fornecimento,
    sigla_unidade_fornecimento,
    nome_unidade_fornecimento,
    descricao_unidade_fornecimento,
    sigla_unidade_medida,
    capacidade_unidade_fornecimento,
    is_ativo_pdm,
    is_ativo_unidade,
    data_hora_atualizacao
from {{ ref('stg_material_unidade_fornecimento') }}

{% if is_incremental() %}
    where data_hora_atualizacao > (select max(data_hora_atualizacao) from {{ this }})
{% endif %}
