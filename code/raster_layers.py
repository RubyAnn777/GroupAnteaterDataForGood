"""Plan v2, step S3: descriptive displacement layers from the raster accounting (raster_zones.py). DESCRIPTION only.

Figures
  fig_v2_zone_map.png        the zone map around La Pampa (team checkpoint: are the boundaries right?)
  fig_v2_stream.png          where new mining appears each year: stacked by zone, totals and growth on top
  fig_v2_sankey.png          per period: new mining split into new land vs return to old pits, flowing to zones
  fig_v2_road_bands.png      crossing the road: new mining by 1-km distance band south/north of the highway
  fig_v2_corridor_share.png  share of Madre de Dios new mining inside the legal corridor, per year
"Newly mined land" = new_land (first-ever mining since 1985, robust to year-to-year flicker); returns to old pits
(remined) appear in the Sankey; "addition" = net change (course measure) = new_land + remined - stopped.
The pixels cannot show people moving: a shift in WHERE new mining appears is consistent with displacement, but
also with new arrivals, the gold price or a different deposit. We say "the mix shifted", never "miners moved".
"""
from __future__ import annotations
import warnings
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from matplotlib.lines import Line2D

from common import (ROOT, OUT, style_axes, finish_figure, headline, label_end, callout, period_band,
                    set_year_ticks, add_event_markers, EVENT_TITLE_PAD, C, INK, INK2, MUTED, SURFACE)
import raster_zones as rz

SRC = "MapBiomas Peru Collection 4 rasters (class 30 mining), zones: SERNANP, INGEMMET D.L. 1100, RAISG roads, MapBiomas Amazonia native communities"
# display groups (several zones merged so the chart stays readable; colors = dataviz reference palette, fixed order)
GROUPS = {
    "La Pampa sector": [7],
    "Corridor across the road": [5],
    "Rest of mining corridor": [6],
    "Native communities": [3, 4],
    "Rest of Tambopata buffer zone": [8],
    "Other buffer zones": [9, 10, 11],
    "Reserves and parks": [1, 2],
    "Rest of Madre de Dios": [12],
}
COL = {"La Pampa sector": C["lapampa"], "Corridor across the road": C["corridor"], "Rest of mining corridor": C["corridor_rest"],
       "Native communities": C["native"], "Rest of Tambopata buffer zone": C["lapampa_tint"], "Other buffer zones": C["buffer_tint"],
       "Reserves and parks": C["reserve"], "Rest of Madre de Dios": C["other"]}
SHORT = {"La Pampa sector": "La Pampa", "Corridor across the road": "Corridor across the road",
         "Rest of mining corridor": "Rest of the legal corridor", "Native communities": "Native communities",
         "Rest of Tambopata buffer zone": "Rest of Tambopata buffer zone", "Other buffer zones": "Other buffer zones",
         "Reserves and parks": "Reserves and parks", "Rest of Madre de Dios": "Rest of Madre de Dios"}
PERIODS = {"2016-18": (2016, 2018), "2019-21": (2019, 2021), "2022-25": (2022, 2025)}


def load():
    z = pd.read_csv(rz.OUT_ZONE)
    z["new_ha"] = z.new_land_ha + z.remined_ha
    z["group"] = z.code.map({c: g for g, cs in GROUPS.items() for c in cs})
    g = z.groupby(["year", "group"])[["mining_ha", "new_land_ha", "remined_ha", "stopped_ha", "new_ha", "from_forest_ha"]].sum()
    return z, g


def fig_zone_map():
    import rasterio
    with rasterio.open(rz.OUT_WIN) as r:
        zone, first = r.read(1), r.read(2); b = r.bounds
    ext = (b.left, b.right, b.bottom, b.top)
    code_col = {c: COL[g] for g, cs in GROUPS.items() for c in cs}
    bg = [int(SURFACE[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    rgb = np.ones(zone.shape + (3,)) * bg
    for c, hx in code_col.items():
        m = zone == c
        rgb[m] = [int(hx[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    rgb = 1 - 0.5 * (1 - rgb)                               # pale zone fill
    mined = first > 0
    rgb[mined] = [0.17, 0.2, 0.22]                          # every pixel ever mined, dark ink
    fig, ax = plt.subplots(figsize=(9, 6.7))
    headline(fig, "One mining belt split by a road: La Pampa outside the legal corridor, the land across it inside",
             "Our zones around La Pampa (dark = land ever mapped as mining, 1985–2025). Team check: are these boundaries right?")
    ax.imshow(rgb, extent=ext, interpolation="nearest")
    L = rz.layers()
    L["ioh"].plot(ax=ax, color=INK, lw=2.4)
    ax.set_xlim(b.left, b.right); ax.set_ylim(b.bottom, b.top); ax.set_aspect(1 / np.cos(np.radians(-12.9)))
    for x in rz.LP_LON:
        ax.axvline(x, color=INK2, ls=(0, (2, 2)), lw=0.9)
    box = dict(facecolor="white", alpha=0.85, edgecolor="none", pad=2.0)
    for nm, (x, y) in {"La Pampa sector": (-69.97, -13.025), "Corridor across\nthe road": (-69.97, -12.80),
                       "Kotsimba\n(native community)": (-70.25, -13.075), "Tambopata reserve": (-69.80, -13.09)}.items():
        ax.text(x, y, nm, fontsize=9, fontweight="medium", ha="center", va="center", color=INK, bbox=box)
    ax.text(-69.70, -12.855, "Interoceanic\nHighway", fontsize=8.5, ha="center", va="center", color=INK, bbox=box)
    ax.text(rz.LP_LON[0] + 0.005, b.top - 0.012, "← La Pampa window →", fontsize=7.5, color=INK2, va="top", ha="left",
            bbox=dict(facecolor="white", alpha=0.7, edgecolor="none", pad=1))
    ax.tick_params(labelsize=8)
    ax.set_xlabel("Longitude (°)"); ax.set_ylabel("Latitude (°)")
    for sp in ax.spines.values():
        sp.set_visible(True); sp.set_color("#c4c0b6")
    present = sorted(set(np.unique(zone)) - {0})
    hs = [Patch(facecolor=COL[g], alpha=0.5, label=SHORT[g]) for g, cs in GROUPS.items() if set(cs) & set(present)]
    hs += [Patch(facecolor="#2b3338", label="Ever mapped as mining"),
           Line2D([], [], color=INK, lw=2.4, label="Interoceanic Highway"),
           Line2D([], [], color=INK2, ls=(0, (2, 2)), lw=0.9, label="La Pampa longitudes (70.15–69.80 W)")]
    fig.legend(handles=hs, loc="lower center", ncol=4, bbox_to_anchor=(0.5, 0.075), fontsize=8, handlelength=1.4,
               columnspacing=1.2)
    finish_figure(fig, f"{SRC}. La Pampa and 'across the road' have no official boundary: longitude window "
                       f"{rz.LP_LON}, corridor within {rz.ACROSS_KM:.0f} km north of the road. Description.",
                  OUT / "fig_v2_zone_map.png", rect_bottom=0.20)


def _gap_stack(ax, x, layers, colors):
    """Stacked area with thin surface-coloured gaps between segments."""
    ax.stackplot(x, layers, colors=colors, edgecolor=SURFACE, linewidth=0.9)


def fig_stream(g):
    yrs = list(range(2010, 2026))
    w = g["new_land_ha"].unstack("group").reindex(index=yrs, columns=list(GROUPS)).fillna(0)
    tot = w.sum(axis=1)
    fig, ax = plt.subplots(figsize=(9, 5.6))
    headline(fig, "After 2019, new mining grew in the legal corridor, not in La Pampa",
             "Land mined for the first time each year in Madre de Dios, hectares, stacked by zone. Numbers: yearly total.")
    period_band(ax, 2018.5, 2021.5, "Operation years")
    _gap_stack(ax, yrs, w.T.values, [COL[c] for c in w.columns])
    ax.plot(yrs, tot, color=INK, lw=0.8, alpha=0.6)
    for y in (2016, 2018, 2021, 2023, 2025):
        ax.annotate(f"{tot[y]:,.0f}", xy=(y, tot[y]), xytext=(0, 5), textcoords="offset points", ha="center",
                    va="bottom", fontsize=8, color=INK2, fontweight="medium")
    # direct labels at the right edge for the big bands, legend for the thin ones
    cum = w.loc[2025].cumsum(); prev = cum.shift(fill_value=0)
    big = ["La Pampa sector", "Corridor across the road", "Rest of mining corridor", "Native communities"]
    for grp in big:
        label_end(ax, 2025.15, (cum[grp] + prev[grp]) / 2, SHORT[grp], COL[grp], dx=4)
    small = [g_ for g_ in GROUPS if g_ not in big]
    ax.legend(handles=[Patch(color=COL[g_], label=SHORT[g_]) for g_ in small], loc="upper left",
              bbox_to_anchor=(0.0, 0.93), fontsize=8, title="Thin bands on top", title_fontsize=8, alignment="left")
    ax.set_ylim(0, tot.max() * 1.18); ax.set_xlim(2009.6, 2025.4)
    ax.set_ylabel("ha per year")
    style_axes(ax); set_year_ticks(ax, yrs, short=True); ax.set_xticks(yrs)
    ax.set_xticklabels([f"'{str(y)[2:]}" for y in yrs])
    add_event_markers(ax, label=True); ax.set_title(" ", pad=EVENT_TITLE_PAD)
    finish_figure(fig, f"{SRC}. Newly mined land = pixels mapped as mining for the first time since 1985 "
                       "(returns to old pits are in the Sankey). A shift in where newly mined land appears fits displacement but does "
                       "not prove that the same miners moved. Description.", OUT / "fig_v2_stream.png", event_note=True)
    return w


def fig_sankey(g):
    """Per period: two sources (new land, old pits) -> zone groups. Band widths = mean ha per year (same scale)."""
    from matplotlib.path import Path as MPath
    from matplotlib.patches import PathPatch
    data = {}; vmax = 0
    for p, (a, b) in PERIODS.items():
        d = g.loc[a:b][["new_land_ha", "remined_ha"]].groupby("group").mean().reindex(list(GROUPS)).fillna(0)
        data[p] = d; vmax = max(vmax, d.values.sum())
    hr = [d.values.sum() / vmax + 0.2 for d in data.values()]
    fig, axes = plt.subplots(3, 1, figsize=(9, 9.6), gridspec_kw={"height_ratios": hr, "hspace": 0.25})
    headline(fig, "New mining more than doubled by 2022–25, and more of it reused old pits",
             "Mean hectares per year mined, by origin (left) and zone (right). Same scale in all three periods.")
    unit = 1.0 / vmax            # data units per ha (x: 0..1 = node area, y in ha-scaled units)
    for ax, (p, d), h_ax in zip(axes, data.items(), hr):
        ax.set_xlim(0, 1); ax.set_ylim(-0.02, h_ax); ax.axis("off")
        top = h_ax - 0.12
        src = {"New land": d.new_land_ha.sum(), "Return to old pits": d.remined_ha.sum()}
        y = top; left = {}
        for s_, v in src.items():
            h = v * unit; left[s_] = [y, y - h]
            ax.add_patch(plt.Rectangle((0.20, y - h), 0.018, h, color=INK2, lw=0))
            ax.text(0.19, y - h / 2, f"{s_}\n{v:,.0f} ha/yr", fontsize=8.5, va="center", ha="right", color=INK)
            y -= h + 0.035
        gap = 0.008
        right = {}; y = top
        for grp in GROUPS:
            v = d.loc[grp].sum(); h = v * unit
            right[grp] = [y, y - h]
            ax.add_patch(plt.Rectangle((0.66, y - h), 0.018, h, color=COL[grp], lw=0))
            y -= h + gap
        # right labels: big groups individually (de-overlapped), small ones summed
        small = ["Rest of Tambopata buffer zone", "Other buffer zones", "Reserves and parks", "Rest of Madre de Dios"]
        last = None
        for grp in GROUPS:
            if grp in small: continue
            v = d.loc[grp].sum(); yc = (right[grp][0] + right[grp][1]) / 2
            if last is not None and last - yc < 0.05: yc = last - 0.05
            ax.text(0.695, yc, f"{SHORT[grp]}  ", fontsize=8.5, va="center", ha="left", color=INK)
            ax.text(0.99, yc, f"{v:,.0f}", fontsize=8.5, va="center", ha="right", color=INK, fontweight="medium")
            last = yc
        sv = sum(d.loc[g_].sum() for g_ in small)
        ys = (right[small[0]][0] + right[small[-1]][1]) / 2 if small else 0
        if last is not None and last - ys < 0.05: ys = last - 0.05
        ax.text(0.695, ys, "Four small zones", fontsize=8, va="center", ha="left", color=INK2)
        ax.text(0.99, ys, f"{sv:,.0f}", fontsize=8, va="center", ha="right", color=INK2)
        for s_, col in (("New land", "new_land_ha"), ("Return to old pits", "remined_ha")):
            for grp in GROUPS:
                v = d.loc[grp, col]; h = v * unit
                if h <= 0: continue
                y0a = left[s_][0]; left[s_][0] -= h
                y0b = right[grp][0]; right[grp][0] -= h
                x0, x1 = 0.218, 0.66; xm = (x0 + x1) / 2
                verts = [(x0, y0a), (xm, y0a), (xm, y0b), (x1, y0b), (x1, y0b - h), (xm, y0b - h),
                         (xm, y0a - h), (x0, y0a - h), (x0, y0a)]
                codes = [MPath.MOVETO, MPath.CURVE4, MPath.CURVE4, MPath.CURVE4, MPath.LINETO, MPath.CURVE4,
                         MPath.CURVE4, MPath.CURVE4, MPath.CLOSEPOLY]
                ax.add_patch(PathPatch(MPath(verts, codes), facecolor=COL[grp], alpha=0.45, lw=0))
        ax.text(0.0, h_ax - 0.02, p, fontsize=11, fontweight="medium", color=INK, va="top")
        ax.text(0.0, h_ax - 0.075, f"{d.values.sum():,.0f} ha/yr in total", fontsize=8.5, color=INK2, va="top")
        ax.text(0.99, h_ax - 0.02, "ha/yr", fontsize=8, color=INK2, va="top", ha="right")
    finish_figure(fig, f"{SRC}. 'Return to old pits' = mining on pixels that were mining in an earlier year but not the year before "
                       "(includes some year-to-year map flicker, about 300 ha/yr in La Pampa before 2019). "
                       "Four small zones = rest of Tambopata buffer zone, other buffer zones, reserves and parks, rest of Madre de Dios. "
                       "Flows are pixels changing class, not people moving. Description.", OUT / "fig_v2_sankey.png")
    return data


def fig_road_bands():
    b = pd.read_csv(rz.OUT_BAND)
    b["new_ha"] = b.new_land_ha                     # first-ever mining (robust to year-to-year flicker)
    fig, axes = plt.subplots(1, 3, figsize=(9, 4.2), sharey=True)
    headline(fig, "After 2019, first-time mining shifted from the south side of the highway to the north side",
             "Land mined for the first time per year, ha, per 1-km band from the highway (La Pampa longitudes only). "
             "Beyond 10 km north = deeper in the corridor")
    res = {}
    for ax, (p, (a, c)) in zip(axes, PERIODS.items()):
        d = b[b.year.between(a, c)].groupby("km_from_road").new_ha.mean()
        res[p] = d
        ax.bar(d.index + 0.5, d.values, width=0.86, color=[C["corridor"] if k >= 0 else C["lapampa"] for k in d.index], lw=0)
        ax.axvline(0, color=INK, lw=1.4)
        ax.axvspan(10, 30, color="#efece5", zorder=-1, lw=0)          # > 10 km north: the rest of the corridor, not "across the road"
        ax.set_xlim(-20, 30)                                         # nothing was mined more than 20 km south
        n, s_ = d[d.index >= 0].sum(), d[d.index < 0].sum()
        ax.set_title(p, pad=20)
        ax.text(0, 1.02, f"south {s_:,.0f}  ·  north {n:,.0f} ha/yr", transform=ax.transAxes, fontsize=8, color=INK2,
                va="bottom", ha="left")
        ax.set_xlabel("km from the highway")
        style_axes(ax)
    ymax = axes[0].get_ylim()[1]
    axes[0].text(-2, ymax * 0.97, "← south:\nLa Pampa side", fontsize=8, color=INK, ha="right", va="top")
    axes[0].text(2, ymax * 0.97, "north: →\ncorridor side", fontsize=8, color=INK, ha="left", va="top")
    axes[0].set_ylabel("ha per year, per 1-km band")
    axes[0].text(20, ymax * 0.97, "> 10 km north:\ndeeper in the\ncorridor", fontsize=7.5, color=INK2, ha="center", va="top")
    finish_figure(fig, f"{SRC}. Only the La Pampa longitudes ({rz.LP_LON}); bands of 1 km measured north-south from "
                       "the highway; the shaded part (more than 10 km north) lies beyond the 'corridor across the road' zone. Description.", OUT / "fig_v2_road_bands.png")
    return res


def fig_corridor_share(g):
    yrs = list(range(2005, 2026))
    w = g["new_land_ha"].unstack("group").reindex(index=yrs).fillna(0)
    cor = w["Corridor across the road"] + w["Rest of mining corridor"]
    share = cor / w.sum(axis=1) * 100
    fig, ax = plt.subplots(figsize=(9, 4.4))
    early, low = share.loc[2005:2009].mean(), share.loc[2014:2018].mean()
    late = share.loc[2022:2025].mean()
    headline(fig, f"The corridor's share of new mining dipped to {low:.0f}% in 2014–18, then returned to its 2005–09 level",
             "Share of land mined for the first time in Madre de Dios that lies inside the legal corridor, % (communities "
             f"excluded). Means: 2005–09 {early:.0f}%, 2022–25 {late:.0f}%")
    period_band(ax, 2018.5, 2021.5)
    ax.text(2020, 3, "Operation years", ha="center", fontsize=7.5, color=INK2)
    ax.plot(yrs, share, color=C["corridor"], lw=2.2, zorder=3)
    ax.plot(yrs, share, "o", color=C["corridor"], ms=4.5, mec="white", mew=1.0, zorder=4)
    for p, (a, b) in PERIODS.items():
        m = share.loc[a:b].mean()
        ax.plot([a - 0.35, b + 0.35], [m] * 2, color=C["corridor"], lw=5, alpha=0.2, solid_capstyle="butt", zorder=2)
        ax.text((a + b) / 2, 93, f"{p.replace('-', '–')} mean", ha="center", va="bottom", fontsize=8, color=INK2)
        ax.text((a + b) / 2, 92, f"{m:.0f}%", ha="center", va="top", fontsize=11, color=INK, fontweight="medium")
    ax.set_ylim(0, 105); ax.set_xlim(2004.5, 2025.5); ax.set_yticks(range(0, 101, 20)); ax.set_ylabel("% of first-time mining")
    style_axes(ax); ax.set_xticks(yrs[::2])
    finish_figure(fig, f"{SRC}. Corridor = D.L. 1100 polygon (INGEMMET, referential) minus native communities. "
                       "Inside the corridor mining can be legal; outside it is presumed illegal. Description.",
                  OUT / "fig_v2_corridor_share.png")
    return share


def run(reg):
    print("\n== v2 descriptive layers (raster) ==")
    if not rz.OUT_ZONE.exists():
        warnings.warn("raster_layers: zone_year_v2.csv missing; skipping"); return
    z, g = load()
    off = pd.read_csv(rz.OUT_OFF)
    o25 = off[off.year == 2025].set_index("unit").mining_ha
    import checks
    checks.check("Raster v2: Tambopata buffer zone mining 2025, ha (course table 20,730)", o25["Tambopata buffer zone"], 20730, tol=60)
    checks.check("Raster v2: Tambopata reserve mining 2025, ha (platform 777)", o25["Tambopata reserve"], 777, tol=5)
    checks.check("Raster v2: Madre de Dios mining 2025, ha (course table 112,622)", o25["Madre de Dios"], 112622, tol=300)
    checks.save()
    fig_zone_map()
    w = fig_stream(g)
    sk = fig_sankey(g)
    rb = fig_road_bands()
    sh = fig_corridor_share(g)
    gp = g.reset_index()
    gp.round(1).to_csv(OUT / "v2_group_year.csv", index=False)
    for p, (a, b) in PERIODS.items():
        k = p.replace("-", "_")
        for grp in GROUPS:
            key = "".join(ch for ch in grp.lower() if ch.isalnum())[:20]
            reg.add(f"v2_new_{key}_{k}", w.loc[a:b, grp].mean(), "ha/yr", f"Land mined for the first time per year, {grp}, {p}", "description", SRC)
        reg.add(f"v2_new_total_{k}", w.loc[a:b].sum(axis=1).mean(), "ha/yr", f"Land mined for the first time per year, all Madre de Dios, {p}", "description", SRC)
        reg.add(f"v2_remined_share_{k}", sk[p].remined_ha.sum() / sk[p].values.sum(), "share", f"Share of new mining on old pits, {p}", "description", SRC)
        reg.add(f"v2_lapampa_remined_{k}", sk[p].loc["La Pampa sector", "remined_ha"], "ha/yr", f"Return to old pits per year, La Pampa sector, {p}", "description", SRC)
        reg.add(f"v2_lapampa_newland_{k}", sk[p].loc["La Pampa sector", "new_land_ha"], "ha/yr", f"New land mined per year, La Pampa sector, {p}", "description", SRC)
        d = rb[p]
        reg.add(f"v2_road_north_{k}", d[d.index >= 0].sum(), "ha/yr", f"First-time mined land per year 0-30 km NORTH of the highway (all 1-km bands; La Pampa longitudes), {p}", "description", SRC)
        reg.add(f"v2_road_south_{k}", d[d.index < 0].sum(), "ha/yr", f"First-time mined land per year 0-30 km SOUTH of the highway (all 1-km bands; La Pampa longitudes), {p}", "description", SRC)
        reg.add(f"v2_corridor_share_{k}", sh.loc[a:b].mean(), "percent", f"Share of first-time mined land inside the legal corridor (excl. communities), {p}", "description", SRC)
    for nm, v in o25.items():
        reg.add("v2_check_" + "".join(ch for ch in nm.lower() if ch.isalnum()) + "_2025", v, "ha",
                f"Raster v2 mining 2025, {nm} (publisher check)", "description", SRC)
    print(w.loc[2014:].round(0).to_string())
