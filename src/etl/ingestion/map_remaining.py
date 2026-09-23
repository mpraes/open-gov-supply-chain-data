import json
from typing import Any

from contracts.camel import snake_row
from contracts.coerce import coerce_id_text
from etl.ingestion.remaining_columns import (
    ALICE_AVISO_COLUMNS,
    ALICE_AVISO_PK,
    ARP_ADESAO_COLUMNS,
    ARP_ADESAO_PK,
    ARP_COLUMNS,
    ARP_EMPENHO_COLUMNS,
    ARP_EMPENHO_PK,
    ARP_ITEM_COLUMNS,
    ARP_ITEM_PK,
    ARP_PK,
    ARP_UNIDADE_COLUMNS,
    ARP_UNIDADE_PK,
    CONTRATACAO_COLUMNS,
    CONTRATACAO_ITEM_COLUMNS,
    CONTRATACAO_ITEM_PK,
    CONTRATACAO_PK,
    CONTRATACAO_RESULTADO_COLUMNS,
    CONTRATACAO_RESULTADO_PK,
    CONTRATO_COLUMNS,
    CONTRATO_ITEM_COLUMNS,
    CONTRATO_ITEM_PK,
    CONTRATO_PK,
    FORNECEDOR_COLUMNS,
    FORNECEDOR_PK,
    INDICADOR_CONSOLIDADO_COLUMNS,
    INDICADOR_CONSOLIDADO_PK,
    INDICADOR_PERIODO_COLUMNS,
    INDICADOR_PERIODO_PK,
    OCDS_RELEASE_COLUMNS,
    OCDS_RELEASE_PK,
)


def mapped_columns(
    row: dict[str, Any],
    required: tuple[str, ...],
    columns: tuple[str, ...],
    extra: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Snake-case an API row and keep only declared columns.

    Example:
        mapped_columns({"idCompra": "1"}, ("id_compra",), ("id_compra", "objeto"))
    """
    fields = snake_row(row)
    if extra is not None:
        fields.update(extra)
    for key in required:
        value = fields.get(key)
        if value is None or value == "":
            raise KeyError(key)
        fields[key] = coerce_id_text(value, key)
    return {name: fields.get(name) for name in columns}


def contratacao_fields(row: dict[str, Any]) -> dict[str, Any]:
    """Map consultarContratacoes_PNCP_14133 to contratacao columns."""
    return mapped_columns(row, CONTRATACAO_PK, CONTRATACAO_COLUMNS)


def contratacao_item_fields(row: dict[str, Any]) -> dict[str, Any]:
    """Map consultarItensContratacoes_PNCP_14133 to contratacao_item columns."""
    return mapped_columns(row, CONTRATACAO_ITEM_PK, CONTRATACAO_ITEM_COLUMNS)


def contratacao_resultado_fields(row: dict[str, Any]) -> dict[str, Any]:
    """Map consultarResultadoItensContratacoes to contratacao_resultado columns."""
    return mapped_columns(row, CONTRATACAO_RESULTADO_PK, CONTRATACAO_RESULTADO_COLUMNS)


def arp_fields(row: dict[str, Any]) -> dict[str, Any]:
    """Map consultarARP to arp columns."""
    return mapped_columns(row, ARP_PK, ARP_COLUMNS, extra=arp_pncp_ata_when_missing(row))


def arp_item_fields(row: dict[str, Any]) -> dict[str, Any]:
    """Map consultarARPItem to arp_item columns."""
    return mapped_columns(
        row, ARP_ITEM_PK, ARP_ITEM_COLUMNS, extra=arp_pncp_ata_when_missing(row)
    )


def arp_pncp_ata_when_missing(row: dict[str, Any]) -> dict[str, Any]:
    """Derive PK from unidade+ata when consultarARP omits numeroControlePncpAta.

    Example:
        arp_pncp_ata_when_missing(
            {"codigoUnidadeGerenciadora": "120636",
             "numeroAtaRegistroPreco": "00265/2026"}
        )
    """
    snake = snake_row(row)
    if snake.get("numero_controle_pncp_ata"):
        return {}
    unidade = snake.get("codigo_unidade_gerenciadora")
    ata = snake.get("numero_ata_registro_preco")
    if unidade in (None, "") or ata in (None, ""):
        return {}
    return {
        "numero_controle_pncp_ata": (
            f"{coerce_id_text(unidade, 'codigo_unidade_gerenciadora')}:"
            f"{coerce_id_text(ata, 'numero_ata_registro_preco')}"
        )
    }


def arp_unidade_fields(row: dict[str, Any]) -> dict[str, Any]:
    """Map consultarUnidadesItem to arp_unidade_item columns."""
    return mapped_columns(row, ARP_UNIDADE_PK, ARP_UNIDADE_COLUMNS)


def arp_empenho_fields(
    row: dict[str, Any],
    *,
    numero_ata: str,
    unidade_gerenciadora: str,
) -> dict[str, Any]:
    """Map consultarEmpenhosSaldoItem and attach the ATA filter keys."""
    return mapped_columns(
        row,
        ARP_EMPENHO_PK,
        ARP_EMPENHO_COLUMNS,
        extra={"numero_ata": numero_ata, "unidade_gerenciadora": unidade_gerenciadora},
    )


def arp_adesao_fields(row: dict[str, Any]) -> dict[str, Any]:
    """Map consultarAdesoesItem to arp_adesao columns."""
    return mapped_columns(row, ARP_ADESAO_PK, ARP_ADESAO_COLUMNS)


def contrato_fields(row: dict[str, Any]) -> dict[str, Any]:
    """Map consultarContratos to contrato columns."""
    return mapped_columns(row, CONTRATO_PK, CONTRATO_COLUMNS)


def contrato_item_fields(row: dict[str, Any]) -> dict[str, Any]:
    """Map consultarContratosItem to contrato_item columns."""
    return mapped_columns(row, CONTRATO_ITEM_PK, CONTRATO_ITEM_COLUMNS)


def fornecedor_fields(row: dict[str, Any]) -> dict[str, Any]:
    """Map consultarFornecedor and derive ni_fornecedor from CNPJ or CPF."""
    snake = snake_row(row)
    ni = snake.get("cnpj") or snake.get("cpf")
    return mapped_columns(row, FORNECEDOR_PK, FORNECEDOR_COLUMNS, extra={"ni_fornecedor": ni})


def indicador_consolidado_fields(row: dict[str, Any]) -> dict[str, Any]:
    """Map consultarIndicadoresConsolidados, ignoring date-named keys."""
    return mapped_columns(row, INDICADOR_CONSOLIDADO_PK, INDICADOR_CONSOLIDADO_COLUMNS)


def indicador_periodo_fields(row: dict[str, Any]) -> dict[str, Any]:
    """Map consultarIndicadoresPorPeriodo to indicador_periodo columns."""
    return mapped_columns(row, INDICADOR_PERIODO_PK, INDICADOR_PERIODO_COLUMNS)


def ocds_release_fields(row: dict[str, Any]) -> dict[str, Any]:
    """Flatten one OCDS release into tabular columns plus JSON payload."""
    buyer = row.get("buyer") if isinstance(row.get("buyer"), dict) else {}
    tender = row.get("tender") if isinstance(row.get("tender"), dict) else {}
    extra = {
        "buyer_id": buyer.get("id"),
        "buyer_name": buyer.get("name"),
        "tender_id": tender.get("id"),
        "tender_title": tender.get("title"),
        "release_json": json.dumps(row, ensure_ascii=True),
    }
    return mapped_columns(row, OCDS_RELEASE_PK, OCDS_RELEASE_COLUMNS, extra=extra)


def alice_aviso_fields(row: dict[str, Any]) -> dict[str, Any]:
    """Map /alice/avisos-restritos objects to alice_aviso columns."""
    return mapped_columns(row, ALICE_AVISO_PK, ALICE_AVISO_COLUMNS)
