from typing import Any

from contracts.material_unidade_fornecimento import MaterialUnidadeFornecimentoRecord
from etl.ingestion.page_runner import run_page_batch_ingestion

ENDPOINT_PATH = "/modulo-material/6_consultarMaterialUnidadeFornecimento"
PAGE_SIZE = 500

UPSERT_SQL = """
INSERT INTO material_unidade_fornecimento (
    cod_pdm, numero_sequencial_unidade_fornecimento, sigla_unidade_fornecimento,
    nome_unidade_fornecimento, descricao_unidade_fornecimento, sigla_unidade_medida,
    capacidade_unidade_fornecimento, status_unidade_fornecimento_pdm,
    status_unidade_fornecimento, data_hora_atualizacao
)
VALUES (
    %(cod_pdm)s, %(numero_sequencial_unidade_fornecimento)s,
    %(sigla_unidade_fornecimento)s, %(nome_unidade_fornecimento)s,
    %(descricao_unidade_fornecimento)s, %(sigla_unidade_medida)s,
    %(capacidade_unidade_fornecimento)s, %(status_unidade_fornecimento_pdm)s,
    %(status_unidade_fornecimento)s, %(data_hora_atualizacao)s
)
ON CONFLICT (cod_pdm, numero_sequencial_unidade_fornecimento) DO UPDATE SET
sigla_unidade_fornecimento = EXCLUDED.sigla_unidade_fornecimento,
nome_unidade_fornecimento = EXCLUDED.nome_unidade_fornecimento,
descricao_unidade_fornecimento = EXCLUDED.descricao_unidade_fornecimento,
sigla_unidade_medida = EXCLUDED.sigla_unidade_medida,
capacidade_unidade_fornecimento = EXCLUDED.capacidade_unidade_fornecimento,
status_unidade_fornecimento_pdm = EXCLUDED.status_unidade_fornecimento_pdm,
status_unidade_fornecimento = EXCLUDED.status_unidade_fornecimento,
data_hora_atualizacao = EXCLUDED.data_hora_atualizacao,
data_hora_carga = now();
"""


def map_material_unidade_fornecimento_row(
    row: dict[str, Any],
) -> MaterialUnidadeFornecimentoRecord:
    """Map one API resultado object to MaterialUnidadeFornecimentoRecord.

    Example:
        record = map_material_unidade_fornecimento_row({"codigoPdm": 1, ...})
    """
    return MaterialUnidadeFornecimentoRecord(
        cod_pdm=row["codigoPdm"],
        sigla_unidade_fornecimento=row["siglaUnidadeFornecimento"],
        nome_unidade_fornecimento=row["nomeUnidadeFornecimento"],
        descricao_unidade_fornecimento=row["descricaoUnidadeFornecimento"],
        sigla_unidade_medida=row["siglaUnidadeMedida"],
        capacidade_unidade_fornecimento=row["capacidadeUnidadeFornecimento"],
        numero_sequencial_unidade_fornecimento=row["numeroSequencialUnidadeFornecimento"],
        status_unidade_fornecimento_pdm=row["statusUnidadeFornecimentoPdm"],
        status_unidade_fornecimento=row["statusUnidadeFornecimento"],
        data_hora_atualizacao=row["dataHoraAtualizacao"],
    )


def main() -> None:
    run_page_batch_ingestion(
        logger_name="material_unidade_fornecimento",
        endpoint_path=ENDPOINT_PATH,
        page_size=PAGE_SIZE,
        upsert_sql=UPSERT_SQL,
        map_row=map_material_unidade_fornecimento_row,
        table_name="material_unidade_fornecimento",
    )


if __name__ == "__main__":
    main()
