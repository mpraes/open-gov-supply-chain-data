import pytest
from pydantic import ValidationError

from contracts.material_natureza_despesa import MaterialNaturezaDespesaRecord


def _valid_kwargs() -> dict[str, object]:
    return {
        "cod_pdm": 1001,
        "cod_natureza_despesa": "339030",
        "nome_natureza_despesa": "material de consumo",
        "status_natureza_despesa": "ativo",
    }


def test_material_natureza_despesa_uppercases_text_fields() -> None:
    record = MaterialNaturezaDespesaRecord(**_valid_kwargs())  # type: ignore[arg-type]
    assert record.nome_natureza_despesa == "MATERIAL DE CONSUMO"
    assert record.status_natureza_despesa == "ATIVO"
    assert record.cod_natureza_despesa == "339030"


def test_material_natureza_despesa_rejects_empty_nome() -> None:
    kwargs = _valid_kwargs()
    kwargs["nome_natureza_despesa"] = "   "
    with pytest.raises(ValidationError):
        MaterialNaturezaDespesaRecord(**kwargs)  # type: ignore[arg-type]


def test_material_natureza_despesa_accepts_null_nome() -> None:
    kwargs = _valid_kwargs()
    kwargs["nome_natureza_despesa"] = None
    record = MaterialNaturezaDespesaRecord(**kwargs)  # type: ignore[arg-type]
    assert record.nome_natureza_despesa is None


def test_material_natureza_despesa_rejects_non_int_cod_pdm() -> None:
    kwargs = _valid_kwargs()
    kwargs["cod_pdm"] = "1001"
    with pytest.raises(ValidationError):
        MaterialNaturezaDespesaRecord(**kwargs)  # type: ignore[arg-type]


def test_material_natureza_despesa_accepts_null_status() -> None:
    kwargs = _valid_kwargs()
    kwargs["status_natureza_despesa"] = None
    record = MaterialNaturezaDespesaRecord(**kwargs)  # type: ignore[arg-type]
    assert record.status_natureza_despesa is None
