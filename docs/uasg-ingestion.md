# Design: UASG ingestion — JSON endpoints

Date: 2026-09-19  
Status: implemented  
Approach: Reuse `run_page_batch_ingestion`; skip CSV

## Scope

JSON endpoints from `docs/dados_api.md` §05. CSV variants are skipped.

| # | Endpoint | Script / table | Driver |
| --- | --- | --- | --- |
| 1 | `2_consultarOrgao` | `uasg_orgao` | `statusOrgao` true then false |
| 2 | `1_consultarUasg` | `uasg` | `statusUasg` true then false |

## Layout

```text
src/sql/create_table_uasg.sql
src/sql/create_table_uasg_orgao.sql
src/contracts/uasg.py
src/contracts/uasg_orgao.py
src/etl/ingestion/uasg/uasg.py
src/etl/ingestion/uasg/uasg_orgao.py
src/etl/ingestion/uasg/query_params.py
src/etl/ingestion/uasg/map_uasg_fields.py
src/tests/test_uasg_*.py
```

## Conventions

- Pydantic `ConfigDict(strict=True)`; names uppercased / stripped
- CNPJ/SIORG codes are stripped, not uppercased
- `PAGE_SIZE = None` — docs do not list `tamanhoPagina`
- Upsert + `data_hora_carga = now()` on conflict
- Resume cursor is per status (`uasg:true`, `uasg:false`) so a slice change does not reuse another job's page watermark
- No FK from `uasg.codigo_orgao` to `uasg_orgao`: the open API can return orphan órgão codes

## How to run

Create tables in load order, then:

```bash
PYTHONPATH=src python src/etl/ingestion/uasg/uasg_orgao.py
PYTHONPATH=src python src/etl/ingestion/uasg/uasg.py
```

Each script walks `status=true` then `status=false` because both endpoints require that boolean.

## API quirks

- `statusUasg` and `statusOrgao` are required query params; omitting them is not a full dump
- `codigoUasg` is documented as string; the contract also accepts int and stores text
- Location / polo / CNPJ fields are often null

## Non-goals

- Airflow DAGs
- CSV downloads
- Filtering by UF, CNPJ, or a single UASG code
