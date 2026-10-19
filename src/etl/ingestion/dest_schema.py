"""Qualifica tabelas e identificadores SQL do schema staging."""

import re

DEST_SCHEMA = "staging"
_SQL_IDENT = re.compile(r"^[a-z][a-z0-9_]*$")


def require_sql_ident(value: str, label: str) -> str:
    """Rejeita identificadores que não podem ser interpolados em SQL.

    Exemplo:
        require_sql_ident("preco_material", "table") == "preco_material"
    """
    if _SQL_IDENT.fullmatch(value) is None:
        raise ValueError(f"{label} expected snake_case identifier, got {value!r}")
    return value


def dest_table(table: str) -> str:
    """Qualifica uma tabela de destino com o schema staging.

    Exemplo:
        dest_table("preco_material") == "staging.preco_material"
    """
    schema = require_sql_ident(DEST_SCHEMA, "schema")
    ident = require_sql_ident(table, "table")
    return f"{schema}.{ident}"


def search_path_options(schema: str = DEST_SCHEMA) -> str:
    """Opções do libpq que definem search_path nesta conexão.

    Exemplo:
        search_path_options() == "-c search_path=staging"
    """
    ident = require_sql_ident(schema, "schema")
    return f"-c search_path={ident}"
