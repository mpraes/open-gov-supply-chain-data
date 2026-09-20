import pytest

from etl.ingestion.legado.legado_sql import legado_upsert_sql


def test_legado_upsert_sql_conflicts_on_id_compra() -> None:
    sql = legado_upsert_sql("legado_licitacao")
    assert "INSERT INTO legado_licitacao" in sql
    assert "ON CONFLICT (id_compra)" in sql
    assert "data_hora_carga = now()" in sql


def test_legado_upsert_sql_conflicts_on_item_pair() -> None:
    sql = legado_upsert_sql("legado_item_licitacao")
    assert "ON CONFLICT (id_compra, id_compra_item)" in sql


def test_legado_upsert_sql_conflicts_on_rdc_identificador() -> None:
    sql = legado_upsert_sql("legado_rdc")
    assert "ON CONFLICT (identificador)" in sql


def test_legado_upsert_sql_rejects_unknown_table() -> None:
    with pytest.raises(ValueError, match="table expected legado_"):
        legado_upsert_sql("other")
