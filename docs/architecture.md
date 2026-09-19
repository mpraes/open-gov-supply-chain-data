# Architecture — Open Gov Supply Chain Data

Snapshot as of 2026-09-19: shared API→upsert pipeline plus CATMAT (material),
CATSER (serviço), pesquisa de preço (preços praticados), PGC (planejamento),
and UASG catalogs.

## System layers

```mermaid
flowchart TB
  subgraph External
    API["compras.gov.br<br/>dadosabertos API"]
    ENV[".env secrets"]
    PG[(Postgres)]
  end

  subgraph src
    subgraph config
      SK["load_secret_key"]
    end

    subgraph clients
      CA["compras_api<br/>fetch_all_resultado_pages"]
    end

    subgraph contracts
      CM["material_* Record"]
      CS["servico_* Record"]
      CP["preco_* Record"]
      CG["pgc_* Record"]
      CU["uasg_* Record"]
    end

    subgraph ingestion["etl/ingestion"]
      DB["db.connect_postgres"]
      PIPE["pipeline.run_api_upsert_ingestion"]
      RUN["script_runner.run_script_ingestion"]
      MAT["material/*.py"]
      SER["servico/*.py"]
      PRE["precos/*.py"]
      PGC["planejamento/*.py"]
      UASG["uasg/*.py"]
    end

    subgraph observability
      LOG["logging_json"]
    end
  end

  ENV --> SK
  SK --> RUN
  MAT --> RUN
  SER --> RUN
  PRE --> RUN
  PGC --> RUN
  UASG --> RUN
  RUN --> DB
  RUN --> PIPE
  PIPE --> CA
  CA --> API
  MAT --> CM
  SER --> CS
  PRE --> CP
  PGC --> CG
  UASG --> CU
  PIPE --> LOG
  DB --> PG
  PIPE --> PG
```

## CATMAT load order

```mermaid
flowchart LR
  G["material_group"] --> C["material_class"] --> P["material_pdm"]
  P --> I["material_item"]
  P --> N["material_natureza_despesa"]
  P --> U["material_unidade_fornecimento"]
  I --> K["material_caracteristica"]
```

## CATSER load order

```mermaid
flowchart LR
  S["servico_secao"] --> D["servico_divisao"] --> G2["servico_grupo"]
  G2 --> C2["servico_classe"] --> SC["servico_subclasse"] --> I2["servico_item"]
  I2 --> UM["servico_unidade_medida"]
  I2 --> ND["servico_natureza_despesa"]
```

**CATSER run order:** secao → divisao → grupo → classe → subclasse → item → (unidade_medida | natureza_despesa).

## Pesquisa de preço load order

Price endpoints require a CATMAT/CATSER item code. Scripts read codes from
the catalog tables, then paginate each code.

```mermaid
flowchart LR
  MI["material_item"] --> PM["preco_material"]
  MI --> PMD["preco_material_detalhe"]
  SI["servico_item"] --> PS["preco_servico"]
  SI --> PSD["preco_servico_detalhe"]
```

JSON endpoints only (`1_consultarMaterial`, `2_consultarMaterialDetalhe`,
`3_consultarServico`, `4_consultarServicoDetalhe`). CSV variants are skipped.

## PGC load order

Detalhe and agregação require `PGC_ORGAO` + `PGC_ANO` in `.env`. Catalogo
walks CATMAT classes and CATSER groups for one PCA year.

```mermaid
flowchart LR
  ENV["PGC_ORGAO + PGC_ANO"] --> PD["pgc_detalhe"]
  ENV --> PA["pgc_agregacao"]
  MC["material_class"] --> PDC["pgc_detalhe_catalogo"]
  SG["servico_grupo"] --> PDC
```

JSON endpoints only (`1_consultarPgcDetalhe`, `2_consultarPgcDetalheCatalogo`,
`3_consultarPgcAgregacao`). CSV variants are skipped.

See [pgc-ingestion.md](./pgc-ingestion.md).

## UASG load order

Both JSON endpoints require a status boolean. Scripts walk `true` then `false`.
CSV variants are skipped.

```mermaid
flowchart LR
  O["uasg_orgao"] --> U["uasg"]
```

See [uasg-ingestion.md](./uasg-ingestion.md).


## Shared ingestion pipeline

See [ingestion-api-upsert-refactor.md](./ingestion-api-upsert-refactor.md).
CATSER details: [servico-catser-ingestion.md](./servico-catser-ingestion.md).
PGC details: [pgc-ingestion.md](./pgc-ingestion.md).
UASG details: [uasg-ingestion.md](./uasg-ingestion.md).

```mermaid
sequenceDiagram
  participant SCR as material|servico|precos|planejamento|uasg main()
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
| Contracts | `src/contracts/material_*.py`, `servico_*.py`, `preco_*.py`, `pgc_*.py`, `uasg*.py` | Pydantic validation |
| Text helpers | `src/contracts/text_normalize.py` | Shared upper/strip helpers |
| Coercion | `src/contracts/coerce.py` | id/number coercion for price and PGC rows |
| DB wrapper | `src/etl/ingestion/db.py` | Injectable Postgres connect |
| Pipeline | `src/etl/ingestion/pipeline.py` | Fetch → map → upsert |
| Script runner | `src/etl/ingestion/script_runner.py` | Wire secrets + DB for scripts |
| CATMAT ETL | `src/etl/ingestion/material/*.py` | Material catalog scripts |
| CATSER ETL | `src/etl/ingestion/servico/*.py` | Serviço catalog scripts |
| Preços ETL | `src/etl/ingestion/precos/*.py` | Practiced-price scripts |
| PGC ETL | `src/etl/ingestion/planejamento/*.py` | Planning (PGC) scripts |
| UASG ETL | `src/etl/ingestion/uasg/*.py` | UASG and órgão scripts |
| SQL | `src/sql/create_table_*.sql` | Table DDL |
| Observability | `src/observability/logging_json.py` | JSON logs |

## Run scripts

```bash
PYTHONPATH=src python src/etl/ingestion/material/material_item.py
PYTHONPATH=src python src/etl/ingestion/servico/servico_secao.py
PYTHONPATH=src python src/etl/ingestion/precos/preco_material.py
PYTHONPATH=src python src/etl/ingestion/planejamento/pgc_detalhe.py
PYTHONPATH=src python src/etl/ingestion/uasg/uasg_orgao.py
PYTHONPATH=src python src/etl/ingestion/uasg/uasg.py
```
