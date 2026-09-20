from etl.ingestion.dest_schema import dest_table


def build_upsert_sql(
    table_name: str,
    columns: tuple[str, ...],
    conflict: tuple[str, ...],
) -> str:
    """Build INSERT ... ON CONFLICT DO UPDATE with data_hora_carga.

    Example:
        build_upsert_sql("t", ("id", "nome"), ("id",))
    """
    qualified = dest_table(table_name)
    cols = ", ".join(columns)
    values = ", ".join(f"%({name})s" for name in columns)
    keys = ", ".join(conflict)
    updates = ",\n".join(
        f"{name} = EXCLUDED.{name}" for name in columns if name not in conflict
    )
    return (
        f"INSERT INTO {qualified} ({cols})\n"
        f"VALUES ({values})\n"
        f"ON CONFLICT ({keys}) DO UPDATE SET\n"
        f"{updates},\n"
        "data_hora_carga = now();"
    )
