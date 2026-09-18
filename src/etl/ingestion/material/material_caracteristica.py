from pathlib import Path

import requests
from psycopg2 import Error as PyscopgError
from psycopg2 import connect
from pydantic import ValidationError

from clients.compras_api import fetch_all_resultado_pages
from config.load_secret_key import load_secret_key_func
from contracts.material_caracteristica import MaterialCaracteristicaRecord
from observability.logging_json import get_json_logger, log_error, log_info

log = get_json_logger("material_caracteristica")

# constants
BASE_URL = "https://dadosabertos.compras.gov.br"
ENV_PATH = Path(__file__).resolve().parents[3] / ".env"
PAGE_SIZE = 500

# Credentials from .env
secret_key_api = load_secret_key_func(ENV_PATH, "DADOS_GOV_API_KEY")
postgres_host = load_secret_key_func(ENV_PATH, "PSQL_HOST")
postgres_port = load_secret_key_func(ENV_PATH, "PSQL_PORT")
postgres_user = load_secret_key_func(ENV_PATH, "PSQL_USER")
postgres_database = load_secret_key_func(ENV_PATH, "PSQL_DB")
postgres_password = load_secret_key_func(ENV_PATH, "PSQL_PASSWORD")

### Getting data from the api
url = f"{BASE_URL}/modulo-material/7_consultarMaterialCaracteristicas"
headers = {"Authorization": f"{secret_key_api}"}

try:
    result = fetch_all_resultado_pages(url, headers, page_size=PAGE_SIZE)
except requests.RequestException as exc:
    log_error(log, "api_fetch_failed", endpoint=url, error=str(exc))
    raise

log_info(log, "api_fetch_ok", rows=len(result), page_size=PAGE_SIZE)

# Loading data into the Postgres

# Query to upsert
UPSERT_SQL = """
INSERT INTO material_caracteristica (
    cod_item, numero_caracteristica, codigo_caracteristica, codigo_valor_caracteristica,
    nome_caracteristica, status_caracteristica, nome_valor_caracteristica,
    status_valor_caracteristica, item_sustentavel, status_item, sigla_unidade_medida,
    data_hora_atualizacao
)
VALUES (
    %(cod_item)s, %(numero_caracteristica)s, %(codigo_caracteristica)s,
    %(codigo_valor_caracteristica)s, %(nome_caracteristica)s, %(status_caracteristica)s,
    %(nome_valor_caracteristica)s, %(status_valor_caracteristica)s, %(item_sustentavel)s,
    %(status_item)s, %(sigla_unidade_medida)s, %(data_hora_atualizacao)s
)
ON CONFLICT (
    cod_item, numero_caracteristica, codigo_caracteristica, codigo_valor_caracteristica
) DO UPDATE SET
nome_caracteristica = EXCLUDED.nome_caracteristica,
status_caracteristica = EXCLUDED.status_caracteristica,
nome_valor_caracteristica = EXCLUDED.nome_valor_caracteristica,
status_valor_caracteristica = EXCLUDED.status_valor_caracteristica,
item_sustentavel = EXCLUDED.item_sustentavel,
status_item = EXCLUDED.status_item,
sigla_unidade_medida = EXCLUDED.sigla_unidade_medida,
data_hora_atualizacao = EXCLUDED.data_hora_atualizacao,
data_hora_carga = now();
"""

# Connection
conn = connect(
    host=postgres_host,
    port=postgres_port,
    user=postgres_user,
    password=postgres_password,
    dbname=postgres_database,
)

inserted = 0
# Execution of the cursor query from the rows
try:
    with conn:
        with conn.cursor() as cur:
            for row in result:
                try:
                    record = MaterialCaracteristicaRecord(
                        cod_item=row["codigoItem"],
                        item_sustentavel=row["itemSustentavel"],
                        status_item=row["statusItem"],
                        codigo_caracteristica=row["codigoCaracteristica"],
                        nome_caracteristica=row["nomeCaracteristica"],
                        status_caracteristica=row["statusCaracteristica"],
                        codigo_valor_caracteristica=row["codigoValorCaracteristica"],
                        nome_valor_caracteristica=row["nomeValorCaracteristica"],
                        status_valor_caracteristica=row["statusValorCaracteristica"],
                        numero_caracteristica=row["numeroCaracteristica"],
                        sigla_unidade_medida=row["siglaUnidadeMedida"],
                        data_hora_atualizacao=row["dataHoraAtualizacao"],
                    )
                except (ValidationError, KeyError) as exc:
                    log_error(
                        log,
                        "row_validation_failed",
                        cod_item=row.get("codigoItem"),
                        numero_caracteristica=row.get("numeroCaracteristica"),
                        error=str(exc),
                    )
                    raise
                cur.execute(UPSERT_SQL, record.model_dump())
                inserted += 1
except PyscopgError as exc:
    log_error(
        log,
        "upsert_failed",
        table="material_caracteristica",
        rows_done=inserted,
        error=str(exc),
    )
    raise
finally:
    conn.close()
log_info(log, "upsert_ok", table="material_caracteristica", rows=inserted)
