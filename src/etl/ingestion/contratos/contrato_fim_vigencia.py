from config.load_secret_key import load_secret_key_func
from etl.ingestion.dest_watermark import DateWatermark
from etl.ingestion.remaining_filters import contratos_orgao_dates
from etl.ingestion.remaining_maps import map_contrato_row
from etl.ingestion.remaining_query_params import (
    contrato_fim_vigencia_query_params,
    slice_job_name,
)
from etl.ingestion.remaining_run import run_remaining_ingestion
from etl.ingestion.script_runner import DEFAULT_ENV_PATH


def main() -> None:
    orgao, inicial, final = contratos_orgao_dates(DEFAULT_ENV_PATH, load_secret_key_func)
    run_remaining_ingestion(
        logger_name="contrato_fim_vigencia",
        endpoint_path="/modulo-contratos/1.2_consultarContratos_FimVigencia",
        table_name="contrato",
        map_row=map_contrato_row,
        query_params=contrato_fim_vigencia_query_params(orgao, inicial, final),
        job_name=slice_job_name("contrato_fim_vigencia", orgao, inicial, final),
        date_watermark=DateWatermark(
            table="contrato",
            column="data_vigencia_final",
            start_param="dataVigenciaFinalMin",
            end_param="dataVigenciaFinalMax",
            where={"codigo_orgao": orgao},
        ),
    )


if __name__ == "__main__":
    main()
