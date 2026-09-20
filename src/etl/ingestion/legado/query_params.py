from clients.compras_api import QueryParams


def legado_licitacao_query_params(
    data_inicial: str,
    data_final: str,
    uasg: int | None = None,
) -> QueryParams:
    """Query params for consultarLicitacao by publication window.

    Example:
        legado_licitacao_query_params("2024-01-01", "2024-12-31")
    """
    return _with_optional_int(
        {
            "data_publicacao_inicial": data_inicial,
            "data_publicacao_final": data_final,
        },
        "uasg",
        uasg,
    )


def legado_item_licitacao_query_params(
    modalidade: int,
    uasg: int | None = None,
) -> QueryParams:
    """Query params for consultarItemLicitacao by modalidade.

    Example:
        legado_item_licitacao_query_params(5)
    """
    return _with_optional_int({"modalidade": modalidade}, "uasg", uasg)


def legado_pregao_query_params(
    data_inicial: str,
    data_final: str,
    uasg: int | None = None,
) -> QueryParams:
    """Query params for consultarPregoes by edital window.

    Example:
        legado_pregao_query_params("2024-01-01", "2024-06-30")
    """
    return _with_optional_int(
        {
            "dt_data_edital_inicial": data_inicial,
            "dt_data_edital_final": data_final,
        },
        "co_uasg",
        uasg,
    )


def legado_item_pregao_query_params(
    data_inicial: str,
    data_final: str,
    uasg: int | None = None,
) -> QueryParams:
    """Query params for consultarItensPregoes by homologação window.

    Example:
        legado_item_pregao_query_params("2024-01-01", "2024-06-30")
    """
    return _with_optional_int(
        {"dt_hom_inicial": data_inicial, "dt_hom_final": data_final},
        "co_uasg",
        uasg,
    )


def legado_compra_sem_licitacao_query_params(
    ano: int,
    uasg: int | None = None,
) -> QueryParams:
    """Query params for consultarComprasSemLicitacao by aviso year.

    Example:
        legado_compra_sem_licitacao_query_params(2024)
    """
    return _with_optional_int({"dt_ano_aviso": ano}, "co_uasg", uasg)


def legado_item_sem_licitacao_query_params(
    ano: int,
    uasg: int | None = None,
) -> QueryParams:
    """Query params for consultarCompraItensSemLicitacao by aviso year.

    Example:
        legado_item_sem_licitacao_query_params(2024)
    """
    return _with_optional_int({"dt_ano_aviso_licitacao": ano}, "co_uasg", uasg)


def legado_rdc_query_params(
    data_inicial: str,
    data_final: str,
    uasg: int | None = None,
) -> QueryParams:
    """Query params for consultarRdc by publication window.

    Example:
        legado_rdc_query_params("2024-01-01", "2024-12-31")
    """
    return _with_optional_int(
        {"data_publicacao_min": data_inicial, "data_publicacao_max": data_final},
        "uasg",
        uasg,
    )


def legado_job_name(script: str, *parts: object) -> str:
    """Resume-cursor name including the active filter slice.

    Example:
        legado_job_name("legado_licitacao", "2024-01-01", "2024-12-31")
    """
    tokens = [script, *[str(part) for part in parts if part is not None]]
    return ":".join(tokens)


def _with_optional_int(
    params: dict[str, str | int],
    key: str,
    value: int | None,
) -> QueryParams:
    if value is None:
        return params
    params[key] = value
    return params
