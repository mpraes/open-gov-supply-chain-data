def build_upsert_sql(
    table_name: str,
    columns: tuple[str, ...],
    conflict: tuple[str, ...],
) -> str:
    """Build INSERT ... ON CONFLICT DO UPDATE with data_hora_carga.

    Example:
        build_upsert_sql("t", ("id", "nome"), ("id",))
    """
    if not table_name.replace("_", "").isalnum() or table_name[0].isdigit():
        raise ValueError(f"table expected snake_case identifier, got {table_name!r}")
    cols = ", ".join(columns)
    values = ", ".join(f"%({name})s" for name in columns)
    keys = ", ".join(conflict)
    updates = ",\n".join(
        f"{name} = EXCLUDED.{name}" for name in columns if name not in conflict
    )
    return (
        f"INSERT INTO {table_name} ({cols})\n"
        f"VALUES ({values})\n"
        f"ON CONFLICT ({keys}) DO UPDATE SET\n"
        f"{updates},\n"
        "data_hora_carga = now();"
    )
