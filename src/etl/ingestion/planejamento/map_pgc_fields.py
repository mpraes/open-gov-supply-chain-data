from typing import Any


def pgc_detalhe_fields(row: dict[str, Any]) -> dict[str, Any]:
    """Map consultarPgcDetalhe API keys to PgcDetalheRecord fields.

    Example:
        pgc_detalhe_fields({"codigoUasg": "1", "orgao": "36000", ...})
    """
    return {
        **_pgc_detalhe_identity_fields(row),
        **_pgc_detalhe_artefato_fields(row),
        **_pgc_detalhe_dfd_fields(row),
        **_pgc_detalhe_material_fields(row),
        **_pgc_detalhe_servico_fields(row),
        **_pgc_detalhe_item_value_fields(row),
        **_pgc_detalhe_projeto_fields(row),
    }


def pgc_agregacao_fields(row: dict[str, Any]) -> dict[str, Any]:
    """Map consultarPgcAgregacao API keys to PgcAgregacaoRecord fields.

    Example:
        pgc_agregacao_fields({"orgao": "36000", "ano": 2026})
    """
    return {
        "orgao": row["orgao"],
        "ano": row["ano"],
        "poder": row.get("poder"),
        "esfera": row.get("esfera"),
        "data_hora_publicacao_pncp": row.get("dataHoraPublicacaoPncp"),
        "data_hora_atualizacao": row.get("dataHoraAtualizacao"),
        "quantidade_total_itens": row.get("quantidadeTotalItens"),
        "valor_total_estimado": row.get("valorTotalEstimado"),
    }


def _pgc_detalhe_identity_fields(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "codigo_uasg": row["codigoUasg"],
        "nome_uasg": row.get("nomeUasg"),
        "orgao": row["orgao"],
        "numero_artefato": row["numeroArtefato"],
        "ano_artefato": row["anoArtefato"],
        "ordem_dfd": row["ordemDfd"],
        "codigo_item_catalogo": row["codigoItemCatalogo"],
        "ano_pca_projeto_compra": row["anoPcaProjetoCompra"],
    }


def _pgc_detalhe_artefato_fields(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "codigo_estado_artefato": row.get("codigoEstadoArtefato"),
        "codigo_categoria_artefato": row.get("codigoCategoriaArtefato"),
        "descricao_artefato": row.get("descricaoArtefato"),
        "codigo_tipo_artefato": row.get("codigoTipoArtefato"),
    }


def _pgc_detalhe_dfd_fields(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "descricao_objeto_dfd": row.get("descricaoObjetoDfd"),
        "nivel_prioridade_dfd": row.get("nivelPrioridadeDfd"),
        "data_prevista_formalizacao_demanda": row.get("dataPrevistaFormalizacaoDemanda"),
        "codigo_area_dfd": row.get("codigoAreaDfd"),
        "tipo_item": row.get("tipoItem"),
        "item_sustentavel": row.get("itemSustentavel"),
    }


def _pgc_detalhe_material_fields(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "codigo_grupo_material": row.get("codigoGrupoMaterial"),
        "nome_grupo_material": row.get("nomeGrupoMaterial"),
        "codigo_classe_material": row.get("codigoClasseMaterial"),
        "nome_classe_material": row.get("nomeClasseMaterial"),
        "codigo_pdm_material": row.get("codigoPdmMaterial"),
        "nome_pdm_material": row.get("nomePdmMaterial"),
    }


def _pgc_detalhe_servico_fields(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "codigo_secao_servico": row.get("codigoSecaoServico"),
        "nome_secao_servico": row.get("nomeSecaoServico"),
        "codigo_divisao_servico": row.get("codigoDivisaoServico"),
        "nome_divisao_servico": row.get("nomeDivisaoServico"),
        "codigo_grupo_servico": row.get("codigoGrupoServico"),
        "nome_grupo_servico": row.get("nomeGrupoServico"),
        "codigo_classe_servico": row.get("codigoClasseServico"),
        "nome_classe_servico": row.get("nomeClasseServico"),
        "codigo_subclasse_servico": row.get("codigoSubclasseServico"),
        "nome_subclasse_servico": row.get("nomeSubclasseServico"),
    }


def _pgc_detalhe_item_value_fields(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "descricao_item_catalogo": row.get("descricaoItemCatalogo"),
        "sigla_unidade_fornecimento": row.get("siglaUnidadeFornecimento"),
        "nome_unidade_fornecimento": row.get("nomeUnidadeFornecimento"),
        "quantidade_item": row.get("quantidadeItem"),
        "valor_unitario_item": row.get("valorUnitarioItem"),
        "valor_total_item": row.get("valorTotalItem"),
    }


def _pgc_detalhe_projeto_fields(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "titulo_projeto_compra": row.get("tituloProjetoCompra"),
        "descricao_projeto_compra": row.get("descricaoProjetoCompra"),
        "data_inicio_processo_compra": row.get("dataInicioProcessoCompra"),
        "data_fim_processo_compra": row.get("dataFimProcessoCompra"),
        "duracao_processo_compra": row.get("duracaoProcessoCompra"),
        "numero_item_pncp": row.get("numeroItemPncp"),
        "status_contratacao_execucao": row.get("statusContratacaoExecucao"),
        "data_hora_publicacao_pncp": row.get("dataHoraPublicacaoPncp"),
        "data_hora_atualizacao_artefato": row.get("dataHoraAtualizacaoArtefato"),
        "data_hora_atualizacao_projeto_compra": row.get("dataHoraAtualizacaoProjetoCompra"),
        "data_hora_atualizacao_dfd": row.get("dataHoraAtualizacaoDfd"),
        "data_hora_atualizacao_item": row.get("dataHoraAtualizacaoItem"),
    }
