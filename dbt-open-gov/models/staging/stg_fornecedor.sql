{{ config(materialized='view') }}

select
    trim(ni_fornecedor) as ni_fornecedor,
    case when lower(trim(ativo)) in ('true', '1', 't', 'sim', 's') then true else false end as is_ativo,
    trim(cnpj) as cnpj,
    trim(cpf) as cpf,
    case when lower(trim(habilitado_licitar)) in ('true', '1', 't', 'sim', 's') then true else false end as is_habilitado_licitar,
    trim(codigo_cnae) as codigo_cnae,
    trim(nome_cnae) as nome_cnae,
    trim(nome_municipio) as nome_municipio,
    trim(natureza_juridica_id) as cod_natureza_juridica,
    trim(natureza_juridica_nome) as nome_natureza_juridica,
    trim(porte_empresa_id) as cod_porte_empresa,
    trim(porte_empresa_nome) as nome_porte_empresa,
    trim(nome_razao_social_fornecedor) as nome_razao_social,
    trim(uf_sigla) as sigla_uf,
    data_hora_carga
from {{ source('open_gov_staging', 'fornecedor') }}
