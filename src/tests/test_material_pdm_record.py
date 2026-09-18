import pytest
from pydantic import ValidationError

from contracts.material_pdm import MaterialPdmRecord


def test_material_pdm_record_uppercases_names() -> None:
    record = MaterialPdmRecord(
        cod_pdm=1001,
        cod_classe=101,
        cod_grupo=10,
        nome_grupo="grupo material",
        nome_classe="classe material",
        nome_pdm="pdm material",
        status_pdm=True,
        data_hora_atualizacao="2024-01-15T10:30:00",
    )
    assert record.nome_grupo == "GRUPO MATERIAL"
    assert record.nome_classe == "CLASSE MATERIAL"
    assert record.nome_pdm == "PDM MATERIAL"


def test_material_pdm_record_rejects_empty_nome_pdm() -> None:
    with pytest.raises(ValidationError):
        MaterialPdmRecord(
            cod_pdm=1001,
            cod_classe=101,
            cod_grupo=10,
            nome_grupo="GRUPO",
            nome_classe="CLASSE",
            nome_pdm="   ",
            status_pdm=True,
            data_hora_atualizacao="2024-01-15T10:30:00",
        )


def test_material_pdm_record_rejects_non_int_cod_pdm() -> None:
    with pytest.raises(ValidationError):
        MaterialPdmRecord(
            cod_pdm="1001",  # type: ignore[arg-type]
            cod_classe=101,
            cod_grupo=10,
            nome_grupo="GRUPO",
            nome_classe="CLASSE",
            nome_pdm="PDM",
            status_pdm=True,
            data_hora_atualizacao="2024-01-15T10:30:00",
        )
