from contracts.catalog_row import CatalogRow, normalize_catalog_row
from pydantic import ValidationError
import pytest


class SampleCatalogRow(CatalogRow):
    id_compra: str
    _float_fields = frozenset({"valor_total"})
    _name_fields = frozenset({"objeto"})


def test_normalize_catalog_row_uppercases_and_parses_amount() -> None:
    row = normalize_catalog_row(
        {"id_compra": 1, "objeto": " notebook ", "valor_total": "1,5", "extra": True},
        float_fields=frozenset({"valor_total"}),
        name_fields=frozenset({"objeto"}),
    )
    assert row["id_compra"] == 1
    assert row["objeto"] == "NOTEBOOK"
    assert row["valor_total"] == 1.5


def test_catalog_row_keeps_extra_fields() -> None:
    record = SampleCatalogRow(id_compra="c1", objeto=" x ", valor_total=2, modalidade=5)
    dumped = record.model_dump()
    assert dumped["id_compra"] == "c1"
    assert dumped["objeto"] == "X"
    assert dumped["valor_total"] == 2.0
    assert dumped["modalidade"] == 5


def test_catalog_row_requires_pk() -> None:
    with pytest.raises(ValidationError):
        SampleCatalogRow(objeto="x")
