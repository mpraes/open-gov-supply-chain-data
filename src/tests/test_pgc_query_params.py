from etl.ingestion.planejamento.query_params import (
    pgc_agregacao_query_params,
    pgc_catalogo_query_params,
    pgc_detalhe_query_params,
)


def test_pgc_detalhe_query_params_requires_orgao_and_year() -> None:
    assert pgc_detalhe_query_params("36000", 2026) == {
        "orgao": "36000",
        "anoPcaProjetoCompra": 2026,
    }


def test_pgc_detalhe_query_params_includes_optional_uasg() -> None:
    assert pgc_detalhe_query_params("36000", 2026, codigo_uasg="153001") == {
        "orgao": "36000",
        "anoPcaProjetoCompra": 2026,
        "codigoUasg": "153001",
    }


def test_pgc_catalogo_query_params_uses_tipo_and_codigo() -> None:
    assert pgc_catalogo_query_params(101, tipo="Material", ano=2026) == {
        "anoPcaProjetoCompra": 2026,
        "tipo": "Material",
        "codigo": 101,
    }


def test_pgc_agregacao_query_params_uses_ano() -> None:
    assert pgc_agregacao_query_params("36000", 2026) == {
        "orgao": "36000",
        "ano": 2026,
    }
