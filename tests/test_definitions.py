"""Guards for plan v3 (docs/PLAN_v3.md): one outcome, one zone registry, one treatment.

Run: uv run pytest -q   (after uv run python code/main.py)
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[1]
CODE = ROOT / "code"
sys.path.insert(0, str(CODE))

# Modules allowed to read the publisher's statistics workbook for buffer zones: course checks and the reconciliation.
WORKBOOK_OK = {"checks.py", "raster_zones.py", "common.py", "definitions.py"}   # loader, docstring, checks, reconciliation
MODULES = sorted(p for p in CODE.glob("*.py"))


def src(p: Path) -> str:
    return p.read_text(encoding="utf-8")


@pytest.mark.parametrize("p", MODULES, ids=lambda p: p.name)
def test_no_workbook_zones(p):
    """Zone designs read zones only through zonedata.py, never the buffer-zone workbook."""
    if p.name in WORKBOOK_OK:
        return
    s = src(p)
    assert 'pack["zb"]' not in s and "pack['zb']" not in s and "peru_bufferzone_year" not in s, \
        f"{p.name} reads the statistics workbook; use zonedata.bz_panel() / region_units()"


@pytest.mark.parametrize("p", MODULES, ids=lambda p: p.name)
def test_no_v2_intermediates(p):
    s = src(p)
    hits = re.findall(r"(zone_year_v2|official_unit_year_v2|cell_year_v2|cell_attr_v2|road_band_year_v2|zones_v2_\w+)", s)
    assert not hits, f"{p.name} reads superseded v2 zone files: {sorted(set(hits))}"


@pytest.mark.parametrize("p", MODULES, ids=lambda p: p.name)
def test_no_private_windows(p):
    """Treatment windows come from definitions.PERIODS; no module hard-codes a 2019-21 window or 2018 reference."""
    if p.name in {"definitions.py", "checks.py"}:
        return
    s = src(p)
    bad = re.findall(r"between\(\s*2019\s*,\s*2021\s*\)|range\(\s*2019\s*,\s*2022\s*\)|\(\s*2019\s*,\s*2021\s*\)|\(\s*2016\s*,\s*2018\s*\)|\(\s*2022\s*,\s*2025\s*\)|loc\[2019:2021\]|!= 2018", s)
    assert not bad, f"{p.name} hard-codes treatment windows {sorted(set(bad))}; use definitions.PERIODS / REF_YEAR"


def test_identity_and_registry():
    z = pd.read_csv(ROOT / "data_intermediate/zone_year.csv")
    import definitions as D
    assert set(z.zone) <= set(D.ZONES)
    g = z.sort_values("year").groupby(["zone", "tenure", "in_mdd"])
    resid = (g.mining_ha.diff() - z.sort_values("year").net_ha).abs().max()
    assert resid < 1e-3


def test_focal_zones_equal_publisher_area():
    """Tambopata BZ raster stock tracks the publisher's workbook closely (same product, same polygon)."""
    r = pd.read_csv(ROOT / "data_intermediate/bz_reconciliation.csv")
    t = r[(r.bz_code == "RN09") & (r.year == 2025)].iloc[0]
    assert abs(t.diff_ha) / t.mining_ha_workbook < 0.01


def test_numbers_in_ha_name_measure_zone_period():
    n = pd.read_csv(ROOT / "output/numbers.csv").fillna("")
    ha = n[n.unit.str.startswith("ha") & n.produced_by.ne("")]
    missing = ha[(ha.measure == "") | (ha.zone == "") | (ha.period == "")]
    assert missing.empty, f"{len(missing)} numbers in ha lack measure/zone/period, e.g. {missing.id.head(10).tolist()}"


@pytest.mark.parametrize("page", ["docs/brief/brief_content.md", "docs/walkthrough/explainer_content.md",
                                  "docs/walkthrough/methods_content.md"])
def test_page_placeholders_exist(page):
    """Every {{id}} in a page source exists in output/numbers.csv (referee 2: pages could not be built)."""
    ids = set(pd.read_csv(ROOT / "output/numbers.csv").id)
    text = re.sub(r"<!--.*?-->", "", (ROOT / page).read_text(encoding="utf-8"), flags=re.S)   # header comments
    used = set(re.findall(r"\{\{\s*([A-Za-z0-9_]+)(?::[^}]*)?\s*\}\}", text)) - {"TEXT"}
    used = {u for u in used if not u.isupper()}                     # page-level TEXT blocks (e.g. DECISIONS_TABLE)
    missing = sorted(used - ids)
    assert not missing, f"{page}: {len(missing)} unknown ids, e.g. {missing[:10]}"


def test_deck_ids_exist():
    js = ROOT / "presentation/deck/build_deck.js"
    if not js.exists():
        pytest.skip("no deck")
    ids = set(pd.read_csv(ROOT / "output/numbers.csv").id)
    used = set(re.findall(r"""need\(\s*['"`]([a-z0-9_]+)['"`]""", js.read_text(encoding="utf-8")))
    missing = sorted(used - ids)
    assert not missing, f"build_deck.js uses unknown ids: {missing[:10]}"
