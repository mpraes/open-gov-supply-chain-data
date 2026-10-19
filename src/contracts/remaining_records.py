"""Linhas de catálogo de contratação, ARP, contrato, fornecedor, indicadores, OCDS e Alice."""

from contracts.catalog_row import CatalogRow


class ContratacaoRecord(CatalogRow):
    """Cabeçalho de contratação da Lei 14.133 de consultarContratacoes_PNCP_14133."""

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
    """Item de contratação da Lei 14.133 de consultarItensContratacoes_PNCP_14133."""

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
    """Resultado de item da Lei 14.133 de consultarResultadoItensContratacoes."""

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
    """Cabeçalho de ata de registro de preço de consultarARP."""

    numero_controle_pncp_ata: str
    _float_fields = frozenset({"valor_total"})
    _name_fields = frozenset({"nome_unidade_gerenciadora", "nome_orgao", "objeto"})


class ArpItemRecord(CatalogRow):
    """Item de ata de registro de preço de consultarARPItem."""

    numero_controle_pncp_ata: str
    numero_item: str
    _float_fields = frozenset(
        {"quantidade_homologada_item", "valor_unitario", "valor_total"}
    )
    _name_fields = frozenset({"descricao_item", "nome_razao_social_fornecedor"})


class ArpUnidadeItemRecord(CatalogRow):
    """Unidade participante de um item de ARP."""

    numero_ata: str
    unidade_gerenciadora: str
    numero_item: str
    codigo_unidade: str
    _name_fields = frozenset({"descricao_item", "nome_unidade"})


class ArpEmpenhoRecord(CatalogRow):
    """Saldo de empenho de um item de ARP."""

    numero_ata: str
    unidade_gerenciadora: str
    numero_item: str
    unidade: str


class ArpAdesaoRecord(CatalogRow):
    """Adesão de um item de ARP."""

    numero_ata: str
    unidade_gerenciadora: str
    unidade_nao_participante: str


class ContratoRecord(CatalogRow):
    """Cabeçalho de contrato de consultarContratos."""

    numero_controle_pncp_contrato: str
    _float_fields = frozenset({"valor_global", "valor_parcela", "valor_acumulado"})
    _name_fields = frozenset({"nome_orgao", "objeto", "nome_razao_social_fornecedor"})


class ContratoItemRecord(CatalogRow):
    """Item de contrato de consultarContratosItem."""

    numero_controle_pncp_contrato: str
    numero_item: str
    _float_fields = frozenset({"quantidade_item", "valor_unitario_item", "valor_total_item"})
    _name_fields = frozenset({"descricao_iitem", "nome_orgao"})


class FornecedorRecord(CatalogRow):
    """Fornecedor de consultarFornecedor."""

    ni_fornecedor: str
    _name_fields = frozenset({"nome_razao_social_fornecedor", "nome_municipio", "uf_sigla"})


class IndicadorConsolidadoRecord(CatalogRow):
    """Totais de uso da API de consultarIndicadoresConsolidados."""

    ano_mes_inicio: str
    ano_mes_fim: str


class IndicadorPeriodoRecord(CatalogRow):
    """Uso da API por período de consultarIndicadoresPorPeriodo."""

    ano_mes: str


class OcdsReleaseRecord(CatalogRow):
    """Release OCDS achatado de /modulo-ocds/1_releases."""

    ocid: str
    id: str
    _name_fields = frozenset({"buyer_name", "tender_title"})


class AliceAvisoRecord(CatalogRow):
    """Análise de aviso restrito do Alice em /alice/avisos-restritos."""

    ticket_analise: str
    _name_fields = frozenset({"descricao_status_analise", "chave_compra"})
