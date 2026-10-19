from etl.ingestion.full_dump import for_each_dump_year
from etl.ingestion.remaining_maps import map_indicador_periodo_row
from etl.ingestion.remaining_query_params import (
    indicador_periodo_query_params,
    slice_job_name,
)
from etl.ingestion.remaining_run import run_remaining_ingestion


def main() -> None:
    for_each_dump_year(_ingest_year)


def _ingest_year(ano: int) -> None:
    run_remaining_ingestion(
        logger_name="indicador_periodo",
        endpoint_path="/modulo-indicadores/2_consultarIndicadoresPorPeriodo",
        table_name="indicador_periodo",
        map_row=map_indicador_periodo_row,
        query_params=indicador_periodo_query_params(ano),
        job_name=slice_job_name("indicador_periodo", ano),
    )


if __name__ == "__main__":
    main()
