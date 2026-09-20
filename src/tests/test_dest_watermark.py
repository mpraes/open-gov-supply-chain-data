from datetime import datetime

import pytest

from etl.ingestion.dest_watermark import (
    DateWatermark,
    apply_date_watermark,
    iso_date_prefix,
    max_dest_iso_date,
    raise_date_window,
    rewrite_job_slice,
)


class FakeWatermarkCursor:
    def __init__(self, value: object) -> None:
        self.value = value
        self.sql: str | None = None
        self.params: object = None

    def execute(self, sql: str, params: object = None) -> None:
        self.sql = sql
        self.params = params

    def fetchone(self) -> tuple[object] | None:
        if self.value is None:
            return None
        return (self.value,)

    def __enter__(self) -> "FakeWatermarkCursor":
        return self

    def __exit__(self, *args: object) -> None:
        return None


class FakeWatermarkConnection:
    def __init__(self, cursor: FakeWatermarkCursor) -> None:
        self.cursor_obj = cursor

    def cursor(self) -> FakeWatermarkCursor:
        return self.cursor_obj


def test_raise_date_window_keeps_env_when_dest_empty() -> None:
    assert raise_date_window("2024-01-01", "2024-12-31", None) == (
        "2024-01-01",
        "2024-12-31",
    )


def test_raise_date_window_overlaps_dest_max_day() -> None:
    assert raise_date_window("2024-01-01", "2024-12-31", "2024-06-15") == (
        "2024-06-15",
        "2024-12-31",
    )


def test_raise_date_window_skips_when_dest_past_env_final() -> None:
    assert raise_date_window("2024-01-01", "2024-06-30", "2024-07-01") is None


def test_raise_date_window_still_fetches_when_dest_equals_final() -> None:
    assert raise_date_window("2024-01-01", "2024-06-15", "2024-06-15") == (
        "2024-06-15",
        "2024-06-15",
    )


def test_raise_date_window_does_not_lower_env_floor() -> None:
    assert raise_date_window("2024-06-01", "2024-12-31", "2024-01-15") == (
        "2024-06-01",
        "2024-12-31",
    )


def test_iso_date_prefix_from_text_and_timestamp() -> None:
    assert iso_date_prefix("2024-06-15 10:30:00") == "2024-06-15"
    assert iso_date_prefix(datetime(2024, 6, 15, 10, 30)) == "2024-06-15"
    assert iso_date_prefix("15/06/2024 10:30:00") == "2024-06-15"


def test_max_dest_iso_date_returns_none_when_empty() -> None:
    cursor = FakeWatermarkCursor(None)
    got = max_dest_iso_date(
        FakeWatermarkConnection(cursor),
        table="contratacao",
        column="data_publicacao_pncp",
    )
    assert got is None
    assert cursor.sql is not None
    assert "MAX(data_publicacao_pncp)" in cursor.sql
    assert "FROM contratacao" in cursor.sql


def test_max_dest_iso_date_normalizes_text_datetime() -> None:
    cursor = FakeWatermarkCursor("2024-06-15T10:30:00")
    got = max_dest_iso_date(
        FakeWatermarkConnection(cursor),
        table="contrato",
        column="data_vigencia_inicial",
        where={"codigo_orgao": "36000"},
    )
    assert got == "2024-06-15"
    assert cursor.params == {"codigo_orgao": "36000"}
    assert cursor.sql is not None
    assert "codigo_orgao = %(codigo_orgao)s" in cursor.sql


def test_max_dest_iso_date_rejects_unsafe_identifier() -> None:
    conn = FakeWatermarkConnection(FakeWatermarkCursor("2024-01-01"))
    with pytest.raises(ValueError, match="table expected snake_case identifier"):
        max_dest_iso_date(conn, table="contratacao;drop", column="data_publicacao_pncp")


def test_apply_date_watermark_rewrites_start_param() -> None:
    cursor = FakeWatermarkCursor("2024-06-15")
    params = apply_date_watermark(
        FakeWatermarkConnection(cursor),
        {
            "dataPublicacaoPncpInicial": "2024-01-01",
            "dataPublicacaoPncpFinal": "2024-12-31",
            "codigoModalidade": 6,
        },
        DateWatermark(
            table="contratacao",
            column="data_publicacao_pncp",
            start_param="dataPublicacaoPncpInicial",
            end_param="dataPublicacaoPncpFinal",
            where={"codigo_modalidade": "6"},
        ),
    )
    assert params is not None
    assert params["dataPublicacaoPncpInicial"] == "2024-06-15"
    assert params["dataPublicacaoPncpFinal"] == "2024-12-31"


def test_apply_date_watermark_returns_none_when_caught_up() -> None:
    cursor = FakeWatermarkCursor("2025-01-01")
    params = apply_date_watermark(
        FakeWatermarkConnection(cursor),
        {
            "dataPublicacaoPncpInicial": "2024-01-01",
            "dataPublicacaoPncpFinal": "2024-12-31",
        },
        DateWatermark(
            table="contratacao",
            column="data_publicacao_pncp",
            start_param="dataPublicacaoPncpInicial",
            end_param="dataPublicacaoPncpFinal",
        ),
    )
    assert params is None


def test_apply_date_watermark_raises_alice_start() -> None:
    cursor = FakeWatermarkCursor("15/06/2024 14:00:00")
    params = apply_date_watermark(
        FakeWatermarkConnection(cursor),
        {
            "dataInicioIntervalo": "01/01/2024 00:00:00",
            "dataFimIntervalo": "31/12/2024 23:59:59",
        },
        DateWatermark(
            table="alice_aviso",
            column="data_solicitacao_analise",
            start_param="dataInicioIntervalo",
            end_param="dataFimIntervalo",
            kind="alice",
        ),
    )
    assert params is not None
    assert params["dataInicioIntervalo"] == "15/06/2024 00:00:00"
    assert params["dataFimIntervalo"] == "31/12/2024 23:59:59"


def test_rewrite_job_slice_replaces_original_start() -> None:
    assert (
        rewrite_job_slice("contratacao:2024-01-01:2024-12-31:6", "2024-01-01", "2024-06-15")
        == "contratacao:2024-06-15:2024-12-31:6"
    )
