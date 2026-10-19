"""Mapeia os objetos dos endpoints do módulo legado para as colunas das tabelas de destino."""

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
    """Mapeia as chaves de consultarLicitacao para os campos de LegadoLicitacaoRecord.

    Exemplo:
        legado_licitacao_fields({"id_compra": "123", "objeto": "x"})
    """
    return pick_row_fields(row, LICITACAO_REQUIRED, LICITACAO_COLUMNS)


def legado_item_licitacao_fields(row: dict[str, Any]) -> dict[str, Any]:
    """Mapeia as chaves de consultarItemLicitacao para os campos de LegadoItemLicitacaoRecord.

    Exemplo:
        legado_item_licitacao_fields({"id_compra": "c1", "id_compra_item": "i1"})
    """
    return pick_row_fields(row, ITEM_LICITACAO_REQUIRED, ITEM_LICITACAO_COLUMNS)


def legado_pregao_fields(row: dict[str, Any]) -> dict[str, Any]:
    """Mapeia as chaves de consultarPregoes para os campos de LegadoPregaoRecord.

    Exemplo:
        legado_pregao_fields({"id_compra": "p1", "no_ausg": "x"})
    """
    return pick_row_fields(row, PREGAO_REQUIRED, PREGAO_COLUMNS)


def legado_item_pregao_fields(row: dict[str, Any]) -> dict[str, Any]:
    """Mapeia as chaves de consultarItensPregoes para os campos de LegadoItemPregaoRecord.

    Exemplo:
        legado_item_pregao_fields({"id_compra": "p1", "id_compra_item": "i1"})
    """
    return pick_row_fields(row, ITEM_PREGAO_REQUIRED, ITEM_PREGAO_COLUMNS)


def legado_compra_sem_licitacao_fields(row: dict[str, Any]) -> dict[str, Any]:
    """Mapeia as chaves de consultarComprasSemLicitacao para o registro de dispensa.

    Exemplo:
        legado_compra_sem_licitacao_fields({"id_compra": "d1"})
    """
    return pick_row_fields(row, COMPRA_SEM_REQUIRED, COMPRA_SEM_COLUMNS)


def legado_item_sem_licitacao_fields(row: dict[str, Any]) -> dict[str, Any]:
    """Mapeia as chaves de consultarCompraItensSemLicitacao para o registro de item de dispensa.

    Exemplo:
        legado_item_sem_licitacao_fields({"id_compra": "d1", "id_compra_item": "i2"})
    """
    return pick_row_fields(row, ITEM_SEM_REQUIRED, ITEM_SEM_COLUMNS)


def legado_rdc_fields(row: dict[str, Any]) -> dict[str, Any]:
    """Mapeia as chaves de consultarRdc para os campos de LegadoRdcRecord.

    Exemplo:
        legado_rdc_fields({"identificador": "rdc-1"})
    """
    return pick_row_fields(row, RDC_REQUIRED, RDC_COLUMNS)


def pick_row_fields(
    row: dict[str, Any],
    required: tuple[str, ...],
    columns: tuple[str, ...],
) -> dict[str, Any]:
    """Copia as chaves obrigatórias da API e as colunas opcionais de um objeto resultado.

    Exemplo:
        pick_row_fields({"id": 1}, ("id",), ("id", "nome"))
    """
    fields: dict[str, Any] = {}
    for key in columns:
        fields[key] = row[key] if key in required else row.get(key)
    return fields
