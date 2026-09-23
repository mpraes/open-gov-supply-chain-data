{{ config(
	materialized='incremental',
	unique_key='id_servico_unidade_medida'
) }}

select
    md5(cast(cod_servico as text) || '-' || cast(sigla_unidade_medida as text)) as id_servico_unidade_medida, 
    cod_servico,
    sigla_unidade_medida,
    nome_unidade_medida,
    is_ativo,
    data_hora_carga
from {{ ref('stg_servico_unidade_medida') }}

{% if is_incremental() %}
    where data_hora_carga > (select max(data_hora_carga) from {{ this }})
{% endif %}
