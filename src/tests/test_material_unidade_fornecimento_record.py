import pytest
from pydantic import ValidationError

from contracts.material_unidade_fornecimento import MaterialUnidadeFornecimentoRecord


def _valid_kwargs() -> dict[str, object]:
    return {
        "cod_pdm": 1001,
        "sigla_unidade_fornecimento": "un",
        "nome_unidade_fornecimento": "unidade",
        "descricao_unidade_fornecimento": "unidade de fornecimento",
        "sigla_unidade_medida": "un",
        "capacidade_unidade_fornecimento": 1,
        "numero_sequencial_unidade_fornecimento": 1,
        "status_unidade_fornecimento_pdm": True,
        "status_unidade_fornecimento": True,
        "data_hora_atualizacao": "2024-01-15T10:30:00",
    }


def test_material_unidade_fornecimento_uppercases_text_fields() -> None:
    record = MaterialUnidadeFornecimentoRecord(**_valid_kwargs())  # type: ignore[arg-type]
    assert record.sigla_unidade_fornecimento == "UN"
    assert record.nome_unidade_fornecimento == "UNIDADE"
    assert record.descricao_unidade_fornecimento == "UNIDADE DE FORNECIMENTO"
    assert record.sigla_unidade_medida == "UN"


def test_material_unidade_fornecimento_rejects_non_int_cod_pdm() -> None:
    kwargs = _valid_kwargs()
    kwargs["cod_pdm"] = "1001"
    with pytest.raises(ValidationError):
        MaterialUnidadeFornecimentoRecord(**kwargs)  # type: ignore[arg-type]


def test_material_unidade_fornecimento_accepts_null_optional_fields() -> None:
    kwargs = _valid_kwargs()
    kwargs["nome_unidade_fornecimento"] = None
    kwargs["descricao_unidade_fornecimento"] = None
    kwargs["sigla_unidade_medida"] = None
    kwargs["capacidade_unidade_fornecimento"] = None
    kwargs["status_unidade_fornecimento_pdm"] = None
    kwargs["status_unidade_fornecimento"] = None
    kwargs["data_hora_atualizacao"] = None
    record = MaterialUnidadeFornecimentoRecord(**kwargs)  # type: ignore[arg-type]
    assert record.nome_unidade_fornecimento is None
    assert record.descricao_unidade_fornecimento is None
    assert record.capacidade_unidade_fornecimento is None


def test_material_unidade_fornecimento_accepts_float_capacidade() -> None:
    kwargs = _valid_kwargs()
    kwargs["capacidade_unidade_fornecimento"] = 300.0
    record = MaterialUnidadeFornecimentoRecord(**kwargs)  # type: ignore[arg-type]
    assert record.capacidade_unidade_fornecimento == 300.0


def test_material_unidade_fornecimento_blank_optional_text_becomes_none() -> None:
    kwargs = _valid_kwargs()
    kwargs["descricao_unidade_fornecimento"] = ""
    kwargs["nome_unidade_fornecimento"] = "   "
    record = MaterialUnidadeFornecimentoRecord(**kwargs)  # type: ignore[arg-type]
    assert record.descricao_unidade_fornecimento is None
    assert record.nome_unidade_fornecimento is None
