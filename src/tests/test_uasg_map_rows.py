from etl.ingestion.uasg.uasg import map_uasg_row
from etl.ingestion.uasg.uasg_orgao import map_uasg_orgao_row


def test_map_uasg_row() -> None:
    record = map_uasg_row(
        {
            "codigoUasg": "153001",
            "nomeUasg": "uasg centro",
            "usoSisg": True,
            "adesaoSiasg": True,
            "siglaUf": "df",
            "codigoMunicipio": 1,
            "codigoMunicipioIbge": 5300108,
            "nomeMunicipioIbge": "brasilia",
            "codigoUnidadePolo": 2,
            "nomeUnidadePolo": "polo",
            "codigoUnidadeEspelho": 3,
            "nomeUnidadeEspelho": "espelho",
            "uasgCadastradora": False,
            "cnpjCpfUasg": "00394460005887",
            "codigoOrgao": 36000,
            "cnpjCpfOrgao": "00394460000112",
            "cnpjCpfOrgaoVinculado": "00394460000200",
            "cnpjCpfOrgaoSuperior": "00394460000380",
            "codigoSiorg": "1234",
            "statusUasg": True,
            "dataImplantacaoSidec": "2024-01-15T10:30:00",
            "dataHoraMovimento": "2024-01-16T11:00:00",
        }
    )
    assert record.codigo_uasg == "153001"
    assert record.nome_uasg == "UASG CENTRO"
    assert record.codigo_orgao == 36000
    assert record.status_uasg is True


def test_map_uasg_orgao_row() -> None:
    record = map_uasg_orgao_row(
        {
            "codigoOrgao": 36000,
            "nomeOrgao": "ministerio",
            "nomeMnemonicoOrgao": "mp",
            "cnpjCpfOrgao": "00394460000112",
            "codigoOrgaoVinculado": 10,
            "cnpjCpfOrgaoVinculado": "1",
            "nomeOrgaoVinculado": "vinculado",
            "codigoOrgaoSuperior": 20,
            "cnpjCpfOrgaoSuperior": "2",
            "nomeOrgaoSuperior": "superior",
            "codigoTipoAdministracao": 1,
            "nomeTipoAdministracao": "direta",
            "poder": "executivo",
            "esfera": "federal",
            "usoSisg": True,
            "statusOrgao": True,
            "dataHoraMovimento": "2024-01-15T10:30:00",
        }
    )
    assert record.codigo_orgao == 36000
    assert record.nome_orgao == "MINISTERIO"
    assert record.status_orgao is True
