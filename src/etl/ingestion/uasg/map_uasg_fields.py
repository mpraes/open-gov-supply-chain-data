"""Mapeia campos da API de UASG e de órgão para os registros de destino."""

from typing import Any


def uasg_fields(row: dict[str, Any]) -> dict[str, Any]:
    """Mapeia as chaves de consultarUasg para os campos de UasgRecord.

    Exemplo:
        uasg_fields({"codigoUasg": "153001", "nomeUasg": "x", "statusUasg": True})
    """
    return {
        **_uasg_identity_fields(row),
        **_uasg_location_fields(row),
        **_uasg_orgao_link_fields(row),
    }


def uasg_orgao_fields(row: dict[str, Any]) -> dict[str, Any]:
    """Mapeia as chaves de consultarOrgao para os campos de UasgOrgaoRecord.

    Exemplo:
        uasg_orgao_fields({"codigoOrgao": 36000, "nomeOrgao": "x", "statusOrgao": True})
    """
    return {
        **_orgao_identity_fields(row),
        **_orgao_hierarchy_fields(row),
        **_orgao_admin_fields(row),
    }


def _uasg_identity_fields(row: dict[str, Any]) -> dict[str, Any]:
    """Extrai identificação, flags SISG e SIASG, SIORG, status e datas da linha de UASG."""
    return {
        "codigo_uasg": row["codigoUasg"],
        "nome_uasg": row["nomeUasg"],
        "uso_sisg": row.get("usoSisg"),
        "adesao_siasg": row.get("adesaoSiasg"),
        "uasg_cadastradora": row.get("uasgCadastradora"),
        "cnpj_cpf_uasg": row.get("cnpjCpfUasg"),
        "codigo_siorg": row.get("codigoSiorg"),
        "status_uasg": row["statusUasg"],
        "data_implantacao_sidec": row.get("dataImplantacaoSidec"),
        "data_hora_movimento": row.get("dataHoraMovimento"),
    }


def _uasg_location_fields(row: dict[str, Any]) -> dict[str, Any]:
    """Extrai UF, município, unidade polo e unidade espelho da linha de UASG."""
    return {
        "sigla_uf": row.get("siglaUf"),
        "codigo_municipio": row.get("codigoMunicipio"),
        "codigo_municipio_ibge": row.get("codigoMunicipioIbge"),
        "nome_municipio_ibge": row.get("nomeMunicipioIbge"),
        "codigo_unidade_polo": row.get("codigoUnidadePolo"),
        "nome_unidade_polo": row.get("nomeUnidadePolo"),
        "codigo_unidade_espelho": row.get("codigoUnidadeEspelho"),
        "nome_unidade_espelho": row.get("nomeUnidadeEspelho"),
    }


def _uasg_orgao_link_fields(row: dict[str, Any]) -> dict[str, Any]:
    """Extrai o código do órgão e os CNPJ/CPF do órgão, do vinculado e do superior."""
    return {
        "codigo_orgao": row.get("codigoOrgao"),
        "cnpj_cpf_orgao": row.get("cnpjCpfOrgao"),
        "cnpj_cpf_orgao_vinculado": row.get("cnpjCpfOrgaoVinculado"),
        "cnpj_cpf_orgao_superior": row.get("cnpjCpfOrgaoSuperior"),
    }


def _orgao_identity_fields(row: dict[str, Any]) -> dict[str, Any]:
    """Extrai código, nome, mnemônico, CNPJ/CPF, status e data de movimento do órgão."""
    return {
        "codigo_orgao": row["codigoOrgao"],
        "nome_orgao": row["nomeOrgao"],
        "nome_mnemonico_orgao": row.get("nomeMnemonicoOrgao"),
        "cnpj_cpf_orgao": row.get("cnpjCpfOrgao"),
        "status_orgao": row["statusOrgao"],
        "data_hora_movimento": row.get("dataHoraMovimento"),
    }


def _orgao_hierarchy_fields(row: dict[str, Any]) -> dict[str, Any]:
    """Extrai código, CNPJ/CPF e nome do órgão vinculado e do órgão superior."""
    return {
        "codigo_orgao_vinculado": row.get("codigoOrgaoVinculado"),
        "cnpj_cpf_orgao_vinculado": row.get("cnpjCpfOrgaoVinculado"),
        "nome_orgao_vinculado": row.get("nomeOrgaoVinculado"),
        "codigo_orgao_superior": row.get("codigoOrgaoSuperior"),
        "cnpj_cpf_orgao_superior": row.get("cnpjCpfOrgaoSuperior"),
        "nome_orgao_superior": row.get("nomeOrgaoSuperior"),
    }


def _orgao_admin_fields(row: dict[str, Any]) -> dict[str, Any]:
    """Extrai tipo de administração, poder, esfera e uso do SISG do órgão."""
    return {
        "codigo_tipo_administracao": row.get("codigoTipoAdministracao"),
        "nome_tipo_administracao": row.get("nomeTipoAdministracao"),
        "poder": row.get("poder"),
        "esfera": row.get("esfera"),
        "uso_sisg": row.get("usoSisg"),
    }
