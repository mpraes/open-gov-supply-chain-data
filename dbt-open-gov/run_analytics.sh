#!/bin/bash
set -eo pipefail

# Directory of this script, so the run does not depend on a hardcoded checkout.
PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
LOG_FILE="$PROJECT_DIR/logs/hourly_analytics.log"
LOCK_FILE="/tmp/dbt_analytics.lock"
mkdir -p "$(dirname "$LOG_FILE")"

exec 200>"$LOCK_FILE"
flock -n 200 || {
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] Execução anterior ainda em andamento. Abortando." | tee -a "$LOG_FILE"
  exit 1
}

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Iniciando atualização horária da camada Analytics..." | tee -a "$LOG_FILE"

# One-shot runner. dbt_docs_server only serves docs and is mounted on an empty dir.
docker run --rm \
  --network workspace-dados_dataeng \
  --env-file "$PROJECT_DIR/.env" \
  -e DBT_PROFILES_DIR=/usr/app/profiles \
  -v "$PROJECT_DIR:/usr/app" \
  -w /usr/app \
  --entrypoint dbt \
  ghcr.io/dbt-labs/dbt-postgres:1.9.latest \
  run --select path:models/analytics --profiles-dir profiles \
  2>&1 | tee -a "$LOG_FILE"

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Concluído com sucesso!" | tee -a "$LOG_FILE"
