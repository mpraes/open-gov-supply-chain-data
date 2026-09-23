{{ config(materialized='view') }}

select
    trim(codigo_uasg) as codigo_uasg,
    trim(nome_uasg) as nome_uasg,
    coalesce(uso_sisg, false) as is_uso_sisg,
    coalesce(adesao_siasg, false) as is_adesao_siasg,
    trim(sigla_uf) as sigla_uf,
    codigo_municipio,
    codigo_municipio_ibge,
    trim(nome_municipio_ibge) as nome_municipio_ibge,
    codigo_unidade_polo,
    trim(nome_unidade_polo) as nome_unidade_polo,
    codigo_unidade_espelho,
    trim(nome_unidade_espelho) as nome_unidade_espelho,
    coalesce(uasg_cadastradora, false) as is_uasg_cadastradora,
    trim(cnpj_cpf_uasg) as cnpj_cpf_uasg,
    codigo_orgao,
    trim(cnpj_cpf_orgao) as cnpj_cpf_orgao,
    trim(cnpj_cpf_orgao_vinculado) as cnpj_cpf_orgao_vinculado,
    trim(cnpj_cpf_orgao_superior) as cnpj_cpf_orgao_superior,
    trim(codigo_siorg) as codigo_siorg,
    coalesce(status_uasg, false) as is_ativo,
    data_implantacao_sidec,
    data_hora_movimento,
    data_hora_carga
from {{ source('open_gov_staging', 'uasg') }}
