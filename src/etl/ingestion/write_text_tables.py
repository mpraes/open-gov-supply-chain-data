from pathlib import Path

from etl.ingestion.dest_schema import dest_table
from etl.ingestion.remaining_columns import TABLE_SPECS


def text_table_sql(table_name: str, columns: tuple[str, ...], conflict: tuple[str, ...]) -> str:
    """Build a TEXT-column CREATE TABLE for mixed API payloads.

    Example:
        text_table_sql("arp", ("id",), ("id",))
    """
    lines = [
        f"{name} TEXT NOT NULL" if name in conflict else f"{name} TEXT" for name in columns
    ]
    pk = ", ".join(conflict)
    return (
        f"CREATE TABLE {dest_table(table_name)} (\n"
        + ",\n".join(lines)
        + ",\ndata_hora_carga TIMESTAMPTZ DEFAULT now(),\n"
        + f"PRIMARY KEY ({pk})\n);\n"
    )


def write_remaining_table_sql(sql_dir: Path) -> list[Path]:
    """Write CREATE TABLE files for every remaining catalog spec.

    Example:
        write_remaining_table_sql(Path("src/sql"))
    """
    written: list[Path] = []
    for table_name, (columns, conflict) in TABLE_SPECS.items():
        path = sql_dir / f"create_table_{table_name}.sql"
        path.write_text(text_table_sql(table_name, columns, conflict), encoding="utf-8")
        written.append(path)
    return written


if __name__ == "__main__":
    root = Path(__file__).resolve().parents[2] / "sql"
    write_remaining_table_sql(root)
