"""The ONE figure for the brief (agent.md §8): output/fig_brief_main.png. Plan v3: net additions with their parts.

Message: in 2019-21 net additions in La Pampa collapsed because new land halved AND mined land stopped; across the
road, in the legal corridor, every part rose; Madre de Dios as a whole kept growing.
Top row (same y-scale): La Pampa sector and the corridor across the road. Bars = the three parts (new land and
re-mined above zero, stopped below zero), line = net additions = new + re-mined - stopped.
Bottom: net additions in all of Madre de Dios by area (Tambopata buffer zone, mining corridor outside buffer zones,
everything else), stacked; they sum to the department.
Data: zonedata (raster_zones.py, MapBiomas Peru Col 4 rasters, our zone registry). Every number in the title and
subtitle is registered (fig_brief_*). Description only.
"""
from __future__ import annotations
import numpy as np
import matplotlib.pyplot as plt

from common import OUT, style_axes, finish_figure, headline, label_end, period_band, C, INK, INK2, MUTED
import definitions as D
import zonedata as Z

Y0 = 2010


def run(pack=None, reg=None):
    print("\n== Brief figure (v3: net additions + parts) ==")
    ru = Z.region_units()
    W = {m: Z.wide(ru, D.COLS[m]).loc[Y0:2025] for m in ["net"] + D.PARTS}
    yrs = list(W["net"].index)
    pm = lambda u, m, p: Z.period_mean(Z.wide(ru, D.COLS[m])[u], p)
    lp_pre, lp_dur = pm("lapampa", "net", "pre"), pm("lapampa", "net", "during")
    x_pre, x_dur = pm("corridor_across", "net", "pre"), pm("corridor_across", "net", "during")
    new_ratio = pm("lapampa", "new", "during") / pm("lapampa", "new", "pre")
    stop_ratio = pm("lapampa", "stopped", "during") / pm("lapampa", "stopped", "pre")
    if reg is not None:
        for k, v, m, u in (("lapampa_net_pre", lp_pre, "net", "lapampa"), ("lapampa_net_during", lp_dur, "net", "lapampa"),
                           ("across_net_pre", x_pre, "net", "corridor_across"), ("across_net_during", x_dur, "net", "corridor_across")):
            p = "2016–18" if k.endswith("pre") else "2019–21"
            reg.add(f"fig_brief_{k}", v, "ha/yr", f"{D.MEASURE_NAME[m]}, {D.UNIT_NAME[u]}, {p}: mean per year (brief figure)",
                    "description", D.SOURCE, measure=m, zone=u, period=p)
        reg.add("fig_brief_lapampa_new_ratio", new_ratio, "ratio", "New land, La Pampa sector, mean 2019–21 / mean 2016–18",
                "description", D.SOURCE, measure="new", zone="lapampa", period="2019–21 vs 2016–18")
        reg.add("fig_brief_lapampa_stopped_ratio", stop_ratio, "ratio", "Stopped land, La Pampa sector, mean 2019–21 / "
                "mean 2016–18", "description", D.SOURCE, measure="stopped", zone="lapampa", period="2019–21 vs 2016–18")
        reg.add("fig_brief_across_net_ratio", x_dur / x_pre, "ratio", "Net additions, corridor across the road, mean "
                "2019–21 / mean 2016–18", "description", D.SOURCE, measure="net", zone="corridor_across",
                period="2019–21 vs 2016–18")

    fig = plt.figure(figsize=(7.4, 5.7))
    gs = fig.add_gridspec(2, 2, height_ratios=[1.1, 1], hspace=0.66, wspace=0.12)
    a1 = fig.add_subplot(gs[0, 0]); a2 = fig.add_subplot(gs[0, 1], sharey=a1); a3 = fig.add_subplot(gs[1, :])
    word = "halved" if 0.4 <= new_ratio <= 0.6 else f"fell {1 - new_ratio:.0%}"
    headline(fig, f"La Pampa's net mining fell from {lp_pre:,.0f} to {lp_dur:,.0f} ha/yr in 2019–21;\n"
                  f"across the road it rose from {x_pre:,.0f} to {x_dur:,.0f}",
             f"Net additions (black line) = new land + re-mined − stopped (bars), ha/yr. In La Pampa, new land {word} "
             f"and stopped land\nrose {stop_ratio:.1f}-fold (most of it in 2019): pits leaving the mining class explain part of the fall. "
             "Description, not a causal estimate.")
    for ax, u, title in ((a1, "lapampa", "La Pampa sector (the target)"),
                         (a2, "corridor_across", "Corridor across the road (legal)")):
        period_band(ax, D.PERIODS["during"][0] - 0.5, D.PERIODS["during"][1] + 0.5,
                    "Mercurio and what\nfollowed (2019–21)" if ax is a1 else None, color="#e6e1d6")
        new, rem, stp, net = (W[m][u].values for m in ("new", "remined", "stopped", "net"))
        ax.bar(yrs, new, color=C["new"], width=0.74, lw=0)
        ax.bar(yrs, rem, bottom=new, color=C["remined"], width=0.74, lw=0, edgecolor="white")
        ax.bar(yrs, -stp, color=C["stopped"], width=0.74, lw=0)
        ax.axhline(0, color=INK2, lw=0.8, zorder=2)
        ax.plot(yrs, net, color=INK, lw=2.0, zorder=4)
        ax.plot(yrs, net, "o", color=INK, ms=3.6, mec="white", mew=0.8, zorder=5)
        ax.set_title(title, fontsize=9.5, pad=6, loc="left")
        style_axes(ax)
        ax.set_xticks(yrs[::3]); ax.set_xticklabels([f"'{str(y)[2:]}" for y in yrs[::3]])
        ax.set_xlim(Y0 - 0.6, 2025.6)
    plt.setp(a2.get_yticklabels(), visible=False)
    a1.set_ylabel("ha/yr")
    lo, hi = a1.get_ylim(); a1.set_ylim(lo * 1.05, hi * 1.12)
    from matplotlib.patches import Patch
    from matplotlib.lines import Line2D
    a1.legend(handles=[Patch(color=C["new"], label="New land"), Patch(color=C["remined"], label="Re-mined"),
                        Patch(color=C["stopped"], label="Stopped (below zero)"),
                        Line2D([], [], color=INK, marker="o", ms=3.6, mec="white", lw=2.0, label="Net additions")],
               loc="lower left", bbox_to_anchor=(0, 1.13), ncol=4, borderaxespad=0,
               fontsize=7.8, frameon=False, handlelength=1.1, columnspacing=1.3)
    # bottom: where Madre de Dios's net additions happened (parts inside the department; they sum to the total)
    z = Z._zone_year()
    z = z[(z.in_mdd == 1) & z.year.between(Y0, 2025)]
    grp = {"lapampa": "tbz", "tambopata_bz_rest": "tbz", "corridor_across": "cor", "corridor_rest": "cor"}
    z = z.assign(g=z.zone.map(grp).fillna("other")).groupby(["year", "g"]).net_ha.sum().unstack().fillna(0)
    tot = z.sum(axis=1)
    pos = z.clip(lower=0); neg = z.clip(upper=0)
    bp = np.zeros(len(z)); bn = np.zeros(len(z))
    for g, c, lab in (("tbz", C["lapampa"], "Tambopata buffer zone"), ("cor", C["corridor"], "Mining corridor (outside buffer zones)"),
                      ("other", C["other"], "Rest of the department")):
        a3.bar(z.index, pos[g], bottom=bp, color=c, width=0.74, lw=0, label=lab)
        a3.bar(z.index, neg[g], bottom=bn, color=c, width=0.74, lw=0)
        bp += pos[g].values; bn += neg[g].values
    a3.axhline(0, color=INK2, lw=0.8)
    a3.plot(z.index, tot, color=INK, lw=1.4, marker="o", ms=3.2, mec="white", label="Madre de Dios, total")
    period_band(a3, D.PERIODS["during"][0] - 0.5, D.PERIODS["during"][1] + 0.5, None, color="#e6e1d6")
    a3.legend(loc="upper left", fontsize=7.5, ncol=2, frameon=False, handlelength=1.0, columnspacing=1.0)
    mean = lambda s: " → ".join(f"{Z.period_mean(s, p):,.0f}" for p in ("pre", "during", "later"))
    a3.set_title(f"All of Madre de Dios: no fall (net additions {mean(tot)} ha/yr, 2016–18 → 2019–21 → 2022–25)",
                 fontsize=9.5, pad=6)
    for x in (2022.5, 2024.5):
        a3.axvline(x, color=MUTED, linestyle=(0, (3, 2)), lw=0.8, zorder=0.5)
    for x, t in ((2022.5, "Emergency Apr 2023"), (2024.5, "Navy out 2025")):
        a3.text(x - 0.1, 0.97, t, transform=a3.get_xaxis_transform(), ha="right", va="top", fontsize=6.8, color=INK2)
    style_axes(a3)
    a3.set_ylabel("ha/yr")
    a3.set_ylim(None, a3.get_ylim()[1] * 1.25)
    a3.annotate("2023 spike: MapBiomas only\n(GLAD alerts, AMW flat)", xy=(2023, tot.loc[2023]), xytext=(2021.8, tot.loc[2023] * 0.62),
                fontsize=6.8, color=INK2, ha="right", va="center", arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.6))
    a3.set_xticks(yrs[::1]); a3.set_xticklabels([f"'{str(y)[2:]}" for y in yrs])
    a3.set_xlim(Y0 - 0.6, 2025.6)
    if reg is not None:
        for p in ("pre", "during", "later"):
            reg.add(f"fig_brief_mdd_net_{p}", Z.period_mean(tot, p), "ha/yr", f"Net additions, Madre de Dios "
                    f"(department), {D.period_label(p)}: mean per year (brief figure)", "description", D.SOURCE,
                    measure="net", zone="mdd", period=D.period_label(p))
    finish_figure(fig, "MapBiomas Peru Collection 4 annual maps (30 m, class 4.2 mining, legal and illegal), our pixel "
                       "accounting on one zone registry (La Pampa = Tambopata buffer zone, 70.15–69.80 W; corridor = "
                       "D.L. 1100). New land = mined for the first time since 1985; re-mined = mined again after a gap; "
                       "stopped = left the mining class (most often it became water). Satellites miss river dredges and mercury.",
                  OUT / "fig_brief_main.png")
