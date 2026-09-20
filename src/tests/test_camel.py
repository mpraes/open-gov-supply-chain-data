from contracts.camel import camel_to_snake, snake_row


def test_camel_to_snake_splits_id_and_acronyms() -> None:
    assert camel_to_snake("idCompra") == "id_compra"
    assert camel_to_snake("orgaoEntidadeCnpj") == "orgao_entidade_cnpj"
    assert camel_to_snake("numeroControlePNCP") == "numero_controle_pncp"
    assert camel_to_snake("codigoNCM") == "codigo_ncm"


def test_snake_row_renames_keys() -> None:
    assert snake_row({"idCompra": "1", "valorTotal": 2}) == {
        "id_compra": "1",
        "valor_total": 2,
    }
