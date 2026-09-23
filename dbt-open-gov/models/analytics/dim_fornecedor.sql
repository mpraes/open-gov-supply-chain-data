{{ config(materialized='table') }}

with base_cadastrados as (
    select
        nullif(trim(regexp_replace(coalesce(ni_fornecedor, ''), '[.\-/]', '', 'g')), '') as ni_fornecedor,
        trim(nome_razao_social) as nome_razao_social,
        is_ativo,
        cnpj,
        cpf,
        is_habilitado_licitar,
        codigo_cnae,
        nome_cnae,
        cod_natureza_juridica,
        nome_natureza_juridica,
        cod_porte_empresa,
        nome_porte_empresa,
        nome_municipio,
        sigla_uf,
        data_hora_carga,
        row_number() over (
            partition by nullif(trim(regexp_replace(coalesce(ni_fornecedor, ''), '[.\-/]', '', 'g')), '')
            order by data_hora_carga desc nulls last
        ) as rn
    from {{ ref('stg_fornecedor') }}
    where ni_fornecedor is not null and trim(ni_fornecedor) != ''
),

cadastrados_unicos as (
    select *
    from base_cadastrados
    where rn = 1 and ni_fornecedor is not null
),

fornecedores_nas_fatos as (
    select distinct 
        nullif(trim(regexp_replace(coalesce(ni_fornecedor, ''), '[.\-/]', '', 'g')), '') as ni_fornecedor
    from {{ ref('stg_preco_material') }}
    where ni_fornecedor is not null and trim(ni_fornecedor) != ''
    
    union
    
    select distinct 
        nullif(trim(regexp_replace(coalesce(ni_fornecedor, ''), '[.\-/]', '', 'g')), '') as ni_fornecedor
    from {{ ref('stg_preco_servico') }}
    where ni_fornecedor is not null and trim(ni_fornecedor) != ''
),

fatos_unicas as (
    select distinct ni_fornecedor
    from fornecedores_nas_fatos
    where ni_fornecedor is not null
),

fornecedores_complementares as (
    select
        f.ni_fornecedor,
        'FORNECEDOR NÃO CADASTRADO NO CADASTRO GERAL' as nome_razao_social,
        false as is_ativo,
        null as cnpj,
        null as cpf,
        false as is_habilitado_licitar,
        null as codigo_cnae,
        null as nome_cnae,
        null as cod_natureza_juridica,
        null as nome_natureza_juridica,
        null as cod_porte_empresa,
        null as nome_porte_empresa,
        null as nome_municipio,
        null as sigla_uf,
        now() as data_hora_carga
    from fatos_unicas f
    left join cadastrados_unicos c on f.ni_fornecedor = c.ni_fornecedor
    where c.ni_fornecedor is null
)

select 
    ni_fornecedor, nome_razao_social, is_ativo, cnpj, cpf, is_habilitado_licitar,
    codigo_cnae, nome_cnae, cod_natureza_juridica, nome_natureza_juridica,
    cod_porte_empresa, nome_porte_empresa, nome_municipio, sigla_uf, data_hora_carga
from cadastrados_unicos

union all

select 
    ni_fornecedor, nome_razao_social, is_ativo, cnpj, cpf, is_habilitado_licitar,
    codigo_cnae, nome_cnae, cod_natureza_juridica, nome_natureza_juridica,
    cod_porte_empresa, nome_porte_empresa, nome_municipio, sigla_uf, data_hora_carga
from fornecedores_complementares
