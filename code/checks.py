"""Source checks. Any failure raises.

Three kinds (plan v3, docs/PLAN_v3.md):
  1. PUBLISHER checks: the starter's six checks (our number = the publisher's number).
  2. REPRODUCTION checks: the course card numbers (Tambopata 1,640 -> 163, Amarakaeri 289 -> 574, DiD -1,762 ha/yr)
     recomputed from the course statistics workbook (data/peru_bufferzone_year.csv). They show we reproduce the card;
     the ANALYSIS no longer uses the workbook (it uses the raster zone registry, zonedata.py).
  3. v3 RECONCILIATION checks: the raster zone registry (MapBiomas Peru Col 4 rasters, our pixel accounting) against
     the publisher's statistics workbook, from data_intermediate/bz_reconciliation.csv (written by raster_zones.py):
     Tambopata and Amarakaeri buffer-zone stock within 1% in every year with real mining, the card's period means
     within 2 ha/yr, and Madre de Dios 2025 within 1%.
"""
from __future__ import annotations
import pandas as pd
from common import OUT, BZ_KEY, additions, period_mean

_rows = []

def check(label: str, value: float, expected: float, tol: float = 1.0):
    """Same logic as starter/gold_starter.py check(): |value - expected| < tol, else raise."""
    ok = abs(value - expected) < tol
    print(f"{'OK  ' if ok else 'FAIL'} {label:70s} {value:>12,.0f}   (expected: {expected:,.0f})")
    _rows.append(dict(label=label, value=value, expected=expected, ok=ok))
    if not ok:
        raise AssertionError(f"{label}: got {value:,.0f}, expected {expected:,.0f}")

def check_rel(label: str, value: float, expected: float, rel: float = 0.01):
    """Relative check: |value - expected| <= rel * |expected|, else raise."""
    check(label, value, expected, tol=rel * abs(expected) + 1e-9)

def check_pending(label: str, our_value: float, note: str = "pending: platform check"):
    """Publisher-side check not yet done: recorded in checks.csv as pending (not a pass, not a failure)."""
    print(f"PEND {label:70s} {our_value:>12,.1f}   ({note})")
    _rows.append(dict(label=label, value=our_value, expected=float("nan"), ok=note))

def check_documented(label: str, value: float, expected: float, status: str):
    """Publisher-side comparison done and documented but NOT asserted (e.g. a known collection difference)."""
    print(f"{status:5.5s}{label:70s} {value:>12,.0f}   (publisher: {expected:,.0f})")
    _rows.append(dict(label=label, value=value, expected=expected, ok=status))

def save():
    """(Re)write output/checks.csv with every check recorded so far (modules call this after adding checks)."""
    pd.DataFrame(_rows).to_csv(OUT / "checks.csv", index=False)

def run_checks(pack: dict) -> None:
    pm, pe, zb, br, sub = pack["prices_m"], pack["pe"], pack["zb"], pack["br"], pack["substance"]
    print("\n== Source checks ==")
    # --- the starter's six checks (publisher numbers, see DOWNLOAD_LOG.csv)
    check("Gold price, August 2026, $ per troy ounce", pm["gold"].iloc[-1], 4411)
    check("Brazil, mining class, all municipalities, 2024, ha",
          br.loc[br["year"] == 2024, "mining_ha"].sum(), 609637)
    check("Peru, Madre de Dios, mining class, 2025, ha",
          pe.loc[(pe["department"] == "Madre de Dios") & (pe["year"] == 2025), "mining_ha"].sum(), 112622)
    check("Peru, Tambopata buffer zone, mining class, 2025, ha",
          zb.loc[(zb["buffer_zone"] == "Tambopata") & (zb["year"] == 2025), "mining_ha"].sum(), 20730)
    check("Brazil, artisanal mining (garimpo), 2025, ha",
          sub.loc[(sub["territory"] == "Brasil") & (sub["year"] == 2025), "mining_artisanal_ha"].sum(), 445987)
    check("Brazil publisher check (course card, MapBiomas Brazil Col 11): artisanal mining in all indigenous lands, 2025, ha",
          sub.loc[(sub["territory"] == "all indigenous lands combined") & (sub["year"] == 2025),
                  "mining_artisanal_ha"].sum(), 39915)

    # --- REPRODUCTION checks (course card), from the statistics workbook: mean annual additions 2016-18 -> 2019-21,
    # buffer zone summed over ALL its departments (the starter's definition). Not used by any analysis (plan v3).
    w = (zb.groupby(["buffer_zone", "pa_category", "year"], as_index=False)["mining_ha"].sum())
    a = additions(w.assign(unit=w["buffer_zone"] + "|" + w["pa_category"]), "unit")
    s = {u: g.set_index("year")["addition_ha"] for u, g in a.groupby("unit")}
    tam, ama = s["Tambopata|Reserva Nacional"], s["Amarakaeri|Reserva Comunal"]
    t0, t1 = period_mean(tam, 2016, 2018), period_mean(tam, 2019, 2021)
    a0, a1 = period_mean(ama, 2016, 2018), period_mean(ama, 2019, 2021)
    check("REPRODUCTION (course card, workbook): Tambopata mean annual addition 2016-18, ha/yr", t0, 1640, tol=1)
    check("REPRODUCTION (course card, workbook): Tambopata mean annual addition 2019-21, ha/yr", t1, 163, tol=1)
    check("REPRODUCTION (course card, workbook): Amarakaeri mean annual addition 2016-18, ha/yr", a0, 289, tol=1)
    check("REPRODUCTION (course card, workbook): Amarakaeri mean annual addition 2019-21, ha/yr", a1, 574, tol=1)
    check("REPRODUCTION (starter, workbook): hand-computed DiD (Tambopata minus Amarakaeri), ha/yr", (t1 - t0) - (a1 - a0), -1762, tol=1.5)

    # --- why does agent.md §10 show 1,638 / 284 / 540? Those are the Madre de Dios ROWS only; Amarakaeri and
    # Tambopata also have small rows in Cusco / Puno. Documented, not a check on the card.
    m = zb[zb["department"] == "Madre de Dios"]
    mm = m.groupby(BZ_KEY + ["year"], as_index=False)["mining_ha"].sum()
    mm = additions(mm.assign(unit=mm["buffer_zone"] + "|" + mm["pa_category"]), "unit")
    ms = {u: g.set_index("year")["addition_ha"] for u, g in mm.groupby("unit")}
    print(f"     (info) MdD-rows-only means: Tambopata 2016-18 {period_mean(ms['Tambopata|Reserva Nacional'],2016,2018):,.1f}, "
          f"Amarakaeri 2016-18 {period_mean(ms['Amarakaeri|Reserva Comunal'],2016,2018):,.1f} "
          f"vs all-department definition {t0:,.1f} / {a0:,.1f}")
    reconcile_v3(pe)
    save()
    print("All checks OK.")


def reconcile_v3(pe=None) -> None:
    """v3 RECONCILIATION: raster zone registry vs the publisher's statistics workbook (check, not data)."""
    from common import ROOT
    import zonedata as Z
    f = ROOT / "data_intermediate" / "bz_reconciliation.csv"
    if not f.exists():
        print("PEND v3 reconciliation: data_intermediate/bz_reconciliation.csv missing (run raster_zones.py)"); return
    print("\n== v3 reconciliation: raster registry vs statistics workbook ==")
    r = pd.read_csv(f)
    for code, name in (("RN09", "Tambopata"), ("RC03", "Amarakaeri")):
        d = r[(r.bz_code == code) & (r.mining_ha_workbook >= 100)]
        rel = (d.diff_ha.abs() / d.mining_ha_workbook)
        worst = d.loc[rel.idxmax()]
        check(f"RECONCILIATION: {name} BZ raster stock vs workbook, worst year {int(worst.year)} of {len(d)}, rel. diff <= 1% "
              "(value = max rel. diff x 100)", 100 * rel.max(), 0.0, tol=1.0)
    t = r[(r.bz_code == "RN09") & (r.year == 2025)].iloc[0]
    check_rel("RECONCILIATION: Tambopata BZ mining 2025, raster registry vs workbook (20,730 ha), ha", t.mining_ha_raster,
              t.mining_ha_workbook, 0.01)
    ru = Z.region_units()
    s = lambda u: ru[ru.unit == u].set_index("year")
    card = {("tambopata_bz", "pre"): 1640, ("tambopata_bz", "during"): 163,
            ("amarakaeri_bz", "pre"): 289, ("amarakaeri_bz", "during"): 574}
    for (u, p), v in card.items():
        check(f"RECONCILIATION: {u} net additions {p} mean, raster registry vs card {v} ha/yr (tol 2)",
              Z.period_mean(s(u).net_ha, p), v, tol=2.0)
    check_rel("RECONCILIATION: Madre de Dios mining 2025, raster registry vs department table (112,622 ha), ha",
              s("mdd").loc[2025, "mining_ha"], 112622, 0.01)

def run_new_data_checks() -> None:
    """Publisher checks for data added on 2026-10-11 (rule-based control search, Brazil). Called from main after the
    intermediates exist. MapBiomas Amazonia Col 6 is read from data_intermediate (raw xlsx is 260 MB, git-ignored)."""
    from common import ROOT
    print("\n== Source checks: new data (2026-10-11) ==")
    f = ROOT / "data_intermediate" / "mb_amazonia_col6_check.csv"
    if f.exists():
        v = pd.read_csv(f)["value"].iloc[0]
        check("MapBiomas Amazonia Col 6, mining area whole region 2023, ha (factsheet p.3: 0.78 Mha)", v, 780_000, tol=5_000)
    m = ROOT / "data_raw/mapbiomas_brazil/MAPBIOMAS-BRAZIL-MINED-SUBSTANCES-MUNICIPALITY-COLLECTION_11.xlsx"
    if m.exists():
        x = pd.read_excel(m, sheet_name="MINED_SUBSTANCE")
        g = x.loc[x["CLASS_LEVEL_1"] == "Garimpo", "y2025"].sum()
        check("MapBiomas Brazil Col 11 mining module, garimpo, all Brazil 2025, ha (platform 445,987)", g, 445_987, tol=1)
    save()
