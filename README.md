# Open Gov Supply Chain Data

<img width="2752" height="1536" alt="Gemini_Generated_Image_d4baw4d4baw4d4ba" src="https://github.com/user-attachments/assets/f07c1f34-0567-4ff6-9e5c-917721b1a65c" />

ETL dos dados abertos de compras públicas do [compras.gov.br](https://dadosabertos.compras.gov.br) para Postgres.

Cada script de ingestão baixa um endpoint, valida o JSON e faz upsert no schema **`staging`**.

## O que entra no banco

| Domínio | Exemplos |
| --- | --- |
| CATMAT | grupo → classe → PDM → item |
| CATSER | seção → divisão → grupo → classe → subclasse → item |
| Preços praticados | `preco_material`, `preco_servico` (+ detalhe) |
| PGC | detalhe, catálogo, agregação |
| UASG | órgão, UASG |
| Legado (Lei 8.666) | licitação, pregão, RDC, compra sem licitação |
| Lei 14.133 e afins | contratações, ARP, contratos, fornecedor, OCDS, indicadores, Alice |

DDL em `src/sql/create_table_*.sql`. Índice da documentação: [`docs/README.md`](docs/README.md). Deploy no homelab: [`docs/guia-deploy.md`](docs/guia-deploy.md). Arquitetura: [`docs/architecture.md`](docs/architecture.md).

## Como a ingestão funciona

Quase todo script só declara endpoint, mapeamento e SQL. O loop fica em dois runners:

- **`run_page_batch_ingestion`** — página a página, com cursor de resume. Usado por CATMAT, CATSER, UASG, PGC, legado e pelos dumps restantes (`run_remaining_ingestion`).
- **`run_preco_batch_ingestion`** — código a código do catálogo (PDM, item CATSER, etc.). Usado pelos 4 scripts de preço e por `pgc_detalhe_catalogo`.

A conexão Postgres define `search_path=staging` e o SQL qualifica as tabelas (`staging.preco_material`, …).

Janelas de data no `.env` são o teto do backfill. O `MAX(data)` no destino sobe o piso (com overlap do último dia). `etl_code_cursor` só retoma crash dentro dessa fatia.

## Setup

Python 3.12+, Postgres com schema `staging`, e um `.env` na raiz:

```
DADOS_GOV_API_KEY=...
PSQL_HOST=...
PSQL_PORT=5432
PSQL_USER=...
PSQL_PASSWORD=...
PSQL_DB=open_gov_supply_chain
```

Alguns jobs pedem filtros extras (`PGC_ORGAO`, `PGC_ANO`, `CONTRATACOES_DATA_*`, `LEGADO_*`, …). Ver os docs em `docs/`.

```bash
uv sync
# ou: python -m venv .venv && .venv/bin/pip install -e .
```

Crie as tabelas no schema `staging` (o client precisa de `search_path=staging`, ou prefixe `staging.` nos `CREATE TABLE`).

## Rodar

```bash
PYTHONPATH=src python src/etl/ingestion/material/material_group.py
PYTHONPATH=src python src/etl/ingestion/material/material_class.py
PYTHONPATH=src python src/etl/ingestion/servico/servico_secao.py
PYTHONPATH=src python src/etl/ingestion/precos/preco_material.py
PYTHONPATH=src python src/etl/ingestion/planejamento/pgc_detalhe.py
PYTHONPATH=src python src/etl/ingestion/uasg/uasg.py
PYTHONPATH=src python src/etl/ingestion/legado/legado_licitacao.py
PYTHONPATH=src python src/etl/ingestion/contratacoes/contratacao.py
```

Logs JSON em `logs/` (`api_fetch_ok`, `upsert_ok`, `preco_batch_ok`, …).

## Testes

```bash
PYTHONPATH=src .venv/bin/pytest src/tests -q
```

I/O externo (API, Postgres, filesystem) é mockado com fakes nomeadas.

## Dev e produção

| Ambiente | Onde | Papel |
| --- | --- | --- |
| **Dev** | WSL (`/home/renan/personal/projects/open-gov-supply-chain-data`) | Editar, testar, commitar, `git push` |
| **Prod** | Homelab (`~/projetos/open-gov-supply-chain-data`) + Airflow em `:8080` | Código atualizado só depois do CI verde |

O workflow [`.github/workflows/ci.yml`](.github/workflows/ci.yml) roda `pytest` no GitHub (`ubuntu-latest`) em todo push/PR para `main`. Se os testes passam e o evento é push (ou *Run workflow*), o runner self-hosted no homelab faz `git pull --ff-only` em produção. DAGs continuam pausadas; dispare no Airflow quando quiser.

`.env` não entra no git e não é sobrescrito pelo deploy.

O runner de produção (`open-gov-homelab`) roda no notebook via `systemctl --user` (`actions.runner.open-gov-homelab.service`). Ele precisa da sessão do usuário `renan` (ou `loginctl enable-linger renan` com sudo) para sobreviver a logout/reboot.

Passo a passo (hosts, Airflow, runner, troubleshooting): [`docs/guia-deploy.md`](docs/guia-deploy.md).
