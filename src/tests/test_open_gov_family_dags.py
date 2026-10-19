from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo
import sys

import pytest

DAGS_DIR = Path(__file__).resolve().parents[2] / "dags"
sys.path.insert(0, str(DAGS_DIR))

from open_gov_catalog import (
    ARP_STEPS,
    CATMAT_READY,
    CATMAT_STEPS,
    CATSER_READY,
    CATSER_STEPS,
    MATERIAL_CLASS_READY,
    SERVICO_GRUPO_READY,
    UASG_ORGAO_READY,
    upstream_of,
)
from open_gov_schedule import every_two_days_at

FACTORY = DAGS_DIR / "open_gov_ingest.py"


def test_factory_serializes_ingest_on_one_slot_pool() -> None:
    src = FACTORY.read_text(encoding="utf-8")
    assert "from airflow.sdk import dag, task" in src or "from airflow.sdk import Asset, dag, task" in src
    assert 'API_POOL = "open_gov_compras_api"' in src
    assert "airflow.models.pool" not in src
    assert "create_or_update_pool" not in src
    assert "pool=API_POOL" in src
    assert "run_named_ingest" in src
    assert "max_active_tasks=1" in src


def test_catmat_follows_documented_load_order() -> None:
    parents = upstream_of(CATMAT_STEPS)
    assert parents["ingest_material_class"] == ("ingest_material_group",)
    assert parents["ingest_material_pdm"] == ("ingest_material_class",)
    assert parents["ingest_material_item"] == ("ingest_material_pdm",)
    assert parents["ingest_material_caracteristica"] == ("ingest_material_item",)
    assert parents["ingest_material_natureza_despesa"] == ("ingest_material_pdm",)


def test_catser_follows_documented_load_order() -> None:
    parents = upstream_of(CATSER_STEPS)
    assert parents["ingest_servico_divisao"] == ("ingest_servico_secao",)
    assert parents["ingest_servico_grupo"] == ("ingest_servico_divisao",)
    assert parents["ingest_servico_item"] == ("ingest_servico_subclasse",)
    assert parents["ingest_servico_unidade_medida"] == ("ingest_servico_item",)


def test_arp_children_wait_for_the_parent_table() -> None:
    parents = upstream_of(ARP_STEPS)
    assert parents["ingest_arp_empenho"] == ("ingest_arp",)
    assert parents["ingest_arp_item"] == ("ingest_arp",)
    assert parents["ingest_arp_unidade_item"] == ("ingest_arp_item",)
    assert parents["ingest_arp_adesao"] == ("ingest_arp_item",)


def test_precos_start_after_both_catalogs() -> None:
    src = (DAGS_DIR / "open_gov_precos.py").read_text(encoding="utf-8")
    assert "CATMAT_READY" in src
    assert "CATSER_READY" in src
    assert CATMAT_READY == "open_gov/catmat"
    assert CATSER_READY == "open_gov/catser"
    assert "paused=False" in src


def test_pgc_catalogo_starts_after_class_and_grupo() -> None:
    src = (DAGS_DIR / "open_gov_pgc_catalogo.py").read_text(encoding="utf-8")
    assert "MATERIAL_CLASS_READY" in src
    assert "SERVICO_GRUPO_READY" in src
    assert MATERIAL_CLASS_READY == "open_gov/material_class"
    assert SERVICO_GRUPO_READY == "open_gov/servico_grupo"


def test_orgao_readers_start_after_uasg_orgao() -> None:
    for name in ("open_gov_pgc.py", "open_gov_contratos.py", "open_gov_ocds.py"):
        src = (DAGS_DIR / name).read_text(encoding="utf-8")
        assert "UASG_ORGAO_READY" in src
    assert UASG_ORGAO_READY == "open_gov/uasg_orgao"


@pytest.mark.parametrize(
    "filename",
    [
        "open_gov_catmat.py",
        "open_gov_catser.py",
        "open_gov_precos.py",
        "open_gov_uasg.py",
        "open_gov_pgc.py",
        "open_gov_pgc_catalogo.py",
        "open_gov_arp.py",
        "open_gov_contratos.py",
        "open_gov_contratacoes.py",
        "open_gov_legado.py",
        "open_gov_ocds.py",
        "open_gov_indicadores.py",
        "open_gov_alice.py",
        "open_gov_fornecedor.py",
    ],
)
def test_family_file_is_discovered_by_airflow(filename: str) -> None:
    src = (DAGS_DIR / filename).read_text(encoding="utf-8")
    assert "airflow" in src.lower()
    assert "register_family_dag" in src
    assert "sys.path.insert(0, str(Path(__file__).resolve().parent))" in src


def test_catmat_and_catser_keep_separate_two_day_schedules() -> None:
    catmat = (DAGS_DIR / "open_gov_catmat.py").read_text(encoding="utf-8")
    catser = (DAGS_DIR / "open_gov_catser.py").read_text(encoding="utf-8")
    assert 'every_two_days_at(8, 0, days="even")' in catmat
    assert "every_two_days_at(8, 0)" in catser
    assert 'days="even"' not in catser
    assert "paused=False" in catmat
    assert "paused=False" in catser


def test_every_two_days_at_builds_sao_paulo_cron() -> None:
    cron, start = every_two_days_at(8, 15)
    assert cron == "15 8 */2 * *"
    assert start == datetime(2026, 9, 27, 8, 15, tzinfo=ZoneInfo("America/Sao_Paulo"))


def test_every_two_days_at_rejects_invalid_clock() -> None:
    with pytest.raises(ValueError, match=r"got hour=24 minute=0"):
        every_two_days_at(24, 0)


def test_every_two_days_at_even_uses_even_dom() -> None:
    cron, start = every_two_days_at(8, 0, days="even")
    assert cron == "0 8 2-30/2 * *"
    assert start == datetime(2026, 9, 27, 8, 0, tzinfo=ZoneInfo("America/Sao_Paulo"))


def test_every_two_days_at_rejects_unknown_days() -> None:
    with pytest.raises(ValueError, match=r"got 'weekly'"):
        every_two_days_at(8, 0, days="weekly")
