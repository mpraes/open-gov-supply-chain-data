from etl.ingestion.remaining_columns import TABLE_SPECS
from etl.ingestion.upsert_sql import build_upsert_sql
from etl.ingestion.write_text_tables import text_table_sql


def test_text_table_sql_marks_pk_not_null() -> None:
    sql = text_table_sql("arp", ("numero_controle_pncp_ata", "objeto"), ("numero_controle_pncp_ata",))
    assert "numero_controle_pncp_ata TEXT NOT NULL" in sql
    assert "PRIMARY KEY (numero_controle_pncp_ata)" in sql


def test_build_upsert_sql_for_contratacao() -> None:
    columns, conflict = TABLE_SPECS["contratacao"]
    sql = build_upsert_sql("contratacao", columns, conflict)
    assert "INSERT INTO contratacao" in sql
    assert "ON CONFLICT (id_compra)" in sql
    assert "data_hora_carga = now()" in sql
