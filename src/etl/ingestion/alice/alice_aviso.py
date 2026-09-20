from clients.compras_api import fetch_one_json_array_page
from config.load_secret_key import load_secret_key_func
from etl.ingestion.dest_watermark import DateWatermark
from etl.ingestion.remaining_filters import alice_datetimes
from etl.ingestion.remaining_maps import map_alice_aviso_row
from etl.ingestion.remaining_query_params import alice_aviso_query_params, slice_job_name
from etl.ingestion.remaining_run import run_remaining_ingestion
from etl.ingestion.script_runner import DEFAULT_ENV_PATH


def main() -> None:
    inicial, final = alice_datetimes(DEFAULT_ENV_PATH, load_secret_key_func)
    run_remaining_ingestion(
        logger_name="alice_aviso",
        endpoint_path="/alice/avisos-restritos",
        table_name="alice_aviso",
        map_row=map_alice_aviso_row,
        query_params=alice_aviso_query_params(inicial, final),
        job_name=slice_job_name("alice_aviso", inicial, final),
        page_size=None,
        fetch_page_fn=fetch_one_json_array_page,
        date_watermark=DateWatermark(
            table="alice_aviso",
            column="data_solicitacao_analise",
            start_param="dataInicioIntervalo",
            end_param="dataFimIntervalo",
            kind="alice",
        ),
    )


if __name__ == "__main__":
    main()
