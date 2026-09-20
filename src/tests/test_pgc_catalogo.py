import pytest

from etl.ingestion.planejamento.pgc_detalhe_catalogo import _catalogo_dest_column


def test_catalogo_dest_column_maps_material_and_servico() -> None:
    assert _catalogo_dest_column("Material") == "codigo_classe_material"
    assert _catalogo_dest_column("Servico") == "codigo_grupo_servico"


def test_catalogo_dest_column_rejects_unknown_tipo() -> None:
    with pytest.raises(ValueError, match="tipo expected Material or Servico"):
        _catalogo_dest_column("Outro")
