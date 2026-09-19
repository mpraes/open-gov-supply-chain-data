_ALLOWED_TABLES = frozenset({"pgc_detalhe", "pgc_detalhe_catalogo"})

PGC_DETALHE_COLUMNS = (
    "codigo_uasg",
    "nome_uasg",
    "orgao",
    "numero_artefato",
    "ano_artefato",
    "codigo_estado_artefato",
    "codigo_categoria_artefato",
    "descricao_artefato",
    "codigo_tipo_artefato",
    "ordem_dfd",
    "descricao_objeto_dfd",
    "nivel_prioridade_dfd",
    "data_prevista_formalizacao_demanda",
    "codigo_area_dfd",
    "tipo_item",
    "item_sustentavel",
    "codigo_grupo_material",
    "nome_grupo_material",
    "codigo_classe_material",
    "nome_classe_material",
    "codigo_pdm_material",
    "nome_pdm_material",
    "codigo_secao_servico",
    "nome_secao_servico",
    "codigo_divisao_servico",
    "nome_divisao_servico",
    "codigo_grupo_servico",
    "nome_grupo_servico",
    "codigo_classe_servico",
    "nome_classe_servico",
    "codigo_subclasse_servico",
    "nome_subclasse_servico",
    "codigo_item_catalogo",
    "descricao_item_catalogo",
    "sigla_unidade_fornecimento",
    "nome_unidade_fornecimento",
    "quantidade_item",
    "valor_unitario_item",
    "valor_total_item",
    "titulo_projeto_compra",
    "descricao_projeto_compra",
    "ano_pca_projeto_compra",
    "data_inicio_processo_compra",
    "data_fim_processo_compra",
    "duracao_processo_compra",
    "numero_item_pncp",
    "status_contratacao_execucao",
    "data_hora_publicacao_pncp",
    "data_hora_atualizacao_artefato",
    "data_hora_atualizacao_projeto_compra",
    "data_hora_atualizacao_dfd",
    "data_hora_atualizacao_item",
)

_CONFLICT_COLUMNS = (
    "codigo_uasg",
    "numero_artefato",
    "ano_artefato",
    "ordem_dfd",
    "codigo_item_catalogo",
    "ano_pca_projeto_compra",
)


def pgc_detalhe_upsert_sql(table_name: str) -> str:
    """Build the upsert statement for a PGC detalhe table.

    Example:
        sql = pgc_detalhe_upsert_sql("pgc_detalhe")
    """
    if table_name not in _ALLOWED_TABLES:
        raise ValueError(
            f"table expected pgc_detalhe or pgc_detalhe_catalogo, got {table_name!r}"
        )
    return _build_upsert_sql(table_name)


def _build_upsert_sql(table_name: str) -> str:
    cols = ", ".join(PGC_DETALHE_COLUMNS)
    values = ", ".join(f"%({name})s" for name in PGC_DETALHE_COLUMNS)
    conflict = ", ".join(_CONFLICT_COLUMNS)
    updates = _excluded_updates()
    return (
        f"INSERT INTO {table_name} ({cols})\n"
        f"VALUES ({values})\n"
        f"ON CONFLICT ({conflict}) DO UPDATE SET\n"
        f"{updates},\n"
        "data_hora_carga = now();"
    )


def _excluded_updates() -> str:
    names = [name for name in PGC_DETALHE_COLUMNS if name not in _CONFLICT_COLUMNS]
    return ",\n".join(f"{name} = EXCLUDED.{name}" for name in names)
