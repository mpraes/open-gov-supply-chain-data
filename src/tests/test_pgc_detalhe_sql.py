import pytest

from etl.ingestion.planejamento.pgc_detalhe_sql import pgc_detalhe_upsert_sql


def test_pgc_detalhe_upsert_sql_targets_allowed_table() -> None:
    sql = pgc_detalhe_upsert_sql("pgc_detalhe")
    assert "INSERT INTO staging.pgc_detalhe" in sql
    assert "ON CONFLICT (codigo_uasg, numero_artefato, ano_artefato, ordem_dfd, codigo_item_catalogo, ano_pca_projeto_compra)" in sql
    assert "data_hora_carga = now()" in sql


def test_pgc_detalhe_upsert_sql_targets_catalogo_table() -> None:
    sql = pgc_detalhe_upsert_sql("pgc_detalhe_catalogo")
    assert "INSERT INTO staging.pgc_detalhe_catalogo" in sql


def test_pgc_detalhe_upsert_sql_rejects_unknown_table() -> None:
    with pytest.raises(ValueError, match="table expected pgc_detalhe or pgc_detalhe_catalogo, got 'other'"):
        pgc_detalhe_upsert_sql("other")
