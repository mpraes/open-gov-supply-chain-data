from clients.compras_api import QueryParams


def contratacao_query_params(
    data_inicial: str,
    data_final: str,
    modalidade: int,
) -> QueryParams:
    """Required filters for consultarContratacoes_PNCP_14133."""
    return {
        "dataPublicacaoPncpInicial": data_inicial,
        "dataPublicacaoPncpFinal": data_final,
        "codigoModalidade": modalidade,
    }


def contratacao_item_query_params(data_inicial: str, data_final: str) -> QueryParams:
    """Required filters for consultarItensContratacoes_PNCP_14133."""
    return {
        "dataInclusaoPncpInicial": data_inicial,
        "dataInclusaoPncpFinal": data_final,
    }


def contratacao_resultado_query_params(data_inicial: str, data_final: str) -> QueryParams:
    """Required filters for consultarResultadoItensContratacoes_PNCP_14133."""
    return {
        "dataResultadoPncpInicial": data_inicial,
        "dataResultadoPncpFinal": data_final,
    }


def arp_query_params(data_inicial: str, data_final: str) -> QueryParams:
    """Required filters for consultarARP by initial validity."""
    return {
        "dataVigenciaInicialMin": data_inicial,
        "dataVigenciaInicialMax": data_final,
    }


def arp_fim_vigencia_query_params(data_inicial: str, data_final: str) -> QueryParams:
    """Required filters for consultarARP_FimVigencia."""
    return {
        "dataVigenciaFinalMin": data_inicial,
        "dataVigenciaFinalMax": data_final,
    }


def arp_ata_query_params(
    numero_ata: str,
    unidade_gerenciadora: str,
    numero_item: str | None = None,
) -> QueryParams:
    """Required ATA keys for ARP child endpoints 3/4/5."""
    params: dict[str, str | int | bool] = {
        "numeroAta": numero_ata,
        "unidadeGerenciadora": unidade_gerenciadora,
    }
    if numero_item is not None:
        params["numeroItem"] = numero_item
    return params


def contrato_query_params(
    orgao: str,
    data_inicial: str,
    data_final: str,
) -> QueryParams:
    """Required filters for consultarContratos."""
    return {
        "codigoOrgao": orgao,
        "dataVigenciaInicialMin": data_inicial,
        "dataVigenciaInicialMax": data_final,
    }


def contrato_fim_vigencia_query_params(
    orgao: str,
    data_inicial: str,
    data_final: str,
) -> QueryParams:
    """Required filters for consultarContratos_FimVigencia."""
    return {
        "codigoOrgao": orgao,
        "dataVigenciaFinalMin": data_inicial,
        "dataVigenciaFinalMax": data_final,
    }


def fornecedor_query_params(ativo: bool) -> QueryParams:
    """Required status filter for consultarFornecedor."""
    return {"ativo": ativo}


def indicador_periodo_query_params(ano: int) -> QueryParams:
    """Required year for consultarIndicadoresPorPeriodo."""
    return {"ano": ano}


def ocds_query_params(buyer_id: str, data_inicial: str, data_final: str) -> QueryParams:
    """Required filters for /modulo-ocds/1_releases."""
    return {
        "buyerID": buyer_id,
        "releaseStartDate": data_inicial,
        "releaseEndDate": data_final,
    }


def alice_aviso_query_params(data_inicial: str, data_final: str) -> QueryParams:
    """Required Alice interval in DD/MM/YYYY HH:MM:SS."""
    return {
        "dataInicioIntervalo": data_inicial,
        "dataFimIntervalo": data_final,
    }


def slice_job_name(script: str, *parts: object) -> str:
    """Resume-cursor name including the active filter slice."""
    tokens = [script, *[str(part) for part in parts if part is not None]]
    return ":".join(tokens)
