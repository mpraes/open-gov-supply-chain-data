from typing import Any

from etl.ingestion.dest_schema import dest_table

_HEADER_CHILDREN = frozenset({"arp_empenho"})
_ITEM_CHILDREN = frozenset({"arp_unidade_item", "arp_adesao"})
AtaHeader = tuple[str, str]
AtaItem = tuple[str, str, str]


def missing_ata_headers(conn: Any, child_table: str) -> list[AtaHeader]:
    """Return dest ARP headers that have no rows in an ARP child table.

    Example:
        missing_ata_headers(conn, "arp_empenho")
    """
    child = _require_child(child_table, _HEADER_CHILDREN)
    sql = (
        "SELECT DISTINCT src.numero_ata_registro_preco, src.codigo_unidade_gerenciadora "
        f"FROM {dest_table('arp')} src WHERE src.numero_ata_registro_preco IS NOT NULL "
        "AND src.codigo_unidade_gerenciadora IS NOT NULL AND NOT EXISTS ("
        f"SELECT 1 FROM {dest_table(child)} dest WHERE dest.numero_ata = src.numero_ata_registro_preco "
        "AND dest.unidade_gerenciadora = src.codigo_unidade_gerenciadora)"
    )
    return [_header_pair(row, index) for index, row in enumerate(_fetch_all(conn, sql))]


def missing_ata_item_triples(conn: Any, child_table: str) -> list[AtaItem]:
    """Return dest ARP item keys missing from a child table.

    Example:
        missing_ata_item_triples(conn, "arp_unidade_item")
    """
    child = _require_child(child_table, _ITEM_CHILDREN)
    sql = _item_missing_sql(child, match_item=child != "arp_adesao")
    return [_item_triple(row, index) for index, row in enumerate(_fetch_all(conn, sql))]


def table_has_rows(conn: Any, table: str) -> bool:
    """Return True when dest table has at least one row.

    Example:
        table_has_rows(conn, "arp")
    """
    ident = dest_table(table)
    with conn.cursor() as cur:
        cur.execute(f"SELECT 1 FROM {ident} LIMIT 1")
        return cur.fetchone() is not None


def resolve_empenho_keys(conn: Any, fallback: AtaHeader) -> list[AtaHeader]:
    """Use dest ARP headers when present, otherwise the env ATA pair."""
    if table_has_rows(conn, "arp"):
        return missing_ata_headers(conn, "arp_empenho")
    return [fallback]


def resolve_item_keys(conn: Any, child_table: str, fallback: AtaItem) -> list[AtaItem]:
    """Use dest ARP item keys when present, otherwise the env ATA triple."""
    if table_has_rows(conn, "arp_item"):
        return missing_ata_item_triples(conn, child_table)
    return [fallback]


def _item_missing_sql(child: str, *, match_item: bool) -> str:
    item_clause = ""
    if match_item:
        item_clause = " AND dest.numero_item = src.numero_item"
    return (
        "SELECT DISTINCT src.numero_ata_registro_preco, src.codigo_unidade_gerenciadora, "
        "src.numero_item FROM "
        f"{dest_table('arp_item')} src "
        "WHERE src.numero_ata_registro_preco IS NOT NULL "
        "AND src.codigo_unidade_gerenciadora IS NOT NULL "
        "AND src.numero_item IS NOT NULL AND NOT EXISTS ("
        f"SELECT 1 FROM {dest_table(child)} dest WHERE dest.numero_ata = src.numero_ata_registro_preco "
        f"AND dest.unidade_gerenciadora = src.codigo_unidade_gerenciadora{item_clause})"
    )


def _require_child(child_table: str, allowed: frozenset[str]) -> str:
    if child_table not in allowed:
        raise ValueError(
            f"child_table expected one of {sorted(allowed)}, got {child_table!r}"
        )
    return child_table


def _fetch_all(conn: Any, sql: str) -> list[tuple[object, ...]]:
    with conn.cursor() as cur:
        cur.execute(sql)
        rows = cur.fetchall()
    return rows


def _header_pair(row: object, index: int) -> AtaHeader:
    values = _text_cells(row, index, 2)
    return values[0], values[1]


def _item_triple(row: object, index: int) -> AtaItem:
    values = _text_cells(row, index, 3)
    return values[0], values[1], values[2]


def _text_cells(row: object, index: int, expected: int) -> list[str]:
    if not isinstance(row, (tuple, list)) or len(row) != expected:
        raise ValueError(
            f"expected ARP key row[{index}] to be a {expected}-tuple, got {row!r}"
        )
    cells: list[str] = []
    for value in row:
        if not isinstance(value, str) or not value:
            raise ValueError(
                f"expected ARP key row[{index}] cells to be non-empty str, got {row!r}"
            )
        cells.append(value)
    return cells
