from config.load_secret_key import load_secret_key_func
from etl.ingestion.dest_watermark import DateWatermark
from etl.ingestion.remaining_filters import contratacoes_dates
from etl.ingestion.remaining_maps import map_contratacao_resultado_row
from etl.ingestion.remaining_query_params import contratacao_resultado_query_params
from etl.ingestion.remaining_run import run_sliced_remaining_ingestion
from etl.ingestion.script_runner import DEFAULT_ENV_PATH


def main() -> None:
    inicial, final = contratacoes_dates(DEFAULT_ENV_PATH, load_secret_key_func)
    run_sliced_remaining_ingestion(
        data_inicial=inicial,
        data_final=final,
        params_for_slice=contratacao_resultado_query_params,
        job_prefix="contratacao_resultado",
        logger_name="contratacao_resultado",
        endpoint_path="/modulo-contratacoes/3_consultarResultadoItensContratacoes_PNCP_14133",
        table_name="contratacao_resultado",
        map_row=map_contratacao_resultado_row,
        date_watermark=DateWatermark(
            table="contratacao_resultado",
            column="data_resultado_pncp",
            start_param="dataResultadoPncpInicial",
            end_param="dataResultadoPncpFinal",
        ),
    )


if __name__ == "__main__":
    main()
