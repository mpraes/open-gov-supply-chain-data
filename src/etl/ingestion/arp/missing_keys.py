"""Resolve chaves de ata ausentes nas tabelas filhas de ARP."""

from typing import Any

from etl.ingestion.dest_schema import dest_table

_HEADER_CHILDREN = frozenset({"arp_empenho"})
_ITEM_CHILDREN = frozenset({"arp_unidade_item", "arp_adesao"})
AtaHeader = tuple[str, str]
AtaItem = tuple[str, str, str]


def missing_ata_headers(conn: Any, child_table: str) -> list[AtaHeader]:
    """Retorna cabeçalhos de ARP no destino que não têm linhas numa tabela filha de ARP.

    Exemplo:
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
    """Retorna chaves de item de ARP no destino que faltam numa tabela filha.

    Exemplo:
        missing_ata_item_triples(conn, "arp_unidade_item")
    """
    child = _require_child(child_table, _ITEM_CHILDREN)
    sql = _item_missing_sql(child, match_item=child != "arp_adesao")
    return [_item_triple(row, index) for index, row in enumerate(_fetch_all(conn, sql))]


def table_has_rows(conn: Any, table: str) -> bool:
    """Retorna True quando a tabela de destino tem ao menos uma linha.

    Exemplo:
        table_has_rows(conn, "arp")
    """
    ident = dest_table(table)
    with conn.cursor() as cur:
        cur.execute(f"SELECT 1 FROM {ident} LIMIT 1")
        return cur.fetchone() is not None


def resolve_empenho_keys(conn: Any, fallback: AtaHeader | None) -> list[AtaHeader]:
    """Usa os cabeçalhos de ARP do destino quando existem; senão, o par de ATA do ambiente.

    Exemplo:
        resolve_empenho_keys(conn, None)
    """
    if table_has_rows(conn, "arp"):
        return missing_ata_headers(conn, "arp_empenho")
    if fallback is None:
        return []
    return [fallback]


def resolve_item_keys(
    conn: Any, child_table: str, fallback: AtaItem | None
) -> list[AtaItem]:
    """Usa as chaves de item de ARP do destino quando existem; senão, a tripla de ATA do ambiente.

    Exemplo:
        resolve_item_keys(conn, "arp_adesao", None)
    """
    if table_has_rows(conn, "arp_item"):
        return missing_ata_item_triples(conn, child_table)
    if fallback is None:
        return []
    return [fallback]


def _item_missing_sql(child: str, *, match_item: bool) -> str:
    """Monta o SELECT de itens de arp_item sem correspondente na tabela filha, confrontando numero_item quando pedido."""
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
    """Valida a tabela filha contra o conjunto permitido e devolve o nome aceito."""
    if child_table not in allowed:
        raise ValueError(
            f"child_table expected one of {sorted(allowed)}, got {child_table!r}"
        )
    return child_table


def _fetch_all(conn: Any, sql: str) -> list[tuple[object, ...]]:
    """Executa o SQL na conexão e devolve todas as linhas do cursor."""
    with conn.cursor() as cur:
        cur.execute(sql)
        rows = cur.fetchall()
    return rows


def _header_pair(row: object, index: int) -> AtaHeader:
    """Converte a linha em par de número da ata e código da unidade gerenciadora."""
    values = _text_cells(row, index, 2)
    return values[0], values[1]


def _item_triple(row: object, index: int) -> AtaItem:
    """Converte a linha em tripla de número da ata, unidade gerenciadora e número do item."""
    values = _text_cells(row, index, 3)
    return values[0], values[1], values[2]


def _text_cells(row: object, index: int, expected: int) -> list[str]:
    """Exige uma tupla do tamanho pedido com textos não vazios e devolve essas células."""
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
