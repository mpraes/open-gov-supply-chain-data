from typing import Any

from contracts.remaining_records import (
    AliceAvisoRecord,
    ArpAdesaoRecord,
    ArpEmpenhoRecord,
    ArpItemRecord,
    ArpRecord,
    ArpUnidadeItemRecord,
    ContratacaoItemRecord,
    ContratacaoRecord,
    ContratacaoResultadoRecord,
    ContratoItemRecord,
    ContratoRecord,
    FornecedorRecord,
    IndicadorConsolidadoRecord,
    IndicadorPeriodoRecord,
    OcdsReleaseRecord,
)
from etl.ingestion.map_remaining import (
    alice_aviso_fields,
    arp_adesao_fields,
    arp_empenho_fields,
    arp_fields,
    arp_item_fields,
    arp_unidade_fields,
    contratacao_fields,
    contratacao_item_fields,
    contratacao_resultado_fields,
    contrato_fields,
    contrato_item_fields,
    fornecedor_fields,
    indicador_consolidado_fields,
    indicador_periodo_fields,
    ocds_release_fields,
)


def map_contratacao_row(row: dict[str, Any]) -> ContratacaoRecord:
    """Map one PNCP contratação header."""
    return ContratacaoRecord(**contratacao_fields(row))


def map_contratacao_item_row(row: dict[str, Any]) -> ContratacaoItemRecord:
    """Map one PNCP contratação item."""
    return ContratacaoItemRecord(**contratacao_item_fields(row))


def map_contratacao_resultado_row(row: dict[str, Any]) -> ContratacaoResultadoRecord:
    """Map one PNCP item result."""
    return ContratacaoResultadoRecord(**contratacao_resultado_fields(row))


def map_arp_row(row: dict[str, Any]) -> ArpRecord:
    """Map one ARP header."""
    return ArpRecord(**arp_fields(row))


def map_arp_item_row(row: dict[str, Any]) -> ArpItemRecord:
    """Map one ARP item."""
    return ArpItemRecord(**arp_item_fields(row))


def map_arp_unidade_row(row: dict[str, Any]) -> ArpUnidadeItemRecord:
    """Map one ARP participating unit."""
    return ArpUnidadeItemRecord(**arp_unidade_fields(row))


def map_arp_empenho_row(
    row: dict[str, Any],
    *,
    numero_ata: str,
    unidade_gerenciadora: str,
) -> ArpEmpenhoRecord:
    """Map one ARP empenho row with ATA keys from the filter."""
    return ArpEmpenhoRecord(
        **arp_empenho_fields(
            row, numero_ata=numero_ata, unidade_gerenciadora=unidade_gerenciadora
        )
    )


def map_arp_adesao_row(row: dict[str, Any]) -> ArpAdesaoRecord:
    """Map one ARP accession row."""
    return ArpAdesaoRecord(**arp_adesao_fields(row))


def map_contrato_row(row: dict[str, Any]) -> ContratoRecord:
    """Map one contract header."""
    return ContratoRecord(**contrato_fields(row))


def map_contrato_item_row(row: dict[str, Any]) -> ContratoItemRecord:
    """Map one contract item."""
    return ContratoItemRecord(**contrato_item_fields(row))


def map_fornecedor_row(row: dict[str, Any]) -> FornecedorRecord:
    """Map one supplier row."""
    return FornecedorRecord(**fornecedor_fields(row))


def map_indicador_consolidado_row(row: dict[str, Any]) -> IndicadorConsolidadoRecord:
    """Map one consolidated indicator row."""
    return IndicadorConsolidadoRecord(**indicador_consolidado_fields(row))


def map_indicador_periodo_row(row: dict[str, Any]) -> IndicadorPeriodoRecord:
    """Map one period indicator row."""
    return IndicadorPeriodoRecord(**indicador_periodo_fields(row))


def map_ocds_release_row(row: dict[str, Any]) -> OcdsReleaseRecord:
    """Map one OCDS release."""
    return OcdsReleaseRecord(**ocds_release_fields(row))


def map_alice_aviso_row(row: dict[str, Any]) -> AliceAvisoRecord:
    """Map one Alice restricted-notice analysis."""
    return AliceAvisoRecord(**alice_aviso_fields(row))
