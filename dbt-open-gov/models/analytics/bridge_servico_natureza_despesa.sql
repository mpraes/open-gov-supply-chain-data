{{ config(
    materialized='incremental',
    unique_key='id_servico_natureza_despesa'
) }}

select
    md5(cast(cod_servico as text) || '-' || cast(cod_natureza_despesa as text)) as id_servico_natureza_despesa,
    cod_servico,
    cod_natureza_despesa,
    nome_natureza_despesa,
    is_ativo,
    data_hora_carga
from {{ ref('stg_servico_natureza_despesa') }}

{% if is_incremental() %}
    where data_hora_carga > (select max(data_hora_carga) from {{ this }})
{% endif %}
