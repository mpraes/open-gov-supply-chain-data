from etl.ingestion.uasg.map_uasg_fields import uasg_fields, uasg_orgao_fields


def test_uasg_fields_maps_identity_and_location() -> None:
    fields = uasg_fields(
        {
            "codigoUasg": "153001",
            "nomeUasg": "uasg centro",
            "siglaUf": "DF",
            "codigoMunicipioIbge": 5300108,
            "nomeMunicipioIbge": "brasilia",
            "statusUasg": True,
            "dataHoraMovimento": "2024-01-15T10:30:00",
        }
    )
    assert fields["codigo_uasg"] == "153001"
    assert fields["nome_uasg"] == "uasg centro"
    assert fields["sigla_uf"] == "DF"
    assert fields["codigo_municipio_ibge"] == 5300108
    assert fields["status_uasg"] is True
    assert fields["codigo_orgao"] is None


def test_uasg_orgao_fields_maps_hierarchy() -> None:
    fields = uasg_orgao_fields(
        {
            "codigoOrgao": 36000,
            "nomeOrgao": "ministerio",
            "nomeOrgaoSuperior": "presidencia",
            "poder": "executivo",
            "statusOrgao": False,
        }
    )
    assert fields["codigo_orgao"] == 36000
    assert fields["nome_orgao"] == "ministerio"
    assert fields["nome_orgao_superior"] == "presidencia"
    assert fields["poder"] == "executivo"
    assert fields["status_orgao"] is False
    assert fields["esfera"] is None
