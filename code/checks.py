"""Source checks. Re-runs the starter's 6 checks plus the Q2 card numbers. Any failure raises."""
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

def check_pending(label: str, our_value: float, note: str = "pending: platform check"):
    """Publisher-side check not yet done: recorded in checks.csv as pending (not a pass, not a failure)."""
    print(f"PEND {label:70s} {our_value:>12,.1f}   ({note})")
    _rows.append(dict(label=label, value=our_value, expected=float("nan"), ok=note))

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
    check("Brazil, artisanal mining in all indigenous lands, 2025, ha",
          sub.loc[(sub["territory"] == "all indigenous lands combined") & (sub["year"] == 2025),
                  "mining_artisanal_ha"].sum(), 39915)

    # --- Q2 card: mean annual additions 2016-18 -> 2019-21, buffer zone summed over ALL its departments
    # (the starter's definition; it reproduces the card). Rounded numbers, tolerance 0.5 ha.
    w = (zb.groupby(["buffer_zone", "pa_category", "year"], as_index=False)["mining_ha"].sum())
    a = additions(w.assign(unit=w["buffer_zone"] + "|" + w["pa_category"]), "unit")
    s = {u: g.set_index("year")["addition_ha"] for u, g in a.groupby("unit")}
    tam, ama = s["Tambopata|Reserva Nacional"], s["Amarakaeri|Reserva Comunal"]
    t0, t1 = period_mean(tam, 2016, 2018), period_mean(tam, 2019, 2021)
    a0, a1 = period_mean(ama, 2016, 2018), period_mean(ama, 2019, 2021)
    check("Card: Tambopata mean annual addition 2016-18, ha/yr", t0, 1640, tol=1)
    check("Card: Tambopata mean annual addition 2019-21, ha/yr", t1, 163, tol=1)
    check("Card: Amarakaeri mean annual addition 2016-18, ha/yr", a0, 289, tol=1)
    check("Card: Amarakaeri mean annual addition 2019-21, ha/yr", a1, 574, tol=1)
    check("Starter: hand-computed DiD (Tambopata minus Amarakaeri), ha/yr", (t1 - t0) - (a1 - a0), -1762, tol=1.5)

    # --- why does agent.md §10 show 1,638 / 284 / 540? Those are the Madre de Dios ROWS only; Amarakaeri and
    # Tambopata also have small rows in Cusco / Puno. Documented, not a check on the card.
    m = zb[zb["department"] == "Madre de Dios"]
    mm = m.groupby(BZ_KEY + ["year"], as_index=False)["mining_ha"].sum()
    mm = additions(mm.assign(unit=mm["buffer_zone"] + "|" + mm["pa_category"]), "unit")
    ms = {u: g.set_index("year")["addition_ha"] for u, g in mm.groupby("unit")}
    print(f"     (info) MdD-rows-only means: Tambopata 2016-18 {period_mean(ms['Tambopata|Reserva Nacional'],2016,2018):,.1f}, "
          f"Amarakaeri 2016-18 {period_mean(ms['Amarakaeri|Reserva Comunal'],2016,2018):,.1f} "
          f"vs all-department definition {t0:,.1f} / {a0:,.1f}")
    save()
    print("All checks OK.")
