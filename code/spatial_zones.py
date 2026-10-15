"""AMW new mining area by onset year and REGISTRY zone, Madre de Dios (spatial robustness, description only).

Reads data_intermediate/amw_zone_year.csv (built by spatial.py: AMW patches rasterized on the v3 zone registry,
area-weighted). Units are the registry's reporting units (definitions.UNITS), the same land as every net-additions
number. MEASURE: AMW new area (union of detected patches, first detection year): comparable to first-time mining,
NOT to net additions (AMW has no stopped / re-mined state); registered with measure="amw_new_area".
2018 rows are the pre-existing STOCK (excluded); 2025-26 are provisional (hatched; 2026 part-year).
AMW is not MapBiomas: the two are never subtracted or added together (agent.md rule 6).
"""
from __future__ import annotations
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

from common import ROOT, OUT, style_axes, add_event_markers, finish_figure, headline, C
import definitions as D
from spatial import MEASURE, MEASURE_TXT, SRC

CSV = ROOT / "data_intermediate" / "amw_zone_year.csv"
PANELS = {   # panel -> registry zones (definitions.ZONES); same names as the net-additions units
    "tambopata_nr": (D.UNIT_NAME["tambopata_nr"], ["tambopata_nr"], C["reserve"]),
    "tambopata_bz": (D.UNIT_NAME["tambopata_bz"], D.UNITS["tambopata_bz"], C["lapampa"]),
    "amarakaeri_bz": (D.UNIT_NAME["amarakaeri_bz"], ["amarakaeri_bz"], C["buffer"]),
    "corridor_outside_bz": (D.UNIT_NAME["corridor_outside_bz"], D.UNITS["corridor_outside_bz"], C["corridor"]),
    "communities": (D.UNIT_NAME["communities"], ["communities"], C["native"]),
    "rest": ("Rest of the region (other protected areas and buffer zones, rest of Madre de Dios)",
             ["other_anp", "bahuaja_bz", "other_bz", "rest_mdd"], C["other"]),
}


def run(reg):
    print("\n== AMW zones (registry) ==")
    d = pd.read_csv(CSV)
    assert set(d.zone) <= set(D.ZONES), "amw_zone_year.csv must use registry zones"
    assert sorted(z for p in PANELS.values() for z in p[1]) == sorted(D.ZONES), "panels must cover the registry"
    d = d[~d.is_stock]
    prov = d.groupby("year")["provisional"].first()
    W = pd.DataFrame({k: d[d.zone.isin(z)].groupby("year").new_ha.sum() for k, (_, z, _) in PANELS.items()}).fillna(0)
    lp = d[d.zone == "lapampa"].groupby("year").new_ha.sum().reindex(W.index, fill_value=0)
    W.round(1).to_csv(OUT / "amw_zones_new_ha.csv")
    yrs = list(W.index)

    fig, axes = plt.subplots(2, 3, figsize=(12, 6.6), sharex=True)
    headline(fig, "AMW new mining area by zone of the registry, 2019–2026",
             "Measure: AMW new area (union of detected patches; comparable to first-time mining, NOT to net additions), "
             "ha per year, by first-detection year.\nZones: the v3 registry (same land as the net-additions numbers). "
             "Hatched = provisional (2026 part-year). Y-axes differ.")
    for ax, (k, (lab, _, col)) in zip(axes.ravel(), PANELS.items()):
        for y in yrs:
            p = bool(prov[y])
            ax.bar(y, W.loc[y, k], width=0.75, color=col, alpha=0.45 if p else 1.0, hatch="///" if p else None,
                   edgecolor=col if p else "white", linewidth=0.6)
            if k == "tambopata_bz":
                ax.bar(y, lp[y], width=0.75, color="none", edgecolor=C["lapampa_tint"], hatch="....", linewidth=0)
        ax.set_title(lab if len(lab) < 45 else "Rest of the region", loc="left", fontsize=10, pad=6)
        style_axes(ax)
        ax.set_xticks(yrs); ax.set_xticklabels([f"'{str(y)[2:]}" for y in yrs], fontsize=8)
        add_event_markers(ax)
    axes[0, 1].legend(handles=[Patch(facecolor=C["lapampa"], edgecolor=C["lapampa_tint"], hatch="....",
                                     label="of which La Pampa sector")], fontsize=7.5, frameon=False, loc="upper left")
    for ax in axes[:, 0]:
        ax.set_ylabel("AMW new area, ha")
    finish_figure(fig, f"Source: {SRC}. 2018 = pre-existing stock, excluded. AMW = mining scars on land, not "
                       "MapBiomas class 4.2; never added to or subtracted from net additions. Rest of the region = "
                       "other protected areas and buffer zones and the rest of Madre de Dios. Description only; no "
                       "river dredging or mercury.", OUT / "fig_spatial_zones.png", event_note=True)

    tot = W.sum(axis=1)
    cor_ten = d[d.tenure == "corridor"].groupby("year").new_ha.sum().reindex(W.index, fill_value=0)
    for pk in ("during", "later"):
        a, b = D.PERIODS[pk]
        per = f"{a}-{b}"
        note = " (2025 provisional)" if b >= 2025 else ""
        reg.add(f"spz_total_ha_{pk}", tot.loc[a:b].sum(), "ha", f"AMW new area, whole registry region, sum {per}{note}. "
                f"Measure: {MEASURE_TXT}", "description", SRC, measure=MEASURE, zone="registry_region", period=per)
        reg.add(f"spz_corridor_share_{pk}", W.loc[a:b, "corridor_outside_bz"].sum() / tot.loc[a:b].sum(), "share",
                f"Share of the region's AMW new area {per} in the mining corridor outside buffer zones{note}",
                "description", SRC, measure="share", zone="corridor_outside_bz", period=per)
        reg.add(f"spz_corridor_tenure_share_{pk}", cor_ten.loc[a:b].sum() / tot.loc[a:b].sum(), "share",
                f"Share of the region's AMW new area {per} on corridor land anywhere (tenure tag, incl. inside buffer "
                f"zones){note}", "description", SRC, measure="share", zone="registry_region", period=per)
        for k, (lab, _, _) in PANELS.items():
            reg.add(f"spz_ha_{pk}_{k}", W.loc[a:b, k].sum(), "ha", f"AMW new area, {lab}, sum {per}{note}. "
                    f"Measure: {MEASURE_TXT}", "description", SRC, measure=MEASURE, zone=k, period=per)
        reg.add(f"spz_ha_{pk}_lapampa", lp.loc[a:b].sum(), "ha", f"AMW new area, La Pampa sector, sum {per}{note}. "
                f"Measure: {MEASURE_TXT}", "description", SRC, measure=MEASURE, zone="lapampa", period=per)
    print(W.round(0).to_string())
    return W


if __name__ == "__main__":
    from common import Numbers
    r = Numbers(); run(r)
    print(pd.DataFrame(r.rows.values())[["id", "value", "unit"]].to_string())
