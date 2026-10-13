"""The ONE figure for the brief (agent.md §8): output/fig_brief_main.png. Redesigned after the critical review.

Message: in 2019-21 first-time mining fell in La Pampa and rose directly across the road in the legal corridor,
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
    pm = lambda s, a, b: s.loc[a:b].mean()
    lp_ratio = pm(lp, 2019, 2021) / pm(lp, 2016, 2018); x_ratio = pm(across, 2019, 2021) / pm(across, 2016, 2018)
    lp_word = "halved" if 0.4 <= lp_ratio <= 0.6 else f"fell {1 - lp_ratio:.0%}"
    fig, (a1, a2) = plt.subplots(2, 1, figsize=(7.4, 6.1), sharex=True, gridspec_kw={"height_ratios": [1.25, 1], "hspace": 0.6})
    headline(fig, f"La Pampa: first-time mining {lp_word} in 2019–21. Across the road: up {x_ratio:.0f}-fold.",
             "Land mined for the first time, ha/yr. Shaded: Mercurio (Feb 2019), COVID-19, Plan Restauración (2021).\n"
             "Dashed: state of emergency (Apr 2023), navy posts withdrawn (2025). Description, not a causal estimate.")
    for ax in (a1, a2):
        period_band(ax, 2018.5, 2021.5, "Operation years" if ax is a1 else None, color="#e6e1d6")
        for x in (2022.5, 2024.5):                                # later waves, drawn at Y - 0.5 (common.py convention)
            ax.axvline(x, color=MUTED, linestyle=(0, (3, 2)), linewidth=0.8, zorder=0.5)
        style_axes(ax)
    for x, t in ((2022.5, "Emergency\nApr 2023"), (2024.5, "Navy posts\nwithdrawn\n2025")):
        a1.text(x - 0.08, 0.90, t, transform=a1.get_xaxis_transform(), ha="right", va="top", fontsize=7, color=INK2)
    for s, c, lab in ((lp, C_LP, "La Pampa\nsector"), (across, C_COR, "Across\nthe road")):
        a1.plot(yrs, s, "-", color=c, lw=2.2, zorder=3)
        a1.plot(yrs, s, "o", color=c, ms=4.5, mec="white", mew=1.0, zorder=4)
        label_end(a1, yrs[-1], s.iloc[-1], lab, c, dx=8)
        for p, (a, b) in PERIODS.items():                         # period means: a band behind the line
            m = s.loc[a:b].mean()
            a1.plot([a - 0.35, b + 0.35], [m] * 2, color=c, lw=4, alpha=0.45, solid_capstyle="butt", zorder=2)
    mean = lambda s: " → ".join(f"{s.loc[a:b].mean():,.0f}" for a, b in PERIODS.values())
    a1.set_ylim(0, max(lp.max(), across.max()) * 1.18)
    a1.set_title("The target and the land across the road", pad=34)
    a1.text(0, 1.02, f"Means (bands) 2016–18 → 2019–21 → 2022–25:\nLa Pampa sector, the target: {mean(lp)} ha/yr  ·  "
            f"across the road, in the legal corridor: {mean(across)} ha/yr", transform=a1.transAxes, fontsize=8, color=INK2, va="bottom", ha="left")
    a2.bar(yrs, cor, color=C_COR, width=0.72, edgecolor="white", linewidth=0)
    a2.bar(yrs, out, bottom=cor, color=C_OUT, width=0.72, edgecolor="white", linewidth=0)
    a2.bar(yrs, [0] * len(yrs), bottom=cor, color="white", width=0.72, edgecolor="white", linewidth=1.2)  # 2px gap
    label_end(a2, yrs[-1] + 0.4, cor.iloc[-1] / 2, "Inside\nthe legal\ncorridor", C_COR, dx=6)
    label_end(a2, yrs[-1] + 0.4, cor.iloc[-1] + out.iloc[-1] / 2, "Outside", C_OUT, dx=6)
    a2.set_ylim(0, (cor + out).max() * 1.08)
    a2.set_title("All of Madre de Dios: no fall, and a growing share inside the legal corridor", pad=22)
    a2.text(0, 1.02, f"Period means 2016–18 → 2019–21 → 2022–25:  {mean(cor + out)} ha/yr", transform=a2.transAxes,
            fontsize=8, color=INK2, va="bottom", ha="left")
    a2.set_xticks(yrs); a2.set_xticklabels([f"'{str(y)[2:]}" for y in yrs])
    a1.set_xlim(2009.4, 2025.6)
    finish_figure(fig, "MapBiomas Peru Collection 4 annual maps (30 m, class 4.2 mining, legal and illegal), cut to our "
                       "zones (La Pampa = Tambopata buffer zone 70.15–69.80 W; corridor = D.L. 1100). First-time mining = "
                       "pixels mapped as mining for the first time since 1985; the class cannot tell legal from illegal mining. "
                       "Satellites miss river dredges and mercury.", OUT / "fig_brief_main.png")
