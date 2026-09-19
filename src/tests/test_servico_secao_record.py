import pytest
from pydantic import ValidationError

from contracts.servico_secao import ServicoSecaoRecord


def test_servico_secao_uppercases_nome() -> None:
    record = ServicoSecaoRecord(
        cod_secao=1,
        nome_secao=" secao a ",
        status_secao=True,
        data_hora_atualizacao="2024-01-15T10:30:00",
    )
    assert record.nome_secao == "SECAO A"


def test_servico_secao_rejects_empty_nome() -> None:
    with pytest.raises(ValidationError):
        ServicoSecaoRecord(
            cod_secao=1,
            nome_secao="  ",
            status_secao=True,
            data_hora_atualizacao="2024-01-15T10:30:00",
        )


def test_servico_secao_rejects_non_int_cod() -> None:
    with pytest.raises(ValidationError):
        ServicoSecaoRecord(
            cod_secao="1",  # type: ignore[arg-type]
            nome_secao="x",
            status_secao=True,
            data_hora_atualizacao="2024-01-15T10:30:00",
        )
