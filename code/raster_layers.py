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

from common import ROOT, OUT, style_axes, finish_figure
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
COL = {"La Pampa sector": "#eb6834", "Corridor across the road": "#2a78d6", "Rest of mining corridor": "#9cc0ea",
       "Native communities": "#e87ba4", "Rest of Tambopata buffer zone": "#eda100", "Other buffer zones": "#1baf7a",
       "Reserves and parks": "#008300", "Rest of Madre de Dios": "#b9b8b2"}
PERIODS = {"2016-18": (2016, 2018), "2019-21": (2019, 2021), "2022-25": (2022, 2025)}


def load():
    z = pd.read_csv(rz.OUT_ZONE)
    z["new_ha"] = z.new_land_ha + z.remined_ha
    z["group"] = z.code.map({c: g for g, cs in GROUPS.items() for c in cs})
    g = z.groupby(["year", "group"])[["mining_ha", "new_land_ha", "remined_ha", "stopped_ha", "new_ha", "from_forest_ha"]].sum()
    return z, g


def fig_zone_map():
    import rasterio
    import geopandas as gpd
    with rasterio.open(rz.OUT_WIN) as r:
        zone, first = r.read(1), r.read(2); b = r.bounds
    ext = (b.left, b.right, b.bottom, b.top)
    code_col = {c: COL[g] for g, cs in GROUPS.items() for c in cs}
    rgb = np.ones(zone.shape + (3,))
    for c, hx in code_col.items():
        m = zone == c
        rgb[m] = [int(hx[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    rgb = 1 - 0.55 * (1 - rgb)                              # pale zone fill
    mined = first > 0
    rgb[mined] = [0.15, 0.15, 0.15]                         # every pixel ever mined, dark
    fig, ax = plt.subplots(figsize=(11, 6.6))
    ax.imshow(rgb, extent=ext, interpolation="nearest")
    L = rz.layers()
    L["ioh"].plot(ax=ax, color="black", lw=2.2)
    ax.text(-69.72, -12.875, "Interoceanic\nHighway", fontsize=8, ha="center")
    ax.set_xlim(b.left, b.right); ax.set_ylim(b.bottom, b.top); ax.set_aspect(1 / np.cos(np.radians(-12.9)))
    for x in rz.LP_LON:
        ax.axvline(x, color="#52514e", ls=":", lw=1)
    for nm, (x, y) in {"La Pampa sector": (-69.97, -13.02), "Corridor across\nthe road": (-69.97, -12.80),
                       "Kotsimba": (-70.22, -13.07), "Tambopata reserve": (-69.80, -13.09)}.items():
        ax.text(x, y, nm, fontsize=9, fontweight="bold", ha="center", color="#0b0b0b",
                bbox=dict(facecolor="white", alpha=0.75, edgecolor="none", pad=1.5))
    present = sorted(set(np.unique(zone)) - {0})
    hs = [Patch(facecolor=COL[g], alpha=0.5, label=g) for g, cs in GROUPS.items() if set(cs) & set(present)]
    hs += [Patch(facecolor="#262626", label="Ever mapped as mining (1985-2025)"),
           Line2D([], [], color="#52514e", ls=":", label="La Pampa longitudes (70.15-69.80 W)")]
    ax.legend(handles=hs, fontsize=7.5, loc="upper left", frameon=True, framealpha=0.92)
    ax.set_title("Zone map v2 around La Pampa: please check these boundaries", loc="left", fontsize=11, fontweight="bold")
    ax.tick_params(labelsize=8)
    finish_figure(fig, f"Sources: {SRC}. La Pampa and 'across the road' have no official boundary: longitude window "
                       f"{rz.LP_LON}, corridor within {rz.ACROSS_KM:.0f} km north of the road. Description.",
                  OUT / "fig_v2_zone_map.png", rect_bottom=0.06)


def fig_stream(g):
    yrs = list(range(2010, 2026))
    w = g["new_land_ha"].unstack("group").reindex(index=yrs, columns=list(GROUPS)).fillna(0)
    tot = w.sum(axis=1)
    fig, (a1, a2) = plt.subplots(2, 1, figsize=(11, 7.4), sharex=True, gridspec_kw={"height_ratios": [1.5, 1]})
    a1.stackplot(yrs, w.T.values, colors=[COL[c] for c in w.columns], edgecolor="white", linewidth=0.6,
                 labels=list(w.columns))
    for y in yrs:
        a1.text(y, tot[y] * 1.02, f"{tot[y] / 1000:.1f}k", ha="center", fontsize=7, color="#52514e")
    a1.set_ylabel("Land mined for the first time (ha)")
    a1.set_title("Land mined for the first time each year, Madre de Dios (stacked by zone; label = total)", loc="left", fontsize=10)
    a1.axvline(2018.5, color="#0b0b0b", lw=1.2); a1.text(2018.6, a1.get_ylim()[1] * 0.96, "Mercurio", fontsize=8, va="top")
    style_axes(a1)
    a1.legend(fontsize=7.5, frameon=False, loc="upper left", ncol=2)
    sh = w.div(tot, axis=0) * 100
    a2.stackplot(yrs, sh.T.values, colors=[COL[c] for c in sh.columns], edgecolor="white", linewidth=0.6)
    a2.set_ylim(0, 100); a2.set_ylabel("Share of the year's\nnewly mined land (%)")
    a2.axvline(2018.5, color="#0b0b0b", lw=1.2)
    style_axes(a2); a2.set_xticks(yrs); a2.set_xticklabels([f"'{str(y)[2:]}" for y in yrs], fontsize=8)
    fig.suptitle("After 2019 newly mined land shifted from La Pampa to the legal corridor",
                 x=0.01, ha="left", fontsize=11, fontweight="bold")
    finish_figure(fig, f"Source: {SRC}. Newly mined land = pixels mapped as mining for the first time since 1985 "
                       "(returns to old pits are in the Sankey). A shift in where newly mined land appears fits displacement but does "
                       "not prove that the same miners moved. Description.", OUT / "fig_v2_stream.png", rect_bottom=0.08)
    return w


def fig_sankey(g):
    """Per period: two sources (new land, old pits) -> zone groups. Band widths = mean ha per year."""
    from matplotlib.path import Path as MPath
    from matplotlib.patches import PathPatch
    fig, axes = plt.subplots(1, 3, figsize=(13, 5.6))
    vmax = 0
    data = {}
    for p, (a, b) in PERIODS.items():
        d = g.loc[a:b][["new_land_ha", "remined_ha"]].groupby("group").mean().reindex(list(GROUPS)).fillna(0)
        data[p] = d; vmax = max(vmax, d.values.sum())
    scale = 0.78 / vmax
    for ax, (p, d) in zip(axes, data.items()):
        ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
        src = {"New land": d.new_land_ha.sum(), "Return to old pits": d.remined_ha.sum()}
        # left nodes
        y = 0.86; left = {}
        for s, v in src.items():
            h = v * scale; left[s] = [y, y - h]; ax.add_patch(plt.Rectangle((0.02, y - h), 0.05, h, color="#52514e"))
            ax.text(0.02, y + 0.005, f"{s}\n{v:,.0f} ha/yr", fontsize=7.5, va="bottom"); y -= h + 0.08
        # right nodes
        y = 0.90; right = {}
        for grp in GROUPS:
            v = d.loc[grp].sum(); h = v * scale
            right[grp] = [y, y - h]
            ax.add_patch(plt.Rectangle((0.78, y - h), 0.05, h, color=COL[grp]))
            if v > vmax * 0.03:
                ax.text(0.85, y - h / 2, f"{grp}  {v:,.0f}", fontsize=7, va="center")
            y -= h + 0.012
        # flows
        for s, col in (("New land", "new_land_ha"), ("Return to old pits", "remined_ha")):
            for grp in GROUPS:
                v = d.loc[grp, col]; h = v * scale
                if h <= 0: continue
                y0a = left[s][0]; left[s][0] -= h
                y0b = right[grp][0]; right[grp][0] -= h
                verts = [(0.07, y0a), (0.42, y0a), (0.43, y0b), (0.78, y0b), (0.78, y0b - h), (0.43, y0b - h),
                         (0.42, y0a - h), (0.07, y0a - h), (0.07, y0a)]
                codes = [MPath.MOVETO, MPath.CURVE4, MPath.CURVE4, MPath.CURVE4, MPath.LINETO, MPath.CURVE4,
                         MPath.CURVE4, MPath.CURVE4, MPath.CLOSEPOLY]
                ax.add_patch(PathPatch(MPath(verts, codes), facecolor=COL[grp], alpha=0.45, lw=0))
        ax.set_title(f"{p}: {d.values.sum():,.0f} ha/yr of new mining", loc="left", fontsize=9.5)
    fig.suptitle("Where new mining came from (new land or old pits) and where it went, per period",
                 x=0.01, ha="left", fontsize=11, fontweight="bold")
    finish_figure(fig, f"Source: {SRC}. Widths = mean hectares per year in the period, same scale in all three panels. "
                       "'Return to old pits' = mining on pixels that were mining in an earlier year but not the year before "
                       "(includes some year-to-year map flicker, about 300 ha/yr in La Pampa before 2019). "
                       "Flows are pixels changing class, not people moving. Description.", OUT / "fig_v2_sankey.png", rect_bottom=0.08)
    return data


def fig_road_bands():
    b = pd.read_csv(rz.OUT_BAND)
    b["new_ha"] = b.new_land_ha                     # first-ever mining (robust to year-to-year flicker)
    fig, axes = plt.subplots(1, 3, figsize=(13, 4.2), sharey=True)
    res = {}
    for ax, (p, (a, c)) in zip(axes, PERIODS.items()):
        d = b[b.year.between(a, c)].groupby("km_from_road").new_ha.mean()
        res[p] = d
        ax.bar(d.index + 0.5, d.values, width=0.92, color=["#2a78d6" if k >= 0 else "#eb6834" for k in d.index])
        ax.axvline(0, color="black", lw=1.6)
        n, s = d[d.index >= 0].sum(), d[d.index < 0].sum()
        ax.set_title(f"{p}: south {s:,.0f} | north {n:,.0f} ha/yr", loc="left", fontsize=9.5)
        ax.set_xlabel("km from the highway (south < 0 < north)")
        style_axes(ax)
    axes[0].set_ylabel("Land mined for the first time\nper year (ha), per 1-km band")
    fig.legend(handles=[Patch(color="#eb6834", label="South of the road: buffer zone side (La Pampa)"),
                        Patch(color="#2a78d6", label="North of the road: legal corridor side")],
               loc="lower center", ncol=2, fontsize=8, frameon=False, bbox_to_anchor=(0.5, 0.12))
    fig.suptitle("Crossing the road: after 2019 newly mined land shifted to the north side of the highway",
                 x=0.01, ha="left", fontsize=11, fontweight="bold")
    finish_figure(fig, f"Source: {SRC}. Only the La Pampa longitudes ({rz.LP_LON}); bands of 1 km measured north-south from "
                       "the highway. Description.", OUT / "fig_v2_road_bands.png", rect_bottom=0.24)
    return res


def fig_corridor_share(g):
    yrs = list(range(2005, 2026))
    w = g["new_land_ha"].unstack("group").reindex(index=yrs).fillna(0)
    cor = w["Corridor across the road"] + w["Rest of mining corridor"]
    share = cor / w.sum(axis=1) * 100
    fig, ax = plt.subplots(figsize=(9, 3.8))
    ax.plot(yrs, share, color="#2a78d6", lw=2, marker="o", ms=4)
    ax.axvline(2018.5, color="#0b0b0b", lw=1.2); ax.text(2018.6, 95, "Mercurio", fontsize=8, va="top")
    ax.set_ylim(0, 100); ax.set_ylabel("% of newly mined land\ninside the legal corridor")
    style_axes(ax); ax.set_xticks(yrs[::2])
    ax.set_title("Share of newly mined land in Madre de Dios inside the legal corridor (communities counted separately)",
                 loc="left", fontsize=10)
    finish_figure(fig, f"Source: {SRC}. Corridor = D.L. 1100 polygon (INGEMMET, referential) minus native communities. "
                       "Inside the corridor mining can be legal; outside it is presumed illegal. Description.",
                  OUT / "fig_v2_corridor_share.png", rect_bottom=0.12)
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
        reg.add(f"v2_road_north_{k}", d[d.index >= 0].sum(), "ha/yr", f"First-time mined land per year 0-15 km NORTH of the highway (La Pampa longitudes), {p}", "description", SRC)
        reg.add(f"v2_road_south_{k}", d[d.index < 0].sum(), "ha/yr", f"First-time mined land per year 0-15 km SOUTH of the highway (La Pampa longitudes), {p}", "description", SRC)
        reg.add(f"v2_corridor_share_{k}", sh.loc[a:b].mean(), "percent", f"Share of first-time mined land inside the legal corridor (excl. communities), {p}", "description", SRC)
    for nm, v in o25.items():
        reg.add("v2_check_" + "".join(ch for ch in nm.lower() if ch.isalnum()) + "_2025", v, "ha",
                f"Raster v2 mining 2025, {nm} (publisher check)", "description", SRC)
    print(w.loc[2014:].round(0).to_string())
