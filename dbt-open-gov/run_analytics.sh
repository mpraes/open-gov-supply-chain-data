#!/bin/bash
set -eo pipefail

PROJECT_DIR="/home/renan/projetos/dbt-open-gov"
LOG_FILE="$PROJECT_DIR/logs/hourly_analytics.log"
LOCK_FILE="/tmp/dbt_analytics.lock"

# Evita execuções simultâneas se um processamento demorar mais de 1 hora
exec 200>"$LOCK_FILE"
flock -n 200 || { echo "[$(date '+%Y-%m-%d %H:%M:%S')] Execução anterior ainda em andamento. Abortando." >> "$LOG_FILE"; exit 1; }

echo "==================================================" >> "$LOG_FILE"
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Iniciando atualização horária da camada Analytics..." >> "$LOG_FILE"

# Identifica automaticamente o ID/Nome do container do serviço dbt via docker compose
cd "$PROJECT_DIR"
CONTAINER_ID="1f3de6998a80"

# Se preferir usar o nome fixo do container, substitua $CONTAINER_ID pelo nome (ex: dbt_container)
docker exec -t --env-file "$PROJECT_DIR/.env" "$CONTAINER_ID" dbt run --select path:models/analytics --profiles-dir profiles >> "$LOG_FILE" 2>&1

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Concluído com sucesso!" >> "$LOG_FILE"
