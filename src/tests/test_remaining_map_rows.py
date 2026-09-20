from etl.ingestion.remaining_maps import (
    map_alice_aviso_row,
    map_arp_empenho_row,
    map_arp_row,
    map_contratacao_row,
    map_contrato_row,
    map_fornecedor_row,
    map_indicador_periodo_row,
    map_ocds_release_row,
)


def test_map_contratacao_row_snakes_and_uppercases() -> None:
    record = map_contratacao_row(
        {
            "idCompra": 12,
            "objetoCompra": " notebook ",
            "valorTotalEstimado": "10,5",
            "modalidadeNome": "pregao",
        }
    )
    dumped = record.model_dump()
    assert dumped["id_compra"] == "12"
    assert dumped["objeto_compra"] == "NOTEBOOK"
    assert dumped["valor_total_estimado"] == 10.5


def test_map_arp_row_uses_pncp_ata_key() -> None:
    record = map_arp_row(
        {"numeroControlePncpAta": "ata-1", "objeto": " registro ", "valorTotal": 3}
    )
    assert record.numero_controle_pncp_ata == "ata-1"
    assert record.model_dump()["objeto"] == "REGISTRO"


def test_map_arp_empenho_row_injects_filter_keys() -> None:
    record = map_arp_empenho_row(
        {"numeroItem": "2", "unidade": "153001", "saldoEmpenho": 1},
        numero_ata="10",
        unidade_gerenciadora="36000",
    )
    dumped = record.model_dump()
    assert dumped["numero_ata"] == "10"
    assert dumped["unidade_gerenciadora"] == "36000"
    assert dumped["numero_item"] == "2"


def test_map_contrato_row_requires_pncp_id() -> None:
    record = map_contrato_row(
        {"numeroControlePncpContrato": "c-1", "objeto": " servico "}
    )
    assert record.numero_controle_pncp_contrato == "c-1"


def test_map_fornecedor_row_prefers_cnpj() -> None:
    record = map_fornecedor_row(
        {"cnpj": "00394460000112", "cpf": "", "nomeRazaoSocialFornecedor": " acme "}
    )
    assert record.ni_fornecedor == "00394460000112"
    assert record.model_dump()["nome_razao_social_fornecedor"] == "ACME"


def test_map_indicador_periodo_row() -> None:
    record = map_indicador_periodo_row({"anoMes": "2024-01", "ano": 2024, "mes": 1})
    assert record.ano_mes == "2024-01"


def test_map_ocds_release_row_flattens_buyer() -> None:
    record = map_ocds_release_row(
        {
            "ocid": "ocds-1",
            "id": "rel-1",
            "buyer": {"id": "BR-1", "name": " orgao "},
            "tender": {"id": "t1", "title": " compra "},
        }
    )
    dumped = record.model_dump()
    assert dumped["buyer_id"] == "BR-1"
    assert dumped["buyer_name"] == "ORGAO"
    assert '"ocid": "ocds-1"' in dumped["release_json"]


def test_map_alice_aviso_row() -> None:
    record = map_alice_aviso_row(
        {"ticketAnalise": "t-1", "chaveCompra": " compra-1 ", "tipoAnalise": 2}
    )
    assert record.ticket_analise == "t-1"
    assert record.model_dump()["chave_compra"] == "COMPRA-1"
