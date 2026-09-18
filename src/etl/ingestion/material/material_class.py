from pathlib import Path

import requests
from psycopg2 import Error as PyscopgError
from psycopg2 import connect
from pydantic import ValidationError

from clients.compras_api import fetch_all_resultado_pages
from config.load_secret_key import load_secret_key_func
from contracts.material_class import MaterialClassRecord
from observability.logging_json import get_json_logger, log_error, log_info

log = get_json_logger("material_class")

# constants
BASE_URL = "https://dadosabertos.compras.gov.br"
ENV_PATH = Path(__file__).resolve().parents[3] / ".env"

# Credentials from .env
secret_key_api = load_secret_key_func(ENV_PATH, "DADOS_GOV_API_KEY")
postgres_host = load_secret_key_func(ENV_PATH, "PSQL_HOST")
postgres_port = load_secret_key_func(ENV_PATH, "PSQL_PORT")
postgres_user = load_secret_key_func(ENV_PATH, "PSQL_USER")
postgres_database = load_secret_key_func(ENV_PATH, "PSQL_DB")
postgres_password = load_secret_key_func(ENV_PATH, "PSQL_PASSWORD")

### Getting data from the api
url = f"{BASE_URL}/modulo-material/2_consultarClasseMaterial"
headers = {"Authorization": f"{secret_key_api}"}

try:
    # Class endpoint has no tamanhoPagina param in the API docs.
    result = fetch_all_resultado_pages(url, headers, page_size=None)
except requests.RequestException as exc:
    log_error(log, "api_fetch_failed", endpoint=url, error=str(exc))
    raise

log_info(log, "api_fetch_ok", rows=len(result))

# Loading data into the Postgres

# Query to upsert
UPSERT_SQL = """
INSERT INTO material_class (
    cod_classe, cod_grupo, nome_grupo, nome_classe, status_classe, data_hora_atualizacao
)
VALUES (
    %(cod_classe)s, %(cod_grupo)s, %(nome_grupo)s, %(nome_classe)s,
    %(status_classe)s, %(data_hora_atualizacao)s
)
ON CONFLICT (cod_classe) DO UPDATE SET
cod_grupo = EXCLUDED.cod_grupo,
nome_grupo = EXCLUDED.nome_grupo,
nome_classe = EXCLUDED.nome_classe,
status_classe = EXCLUDED.status_classe,
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
                    record = MaterialClassRecord(
                        cod_classe=row["codigoClasse"],
                        cod_grupo=row["codigoGrupo"],
                        nome_grupo=row["nomeGrupo"],
                        nome_classe=row["nomeClasse"],
                        status_classe=row["statusClasse"],
                        data_hora_atualizacao=row["dataHoraAtualizacao"],
                    )
                except (ValidationError, KeyError) as exc:
                    log_error(
                        log,
                        "row_validation_failed",
                        cod_classe=row.get("codigoClasse"),
                        error=str(exc),
                    )
                    raise
                cur.execute(UPSERT_SQL, record.model_dump())
                inserted += 1
except PyscopgError as exc:
    log_error(log, "upsert_failed", table="material_class", rows_done=inserted, error=str(exc))
    raise
finally:
    conn.close()
log_info(log, "upsert_ok", table="material_class", rows=inserted)
