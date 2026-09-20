from etl.ingestion.legado.legado_columns import (
    COMPRA_SEM_COLUMNS,
    ITEM_LICITACAO_COLUMNS,
    ITEM_PREGAO_COLUMNS,
    ITEM_SEM_COLUMNS,
    LICITACAO_COLUMNS,
    PREGAO_COLUMNS,
    RDC_COLUMNS,
)

_TABLES: dict[str, tuple[tuple[str, ...], tuple[str, ...]]] = {
    "legado_licitacao": (LICITACAO_COLUMNS, ("id_compra",)),
    "legado_item_licitacao": (ITEM_LICITACAO_COLUMNS, ("id_compra", "id_compra_item")),
    "legado_pregao": (PREGAO_COLUMNS, ("id_compra",)),
    "legado_item_pregao": (ITEM_PREGAO_COLUMNS, ("id_compra", "id_compra_item")),
    "legado_compra_sem_licitacao": (COMPRA_SEM_COLUMNS, ("id_compra",)),
    "legado_item_sem_licitacao": (ITEM_SEM_COLUMNS, ("id_compra", "id_compra_item")),
    "legado_rdc": (RDC_COLUMNS, ("identificador",)),
}


def legado_upsert_sql(table_name: str) -> str:
    """Build the upsert statement for a LEGADO table.

    Example:
        sql = legado_upsert_sql("legado_licitacao")
    """
    spec = _TABLES.get(table_name)
    if spec is None:
        allowed = ", ".join(sorted(_TABLES))
        raise ValueError(f"table expected legado_* ({allowed}), got {table_name!r}")
    columns, conflict = spec
    return _build_upsert_sql(table_name, columns, conflict)


def _build_upsert_sql(
    table_name: str,
    columns: tuple[str, ...],
    conflict: tuple[str, ...],
) -> str:
    cols = ", ".join(columns)
    values = ", ".join(f"%({name})s" for name in columns)
    keys = ", ".join(conflict)
    updates = _excluded_updates(columns, conflict)
    return (
        f"INSERT INTO {table_name} ({cols})\n"
        f"VALUES ({values})\n"
        f"ON CONFLICT ({keys}) DO UPDATE SET\n"
        f"{updates},\n"
        "data_hora_carga = now();"
    )


def _excluded_updates(columns: tuple[str, ...], conflict: tuple[str, ...]) -> str:
    names = [name for name in columns if name not in conflict]
    return ",\n".join(f"{name} = EXCLUDED.{name}" for name in names)
