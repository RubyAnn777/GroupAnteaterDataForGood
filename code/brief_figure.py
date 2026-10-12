"""The ONE figure for the brief (agent.md §8): output/fig_brief_main.png. Redesigned after the critical review.

Message: after Mercurio, first-time mining fell in La Pampa and rose directly across the road in the legal corridor,
while Madre de Dios as a whole kept growing.
Top panel: land mined for the first time each year (MapBiomas Peru Col 4 rasters, zones v2): La Pampa sector (treated)
and the legal corridor within 10 km across the highway; thick segments = period means (2016-18, 2019-21, 2022-25).
Bottom panel: first-time mining in all of Madre de Dios, split into inside the legal corridor and outside.
Uses data_intermediate/zone_year_v2.csv (raster_zones.py). Project palette: orange = La Pampa, blue = corridor,
grey = outside the corridor. Description only.
"""
from __future__ import annotations
import warnings
import pandas as pd
import matplotlib.pyplot as plt

from common import ROOT, OUT, style_axes, finish_figure

PERIODS = {"2016-18": (2016, 2018), "2019-21": (2019, 2021), "2022-25": (2022, 2025)}
C_LP, C_COR, C_OUT, C_EV = "#eb6834", "#2a78d6", "#7d7c78", "#0b0b0b"


def run(pack=None):
    print("\n== Brief figure ==")
    f = ROOT / "data_intermediate" / "zone_year_v2.csv"
    if not f.exists():
        warnings.warn("brief_figure: zone_year_v2.csv missing; skipping"); return
    z = pd.read_csv(f).pivot(index="year", columns="code", values="new_land_ha").fillna(0).loc[2010:2025]
    lp, across = z[7], z[5]
    cor = z[[5, 6]].sum(axis=1); out = z.drop(columns=[5, 6]).sum(axis=1)
    yrs = list(z.index)
    fig, (a1, a2) = plt.subplots(2, 1, figsize=(8.6, 6.4), sharex=True, gridspec_kw={"height_ratios": [1.25, 1]})
    for s, c, lab in ((lp, C_LP, "La Pampa sector (target, illegal zone)"), (across, C_COR, "Legal corridor across the road (≤10 km)")):
        a1.plot(yrs, s, "o-", color=c, lw=2, ms=4, label=lab)
        for p, (a, b) in PERIODS.items():
            a1.plot([a - 0.4, b + 0.4], [s.loc[a:b].mean()] * 2, color=c, lw=5, alpha=0.35, solid_capstyle="butt")
    for ax in (a1, a2):
        ax.axvline(2018.5, color=C_EV, lw=1.4)
        style_axes(ax)
    a1.text(2018.6, a1.get_ylim()[1] * 0.97, "Operation Mercurio\nFeb 2019", fontsize=8, va="top")
    a1.set_ylabel("Land mined for the\nfirst time (ha/yr)")
    a1.set_ylim(top=max(lp.max(), across.max()) * 1.32)
    a1.legend(fontsize=8, frameon=False, loc="upper right")
    a1.set_title("Next to the target: La Pampa fell, the corridor across the road rose", loc="left", fontsize=9.5)
    a2.bar(yrs, cor, color=C_COR, width=0.72, label="Inside the legal corridor")
    a2.bar(yrs, out, bottom=cor, color=C_OUT, width=0.72, label="Outside the corridor")
    a2.set_ylabel("Land mined for the\nfirst time (ha/yr)")
    a2.legend(fontsize=8, frameon=False, loc="upper left")
    a2.set_title("Madre de Dios as a whole kept growing, mostly inside the corridor", loc="left", fontsize=9.5)
    a2.set_xticks(yrs); a2.set_xticklabels([f"'{str(y)[2:]}" for y in yrs], fontsize=8)
    fig.suptitle("After Mercurio, new mining moved across the road; the region did not mine less",
                 x=0.01, ha="left", fontsize=11, fontweight="bold")
    finish_figure(fig, "Source: MapBiomas Peru Collection 4 annual maps (30 m, class 4.2 mining, legal and illegal), cut to our "
                       "zones (La Pampa = Tambopata buffer zone 70.15-69.80 W; corridor = D.L. 1100). First-time mining = "
                       "pixels mapped as mining for the first time since 1985. Thick segments = period means. Satellites "
                       "miss river dredges and mercury. Description.", OUT / "fig_brief_main.png", rect_bottom=0.13)
