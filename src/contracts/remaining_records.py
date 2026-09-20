from contracts.catalog_row import CatalogRow


class ContratacaoRecord(CatalogRow):
    """Lei 14.133 contracting header from consultarContratacoes_PNCP_14133."""

    id_compra: str
    _float_fields = frozenset({"valor_total_estimado", "valor_total_homologado"})
    _name_fields = frozenset(
        {
            "orgao_entidade_razao_social",
            "modalidade_nome",
            "objeto_compra",
            "amparo_legal_nome",
        }
    )


class ContratacaoItemRecord(CatalogRow):
    """Lei 14.133 contracting item from consultarItensContratacoes_PNCP_14133."""

    id_compra: str
    id_compra_item: str
    _float_fields = frozenset(
        {
            "quantidade",
            "valor_unitario_estimado",
            "valor_total",
            "quantidade_resultado",
            "valor_unitario_resultado",
            "valor_total_resultado",
        }
    )
    _name_fields = frozenset({"descricao_resumida", "nome_fornecedor", "nome_pdm"})


class ContratacaoResultadoRecord(CatalogRow):
    """Lei 14.133 item result from consultarResultadoItensContratacoes."""

    id_compra: str
    id_compra_item: str
    sequencial_resultado: str
    _float_fields = frozenset(
        {
            "quantidade_homologada",
            "valor_unitario_homologado",
            "valor_total_homologado",
            "percentual_desconto",
        }
    )
    _name_fields = frozenset({"nome_razao_social_fornecedor"})


class ArpRecord(CatalogRow):
    """Price-registration header from consultarARP."""

    numero_controle_pncp_ata: str
    _float_fields = frozenset({"valor_total"})
    _name_fields = frozenset({"nome_unidade_gerenciadora", "nome_orgao", "objeto"})


class ArpItemRecord(CatalogRow):
    """Price-registration item from consultarARPItem."""

    numero_controle_pncp_ata: str
    numero_item: str
    _float_fields = frozenset(
        {"quantidade_homologada_item", "valor_unitario", "valor_total"}
    )
    _name_fields = frozenset({"descricao_item", "nome_razao_social_fornecedor"})


class ArpUnidadeItemRecord(CatalogRow):
    """Participating unit of an ARP item."""

    numero_ata: str
    unidade_gerenciadora: str
    numero_item: str
    codigo_unidade: str
    _name_fields = frozenset({"descricao_item", "nome_unidade"})


class ArpEmpenhoRecord(CatalogRow):
    """ARP item commitment balance."""

    numero_ata: str
    unidade_gerenciadora: str
    numero_item: str
    unidade: str


class ArpAdesaoRecord(CatalogRow):
    """ARP item accession."""

    numero_ata: str
    unidade_gerenciadora: str
    unidade_nao_participante: str


class ContratoRecord(CatalogRow):
    """Contract header from consultarContratos."""

    numero_controle_pncp_contrato: str
    _float_fields = frozenset({"valor_global", "valor_parcela", "valor_acumulado"})
    _name_fields = frozenset({"nome_orgao", "objeto", "nome_razao_social_fornecedor"})


class ContratoItemRecord(CatalogRow):
    """Contract item from consultarContratosItem."""

    numero_controle_pncp_contrato: str
    numero_item: str
    _float_fields = frozenset({"quantidade_item", "valor_unitario_item", "valor_total_item"})
    _name_fields = frozenset({"descricao_iitem", "nome_orgao"})


class FornecedorRecord(CatalogRow):
    """Supplier from consultarFornecedor."""

    ni_fornecedor: str
    _name_fields = frozenset({"nome_razao_social_fornecedor", "nome_municipio", "uf_sigla"})


class IndicadorConsolidadoRecord(CatalogRow):
    """API usage totals from consultarIndicadoresConsolidados."""

    ano_mes_inicio: str
    ano_mes_fim: str


class IndicadorPeriodoRecord(CatalogRow):
    """API usage by period from consultarIndicadoresPorPeriodo."""

    ano_mes: str


class OcdsReleaseRecord(CatalogRow):
    """Flattened OCDS release from /modulo-ocds/1_releases."""

    ocid: str
    id: str
    _name_fields = frozenset({"buyer_name", "tender_title"})


class AliceAvisoRecord(CatalogRow):
    """Alice restricted-notice analysis from /alice/avisos-restritos."""

    ticket_analise: str
    _name_fields = frozenset({"descricao_status_analise", "chave_compra"})
