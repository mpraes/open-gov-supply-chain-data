from typing import Any

from etl.ingestion.legado.legado_columns import (
    COMPRA_SEM_COLUMNS,
    COMPRA_SEM_REQUIRED,
    ITEM_LICITACAO_COLUMNS,
    ITEM_LICITACAO_REQUIRED,
    ITEM_PREGAO_COLUMNS,
    ITEM_PREGAO_REQUIRED,
    ITEM_SEM_COLUMNS,
    ITEM_SEM_REQUIRED,
    LICITACAO_COLUMNS,
    LICITACAO_REQUIRED,
    PREGAO_COLUMNS,
    PREGAO_REQUIRED,
    RDC_COLUMNS,
    RDC_REQUIRED,
)


def legado_licitacao_fields(row: dict[str, Any]) -> dict[str, Any]:
    """Map consultarLicitacao keys to LegadoLicitacaoRecord fields.

    Example:
        legado_licitacao_fields({"id_compra": "123", "objeto": "x"})
    """
    return pick_row_fields(row, LICITACAO_REQUIRED, LICITACAO_COLUMNS)


def legado_item_licitacao_fields(row: dict[str, Any]) -> dict[str, Any]:
    """Map consultarItemLicitacao keys to LegadoItemLicitacaoRecord fields.

    Example:
        legado_item_licitacao_fields({"id_compra": "c1", "id_compra_item": "i1"})
    """
    return pick_row_fields(row, ITEM_LICITACAO_REQUIRED, ITEM_LICITACAO_COLUMNS)


def legado_pregao_fields(row: dict[str, Any]) -> dict[str, Any]:
    """Map consultarPregoes keys to LegadoPregaoRecord fields.

    Example:
        legado_pregao_fields({"id_compra": "p1", "no_ausg": "x"})
    """
    return pick_row_fields(row, PREGAO_REQUIRED, PREGAO_COLUMNS)


def legado_item_pregao_fields(row: dict[str, Any]) -> dict[str, Any]:
    """Map consultarItensPregoes keys to LegadoItemPregaoRecord fields.

    Example:
        legado_item_pregao_fields({"id_compra": "p1", "id_compra_item": "i1"})
    """
    return pick_row_fields(row, ITEM_PREGAO_REQUIRED, ITEM_PREGAO_COLUMNS)


def legado_compra_sem_licitacao_fields(row: dict[str, Any]) -> dict[str, Any]:
    """Map consultarComprasSemLicitacao keys to the dispensa record.

    Example:
        legado_compra_sem_licitacao_fields({"id_compra": "d1"})
    """
    return pick_row_fields(row, COMPRA_SEM_REQUIRED, COMPRA_SEM_COLUMNS)


def legado_item_sem_licitacao_fields(row: dict[str, Any]) -> dict[str, Any]:
    """Map consultarCompraItensSemLicitacao keys to the dispensa item record.

    Example:
        legado_item_sem_licitacao_fields({"id_compra": "d1", "id_compra_item": "i2"})
    """
    return pick_row_fields(row, ITEM_SEM_REQUIRED, ITEM_SEM_COLUMNS)


def legado_rdc_fields(row: dict[str, Any]) -> dict[str, Any]:
    """Map consultarRdc keys to LegadoRdcRecord fields.

    Example:
        legado_rdc_fields({"identificador": "rdc-1"})
    """
    return pick_row_fields(row, RDC_REQUIRED, RDC_COLUMNS)


def pick_row_fields(
    row: dict[str, Any],
    required: tuple[str, ...],
    columns: tuple[str, ...],
) -> dict[str, Any]:
    """Copy required API keys and optional columns from one resultado object.

    Example:
        pick_row_fields({"id": 1}, ("id",), ("id", "nome"))
    """
    fields: dict[str, Any] = {}
    for key in columns:
        fields[key] = row[key] if key in required else row.get(key)
    return fields
