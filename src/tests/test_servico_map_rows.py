from etl.ingestion.servico.servico_classe import map_servico_classe_row
from etl.ingestion.servico.servico_divisao import map_servico_divisao_row
from etl.ingestion.servico.servico_grupo import map_servico_grupo_row
from etl.ingestion.servico.servico_item import map_servico_item_row
from etl.ingestion.servico.servico_natureza_despesa import map_servico_natureza_despesa_row
from etl.ingestion.servico.servico_secao import map_servico_secao_row
from etl.ingestion.servico.servico_subclasse import map_servico_subclasse_row
from etl.ingestion.servico.servico_unidade_medida import map_servico_unidade_medida_row


def test_map_servico_secao_row() -> None:
    record = map_servico_secao_row(
        {
            "codigoSecao": 1,
            "nomeSecao": "secao",
            "statusSecao": True,
            "dataHoraAtualizacao": "2024-01-15T10:30:00",
        }
    )
    assert record.cod_secao == 1
    assert record.nome_secao == "SECAO"


def test_map_servico_divisao_row() -> None:
    record = map_servico_divisao_row(
        {
            "codigoSecao": 1,
            "nomeSecao": "s",
            "codigoDivisao": 2,
            "nomeDivisao": "d",
            "statusDivisao": True,
            "dataHoraAtualizacao": "2024-01-15T10:30:00",
        }
    )
    assert record.cod_divisao == 2


def test_map_servico_grupo_row() -> None:
    record = map_servico_grupo_row(
        {
            "nomeSecao": "s",
            "codigoDivisao": 2,
            "nomeDivisao": "d",
            "codigoGrupo": 3,
            "nomeGrupo": "g",
            "statusGrupo": True,
            "dataHoraAtualizacao": "2024-01-15T10:30:00",
        }
    )
    assert record.cod_grupo == 3


def test_map_servico_classe_row_uses_status_grupo_api_field() -> None:
    record = map_servico_classe_row(
        {
            "codigoGrupo": 3,
            "nomeGrupo": "g",
            "codigoClasse": 4,
            "nomeClasse": "c",
            "statusGrupo": False,
            "dataHoraAtualizacao": "2024-01-15T10:30:00",
        }
    )
    assert record.cod_classe == 4
    assert record.status_classe is False


def test_map_servico_subclasse_row() -> None:
    record = map_servico_subclasse_row(
        {
            "codigoClasse": 4,
            "nomeClasse": "c",
            "codigoSubclasse": 5,
            "nomeSubclasse": "sc",
            "statusSubclasse": True,
            "dataHoraAtualizacao": "2024-01-15T10:30:00",
        }
    )
    assert record.cod_subclasse == 5


def test_map_servico_item_row() -> None:
    record = map_servico_item_row(
        {
            "codigoSecao": 1,
            "nomeSecao": "s",
            "codigoDivisao": 2,
            "nomeDivisao": "d",
            "codigoGrupo": 3,
            "nomeGrupo": "g",
            "codigoClasse": 4,
            "nomeClasse": "c",
            "codigoSubclasse": 5,
            "nomeSubclasse": "sc",
            "codigoServico": 100,
            "nomeServico": "servico",
            "codigoCpc": 9,
            "exclusivoCentralCompras": True,
            "statusServico": True,
            "dataHoraAtualizacao": "2024-01-15T10:30:00",
        }
    )
    assert record.cod_servico == 100
    assert record.exclusivo_central_compras is True


def test_map_servico_unidade_medida_row() -> None:
    record = map_servico_unidade_medida_row(
        {
            "codigoServico": 100,
            "siglaUnidadeMedida": "un",
            "nomeUnidadeMedida": "unidade",
            "statusUnidadeMedida": True,
        }
    )
    assert record.sigla_unidade_medida == "UN"


def test_map_servico_natureza_despesa_row() -> None:
    record = map_servico_natureza_despesa_row(
        {
            "codigoServico": 100,
            "codigoNaturezaDespesa": "339039",
            "nomeNaturezaDespesa": "servicos",
            "statusNaturezaDespesa": True,
        }
    )
    assert record.cod_natureza_despesa == "339039"
