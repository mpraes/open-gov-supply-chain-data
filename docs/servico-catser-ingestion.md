# Design: CATSER (serviço) ingestion — all 8 endpoints

Date: 2026-09-18  
Status: implemented (scope A)  
Approach: Reuse `run_script_ingestion` / `run_api_upsert_ingestion`; mirror material layout

## Scope

All CATSER catalog endpoints from `docs/dados_api.md` §02:

| # | Endpoint | Script / table |
| --- | --- | --- |
| 1 | `1_consultarSecaoServico` | `servico_secao` |
| 2 | `2_consultarDivisaoServico` | `servico_divisao` |
| 3 | `3_consultarGrupoServico` | `servico_grupo` |
| 4 | `4_consultarClasseServico` | `servico_classe` |
| 5 | `5_consultarSubClasseServico` | `servico_subclasse` |
| 6 | `6_consultarItemServico` | `servico_item` |
| 7 | `7_consultarUndMedidaServico` | `servico_unidade_medida` |
| 8 | `8_consultarNaturezaDespesaServico` | `servico_natureza_despesa` |

## Layout

```text
src/sql/create_table_servico_*.sql          (8 DDL files)
src/contracts/servico_*.py                  (8 records)
src/contracts/text_normalize.py             (shared helpers)
src/etl/ingestion/servico/servico_*.py      (8 scripts)
src/tests/test_servico_secao_record.py
src/tests/test_servico_records.py
src/tests/test_servico_map_rows.py
src/tests/test_text_normalize.py
```

## Conventions (match material)

- Pydantic `ConfigDict(strict=True)`; text fields uppercased / stripped via `contracts/text_normalize.py`
- `PAGE_SIZE = None` except item (`500`) — only item docs list `tamanhoPagina`
- Upsert + `data_hora_carga = now()` on conflict
- Thin scripts: constants + `map_*_row` + `main()` → `run_script_ingestion`
- Preferred load order: secao → divisao → grupo → classe → subclasse → item → (unidade | natureza)
- Leaf tables (`subclasse`, `unidade_medida`, `natureza_despesa`) have **no FK** to parents:
  the open API can return orphan codes not present in the parent catalog.

## How to run

Create tables in FK order, then:

```bash
PYTHONPATH=src python src/etl/ingestion/servico/servico_secao.py
PYTHONPATH=src python src/etl/ingestion/servico/servico_divisao.py
PYTHONPATH=src python src/etl/ingestion/servico/servico_grupo.py
PYTHONPATH=src python src/etl/ingestion/servico/servico_classe.py
PYTHONPATH=src python src/etl/ingestion/servico/servico_subclasse.py
PYTHONPATH=src python src/etl/ingestion/servico/servico_item.py
PYTHONPATH=src python src/etl/ingestion/servico/servico_unidade_medida.py
PYTHONPATH=src python src/etl/ingestion/servico/servico_natureza_despesa.py
```

## API quirks

- `4_consultarClasseServico` response field is `statusGrupo` (docs); stored as `status_classe`
- `3_consultarGrupoServico` returns `nomeSecao` but not `codigoSecao`; `nomeSecao` can be `null`
- Unidade medida has no `dataHoraAtualizacao` in the sample response
- `6_consultarItemServico` often sends nulls for hierarchy fields (`classe`,
  `subclasse`, and potentially higher levels); only `cod_servico` /
  `nome_servico` are required in our contract

## Non-goals

- Airflow DAGs
- Changing shared pipeline APIs
