from pathlib import Path

import requests
from psycopg2 import Error as PyscopgError
from psycopg2 import connect
from pydantic import ValidationError

from clients.compras_api import fetch_all_resultado_pages
from config.load_secret_key import load_secret_key_func
from contracts.material_item import MaterialItemRecord
from observability.logging_json import get_json_logger, log_error, log_info

log = get_json_logger("material_item")

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
url = f"{BASE_URL}/modulo-material/4_consultarItemMaterial"
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
INSERT INTO material_item (
    cod_item, cod_grupo, nome_grupo, cod_classe, nome_classe, cod_pdm, nome_pdm,
    descricao_item, status_item, item_sustentavel, codigo_ncm, descricao_ncm,
    aplica_margem_preferencia, data_hora_atualizacao
)
VALUES (
    %(cod_item)s, %(cod_grupo)s, %(nome_grupo)s, %(cod_classe)s, %(nome_classe)s,
    %(cod_pdm)s, %(nome_pdm)s, %(descricao_item)s, %(status_item)s,
    %(item_sustentavel)s, %(codigo_ncm)s, %(descricao_ncm)s,
    %(aplica_margem_preferencia)s, %(data_hora_atualizacao)s
)
ON CONFLICT (cod_item) DO UPDATE SET
cod_grupo = EXCLUDED.cod_grupo,
nome_grupo = EXCLUDED.nome_grupo,
cod_classe = EXCLUDED.cod_classe,
nome_classe = EXCLUDED.nome_classe,
cod_pdm = EXCLUDED.cod_pdm,
nome_pdm = EXCLUDED.nome_pdm,
descricao_item = EXCLUDED.descricao_item,
status_item = EXCLUDED.status_item,
item_sustentavel = EXCLUDED.item_sustentavel,
codigo_ncm = EXCLUDED.codigo_ncm,
descricao_ncm = EXCLUDED.descricao_ncm,
aplica_margem_preferencia = EXCLUDED.aplica_margem_preferencia,
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
                    record = MaterialItemRecord(
                        cod_item=row["codigoItem"],
                        cod_grupo=row["codigoGrupo"],
                        nome_grupo=row["nomeGrupo"],
                        cod_classe=row["codigoClasse"],
                        nome_classe=row["nomeClasse"],
                        cod_pdm=row["codigoPdm"],
                        nome_pdm=row["nomePdm"],
                        descricao_item=row["descricaoItem"],
                        status_item=row["statusItem"],
                        item_sustentavel=row["itemSustentavel"],
                        codigo_ncm=row["codigo_ncm"],
                        descricao_ncm=row["descricao_ncm"],
                        aplica_margem_preferencia=row["aplica_margem_preferencia"],
                        data_hora_atualizacao=row["dataHoraAtualizacao"],
                    )
                except (ValidationError, KeyError) as exc:
                    log_error(
                        log,
                        "row_validation_failed",
                        cod_item=row.get("codigoItem"),
                        error=str(exc),
                    )
                    raise
                cur.execute(UPSERT_SQL, record.model_dump())
                inserted += 1
except PyscopgError as exc:
    log_error(log, "upsert_failed", table="material_item", rows_done=inserted, error=str(exc))
    raise
finally:
    conn.close()
log_info(log, "upsert_ok", table="material_item", rows=inserted)
