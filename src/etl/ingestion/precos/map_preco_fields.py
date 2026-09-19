from typing import Any


def preco_detalhe_fields(row: dict[str, Any]) -> dict[str, Any]:
    """Map consultar*Detalhe API keys to PrecoDetalheRecord fields.

    Example:
        preco_detalhe_fields({"idCompra": 1, "idItemCompra": 2, ...})
    """
    return {
        **_preco_identity_fields(row),
        "objeto_compra": row.get("objetoCompra"),
        "descricao_detalhada_item": row.get("descricaoDetalhadaItem"),
        "data_atualizacao_fato": row.get("dataAtualizacaoFato"),
    }


def preco_servico_fields(row: dict[str, Any]) -> dict[str, Any]:
    """Map consultarServico API keys to PrecoServicoRecord fields.

    Example:
        preco_servico_fields({"idCompra": "c1", "idItemCompra": 1, ...})
    """
    return {
        **_preco_identity_fields(row),
        **_preco_item_value_fields(row),
        **_preco_uasg_fields(row),
        **_preco_servico_detalhe_fields(row),
    }


def preco_material_fields(row: dict[str, Any]) -> dict[str, Any]:
    """Map consultarMaterial API keys to PrecoMaterialRecord fields.

    Example:
        preco_material_fields({"idCompra": 1, "marca": "x", ...})
    """
    return {
        **preco_servico_fields(row),
        **_preco_material_extra_fields(row),
    }


def _preco_identity_fields(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "id_compra": row["idCompra"],
        "id_item_compra": row["idItemCompra"],
        "numero_item_compra": row.get("numeroItemCompra"),
        "codigo_item_catalogo": row["codigoItemCatalogo"],
    }


def _preco_item_value_fields(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "forma": row.get("forma"),
        "modalidade": row.get("modalidade"),
        "criterio_julgamento": row.get("criterioJulgamento"),
        "descricao_item": row.get("descricaoItem"),
        "nome_unidade_medida": row.get("nomeUnidadeMedida"),
        "sigla_unidade_medida": row.get("siglaUnidadeMedida"),
        "quantidade": row.get("quantidade"),
        "preco_unitario": row.get("precoUnitario"),
        "percentual_maior_desconto": row.get("percentualMaiorDesconto"),
        "ni_fornecedor": row.get("niFornecedor"),
        "nome_fornecedor": row.get("nomeFornecedor"),
    }


def _preco_uasg_fields(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "codigo_uasg": row.get("codigoUasg"),
        "nome_uasg": row.get("nomeUasg"),
        "codigo_municipio": row.get("codigoMunicipio"),
        "municipio": row.get("municipio"),
        "estado": row.get("estado"),
        "codigo_orgao": row.get("codigoOrgao"),
        "nome_orgao": row.get("nomeOrgao"),
        "poder": row.get("poder"),
        "esfera": row.get("esfera"),
        "data_compra": row.get("dataCompra"),
        "data_hora_atualizacao_compra": row.get("dataHoraAtualizacaoCompra"),
        "data_hora_atualizacao_item": row.get("dataHoraAtualizacaoItem"),
        "data_resultado": row.get("dataResultado"),
        "data_hora_atualizacao_uasg": row.get("dataHoraAtualizacaoUasg"),
    }


def _preco_servico_detalhe_fields(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "objeto_compra": row.get("objetoCompra"),
        "descricao_detalhada_item": row.get("descricaoDetalhadaItem"),
        "data_atualizacao_fato": row.get("dataAtualizacaoFato"),
    }


def _preco_material_extra_fields(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "sigla_unidade_fornecimento": row.get("siglaUnidadeFornecimento"),
        "nome_unidade_fornecimento": row.get("nomeUnidadeFornecimento"),
        "capacidade_unidade_fornecimento": row.get("capacidadeUnidadeFornecimento"),
        "marca": row.get("marca"),
        "codigo_classe": row.get("codigoClasse"),
        "nome_classe": row.get("nomeClasse"),
        "id_compra_item": row.get("idCompraItem"),
        "codigo_pdm": row.get("codigoPdm"),
        "nome_pdm": row.get("nomePdm"),
    }
