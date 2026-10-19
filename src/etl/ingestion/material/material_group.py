"""Ingere grupos de material na tabela material_group."""

from typing import Any

from contracts.material_group import MaterialGroupRecord
from etl.ingestion.dest_schema import dest_table
from etl.ingestion.page_runner import run_page_batch_ingestion

ENDPOINT_PATH = "/modulo-material/1_consultarGrupoMaterial"

# O endpoint de grupo não documenta o parâmetro tamanhoPagina.
PAGE_SIZE: int | None = None

UPSERT_SQL = f"""
INSERT INTO {dest_table("material_group")} (cod_grupo, nome_grupo, status_grupo, data_hora_atualizacao)
VALUES (%(cod_grupo)s, %(nome_grupo)s, %(status_grupo)s, %(data_hora_atualizacao)s)
ON CONFLICT (cod_grupo) DO UPDATE SET
nome_grupo = EXCLUDED.nome_grupo,
status_grupo = EXCLUDED.status_grupo,
data_hora_atualizacao = EXCLUDED.data_hora_atualizacao,
data_hora_carga = now();
"""


def map_material_group_row(row: dict[str, Any]) -> MaterialGroupRecord:
    """Mapeia um objeto resultado da API para MaterialGroupRecord.

    Exemplo:
        record = map_material_group_row({"codigoGrupo": 1, "nomeGrupo": "x", ...})
    """
    return MaterialGroupRecord(
        cod_grupo=row["codigoGrupo"],
        nome_grupo=row["nomeGrupo"],
        status_grupo=row["statusGrupo"],
        data_hora_atualizacao=row["dataHoraAtualizacao"],
    )


def main() -> None:
    """Consulta /modulo-material/1_consultarGrupoMaterial e grava o resultado na tabela material_group."""
    run_page_batch_ingestion(
        logger_name="material_group",
        endpoint_path=ENDPOINT_PATH,
        page_size=PAGE_SIZE,
        upsert_sql=UPSERT_SQL,
        map_row=map_material_group_row,
        table_name="material_group",
    )


if __name__ == "__main__":
    main()
