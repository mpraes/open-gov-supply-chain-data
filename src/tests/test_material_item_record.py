import pytest
from pydantic import ValidationError

from contracts.material_item import MaterialItemRecord


def _valid_item_kwargs() -> dict[str, object]:
    return {
        "cod_item": 9001,
        "cod_grupo": 10,
        "nome_grupo": "grupo material",
        "cod_classe": 101,
        "nome_classe": "classe material",
        "cod_pdm": 1001,
        "nome_pdm": "pdm material",
        "descricao_item": "item material",
        "status_item": True,
        "item_sustentavel": False,
        "codigo_ncm": "12345678",
        "descricao_ncm": "ncm descricao",
        "aplica_margem_preferencia": True,
        "data_hora_atualizacao": "2024-01-15T10:30:00",
    }


def test_material_item_record_uppercases_text_fields() -> None:
    record = MaterialItemRecord(**_valid_item_kwargs())  # type: ignore[arg-type]
    assert record.nome_grupo == "GRUPO MATERIAL"
    assert record.nome_classe == "CLASSE MATERIAL"
    assert record.nome_pdm == "PDM MATERIAL"
    assert record.descricao_item == "ITEM MATERIAL"
    assert record.descricao_ncm == "NCM DESCRICAO"


def test_material_item_record_rejects_empty_descricao_item() -> None:
    kwargs = _valid_item_kwargs()
    kwargs["descricao_item"] = "   "
    with pytest.raises(ValidationError):
        MaterialItemRecord(**kwargs)  # type: ignore[arg-type]


def test_material_item_record_rejects_non_int_cod_item() -> None:
    kwargs = _valid_item_kwargs()
    kwargs["cod_item"] = "9001"
    with pytest.raises(ValidationError):
        MaterialItemRecord(**kwargs)  # type: ignore[arg-type]


def test_material_item_record_accepts_null_optional_fields() -> None:
    kwargs = _valid_item_kwargs()
    kwargs["codigo_ncm"] = None
    kwargs["descricao_ncm"] = None
    kwargs["aplica_margem_preferencia"] = None
    record = MaterialItemRecord(**kwargs)  # type: ignore[arg-type]
    assert record.codigo_ncm is None
    assert record.descricao_ncm is None
    assert record.aplica_margem_preferencia is None
