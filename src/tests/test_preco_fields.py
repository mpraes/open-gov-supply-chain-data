from etl.ingestion.precos.map_preco_fields import (
    preco_detalhe_fields,
    preco_material_fields,
    preco_servico_fields,
)


def test_preco_detalhe_fields_maps_identity_and_objeto() -> None:
    fields = preco_detalhe_fields(
        {
            "idCompra": 1,
            "idItemCompra": 2,
            "codigoItemCatalogo": 3,
            "objetoCompra": "obj",
        }
    )
    assert fields["id_compra"] == 1
    assert fields["id_item_compra"] == 2
    assert fields["objeto_compra"] == "obj"


def test_preco_servico_fields_maps_preco_unitario() -> None:
    fields = preco_servico_fields(
        {
            "idCompra": "c1",
            "idItemCompra": 2,
            "codigoItemCatalogo": 7250,
            "precoUnitario": 1.5,
        }
    )
    assert fields["preco_unitario"] == 1.5
    assert fields["codigo_uasg"] is None


def test_preco_material_fields_includes_marca() -> None:
    fields = preco_material_fields(
        {
            "idCompra": 1,
            "idItemCompra": 2,
            "codigoItemCatalogo": 3,
            "marca": "dell",
        }
    )
    assert fields["marca"] == "dell"
    assert fields["preco_unitario"] is None
