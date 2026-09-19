# Design: PGC (planejamento) ingestion — JSON endpoints

Date: 2026-09-18  
Status: implemented  
Approach: Reuse `run_page_batch_ingestion` / `run_preco_batch_ingestion`; skip CSV

## Scope

JSON endpoints from `docs/dados_api.md` §04. CSV variants are skipped.

| # | Endpoint | Script / table | Driver |
| --- | --- | --- | --- |
| 1 | `1_consultarPgcDetalhe` | `pgc_detalhe` | `PGC_ORGAO` + `PGC_ANO` (+ optional `PGC_CODIGO_UASG`) |
| 2 | `2_consultarPgcDetalheCatalogo` | `pgc_detalhe_catalogo` | `PGC_ANO` + CATMAT class / CATSER group codes |
| 3 | `3_consultarPgcAgregacao` | `pgc_agregacao` | `PGC_ORGAO` + `PGC_ANO` |

## Layout

```text
src/sql/create_table_pgc_*.sql
src/contracts/pgc_detalhe.py
src/contracts/pgc_agregacao.py
src/etl/ingestion/planejamento/pgc_detalhe.py
src/etl/ingestion/planejamento/pgc_detalhe_catalogo.py
src/etl/ingestion/planejamento/pgc_agregacao.py
src/etl/ingestion/planejamento/query_params.py
src/etl/ingestion/planejamento/pgc_filters.py
src/etl/ingestion/planejamento/map_pgc_fields.py
src/etl/ingestion/planejamento/pgc_detalhe_sql.py
src/tests/test_pgc_*.py
```

## Conventions

- Pydantic `ConfigDict(strict=True)`; text uppercased / stripped
- Endpoint 1 and 2 share `PgcDetalheRecord` (same API shape)
- `PAGE_SIZE = 100` when `tamanhoPagina` exists; agregação has none (`None`)
- Upsert + `data_hora_carga = now()` on conflict
- Resume cursor is per órgão+year (`pgc_detalhe:36000:2026`) so a filter change does not reuse another job's page watermark
- Catalogo walks `material_class.cod_classe` (`tipo=Material`) then `servico_grupo.cod_grupo` (`tipo=Servico`)

## How to run

Set in `.env`:

```bash
PGC_ORGAO=36000
PGC_ANO=2026
# optional: PGC_CODIGO_UASG=153001
```

Create tables, then:

```bash
PYTHONPATH=src python src/etl/ingestion/planejamento/pgc_detalhe.py
PYTHONPATH=src python src/etl/ingestion/planejamento/pgc_detalhe_catalogo.py
PYTHONPATH=src python src/etl/ingestion/planejamento/pgc_agregacao.py
```

`pgc_detalhe` and `pgc_agregacao` need `PGC_ORGAO` + `PGC_ANO`.  
`pgc_detalhe_catalogo` needs `PGC_ANO` and already-loaded `material_class` / `servico_grupo`.

## API quirks

- Endpoint 1 and 3 require `orgao`; there is no órgão catalog in this repo yet, so filters come from `.env`
- Endpoint 1/2 use `anoPcaProjetoCompra`; endpoint 3 uses `ano`
- Material vs serviço hierarchy fields are mutually sparse; only identity keys are required
- Endpoint 1 and 2 can overlap; they land in different tables

## Non-goals

- Airflow DAGs
- CSV downloads
