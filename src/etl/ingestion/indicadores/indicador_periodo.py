from config.load_secret_key import load_secret_key_func
from etl.ingestion.remaining_filters import indicadores_ano
from etl.ingestion.remaining_maps import map_indicador_periodo_row
from etl.ingestion.remaining_query_params import (
    indicador_periodo_query_params,
    slice_job_name,
)
from etl.ingestion.remaining_run import run_remaining_ingestion
from etl.ingestion.script_runner import DEFAULT_ENV_PATH


def main() -> None:
    ano = indicadores_ano(DEFAULT_ENV_PATH, load_secret_key_func)
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
