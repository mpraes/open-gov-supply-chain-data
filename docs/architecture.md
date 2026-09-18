# Architecture — Open Gov Supply Chain Data (CATMAT)

Snapshot of the material ETL architecture as of 2026-09-18
(updated after the shared API→upsert ingestion refactor).

## System layers

```mermaid
flowchart TB
  subgraph External
    API["compras.gov.br<br/>dadosabertos API"]
    ENV[".env secrets"]
    PG[(Postgres<br/>open_gov_supply_chain)]
  end

  subgraph src
    subgraph config
      SK["load_secret_key"]
    end

    subgraph clients
      CA["compras_api<br/>fetch_all_resultado_pages"]
    end

    subgraph contracts
      C1["MaterialGroupRecord"]
      C2["MaterialClassRecord"]
      C3["MaterialPdmRecord"]
      C4["MaterialItemRecord"]
      C5["MaterialNaturezaDespesaRecord"]
      C6["MaterialUnidadeFornecimentoRecord"]
      C7["MaterialCaracteristicaRecord"]
    end

    subgraph ingestion["etl/ingestion"]
      DB["db.connect_postgres"]
      PIPE["pipeline.run_api_upsert_ingestion"]
      RUN["script_runner.run_script_ingestion"]

      subgraph material["material/*.py"]
        E1["material_group"]
        E2["material_class"]
        E3["material_pdm"]
        E4["material_item"]
        E5["material_natureza_despesa"]
        E6["material_unidade_fornecimento"]
        E7["material_caracteristica"]
      end
    end

    subgraph observability
      LOG["logging_json<br/>stdout + logs/*.log"]
    end
  end

  ENV --> SK
  SK --> RUN
  material --> RUN
  RUN --> DB
  RUN --> PIPE
  PIPE --> CA
  CA --> API
  material --> contracts
  PIPE --> LOG
  DB --> PG
  PIPE --> PG
```

## Load order and table FKs (CATMAT hierarchy)

```mermaid
flowchart LR
  G["material_group<br/>1_consultarGrupoMaterial"]
  C["material_class<br/>2_consultarClasseMaterial"]
  P["material_pdm<br/>3_consultarPdmMaterial"]
  I["material_item<br/>4_consultarItemMaterial"]
  N["material_natureza_despesa<br/>5_consultarMaterialNaturezaDespesa"]
  U["material_unidade_fornecimento<br/>6_consultarMaterialUnidadeFornecimento"]
  K["material_caracteristica<br/>7_consultarMaterialCaracteristicas"]

  G --> C --> P
  P --> I
  P --> N
  P --> U
  I --> K
```

**Recommended run order:** group → class → pdm → (item | natureza | unidade) → caracteristica (after item).

## Shared ingestion pipeline

Reusable for any paginated `resultado` API → Postgres upsert ETL
(not only material). See also [ingestion-api-upsert-refactor.md](./ingestion-api-upsert-refactor.md).

```mermaid
sequenceDiagram
  participant SCR as material/*.py main()
  participant RUN as script_runner
  participant CFG as config
  participant PIPE as pipeline
  participant CLI as clients/compras_api
  participant API as compras.gov.br
  participant MAP as map_*_row + contracts
  participant LOG as observability
  participant DB as Postgres

  SCR->>RUN: run_script_ingestion(...)
  RUN->>CFG: load API + Postgres secrets
  RUN->>DB: connect_postgres
  RUN->>PIPE: run_api_upsert_ingestion
  PIPE->>CLI: fetch_all_resultado_pages
  CLI->>API: GET pagina / tamanhoPagina
  API-->>CLI: resultado[]
  CLI-->>PIPE: all rows
  PIPE->>LOG: api_fetch_ok
  loop each row
    PIPE->>MAP: map_row + validate
    PIPE->>DB: UPSERT
  end
  PIPE->>LOG: upsert_ok / errors
  RUN->>DB: conn.close()
```

## Module map

| Layer | Path | Role |
| --- | --- | --- |
| Config | `src/config/load_secret_key.py` | Load secrets from `.env` |
| Client | `src/clients/compras_api.py` | Paginated API fetch |
| Contracts | `src/contracts/material_*.py` | Pydantic validation / normalization |
| DB wrapper | `src/etl/ingestion/db.py` | Injectable Postgres connect |
| Pipeline | `src/etl/ingestion/pipeline.py` | Fetch → map → upsert |
| Script runner | `src/etl/ingestion/script_runner.py` | Wire secrets + DB for CLI/Airflow scripts |
| ETL scripts | `src/etl/ingestion/material/*.py` | Endpoint, SQL, `map_row`, `main()` |
| SQL | `src/sql/create_table_*.sql` | Table DDL |
| Observability | `src/observability/logging_json.py` | JSON logs to stdout + per-level files |

## Run a material script

```bash
PYTHONPATH=src python src/etl/ingestion/material/material_item.py
```
