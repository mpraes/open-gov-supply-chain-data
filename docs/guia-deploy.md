# Guia de deploy — produção no homelab

Como o código sai do WSL (dev), passa no CI e chega no notebook (prod),
sem disparar ingestão sozinho.

## Visão geral

```text
WSL (dev)  →  git push main  →  GitHub Actions (pytest)
                                      ↓ se verde
                               runner no homelab
                                      ↓
                    git pull em ~/projetos/open-gov-supply-chain-data
                                      ↓
                         Airflow já lê esse diretório
                         (DAGs continuam pausadas)
```

| Papel | Máquina | Caminho |
| --- | --- | --- |
| Dev | WSL | `/home/renan/personal/projects/open-gov-supply-chain-data` |
| Prod | Homelab (`ssh homelab`) | `~/projetos/open-gov-supply-chain-data` |
| Airflow prod | Homelab | `~/data-eng/airflow` — UI em `:8080` |
| Runner CI | Homelab | `~/actions-runner-open-gov` |

`.env` **não** vai para o git. Cada máquina tem o seu.

## Fluxo do dia a dia (já instalado)

No WSL:

```bash
cd /home/renan/personal/projects/open-gov-supply-chain-data
PYTHONPATH=src pytest src/tests -q
git add …
git commit
git push origin main
```

Espere o workflow **CI** ficar verde em
https://github.com/mpraes/open-gov-supply-chain-data/actions

O job `deploy-prod` faz `git pull --ff-only` no homelab. Confira:

```bash
ssh homelab 'cd ~/projetos/open-gov-supply-chain-data && git log -1 --oneline'
```

Dispare a DAG no Airflow (elas nascem pausadas):
http://meu_servidor:8080/dags
(login `airflow` / `airflow`). Sem o nome no `/etc/hosts`, use
http://192.168.2.120:8080/dags

Para redeploy sem commit novo: **Actions → CI → Run workflow**.

## Serviços no homelab

| Serviço | URL |
| --- | --- |
| Airflow | http://meu_servidor:8080 |
| Filebrowser | http://meu_servidor:8084 |
| Portainer | http://meu_servidor:9443 |
| dbt docs | http://meu_servidor:8580 |

No notebook, uma vez (pede sudo):

```bash
echo '192.168.2.120 meu_servidor' | sudo tee -a /etc/hosts
```

O mesmo nome em outro PC da LAN: a mesma linha no `hosts` daquela máquina.

## Primeira vez no homelab

Faça isto só se estiver montando o notebook do zero.

### 1. Código e `.env`

```bash
ssh homelab
mkdir -p ~/projetos
cd ~/projetos
git clone git@github.com:mpraes/open-gov-supply-chain-data.git
cd open-gov-supply-chain-data
# copie um .env (nunca commite). PSQL_HOST=localhost vira
# host.docker.internal dentro do Airflow.
```

Crie o schema `staging` e as tabelas (`src/sql/create_table_*.sql`) no
Postgres de dados (`postgres_db` na porta 5432).

### 2. Airflow

Compose em `~/data-eng/airflow` (LocalExecutor, UI `8080:8080`).
Volumes importantes:

- DAGs: `~/projetos/open-gov-supply-chain-data/dags` → `/opt/airflow/dags`
- Código: o mesmo clone → `/home/renan/personal/projects/open-gov-supply-chain-data`
  (caminho que `dags/open_gov_ingest.py` usa)

```bash
cd ~/data-eng/airflow
docker compose up -d
```

### 3. Runner GitHub Actions

O runner `open-gov-homelab` (labels `self-hosted`, `homelab`) vive em
`~/actions-runner-open-gov` e sobe com:

```bash
systemctl --user enable --now actions.runner.open-gov-homelab.service
systemctl --user status actions.runner.open-gov-homelab.service
```

Para continuar após logout/reboot (precisa sudo uma vez):

```bash
sudo loginctl enable-linger renan
```

Não reutilize o runner de `ingestao_no_limite`.

Para registrar de novo (token no GitHub → repo → Settings → Actions → Runners):

```bash
cd ~/actions-runner-open-gov
./config.sh --url https://github.com/mpraes/open-gov-supply-chain-data \
  --token <TOKEN> --name open-gov-homelab --labels homelab --unattended --replace
```

## O que o CI não faz

- Não dispara DAG
- Não sobrescreve `.env`
- Não roda pytest no notebook (só no `ubuntu-latest`)
- Não faz `git push --force` no clone de produção (`--ff-only`)

Se o pull falhar (commit local no homelab), limpe o working tree de prod
ou faça rebase à mão — o job não apaga alterações locais.

## Operar o Airflow

```bash
ssh homelab
cd ~/data-eng/airflow
docker compose ps
docker compose logs -f airflow-apiserver
docker compose restart airflow-scheduler
```

Trocar a porta da UI: `ports` no `docker-compose.yaml` e
`docker compose up -d airflow-apiserver`.

## Analytics (dbt)

Opcional, no clone: `dbt-open-gov/`. Não entra no job de deploy além do
`git pull`. Rode `dbt` no notebook quando quiser materializar o analytics.

## Problemas comuns

| Sintoma | O que checar |
| --- | --- |
| CI verde, prod no commit antigo | Runner `offline`? `systemctl --user status actions.runner.open-gov-homelab` |
| Job `deploy-prod` queued | Label `homelab` e runner **online** no GitHub |
| `git pull --ff-only` recusou | Commit local em `~/projetos/open-gov-supply-chain-data` |
| DAG não aparece | Volume das DAGs; logs do `airflow-dag-processor` |
| `numero_controle_pncp_ata` nulo | Mapper deriva `{unidade}:{numero_ata}` (ver remaining-ingestion) |
| Janela ARP > 365 dias | `run_sliced_remaining_ingestion` fatia automaticamente |
| UI 8080 ocupada | Filebrowser deve estar em **8084**, não em 8080 |
