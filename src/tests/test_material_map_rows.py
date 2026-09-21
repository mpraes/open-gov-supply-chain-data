from etl.ingestion.material.material_caracteristica import map_material_caracteristica_row
from etl.ingestion.material.material_class import map_material_class_row
from etl.ingestion.material.material_group import map_material_group_row
from etl.ingestion.material.material_item import map_material_item_row
from etl.ingestion.material.material_natureza_despesa import (
    map_material_natureza_despesa_row,
)
from etl.ingestion.material.material_pdm import map_material_pdm_row
from etl.ingestion.material.material_unidade_fornecimento import (
    map_material_unidade_fornecimento_row,
)


def test_map_material_group_row_maps_api_keys() -> None:
    record = map_material_group_row(
        {
            "codigoGrupo": 10,
            "nomeGrupo": "grupo",
            "statusGrupo": True,
            "dataHoraAtualizacao": "2024-01-01T00:00:00",
        }
    )
    assert record.cod_grupo == 10
    assert record.nome_grupo == "GRUPO"


def test_map_material_class_row_maps_api_keys() -> None:
    record = map_material_class_row(
        {
            "codigoClasse": 101,
            "codigoGrupo": 10,
            "nomeGrupo": "grupo",
            "nomeClasse": "classe",
            "statusClasse": True,
            "dataHoraAtualizacao": "2024-01-01T00:00:00",
        }
    )
    assert record.cod_classe == 101
    assert record.nome_classe == "CLASSE"


def test_map_material_pdm_row_maps_api_keys() -> None:
    record = map_material_pdm_row(
        {
            "codigoPdm": 1001,
            "codigoClasse": 101,
            "codigoGrupo": 10,
            "nomeGrupo": "grupo",
            "nomeClasse": "classe",
            "nomePdm": "pdm",
            "statusPdm": True,
            "dataHoraAtualizacao": "2024-01-01T00:00:00",
        }
    )
    assert record.cod_pdm == 1001
    assert record.nome_pdm == "PDM"


def test_map_material_item_row_maps_api_keys() -> None:
    record = map_material_item_row(
        {
            "codigoItem": 9001,
            "codigoGrupo": 10,
            "nomeGrupo": "grupo",
            "codigoClasse": 101,
            "nomeClasse": "classe",
            "codigoPdm": 1001,
            "nomePdm": "pdm",
            "descricaoItem": "item",
            "statusItem": True,
            "itemSustentavel": False,
            "codigo_ncm": "12345678",
            "descricao_ncm": "ncm",
            "aplica_margem_preferencia": True,
            "dataHoraAtualizacao": "2024-01-01T00:00:00",
        }
    )
    assert record.cod_item == 9001
    assert record.descricao_item == "ITEM"


def test_map_material_natureza_despesa_row_maps_api_keys() -> None:
    record = map_material_natureza_despesa_row(
        {
            "codigoPdm": 1001,
            "codigoNaturezaDespesa": "339030",
            "nomeNaturezaDespesa": "consumo",
            "statusNaturezaDespesa": "ativo",
        }
    )
    assert record.cod_natureza_despesa == "339030"
    assert record.nome_natureza_despesa == "CONSUMO"


def test_map_material_unidade_fornecimento_row_maps_api_keys() -> None:
    record = map_material_unidade_fornecimento_row(
        {
            "codigoPdm": 1001,
            "siglaUnidadeFornecimento": "un",
            "nomeUnidadeFornecimento": "unidade",
            "descricaoUnidadeFornecimento": "desc",
            "siglaUnidadeMedida": "un",
            "capacidadeUnidadeFornecimento": 1.5,
            "numeroSequencialUnidadeFornecimento": 1,
            "statusUnidadeFornecimentoPdm": True,
            "statusUnidadeFornecimento": True,
            "dataHoraAtualizacao": "2024-01-01T00:00:00",
        }
    )
    assert record.numero_sequencial_unidade_fornecimento == 1
    assert record.sigla_unidade_fornecimento == "UN"


def test_map_material_caracteristica_row_maps_api_keys() -> None:
    record = map_material_caracteristica_row(
        {
            "codigoItem": 9001,
            "itemSustentavel": True,
            "statusItem": True,
            "codigoCaracteristica": "c1",
            "nomeCaracteristica": "cor",
            "statusCaracteristica": True,
            "codigoValorCaracteristica": "v1",
            "nomeValorCaracteristica": "azul",
            "statusValorCaracteristica": True,
            "numeroCaracteristica": 1,
            "siglaUnidadeMedida": "un",
            "dataHoraAtualizacao": "2024-01-01T00:00:00",
        }
    )
    assert record.cod_item == 9001
    assert record.nome_caracteristica == "COR"


def test_map_material_caracteristica_row_accepts_null_codigo_valor() -> None:
    record = map_material_caracteristica_row(
        {
            "codigoItem": 19,
            "itemSustentavel": False,
            "statusItem": True,
            "codigoCaracteristica": "AAYZ",
            "nomeCaracteristica": "NOME",
            "statusCaracteristica": True,
            "codigoValorCaracteristica": None,
            "nomeValorCaracteristica": "JAPONA MASCULINA",
            "statusValorCaracteristica": None,
            "numeroCaracteristica": 1,
            "siglaUnidadeMedida": None,
            "dataHoraAtualizacao": "2024-05-14T03:00:00.143484",
        }
    )
    assert record.codigo_valor_caracteristica == "JAPONA MASCULINA"
    assert record.nome_valor_caracteristica == "JAPONA MASCULINA"
