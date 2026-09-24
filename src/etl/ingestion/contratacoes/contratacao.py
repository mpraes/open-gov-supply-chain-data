from config.load_secret_key import load_secret_key_func
from etl.ingestion.dest_watermark import DateWatermark
from etl.ingestion.remaining_filters import contratacoes_dates, contratacoes_modalidades
from etl.ingestion.remaining_maps import map_contratacao_row
from etl.ingestion.remaining_query_params import contratacao_query_params
from etl.ingestion.remaining_run import run_sliced_remaining_ingestion
from etl.ingestion.script_runner import DEFAULT_ENV_PATH


def main() -> None:
    inicial, final = contratacoes_dates(DEFAULT_ENV_PATH, load_secret_key_func)
    for modalidade in contratacoes_modalidades(DEFAULT_ENV_PATH, load_secret_key_func):
        _ingest_contratacao_modalidade(inicial, final, modalidade)


def _ingest_contratacao_modalidade(
    inicial: str, final: str, modalidade: int
) -> None:
    run_sliced_remaining_ingestion(
        data_inicial=inicial,
        data_final=final,
        params_for_slice=lambda ini, fin: contratacao_query_params(ini, fin, modalidade),
        job_prefix=f"contratacao:{modalidade}",
        logger_name="contratacao",
        endpoint_path="/modulo-contratacoes/1_consultarContratacoes_PNCP_14133",
        table_name="contratacao",
        map_row=map_contratacao_row,
        date_watermark=DateWatermark(
            table="contratacao",
            column="data_publicacao_pncp",
            start_param="dataPublicacaoPncpInicial",
            end_param="dataPublicacaoPncpFinal",
            where={"codigo_modalidade": str(modalidade)},
        ),
    )


if __name__ == "__main__":
    main()
