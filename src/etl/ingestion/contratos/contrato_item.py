"""Ingere itens de contrato na tabela contrato_item por órgão."""

from etl.ingestion.dest_watermark import DateWatermark
from etl.ingestion.full_dump import full_dump_dates
from etl.ingestion.orgao_catalog import read_orgao_codes
from etl.ingestion.remaining_maps import map_contrato_item_row
from etl.ingestion.remaining_query_params import contrato_query_params
from etl.ingestion.remaining_run import run_sliced_remaining_ingestion


def main() -> None:
    """Percorre os órgãos da carga completa e consulta /modulo-contratos/2_consultarContratosItem, gravando na tabela contrato_item."""
    inicial, final = full_dump_dates()
    for code in read_orgao_codes():
        _ingest_orgao(str(code), inicial, final)


def _ingest_orgao(orgao: str, inicial: str, final: str) -> None:
    """Consulta /modulo-contratos/2_consultarContratosItem do órgão em fatias de vigência inicial e grava na tabela contrato_item."""
    run_sliced_remaining_ingestion(
        data_inicial=inicial,
        data_final=final,
        params_for_slice=lambda start, end: contrato_query_params(orgao, start, end),
        job_prefix=f"contrato_item:{orgao}",
        logger_name="contrato_item",
        endpoint_path="/modulo-contratos/2_consultarContratosItem",
        table_name="contrato_item",
        map_row=map_contrato_item_row,
        date_watermark=DateWatermark(
            table="contrato_item",
            column="data_vigencia_inicial",
            start_param="dataVigenciaInicialMin",
            end_param="dataVigenciaInicialMax",
            where={"codigo_orgao": orgao},
        ),
    )


if __name__ == "__main__":
    main()
