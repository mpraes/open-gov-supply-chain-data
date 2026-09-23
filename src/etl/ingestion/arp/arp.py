from config.load_secret_key import load_secret_key_func
from etl.ingestion.dest_watermark import DateWatermark
from etl.ingestion.remaining_filters import arp_dates
from etl.ingestion.remaining_maps import map_arp_row
from etl.ingestion.remaining_query_params import arp_query_params
from etl.ingestion.remaining_run import run_sliced_remaining_ingestion
from etl.ingestion.script_runner import DEFAULT_ENV_PATH


def main() -> None:
    inicial, final = arp_dates(DEFAULT_ENV_PATH, load_secret_key_func)
    run_sliced_remaining_ingestion(
        data_inicial=inicial,
        data_final=final,
        params_for_slice=arp_query_params,
        job_prefix="arp",
        logger_name="arp",
        endpoint_path="/modulo-arp/1_consultarARP",
        table_name="arp",
        map_row=map_arp_row,
        date_watermark=DateWatermark(
            table="arp",
            column="data_vigencia_inicial",
            start_param="dataVigenciaInicialMin",
            end_param="dataVigenciaInicialMax",
        ),
    )


if __name__ == "__main__":
    main()
