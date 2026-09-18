import pytest
from pydantic import ValidationError

from contracts.material_class import MaterialClassRecord


def test_material_class_record_uppercases_names() -> None:
    record = MaterialClassRecord(
        cod_classe=101,
        cod_grupo=10,
        nome_grupo="grupo material",
        nome_classe="classe material",
        status_classe=True,
        data_hora_atualizacao="2024-01-15T10:30:00",
    )
    assert record.nome_grupo == "GRUPO MATERIAL"
    assert record.nome_classe == "CLASSE MATERIAL"


def test_material_class_record_rejects_empty_nome_classe() -> None:
    with pytest.raises(ValidationError):
        MaterialClassRecord(
            cod_classe=101,
            cod_grupo=10,
            nome_grupo="GRUPO",
            nome_classe="   ",
            status_classe=True,
            data_hora_atualizacao="2024-01-15T10:30:00",
        )


def test_material_class_record_rejects_non_int_cod_classe() -> None:
    with pytest.raises(ValidationError):
        MaterialClassRecord(
            cod_classe="101",  # type: ignore[arg-type]
            cod_grupo=10,
            nome_grupo="GRUPO",
            nome_classe="CLASSE",
            status_classe=True,
            data_hora_atualizacao="2024-01-15T10:30:00",
        )
