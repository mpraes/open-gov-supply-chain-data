from etl.ingestion.planejamento.map_pgc_fields import (
    pgc_agregacao_fields,
    pgc_detalhe_fields,
)


def test_pgc_detalhe_fields_maps_identity_and_values() -> None:
    fields = pgc_detalhe_fields(
        {
            "codigoUasg": "153001",
            "nomeUasg": "uasg",
            "orgao": "36000",
            "numeroArtefato": 12,
            "anoArtefato": 2026,
            "ordemDfd": 1,
            "codigoItemCatalogo": "449156",
            "descricaoItemCatalogo": "notebook",
            "anoPcaProjetoCompra": 2026,
            "quantidadeItem": 2,
            "valorUnitarioItem": 10.5,
            "nomeGrupoMaterial": "grupo",
        }
    )
    assert fields["codigo_uasg"] == "153001"
    assert fields["numero_artefato"] == 12
    assert fields["codigo_item_catalogo"] == "449156"
    assert fields["valor_unitario_item"] == 10.5
    assert fields["nome_grupo_material"] == "grupo"
    assert fields["codigo_secao_servico"] is None


def test_pgc_agregacao_fields_maps_totals() -> None:
    fields = pgc_agregacao_fields(
        {
            "orgao": "36000",
            "ano": 2026,
            "poder": "executivo",
            "valorTotalEstimado": 99.5,
        }
    )
    assert fields["orgao"] == "36000"
    assert fields["ano"] == 2026
    assert fields["valor_total_estimado"] == 99.5
    assert fields["esfera"] is None
