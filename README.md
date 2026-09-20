# Open Gov Supply Chain Data

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

DDL em `src/sql/create_table_*.sql`. Detalhes de ordem e filtros: [`docs/architecture.md`](docs/architecture.md).

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
