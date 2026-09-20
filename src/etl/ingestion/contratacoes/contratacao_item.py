from config.load_secret_key import load_secret_key_func
from etl.ingestion.dest_watermark import DateWatermark
from etl.ingestion.remaining_filters import contratacoes_dates
from etl.ingestion.remaining_maps import map_contratacao_item_row
from etl.ingestion.remaining_query_params import (
    contratacao_item_query_params,
    slice_job_name,
)
from etl.ingestion.remaining_run import run_remaining_ingestion
from etl.ingestion.script_runner import DEFAULT_ENV_PATH


def main() -> None:
    inicial, final = contratacoes_dates(DEFAULT_ENV_PATH, load_secret_key_func)
    run_remaining_ingestion(
        logger_name="contratacao_item",
        endpoint_path="/modulo-contratacoes/2_consultarItensContratacoes_PNCP_14133",
        table_name="contratacao_item",
        map_row=map_contratacao_item_row,
        query_params=contratacao_item_query_params(inicial, final),
        job_name=slice_job_name("contratacao_item", inicial, final),
        date_watermark=DateWatermark(
            table="contratacao_item",
            column="data_inclusao_pncp",
            start_param="dataInclusaoPncpInicial",
            end_param="dataInclusaoPncpFinal",
        ),
    )


if __name__ == "__main__":
    main()
