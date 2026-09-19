import pytest
from pydantic import ValidationError

from contracts.uasg import UasgRecord
from contracts.uasg_orgao import UasgOrgaoRecord


def test_uasg_uppercases_names_and_keeps_codigo() -> None:
    record = UasgRecord(
        codigo_uasg=153001,
        nome_uasg=" uasg centro ",
        sigla_uf=" df ",
        nome_municipio_ibge=" brasilia ",
        cnpj_cpf_uasg=" 00394460005887 ",
        status_uasg=True,
    )
    assert record.codigo_uasg == "153001"
    assert record.nome_uasg == "UASG CENTRO"
    assert record.sigla_uf == "DF"
    assert record.nome_municipio_ibge == "BRASILIA"
    assert record.cnpj_cpf_uasg == "00394460005887"


def test_uasg_rejects_blank_nome() -> None:
    with pytest.raises(ValidationError):
        UasgRecord(codigo_uasg="153001", nome_uasg="  ", status_uasg=True)


def test_uasg_orgao_uppercases_names() -> None:
    record = UasgOrgaoRecord(
        codigo_orgao=36000,
        nome_orgao=" ministerio ",
        nome_mnemonico_orgao=" mp ",
        poder=" executivo ",
        esfera=" federal ",
        status_orgao=True,
    )
    assert record.nome_orgao == "MINISTERIO"
    assert record.nome_mnemonico_orgao == "MP"
    assert record.poder == "EXECUTIVO"
    assert record.esfera == "FEDERAL"


def test_uasg_orgao_rejects_non_int_codigo() -> None:
    with pytest.raises(ValidationError):
        UasgOrgaoRecord(
            codigo_orgao="36000",  # type: ignore[arg-type]
            nome_orgao="x",
            status_orgao=True,
        )
