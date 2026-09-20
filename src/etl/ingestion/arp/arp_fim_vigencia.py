from config.load_secret_key import load_secret_key_func
from etl.ingestion.dest_watermark import DateWatermark
from etl.ingestion.remaining_filters import arp_dates
from etl.ingestion.remaining_maps import map_arp_row
from etl.ingestion.remaining_query_params import (
    arp_fim_vigencia_query_params,
    slice_job_name,
)
from etl.ingestion.remaining_run import run_remaining_ingestion
from etl.ingestion.script_runner import DEFAULT_ENV_PATH


def main() -> None:
    inicial, final = arp_dates(DEFAULT_ENV_PATH, load_secret_key_func)
    run_remaining_ingestion(
        logger_name="arp_fim_vigencia",
        endpoint_path="/modulo-arp/1.2_consultarARP_FimVigencia",
        table_name="arp",
        map_row=map_arp_row,
        query_params=arp_fim_vigencia_query_params(inicial, final),
        job_name=slice_job_name("arp_fim_vigencia", inicial, final),
        date_watermark=DateWatermark(
            table="arp",
            column="data_vigencia_final",
            start_param="dataVigenciaFinalMin",
            end_param="dataVigenciaFinalMax",
        ),
    )


if __name__ == "__main__":
    main()
