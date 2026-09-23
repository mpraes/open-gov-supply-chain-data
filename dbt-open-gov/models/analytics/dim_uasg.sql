{{ config(materialized='table') }}

select
    codigo_uasg,
    nome_uasg,
    is_ativo,
    is_uso_sisg,
    is_adesao_siasg,
    sigla_uf,
    codigo_municipio_ibge,
    nome_municipio_ibge,
    codigo_orgao,
    cnpj_cpf_orgao,
    codigo_siorg,
    data_implantacao_sidec,
    data_hora_carga
from {{ ref('stg_uasg') }}
