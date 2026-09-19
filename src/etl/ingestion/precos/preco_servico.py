from typing import Any

from contracts.preco_servico import PrecoServicoRecord
from etl.ingestion.precos.batch_runner import run_preco_batch_ingestion
from etl.ingestion.precos.map_preco_fields import preco_servico_fields
from etl.ingestion.precos.query_params import catalogo_item_query_params

ENDPOINT_PATH = "/modulo-pesquisa-preco/3_consultarServico"
PAGE_SIZE = 100
BATCH_SIZE = 20
CATALOG_TABLE = "servico_item"
CATALOG_COLUMN = "cod_servico"

UPSERT_SQL = """
INSERT INTO preco_servico (
    id_compra, id_item_compra, numero_item_compra, codigo_item_catalogo,
    forma, modalidade, criterio_julgamento, descricao_item,
    nome_unidade_medida, sigla_unidade_medida, quantidade, preco_unitario,
    percentual_maior_desconto, ni_fornecedor, nome_fornecedor, codigo_uasg,
    nome_uasg, codigo_municipio, municipio, estado, codigo_orgao, nome_orgao,
    poder, esfera, data_compra, data_hora_atualizacao_compra,
    data_hora_atualizacao_item, data_resultado, data_hora_atualizacao_uasg,
    objeto_compra, descricao_detalhada_item, data_atualizacao_fato
)
VALUES (
    %(id_compra)s, %(id_item_compra)s, %(numero_item_compra)s, %(codigo_item_catalogo)s,
    %(forma)s, %(modalidade)s, %(criterio_julgamento)s, %(descricao_item)s,
    %(nome_unidade_medida)s, %(sigla_unidade_medida)s, %(quantidade)s, %(preco_unitario)s,
    %(percentual_maior_desconto)s, %(ni_fornecedor)s, %(nome_fornecedor)s, %(codigo_uasg)s,
    %(nome_uasg)s, %(codigo_municipio)s, %(municipio)s, %(estado)s, %(codigo_orgao)s,
    %(nome_orgao)s, %(poder)s, %(esfera)s, %(data_compra)s, %(data_hora_atualizacao_compra)s,
    %(data_hora_atualizacao_item)s, %(data_resultado)s, %(data_hora_atualizacao_uasg)s,
    %(objeto_compra)s, %(descricao_detalhada_item)s, %(data_atualizacao_fato)s
)
ON CONFLICT (id_compra, id_item_compra) DO UPDATE SET
numero_item_compra = EXCLUDED.numero_item_compra,
codigo_item_catalogo = EXCLUDED.codigo_item_catalogo,
forma = EXCLUDED.forma,
modalidade = EXCLUDED.modalidade,
criterio_julgamento = EXCLUDED.criterio_julgamento,
descricao_item = EXCLUDED.descricao_item,
nome_unidade_medida = EXCLUDED.nome_unidade_medida,
sigla_unidade_medida = EXCLUDED.sigla_unidade_medida,
quantidade = EXCLUDED.quantidade,
preco_unitario = EXCLUDED.preco_unitario,
percentual_maior_desconto = EXCLUDED.percentual_maior_desconto,
ni_fornecedor = EXCLUDED.ni_fornecedor,
nome_fornecedor = EXCLUDED.nome_fornecedor,
codigo_uasg = EXCLUDED.codigo_uasg,
nome_uasg = EXCLUDED.nome_uasg,
codigo_municipio = EXCLUDED.codigo_municipio,
municipio = EXCLUDED.municipio,
estado = EXCLUDED.estado,
codigo_orgao = EXCLUDED.codigo_orgao,
nome_orgao = EXCLUDED.nome_orgao,
poder = EXCLUDED.poder,
esfera = EXCLUDED.esfera,
data_compra = EXCLUDED.data_compra,
data_hora_atualizacao_compra = EXCLUDED.data_hora_atualizacao_compra,
data_hora_atualizacao_item = EXCLUDED.data_hora_atualizacao_item,
data_resultado = EXCLUDED.data_resultado,
data_hora_atualizacao_uasg = EXCLUDED.data_hora_atualizacao_uasg,
objeto_compra = EXCLUDED.objeto_compra,
descricao_detalhada_item = EXCLUDED.descricao_detalhada_item,
data_atualizacao_fato = EXCLUDED.data_atualizacao_fato,
data_hora_carga = now();
"""


def map_preco_servico_row(row: dict[str, Any]) -> PrecoServicoRecord:
    """Map one consultarServico resultado object to PrecoServicoRecord.

    Example:
        record = map_preco_servico_row({"idCompra": "c1", "idItemCompra": 1, ...})
    """
    return PrecoServicoRecord(**preco_servico_fields(row))


def main() -> None:
    run_preco_batch_ingestion(
        logger_name="preco_servico",
        endpoint_path=ENDPOINT_PATH,
        page_size=PAGE_SIZE,
        upsert_sql=UPSERT_SQL,
        map_row=map_preco_servico_row,
        table_name="preco_servico",
        catalog_table=CATALOG_TABLE,
        catalog_column=CATALOG_COLUMN,
        params_for_code=catalogo_item_query_params,
        batch_size=BATCH_SIZE,
    )


if __name__ == "__main__":
    main()
