# Material ingestion refactor (2026-09-18)

Register of the AGENTS.md-aligned refactor of `src/etl/ingestion/material/`.

## Goals

- Remove duplicated fetch → validate → upsert logic across seven scripts
- Inject dependencies (secrets, DB connect, page fetch) for testability
- Keep **seven runnable script paths** for later Airflow scheduling
- Place shared helpers where **non-material** ETLs (serviço, prices, …) can reuse them

## What was added

| Path | Role |
| --- | --- |
| `src/etl/ingestion/db.py` | `connect_postgres(...)` — thin injectable wrapper over `psycopg2.connect` |
| `src/etl/ingestion/pipeline.py` | `run_api_upsert_ingestion(...)` — fetch pages → `map_row` → upsert |
| `src/etl/ingestion/script_runner.py` | `run_script_ingestion(...)` — load `.env`, open DB, call pipeline, always `close()` |
| `src/etl/__init__.py`, `ingestion/__init__.py`, `material/__init__.py` | Package markers for imports |

## What changed in the seven scripts

Each of:

- `material_group.py`
- `material_class.py`
- `material_pdm.py`
- `material_item.py`
- `material_natureza_despesa.py`
- `material_unidade_fornecimento.py`
- `material_caracteristica.py`

now contains only:

1. Endpoint path + optional `PAGE_SIZE` + `UPSERT_SQL`
2. `map_<entity>_row(row) -> Record` (API JSON → Pydantic contract)
3. `main()` → `run_script_ingestion(...)`
4. `if __name__ == "__main__": main()`

**No secrets, HTTP, or DB I/O at import time.**

## Runtime flow

```text
python …/material_item.py
  → main()
    → run_script_ingestion(...)
         → load DADOS_GOV_API_KEY + PSQL_* from .env
         → connect_postgres(...)
         → run_api_upsert_ingestion(...)
              → fetch_all_resultado_pages (client)
              → map_row → record.model_dump()
              → UPSERT via cursor
         → conn.close() in finally
```

Structured JSON logging (`api_fetch_ok`, `row_validation_failed`, `upsert_ok` / `upsert_failed`) is unchanged in intent; validation failures log `table` + `offending_row` + `error`.

## Reuse for other APIs / tables

Call the same shared modules from a new script under e.g. `src/etl/ingestion/servico/`:

1. Define `ENDPOINT_PATH`, `PAGE_SIZE`, `UPSERT_SQL`
2. Implement `map_*_row` to a contract in `src/contracts/`
3. Call `run_script_ingestion(logger_name=..., table_name=..., map_row=..., ...)`

Only the paginated `resultado` → row upsert pattern is covered. Other shapes may reuse `connect_postgres` alone and add a different runner later.

## Tests added

| Test module | Covers |
| --- | --- |
| `src/tests/test_connect_postgres.py` | Connect kwargs forwarding via `FakePsycopgConnect` |
| `src/tests/test_api_upsert_ingestion.py` | Happy path, fetch failure, mapping failure, DB failure |
| `src/tests/test_script_runner.py` | Secret/DB wiring + connection always closed |
| `src/tests/test_material_map_rows.py` | API key → contract field mapping for all seven entities |

Named fake classes only (no inline stubs), matching existing `FakeHttpGet` style.

Run:

```bash
.venv/bin/pytest src/tests/ -q
```

## How to run a script (Airflow-friendly)

Same paths as before; ensure `src` is on `PYTHONPATH`:

```bash
PYTHONPATH=src python src/etl/ingestion/material/material_group.py
PYTHONPATH=src python src/etl/ingestion/material/material_item.py
# …
```

**Recommended load order:** group → class → pdm → (item | natureza | unidade) → caracteristica (after item).

## Design notes (local, gitignored)

Agent working notes also live under `docs/superpowers/` (ignored by git):

- `docs/superpowers/specs/2026-09-18-api-upsert-ingestion-refactor-design.md`
- `docs/superpowers/plans/2026-09-18-api-upsert-ingestion-refactor.md`

This file is the **tracked** project register of the change.
