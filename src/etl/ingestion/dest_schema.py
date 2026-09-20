import re

DEST_SCHEMA = "staging"
_SQL_IDENT = re.compile(r"^[a-z][a-z0-9_]*$")


def require_sql_ident(value: str, label: str) -> str:
    """Reject identifiers that cannot be interpolated into SQL.

    Example:
        require_sql_ident("preco_material", "table") == "preco_material"
    """
    if _SQL_IDENT.fullmatch(value) is None:
        raise ValueError(f"{label} expected snake_case identifier, got {value!r}")
    return value


def dest_table(table: str) -> str:
    """Qualify a dest table with the staging schema.

    Example:
        dest_table("preco_material") == "staging.preco_material"
    """
    schema = require_sql_ident(DEST_SCHEMA, "schema")
    ident = require_sql_ident(table, "table")
    return f"{schema}.{ident}"


def search_path_options(schema: str = DEST_SCHEMA) -> str:
    """libpq options that set search_path for this connection.

    Example:
        search_path_options() == "-c search_path=staging"
    """
    ident = require_sql_ident(schema, "schema")
    return f"-c search_path={ident}"
