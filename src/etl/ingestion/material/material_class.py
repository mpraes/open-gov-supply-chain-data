from typing import Any

from contracts.material_class import MaterialClassRecord
from etl.ingestion.script_runner import run_script_ingestion

ENDPOINT_PATH = "/modulo-material/2_consultarClasseMaterial"

# Class endpoint has no tamanhoPagina param in the API docs.
PAGE_SIZE: int | None = None

UPSERT_SQL = """
INSERT INTO material_class (
    cod_classe, cod_grupo, nome_grupo, nome_classe, status_classe, data_hora_atualizacao
)
VALUES (
    %(cod_classe)s, %(cod_grupo)s, %(nome_grupo)s, %(nome_classe)s,
    %(status_classe)s, %(data_hora_atualizacao)s
)
ON CONFLICT (cod_classe) DO UPDATE SET
cod_grupo = EXCLUDED.cod_grupo,
nome_grupo = EXCLUDED.nome_grupo,
nome_classe = EXCLUDED.nome_classe,
status_classe = EXCLUDED.status_classe,
data_hora_atualizacao = EXCLUDED.data_hora_atualizacao,
data_hora_carga = now();
"""


def map_material_class_row(row: dict[str, Any]) -> MaterialClassRecord:
    """Map one API resultado object to MaterialClassRecord.

    Example:
        record = map_material_class_row({"codigoClasse": 1, "codigoGrupo": 2, ...})
    """
    return MaterialClassRecord(
        cod_classe=row["codigoClasse"],
        cod_grupo=row["codigoGrupo"],
        nome_grupo=row["nomeGrupo"],
        nome_classe=row["nomeClasse"],
        status_classe=row["statusClasse"],
        data_hora_atualizacao=row["dataHoraAtualizacao"],
    )


def main() -> None:
    run_script_ingestion(
        logger_name="material_class",
        endpoint_path=ENDPOINT_PATH,
        page_size=PAGE_SIZE,
        upsert_sql=UPSERT_SQL,
        map_row=map_material_class_row,
        table_name="material_class",
    )


if __name__ == "__main__":
    main()
