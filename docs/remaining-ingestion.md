# Design: remaining API modules — list dumps

Date: 2026-09-23  
Status: implemented  
Approach: Reuse `run_page_batch_ingestion` via `run_remaining_ingestion`; skip `_Id` lookups

Operação (dev/prod/CI): [guia-deploy.md](./guia-deploy.md).

## In scope

| Module | Endpoints | Tables | Driver |
| --- | --- | --- | --- |
| 07 Contratações | 1, 2, 3 | `contratacao`, `contratacao_item`, `contratacao_resultado` | dest `MAX` of the API date column; `.env` `CONTRATACOES_DATA_*` is the ceiling |
| 08 ARP | 1, 1.2, 2, 3, 4, 5 | `arp`, `arp_item`, `arp_unidade_item`, `arp_empenho`, `arp_adesao` | dest `MAX` vigencia dates; children walk missing dest ATA keys (`.env` ATA fallback) |
| 09 Contratos | 1, 1.2, 2 | `contrato`, `contrato_item` | dest `MAX` vigencia dates scoped by `codigo_orgao`; `.env` is the ceiling |
| 10 Fornecedor | 1 | `fornecedor` | `ativo` true then false (page-resume; API has no dest filter) |
| 11 OCDS | `1_releases` | `ocds_release` | dest `MAX(date)` per `buyer_id`; `.env` ceiling |
| 97 Indicadores | 1, 2 | `indicador_consolidado`, `indicador_periodo` | none / `INDICADORES_ANO` (page-resume) |
| 98 Alice | `avisos-restritos` | `alice_aviso` | dest `MAX(data_solicitacao_analise)` as Alice datetime |

`1.2` FimVigencia scripts upsert into the same header table with a different job name.

Date-window jobs raise `data_*Inicial` from dest `MAX(date)` (last-day overlap).
The page cursor is crash resume for that raised slice. Fornecedor and indicadores
cannot skip dest rows at the API.

ARP children (`empenho`, `unidade_item`, `adesao`) call the API only for ATA keys
present in dest `arp` / `arp_item` and missing from the child table. `.env`
`ARP_NUMERO_ATA` is used only when the parent dest table is empty.

`arp`, `arp_item`, and `arp_fim_vigencia` call `run_sliced_remaining_ingestion`
so a window longer than 365 days becomes consecutive jobs
(`arp:2024-01-01:2024-12-31`, …). The API rejects larger ranges.

When `numeroControlePncpAta` is null, `arp_pncp_ata_when_missing` sets the PK to
`{codigo_unidade_gerenciadora}:{numero_ata_registro_preco}`. Rows that lack both
the PNCP id and that pair still fail mapping. A later real PNCP id would be a
second row.

## Out of scope

- Lookup-by-id (`*.1_*`)
- Alice `compras` and `tickets` (lookup by chave/ticket, not a dump)
- 99 Usuarios (user-admin API, PII, write methods)
- Autenticacao

## How to run

```bash
CONTRATACOES_DATA_INICIAL=2024-01-01
CONTRATACOES_DATA_FINAL=2024-12-31
CONTRATACOES_MODALIDADE=6
ARP_DATA_INICIAL=2024-01-01
ARP_DATA_FINAL=2024-12-31
ARP_NUMERO_ATA=...
ARP_UNIDADE_GERENCIADORA=...
ARP_NUMERO_ITEM=...
CONTRATOS_ORGAO=36000
CONTRATOS_DATA_INICIAL=2024-01-01
CONTRATOS_DATA_FINAL=2024-12-31
OCDS_BUYER_ID=00394460000112
OCDS_DATA_INICIAL=2024-01-01
OCDS_DATA_FINAL=2024-12-31
INDICADORES_ANO=2024
ALICE_DATA_INICIAL="01/01/2024 00:00:00"
ALICE_DATA_FINAL="31/12/2024 23:59:59"
```

```bash
PYTHONPATH=src python src/etl/ingestion/contratacoes/contratacao.py
PYTHONPATH=src python src/etl/ingestion/arp/arp.py
PYTHONPATH=src python src/etl/ingestion/contratos/contrato.py
PYTHONPATH=src python src/etl/ingestion/fornecedor/fornecedor.py
PYTHONPATH=src python src/etl/ingestion/ocds/ocds_release.py
PYTHONPATH=src python src/etl/ingestion/indicadores/indicador_periodo.py
PYTHONPATH=src python src/etl/ingestion/alice/alice_aviso.py
```

## API quirks

- Remaining tables use TEXT columns: the API mixes ints, bools, and date strings
- OCDS uses `page` / `offSet` / `releases` / `links.next`, not `resultado`
- Alice avisos returns a JSON array, not `{resultado, totalPaginas}`
- Contract item description field is `descricaoIitem` (API typo), stored as `descricao_iitem`
- Fornecedor primary key is `ni_fornecedor` = CNPJ or CPF
