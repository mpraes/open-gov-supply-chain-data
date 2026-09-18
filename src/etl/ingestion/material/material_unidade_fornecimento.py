from pathlib import Path

import requests
from psycopg2 import Error as PyscopgError
from psycopg2 import connect
from pydantic import ValidationError

from clients.compras_api import fetch_all_resultado_pages
from config.load_secret_key import load_secret_key_func
from contracts.material_unidade_fornecimento import MaterialUnidadeFornecimentoRecord
from observability.logging_json import get_json_logger, log_error, log_info

log = get_json_logger("material_unidade_fornecimento")

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
url = f"{BASE_URL}/modulo-material/6_consultarMaterialUnidadeFornecimento"
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
INSERT INTO material_unidade_fornecimento (
    cod_pdm, numero_sequencial_unidade_fornecimento, sigla_unidade_fornecimento,
    nome_unidade_fornecimento, descricao_unidade_fornecimento, sigla_unidade_medida,
    capacidade_unidade_fornecimento, status_unidade_fornecimento_pdm,
    status_unidade_fornecimento, data_hora_atualizacao
)
VALUES (
    %(cod_pdm)s, %(numero_sequencial_unidade_fornecimento)s,
    %(sigla_unidade_fornecimento)s, %(nome_unidade_fornecimento)s,
    %(descricao_unidade_fornecimento)s, %(sigla_unidade_medida)s,
    %(capacidade_unidade_fornecimento)s, %(status_unidade_fornecimento_pdm)s,
    %(status_unidade_fornecimento)s, %(data_hora_atualizacao)s
)
ON CONFLICT (cod_pdm, numero_sequencial_unidade_fornecimento) DO UPDATE SET
sigla_unidade_fornecimento = EXCLUDED.sigla_unidade_fornecimento,
nome_unidade_fornecimento = EXCLUDED.nome_unidade_fornecimento,
descricao_unidade_fornecimento = EXCLUDED.descricao_unidade_fornecimento,
sigla_unidade_medida = EXCLUDED.sigla_unidade_medida,
capacidade_unidade_fornecimento = EXCLUDED.capacidade_unidade_fornecimento,
status_unidade_fornecimento_pdm = EXCLUDED.status_unidade_fornecimento_pdm,
status_unidade_fornecimento = EXCLUDED.status_unidade_fornecimento,
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
                    record = MaterialUnidadeFornecimentoRecord(
                        cod_pdm=row["codigoPdm"],
                        sigla_unidade_fornecimento=row["siglaUnidadeFornecimento"],
                        nome_unidade_fornecimento=row["nomeUnidadeFornecimento"],
                        descricao_unidade_fornecimento=row["descricaoUnidadeFornecimento"],
                        sigla_unidade_medida=row["siglaUnidadeMedida"],
                        capacidade_unidade_fornecimento=row["capacidadeUnidadeFornecimento"],
                        numero_sequencial_unidade_fornecimento=row[
                            "numeroSequencialUnidadeFornecimento"
                        ],
                        status_unidade_fornecimento_pdm=row["statusUnidadeFornecimentoPdm"],
                        status_unidade_fornecimento=row["statusUnidadeFornecimento"],
                        data_hora_atualizacao=row["dataHoraAtualizacao"],
                    )
                except (ValidationError, KeyError) as exc:
                    log_error(
                        log,
                        "row_validation_failed",
                        cod_pdm=row.get("codigoPdm"),
                        numero_sequencial=row.get("numeroSequencialUnidadeFornecimento"),
                        error=str(exc),
                    )
                    raise
                cur.execute(UPSERT_SQL, record.model_dump())
                inserted += 1
except PyscopgError as exc:
    log_error(
        log,
        "upsert_failed",
        table="material_unidade_fornecimento",
        rows_done=inserted,
        error=str(exc),
    )
    raise
finally:
    conn.close()
log_info(log, "upsert_ok", table="material_unidade_fornecimento", rows=inserted)
