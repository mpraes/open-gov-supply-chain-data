from etl.ingestion.remaining_query_params import (
    alice_aviso_query_params,
    arp_ata_query_params,
    arp_fim_vigencia_query_params,
    arp_query_params,
    contratacao_item_query_params,
    contratacao_query_params,
    contratacao_resultado_query_params,
    contrato_fim_vigencia_query_params,
    contrato_query_params,
    fornecedor_query_params,
    indicador_periodo_query_params,
    ocds_query_params,
    slice_job_name,
)


def test_contratacao_query_params_requires_dates_and_modalidade() -> None:
    assert contratacao_query_params("2024-01-01", "2024-12-31", 6) == {
        "dataPublicacaoPncpInicial": "2024-01-01",
        "dataPublicacaoPncpFinal": "2024-12-31",
        "codigoModalidade": 6,
    }


def test_arp_query_params_uses_vigencia_inicial() -> None:
    assert arp_query_params("2024-01-01", "2024-06-30") == {
        "dataVigenciaInicialMin": "2024-01-01",
        "dataVigenciaInicialMax": "2024-06-30",
    }


def test_arp_ata_query_params_includes_optional_item() -> None:
    assert arp_ata_query_params("1", "153001") == {
        "numeroAta": "1",
        "unidadeGerenciadora": "153001",
    }
    assert arp_ata_query_params("1", "153001", "3")["numeroItem"] == "3"


def test_contrato_query_params_requires_orgao() -> None:
    params = contrato_query_params("36000", "2024-01-01", "2024-12-31")
    assert params["codigoOrgao"] == "36000"


def test_fornecedor_and_ocds_and_alice_params() -> None:
    assert fornecedor_query_params(True) == {"ativo": True}
    assert ocds_query_params("00394460000112", "2024-01-01", "2024-01-31")["buyerID"] == (
        "00394460000112"
    )
    assert alice_aviso_query_params("01/01/2024 00:00:00", "31/01/2024 23:59:59")[
        "dataInicioIntervalo"
    ] == "01/01/2024 00:00:00"


def test_date_window_aliases() -> None:
    assert contratacao_item_query_params("2024-01-01", "2024-01-31")[
        "dataInclusaoPncpInicial"
    ] == "2024-01-01"
    assert contratacao_resultado_query_params("2024-01-01", "2024-01-31")[
        "dataResultadoPncpInicial"
    ] == "2024-01-01"
    assert arp_fim_vigencia_query_params("2024-01-01", "2024-01-31")[
        "dataVigenciaFinalMin"
    ] == "2024-01-01"
    assert contrato_fim_vigencia_query_params("36000", "2024-01-01", "2024-01-31")[
        "dataVigenciaFinalMax"
    ] == "2024-01-31"
    assert indicador_periodo_query_params(2024) == {"ano": 2024}


def test_slice_job_name_skips_none() -> None:
    assert slice_job_name("arp", "2024-01-01", None) == "arp:2024-01-01"
