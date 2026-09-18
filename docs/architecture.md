# Architecture — Open Gov Supply Chain Data (CATMAT)

Snapshot of the material ETL architecture as of 2026-09-18.

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

    subgraph etl_material["etl/material"]
      E1["material_group"]
      E2["material_class"]
      E3["material_pdm"]
      E4["material_item"]
      E5["material_natureza_despesa"]
      E6["material_unidade_fornecimento"]
      E7["material_caracteristica"]
    end

    subgraph observability
      LOG["logging_json<br/>stdout + logs/*.log"]
    end
  end

  ENV --> SK
  SK --> etl_material
  etl_material --> CA
  CA --> API
  etl_material --> contracts
  etl_material --> LOG
  etl_material --> PG
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

## Single ETL pipeline (shared pattern)

```mermaid
sequenceDiagram
  participant ETL as etl/material/*.py
  participant CFG as config
  participant CLI as clients/compras_api
  participant API as compras.gov.br
  participant CTR as contracts
  participant LOG as observability
  participant DB as Postgres

  ETL->>CFG: load API + Postgres secrets
  ETL->>CLI: fetch_all_resultado_pages
  CLI->>API: GET pagina / tamanhoPagina
  API-->>CLI: resultado[]
  CLI-->>ETL: all rows
  ETL->>LOG: api_fetch_ok
  loop each row
    ETL->>CTR: validate + normalize
    ETL->>DB: UPSERT
  end
  ETL->>LOG: upsert_ok / errors to files
```

## Module map

| Layer | Path | Role |
| --- | --- | --- |
| Config | `src/config/load_secret_key.py` | Load secrets from `.env` |
| Client | `src/clients/compras_api.py` | Paginated API fetch |
| Contracts | `src/contracts/material_*.py` | Pydantic validation / normalization |
| ETL | `src/etl/material/*.py` | Extract → validate → upsert |
| SQL | `src/sql/create_table_*.sql` | Table DDL |
| Observability | `src/observability/logging_json.py` | JSON logs to stdout + per-level files |
