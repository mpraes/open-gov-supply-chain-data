from config.load_secret_key import load_secret_key_func
from etl.ingestion.dest_watermark import DateWatermark
from etl.ingestion.remaining_filters import contratacoes_dates
from etl.ingestion.remaining_maps import map_contratacao_resultado_row
from etl.ingestion.remaining_query_params import (
    contratacao_resultado_query_params,
    slice_job_name,
)
from etl.ingestion.remaining_run import run_remaining_ingestion
from etl.ingestion.script_runner import DEFAULT_ENV_PATH


def main() -> None:
    inicial, final = contratacoes_dates(DEFAULT_ENV_PATH, load_secret_key_func)
    run_remaining_ingestion(
        logger_name="contratacao_resultado",
        endpoint_path="/modulo-contratacoes/3_consultarResultadoItensContratacoes_PNCP_14133",
        table_name="contratacao_resultado",
        map_row=map_contratacao_resultado_row,
        query_params=contratacao_resultado_query_params(inicial, final),
        job_name=slice_job_name("contratacao_resultado", inicial, final),
        date_watermark=DateWatermark(
            table="contratacao_resultado",
            column="data_resultado_pncp",
            start_param="dataResultadoPncpInicial",
            end_param="dataResultadoPncpFinal",
        ),
    )


if __name__ == "__main__":
    main()
