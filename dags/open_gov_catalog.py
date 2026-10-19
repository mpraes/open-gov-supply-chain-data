from dataclasses import dataclass


CATMAT_READY = "open_gov/catmat"
CATSER_READY = "open_gov/catser"
MATERIAL_CLASS_READY = "open_gov/material_class"
SERVICO_GRUPO_READY = "open_gov/servico_grupo"
UASG_ORGAO_READY = "open_gov/uasg_orgao"


@dataclass(frozen=True)
class IngestStep:
    task_id: str
    module_path: str
    upstream: tuple[str, ...] = ()
    outlet: str | None = None


def upstream_of(steps: tuple[IngestStep, ...]) -> dict[str, tuple[str, ...]]:
    """Map each task id to the tasks that must finish first.

    Example:
        upstream_of(CATMAT_STEPS)["ingest_material_class"]
    """
    return {step.task_id: step.upstream for step in steps}


CATMAT_STEPS: tuple[IngestStep, ...] = (
    IngestStep("ingest_material_group", "etl.ingestion.material.material_group"),
    IngestStep(
        "ingest_material_class",
        "etl.ingestion.material.material_class",
        upstream=("ingest_material_group",),
        outlet=MATERIAL_CLASS_READY,
    ),
    IngestStep(
        "ingest_material_pdm",
        "etl.ingestion.material.material_pdm",
        upstream=("ingest_material_class",),
    ),
    IngestStep(
        "ingest_material_item",
        "etl.ingestion.material.material_item",
        upstream=("ingest_material_pdm",),
    ),
    IngestStep(
        "ingest_material_natureza_despesa",
        "etl.ingestion.material.material_natureza_despesa",
        upstream=("ingest_material_pdm",),
    ),
    IngestStep(
        "ingest_material_unidade_fornecimento",
        "etl.ingestion.material.material_unidade_fornecimento",
        upstream=("ingest_material_pdm",),
    ),
    IngestStep(
        "ingest_material_caracteristica",
        "etl.ingestion.material.material_caracteristica",
        upstream=("ingest_material_item",),
    ),
)

CATSER_STEPS: tuple[IngestStep, ...] = (
    IngestStep("ingest_servico_secao", "etl.ingestion.servico.servico_secao"),
    IngestStep(
        "ingest_servico_divisao",
        "etl.ingestion.servico.servico_divisao",
        upstream=("ingest_servico_secao",),
    ),
    IngestStep(
        "ingest_servico_grupo",
        "etl.ingestion.servico.servico_grupo",
        upstream=("ingest_servico_divisao",),
        outlet=SERVICO_GRUPO_READY,
    ),
    IngestStep(
        "ingest_servico_classe",
        "etl.ingestion.servico.servico_classe",
        upstream=("ingest_servico_grupo",),
    ),
    IngestStep(
        "ingest_servico_subclasse",
        "etl.ingestion.servico.servico_subclasse",
        upstream=("ingest_servico_classe",),
    ),
    IngestStep(
        "ingest_servico_item",
        "etl.ingestion.servico.servico_item",
        upstream=("ingest_servico_subclasse",),
    ),
    IngestStep(
        "ingest_servico_unidade_medida",
        "etl.ingestion.servico.servico_unidade_medida",
        upstream=("ingest_servico_item",),
    ),
    IngestStep(
        "ingest_servico_natureza_despesa",
        "etl.ingestion.servico.servico_natureza_despesa",
        upstream=("ingest_servico_item",),
    ),
)

PRECO_STEPS: tuple[IngestStep, ...] = (
    IngestStep("ingest_preco_material", "etl.ingestion.precos.preco_material"),
    IngestStep(
        "ingest_preco_material_detalhe",
        "etl.ingestion.precos.preco_material_detalhe",
        upstream=("ingest_preco_material",),
    ),
    IngestStep(
        "ingest_preco_servico",
        "etl.ingestion.precos.preco_servico",
        upstream=("ingest_preco_material_detalhe",),
    ),
    IngestStep(
        "ingest_preco_servico_detalhe",
        "etl.ingestion.precos.preco_servico_detalhe",
        upstream=("ingest_preco_servico",),
    ),
)

UASG_STEPS: tuple[IngestStep, ...] = (
    IngestStep(
        "ingest_uasg_orgao",
        "etl.ingestion.uasg.uasg_orgao",
        outlet=UASG_ORGAO_READY,
    ),
    IngestStep(
        "ingest_uasg",
        "etl.ingestion.uasg.uasg",
        upstream=("ingest_uasg_orgao",),
    ),
)

PGC_STEPS: tuple[IngestStep, ...] = (
    IngestStep("ingest_pgc_detalhe", "etl.ingestion.planejamento.pgc_detalhe"),
    IngestStep(
        "ingest_pgc_agregacao",
        "etl.ingestion.planejamento.pgc_agregacao",
        upstream=("ingest_pgc_detalhe",),
    ),
)

PGC_CATALOGO_STEPS: tuple[IngestStep, ...] = (
    IngestStep(
        "ingest_pgc_detalhe_catalogo",
        "etl.ingestion.planejamento.pgc_detalhe_catalogo",
    ),
)

ARP_STEPS: tuple[IngestStep, ...] = (
    IngestStep("ingest_arp", "etl.ingestion.arp.arp"),
    IngestStep(
        "ingest_arp_fim_vigencia",
        "etl.ingestion.arp.arp_fim_vigencia",
        upstream=("ingest_arp",),
    ),
    IngestStep(
        "ingest_arp_item",
        "etl.ingestion.arp.arp_item",
        upstream=("ingest_arp",),
    ),
    IngestStep(
        "ingest_arp_empenho",
        "etl.ingestion.arp.arp_empenho",
        upstream=("ingest_arp",),
    ),
    IngestStep(
        "ingest_arp_unidade_item",
        "etl.ingestion.arp.arp_unidade_item",
        upstream=("ingest_arp_item",),
    ),
    IngestStep(
        "ingest_arp_adesao",
        "etl.ingestion.arp.arp_adesao",
        upstream=("ingest_arp_item",),
    ),
)

CONTRATO_STEPS: tuple[IngestStep, ...] = (
    IngestStep("ingest_contrato", "etl.ingestion.contratos.contrato"),
    IngestStep(
        "ingest_contrato_item",
        "etl.ingestion.contratos.contrato_item",
        upstream=("ingest_contrato",),
    ),
    IngestStep(
        "ingest_contrato_fim_vigencia",
        "etl.ingestion.contratos.contrato_fim_vigencia",
        upstream=("ingest_contrato",),
    ),
)

CONTRATACAO_STEPS: tuple[IngestStep, ...] = (
    IngestStep("ingest_contratacao", "etl.ingestion.contratacoes.contratacao"),
    IngestStep(
        "ingest_contratacao_item",
        "etl.ingestion.contratacoes.contratacao_item",
        upstream=("ingest_contratacao",),
    ),
    IngestStep(
        "ingest_contratacao_resultado",
        "etl.ingestion.contratacoes.contratacao_resultado",
        upstream=("ingest_contratacao",),
    ),
)

LEGADO_STEPS: tuple[IngestStep, ...] = (
    IngestStep("ingest_legado_licitacao", "etl.ingestion.legado.legado_licitacao"),
    IngestStep(
        "ingest_legado_item_licitacao",
        "etl.ingestion.legado.legado_item_licitacao",
        upstream=("ingest_legado_licitacao",),
    ),
    IngestStep(
        "ingest_legado_pregao",
        "etl.ingestion.legado.legado_pregao",
        upstream=("ingest_legado_item_licitacao",),
    ),
    IngestStep(
        "ingest_legado_item_pregao",
        "etl.ingestion.legado.legado_item_pregao",
        upstream=("ingest_legado_pregao",),
    ),
    IngestStep(
        "ingest_legado_compra_sem_licitacao",
        "etl.ingestion.legado.legado_compra_sem_licitacao",
        upstream=("ingest_legado_item_pregao",),
    ),
    IngestStep(
        "ingest_legado_item_sem_licitacao",
        "etl.ingestion.legado.legado_item_sem_licitacao",
        upstream=("ingest_legado_compra_sem_licitacao",),
    ),
    IngestStep(
        "ingest_legado_rdc",
        "etl.ingestion.legado.legado_rdc",
        upstream=("ingest_legado_item_sem_licitacao",),
    ),
)

OCDS_STEPS: tuple[IngestStep, ...] = (
    IngestStep("ingest_ocds_release", "etl.ingestion.ocds.ocds_release"),
)

INDICADOR_STEPS: tuple[IngestStep, ...] = (
    IngestStep(
        "ingest_indicador_consolidado",
        "etl.ingestion.indicadores.indicador_consolidado",
    ),
    IngestStep(
        "ingest_indicador_periodo",
        "etl.ingestion.indicadores.indicador_periodo",
        upstream=("ingest_indicador_consolidado",),
    ),
)

ALICE_STEPS: tuple[IngestStep, ...] = (
    IngestStep("ingest_alice_aviso", "etl.ingestion.alice.alice_aviso"),
)

FORNECEDOR_STEPS: tuple[IngestStep, ...] = (
    IngestStep("ingest_fornecedor", "etl.ingestion.fornecedor.fornecedor"),
)
