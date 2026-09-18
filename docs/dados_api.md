# API Compras.gov.br

Compras Públicas em Dados Abertos

- **Version:** `1.0.0`
- **OpenAPI:** `3.1.0`
- **Base URL:** `https://dadosabertos.compras.gov.br`

Protected routes use HTTP Bearer JWT (`Authorization: Bearer <token>`).

## Contents

- [01 - CATÁLOGO - MATERIAL](#01-catálogo-material)
- [02 - CATÁLOGO - SERVIÇO](#02-catálogo-serviço)
- [03 - PESQUISA DE PREÇO - PREÇOS PRATICADOS](#03-pesquisa-de-preço-preços-praticados)
- [04 - PGC](#04-pgc)
- [05 - UASG](#05-uasg)
- [06 - LEGADO](#06-legado)
- [07 - CONTRATAÇÕES](#07-contratações)
- [08 - ARP](#08-arp)
- [09 - CONTRATOS](#09-contratos)
- [10 - FORNECEDOR](#10-fornecedor)
- [11 - OCDS](#11-ocds)
- [97 - INDICADORES](#97-indicadores)
- [98 - ALICE](#98-alice)
- [99 - USUARIOS](#99-usuarios)
- [AUTENTICACAO](#autenticacao)

## 01 - CATÁLOGO - MATERIAL

Catálogo de Materiais (CATMAT): Consulta itens de materiais com dados detalhados.

### `GET /modulo-material/1_consultarGrupoMaterial`

#### Parameters

| Name | In | Type | Required | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `pagina` | query | `integer(int32)` | no | 1 |  |
| `codigoGrupo` | query | `integer(int64)` | no |  |  |
| `statusGrupo` | query | `boolean` | no |  |  |

#### Response

- **Status:** `200`
- **Content type:** `*/*`

```json
{
  "resultado": [
    {
      "codigoGrupo": 0,
      "nomeGrupo": "string",
      "statusGrupo": true,
      "dataHoraAtualizacao": "2024-01-15 10:30:00"
    }
  ],
  "totalRegistros": 0,
  "totalPaginas": 0,
  "paginasRestantes": 0
}
```

### `GET /modulo-material/2_consultarClasseMaterial`

#### Parameters

| Name | In | Type | Required | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `pagina` | query | `integer(int32)` | no | 1 |  |
| `codigoGrupo` | query | `integer(int64)` | no |  |  |
| `codigoClasse` | query | `integer(int64)` | no |  |  |
| `statusClasse` | query | `boolean` | no |  |  |
| `bps` | query | `boolean` | no | false |  |

#### Response

- **Status:** `200`
- **Content type:** `*/*`

```json
{
  "resultado": [
    {
      "codigoClasse": 0,
      "codigoGrupo": 0,
      "nomeGrupo": "string",
      "nomeClasse": "string",
      "statusClasse": true,
      "dataHoraAtualizacao": "2024-01-15T10:30:00"
    }
  ],
  "totalRegistros": 0,
  "totalPaginas": 0,
  "paginasRestantes": 0
}
```

### `GET /modulo-material/3_consultarPdmMaterial`

#### Parameters

| Name | In | Type | Required | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `pagina` | query | `integer(int32)` | no | 1 |  |
| `tamanhoPagina` | query | `integer(int32)` | no | 10 |  |
| `statusPdm` | query | `boolean` | no |  |  |
| `codigoPdm` | query | `integer(int64)` | no |  |  |
| `codigoGrupo` | query | `integer(int64)` | no |  |  |
| `codigoClasse` | query | `integer(int64)` | no |  |  |
| `bps` | query | `boolean` | no | false |  |

#### Response

- **Status:** `200`
- **Content type:** `*/*`

```json
{
  "resultado": [
    {
      "codigoGrupo": 0,
      "nomeGrupo": "string",
      "codigoClasse": 0,
      "nomeClasse": "string",
      "codigoPdm": 0,
      "nomePdm": "string",
      "statusPdm": true,
      "dataHoraAtualizacao": "2024-01-15T10:30:00"
    }
  ],
  "totalRegistros": 0,
  "totalPaginas": 0,
  "paginasRestantes": 0
}
```

### `GET /modulo-material/4_consultarItemMaterial`

#### Parameters

| Name | In | Type | Required | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `pagina` | query | `integer(int32)` | no | 1 |  |
| `tamanhoPagina` | query | `integer(int32)` | no | 10 |  |
| `codigoItem` | query | `integer(int64)` | no |  |  |
| `codigoGrupo` | query | `integer(int64)` | no |  |  |
| `codigoClasse` | query | `integer(int64)` | no |  |  |
| `codigoPdm` | query | `integer(int64)` | no |  |  |
| `descricaoItem` | query | `string` | no |  |  |
| `statusItem` | query | `boolean` | no |  |  |
| `bps` | query | `boolean` | no | false |  |
| `codigo_ncm` | query | `string` | no |  |  |

#### Response

- **Status:** `200`
- **Content type:** `*/*`

```json
{
  "resultado": [
    {
      "codigoItem": 0,
      "codigoGrupo": 0,
      "nomeGrupo": "string",
      "codigoClasse": 0,
      "nomeClasse": "string",
      "codigoPdm": 0,
      "nomePdm": "string",
      "descricaoItem": "string",
      "statusItem": true,
      "itemSustentavel": true,
      "codigo_ncm": "string",
      "descricao_ncm": "string",
      "aplica_margem_preferencia": true,
      "dataHoraAtualizacao": "2024-01-15T10:30:00"
    }
  ],
  "totalRegistros": 0,
  "totalPaginas": 0,
  "paginasRestantes": 0
}
```

### `GET /modulo-material/5_consultarMaterialNaturezaDespesa`

#### Parameters

| Name | In | Type | Required | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `pagina` | query | `integer(int32)` | no | 1 |  |
| `tamanhoPagina` | query | `integer(int32)` | no | 10 |  |
| `codigoPdm` | query | `integer(int64)` | no |  |  |
| `codigoNaturezaDespesa` | query | `string` | no |  |  |
| `statusNaturezaDespesa` | query | `boolean` | no |  |  |

#### Response

- **Status:** `200`
- **Content type:** `*/*`

```json
{
  "resultado": [
    {
      "codigoPdm": 0,
      "codigoNaturezaDespesa": "string",
      "nomeNaturezaDespesa": "string",
      "statusNaturezaDespesa": "string"
    }
  ],
  "totalRegistros": 0,
  "totalPaginas": 0,
  "paginasRestantes": 0
}
```

### `GET /modulo-material/6_consultarMaterialUnidadeFornecimento`

#### Parameters

| Name | In | Type | Required | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `pagina` | query | `integer(int32)` | no | 1 |  |
| `tamanhoPagina` | query | `integer(int32)` | no | 10 |  |
| `codigoPdm` | query | `integer(int64)` | no |  |  |
| `statusUnidadeFornecimentoPdm` | query | `boolean` | no |  |  |

#### Response

- **Status:** `200`
- **Content type:** `*/*`

```json
{
  "resultado": [
    {
      "codigoPdm": 0,
      "siglaUnidadeFornecimento": "string",
      "nomeUnidadeFornecimento": "string",
      "descricaoUnidadeFornecimento": "string",
      "siglaUnidadeMedida": "string",
      "capacidadeUnidadeFornecimento": 0,
      "numeroSequencialUnidadeFornecimento": 0,
      "statusUnidadeFornecimentoPdm": true,
      "statusUnidadeFornecimento": true,
      "dataHoraAtualizacao": "2024-01-15T10:30:00"
    }
  ],
  "totalRegistros": 0,
  "totalPaginas": 0,
  "paginasRestantes": 0
}
```

### `GET /modulo-material/7_consultarMaterialCaracteristicas`

#### Parameters

| Name | In | Type | Required | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `pagina` | query | `integer(int32)` | no | 1 |  |
| `tamanhoPagina` | query | `integer(int32)` | no | 10 |  |
| `codigoItem` | query | `integer(int64)` | no |  |  |

#### Response

- **Status:** `200`
- **Content type:** `*/*`

```json
{
  "resultado": [
    {
      "codigoItem": 0,
      "itemSustentavel": true,
      "statusItem": true,
      "codigoCaracteristica": "string",
      "nomeCaracteristica": "string",
      "statusCaracteristica": true,
      "codigoValorCaracteristica": "string",
      "nomeValorCaracteristica": "string",
      "statusValorCaracteristica": true,
      "numeroCaracteristica": 0,
      "siglaUnidadeMedida": "string",
      "dataHoraAtualizacao": "2022-01-01T00:00:00"
    }
  ],
  "totalRegistros": 0,
  "totalPaginas": 0,
  "paginasRestantes": 0
}
```

## 02 - CATÁLOGO - SERVIÇO

Catálogo de Serviços (CATSER): Consulta serviços com informações detalhadas.

### `GET /modulo-servico/1_consultarSecaoServico`

#### Parameters

| Name | In | Type | Required | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `pagina` | query | `integer(int32)` | no | 1 |  |
| `codigoSecao` | query | `integer(int64)` | no |  |  |
| `statusSecao` | query | `boolean` | no |  |  |

#### Response

- **Status:** `200`
- **Content type:** `*/*`

```json
{
  "resultado": [
    {
      "codigoSecao": 0,
      "nomeSecao": "string",
      "statusSecao": true,
      "dataHoraAtualizacao": "2024-01-15T10:30:00"
    }
  ],
  "totalRegistros": 0,
  "totalPaginas": 0,
  "paginasRestantes": 0
}
```

### `GET /modulo-servico/2_consultarDivisaoServico`

#### Parameters

| Name | In | Type | Required | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `pagina` | query | `integer(int32)` | no | 1 |  |
| `codigoSecao` | query | `integer(int64)` | no |  |  |
| `codigoDivisao` | query | `integer(int64)` | no |  |  |
| `statusDivisao` | query | `boolean` | no |  |  |

#### Response

- **Status:** `200`
- **Content type:** `*/*`

```json
{
  "resultado": [
    {
      "codigoSecao": 0,
      "nomeSecao": "string",
      "codigoDivisao": 0,
      "nomeDivisao": "string",
      "statusDivisao": true,
      "dataHoraAtualizacao": "2024-01-15T10:30:00"
    }
  ],
  "totalRegistros": 0,
  "totalPaginas": 0,
  "paginasRestantes": 0
}
```

### `GET /modulo-servico/3_consultarGrupoServico`

#### Parameters

| Name | In | Type | Required | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `pagina` | query | `integer(int32)` | no | 1 |  |
| `codigoDivisao` | query | `integer(int64)` | no |  |  |
| `codigoGrupo` | query | `integer(int64)` | no |  |  |
| `statusGrupo` | query | `boolean` | no |  |  |

#### Response

- **Status:** `200`
- **Content type:** `*/*`

```json
{
  "resultado": [
    {
      "nomeSecao": "string",
      "codigoDivisao": 0,
      "nomeDivisao": "string",
      "codigoGrupo": 0,
      "nomeGrupo": "string",
      "statusGrupo": true,
      "dataHoraAtualizacao": "2024-01-15T10:30:00"
    }
  ],
  "totalRegistros": 0,
  "totalPaginas": 0,
  "paginasRestantes": 0
}
```

### `GET /modulo-servico/4_consultarClasseServico`

#### Parameters

| Name | In | Type | Required | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `pagina` | query | `integer(int32)` | no | 1 |  |
| `codigoGrupo` | query | `integer(int64)` | no |  |  |
| `codigoClasse` | query | `integer(int64)` | no |  |  |
| `statusGrupo` | query | `boolean` | no |  |  |

#### Response

- **Status:** `200`
- **Content type:** `*/*`

```json
{
  "resultado": [
    {
      "codigoGrupo": 0,
      "nomeGrupo": "string",
      "codigoClasse": 0,
      "nomeClasse": "string",
      "statusGrupo": true,
      "dataHoraAtualizacao": "2024-01-15T10:30:00"
    }
  ],
  "totalRegistros": 0,
  "totalPaginas": 0,
  "paginasRestantes": 0
}
```

### `GET /modulo-servico/5_consultarSubClasseServico`

#### Parameters

| Name | In | Type | Required | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `pagina` | query | `integer(int32)` | no | 1 |  |
| `codigoClasse` | query | `integer(int64)` | no |  |  |
| `codigoSubclasse` | query | `integer(int64)` | no |  |  |
| `statusSubclasse` | query | `boolean` | no |  |  |

#### Response

- **Status:** `200`
- **Content type:** `*/*`

```json
{
  "resultado": [
    {
      "codigoClasse": 0,
      "nomeClasse": "string",
      "codigoSubclasse": 0,
      "nomeSubclasse": "string",
      "statusSubclasse": true,
      "dataHoraAtualizacao": "2024-01-15T10:30:00"
    }
  ],
  "totalRegistros": 0,
  "totalPaginas": 0,
  "paginasRestantes": 0
}
```

### `GET /modulo-servico/6_consultarItemServico`

#### Parameters

| Name | In | Type | Required | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `pagina` | query | `integer(int32)` | no | 1 |  |
| `tamanhoPagina` | query | `integer(int32)` | no | 10 |  |
| `codigoSecao` | query | `integer(int64)` | no |  |  |
| `codigoDivisao` | query | `integer(int64)` | no |  |  |
| `codigoGrupo` | query | `integer(int64)` | no |  |  |
| `codigoClasse` | query | `integer(int64)` | no |  |  |
| `codigoSubclasse` | query | `integer(int64)` | no |  |  |
| `codigoCpc` | query | `integer(int64)` | no |  |  |
| `codigoServico` | query | `integer(int64)` | no |  |  |
| `exclusivoCentralCompras` | query | `boolean` | no |  |  |
| `statusServico` | query | `boolean` | no |  |  |

#### Response

- **Status:** `200`
- **Content type:** `*/*`

```json
{
  "resultado": [
    {
      "codigoSecao": 0,
      "nomeSecao": "string",
      "codigoDivisao": 0,
      "nomeDivisao": "string",
      "codigoGrupo": 0,
      "nomeGrupo": "string",
      "codigoClasse": 0,
      "nomeClasse": "string",
      "codigoSubclasse": 0,
      "nomeSubclasse": "string",
      "codigoServico": 0,
      "nomeServico": "string",
      "codigoCpc": 0,
      "exclusivoCentralCompras": true,
      "statusServico": true,
      "dataHoraAtualizacao": "2024-01-15T10:30:00"
    }
  ],
  "totalRegistros": 0,
  "totalPaginas": 0,
  "paginasRestantes": 0
}
```

### `GET /modulo-servico/7_consultarUndMedidaServico`

#### Parameters

| Name | In | Type | Required | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `pagina` | query | `integer(int32)` | no | 1 |  |
| `codigoServico` | query | `integer(int64)` | no |  |  |
| `statusUnidadeMedida` | query | `boolean` | no |  |  |

#### Response

- **Status:** `200`
- **Content type:** `*/*`

```json
{
  "resultado": [
    {
      "codigoServico": 0,
      "siglaUnidadeMedida": "string",
      "nomeUnidadeMedida": "string",
      "statusUnidadeMedida": true
    }
  ],
  "totalRegistros": 0,
  "totalPaginas": 0,
  "paginasRestantes": 0
}
```

### `GET /modulo-servico/8_consultarNaturezaDespesaServico`

#### Parameters

| Name | In | Type | Required | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `pagina` | query | `integer(int32)` | no | 1 |  |
| `codigoServico` | query | `integer(int64)` | no |  |  |
| `codigoNaturezaDespesa` | query | `string` | no |  |  |
| `statusNaturezaDespesa` | query | `boolean` | no |  |  |

#### Response

- **Status:** `200`
- **Content type:** `*/*`

```json
{
  "resultado": [
    {
      "codigoServico": 0,
      "codigoNaturezaDespesa": "string",
      "nomeNaturezaDespesa": "string",
      "statusNaturezaDespesa": true
    }
  ],
  "totalRegistros": 0,
  "totalPaginas": 0,
  "paginasRestantes": 0
}
```

## 03 - PESQUISA DE PREÇO - PREÇOS PRATICADOS

Consulta preços praticados nas compras públicas por códigos de itens do CATMAT e CATSER.

### `GET /modulo-pesquisa-preco/1_consultarMaterial`

#### Parameters

| Name | In | Type | Required | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `pagina` | query | `integer(int32)` | no | 1 |  |
| `tamanhoPagina` | query | `integer(int32)` | no | 10 |  |
| `tipo` | query | `string` | yes |  | Values: `codigoItemCatalogo`, `codigoPdm` |
| `codigo` | query | `string` | yes |  |  |
| `codigoUasg` | query | `string` | no |  |  |
| `estado` | query | `string` | no |  |  |
| `codigoMunicipio` | query | `integer(int32)` | no |  |  |
| `dataResultado` | query | `boolean` | no | false |  |
| `codigoClasse` | query | `integer(int32)` | no |  |  |
| `poder` | query | `string` | no |  |  |
| `esfera` | query | `string` | no |  |  |
| `idCompra` | query | `string` | no |  |  |
| `dataCompraInicio` | query | `string` | no |  | YYYY-MM-DD |
| `dataCompraFim` | query | `string` | no |  | YYYY-MM-DD |

#### Response

- **Status:** `200`
- **Content type:** `*/*`

```json
{
  "resultado": [
    {
      "idCompra": 0,
      "dataCompra": "YYYY-MM-DD",
      "forma": "string",
      "modalidade": 0,
      "dataHoraAtualizacaoCompra": "2024-01-15T10:30:00",
      "idItemCompra": 0,
      "numeroItemCompra": 0,
      "niFornecedor": "string",
      "codigoItemCatalogo": 0,
      "quantidade": 0,
      "precoUnitario": 0,
      "descricaoItem": "string",
      "siglaUnidadeFornecimento": "string",
      "nomeUnidadeFornecimento": "string",
      "capacidadeUnidadeFornecimento": 0,
      "siglaUnidadeMedida": "string",
      "nomeUnidadeMedida": "string",
      "criterioJulgamento": "string",
      "percentualMaiorDesconto": 0,
      "nomeFornecedor": "string",
      "marca": "string",
      "dataResultado": "YYYY-MM-DD",
      "dataHoraAtualizacaoItem": "2024-01-15T10:30:00",
      "codigoUasg": "string",
      "nomeUasg": "string",
      "codigoOrgao": 0,
      "nomeOrgao": "string",
      "estado": "string",
      "codigoMunicipio": 0,
      "municipio": "string",
      "poder": "string",
      "esfera": "string",
      "dataHoraAtualizacaoUasg": "2024-01-15T10:30:00",
      "codigoClasse": 0,
      "nomeClasse": "string",
      "idCompraItem": "string",
      "objetoCompra": "string",
      "descricaoDetalhadaItem": "string",
      "dataAtualizacaoFato": "2024-01-15T10:30:00",
      "codigoPdm": "string",
      "nomePdm": "string"
    }
  ],
  "totalRegistros": 0,
  "totalPaginas": 0,
  "paginasRestantes": 0
}
```

### `GET /modulo-pesquisa-preco/1.1_consultarMaterial_CSV`

#### Parameters

| Name | In | Type | Required | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `pagina` | query | `integer(int32)` | no | 1 |  |
| `tamanhoPagina` | query | `integer(int32)` | no | 10 |  |
| `tipo` | query | `string` | yes |  | Values: `codigoItemCatalogo`, `codigoPdm` |
| `codigo` | query | `string` | yes |  |  |
| `codigoUasg` | query | `string` | no |  |  |
| `estado` | query | `string` | no |  |  |
| `codigoMunicipio` | query | `integer(int32)` | no |  |  |
| `dataResultado` | query | `boolean` | no | false |  |
| `codigoClasse` | query | `integer(int32)` | no |  |  |
| `poder` | query | `string` | no |  |  |
| `esfera` | query | `string` | no |  |  |
| `idCompra` | query | `string` | no |  |  |
| `dataCompraInicio` | query | `string` | no |  | YYYY-MM-DD |
| `dataCompraFim` | query | `string` | no |  | YYYY-MM-DD |

#### Response

- **Status:** `200`
- **Content type:** `text/csv`

CSV download (`text/csv`).

### `GET /modulo-pesquisa-preco/2_consultarMaterialDetalhe`

#### Parameters

| Name | In | Type | Required | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `pagina` | query | `integer(int32)` | no | 1 |  |
| `tamanhoPagina` | query | `integer(int32)` | no | 10 |  |
| `codigoItemCatalogo` | query | `integer(int32)` | yes |  |  |
| `dataCompraInicio` | query | `string` | no |  | YYYY-MM-DD |
| `dataCompraFim` | query | `string` | no |  | YYYY-MM-DD |

#### Response

- **Status:** `200`
- **Content type:** `*/*`

```json
{
  "resultado": [
    {
      "idCompra": "string",
      "idItemCompra": 0,
      "numeroItemCompra": 0,
      "codigoItemCatalogo": 0,
      "objetoCompra": "string",
      "descricaoDetalhadaItem": "string",
      "dataAtualizacaoFato": "2024-01-15T10:30:00"
    }
  ],
  "totalRegistros": 0,
  "totalPaginas": 0,
  "paginasRestantes": 0
}
```

### `GET /modulo-pesquisa-preco/2.1_consultarMaterialDetalhe_CSV`

#### Parameters

| Name | In | Type | Required | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `pagina` | query | `integer(int32)` | no | 1 |  |
| `tamanhoPagina` | query | `integer(int32)` | no | 10 |  |
| `codigoItemCatalogo` | query | `integer(int32)` | no |  |  |
| `dataCompraInicio` | query | `string` | no |  | YYYY-MM-DD |
| `dataCompraFim` | query | `string` | no |  | YYYY-MM-DD |

#### Response

- **Status:** `200`
- **Content type:** `text/csv`

CSV download (`text/csv`).

### `GET /modulo-pesquisa-preco/3_consultarServico`

#### Parameters

| Name | In | Type | Required | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `pagina` | query | `integer(int32)` | no | 1 |  |
| `tamanhoPagina` | query | `integer(int32)` | no | 10 |  |
| `codigoItemCatalogo` | query | `integer(int32)` | yes |  |  |
| `codigoUasg` | query | `string` | no |  |  |
| `estado` | query | `string` | no |  |  |
| `codigoMunicipio` | query | `integer(int32)` | no |  |  |
| `dataResultado` | query | `boolean` | no | false |  |
| `poder` | query | `string` | no |  |  |
| `esfera` | query | `string` | no |  |  |
| `dataCompraInicio` | query | `string` | no |  | YYYY-MM-DD |
| `dataCompraFim` | query | `string` | no |  | YYYY-MM-DD |
| `idCompra` | query | `string` | no |  |  |

#### Response

- **Status:** `200`
- **Content type:** `*/*`

```json
{
  "resultado": [
    {
      "idCompra": "string",
      "idItemCompra": 0,
      "forma": "string",
      "modalidade": 0,
      "criterioJulgamento": "string",
      "numeroItemCompra": 0,
      "descricaoItem": "string",
      "codigoItemCatalogo": 0,
      "nomeUnidadeMedida": "string",
      "siglaUnidadeMedida": "string",
      "quantidade": 0,
      "precoUnitario": 0,
      "percentualMaiorDesconto": 0,
      "niFornecedor": "string",
      "nomeFornecedor": "string",
      "codigoUasg": "string",
      "nomeUasg": "string",
      "codigoMunicipio": 0,
      "municipio": "string",
      "estado": "string",
      "codigoOrgao": 0,
      "nomeOrgao": "string",
      "poder": "string",
      "esfera": "string",
      "dataCompra": "2024-01-15",
      "dataHoraAtualizacaoCompra": "2024-01-15T10:30:00",
      "dataHoraAtualizacaoItem": "2024-01-15T10:30:00",
      "dataResultado": "2024-01-1",
      "dataHoraAtualizacaoUasg": "2024-01-15T10:30:00",
      "objetoCompra": "string",
      "descricaoDetalhadaItem": "string",
      "dataAtualizacaoFato": "2024-01-15T10:30:00"
    }
  ],
  "totalRegistros": 0,
  "totalPaginas": 0,
  "paginasRestantes": 0
}
```

### `GET /modulo-pesquisa-preco/3.1_consultarServico_CSV`

#### Parameters

| Name | In | Type | Required | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `pagina` | query | `integer(int32)` | no | 1 |  |
| `tamanhoPagina` | query | `integer(int32)` | no | 10 |  |
| `codigoItemCatalogo` | query | `integer(int32)` | yes |  |  |
| `codigoUasg` | query | `string` | no |  |  |
| `estado` | query | `string` | no |  |  |
| `codigoMunicipio` | query | `integer(int32)` | no |  |  |
| `dataResultado` | query | `boolean` | no | false |  |
| `poder` | query | `string` | no |  |  |
| `esfera` | query | `string` | no |  |  |
| `dataCompraInicio` | query | `string` | no |  | YYYY-MM-DD |
| `dataCompraFim` | query | `string` | no |  | YYYY-MM-DD |
| `idCompra` | query | `string` | no |  |  |

#### Response

- **Status:** `200`
- **Content type:** `text/csv`

CSV download (`text/csv`).

### `GET /modulo-pesquisa-preco/4_consultarServicoDetalhe`

#### Parameters

| Name | In | Type | Required | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `pagina` | query | `integer(int32)` | no | 1 |  |
| `tamanhoPagina` | query | `integer(int32)` | no | 10 |  |
| `codigoItemCatalogo` | query | `integer(int32)` | yes |  |  |
| `dataCompraInicio` | query | `string` | no |  | YYYY-MM-DD |
| `dataCompraFim` | query | `string` | no |  | YYYY-MM-DD |

#### Response

- **Status:** `200`
- **Content type:** `*/*`

```json
{
  "resultado": [
    {
      "idCompra": "string",
      "idItemCompra": 0,
      "numeroItemCompra": 0,
      "codigoItemCatalogo": 0,
      "objetoCompra": "string",
      "descricaoDetalhadaItem": "string",
      "dataAtualizacaoFato": "2024-01-15T10:30:00"
    }
  ],
  "totalRegistros": 0,
  "totalPaginas": 0,
  "paginasRestantes": 0
}
```

### `GET /modulo-pesquisa-preco/4.1_consultarServicoDetalhe_CSV`

#### Parameters

| Name | In | Type | Required | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `pagina` | query | `integer(int32)` | no | 1 |  |
| `tamanhoPagina` | query | `integer(int32)` | no | 10 |  |
| `codigoItemCatalogo` | query | `integer(int32)` | no |  |  |
| `dataCompraInicio` | query | `string` | no |  | YYYY-MM-DD |
| `dataCompraFim` | query | `string` | no |  | YYYY-MM-DD |

#### Response

- **Status:** `200`
- **Content type:** `text/csv`

CSV download (`text/csv`).

## 04 - PGC

Consulta dados sobre Planejamento e Gerenciamento de Contratações (PGC).

### `GET /modulo-pgc/1_consultarPgcDetalhe`

#### Parameters

| Name | In | Type | Required | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `pagina` | query | `integer(int32)` | no | 1 |  |
| `tamanhoPagina` | query | `integer(int32)` | no | 10 |  |
| `orgao` | query | `string` | yes |  |  |
| `anoPcaProjetoCompra` | query | `integer(int32)` | yes |  |  |
| `codigoUasg` | query | `string` | no |  |  |

#### Response

- **Status:** `200`
- **Content type:** `*/*`

```json
{
  "resultado": [
    {
      "codigoUasg": "string",
      "nomeUasg": "string",
      "orgao": "string",
      "numeroArtefato": 0,
      "anoArtefato": 0,
      "codigoEstadoArtefato": 0,
      "codigoCategoriaArtefato": 0,
      "descricaoArtefato": "string",
      "codigoTipoArtefato": 0,
      "ordemDfd": 0,
      "descricaoObjetoDfd": "string",
      "nivelPrioridadeDfd": 0,
      "dataPrevistaFormalizacaoDemanda": "2024-01-15T10:30:00",
      "codigoAreaDfd": "string",
      "tipoItem": "string",
      "itemSustentavel": true,
      "codigoGrupoMaterial": 0,
      "nomeGrupoMaterial": "string",
      "codigoClasseMaterial": 0,
      "nomeClasseMaterial": "string",
      "codigoPdmMaterial": 0,
      "nomePdmMaterial": "string",
      "codigoSecaoServico": 0,
      "nomeSecaoServico": "string",
      "codigoDivisaoServico": 0,
      "nomeDivisaoServico": "string",
      "codigoGrupoServico": 0,
      "nomeGrupoServico": "string",
      "codigoClasseServico": 0,
      "nomeClasseServico": "string",
      "codigoSubclasseServico": 0,
      "nomeSubclasseServico": "string",
      "codigoItemCatalogo": "string",
      "descricaoItemCatalogo": "string",
      "siglaUnidadeFornecimento": "string",
      "nomeUnidadeFornecimento": "string",
      "quantidadeItem": 0,
      "valorUnitarioItem": 0,
      "valorTotalItem": 0,
      "tituloProjetoCompra": "string",
      "descricaoProjetoCompra": "string",
      "anoPcaProjetoCompra": 0,
      "dataInicioProcessoCompra": "2024-01-15T10:30:00",
      "dataFimProcessoCompra": "2024-01-15T10:30:00",
      "duracaoProcessoCompra": 0,
      "numeroItemPncp": 0,
      "statusContratacaoExecucao": 0,
      "dataHoraPublicacaoPncp": "2024-01-15T10:30:00",
      "dataHoraAtualizacaoArtefato": "2024-01-15T10:30:00",
      "dataHoraAtualizacaoProjetoCompra": "2024-01-15T10:30:00",
      "dataHoraAtualizacaoDfd": "2024-01-15T10:30:00",
      "dataHoraAtualizacaoItem": "2024-01-15T10:30:00"
    }
  ],
  "totalRegistros": 0,
  "totalPaginas": 0,
  "paginasRestantes": 0
}
```

### `GET /modulo-pgc/1.1_consultarPgcDetalhe_CSV`

#### Parameters

| Name | In | Type | Required | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `pagina` | query | `integer(int32)` | no | 1 |  |
| `tamanhoPagina` | query | `integer(int32)` | no | 10 |  |
| `orgao` | query | `string` | yes |  |  |
| `anoPcaProjetoCompra` | query | `integer(int32)` | yes |  |  |
| `codigoUasg` | query | `string` | no |  |  |

#### Response

- **Status:** `200`
- **Content type:** `text/csv`

CSV download (`text/csv`).

### `GET /modulo-pgc/2_consultarPgcDetalheCatalogo`

#### Parameters

| Name | In | Type | Required | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `pagina` | query | `integer(int32)` | no | 1 |  |
| `tamanhoPagina` | query | `integer(int32)` | no | 10 |  |
| `anoPcaProjetoCompra` | query | `integer(int32)` | yes |  |  |
| `tipo` | query | `string` | yes |  | Values: `Servico`, `Material` |
| `codigo` | query | `integer(int32)` | yes |  | Código de classe para material ou código do grupo para serviço |

#### Response

- **Status:** `200`
- **Content type:** `*/*`

```json
{
  "resultado": [
    {
      "codigoUasg": "string",
      "nomeUasg": "string",
      "orgao": "string",
      "numeroArtefato": 0,
      "anoArtefato": 0,
      "codigoEstadoArtefato": 0,
      "codigoCategoriaArtefato": 0,
      "descricaoArtefato": "string",
      "codigoTipoArtefato": 0,
      "ordemDfd": 0,
      "descricaoObjetoDfd": "string",
      "nivelPrioridadeDfd": 0,
      "dataPrevistaFormalizacaoDemanda": "2024-01-15T10:30:00",
      "codigoAreaDfd": "string",
      "tipoItem": "string",
      "itemSustentavel": true,
      "codigoGrupoMaterial": 0,
      "nomeGrupoMaterial": "string",
      "codigoClasseMaterial": 0,
      "nomeClasseMaterial": "string",
      "codigoPdmMaterial": 0,
      "nomePdmMaterial": "string",
      "codigoSecaoServico": 0,
      "nomeSecaoServico": "string",
      "codigoDivisaoServico": 0,
      "nomeDivisaoServico": "string",
      "codigoGrupoServico": 0,
      "nomeGrupoServico": "string",
      "codigoClasseServico": 0,
      "nomeClasseServico": "string",
      "codigoSubclasseServico": 0,
      "nomeSubclasseServico": "string",
      "codigoItemCatalogo": "string",
      "descricaoItemCatalogo": "string",
      "siglaUnidadeFornecimento": "string",
      "nomeUnidadeFornecimento": "string",
      "quantidadeItem": 0,
      "valorUnitarioItem": 0,
      "valorTotalItem": 0,
      "tituloProjetoCompra": "string",
      "descricaoProjetoCompra": "string",
      "anoPcaProjetoCompra": 0,
      "dataInicioProcessoCompra": "2024-01-15T10:30:00",
      "dataFimProcessoCompra": "2024-01-15T10:30:00",
      "duracaoProcessoCompra": 0,
      "numeroItemPncp": 0,
      "statusContratacaoExecucao": 0,
      "dataHoraPublicacaoPncp": "2024-01-15T10:30:00",
      "dataHoraAtualizacaoArtefato": "2024-01-15T10:30:00",
      "dataHoraAtualizacaoProjetoCompra": "2024-01-15T10:30:00",
      "dataHoraAtualizacaoDfd": "2024-01-15T10:30:00",
      "dataHoraAtualizacaoItem": "2024-01-15T10:30:00"
    }
  ],
  "totalRegistros": 0,
  "totalPaginas": 0,
  "paginasRestantes": 0
}
```

### `GET /modulo-pgc/2.1_consultarPgcDetalheCatalogo_CSV`

#### Parameters

| Name | In | Type | Required | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `pagina` | query | `integer(int32)` | no | 1 |  |
| `tamanhoPagina` | query | `integer(int32)` | no | 10 |  |
| `anoPcaProjetoCompra` | query | `integer(int32)` | yes |  |  |
| `tipo` | query | `string` | yes |  | Values: `Servico`, `Material` |
| `codigo` | query | `integer(int32)` | yes |  | Código de classe para material ou código do grupo para serviço |

#### Response

- **Status:** `200`
- **Content type:** `text/csv`

CSV download (`text/csv`).

### `GET /modulo-pgc/3_consultarPgcAgregacao`

#### Parameters

| Name | In | Type | Required | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `pagina` | query | `integer(int32)` | no | 1 |  |
| `orgao` | query | `string` | yes |  |  |
| `ano` | query | `integer(int32)` | yes |  |  |

#### Response

- **Status:** `200`
- **Content type:** `*/*`

```json
{
  "resultado": [
    {
      "orgao": "string",
      "ano": 0,
      "poder": "string",
      "esfera": "string",
      "dataHoraPublicacaoPncp": "2024-01-15T10:30:00",
      "dataHoraAtualizacao": "2024-01-15T10:30:00",
      "quantidadeTotalItens": 0,
      "valorTotalEstimado": 0
    }
  ],
  "totalRegistros": 0,
  "totalPaginas": 0,
  "paginasRestantes": 0
}
```

### `GET /modulo-pgc/3.1_consultarPgcAgregacao_CSV`

#### Parameters

| Name | In | Type | Required | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `pagina` | query | `integer(int32)` | no | 1 |  |
| `orgao` | query | `string` | yes |  |  |
| `ano` | query | `integer(int32)` | yes |  |  |

#### Response

- **Status:** `200`
- **Content type:** `text/csv`

CSV download (`text/csv`).

## 05 - UASG

Consulta dados sobre Unidades Administrativas de Serviços Gerais (UASG).

### `GET /modulo-uasg/1_consultarUasg`

#### Parameters

| Name | In | Type | Required | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `pagina` | query | `integer(int32)` | no | 1 |  |
| `codigoUasg` | query | `string` | no |  |  |
| `usoSisg` | query | `boolean` | no |  |  |
| `cnpjCpfOrgao` | query | `string` | no |  |  |
| `cnpjCpfOrgaoVinculado` | query | `string` | no |  |  |
| `cnpjCpfOrgaoSuperior` | query | `string` | no |  |  |
| `siglaUf` | query | `string` | no |  |  |
| `statusUasg` | query | `boolean` | yes |  |  |

#### Response

- **Status:** `200`
- **Content type:** `*/*`

```json
{
  "resultado": [
    {
      "codigoUasg": "string",
      "nomeUasg": "string",
      "usoSisg": true,
      "adesaoSiasg": true,
      "siglaUf": "string",
      "codigoMunicipio": 0,
      "codigoMunicipioIbge": 0,
      "nomeMunicipioIbge": "string",
      "codigoUnidadePolo": 0,
      "nomeUnidadePolo": "string",
      "codigoUnidadeEspelho": 0,
      "nomeUnidadeEspelho": "string",
      "uasgCadastradora": true,
      "cnpjCpfUasg": "string",
      "codigoOrgao": 0,
      "cnpjCpfOrgao": "string",
      "cnpjCpfOrgaoVinculado": "string",
      "cnpjCpfOrgaoSuperior": "string",
      "codigoSiorg": "string",
      "statusUasg": true,
      "dataImplantacaoSidec": "2024-01-15T10:30:00",
      "dataHoraMovimento": "2024-01-15T10:30:00"
    }
  ],
  "totalRegistros": 0,
  "totalPaginas": 0,
  "paginasRestantes": 0
}
```

### `GET /modulo-uasg/1.1_consultarUasg_CSV`

#### Parameters

| Name | In | Type | Required | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `pagina` | query | `integer(int32)` | no | 1 |  |
| `codigoUasg` | query | `string` | no |  |  |
| `usoSisg` | query | `boolean` | no |  |  |
| `cnpjCpfOrgao` | query | `string` | no |  |  |
| `cnpjCpfOrgaoVinculado` | query | `string` | no |  |  |
| `cnpjCpfOrgaoSuperior` | query | `string` | no |  |  |
| `siglaUf` | query | `string` | no |  |  |
| `statusUasg` | query | `boolean` | yes |  |  |

#### Response

- **Status:** `200`
- **Content type:** `text/csv`

CSV download (`text/csv`).

### `GET /modulo-uasg/2_consultarOrgao`

#### Parameters

| Name | In | Type | Required | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `pagina` | query | `integer(int32)` | no | 1 |  |
| `cnpjCpfOrgao` | query | `string` | no |  |  |
| `cnpjCpfOrgaoVinculado` | query | `string` | no |  |  |
| `cnpjCpfOrgaoSuperior` | query | `string` | no |  |  |
| `codigoOrgao` | query | `integer(int32)` | no |  |  |
| `statusOrgao` | query | `boolean` | yes |  |  |
| `usoSisg` | query | `boolean` | no |  |  |

#### Response

- **Status:** `200`
- **Content type:** `*/*`

```json
{
  "resultado": [
    {
      "codigoOrgao": 0,
      "nomeOrgao": "string",
      "nomeMnemonicoOrgao": "string",
      "cnpjCpfOrgao": "string",
      "codigoOrgaoVinculado": 0,
      "cnpjCpfOrgaoVinculado": "string",
      "nomeOrgaoVinculado": "string",
      "codigoOrgaoSuperior": 0,
      "cnpjCpfOrgaoSuperior": "string",
      "nomeOrgaoSuperior": "string",
      "codigoTipoAdministracao": 0,
      "nomeTipoAdministracao": "string",
      "poder": "string",
      "esfera": "string",
      "usoSisg": true,
      "statusOrgao": true,
      "dataHoraMovimento": "2024-01-15T10:30:00"
    }
  ],
  "totalRegistros": 0,
  "totalPaginas": 0,
  "paginasRestantes": 0
}
```

### `GET /modulo-uasg/2.1_consultarOrgao_CSV`

#### Parameters

| Name | In | Type | Required | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `pagina` | query | `integer(int32)` | no | 1 |  |
| `cnpjCpfOrgao` | query | `string` | no |  |  |
| `cnpjCpfOrgaoVinculado` | query | `string` | no |  |  |
| `cnpjCpfOrgaoSuperior` | query | `string` | no |  |  |
| `codigoOrgao` | query | `integer(int32)` | no |  |  |
| `statusOrgao` | query | `boolean` | yes |  |  |
| `usoSisg` | query | `boolean` | no |  |  |

#### Response

- **Status:** `200`
- **Content type:** `text/csv`

CSV download (`text/csv`).

## 06 - LEGADO

Consulta licitações realizadas sob a Lei nº 8.666/1993 e leis anteriores à Lei nº 14.133/2021.

### `GET /modulo-legado/1_consultarLicitacao`

#### Parameters

| Name | In | Type | Required | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `pagina` | query | `integer(int32)` | no | 1 |  |
| `tamanhoPagina` | query | `integer(int32)` | no | 10 |  |
| `uasg` | query | `integer(int32)` | no |  |  |
| `numero_aviso` | query | `integer(int32)` | no |  |  |
| `modalidade` | query | `integer(int32)` | no |  |  |
| `data_publicacao_inicial` | query | `string` | yes |  | YYYY-MM-DD |
| `data_publicacao_final` | query | `string` | yes |  | YYYY-MM-DD |
| `pertence14133` | query | `boolean` | no |  |  |

#### Response

- **Status:** `200`
- **Content type:** `*/*`

```json
{
  "resultado": [
    {
      "id_compra": "string",
      "identificador": "string",
      "numero_processo": "string",
      "uasg": 0,
      "modalidade": 0,
      "nome_modalidade": "string",
      "numero_aviso": 0,
      "situacao_aviso": "string",
      "tipo_pregao": "string",
      "tipo_recurso": "string",
      "nome_responsavel": "string",
      "funcao_responsavel": "string",
      "numero_itens": 0,
      "valor_estimado_total": 0,
      "valor_homologado_total": 0,
      "informacoes_gerais": "string",
      "objeto": "string",
      "endereco_entrega_edital": "string",
      "codigo_municipio_uasg": 0,
      "data_abertura_proposta": "2024-01-15",
      "data_entrega_edital": "2024-01-15",
      "data_entrega_proposta": "2024-01-15",
      "data_publicacao": "2024-01-15",
      "dt_alteracao": "2024-01-15T10:30:00",
      "pertence14133": true
    }
  ],
  "totalRegistros": 0,
  "totalPaginas": 0,
  "paginasRestantes": 0
}
```

### `GET /modulo-legado/1.1_consultarLicitacao_Id`

#### Parameters

| Name | In | Type | Required | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `id_compra` | query | `string` | yes |  |  |
| `dt_alteracao` | query | `string` | no |  | YYYY-MM-DD |

#### Response

- **Status:** `200`
- **Content type:** `*/*`

```json
{
  "resultado": [
    {
      "id_compra": "string",
      "identificador": "string",
      "numero_processo": "string",
      "uasg": 0,
      "modalidade": 0,
      "nome_modalidade": "string",
      "numero_aviso": 0,
      "situacao_aviso": "string",
      "tipo_pregao": "string",
      "tipo_recurso": "string",
      "nome_responsavel": "string",
      "funcao_responsavel": "string",
      "numero_itens": 0,
      "valor_estimado_total": 0,
      "valor_homologado_total": 0,
      "informacoes_gerais": "string",
      "objeto": "string",
      "endereco_entrega_edital": "string",
      "codigo_municipio_uasg": 0,
      "data_abertura_proposta": "2024-01-15",
      "data_entrega_edital": "2024-01-15",
      "data_entrega_proposta": "2024-01-15",
      "data_publicacao": "2024-01-15",
      "dt_alteracao": "2024-01-15T10:30:00",
      "pertence14133": true
    }
  ],
  "totalRegistros": 0,
  "totalPaginas": 0,
  "paginasRestantes": 0
}
```

### `GET /modulo-legado/2_consultarItemLicitacao`

#### Parameters

| Name | In | Type | Required | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `pagina` | query | `integer(int32)` | no | 1 |  |
| `tamanhoPagina` | query | `integer(int32)` | no | 10 |  |
| `uasg` | query | `integer(int32)` | no |  |  |
| `numero_aviso` | query | `integer(int32)` | no |  |  |
| `modalidade` | query | `integer(int32)` | yes |  |  |
| `decreto_7174` | query | `boolean` | no |  |  |
| `codigo_item_material` | query | `integer(int32)` | no |  |  |
| `codigo_item_servico` | query | `integer(int32)` | no |  |  |
| `cnpj_fornecedor` | query | `string` | no |  |  |
| `cpfVencedor` | query | `string` | no |  |  |

#### Response

- **Status:** `200`
- **Content type:** `*/*`

```json
{
  "resultado": [
    {
      "numero_licitacao": "string",
      "uasg": 0,
      "nome_uasg": "string",
      "modalidade": 0,
      "nome_modalidade": "string",
      "numero_aviso": 0,
      "numero_item_licitacao": 0,
      "codigo_item_material": 0,
      "nome_material": "string",
      "codigo_item_servico": 0,
      "nome_servico": "string",
      "cnpj_fornecedor": "string",
      "nome_fornecedor": "string",
      "quantidade": 0,
      "unidade": "string",
      "descricao_item": "string",
      "beneficio": "string",
      "valor_estimado": 0,
      "decreto_7174": "string",
      "criterio_julgamento": "string",
      "cpf_vencedor": "string",
      "nome_vencedor_pf": "string",
      "sustentavel": 0,
      "dt_alteracao": "2024-01-15T10:30:00",
      "id_compra": "string",
      "id_compra_item": "string"
    }
  ],
  "totalRegistros": 0,
  "totalPaginas": 0,
  "paginasRestantes": 0
}
```

### `GET /modulo-legado/2.1_consultarItemLicitacao_Id`

#### Parameters

| Name | In | Type | Required | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `id_compra` | query | `string` | yes |  |  |
| `id_compra_item` | query | `string` | no |  |  |
| `dt_alteracao` | query | `string` | no |  | YYYY-MM-DD |

#### Response

- **Status:** `200`
- **Content type:** `*/*`

```json
{
  "resultado": [
    {
      "numero_licitacao": "string",
      "uasg": 0,
      "nome_uasg": "string",
      "modalidade": 0,
      "nome_modalidade": "string",
      "numero_aviso": 0,
      "numero_item_licitacao": 0,
      "codigo_item_material": 0,
      "nome_material": "string",
      "codigo_item_servico": 0,
      "nome_servico": "string",
      "cnpj_fornecedor": "string",
      "nome_fornecedor": "string",
      "quantidade": 0,
      "unidade": "string",
      "descricao_item": "string",
      "beneficio": "string",
      "valor_estimado": 0,
      "decreto_7174": "string",
      "criterio_julgamento": "string",
      "cpf_vencedor": "string",
      "nome_vencedor_pf": "string",
      "sustentavel": 0,
      "dt_alteracao": "2024-01-15T10:30:00",
      "id_compra": "string",
      "id_compra_item": "string"
    }
  ],
  "totalRegistros": 0,
  "totalPaginas": 0,
  "paginasRestantes": 0
}
```

### `GET /modulo-legado/3_consultarPregoes`

#### Parameters

| Name | In | Type | Required | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `pagina` | query | `integer(int32)` | no | 1 |  |
| `tamanhoPagina` | query | `integer(int32)` | no | 10 |  |
| `co_uasg` | query | `integer(int32)` | no |  |  |
| `co_orgao` | query | `integer(int32)` | no |  |  |
| `numero` | query | `integer(int32)` | no |  |  |
| `ds_tipo_pregao_compra` | query | `string` | no |  |  |
| `dt_data_edital_inicial` | query | `string` | yes |  | YYYY-MM-DD |
| `dt_data_edital_final` | query | `string` | yes |  | YYYY-MM-DD |
| `pertence14133` | query | `boolean` | no |  |  |

#### Response

- **Status:** `200`
- **Content type:** `*/*`

```json
{
  "resultado": [
    {
      "id_compra": "string",
      "co_processo": "string",
      "co_portaria": "string",
      "co_uasg": 0,
      "no_ausg": "string",
      "co_orgao": 0,
      "no_orgao": "string",
      "numero": 0,
      "ds_situacao_pregao": "string",
      "ds_tipo_pregao": "string",
      "ds_tipo_pregao_compra": "string",
      "tx_objeto": "string",
      "valor_estimado_total": "string",
      "valor_homologado_total": "string",
      "dt_portaria": "2024-01-15T10:30:00",
      "dt_data_edital": "2024-01-15T10:30:00",
      "dt_inicio_proposta": "2024-01-15T10:30:00",
      "dt_fim_proposta": "2024-01-15T10:30:00",
      "dt_alteracao": "2024-01-15T10:30:00",
      "dt_encerramento": "2024-01-15T10:30:00",
      "dt_resultado": "2024-01-15T10:30:00",
      "pertence14133": true
    }
  ],
  "totalRegistros": 0,
  "totalPaginas": 0,
  "paginasRestantes": 0
}
```

### `GET /modulo-legado/3.1_consultarPregoes_Id`

#### Parameters

| Name | In | Type | Required | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `id_compra` | query | `string` | yes |  |  |
| `dt_alteracao` | query | `string` | no |  | YYYY-MM-DD |

#### Response

- **Status:** `200`
- **Content type:** `*/*`

```json
{
  "resultado": [
    {
      "id_compra": "string",
      "co_processo": "string",
      "co_portaria": "string",
      "co_uasg": 0,
      "no_ausg": "string",
      "co_orgao": 0,
      "no_orgao": "string",
      "numero": 0,
      "ds_situacao_pregao": "string",
      "ds_tipo_pregao": "string",
      "ds_tipo_pregao_compra": "string",
      "tx_objeto": "string",
      "valor_estimado_total": "string",
      "valor_homologado_total": "string",
      "dt_portaria": "2024-01-15T10:30:00",
      "dt_data_edital": "2024-01-15T10:30:00",
      "dt_inicio_proposta": "2024-01-15T10:30:00",
      "dt_fim_proposta": "2024-01-15T10:30:00",
      "dt_alteracao": "2024-01-15T10:30:00",
      "dt_encerramento": "2024-01-15T10:30:00",
      "dt_resultado": "2024-01-15T10:30:00",
      "pertence14133": true
    }
  ],
  "totalRegistros": 0,
  "totalPaginas": 0,
  "paginasRestantes": 0
}
```

### `GET /modulo-legado/4_consultarItensPregoes`

#### Parameters

| Name | In | Type | Required | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `pagina` | query | `integer(int32)` | no | 1 |  |
| `tamanhoPagina` | query | `integer(int32)` | no | 10 |  |
| `co_uasg` | query | `integer(int32)` | no |  |  |
| `decreto_7174` | query | `string` | no |  |  |
| `fornecedor_vencedor` | query | `string` | no |  |  |
| `dt_hom_inicial` | query | `string` | yes |  | YYYY-MM-DD |
| `dt_hom_final` | query | `string` | yes |  | YYYY-MM-DD |

#### Response

- **Status:** `200`
- **Content type:** `*/*`

```json
{
  "resultado": [
    {
      "id_compra": "string",
      "id_compra_item": "string",
      "decreto_7174": "string",
      "situacao_item": "string",
      "descricao_item": "string",
      "descricao_detalhada_item": "string",
      "margem_preferencial": "string",
      "tratamento_diferenciado": "string",
      "quantidade_item": "string",
      "unidade_fornecimento": "string",
      "valor_estimado_item": "string",
      "menor_lance": "string",
      "valor_negociado": "string",
      "valor_homologado_item": "string",
      "fornecedor_vencedor": "string",
      "no_adjudic": "string",
      "no_hom": "string",
      "dt_encerramento": "2026-07-06T19:53:33.156Z",
      "dt_adjudic": "2026-07-06T19:53:33.156Z",
      "dt_hom": "2026-07-06T19:53:33.156Z",
      "dt_alteracao": "2026-07-06T19:53:33.156Z"
    }
  ],
  "totalRegistros": 0,
  "totalPaginas": 0,
  "paginasRestantes": 0
}
```

### `GET /modulo-legado/4.1_consultarItensPregoes_Id`

#### Parameters

| Name | In | Type | Required | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `id_compra` | query | `string` | yes |  |  |
| `id_compra_item` | query | `string` | no |  |  |
| `dt_alteracao` | query | `string` | no |  | YYYY-MM-DD |

#### Response

- **Status:** `200`
- **Content type:** `*/*`

```json
{
  "resultado": [
    {
      "id_compra": "string",
      "id_compra_item": "string",
      "decreto_7174": "string",
      "situacao_item": "string",
      "descricao_item": "string",
      "descricao_detalhada_item": "string",
      "margem_preferencial": "string",
      "tratamento_diferenciado": "string",
      "quantidade_item": "string",
      "unidade_fornecimento": "string",
      "valor_estimado_item": "string",
      "menor_lance": "string",
      "valor_negociado": "string",
      "valor_homologado_item": "string",
      "fornecedor_vencedor": "string",
      "no_adjudic": "string",
      "no_hom": "string",
      "dt_encerramento": "2026-07-06T19:53:33.156Z",
      "dt_adjudic": "2026-07-06T19:53:33.156Z",
      "dt_hom": "2026-07-06T19:53:33.156Z",
      "dt_alteracao": "2026-07-06T19:53:33.156Z"
    }
  ],
  "totalRegistros": 0,
  "totalPaginas": 0,
  "paginasRestantes": 0
}
```

### `GET /modulo-legado/5_consultarComprasSemLicitacao`

#### Parameters

| Name | In | Type | Required | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `pagina` | query | `integer(int32)` | no | 1 |  |
| `tamanhoPagina` | query | `integer(int32)` | no | 10 |  |
| `dt_ano_aviso` | query | `integer(int32)` | yes |  |  |
| `nu_aviso_licitacao` | query | `integer(int64)` | no |  |  |
| `co_modalidade_licitacao` | query | `integer(int32)` | no |  |  |
| `co_orgao` | query | `string` | no |  |  |
| `co_orgao_superior` | query | `string` | no |  |  |
| `co_uasg` | query | `integer(int64)` | no |  |  |
| `dtDeclaracaoDispensaInicial` | query | `string` | no |  | YYYY-MM-DD |
| `dtDeclaracaoDispensaFinal` | query | `string` | no |  | YYYY-MM-DD |
| `dtRatificacao` | query | `string` | no |  | YYYY-MM-DD |
| `dtPublicacao` | query | `string` | no |  | YYYY-MM-DD |
| `pertence14133` | query | `boolean` | no |  |  |

#### Response

- **Status:** `200`
- **Content type:** `*/*`

```json
{
  "resultado": [
    {
      "id_compra": "string",
      "co_orgao": "string",
      "co_orgao_superior": "string",
      "co_uasg": 0,
      "no_ausg": "string",
      "co_modalidade_licitacao": 0,
      "ds_lei": "string",
      "nu_processo": "string",
      "qt_total_item": 0,
      "vr_estimado": 0,
      "nu_aviso_licitacao": 0,
      "ds_objeto_licitacao": "string",
      "ds_fundamento_legal": "string",
      "ds_justificativa": "string",
      "no_responsavel_decl_disp": "string",
      "no_cargo_resp_decl_disp": "string",
      "no_responsavel_ratificacao": "string",
      "no_cargo_resp_ratificacao": "string",
      "dt_declaracao_dispensa": "2024-01-15",
      "dt_ratificacao": "2024-01-15",
      "dt_publicacao": "2024-01-15",
      "dt_ano_aviso": 0,
      "dt_alteracao": "2024-01-15",
      "pertence14133": true
    }
  ],
  "totalRegistros": 0,
  "totalPaginas": 0,
  "paginasRestantes": 0
}
```

### `GET /modulo-legado/5.1_consultarCompraSemLicitacao_Id`

#### Parameters

| Name | In | Type | Required | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `idCompra` | query | `string` | yes |  |  |

#### Response

- **Status:** `200`
- **Content type:** `*/*`

```json
{
  "resultado": [
    {
      "id_compra": "string",
      "co_orgao": "string",
      "co_orgao_superior": "string",
      "co_uasg": 0,
      "no_ausg": "string",
      "co_modalidade_licitacao": 0,
      "ds_lei": "string",
      "nu_processo": "string",
      "qt_total_item": 0,
      "vr_estimado": 0,
      "nu_aviso_licitacao": 0,
      "ds_objeto_licitacao": "string",
      "ds_fundamento_legal": "string",
      "ds_justificativa": "string",
      "no_responsavel_decl_disp": "string",
      "no_cargo_resp_decl_disp": "string",
      "no_responsavel_ratificacao": "string",
      "no_cargo_resp_ratificacao": "string",
      "dt_declaracao_dispensa": "2024-01-15",
      "dt_ratificacao": "2024-01-15",
      "dt_publicacao": "2024-01-15",
      "dt_ano_aviso": 0,
      "dt_alteracao": "2024-01-15",
      "pertence14133": true
    }
  ],
  "totalRegistros": 0,
  "totalPaginas": 0,
  "paginasRestantes": 0
}
```

### `GET /modulo-legado/6_consultarCompraItensSemLicitacao`

#### Parameters

| Name | In | Type | Required | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `pagina` | query | `integer(int32)` | no | 1 |  |
| `tamanhoPagina` | query | `integer(int32)` | no | 10 |  |
| `co_uasg` | query | `integer` | no |  |  |
| `co_orgao` | query | `string` | no |  |  |
| `dt_ano_aviso_licitacao` | query | `integer(int32)` | yes |  |  |
| `co_modalidade_licitacao` | query | `integer(int32)` | no |  |  |
| `co_conjunto_materiais` | query | `integer(int32)` | no |  |  |
| `co_servico` | query | `integer(int32)` | no |  |  |
| `nu_cpf_cnpj_fornecedor` | query | `string` | no |  |  |

#### Response

- **Status:** `200`
- **Content type:** `*/*`

```json
{
  "resultado": [
    {
      "co_conjunto_materiais": 0,
      "co_servico": 0,
      "ds_detalhada": "string",
      "in_tipo_fornecedor_vencedor": "string",
      "no_fornecedor_vencedor": "string",
      "no_conjunto_materiais": "string",
      "no_marca_material": "string",
      "no_servico": "string",
      "no_unidade_medida": "string",
      "nu_cnpj_vencedor": "string",
      "nu_cpf_vencedor": "string",
      "qt_material_alt": 0,
      "vr_estimado": 0,
      "in_material_servico": "string",
      "dt_publicacao": "YYYY-MM-DD",
      "id_compra": "string",
      "id_compra_item": "string",
      "co_uasg": 0,
      "co_modalidade_licitacao": 0,
      "no_modalidade_licitacao": "string",
      "nu_aviso_licitacao": 0,
      "dt_ano_aviso_licitacao": 0,
      "nu_inciso": "string",
      "nu_processo": "string",
      "qt_total_item": 0,
      "ds_objeto_licitacao": "string",
      "ds_fundamento_legal": "string",
      "ds_justificativa": "string",
      "nu_cpf_resp_decl_disp": "string",
      "nu_cpf_resp_ratificacao": "string",
      "nu_cpf_resp_publicacao": "string",
      "no_responsavel_decl_disp": "string",
      "no_cargo_resp_decl_disp": "string",
      "no_responsavel_ratificacao": "string",
      "no_cargo_resp_ratificacao": "string",
      "nu_item_material": 0,
      "vr_estimado_item": 0,
      "ds_fabricante": "string",
      "dt_alteracao": "2024-01-15T10:30:00",
      "co_orgao": "string"
    }
  ],
  "totalRegistros": 0,
  "totalPaginas": 0,
  "paginasRestantes": 0
}
```

### `GET /modulo-legado/6.1_consultarItensComprasSemLicitacao_Id`

#### Parameters

| Name | In | Type | Required | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `id_compra` | query | `string` | yes |  |  |
| `id_compra_item` | query | `string` | no |  |  |
| `dt_alteracao` | query | `string` | no |  | YYYY-MM-DD |

#### Response

- **Status:** `200`
- **Content type:** `*/*`

```json
{
  "resultado": [
    {
      "co_conjunto_materiais": 0,
      "co_servico": 0,
      "ds_detalhada": "string",
      "in_tipo_fornecedor_vencedor": "string",
      "no_fornecedor_vencedor": "string",
      "no_conjunto_materiais": "string",
      "no_marca_material": "string",
      "no_servico": "string",
      "no_unidade_medida": "string",
      "nu_cnpj_vencedor": "string",
      "nu_cpf_vencedor": "string",
      "qt_material_alt": 0,
      "vr_estimado": 0,
      "in_material_servico": "string",
      "dt_publicacao": "YYYY-MM-DD",
      "id_compra": "string",
      "id_compra_item": "string",
      "co_uasg": 0,
      "co_modalidade_licitacao": 0,
      "no_modalidade_licitacao": "string",
      "nu_aviso_licitacao": 0,
      "dt_ano_aviso_licitacao": 0,
      "nu_inciso": "string",
      "nu_processo": "string",
      "qt_total_item": 0,
      "ds_objeto_licitacao": "string",
      "ds_fundamento_legal": "string",
      "ds_justificativa": "string",
      "nu_cpf_resp_decl_disp": "string",
      "nu_cpf_resp_ratificacao": "string",
      "nu_cpf_resp_publicacao": "string",
      "no_responsavel_decl_disp": "string",
      "no_cargo_resp_decl_disp": "string",
      "no_responsavel_ratificacao": "string",
      "no_cargo_resp_ratificacao": "string",
      "nu_item_material": 0,
      "vr_estimado_item": 0,
      "ds_fabricante": "string",
      "dt_alteracao": "2024-01-15T10:30:00",
      "co_orgao": "string"
    }
  ],
  "totalRegistros": 0,
  "totalPaginas": 0,
  "paginasRestantes": 0
}
```

### `GET /modulo-legado/7_consultarRdc`

#### Parameters

| Name | In | Type | Required | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `pagina` | query | `integer(int32)` | no | 1 |  |
| `tamanhoPagina` | query | `integer(int32)` | no | 10 |  |
| `data_publicacao_min` | query | `string` | yes |  | YYYY-MM-DD |
| `data_publicacao_max` | query | `string` | yes |  | YYYY-MM-DD |
| `endereco_entrega_edital` | query | `string` | no |  |  |
| `forma_de_realizacao` | query | `string` | no |  |  |
| `funcao_responsavel` | query | `string` | no |  |  |
| `modalidade` | query | `integer(int32)` | no |  |  |
| `nome_responsavel` | query | `string` | no |  |  |
| `numero_aviso` | query | `integer(int32)` | no |  |  |
| `objeto` | query | `string` | no |  |  |
| `orgao` | query | `integer(int32)` | no |  |  |
| `situacao_aviso` | query | `string` | no |  |  |
| `uasg` | query | `integer(int32)` | no |  |  |
| `uf_uasg` | query | `string` | no |  |  |
| `valor_estimado_total_max` | query | `number` | no |  |  |
| `valor_estimado_total_min` | query | `number` | no |  |  |
| `valor_homologado_total_max` | query | `number` | no |  |  |
| `valor_homologado_total_min` | query | `number` | no |  |  |

#### Response

- **Status:** `200`
- **Content type:** `*/*`

```json
{
  "resultado": [
    {
      "data_abertura_proposta": "2024-01-15",
      "data_entrega_edital": "2024-01-15",
      "data_entrega_proposta": "2024-01-15",
      "data_publicacao": "2024-01-15",
      "endereco_entrega_edital": "string",
      "forma_de_realizacao_licitacao": "string",
      "funcao_responsavel": "string",
      "identificador": "string",
      "informacoes_gerais": "string",
      "modalidade": 0,
      "nome_responsavel": 0,
      "numero_aviso": 0,
      "numero_itens": 0,
      "numero_processo": "string",
      "objeto": "string",
      "situacao_aviso": "string",
      "tipo_recurso": "string",
      "uasg": 0,
      "orgao_uasg": 0,
      "uf_uasg": "string"
    }
  ],
  "totalRegistros": 0,
  "totalPaginas": 0,
  "paginasRestantes": 0
}
```

## 07 - CONTRATAÇÕES

Consulta contratações realizadas sob a Lei nº 14.133/2021.

### `GET /modulo-contratacoes/1_consultarContratacoes_PNCP_14133`

#### Parameters

| Name | In | Type | Required | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `pagina` | query | `integer(int32)` | no | 1 |  |
| `tamanhoPagina` | query | `integer(int32)` | no | 10 |  |
| `unidadeOrgaoCodigoUnidade` | query | `string` | no |  |  |
| `codigoOrgao` | query | `integer(int32)` | no |  |  |
| `orgaoEntidadeCnpj` | query | `string` | no |  |  |
| `dataPublicacaoPncpInicial` | query | `string` | yes |  | YYYY-MM-DD |
| `dataPublicacaoPncpFinal` | query | `string` | yes |  | YYYY-MM-DD |
| `codigoModalidade` | query | `integer(int32)` | yes |  |  |
| `unidadeOrgaoCodigoIbge` | query | `integer` | no |  |  |
| `unidadeOrgaoUfSigla` | query | `string` | no |  |  |
| `dataAualizacaoPncp` | query | `string` | no |  | YYYY-MM-DD |
| `amparoLegalCodigoPncp` | query | `integer(int32)` | no |  |  |
| `contratacaoExcluida` | query | `boolean` | no |  |  |

#### Response

- **Status:** `200`
- **Content type:** `*/*`

```json
{
  "resultado": [
    {
      "idCompra": "string",
      "numeroControlePNCP": "string",
      "anoCompraPncp": 0,
      "sequencialCompraPncp": 0,
      "orgaoEntidadeCnpj": "string",
      "orgaoSubrogadoCnpj": "string",
      "codigoOrgao": 0,
      "orgaoEntidadeRazaoSocial": "string",
      "orgaoSubrogadoRazaoSocial": "string",
      "orgaoEntidadeEsferaId": "string",
      "orgaoSubrogadoEsferaId": "string",
      "orgaoEntidadePoderId": "string",
      "orgaoSubrogadoPoderId": "string",
      "unidadeOrgaoCodigoUnidade": "string",
      "unidadeSubrogadaCodigoUnidade": "string",
      "unidadeOrgaoNomeUnidade": "string",
      "unidadeSubrogadaNomeUnidade": "string",
      "unidadeOrgaoUfSigla": "string",
      "unidadeSubrogadaUfSigla": "string",
      "unidadeOrgaoMunicipioNome": "string",
      "unidadeSubrogadaMunicipioNome": "string",
      "unidadeOrgaoCodigoIbge": 0,
      "unidadeSubrogadaCodigoIbge": 0,
      "numeroCompra": "string",
      "modalidadeIdPncp": 0,
      "codigoModalidade": 0,
      "modalidadeNome": "string",
      "srp": 0,
      "modoDisputaIdPncp": 0,
      "codigoModoDisputa": 0,
      "amparoLegalCodigoPncp": 0,
      "amparoLegalNome": "string",
      "amparoLegalDescricao": "string",
      "informacaoComplementar": "string",
      "processo": "string",
      "objetoCompra": "string",
      "existeResultado": 0,
      "orcamentoSigilosoCodigo": 0,
      "orcamentoSigilosoDescricao": "string",
      "situacaoCompraIdPncp": 0,
      "situacaoCompraNomePncp": "string",
      "tipoInstrumentoConvocatorioCodigoPncp": 0,
      "tipoInstrumentoConvocatorioNome": "string",
      "modoDisputaNomePncp": "string",
      "valorTotalEstimado": 0,
      "valorTotalHomologado": 0,
      "dataInclusaoPncp": "2024-01-15 10:30:00",
      "dataAtualizacaoPncp": "2024-01-15 10:30:00",
      "dataPublicacaoPncp": "2024-01-15 10:30:00",
      "dataAberturaPropostaPncp": "2024-01-15 10:30:00",
      "dataEncerramentoPropostaPncp": "2024-01-15 10:30:00",
      "contratacaoExcluida": 0
    }
  ],
  "totalRegistros": 0,
  "totalPaginas": 0,
  "paginasRestantes": 0
}
```

### `GET /modulo-contratacoes/1.1_consultarContratacoes_PNCP_14133_Id`

#### Parameters

| Name | In | Type | Required | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `tipo` | query | `string` | yes |  | Values: `idCompra`, `numeroControlePNCPCompra` |
| `codigo` | query | `string` | yes |  |  |
| `dataAtualizacaoPncp` | query | `string` | no |  | YYYY-MM-DD |

#### Response

- **Status:** `200`
- **Content type:** `*/*`

```json
{
  "resultado": [
    {
      "idCompra": "string",
      "numeroControlePNCP": "string",
      "anoCompraPncp": 0,
      "sequencialCompraPncp": 0,
      "orgaoEntidadeCnpj": "string",
      "orgaoSubrogadoCnpj": "string",
      "codigoOrgao": 0,
      "orgaoEntidadeRazaoSocial": "string",
      "orgaoSubrogadoRazaoSocial": "string",
      "orgaoEntidadeEsferaId": "string",
      "orgaoSubrogadoEsferaId": "string",
      "orgaoEntidadePoderId": "string",
      "orgaoSubrogadoPoderId": "string",
      "unidadeOrgaoCodigoUnidade": "string",
      "unidadeSubrogadaCodigoUnidade": "string",
      "unidadeOrgaoNomeUnidade": "string",
      "unidadeSubrogadaNomeUnidade": "string",
      "unidadeOrgaoUfSigla": "string",
      "unidadeSubrogadaUfSigla": "string",
      "unidadeOrgaoMunicipioNome": "string",
      "unidadeSubrogadaMunicipioNome": "string",
      "unidadeOrgaoCodigoIbge": 0,
      "unidadeSubrogadaCodigoIbge": 0,
      "numeroCompra": "string",
      "modalidadeIdPncp": 0,
      "codigoModalidade": 0,
      "modalidadeNome": "string",
      "srp": 0,
      "modoDisputaIdPncp": 0,
      "codigoModoDisputa": 0,
      "amparoLegalCodigoPncp": 0,
      "amparoLegalNome": "string",
      "amparoLegalDescricao": "string",
      "informacaoComplementar": "string",
      "processo": "string",
      "objetoCompra": "string",
      "existeResultado": 0,
      "orcamentoSigilosoCodigo": 0,
      "orcamentoSigilosoDescricao": "string",
      "situacaoCompraIdPncp": 0,
      "situacaoCompraNomePncp": "string",
      "tipoInstrumentoConvocatorioCodigoPncp": 0,
      "tipoInstrumentoConvocatorioNome": "string",
      "modoDisputaNomePncp": "string",
      "valorTotalEstimado": 0,
      "valorTotalHomologado": 0,
      "dataInclusaoPncp": "2024-01-15 10:30:00",
      "dataAtualizacaoPncp": "2024-01-15 10:30:00",
      "dataPublicacaoPncp": "2024-01-15 10:30:00",
      "dataAberturaPropostaPncp": "2024-01-15 10:30:00",
      "dataEncerramentoPropostaPncp": "2024-01-15 10:30:00",
      "contratacaoExcluida": 0
    }
  ],
  "totalRegistros": 0,
  "totalPaginas": 0,
  "paginasRestantes": 0
}
```

### `GET /modulo-contratacoes/2_consultarItensContratacoes_PNCP_14133`

#### Parameters

| Name | In | Type | Required | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `pagina` | query | `integer(int32)` | no | 1 |  |
| `tamanhoPagina` | query | `integer(int32)` | no | 10 |  |
| `unidadeOrgaoCodigoUnidade` | query | `string` | no |  |  |
| `orgaoEntidadeCnpj` | query | `string` | no |  |  |
| `situacaoCompraItem` | query | `string` | no |  |  |
| `materialOuServico` | query | `string` | no |  |  |
| `codigoClasse` | query | `integer(int32)` | no |  |  |
| `codigoGrupo` | query | `integer(int32)` | no |  |  |
| `codItemCatalogo` | query | `integer(int32)` | no |  |  |
| `temResultado` | query | `boolean` | no |  |  |
| `codFornecedor` | query | `string` | no |  |  |
| `dataInclusaoPncpInicial` | query | `string` | yes |  | YYYY-MM-DD |
| `dataInclusaoPncpFinal` | query | `string` | yes |  | YYYY-MM-DD |
| `dataAtualizacaoPncp` | query | `string` | no |  |  |
| `bps` | query | `boolean` | no | false |  |
| `margemPreferenciaNormal` | query | `boolean` | no |  |  |
| `codigoNCM` | query | `string` | no |  |  |
| `codigoPdm` | query | `string` | no |  |  |

#### Response

- **Status:** `200`
- **Content type:** `*/*`

```json
{
  "resultado": [
    {
      "idCompra": "string",
      "idCompraItem": "string",
      "idContratacaoPNCP": "string",
      "unidadeOrgaoCodigoUnidade": "string",
      "orgaoEntidadeCnpj": "string",
      "numeroItemPncp": 0,
      "numeroItemCompra": 0,
      "numeroGrupo": 0,
      "descricaoResumida": "string",
      "materialOuServico": "string",
      "materialOuServicoNome": "string",
      "codigoClasse": 0,
      "codigoGrupo": 0,
      "codItemCatalogo": 0,
      "descricaodetalhada": "string",
      "unidadeMedida": "string",
      "orcamentoSigiloso": true,
      "itemCategoriaIdPncp": 0,
      "itemCategoriaNome": "string",
      "criterioJulgamentoIdPncp": 0,
      "criterioJulgamentoNome": "string",
      "situacaoCompraItem": "string",
      "situacaoCompraItemNome": "string",
      "tipoBeneficio": "string",
      "tipoBeneficioNome": "string",
      "incentivoProdutivoBasico": true,
      "quantidade": 0,
      "valorUnitarioEstimado": 0,
      "valorTotal": 0,
      "temResultado": true,
      "codFornecedor": "string",
      "nomeFornecedor": "string",
      "quantidadeResultado": 0,
      "valorUnitarioResultado": 0,
      "valorTotalResultado": 0,
      "dataInclusaoPncp": "2024-01-15 10:30:00",
      "dataAtualizacaoPncp": "2024-01-15 10:30:00",
      "dataResultado": "string",
      "margemPreferenciaNormal": true,
      "percentualMargemPreferenciaNormal": 0,
      "margemPreferenciaAdicional": true,
      "percentualMargemPreferenciaAdicional": 0,
      "codigoNCM": "string",
      "descricaoNCM": "string",
      "numeroControlePNCPCompra": "string",
      "codigoPdm": "string",
      "nomePdm": "string"
    }
  ],
  "totalRegistros": 0,
  "totalPaginas": 0,
  "paginasRestantes": 0
}
```

### `GET /modulo-contratacoes/2.1_consultarItensContratacoes_PNCP_14133_Id`

#### Parameters

| Name | In | Type | Required | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `tipo` | query | `string` | yes |  | Values: `idCompra`, `numeroControlePNCPCompra` |
| `codigo` | query | `string` | yes |  |  |
| `idCompraItem` | query | `string` | no |  |  |
| `dataAtualizacaoPncp` | query | `string` | no |  | YYYY-MM-DD |

#### Response

- **Status:** `200`
- **Content type:** `*/*`

```json
{
  "resultado": [
    {
      "idCompra": "string",
      "idCompraItem": "string",
      "idContratacaoPNCP": "string",
      "unidadeOrgaoCodigoUnidade": "string",
      "orgaoEntidadeCnpj": "string",
      "numeroItemPncp": 0,
      "numeroItemCompra": 0,
      "numeroGrupo": 0,
      "descricaoResumida": "string",
      "materialOuServico": "string",
      "materialOuServicoNome": "string",
      "codigoClasse": 0,
      "codigoGrupo": 0,
      "codItemCatalogo": 0,
      "descricaodetalhada": "string",
      "unidadeMedida": "string",
      "orcamentoSigiloso": true,
      "itemCategoriaIdPncp": 0,
      "itemCategoriaNome": "string",
      "criterioJulgamentoIdPncp": 0,
      "criterioJulgamentoNome": "string",
      "situacaoCompraItem": "string",
      "situacaoCompraItemNome": "string",
      "tipoBeneficio": "string",
      "tipoBeneficioNome": "string",
      "incentivoProdutivoBasico": true,
      "quantidade": 0,
      "valorUnitarioEstimado": 0,
      "valorTotal": 0,
      "temResultado": true,
      "codFornecedor": "string",
      "nomeFornecedor": "string",
      "quantidadeResultado": 0,
      "valorUnitarioResultado": 0,
      "valorTotalResultado": 0,
      "dataInclusaoPncp": "2024-01-15 10:30:00",
      "dataAtualizacaoPncp": "2024-01-15 10:30:00",
      "dataResultado": "string",
      "margemPreferenciaNormal": true,
      "percentualMargemPreferenciaNormal": 0,
      "margemPreferenciaAdicional": true,
      "percentualMargemPreferenciaAdicional": 0,
      "codigoNCM": "string",
      "descricaoNCM": "string",
      "numeroControlePNCPCompra": "string",
      "codigoPdm": "string",
      "nomePdm": "string"
    }
  ],
  "totalRegistros": 0,
  "totalPaginas": 0,
  "paginasRestantes": 0
}
```

### `GET /modulo-contratacoes/3_consultarResultadoItensContratacoes_PNCP_14133`

#### Parameters

| Name | In | Type | Required | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `pagina` | query | `integer(int32)` | no | 1 |  |
| `tamanhoPagina` | query | `integer(int32)` | no | 10 |  |
| `unidadeOrgaoCodigoUnidade` | query | `string` | no |  |  |
| `orgaoEntidadeCnpj` | query | `string` | no |  |  |
| `niFornecedor` | query | `string` | no |  |  |
| `codigoPais` | query | `string` | no |  |  |
| `porteFornecedorId` | query | `integer(int32)` | no |  |  |
| `naturezaJuridicaId` | query | `string` | no |  |  |
| `situacaoCompraItemResultadoId` | query | `integer` | no |  |  |
| `valorUnitarioHomologadoInicial` | query | `number` | no |  |  |
| `valorUnitarioHomologadoFinal` | query | `number` | no |  |  |
| `valorTotalHomologadoInicial` | query | `number` | no |  |  |
| `valorTotalHomologadoFinal` | query | `number` | no |  |  |
| `dataResultadoPncpInicial` | query | `string` | yes |  | YYYY-MM-DD |
| `dataResultadoPncpFinal` | query | `string` | yes |  | YYYY-MM-DD |
| `aplicacaoMargemPreferencia` | query | `boolean` | no |  |  |
| `aplicacaoBeneficioMeepp` | query | `boolean` | no |  |  |
| `aplicacaoCriterioDesempate` | query | `boolean` | no |  |  |

#### Response

- **Status:** `200`
- **Content type:** `*/*`

```json
{
  "resultado": [
    {
      "idCompraItem": "string",
      "idCompra": "string",
      "idContratacaoPNCP": "string",
      "unidadeOrgaoCodigoUnidade": "string",
      "unidadeOrgaoUfSigla": "string",
      "numeroItemPncp": 0,
      "sequencialResultado": 0,
      "niFornecedor": "string",
      "tipoPessoa": "string",
      "nomeRazaoSocialFornecedor": "string",
      "codigoPais": "string",
      "indicadorSubcontratacao": true,
      "ordemClassificacaoSrp": 0,
      "quantidadeHomologada": 0,
      "valorUnitarioHomologado": 0,
      "valorTotalHomologado": 0,
      "percentualDesconto": 0,
      "situacaoCompraItemResultadoId": 0,
      "situacaoCompraItemResultadoNome": "string",
      "motivoCancelamento": "string",
      "porteFornecedorId": 0,
      "porteFornecedorNome": "string",
      "naturezaJuridicaNome": "string",
      "naturezaJuridicaId": "string",
      "dataInclusaoPncp": "2024-01-15 10:30:00",
      "dataAtualizacaoPncp": "2024-01-15 10:30:00",
      "dataCancelamentoPncp": "2024-01-15 10:30:00",
      "dataResultadoPncp": "2024-01-15 10:30:00",
      "numeroControlePNCPCompra": "string",
      "orgaoEntidadeCnpj": "string",
      "aplicacaoMargemPreferencia": true,
      "amparoLegalMargemPreferenciaId": 0,
      "amparoLegalMargemPreferenciaNome": "string",
      "aplicacaoBeneficioMeepp": true,
      "aplicacaoCriterioDesempate": true,
      "amparoLegalCriterioDesempateId": 0,
      "amparoLegalCriterioDesempateNome": "string",
      "moedaEstrangeiraId": 0,
      "dataCotacaoMoedaEstrangeira": "2024-01-15 10:30:00",
      "valorNominalMoedaEstrangeira": 0,
      "paisOrigemProdutoServicoId": "string",
      "timezoneCotacaoMoedaEstrangeira": "string"
    }
  ],
  "totalRegistros": 0,
  "totalPaginas": 0,
  "paginasRestantes": 0
}
```

### `GET /modulo-contratacoes/3.1_consultarResultadoItensContratacoes_PNCP_14133_Id`

#### Parameters

| Name | In | Type | Required | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `tipo` | query | `string` | yes |  | Values: `idCompra`, `numeroControlePNCPCompra` |
| `codigo` | query | `string` | yes |  |  |
| `idCompraItem` | query | `string` | no |  |  |
| `dataAtualizacaoPncp` | query | `string` | no |  | YYYY-MM-DD |

#### Response

- **Status:** `200`
- **Content type:** `*/*`

```json
{
  "resultado": [
    {
      "idCompraItem": "string",
      "idCompra": "string",
      "idContratacaoPNCP": "string",
      "unidadeOrgaoCodigoUnidade": "string",
      "unidadeOrgaoUfSigla": "string",
      "numeroItemPncp": 0,
      "sequencialResultado": 0,
      "niFornecedor": "string",
      "tipoPessoa": "string",
      "nomeRazaoSocialFornecedor": "string",
      "codigoPais": "string",
      "indicadorSubcontratacao": true,
      "ordemClassificacaoSrp": 0,
      "quantidadeHomologada": 0,
      "valorUnitarioHomologado": 0,
      "valorTotalHomologado": 0,
      "percentualDesconto": 0,
      "situacaoCompraItemResultadoId": 0,
      "situacaoCompraItemResultadoNome": "string",
      "motivoCancelamento": "string",
      "porteFornecedorId": 0,
      "porteFornecedorNome": "string",
      "naturezaJuridicaNome": "string",
      "naturezaJuridicaId": "string",
      "dataInclusaoPncp": "2024-01-15 10:30:00",
      "dataAtualizacaoPncp": "2024-01-15 10:30:00",
      "dataCancelamentoPncp": "2024-01-15 10:30:00",
      "dataResultadoPncp": "2024-01-15 10:30:00",
      "numeroControlePNCPCompra": "string",
      "orgaoEntidadeCnpj": "string",
      "aplicacaoMargemPreferencia": true,
      "amparoLegalMargemPreferenciaId": 0,
      "amparoLegalMargemPreferenciaNome": "string",
      "aplicacaoBeneficioMeepp": true,
      "aplicacaoCriterioDesempate": true,
      "amparoLegalCriterioDesempateId": 0,
      "amparoLegalCriterioDesempateNome": "string",
      "moedaEstrangeiraId": 0,
      "dataCotacaoMoedaEstrangeira": "2024-01-15 10:30:00",
      "valorNominalMoedaEstrangeira": 0,
      "paisOrigemProdutoServicoId": "string",
      "timezoneCotacaoMoedaEstrangeira": "string"
    }
  ],
  "totalRegistros": 0,
  "totalPaginas": 0,
  "paginasRestantes": 0
}
```

## 08 - ARP

Consulta Atas de Registro de Preços (ARP) e seus respectivos itens.

### `GET /modulo-arp/1_consultarARP`

#### Parameters

| Name | In | Type | Required | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `pagina` | query | `integer(int32)` | no | 1 |  |
| `tamanhoPagina` | query | `integer(int32)` | no | 10 |  |
| `codigoUnidadeGerenciadora` | query | `string` | no |  |  |
| `codigoModalidadeCompra` | query | `string` | no |  |  |
| `numeroAtaRegistroPreco` | query | `string` | no |  |  |
| `dataVigenciaInicialMin` | query | `string` | yes |  | YYYY-MM-DD |
| `dataVigenciaInicialMax` | query | `string` | yes |  | YYYY-MM-DD |
| `dataAssinaturaInicial` | query | `string` | no |  | YYYY-MM-DD |
| `dataAssinaturaFinal` | query | `string` | no |  | YYYY-MM-DD |

#### Response

- **Status:** `200`
- **Content type:** `*/*`

```json
{
  "resultado": [
    {
      "numeroAtaRegistroPreco": "string",
      "codigoUnidadeGerenciadora": "string",
      "nomeUnidadeGerenciadora": "string",
      "codigoOrgao": 0,
      "nomeOrgao": "string",
      "linkAtaPNCP": "string",
      "linkCompraPNCP": "string",
      "numeroCompra": "string",
      "anoCompra": "string",
      "codigoModalidadeCompra": "string",
      "nomeModalidadeCompra": "string",
      "dataAssinatura": "2024-01-15",
      "dataVigenciaInicial": "2024-01-15",
      "dataVigenciaFinal": "2024-01-15",
      "valorTotal": 0,
      "statusAta": "string",
      "objeto": "string",
      "quantidadeItens": 0,
      "dataHoraAtualizacao": "2024-01-15 10:30:00",
      "dataHoraInclusao": "2024-01-15 10:30:00",
      "dataHoraExclusao": "2024-01-15 10:30:00",
      "ataExcluido": true,
      "numeroControlePncpAta": "string",
      "numeroControlePncpCompra": "string",
      "idCompra": "string"
    }
  ],
  "totalRegistros": 0,
  "totalPaginas": 0,
  "paginasRestantes": 0
}
```

### `GET /modulo-arp/1.1_consultarARP_Id`

#### Parameters

| Name | In | Type | Required | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `numeroControlePncpAta` | query | `string` | yes |  |  |
| `dataAtualizacao` | query | `string` | no |  | YYYY-MM-DD |

#### Response

- **Status:** `200`
- **Content type:** `*/*`

```json
{
  "resultado": [
    {
      "numeroAtaRegistroPreco": "string",
      "codigoUnidadeGerenciadora": "string",
      "nomeUnidadeGerenciadora": "string",
      "codigoOrgao": 0,
      "nomeOrgao": "string",
      "linkAtaPNCP": "string",
      "linkCompraPNCP": "string",
      "numeroCompra": "string",
      "anoCompra": "string",
      "codigoModalidadeCompra": "string",
      "nomeModalidadeCompra": "string",
      "dataAssinatura": "2024-01-15",
      "dataVigenciaInicial": "2024-01-15",
      "dataVigenciaFinal": "2024-01-15",
      "valorTotal": 0,
      "statusAta": "string",
      "objeto": "string",
      "quantidadeItens": 0,
      "dataHoraAtualizacao": "2024-01-15 10:30:00",
      "dataHoraInclusao": "2024-01-15 10:30:00",
      "dataHoraExclusao": "2024-01-15 10:30:00",
      "ataExcluido": true,
      "numeroControlePncpAta": "string",
      "numeroControlePncpCompra": "string",
      "idCompra": "string"
    }
  ],
  "totalRegistros": 0,
  "totalPaginas": 0,
  "paginasRestantes": 0
}
```

### `GET /modulo-arp/1.2_consultarARP_FimVigencia`

#### Parameters

| Name | In | Type | Required | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `pagina` | query | `integer(int32)` | no | 1 |  |
| `tamanhoPagina` | query | `integer(int32)` | no | 10 |  |
| `codigoUnidadeGerenciadora` | query | `string` | no |  |  |
| `codigoModalidadeCompra` | query | `string` | no |  |  |
| `numeroAtaRegistroPreco` | query | `string` | no |  |  |
| `dataVigenciaFinalMin` | query | `string` | yes |  | YYYY-MM-DD |
| `dataVigenciaFinalMax` | query | `string` | yes |  | YYYY-MM-DD |
| `dataAssinaturaInicial` | query | `string` | no |  | YYYY-MM-DD |
| `dataAssinaturaFinal` | query | `string` | no |  | YYYY-MM-DD |

#### Response

- **Status:** `200`
- **Content type:** `*/*`

```json
{
  "resultado": [
    {
      "numeroAtaRegistroPreco": "string",
      "codigoUnidadeGerenciadora": "string",
      "nomeUnidadeGerenciadora": "string",
      "codigoOrgao": 0,
      "nomeOrgao": "string",
      "linkAtaPNCP": "string",
      "linkCompraPNCP": "string",
      "numeroCompra": "string",
      "anoCompra": "string",
      "codigoModalidadeCompra": "string",
      "nomeModalidadeCompra": "string",
      "dataAssinatura": "2024-01-15",
      "dataVigenciaInicial": "2024-01-15",
      "dataVigenciaFinal": "2024-01-15",
      "valorTotal": 0,
      "statusAta": "string",
      "objeto": "string",
      "quantidadeItens": 0,
      "dataHoraAtualizacao": "2024-01-15 10:30:00",
      "dataHoraInclusao": "2024-01-15 10:30:00",
      "dataHoraExclusao": "2024-01-15 10:30:00",
      "ataExcluido": true,
      "numeroControlePncpAta": "string",
      "numeroControlePncpCompra": "string",
      "idCompra": "string"
    }
  ],
  "totalRegistros": 0,
  "totalPaginas": 0,
  "paginasRestantes": 0
}
```

### `GET /modulo-arp/2_consultarARPItem`

#### Parameters

| Name | In | Type | Required | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `pagina` | query | `integer(int32)` | no | 1 |  |
| `tamanhoPagina` | query | `integer(int32)` | no | 10 |  |
| `codigoUnidadeGerenciadora` | query | `integer(int32)` | no |  |  |
| `codigoModalidadeCompra` | query | `string` | no |  |  |
| `dataVigenciaInicialMin` | query | `string` | yes |  | YYYY-MM-DD |
| `dataVigenciaInicialMax` | query | `string` | yes |  | YYYY-MM-DD |
| `dataAssinaturaInicial` | query | `string` | no |  | YYYY-MM-DD |
| `dataAssinaturaFinal` | query | `string` | no |  | YYYY-MM-DD |
| `numeroItem` | query | `string` | no |  |  |
| `codigoItem` | query | `integer(int32)` | no |  |  |
| `tipoItem` | query | `string` | no |  |  |
| `niFornecedor` | query | `string` | no |  |  |
| `codigoPdm` | query | `integer(int32)` | no |  |  |
| `numeroCompra` | query | `string` | no |  |  |

#### Response

- **Status:** `200`
- **Content type:** `*/*`

```json
{
  "resultado": [
    {
      "numeroAtaRegistroPreco": "string",
      "codigoUnidadeGerenciadora": "string",
      "numeroCompra": "string",
      "anoCompra": "string",
      "codigoModalidadeCompra": "string",
      "dataAssinatura": "2024-01-15 10:30:00",
      "dataVigenciaInicial": "YYYY-MM-DD",
      "dataVigenciaFinal": "YYYY-MM-DD",
      "numeroItem": "string",
      "codigoItem": 0,
      "descricaoItem": "string",
      "tipoItem": "string",
      "quantidadeHomologadaItem": 0,
      "classificacaoFornecedor": "string",
      "niFornecedor": "string",
      "nomeRazaoSocialFornecedor": "string",
      "quantidadeHomologadaVencedor": 0,
      "valorUnitario": 0,
      "valorTotal": 0,
      "maximoAdesao": 0,
      "nomeUnidadeGerenciadora": "string",
      "nomeModalidadeCompra": "string",
      "idCompra": "string",
      "numeroControlePncpCompra": "string",
      "dataHoraInclusao": "2024-01-15 10:30:00",
      "dataHoraAtualizacao": "2024-01-15 10:30:00",
      "quantidadeEmpenhada": 0,
      "percentualMaiorDesconto": 0,
      "situacaoSicaf": "string",
      "dataHoraExclusao": "2024-01-15 10:30:00",
      "itemExcluido": true,
      "numeroControlePncpAta": "string",
      "codigoPdm": 0,
      "nomePdm": "string"
    }
  ],
  "totalRegistros": 0,
  "totalPaginas": 0,
  "paginasRestantes": 0
}
```

### `GET /modulo-arp/2.1_consultarARPItem_Id`

#### Parameters

| Name | In | Type | Required | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `numeroControlePncpAta` | query | `string` | yes |  |  |
| `dataAtualizacao` | query | `string` | no |  | YYYY-MM-DD |

#### Response

- **Status:** `200`
- **Content type:** `*/*`

```json
{
  "resultado": [
    {
      "numeroAtaRegistroPreco": "string",
      "codigoUnidadeGerenciadora": "string",
      "numeroCompra": "string",
      "anoCompra": "string",
      "codigoModalidadeCompra": "string",
      "dataAssinatura": "2024-01-15 10:30:00",
      "dataVigenciaInicial": "YYYY-MM-DD",
      "dataVigenciaFinal": "YYYY-MM-DD",
      "numeroItem": "string",
      "codigoItem": 0,
      "descricaoItem": "string",
      "tipoItem": "string",
      "quantidadeHomologadaItem": 0,
      "classificacaoFornecedor": "string",
      "niFornecedor": "string",
      "nomeRazaoSocialFornecedor": "string",
      "quantidadeHomologadaVencedor": 0,
      "valorUnitario": 0,
      "valorTotal": 0,
      "maximoAdesao": 0,
      "nomeUnidadeGerenciadora": "string",
      "nomeModalidadeCompra": "string",
      "idCompra": "string",
      "numeroControlePncpCompra": "string",
      "dataHoraInclusao": "2024-01-15 10:30:00",
      "dataHoraAtualizacao": "2024-01-15 10:30:00",
      "quantidadeEmpenhada": 0,
      "percentualMaiorDesconto": 0,
      "situacaoSicaf": "string",
      "dataHoraExclusao": "2024-01-15 10:30:00",
      "itemExcluido": true,
      "numeroControlePncpAta": "string",
      "codigoPdm": 0,
      "nomePdm": "string"
    }
  ],
  "totalRegistros": 0,
  "totalPaginas": 0,
  "paginasRestantes": 0
}
```

### `GET /modulo-arp/3_consultarUnidadesItem`

#### Parameters

| Name | In | Type | Required | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `pagina` | query | `integer(int32)` | no | 1 |  |
| `tamanhoPagina` | query | `integer(int32)` | no | 10 |  |
| `numeroAta` | query | `string` | yes |  |  |
| `unidadeGerenciadora` | query | `string` | yes |  |  |
| `numeroItem` | query | `string` | yes |  |  |
| `dataAtualizacao` | query | `string` | no |  | YYYY-MM-DD |

#### Response

- **Status:** `200`
- **Content type:** `*/*`

```json
{
  "resultado": [
    {
      "numeroAta": "string",
      "unidadeGerenciadora": "string",
      "numeroItem": "string",
      "codigoPdm": "string",
      "descricaoItem": "string",
      "fornecedor": "string",
      "quantidadeRegistrada": 0,
      "saldoAdesoes": 0,
      "saldoRemanejamentoEmpenho": 0,
      "qtdLimiteAdesao": 0,
      "qtdLimiteInformadoCompra": 0,
      "aceitaAdesao": true,
      "dataHoraInclusao": "2024-01-15 10:30:00",
      "dataHoraAtualizacao": "2024-01-15 10:30:00",
      "dataHoraExclusao": "2024-01-15 10:30:00",
      "codigoUnidade": "string",
      "nomeUnidade": "string",
      "tipoUnidade": "string"
    }
  ],
  "totalRegistros": 0,
  "totalPaginas": 0,
  "paginasRestantes": 0
}
```

### `GET /modulo-arp/4_consultarEmpenhosSaldoItem`

#### Parameters

| Name | In | Type | Required | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `pagina` | query | `integer(int32)` | no | 1 |  |
| `tamanhoPagina` | query | `integer(int32)` | no | 10 |  |
| `numeroAta` | query | `string` | yes |  |  |
| `unidadeGerenciadora` | query | `string` | yes |  |  |
| `dataAtualizacao` | query | `string` | no |  | YYYY-MM-DD |

#### Response

- **Status:** `200`
- **Content type:** `*/*`

```json
{
  "resultado": [
    {
      "numeroItem": "string",
      "unidade": "string",
      "tipo": "string",
      "quantidadeRegistrada": 0,
      "quantidadeEmpenhada": 0,
      "saldoEmpenho": 0,
      "dataHoraInclusao": "2024-01-15 10:30:00",
      "dataHoraAtualizacao": "2024-01-15 10:30:00"
    }
  ],
  "totalRegistros": 0,
  "totalPaginas": 0,
  "paginasRestantes": 0
}
```

### `GET /modulo-arp/5_consultarAdesoesItem`

#### Parameters

| Name | In | Type | Required | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `pagina` | query | `integer(int32)` | no | 1 |  |
| `tamanhoPagina` | query | `integer(int32)` | no | 10 |  |
| `numeroAta` | query | `string` | yes |  |  |
| `unidadeGerenciadora` | query | `string` | yes |  |  |
| `numeroItem` | query | `string` | yes |  |  |
| `unidade` | query | `string` | no |  |  |
| `dataAtualizacao` | query | `string` | no |  | YYYY-MM-DD |

#### Response

- **Status:** `200`
- **Content type:** `*/*`

```json
{
  "resultado": [
    {
      "numeroAta": "string",
      "unidadeGerenciadora": "string",
      "unidadeNaoParticipante": "string",
      "dataAprovacaoAnalise": "2024-01-15 10:30:00",
      "quantidadeAprovadaAdesao": 0
    }
  ],
  "totalRegistros": 0,
  "totalPaginas": 0,
  "paginasRestantes": 0
}
```

## 09 - CONTRATOS

Consulta contratos e seus respectivos itens.

### `GET /modulo-contratos/1_consultarContratos`

#### Parameters

| Name | In | Type | Required | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `pagina` | query | `integer(int32)` | no | 1 |  |
| `tamanhoPagina` | query | `integer(int32)` | no | 10 |  |
| `codigoOrgao` | query | `string` | yes |  |  |
| `codigoUnidadeGestora` | query | `string` | no |  |  |
| `codigoUnidadeGestoraOrigemContrato` | query | `string` | no |  |  |
| `codigoUnidadeRealizadoraCompra` | query | `string` | no |  |  |
| `numeroContrato` | query | `string` | no |  |  |
| `codigoModalidadeCompra` | query | `string` | no |  |  |
| `codigoTipo` | query | `string` | no |  |  |
| `codigoCategoria` | query | `string` | no |  |  |
| `niFornecedor` | query | `string` | no |  |  |
| `dataVigenciaInicialMin` | query | `string` | yes |  | YYYY-MM-DD |
| `dataVigenciaInicialMax` | query | `string` | yes |  | YYYY-MM-DD |

#### Response

- **Status:** `200`
- **Content type:** `*/*`

```json
{
  "resultado": [
    {
      "codigoOrgao": "string",
      "nomeOrgao": "string",
      "codigoUnidadeGestora": "string",
      "nomeUnidadeGestora": "string",
      "codigoUnidadeGestoraOrigemContrato": "string",
      "nomeUnidadeGestoraOrigemContrato": "string",
      "receitaDespesa": "string",
      "numeroContrato": "string",
      "codigoUnidadeRealizadoraCompra": "string",
      "nomeUnidadeRealizadoraCompra": "string",
      "numeroCompra": "string",
      "codigoModalidadeCompra": "string",
      "nomeModalidadeCompra": "string",
      "codigoTipo": "string",
      "nomeTipo": "string",
      "codigoCategoria": "string",
      "nomeCategoria": "string",
      "codigoSubcategoria": "string",
      "nomeSubcategoria": "string",
      "niFornecedor": "string",
      "nomeRazaoSocialFornecedor": "string",
      "processo": "string",
      "objeto": "string",
      "informacoesComplementares": "string",
      "dataVigenciaInicial": "2024-01-15 10:30:00",
      "dataVigenciaFinal": "2024-01-15 10:30:00",
      "valorGlobal": 0,
      "numeroParcelas": 0,
      "valorParcela": 0,
      "valorAcumulado": 0,
      "totalDespesasAcessorias": 0,
      "dataHoraInclusao": "2024-01-15 10:30:00",
      "numeroControlePncpContrato": "string",
      "numeroControlePncpCompra": "string",
      "idCompra": "string",
      "dataHoraExclusao": "2024-01-15 10:30:00",
      "contratoExcluido": true,
      "unidadesRequisitantes": "string"
    }
  ],
  "totalRegistros": 0,
  "totalPaginas": 0,
  "paginasRestantes": 0
}
```

### `GET /modulo-contratos/1.1_consultarContratos_Id`

#### Parameters

| Name | In | Type | Required | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `codigo` | query | `string` | yes |  |  |
| `tipo` | query | `string` | yes |  | Values: `idCompra`, `numeroControlePncpContrato` |

#### Response

- **Status:** `200`
- **Content type:** `*/*`

```json
{
  "resultado": [
    {
      "codigoOrgao": "string",
      "nomeOrgao": "string",
      "codigoUnidadeGestora": "string",
      "nomeUnidadeGestora": "string",
      "codigoUnidadeGestoraOrigemContrato": "string",
      "nomeUnidadeGestoraOrigemContrato": "string",
      "receitaDespesa": "string",
      "numeroContrato": "string",
      "codigoUnidadeRealizadoraCompra": "string",
      "nomeUnidadeRealizadoraCompra": "string",
      "numeroCompra": "string",
      "codigoModalidadeCompra": "string",
      "nomeModalidadeCompra": "string",
      "codigoTipo": "string",
      "nomeTipo": "string",
      "codigoCategoria": "string",
      "nomeCategoria": "string",
      "codigoSubcategoria": "string",
      "nomeSubcategoria": "string",
      "niFornecedor": "string",
      "nomeRazaoSocialFornecedor": "string",
      "processo": "string",
      "objeto": "string",
      "informacoesComplementares": "string",
      "dataVigenciaInicial": "2024-01-15 10:30:00",
      "dataVigenciaFinal": "2024-01-15 10:30:00",
      "valorGlobal": 0,
      "numeroParcelas": 0,
      "valorParcela": 0,
      "valorAcumulado": 0,
      "totalDespesasAcessorias": 0,
      "dataHoraInclusao": "2024-01-15 10:30:00",
      "numeroControlePncpContrato": "string",
      "numeroControlePncpCompra": "string",
      "idCompra": "string",
      "dataHoraExclusao": "2024-01-15 10:30:00",
      "contratoExcluido": true,
      "unidadesRequisitantes": "string"
    }
  ],
  "totalRegistros": 0,
  "totalPaginas": 0,
  "paginasRestantes": 0
}
```

### `GET /modulo-contratos/1.2_consultarContratos_FimVigencia`

#### Parameters

| Name | In | Type | Required | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `pagina` | query | `integer(int32)` | no | 1 |  |
| `tamanhoPagina` | query | `integer(int32)` | no | 10 |  |
| `codigoOrgao` | query | `string` | yes |  |  |
| `codigoUnidadeGestora` | query | `string` | no |  |  |
| `codigoUnidadeGestoraOrigemContrato` | query | `string` | no |  |  |
| `codigoUnidadeRealizadoraCompra` | query | `string` | no |  |  |
| `numeroContrato` | query | `string` | no |  |  |
| `codigoModalidadeCompra` | query | `string` | no |  |  |
| `codigoTipo` | query | `string` | no |  |  |
| `codigoCategoria` | query | `string` | no |  |  |
| `niFornecedor` | query | `string` | no |  |  |
| `dataVigenciaFinalMin` | query | `string` | yes |  | YYYY-MM-DD |
| `dataVigenciaFinalMax` | query | `string` | yes |  | YYYY-MM-DD |

#### Response

- **Status:** `200`
- **Content type:** `*/*`

```json
{
  "resultado": [
    {
      "codigoOrgao": "string",
      "nomeOrgao": "string",
      "codigoUnidadeGestora": "string",
      "nomeUnidadeGestora": "string",
      "codigoUnidadeGestoraOrigemContrato": "string",
      "nomeUnidadeGestoraOrigemContrato": "string",
      "receitaDespesa": "string",
      "numeroContrato": "string",
      "codigoUnidadeRealizadoraCompra": "string",
      "nomeUnidadeRealizadoraCompra": "string",
      "numeroCompra": "string",
      "codigoModalidadeCompra": "string",
      "nomeModalidadeCompra": "string",
      "codigoTipo": "string",
      "nomeTipo": "string",
      "codigoCategoria": "string",
      "nomeCategoria": "string",
      "codigoSubcategoria": "string",
      "nomeSubcategoria": "string",
      "niFornecedor": "string",
      "nomeRazaoSocialFornecedor": "string",
      "processo": "string",
      "objeto": "string",
      "informacoesComplementares": "string",
      "dataVigenciaInicial": "2024-01-15 10:30:00",
      "dataVigenciaFinal": "2024-01-15 10:30:00",
      "valorGlobal": 0,
      "numeroParcelas": 0,
      "valorParcela": 0,
      "valorAcumulado": 0,
      "totalDespesasAcessorias": 0,
      "dataHoraInclusao": "2024-01-15 10:30:00",
      "numeroControlePncpContrato": "string",
      "numeroControlePncpCompra": "string",
      "idCompra": "string",
      "dataHoraExclusao": "2024-01-15 10:30:00",
      "contratoExcluido": true,
      "unidadesRequisitantes": "string"
    }
  ],
  "totalRegistros": 0,
  "totalPaginas": 0,
  "paginasRestantes": 0
}
```

### `GET /modulo-contratos/2_consultarContratosItem`

#### Parameters

| Name | In | Type | Required | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `pagina` | query | `integer(int32)` | no | 1 |  |
| `tamanhoPagina` | query | `integer(int32)` | no | 10 |  |
| `codigoOrgao` | query | `string` | yes |  |  |
| `codigoUnidadeGestora` | query | `string` | no |  |  |
| `codigoUnidadeGestoraOrigemContrato` | query | `string` | no |  |  |
| `codigoUnidadeRealizadoraCompra` | query | `string` | no |  |  |
| `numeroContrato` | query | `string` | no |  |  |
| `codigoModalidadeCompra` | query | `string` | no |  |  |
| `tipoItem` | query | `string` | no |  |  |
| `codigoItem` | query | `integer(int32)` | no |  |  |
| `niFornecedor` | query | `string` | no |  |  |
| `dataVigenciaInicialMin` | query | `string` | yes |  | YYYY-MM-DD |
| `dataVigenciaInicialMax` | query | `string` | yes |  | YYYY-MM-DD |
| `poder` | query | `string` | no |  | Values: `Executivo`, `Legislativo`, `Judiciário` |
| `esfera` | query | `string` | no |  | Values: `Federal`, `Estadual`, `Municipal` |
| `idCompra` | query | `string` | no |  |  |

#### Response

- **Status:** `200`
- **Content type:** `*/*`

```json
{
  "resultado": [
    {
      "codigoOrgao": "string",
      "codigoUnidadeGestora": "string",
      "codigoUnidadeGestoraOrigemContrato": "string",
      "codigoUnidadeRealizadoraCompra": "string",
      "codigoModalidadeCompra": "string",
      "numeroContrato": "string",
      "niFornecedor": "string",
      "nomeRazaoSocialFornecedor": "string",
      "processo": "string",
      "dataVigenciaInicial": "2024-01-15 10:30:00",
      "dataVigenciaFinal": "2024-01-15 10:30:00",
      "valorGlobal": 0,
      "tipoItem": "string",
      "codigoItem": 0,
      "descricaoIitem": "string",
      "quantidadeItem": 0,
      "valorUnitarioItem": 0,
      "valorTotalItem": 0,
      "dataHoraInclusao": "2024-01-15 10:30:00",
      "numeroControlePncpContrato": "string",
      "idCompra": "string",
      "dataHoraExclusaoContrato": "2024-01-15 10:30:00",
      "contratoExcluido": true,
      "nomeOrgao": "string",
      "nomeUnidadeGestora": "string",
      "nomeUnidadeGestoraOrigemContrato": "string",
      "nomeUnidadeRealizadoraCompra": "string",
      "nomeModalidadeCompra": "string",
      "numeroCompra": "string",
      "dataHoraExclusaoItem": "2024-01-15 10:30:00",
      "contratoItemExcluido": true,
      "numeroItem": "string",
      "esfera": "string",
      "poder": "string",
      "numeroControlePncpCompra": "string"
    }
  ],
  "totalRegistros": 0,
  "totalPaginas": 0,
  "paginasRestantes": 0
}
```

### `GET /modulo-contratos/2.1_consultarContratosItem_Id`

#### Parameters

| Name | In | Type | Required | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `tipo` | query | `string` | yes |  | Values: `idCompra`, `numeroControlePncpContrato` |
| `codigo` | query | `string` | yes |  |  |

#### Response

- **Status:** `200`
- **Content type:** `*/*`

```json
{
  "resultado": [
    {
      "codigoOrgao": "string",
      "codigoUnidadeGestora": "string",
      "codigoUnidadeGestoraOrigemContrato": "string",
      "codigoUnidadeRealizadoraCompra": "string",
      "codigoModalidadeCompra": "string",
      "numeroContrato": "string",
      "niFornecedor": "string",
      "nomeRazaoSocialFornecedor": "string",
      "processo": "string",
      "dataVigenciaInicial": "2024-01-15 10:30:00",
      "dataVigenciaFinal": "2024-01-15 10:30:00",
      "valorGlobal": 0,
      "tipoItem": "string",
      "codigoItem": 0,
      "descricaoIitem": "string",
      "quantidadeItem": 0,
      "valorUnitarioItem": 0,
      "valorTotalItem": 0,
      "dataHoraInclusao": "2024-01-15 10:30:00",
      "numeroControlePncpContrato": "string",
      "idCompra": "string",
      "dataHoraExclusaoContrato": "2024-01-15 10:30:00",
      "contratoExcluido": true,
      "nomeOrgao": "string",
      "nomeUnidadeGestora": "string",
      "nomeUnidadeGestoraOrigemContrato": "string",
      "nomeUnidadeRealizadoraCompra": "string",
      "nomeModalidadeCompra": "string",
      "numeroCompra": "string",
      "dataHoraExclusaoItem": "2024-01-15 10:30:00",
      "contratoItemExcluido": true,
      "numeroItem": "string",
      "esfera": "string",
      "poder": "string",
      "numeroControlePncpCompra": "string"
    }
  ],
  "totalRegistros": 0,
  "totalPaginas": 0,
  "paginasRestantes": 0
}
```

## 10 - FORNECEDOR

Consulta fornecedores registrados.

### `GET /modulo-fornecedor/1_consultarFornecedor`

#### Parameters

| Name | In | Type | Required | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `pagina` | query | `integer(int32)` | no | 1 |  |
| `tamanhoPagina` | query | `integer(int32)` | no | 10 |  |
| `cnpj` | query | `string` | no |  |  |
| `cpf` | query | `string` | no |  |  |
| `naturezaJuridicaId` | query | `integer(int64)` | no |  |  |
| `porteEmpresaId` | query | `integer(int64)` | no |  |  |
| `codigoCnae` | query | `integer` | no |  |  |
| `ativo` | query | `boolean` | yes |  |  |

#### Response

- **Status:** `200`
- **Content type:** `*/*`

```json
{
  "resultado": [
    {
      "ativo": true,
      "cnpj": "string",
      "cpf": "string",
      "habilitadoLicitar": true,
      "codigoCnae": 0,
      "nomeCnae": "string",
      "nomeMunicipio": "string",
      "naturezaJuridicaId": 0,
      "naturezaJuridicaNome": "string",
      "porteEmpresaId": 0,
      "porteEmpresaNome": "string",
      "nomeRazaoSocialFornecedor": "string",
      "ufSigla": "string"
    }
  ],
  "totalRegistros": 0,
  "totalPaginas": 0,
  "paginasRestantes": 0
}
```

## 11 - OCDS

Consulta contratações no formato OCDS (Open Contracting Data Standard).

### `GET /modulo-ocds/1_releases`

#### Parameters

| Name | In | Type | Required | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `page` | query | `integer(int32)` | no | 1 |  |
| `offSet` | query | `integer(int32)` | no | 10 |  |
| `buyerID` | query | `string` | yes |  | BR-CNPJ |
| `releaseStartDate` | query | `string` | yes |  | YYYY-MM-DD |
| `releaseEndDate` | query | `string` | yes |  | YYYY-MM-DD |

#### Response

- **Status:** `200`
- **Content type:** `*/*`

```json
{
  "publisherDTO": {
    "name": "string",
    "uri": "string"
  },
  "publishedDate": "2024-01-15T10:30:00",
  "version": "string",
  "publicationPolicy": "string",
  "license": "string",
  "extensions": [
    "string"
  ],
  "releases": [
    {
      "ocid": "string",
      "id": "string",
      "date": "2024-01-15T10:30:00",
      "tag": [
        "string"
      ],
      "initiationType": "string",
      "buyer": {
        "id": "string",
        "name": "string"
      },
      "language": "string",
      "parties": [
        {
          "id": "string",
          "name": "string",
          "identifier": {
            "scheme": "string",
            "id": "string",
            "legalName": "string"
          },
          "additionalIdentifiers": [
            {
              "id": "string",
              "legalName": "string"
            }
          ],
          "address": {
            "region": "string",
            "locality": "string",
            "countryName": "string"
          },
          "roles": [
            "string"
          ],
          "details": {
            "classifications": [
              {
                "scheme": "string",
                "id": "string",
                "uri": "string"
              }
            ]
          },
          "suppliers": [
            {
              "id": "string",
              "name": "string"
            }
          ]
        }
      ],
      "tender": {
        "id": "string",
        "title": "string",
        "description": "string",
        "procuringEntity": {
          "name": "string",
          "id": "string"
        },
        "value": {
          "amount": 0,
          "currency": "string"
        },
        "procurementMethod": "string",
        "procurementMethodDetails": "string",
        "procurementMethodRationale": "string",
        "submissionMethod": [
          "string"
        ],
        "tenderPeriod": {
          "startDate": "2024-01-15T10:30:00",
          "endDate": "2024-01-15T10:30:00",
          "maxExtentDate": "2024-01-15T10:30:00",
          "durationInDays": 0
        },
        "items": [
          {
            "id": "string",
            "description": "string",
            "statusDetails": "string",
            "quantity": 0,
            "unit": {
              "name": "string",
              "value": {
                "amount": 0,
                "currency": "string"
              }
            },
            "relatedLot": "string"
          }
        ],
        "lots": [
          {
            "id": "string",
            "statusDetailsId": "string",
            "statusDetails": "string",
            "value": {
              "amount": 0,
              "currency": "string"
            },
            "confidentialBudget": true,
            "asset": "string",
            "realEstateRegistrationCode": "string",
            "standardPreferenceMarginApplicability": true,
            "standardPreferenceMarginPercentage": 0,
            "additionalPreferenceMarginApplicability": true,
            "additionalPreferenceMarginPercentage": 0,
            "ncmNbsCode": "string",
            "ncmNbsDescription": "string",
            "catalogItemCategoryId": 0,
            "catalogItemCategoryName": "string",
            "catalogItemCode": 0,
            "awardCriteria": "string",
            "awardCriteriaDetails": "string",
            "sustainability": [
              {
                "goal": "string",
                "strategies": [
                  null
                ]
              }
            ],
            "otherRequirements": {
              "reservedParticipation": [
                "string"
              ]
            },
            "subcontractingTerms": {
              "description": "string"
            }
          }
        ]
      },
      "awards": [
        {
          "id": "string",
          "title": "string",
          "description": "string",
          "date": "2024-01-15T10:30:00",
          "hasSubcontracting": true,
          "value": {
            "amount": 0,
            "currency": "string"
          },
          "suppliers": [
            {
              "id": "string",
              "name": "string"
            }
          ],
          "items": [
            {
              "id": "string",
              "description": "string",
              "statusDetails": "string",
              "quantity": 0,
              "unit": {
                "name": "string",
                "value": {
                  "amount": null,
                  "currency": null
                }
              },
              "relatedLot": "string"
            }
          ]
        }
      ]
    }
  ],
  "links": {
    "next": "string",
    "prev": "string"
  },
  "uri": "string"
}
```

## 97 - INDICADORES

Este módulo expõe endpoints de indicadores de uso e desempenho da API Compras V2.

### `GET /modulo-indicadores/1_consultarIndicadoresConsolidados`

#### Parameters

_No parameters._

#### Response

- **Status:** `200`
- **Content type:** `*/*`

```json
{
  "resultado": [
    {
      "anoMesInicio": "string",
      "anoMesFim": "string",
      "2026-04-26": "YYYY-MM-DD",
      "totalServicos": 0,
      "totalRequisicoes": 0,
      "percentualSucesso": 0,
      "mediaTempoRespostaMs": 0,
      "totalDownloadGb": 0,
      "mediaDownloadMesGb": 0
    }
  ],
  "totalRegistros": 0,
  "totalPaginas": 0,
  "paginasRestantes": 0
}
```

### `GET /modulo-indicadores/2_consultarIndicadoresPorPeriodo`

#### Parameters

| Name | In | Type | Required | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `pagina` | query | `integer(int32)` | no | 1 |  |
| `tamanhoPagina` | query | `integer(int32)` | no | 10 |  |
| `ano` | query | `integer(int32)` | yes |  |  |
| `mes` | query | `integer(int32)` | no |  |  |

#### Response

- **Status:** `200`
- **Content type:** `*/*`

```json
{
  "resultado": [
    {
      "anoMes": "string",
      "ano": 0,
      "mes": 0,
      "totalServicos": 0,
      "totalRequisicoes": 0,
      "percentualSucesso": 0,
      "mediaTempoRespostaMs": 0,
      "totalDownloadGb": 0,
      "totalDownloadMbytes": 0
    }
  ],
  "totalRegistros": 0,
  "totalPaginas": 0,
  "paginasRestantes": 0
}
```

## 98 - ALICE

Serviços de integração Analisador de Licitações, Contratos e Editais (Alice) e Compras.gov.

### `GET /alice/avisos-restritos`

#### Parameters

| Name | In | Type | Required | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `dataInicioIntervalo` | query | `string` | yes |  | DD/MM/YYYY HH:MM:SS |
| `dataFimIntervalo` | query | `string` | yes |  | DD/MM/YYYY HH:MM:SS |

#### Response

- **Status:** `200`
- **Content type:** `*/*`

```json
[
  {
    "msgErro": "string",
    "dataSolicitacaoAnalise": "string",
    "dataEncerramentoAnalise": "string",
    "ticketAnalise": "string",
    "tipoAnalise": 0,
    "codigoStatusAnalise": 0,
    "descricaoStatusAnalise": "string",
    "chaveCompra": "string"
  }
]
```

### `GET /alice/compras`

#### Parameters

| Name | In | Type | Required | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `chavesCompra` | query | `array[string]` | yes |  |  |

#### Response

- **Status:** `200`
- **Content type:** `*/*`

```json
[
  {
    "msgErro": "string",
    "dataSolicitacaoAnalise": "string",
    "dataEncerramentoAnalise": "string",
    "ticketAnalise": "string",
    "tipoAnalise": 0,
    "codigoStatusAnalise": 0,
    "descricaoStatusAnalise": "string",
    "chaveCompra": "string"
  }
]
```

### `GET /alice/tickets`

#### Parameters

| Name | In | Type | Required | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `tickets` | query | `array[string]` | yes |  |  |

#### Response

- **Status:** `200`
- **Content type:** `*/*`

```json
[
  {
    "msgErro": "string",
    "dataSolicitacaoAnalise": "string",
    "dataEncerramentoAnalise": "string",
    "ticketAnalise": "string",
    "tipoAnalise": 0,
    "codigoStatusAnalise": 0,
    "descricaoStatusAnalise": "string",
    "chaveCompra": "string",
    "itens": [
      {
        "idAviso": 0,
        "codigoTipoAviso": 0,
        "nomeTipoAviso": "string",
        "texto": "string",
        "descricao": "string",
        "fundamentacao": "string",
        "numeroSequencialAviso": 0
      }
    ]
  }
]
```

## 99 - USUARIOS

Serviço de gestão de usuários.

### `PATCH /usuarios/atualizar/{id}`

#### Parameters

| Name | In | Type | Required | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `id` | path | `integer(int32)` | yes |  |  |

#### Request body

Content type: `application/json`

```json
{
  "nome": "string",
  "cpfCnpj": "string",
  "email": "string",
  "telefone": "string",
  "administrador": true,
  "dataInclusao": "2024-01-15T10:30:00",
  "dataAtualizacao": "2024-01-15T10:30:00",
  "dataDelecaoSuspensao": "2024-01-15T10:30:00",
  "excluidoSuspenso": true,
  "razaoExclusaoSuspensao": "string"
}
```

#### Response

- **Status:** `200`
- **Content type:** `*/*`

```json
{
  "id": 0,
  "nome": "string",
  "cpfCnpj": "string",
  "email": "string",
  "telefone": "string",
  "login": "string",
  "administrador": true,
  "dataInclusao": "2024-01-15T10:30:00",
  "dataAtualizacao": "2024-01-15T10:30:00",
  "dataDelecaoSuspensao": "2024-01-15T10:30:00",
  "excluidoSuspenso": true,
  "razaoExclusaoSuspensao": "string"
}
```

### `GET /usuarios/consultar`

#### Parameters

| Name | In | Type | Required | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `id` | query | `integer(int32)` | no |  |  |

#### Response

- **Status:** `200`
- **Content type:** `*/*`

```json
[
  {
    "id": 0,
    "nome": "string",
    "cpfCnpj": "string",
    "email": "string",
    "telefone": "string",
    "login": "string",
    "administrador": true,
    "dataInclusao": "2024-01-15T10:30:00",
    "dataAtualizacao": "2024-01-15T10:30:00",
    "dataDelecaoSuspensao": "2024-01-15T10:30:00",
    "excluidoSuspenso": true,
    "razaoExclusaoSuspensao": "string"
  }
]
```

### `POST /usuarios/criar`

#### Parameters

_No parameters._

#### Request body

Content type: `application/json`

```json
{
  "nome": "string",
  "cpfCnpj": "string",
  "email": "string",
  "telefone": "string",
  "administrador": true,
  "dataInclusao": "2024-01-15T10:30:00",
  "dataAtualizacao": "2024-01-15T10:30:00",
  "dataDelecaoSuspensao": "2024-01-15T10:30:00",
  "excluidoSuspenso": true,
  "razaoExclusaoSuspensao": "string"
}
```

#### Response

- **Status:** `200`
- **Content type:** `*/*`

```json
{
  "nome": "string",
  "cpfCnpj": "string",
  "email": "string",
  "telefone": "string",
  "administrador": true,
  "dataInclusao": "2024-01-15T10:30:00",
  "dataAtualizacao": "2024-01-15T10:30:00",
  "dataDelecaoSuspensao": "2024-01-15T10:30:00",
  "excluidoSuspenso": true,
  "razaoExclusaoSuspensao": "string",
  "login": "string",
  "senha": "string"
}
```

### `PATCH /usuarios/resetSenha/{id}`

#### Parameters

| Name | In | Type | Required | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `id` | path | `integer(int32)` | yes |  |  |

#### Response

- **Status:** `200`
- **Content type:** `*/*`

```text
"string"
```

## AUTENTICACAO

Descrição do serviço de autenticação de usuários

### `POST /autenticacao/login`

#### Parameters

_No parameters._

#### Request body

Content type: `application/json`

```json
{
  "login": "string",
  "senha": "string"
}
```

#### Response

- **Status:** `200`
- **Content type:** `*/*`

```text
"string"
```
