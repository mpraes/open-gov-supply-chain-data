from pathlib import Path

import requests
from psycopg2 import Error as PyscopgError
from psycopg2 import connect
from pydantic import ValidationError

from clients.compras_api import fetch_all_resultado_pages
from config.load_secret_key import load_secret_key_func
from contracts.material_natureza_despesa import MaterialNaturezaDespesaRecord
from observability.logging_json import get_json_logger, log_error, log_info

log = get_json_logger("material_natureza_despesa")

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
url = f"{BASE_URL}/modulo-material/5_consultarMaterialNaturezaDespesa"
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
INSERT INTO material_natureza_despesa (
    cod_pdm, cod_natureza_despesa, nome_natureza_despesa, status_natureza_despesa
)
VALUES (
    %(cod_pdm)s, %(cod_natureza_despesa)s, %(nome_natureza_despesa)s,
    %(status_natureza_despesa)s
)
ON CONFLICT (cod_pdm, cod_natureza_despesa) DO UPDATE SET
nome_natureza_despesa = EXCLUDED.nome_natureza_despesa,
status_natureza_despesa = EXCLUDED.status_natureza_despesa,
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
                    record = MaterialNaturezaDespesaRecord(
                        cod_pdm=row["codigoPdm"],
                        cod_natureza_despesa=row["codigoNaturezaDespesa"],
                        nome_natureza_despesa=row["nomeNaturezaDespesa"],
                        status_natureza_despesa=row["statusNaturezaDespesa"],
                    )
                except (ValidationError, KeyError) as exc:
                    log_error(
                        log,
                        "row_validation_failed",
                        cod_pdm=row.get("codigoPdm"),
                        cod_natureza_despesa=row.get("codigoNaturezaDespesa"),
                        error=str(exc),
                    )
                    raise
                cur.execute(UPSERT_SQL, record.model_dump())
                inserted += 1
except PyscopgError as exc:
    log_error(
        log,
        "upsert_failed",
        table="material_natureza_despesa",
        rows_done=inserted,
        error=str(exc),
    )
    raise
finally:
    conn.close()
log_info(log, "upsert_ok", table="material_natureza_despesa", rows=inserted)
