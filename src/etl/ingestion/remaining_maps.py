"""Monta os registros das tabelas restantes a partir dos campos já mapeados."""

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
    """Mapeia um cabeçalho de contratação do PNCP."""
    return ContratacaoRecord(**contratacao_fields(row))


def map_contratacao_item_row(row: dict[str, Any]) -> ContratacaoItemRecord:
    """Mapeia um item de contratação do PNCP."""
    return ContratacaoItemRecord(**contratacao_item_fields(row))


def map_contratacao_resultado_row(row: dict[str, Any]) -> ContratacaoResultadoRecord:
    """Mapeia um resultado de item do PNCP."""
    return ContratacaoResultadoRecord(**contratacao_resultado_fields(row))


def map_arp_row(row: dict[str, Any]) -> ArpRecord:
    """Mapeia um cabeçalho de ARP."""
    return ArpRecord(**arp_fields(row))


def map_arp_item_row(row: dict[str, Any]) -> ArpItemRecord:
    """Mapeia um item de ARP."""
    return ArpItemRecord(**arp_item_fields(row))


def map_arp_unidade_row(row: dict[str, Any]) -> ArpUnidadeItemRecord:
    """Mapeia uma unidade participante de ARP."""
    return ArpUnidadeItemRecord(**arp_unidade_fields(row))


def map_arp_empenho_row(
    row: dict[str, Any],
    *,
    numero_ata: str,
    unidade_gerenciadora: str,
) -> ArpEmpenhoRecord:
    """Mapeia uma linha de empenho de ARP com as chaves da ATA vindas do filtro."""
    return ArpEmpenhoRecord(
        **arp_empenho_fields(
            row, numero_ata=numero_ata, unidade_gerenciadora=unidade_gerenciadora
        )
    )


def map_arp_adesao_row(row: dict[str, Any]) -> ArpAdesaoRecord:
    """Mapeia uma linha de adesão de ARP."""
    return ArpAdesaoRecord(**arp_adesao_fields(row))


def map_contrato_row(row: dict[str, Any]) -> ContratoRecord:
    """Mapeia um cabeçalho de contrato."""
    return ContratoRecord(**contrato_fields(row))


def map_contrato_item_row(row: dict[str, Any]) -> ContratoItemRecord:
    """Mapeia um item de contrato."""
    return ContratoItemRecord(**contrato_item_fields(row))


def map_fornecedor_row(row: dict[str, Any]) -> FornecedorRecord:
    """Mapeia uma linha de fornecedor."""
    return FornecedorRecord(**fornecedor_fields(row))


def map_indicador_consolidado_row(row: dict[str, Any]) -> IndicadorConsolidadoRecord:
    """Mapeia uma linha de indicador consolidado."""
    return IndicadorConsolidadoRecord(**indicador_consolidado_fields(row))


def map_indicador_periodo_row(row: dict[str, Any]) -> IndicadorPeriodoRecord:
    """Mapeia uma linha de indicador por período."""
    return IndicadorPeriodoRecord(**indicador_periodo_fields(row))


def map_ocds_release_row(row: dict[str, Any]) -> OcdsReleaseRecord:
    """Mapeia um release OCDS."""
    return OcdsReleaseRecord(**ocds_release_fields(row))


def map_alice_aviso_row(row: dict[str, Any]) -> AliceAvisoRecord:
    """Mapeia uma análise de aviso restrito do Alice."""
    return AliceAvisoRecord(**alice_aviso_fields(row))
