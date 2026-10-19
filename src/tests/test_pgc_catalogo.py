from datetime import date

import pytest

from etl.ingestion.planejamento.pgc_detalhe_catalogo import (
    _catalogo_dest_column,
    pgc_catalogo_years,
)


def test_catalogo_dest_column_maps_material_and_servico() -> None:
    assert _catalogo_dest_column("Material") == "codigo_classe_material"
    assert _catalogo_dest_column("Servico") == "codigo_grupo_servico"


def test_pgc_catalogo_years_start_when_the_api_has_rows() -> None:
    assert pgc_catalogo_years(today=date(2026, 10, 19)) == (2022, 2023, 2024, 2025, 2026)


def test_pgc_catalogo_years_empty_before_first_pca_year() -> None:
    assert pgc_catalogo_years(today=date(2021, 12, 31)) == ()


def test_catalogo_dest_column_rejects_unknown_tipo() -> None:
    with pytest.raises(ValueError, match="tipo expected Material or Servico"):
        _catalogo_dest_column("Outro")
