# Design: LEGADO ingestion — JSON list endpoints

Date: 2026-09-19  
Status: implemented  
Approach: Reuse `run_page_batch_ingestion`; skip `_Id` lookups

Operação (dev/prod/CI): [guia-deploy.md](./guia-deploy.md).

## Scope

JSON list endpoints from `docs/dados_api.md` §06. Lookup-by-id variants
(`1.1`, `2.1`, `3.1`, `4.1`, `5.1`, `6.1`) share the same row shape and are skipped.

| # | Endpoint | Script / table | Driver |
| --- | --- | --- | --- |
| 1 | `1_consultarLicitacao` | `legado_licitacao` | `LEGADO_DATA_INICIAL` + `LEGADO_DATA_FINAL` |
| 2 | `2_consultarItemLicitacao` | `legado_item_licitacao` | `LEGADO_MODALIDADE` |
| 3 | `3_consultarPregoes` | `legado_pregao` | date range (edital) |
| 4 | `4_consultarItensPregoes` | `legado_item_pregao` | date range (homologação) |
| 5 | `5_consultarComprasSemLicitacao` | `legado_compra_sem_licitacao` | `LEGADO_ANO` |
| 6 | `6_consultarCompraItensSemLicitacao` | `legado_item_sem_licitacao` | `LEGADO_ANO` |
| 7 | `7_consultarRdc` | `legado_rdc` | date range (publicação) |

Optional `LEGADO_UASG` narrows every endpoint that accepts UASG / `co_uasg`.

## Layout

```text
src/sql/create_table_legado_*.sql
src/contracts/legado_*.py
src/etl/ingestion/legado/*.py
src/tests/test_legado_*.py
```

## Conventions

- Pydantic `ConfigDict(strict=True)`; names uppercased / stripped
- Amounts accept int, float, or numeric string (`"1,25"`)
- `PAGE_SIZE = 100` (`tamanhoPagina` is documented)
- Upsert + `data_hora_carga = now()` on conflict
- Resume cursor includes the raised dest window (`legado_licitacao:2024-06-15:2024-12-31`)
- Date-window jobs (`licitacao`, `pregao`, `item_pregao`, `rdc`) raise the API start date from dest `MAX` of the matching column; `.env` `LEGADO_DATA_*` is the ceiling
- Modalidade/year dumps (`item_licitacao`, dispensa) stay page-resume; the API has no dest date filter
- No FKs: items can arrive without a parent header in the same window
- API field `no_ausg` is stored as-is (documented typo for nome UASG)

## How to run

Set in `.env`:

```bash
LEGADO_DATA_INICIAL=2024-01-01
LEGADO_DATA_FINAL=2024-12-31
LEGADO_ANO=2024
LEGADO_MODALIDADE=5
# optional: LEGADO_UASG=153001
```

Create tables, then:

```bash
PYTHONPATH=src python src/etl/ingestion/legado/legado_licitacao.py
PYTHONPATH=src python src/etl/ingestion/legado/legado_item_licitacao.py
PYTHONPATH=src python src/etl/ingestion/legado/legado_pregao.py
PYTHONPATH=src python src/etl/ingestion/legado/legado_item_pregao.py
PYTHONPATH=src python src/etl/ingestion/legado/legado_compra_sem_licitacao.py
PYTHONPATH=src python src/etl/ingestion/legado/legado_item_sem_licitacao.py
PYTHONPATH=src python src/etl/ingestion/legado/legado_rdc.py
```

Date-window scripts share `LEGADO_DATA_*`. Dispensa scripts need `LEGADO_ANO`.
Item de licitação needs `LEGADO_MODALIDADE`.

## API quirks

- There is no unfiltered dump: every list endpoint requires a date range, year, or modalidade
- Pregão amounts arrive as strings; RDC `nome_responsavel` can be numeric
- RDC has no `id_compra`; the primary key is `identificador`

## Non-goals

- Airflow DAGs
- Lookup-by-id endpoints
- Walking every modalidade automatically
