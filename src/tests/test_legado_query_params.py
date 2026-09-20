from etl.ingestion.legado.query_params import (
    legado_compra_sem_licitacao_query_params,
    legado_item_licitacao_query_params,
    legado_item_pregao_query_params,
    legado_item_sem_licitacao_query_params,
    legado_job_name,
    legado_licitacao_query_params,
    legado_pregao_query_params,
    legado_rdc_query_params,
)


def test_legado_licitacao_query_params_requires_dates() -> None:
    assert legado_licitacao_query_params("2024-01-01", "2024-12-31") == {
        "data_publicacao_inicial": "2024-01-01",
        "data_publicacao_final": "2024-12-31",
    }


def test_legado_licitacao_query_params_includes_optional_uasg() -> None:
    params = legado_licitacao_query_params("2024-01-01", "2024-12-31", uasg=153001)
    assert params["uasg"] == 153001


def test_legado_item_licitacao_query_params_requires_modalidade() -> None:
    assert legado_item_licitacao_query_params(5) == {"modalidade": 5}


def test_legado_pregao_query_params_uses_edital_dates() -> None:
    assert legado_pregao_query_params("2024-01-01", "2024-06-30") == {
        "dt_data_edital_inicial": "2024-01-01",
        "dt_data_edital_final": "2024-06-30",
    }


def test_legado_item_pregao_query_params_uses_homologacao_dates() -> None:
    assert legado_item_pregao_query_params("2024-01-01", "2024-06-30") == {
        "dt_hom_inicial": "2024-01-01",
        "dt_hom_final": "2024-06-30",
    }


def test_legado_compra_sem_licitacao_query_params_uses_ano() -> None:
    assert legado_compra_sem_licitacao_query_params(2024) == {"dt_ano_aviso": 2024}


def test_legado_item_sem_licitacao_query_params_uses_ano() -> None:
    assert legado_item_sem_licitacao_query_params(2024) == {
        "dt_ano_aviso_licitacao": 2024
    }


def test_legado_rdc_query_params_uses_publicacao_range() -> None:
    assert legado_rdc_query_params("2024-01-01", "2024-12-31") == {
        "data_publicacao_min": "2024-01-01",
        "data_publicacao_max": "2024-12-31",
    }


def test_legado_job_name_joins_filter_parts() -> None:
    assert legado_job_name("legado_licitacao", "2024-01-01", "2024-12-31") == (
        "legado_licitacao:2024-01-01:2024-12-31"
    )
    assert legado_job_name("legado_item_licitacao", 5, None) == "legado_item_licitacao:5"
