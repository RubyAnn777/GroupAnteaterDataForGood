"""The ONE figure for the brief (agent.md §8): output/fig_brief_main.png. Plan v3.1: lean, one zone in the time series.

Message: net mining additions in the Tambopata buffer zone collapsed in 2019–21 (new land fell, and many pits went
quiet), came back in 2022–25 (much of it on old pits), while the legal mining corridor kept growing, so the
department never fell.
Top: Tambopata buffer zone, 2014–2025: bars = the three parts (new land and re-mined above zero, stopped below zero),
line = net additions = new + re-mined − stopped. Only Mercurio and the 2023 emergency are labelled.
Bottom: period means of net additions (2016–18, 2019–21, 2022–25) for the Tambopata buffer zone, the legal mining
corridor outside buffer zones (D.L. 1100) and the rest of Madre de Dios; corridor and rest are their Madre de Dios parts; the buffer zone is shown whole (as in the text).
Data: zonedata (raster_zones.py; MapBiomas Peru Col 4). Every number in the title is registered (fig_brief_*).
Description only.
"""
from __future__ import annotations
import numpy as np
import matplotlib.pyplot as plt

from common import OUT, style_axes, finish_figure, headline, period_band, C, INK, INK2, MUTED
import definitions as D
import zonedata as Z

Y0, Y1 = D.YEARS
T = D.TREATED_ZONE


def run(pack=None, reg=None):
    print("\n== Brief figure (v3.1: Tambopata buffer zone parts + where it went) ==")
    ru = Z.region_units()
    W = {m: Z.wide(ru, D.COLS[m]).loc[Y0:Y1] for m in ["net"] + D.PARTS}
    yrs = list(W["net"].index)
    pm = lambda s, p: Z.period_mean(s, p)
    t_net = Z.wide(ru, "net_ha")[T]
    pre, dur, lat = pm(t_net, "pre"), pm(t_net, "during"), pm(t_net, "later")

    # where it went: department parts inside Madre de Dios, three groups that sum to the department
    z = Z._zone_year()
    z = z[(z.in_mdd == 1)]
    grp = {"lapampa": "tbz", "tambopata_bz_rest": "tbz", "corridor_across": "cor", "corridor_rest": "cor"}
    g = z.assign(g=z.zone.map(grp).fillna("rest")).groupby(["year", "g"]).net_ha.sum().unstack().fillna(0)
    g["tbz"] = t_net.reindex(g.index)            # the whole official buffer zone (as in the title and the text)
    per = {p: {k: pm(g[k], p) for k in ("tbz", "cor", "rest")} for p in ("pre", "during", "later")}
    if reg is not None:
        for p, v in (("pre", pre), ("during", dur), ("later", lat)):
            reg.add(f"fig_brief_tbz_net_{p}", v, "ha/yr", f"Net additions, Tambopata buffer zone, {D.period_label(p)}: "
                    "mean per year (brief figure)", "description", D.SOURCE, measure="net", zone=T, period=D.period_label(p))
            for k, nm in (("cor", "legal mining corridor outside buffer zones (in Madre de Dios)"),
                          ("rest", "rest of Madre de Dios (outside the Tambopata buffer zone and the corridor)")):
                reg.add(f"fig_brief_{k}_net_{p}", per[p][k], "ha/yr", f"Net additions, {nm}, {D.period_label(p)}: mean "
                        "per year (brief figure)", "description", D.SOURCE, measure="net",
                        zone="corridor_outside_bz" if k == "cor" else "mdd_rest_ex_tbz_cor", period=D.period_label(p))

    fig = plt.figure(figsize=(7.4, 4.75))
    gs = fig.add_gridspec(2, 1, height_ratios=[1.5, 1], hspace=0.62)
    a1 = fig.add_subplot(gs[0]); a2 = fig.add_subplot(gs[1])
    headline(fig, f"Tambopata buffer zone: net mining fell from {pre:,.0f} to {dur:,.0f} ha/yr,\n"
                  f"then came back; the legal corridor kept growing",
             "Net mining additions, ha/yr (black line) = new land + re-mined − stopped (bars). "
             "Description, not a causal estimate.")
    # --- top: parts, Tambopata buffer zone
    period_band(a1, D.PERIODS["during"][0] - 0.5, D.PERIODS["during"][1] + 0.5, None, color="#e6e1d6")
    new, rem, stp, net = (W[m][T].values for m in ("new", "remined", "stopped", "net"))
    a1.bar(yrs, new, color=C["new"], width=0.72, lw=0, label="New land")
    a1.bar(yrs, rem, bottom=new, color=C["remined"], width=0.72, lw=0, label="Re-mined")
    a1.bar(yrs, -stp, color=C["stopped"], width=0.72, lw=0, label="Stopped (below zero)")
    a1.axhline(0, color=INK2, lw=0.8)
    a1.plot(yrs, net, color=INK, lw=2.0, marker="o", ms=3.6, mec="white", mew=0.8, label="Net additions", zorder=5)
    for x, t in ((D.FIRST_POST - 0.5, "Mercurio\nFeb 2019"), (2022.5, "Emergency\nApr 2023")):
        a1.axvline(x, color=INK if "Mercurio" in t else MUTED, lw=1.0 if "Mercurio" in t else 0.8,
                   linestyle="-" if "Mercurio" in t else (0, (3, 2)), zorder=0.6)
        a1.text(x + (0.1 if "Mercurio" in t else -0.1), 0.98, t, transform=a1.get_xaxis_transform(),
                ha="left" if "Mercurio" in t else "right", va="top", fontsize=7, color=INK2)
    a1.set_title("Tambopata buffer zone, 2014–2025 (shaded: 2019–21)", fontsize=9.5, loc="left", pad=6)
    a1.legend(loc="lower left", bbox_to_anchor=(0, 1.13), ncol=4, fontsize=7.6, frameon=False, handlelength=1.1,
              columnspacing=1.2, borderaxespad=0)
    a1.set_ylabel("ha/yr")
    style_axes(a1)
    a1.set_xticks(yrs[::2]); a1.set_xticklabels([str(y) for y in yrs[::2]])
    a1.set_xlim(Y0 - 0.6, Y1 + 0.6)
    # --- bottom: where it went, period means
    labs = {"pre": "2016–18", "during": "2019–21", "later": "2022–25"}
    keys = [("tbz", "Tambopata buffer zone", C["lapampa"]), ("cor", "Legal mining corridor", C["corridor"]),
            ("rest", "Rest of Madre de Dios", C["other"])]
    x = np.arange(3); w = 0.26
    for i, (k, nm, c) in enumerate(keys):
        v = [per[p][k] for p in labs]
        a2.bar(x + (i - 1) * w, v, width=w * 0.92, color=c, lw=0, label=nm)
        for xi, vi in zip(x + (i - 1) * w, v):
            a2.text(xi, max(vi, 0) + 120, f"{vi:,.0f}", ha="center", va="bottom", fontsize=6.6, color=INK2)
    a2.axhline(0, color=INK2, lw=0.8)
    a2.set_xticks(x); a2.set_xticklabels(list(labs.values()))
    a2.set_title("Where it went: Madre de Dios, net additions, mean per year", fontsize=9.5, loc="left", pad=6)
    a2.legend(loc="upper left", fontsize=7.6, frameon=False, handlelength=1.1)
    a2.set_ylabel("ha/yr")
    a2.set_ylim(None, max(max(d.values()) for d in per.values()) * 1.18)
    style_axes(a2)
    finish_figure(fig, "MapBiomas Peru Collection 4 annual maps (30 m, class 4.2: all mining, legal and illegal), our pixel "
                       "accounting on one zone registry. New land = mined for the first time since 1985; re-mined = mined "
                       "again after a gap; stopped = left the mining class. Legal mining corridor = D.L. 1100 land outside "
                       "buffer zones. Satellites miss river dredges and mercury.", OUT / "fig_brief_main.png")
