from etl.ingestion.uasg.uasg import UPSERT_SQL as UASG_UPSERT_SQL
from etl.ingestion.uasg.uasg_orgao import UPSERT_SQL as ORGAO_UPSERT_SQL


def test_uasg_upsert_sql_conflicts_on_codigo() -> None:
    assert "INSERT INTO uasg" in UASG_UPSERT_SQL
    assert "ON CONFLICT (codigo_uasg)" in UASG_UPSERT_SQL
    assert "data_hora_carga = now()" in UASG_UPSERT_SQL


def test_uasg_orgao_upsert_sql_conflicts_on_codigo() -> None:
    assert "INSERT INTO uasg_orgao" in ORGAO_UPSERT_SQL
    assert "ON CONFLICT (codigo_orgao)" in ORGAO_UPSERT_SQL
    assert "data_hora_carga = now()" in ORGAO_UPSERT_SQL
