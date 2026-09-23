{{ config(
    materialized='incremental',
    unique_key='id_pdm_natureza_despesa'
) }}

select
    md5(cast(cod_pdm as text) || '-' || cast(cod_natureza_despesa as text)) as id_pdm_natureza_despesa,
    cod_pdm,
    cod_natureza_despesa,
    nome_natureza_despesa,
    status_natureza_despesa,
    data_hora_carga
from {{ ref('stg_material_natureza_despesa') }}

{% if is_incremental() %}
    where data_hora_carga > (select max(data_hora_carga) from {{ this }})
{% endif %}
