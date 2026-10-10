"""AMW new mining area by onset year and zone, Madre de Dios (spatial robustness, description only).

Reads data_intermediate/amw_zone_year.csv (built by spatial.py from the Amazon Mining Watch patches).
2018 rows are the pre-existing STOCK (is_stock) and are excluded; 2025-26 are provisional (hatched, lighter).
AMW is not MapBiomas: the two never get subtracted or added together (agent.md rule 6).
"""
from __future__ import annotations
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

from common import ROOT, OUT, style_axes, add_event_markers, finish_figure, EVENT_TITLE_PAD

CSV = ROOT / "data_intermediate" / "amw_zone_year.csv"
SRC = "data_intermediate/amw_zone_year.csv"
GROUPS = {   # panel label -> member units
    "Tambopata NR (reserve)": ["Tambopata NR"],
    "Tambopata BZ": ["Tambopata BZ"],
    "Amarakaeri RC + BZ": ["Amarakaeri RC", "Amarakaeri BZ"],
    "Bahuaja-Sonene NP + BZ": ["Bahuaja-Sonene NP", "Bahuaja-Sonene BZ"],
    "Mining corridor (DL 1100)": ["Mining corridor (DL 1100)"],
    "Other Madre de Dios (box)": ["Other Madre de Dios box"],
}
COL = {"Tambopata NR (reserve)": "#B03A2E", "Tambopata BZ": "#d9a441", "Amarakaeri RC + BZ": "#7a9cc6",
       "Bahuaja-Sonene NP + BZ": "#6aa84f", "Mining corridor (DL 1100)": "#555555", "Other Madre de Dios (box)": "#8E7CC3"}

def run(reg):
    print("\n== AMW zones ==")
    d = pd.read_csv(CSV)
    assert d["is_stock"].eq(d["year"] == 2018).all()
    d = d[~d["is_stock"]]
    prov = d.groupby("year")["provisional"].first()
    g = {}
    for lab, units in GROUPS.items():
        s = d[d["unit"].isin(units)].groupby("year")["new_ha"].sum()
        assert set(d[d["unit"].isin(units)]["unit"]) == set(units)
        g[lab] = s
    W = pd.DataFrame(g)
    W.round(1).to_csv(OUT / "amw_zones_new_ha.csv")
    yrs = list(W.index)

    fig, axes = plt.subplots(2, 3, figsize=(12, 6.8), sharex=True)
    for ax, lab in zip(axes.ravel(), GROUPS):
        for y in yrs:
            p = bool(prov[y])
            ax.bar(y, W.loc[y, lab], width=0.75, color=COL[lab], alpha=0.45 if p else 1.0,
                   hatch="///" if p else None, edgecolor="white" if not p else COL[lab], linewidth=0.6)
        ax.set_title(lab, loc="left", fontsize=10, pad=6)
        style_axes(ax)
        ax.set_xticks(yrs); ax.set_xticklabels([str(y) for y in yrs], fontsize=7.5, rotation=45)
        add_event_markers(ax)
    for ax in axes[:, 0]: ax.set_ylabel("New AMW mining area\nin onset year (ha)")
    fig.legend(handles=[Patch(facecolor="#888888", label="Final years (2019-24)"),
                        Patch(facecolor="#bbbbbb", hatch="///", edgecolor="#888888", label="Provisional (2025-26; 2026 is part-year)")],
               loc="lower center", fontsize=8, frameon=False, ncol=2, bbox_to_anchor=(0.5, 0.085))
    finish_figure(fig, "Source: Amazon Mining Watch (AMW) mining patches by onset year, summed by zone. 2018 = pre-existing stock, excluded. "
                       "AMW is detected mining on land, not MapBiomas class 4.2: the two series are never added or subtracted. "
                       "Y-axes differ by panel. Red solid line = Operation Mercurio (Feb 2019); dashed = COVID-19 (2020), Plan Restauracion (2021), state of emergency (Apr 2023). Description only; no river dredging or mercury.",
                  OUT / "fig_spatial_zones.png", rect_bottom=0.16, event_note=False)

    # numbers
    SRCN = SRC
    corr = W["Mining corridor (DL 1100)"]; tot = W.sum(axis=1)
    for lab, (a, b) in {"2019_21": (2019, 2021), "2022_24": (2022, 2024)}.items():
        c, t = corr.loc[a:b].sum(), tot.loc[a:b].sum()
        reg.add(f"spz_corridor_ha_{lab}", c, "ha", f"AMW new mining area in the DL 1100 corridor {a}-{b} (sum)", "description", SRCN)
        reg.add(f"spz_total_ha_{lab}", t, "ha", f"AMW new mining area, all six zones {a}-{b} (sum)", "description", SRCN)
        reg.add(f"spz_corridor_share_{lab}", c / t, "share", f"Corridor share of AMW new area in the six zones {a}-{b}", "description", SRCN)
        reg.add(f"spz_noncorridor_share_{lab}", 1 - c / t, "share", f"Non-corridor share {a}-{b}", "description", SRCN)
        for lab2 in GROUPS:
            reg.add(f"spz_ha_{lab}_" + "".join(ch for ch in lab2.lower() if ch.isalnum())[:22],
                    W.loc[a:b, lab2].sum(), "ha", f"AMW new area {lab2}, {a}-{b} (sum)", "description", SRCN)
    reg.add("spz_tambopata_nr_2025_26_ha", W.loc[2025:2026, "Tambopata NR (reserve)"].sum(), "ha",
            "AMW new mining area inside Tambopata NR, 2025-26 (PROVISIONAL, 2026 part-year)", "description", SRCN)
    reg.add("spz_tambopata_nr_2019_24_ha", W.loc[2019:2024, "Tambopata NR (reserve)"].sum(), "ha",
            "AMW new mining area inside Tambopata NR, 2019-24 (sum)", "description", SRCN)
    print(W.round(0).to_string())
    for k in ("2019_21", "2022_24"):
        print(k, "corridor share", round(reg.get(f"spz_corridor_share_{k}"), 3))
    return W
