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

from common import ROOT, OUT, style_axes, finish_figure, headline, label_end, period_band, C, INK, INK2, MUTED

PERIODS = {"2016-18": (2016, 2018), "2019-21": (2019, 2021), "2022-25": (2022, 2025)}
C_LP, C_COR, C_OUT = C["lapampa"], C["corridor"], C["other"]


def run(pack=None):
    print("\n== Brief figure ==")
    f = ROOT / "data_intermediate" / "zone_year_v2.csv"
    if not f.exists():
        warnings.warn("brief_figure: zone_year_v2.csv missing; skipping"); return
    z = pd.read_csv(f).pivot(index="year", columns="code", values="new_land_ha").fillna(0).loc[2010:2025]
    lp, across = z[7], z[5]
    cor = z[[5, 6]].sum(axis=1); out = z.drop(columns=[5, 6]).sum(axis=1)
    yrs = list(z.index)
    fig, (a1, a2) = plt.subplots(2, 1, figsize=(9, 7.0), sharex=True, gridspec_kw={"height_ratios": [1.3, 1], "hspace": 0.5})
    headline(fig, "Mercurio emptied La Pampa for two years. New mining crossed the road.",
             "Land mined for the first time, hectares per year. Shaded: Mercurio and Plan Restauración (2019–21).")
    for ax in (a1, a2):
        period_band(ax, 2018.5, 2021.5, "Operation years" if ax is a1 else None)
        style_axes(ax)
    for s, c, lab in ((lp, C_LP, "La Pampa\n(target, illegal)"), (across, C_COR, "Corridor across\nthe road (legal)")):
        a1.plot(yrs, s, "-", color=c, lw=2.2, zorder=3)
        a1.plot(yrs, s, "o", color=c, ms=4.5, mec="white", mew=1.0, zorder=4)
        label_end(a1, yrs[-1], s.iloc[-1], lab, c, dx=8)
        for p, (a, b) in PERIODS.items():                         # period means: a faint band behind the line
            m = s.loc[a:b].mean()
            a1.plot([a - 0.35, b + 0.35], [m] * 2, color=c, lw=5, alpha=0.2, solid_capstyle="butt", zorder=2)
    mean = lambda s: " → ".join(f"{s.loc[a:b].mean():,.0f}" for a, b in PERIODS.values())
    a1.set_ylim(0, max(lp.max(), across.max()) * 1.18)
    a1.set_title("Next to the target", pad=22)
    a1.text(0, 1.02, f"Period means 2016–18 → 2019–21 → 2022–25 (faint bands):  La Pampa {mean(lp)}  ·  across the road "
            f"{mean(across)} ha/yr", transform=a1.transAxes, fontsize=8, color=INK2, va="bottom", ha="left")
    a2.bar(yrs, cor, color=C_COR, width=0.72, edgecolor="white", linewidth=0)
    a2.bar(yrs, out, bottom=cor, color=C_OUT, width=0.72, edgecolor="white", linewidth=0)
    a2.bar(yrs, [0] * len(yrs), bottom=cor, color="white", width=0.72, edgecolor="white", linewidth=1.2)  # 2px gap
    label_end(a2, yrs[-1] + 0.4, cor.iloc[-1] / 2, "Inside the\nlegal corridor", C_COR, dx=6)
    label_end(a2, yrs[-1] + 0.4, cor.iloc[-1] + out.iloc[-1] / 2, "Outside", C_OUT, dx=6)
    a2.set_ylim(0, (cor + out).max() * 1.08)
    a2.set_title("All of Madre de Dios: no fall, and most new mining inside the corridor", pad=22)
    a2.text(0, 1.02, f"Period means 2016–18 → 2019–21 → 2022–25:  {mean(cor + out)} ha/yr", transform=a2.transAxes,
            fontsize=8, color=INK2, va="bottom", ha="left")
    a2.set_xticks(yrs); a2.set_xticklabels([f"'{str(y)[2:]}" for y in yrs])
    a1.set_xlim(2009.4, 2025.6)
    finish_figure(fig, "MapBiomas Peru Collection 4 annual maps (30 m, class 4.2 mining, legal and illegal), cut to our "
                       "zones (La Pampa = Tambopata buffer zone 70.15–69.80 W; corridor = D.L. 1100). First-time mining = "
                       "pixels mapped as mining for the first time since 1985. Satellites miss river dredges and mercury. "
                       "Description, not a causal estimate.", OUT / "fig_brief_main.png")
