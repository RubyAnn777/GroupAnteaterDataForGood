"""Plan v3: descriptive displacement layers from the ONE raster accounting (raster_zones.py). DESCRIPTION only.

Outcome (definitions.OUTCOME): NET mining additions, ha/yr = new land + re-mined - stopped, MapBiomas Peru Collection 4
rasters, our pixel accounting. Zones: definitions.ZONES, read from data_intermediate/zone_year.csv (zone x tenure x
in_mdd x year); department figures keep only land inside Madre de Dios (in_mdd = 1), so the Cusco part of the
Amarakaeri buffer zone is not in them. Treatment: definitions.PERIODS (2016-18 / 2019-21 / later years 2022-25).

Figures
  fig_v2_zone_map.png        the zone registry around La Pampa (team checkpoint: are the boundaries right?)
  fig_v2_stream.png          where net additions appear each year, Madre de Dios, by zone group (bars; parts in the
                             small multiples below)
  fig_v2_parts_by_zone.png   small multiples: net = new + re-mined - stopped for La Pampa, across the road, the rest of
                             the corridor and native communities (one panel per zone)
  fig_v2_sankey.png          per period: land newly mined or re-mined (gross inflow) to zones; stopped and net named
  fig_v2_road_bands.png      crossing the road: net additions by 1-km distance band south/north of the highway
  fig_v2_corridor_share.png  share of Madre de Dios additions on corridor land (D.L. 1100 tenure), net and new land
The pixels cannot show people moving: a shift in WHERE mining is added fits displacement but also new arrivals, the
gold price or a different deposit. We say "the mix shifted", never "miners moved".

Shared helpers for the other raster modules (glad_alerts, raster_gold, v2_legality, v2_products_check, v2_extra):
GROUPS (display groups of registry slugs), group_of(), zone_raster() (zone slug codes, first-mined year, tenure,
transform, Madre de Dios mask from zones_mdd.tif), pixel_ha().
"""
from __future__ import annotations
import warnings
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from matplotlib.lines import Line2D

from common import (ROOT, OUT, style_axes, finish_figure, headline, label_end, callout, period_band,
                    set_year_ticks, add_event_markers, EVENT_TITLE_PAD, C, INK, INK2, MUTED, SURFACE, AXIS)
import definitions as D
import zonedata as Z
import raster_zones as rz

SRC = (f"{D.SOURCE}; zones: SERNANP, INGEMMET D.L. 1100, RAISG roads, MapBiomas Amazonia native communities "
       "(registry: definitions.ZONES)")
# display groups = unions of registry zones (definitions.ZONES slugs); fixed order and colours
GROUPS = {
    "La Pampa sector": ["lapampa"],
    "Corridor across the road": ["corridor_across"],
    "Rest of mining corridor": ["corridor_rest"],
    "Native communities": ["communities"],
    "Rest of Tambopata buffer zone": ["tambopata_bz_rest"],
    "Amarakaeri buffer zone": ["amarakaeri_bz"],
    "Other buffer zones": ["bahuaja_bz", "other_bz"],
    "Reserves and parks": ["tambopata_nr", "other_anp"],
    "Rest of Madre de Dios": ["rest_mdd"],
}
GKEY = {"La Pampa sector": "lapampa", "Corridor across the road": "corridor_across",
        "Rest of mining corridor": "corridor_rest", "Native communities": "communities",
        "Rest of Tambopata buffer zone": "tambopata_bz_rest", "Amarakaeri buffer zone": "amarakaeri_bz",
        "Other buffer zones": "other_bz", "Reserves and parks": "protected", "Rest of Madre de Dios": "rest_mdd"}
COL = {"La Pampa sector": C["lapampa"], "Corridor across the road": C["corridor"], "Rest of mining corridor": C["corridor_rest"],
       "Native communities": C["native"], "Rest of Tambopata buffer zone": C["lapampa_tint"],
       "Amarakaeri buffer zone": C["buffer"], "Other buffer zones": C["buffer_tint"],
       "Reserves and parks": C["reserve"], "Rest of Madre de Dios": C["other"]}
SHORT = {"La Pampa sector": "La Pampa", "Corridor across the road": "Corridor across the road",
         "Rest of mining corridor": "Rest of the legal corridor", "Native communities": "Native communities",
         "Rest of Tambopata buffer zone": "Rest of Tambopata buffer zone",
         "Amarakaeri buffer zone": "Amarakaeri buffer zone (Madre de Dios part)", "Other buffer zones": "Other buffer zones",
         "Reserves and parks": "Reserves and parks", "Rest of Madre de Dios": "Rest of Madre de Dios"}
PER = ("pre", "during", "later")
MEAS = ["net"] + D.PARTS
FLOW = ["mining_ha", "net_ha", "new_ha", "remined_ha", "stopped_ha"]


def group_of(slug: str) -> str:
    return {s: g for g, ss in GROUPS.items() for s in ss}.get(slug, "")


def code_group() -> dict[int, str]:
    """zone code (definitions.ZONE_CODE) -> display group."""
    return {D.ZONE_CODE[s]: g for g, ss in GROUPS.items() for s in ss}


def pixel_ha(t, shape) -> np.ndarray:
    return np.broadcast_to(rz.row_area(t, shape[0])[:, None], shape)


def mdd_mask(t, shape) -> np.ndarray:
    """Madre de Dios polygon (geoBoundaries ADM1) on a grid, rasterized exactly as raster_zones does (in_mdd)."""
    import geopandas as gpd
    dep = gpd.read_file(rz.RAW / "geoboundaries/geoBoundaries-PER-ADM1.geojson").to_crs(4326)
    return rz.rasterizer(shape, t)([dep[dep.shapeName == "Madre de Dios"].geometry.union_all()])


def zone_raster():
    """zones_mdd.tif: zone code (definitions.ZONES), first year mapped as mining (0 = never), tenure code; plus the
    transform and the Madre de Dios mask. The region = Madre de Dios + the whole Tambopata and Amarakaeri BZs."""
    import rasterio
    with rasterio.open(rz.OUT_FULL) as r:
        zone, first, ten, t = r.read(1), r.read(2), r.read(3), r.transform
    return zone, first, ten, t, mdd_mask(t, zone.shape)


def load():
    """Zone-year table inside Madre de Dios, with display group; and the group x year sums."""
    z = pd.read_csv(rz.OUT_ZONE)
    z = z[z.in_mdd == 1].copy()
    z["grp"] = z.zone.map(group_of)
    assert z.grp.ne("").all()
    g = z.groupby(["year", "grp"])[FLOW].sum(min_count=1)
    return z, g


def pmean(s: pd.Series, p: str) -> float:
    return Z.period_mean(s, p)


# --------------------------------------------------------------------------- figures
def fig_zone_map():
    import rasterio
    with rasterio.open(rz.OUT_WIN) as r:
        zone, first, ten = r.read(1), r.read(2), r.read(3); b = r.bounds
    ext = (b.left, b.right, b.bottom, b.top)
    code_col = {c: COL[g] for c, g in code_group().items()}
    bg = [int(SURFACE[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    rgb = np.ones(zone.shape + (3,)) * bg
    for c, hx in code_col.items():
        rgb[zone == c] = [int(hx[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    rgb = 1 - 0.5 * (1 - rgb)                               # pale zone fill
    kots = ten == list(D.TENURE.values()).index("kotsimba")
    rgb[kots] = 1 - 0.75 * (1 - rgb[kots])                  # Kotsimba (inside the BZ): lighter, outlined below
    rgb[first > 0] = [0.17, 0.2, 0.22]                      # every pixel ever mined, dark ink
    fig, ax = plt.subplots(figsize=(9, 6.7))
    headline(fig, "One mining belt split by a road: La Pampa in the buffer zone, the land across it in the legal corridor",
             "Zone registry around La Pampa (dark = land ever mapped as mining, 1985–2025). Team check: are these boundaries right?")
    ax.imshow(rgb, extent=ext, interpolation="nearest")
    ax.contour(np.flipud(kots.astype(float)), levels=[0.5], extent=ext, colors=[C["native"]], linewidths=0.9, origin="lower")
    L = rz.layers()
    L["ioh"].plot(ax=ax, color=INK, lw=2.4)
    ax.set_xlim(b.left, b.right); ax.set_ylim(b.bottom, b.top); ax.set_aspect(1 / np.cos(np.radians(-12.9)))
    for x in D.LP_LON:
        ax.axvline(x, color=INK2, ls=(0, (2, 2)), lw=0.9)
    box = dict(facecolor="white", alpha=0.85, edgecolor="none", pad=2.0)
    for nm, (x, y) in {"La Pampa sector": (-69.97, -13.025), "Corridor across\nthe road": (-69.97, -12.80),
                       "Kotsimba (native community,\ninside the buffer zone)": (-70.25, -13.075),
                       "Tambopata reserve": (-69.80, -13.09)}.items():
        ax.text(x, y, nm, fontsize=9, fontweight="medium", ha="center", va="center", color=INK, bbox=box)
    ax.text(-69.70, -12.855, "Interoceanic\nHighway", fontsize=8.5, ha="center", va="center", color=INK, bbox=box)
    ax.text(D.LP_LON[0] + 0.005, b.top - 0.012, "← La Pampa window →", fontsize=7.5, color=INK2, va="top", ha="left",
            bbox=dict(facecolor="white", alpha=0.7, edgecolor="none", pad=1))
    ax.tick_params(labelsize=8)
    ax.set_xlabel("Longitude (°)"); ax.set_ylabel("Latitude (°)")
    for sp in ax.spines.values():
        sp.set_visible(True); sp.set_color(AXIS)
    present = {D.CODE_ZONE.get(int(c)) for c in np.unique(zone) if c > 0}
    hs = [Patch(facecolor=COL[g], alpha=0.5, label=SHORT[g]) for g, ss in GROUPS.items() if set(ss) & present]
    hs += [Patch(facecolor="#2b3338", label="Ever mapped as mining"),
           Line2D([], [], color=C["native"], lw=0.9, label="Kotsimba (tenure tag)"),
           Line2D([], [], color=INK, lw=2.4, label="Interoceanic Highway"),
           Line2D([], [], color=INK2, ls=(0, (2, 2)), lw=0.9, label="La Pampa longitudes (70.15–69.80 W)")]
    fig.legend(handles=hs, loc="lower center", ncol=4, bbox_to_anchor=(0.5, 0.075), fontsize=8, handlelength=1.4,
               columnspacing=1.2)
    finish_figure(fig, f"{SRC}. La Pampa and 'across the road' have no official boundary: longitude window "
                       f"{D.LP_LON}, corridor within {D.ACROSS_KM:.0f} km north of the road. Official buffer zones are kept "
                       "whole; Kotsimba and corridor land inside them are tenure tags. Description.",
                  OUT / "fig_v2_zone_map.png", rect_bottom=0.20)


def fig_stream(g):
    """Net additions by zone group, Madre de Dios, stacked bars (positive groups up, negative groups down)."""
    yrs = list(range(2010, 2026))
    w = g["net_ha"].unstack("grp").reindex(index=yrs, columns=list(GROUPS)).fillna(0)
    tot = w.sum(axis=1)
    # the ONE corridor-share definition (as fig_corridor_share and v2_corridor_share_*_net): corridor-tenure land, any zone
    zz = Z._zone_year(); zz = zz[zz.in_mdd == 1]
    cor = zz[zz.tenure == "corridor"].groupby("year").net_ha.sum(); tt = zz.groupby("year").net_ha.sum()
    share = {p: cor.loc[slice(*D.PERIODS[p])].sum() / tt.loc[slice(*D.PERIODS[p])].sum() for p in PER}
    fig, ax = plt.subplots(figsize=(9, 5.6))
    headline(fig, f"After 2019 most net additions landed on legal-corridor land "
                  f"({share['pre']:.0%} → {share['during']:.0%} of the department's)",
             "Net mining additions (new land + re-mined − stopped), Madre de Dios, ha/yr, stacked by zone, 2010–2025.\n"
             "Shaded: Mercurio and what followed (2019–21). Numbers: yearly total.")
    period_band(ax, D.PERIODS["during"][0] - 0.5, D.PERIODS["during"][1] + 0.5)
    pos = np.zeros(len(yrs)); neg = np.zeros(len(yrs))
    for grp in w.columns:
        v = w[grp].values
        up = np.clip(v, 0, None); dn = np.clip(v, None, 0)
        ax.bar(yrs, up, bottom=pos, color=COL[grp], width=0.78, edgecolor=SURFACE, linewidth=0.8)
        ax.bar(yrs, dn, bottom=neg, color=COL[grp], width=0.78, edgecolor=SURFACE, linewidth=0.8)
        pos += up; neg += dn
    ax.axhline(0, color=INK2, lw=0.8)
    for y in (2016, 2018, 2021, 2023, 2025):
        ax.annotate(f"{tot[y]:,.0f}", xy=(y, pos[yrs.index(y)]), xytext=(0, 4), textcoords="offset points",
                    ha="center", va="bottom", fontsize=8, color=INK2, fontweight="medium")
    ax.legend(handles=[Patch(color=COL[g_], label=SHORT[g_]) for g_ in GROUPS], loc="upper left",
              bbox_to_anchor=(0.0, 0.93), fontsize=7.5, ncol=1)
    ax.set_ylim(min(neg.min() * 1.2, -200), pos.max() * 1.15); ax.set_xlim(2009.4, 2025.6)
    ax.set_ylabel("Net additions, ha/yr")
    style_axes(ax); ax.set_xticks(yrs); ax.set_xticklabels([f"'{str(y)[2:]}" for y in yrs])
    add_event_markers(ax, label=True); ax.set_title(" ", pad=EVENT_TITLE_PAD)
    finish_figure(fig, f"{SRC}. Madre de Dios part only. Net additions = stock(t) − stock(t−1); groups with a net loss "
                       "are drawn below zero. A shift in where land is added fits displacement but does not prove that the "
                       "same miners moved. Description.", OUT / "fig_v2_stream.png", event_note=True)
    return w


def fig_parts(g):
    """Small multiples: net and its three parts, one panel per zone (coordinator rule: parts never next to La Pampa's
    orange line; zone named in the panel title)."""
    yrs = list(range(2010, 2026))
    show = ["La Pampa sector", "Corridor across the road", "Rest of mining corridor", "Native communities"]
    W = {m: g[D.COLS[m]].unstack("grp").reindex(index=yrs) for m in MEAS}
    lp = {p: pmean(W["net"]["La Pampa sector"], p) for p in ("pre", "during")}
    ac = {p: pmean(W["net"]["Corridor across the road"], p) for p in ("pre", "during")}
    fig, axes = plt.subplots(2, 2, figsize=(9, 6.6), sharex=True, gridspec_kw={"hspace": 0.55, "wspace": 0.22})
    headline(fig, f"Net additions 2016–18 → 2019–21: La Pampa {lp['pre']:,.0f} → {lp['during']:,.0f} ha/yr, "
                  f"across the road {ac['pre']:,.0f} → {ac['during']:,.0f}",
             "Net mining additions = new land + re-mined − stopped, ha/yr, 2010–2025, one panel per zone (own scale)")
    for i, (ax, grp) in enumerate(zip(axes.ravel(), show)):
        new, rem, stp, net = (W[m][grp].values for m in ("new", "remined", "stopped", "net"))
        period_band(ax, D.PERIODS["during"][0] - 0.5, D.PERIODS["during"][1] + 0.5)
        ax.bar(yrs, new, color=C["new"], width=0.75, edgecolor=SURFACE, linewidth=0.6)
        ax.bar(yrs, rem, bottom=new, color=C["remined"], width=0.75, edgecolor=SURFACE, linewidth=0.6)
        ax.bar(yrs, -stp, color=C["stopped"], width=0.75, edgecolor=SURFACE, linewidth=0.6)
        ax.plot(yrs, net, color=INK, lw=1.8, marker="o", ms=3.5, mec=SURFACE, zorder=4)
        ax.axhline(0, color=INK2, lw=0.7)
        ax.set_title(SHORT[grp], fontsize=10)
        style_axes(ax)
        ax.set_xticks(yrs[::3]); ax.set_xticklabels([str(y) for y in yrs[::3]])
        if i == 0:
            ax.legend(handles=[Patch(color=C["new"], label="New land"), Patch(color=C["remined"], label="Re-mined"),
                               Patch(color=C["stopped"], label="− Stopped"),
                               Line2D([], [], color=INK, lw=1.8, marker="o", ms=3.5, label="Net additions")],
                      loc="upper left", fontsize=7.5, ncol=2)
    finish_figure(fig, f"{SRC}. Madre de Dios part. Shaded: 2019–21 (Mercurio and what followed). Stopped = land that "
                       "left the mining class (flooded, regrowing, abandoned or reclassified), drawn below zero. Description.",
                  OUT / "fig_v2_parts_by_zone.png")


def fig_sankey(g):
    """Per period: two sources (new land, re-mined) -> zone groups. Band widths = mean ha/yr (same scale). Gross inflow:
    stopped land is NOT in the flows; the period's stopped and net totals are written next to each panel."""
    from matplotlib.path import Path as MPath
    from matplotlib.patches import PathPatch
    data = {}; vmax = 0; side = {}
    for p in PER:
        a, b = D.PERIODS[p]
        d = g.loc[a:b][["new_ha", "remined_ha"]].groupby("grp").mean().reindex(list(GROUPS)).fillna(0)
        data[p] = d; vmax = max(vmax, d.values.sum())
        side[p] = g.loc[a:b][["stopped_ha", "net_ha"]].groupby("year").sum().mean()
    hr = [d.values.sum() / vmax + 0.2 for d in data.values()]
    fig, axes = plt.subplots(3, 1, figsize=(9, 9.6), gridspec_kw={"height_ratios": hr, "hspace": 0.25})
    r_ = {p: data[p].remined_ha.sum() / data[p].values.sum() for p in PER}
    headline(fig, f"Land newly mined or re-mined grew {data['later'].values.sum() / data['pre'].values.sum():.1f}-fold "
                  f"by 2022–25; re-mined share {r_['pre']:.0%} → {r_['later']:.0%}",
             "Gross inflow (not net): mean ha/yr newly mined or re-mined, by origin (left) and zone (right), Madre de "
             "Dios.\nStopped land and net additions are named under each period.")
    unit = 1.0 / vmax
    for ax, (p, d), h_ax in zip(axes, data.items(), hr):
        ax.set_xlim(0, 1); ax.set_ylim(-0.02, h_ax); ax.axis("off")
        top = h_ax - 0.12
        src = {"New land": d.new_ha.sum(), "Re-mined": d.remined_ha.sum()}
        y = top; left = {}
        for s_, v in src.items():
            h = v * unit; left[s_] = [y, y - h]
            ax.add_patch(plt.Rectangle((0.20, y - h), 0.018, h, color=C["new"] if s_ == "New land" else C["remined"], lw=0))
            ax.text(0.19, y - h / 2, f"{s_}\n{v:,.0f} ha/yr", fontsize=8.5, va="center", ha="right", color=INK)
            y -= h + 0.035
        gap = 0.008
        right = {}; y = top
        for grp in GROUPS:
            v = d.loc[grp].sum(); h = v * unit
            right[grp] = [y, y - h]
            ax.add_patch(plt.Rectangle((0.66, y - h), 0.018, h, color=COL[grp], lw=0))
            y -= h + gap
        small = ["Rest of Tambopata buffer zone", "Amarakaeri buffer zone", "Other buffer zones", "Reserves and parks",
                 "Rest of Madre de Dios"]
        last = None
        for grp in GROUPS:
            if grp in small: continue
            v = d.loc[grp].sum(); yc = (right[grp][0] + right[grp][1]) / 2
            if last is not None and last - yc < 0.05: yc = last - 0.05
            ax.text(0.695, yc, f"{SHORT[grp]}  ", fontsize=8.5, va="center", ha="left", color=INK)
            ax.text(0.99, yc, f"{v:,.0f}", fontsize=8.5, va="center", ha="right", color=INK, fontweight="medium")
            last = yc
        sv = sum(d.loc[g_].sum() for g_ in small)
        ys = (right[small[0]][0] + right[small[-1]][1]) / 2
        if last is not None and last - ys < 0.05: ys = last - 0.05
        ax.text(0.695, ys, "Five small zones", fontsize=8, va="center", ha="left", color=INK2)
        ax.text(0.99, ys, f"{sv:,.0f}", fontsize=8, va="center", ha="right", color=INK2)
        for s_, col in (("New land", "new_ha"), ("Re-mined", "remined_ha")):
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
        ax.text(0.0, h_ax - 0.02, D.period_label(p), fontsize=11, fontweight="medium", color=INK, va="top")
        ax.text(0.11, h_ax - 0.028, f"{d.values.sum():,.0f} ha/yr newly mined or re-mined  − {side[p].stopped_ha:,.0f} "
                                    f"stopped  = {side[p].net_ha:,.0f} net", fontsize=8.5, color=INK2, va="top")
        ax.text(0.99, h_ax - 0.02, "ha/yr", fontsize=8, color=INK2, va="top", ha="right")
    finish_figure(fig, f"{SRC}. Madre de Dios part. Re-mined = mining on pixels mapped as mining in an earlier year but "
                       "not the year before (includes some year-to-year map flicker). Five small zones = rest of Tambopata "
                       "buffer zone, Amarakaeri (Madre de Dios part), other buffer zones, reserves and parks, rest of Madre "
                       "de Dios. Flows are pixels changing class, not people moving. Description.", OUT / "fig_v2_sankey.png")
    return data, side


def fig_road_bands():
    b = pd.read_csv(rz.OUT_BAND)
    fig, axes = plt.subplots(1, 3, figsize=(9, 4.2), sharey=True)
    res = {}
    for p in PER:
        a, c = D.PERIODS[p]
        res[p] = b[b.year.between(a, c)].groupby("km_from_road")[[D.COLS[m] for m in MEAS]].mean()
    n = {p: res[p].loc[res[p].index >= 0, "net_ha"].sum() for p in PER}
    s = {p: res[p].loc[res[p].index < 0, "net_ha"].sum() for p in PER}
    headline(fig, f"In 2019–21 net additions moved north of the highway: south {s['pre']:,.0f} → "
                  f"{s['during']:,.0f}, north {n['pre']:,.0f} → {n['during']:,.0f} ha/yr",
             "Net mining additions per year, ha, per 1-km band from the highway (La Pampa longitudes only). "
             "Beyond 10 km north = deeper in the corridor")
    for ax, p in zip(axes, PER):
        d = res[p].net_ha
        ax.bar(d.index + 0.5, d.values, width=0.86, color=[C["corridor"] if k >= 0 else C["lapampa"] for k in d.index], lw=0)
        ax.axvline(0, color=INK, lw=1.4); ax.axhline(0, color=INK2, lw=0.6)
        ax.axvspan(10, 30, color="#efece5", zorder=-1, lw=0)
        ax.set_xlim(-20, 30)
        ax.set_title(D.period_label(p), pad=20)
        ax.text(0, 1.02, f"south {s[p]:,.0f}  ·  north {n[p]:,.0f} ha/yr", transform=ax.transAxes, fontsize=8, color=INK2,
                va="bottom", ha="left")
        ax.set_xlabel("km from the highway")
        style_axes(ax)
    ymax = axes[0].get_ylim()[1]
    axes[0].text(-2, ymax * 0.97, "← south:\nLa Pampa side", fontsize=8, color=INK, ha="right", va="top")
    axes[0].text(2, ymax * 0.97, "north: →\ncorridor side", fontsize=8, color=INK, ha="left", va="top")
    axes[0].set_ylabel("Net additions, ha/yr per 1-km band")
    axes[0].text(20, ymax * 0.97, "> 10 km north:\ndeeper in the\ncorridor", fontsize=7.5, color=INK2, ha="center", va="top")
    finish_figure(fig, f"{SRC}. Only the La Pampa longitudes ({D.LP_LON}), all land in the bands (every zone); 1-km bands "
                       "measured north-south from the highway, −30 to +30 km; the shaded part (more than 10 km north) lies "
                       "beyond the 'corridor across the road' zone. Description.", OUT / "fig_v2_road_bands.png")
    return res


def fig_corridor_share(z):
    """Share of Madre de Dios additions on corridor-tenure land (D.L. 1100 polygon minus native communities, any zone),
    net and new land. Period values = ratio of period sums (additive), yearly points = that year's ratio."""
    yrs = list(range(2005, 2026))
    cor = z[z.tenure == "corridor"].groupby("year")[["net_ha", "new_ha"]].sum().reindex(yrs)
    tot = z.groupby("year")[["net_ha", "new_ha"]].sum().reindex(yrs)
    share = cor / tot * 100
    per = {p: (cor.loc[slice(*D.PERIODS[p])].sum() / tot.loc[slice(*D.PERIODS[p])].sum() * 100) for p in PER}
    fig, ax = plt.subplots(figsize=(9, 4.4))
    headline(fig, f"The corridor's share of net additions: {per['pre'].net_ha:.0f}% (2016–18), "
                  f"{per['during'].net_ha:.0f}% (2019–21), {per['later'].net_ha:.0f}% (2022–25)",
             "Share of Madre de Dios mining additions on legal-corridor land (D.L. 1100, native communities excluded), %, "
             "2005–2025.\nDark: net additions; light: new land (first-time mining)")
    period_band(ax, D.PERIODS["during"][0] - 0.5, D.PERIODS["during"][1] + 0.5)
    ax.text(np.mean(D.PERIODS["during"]), 3, "Mercurio and what followed", ha="center", fontsize=7.5, color=INK2)
    ax.plot(yrs, share.new_ha, color=C["corridor_rest"], lw=1.6, zorder=3)
    ax.plot(yrs, share.new_ha, "o", color=C["corridor_rest"], ms=3.5, mec="white", mew=0.8, zorder=4)
    ax.plot(yrs, share.net_ha, color=C["corridor"], lw=2.2, zorder=3)
    ax.plot(yrs, share.net_ha, "o", color=C["corridor"], ms=4.5, mec="white", mew=1.0, zorder=4)
    up = share.new_ha.iloc[-1] >= share.net_ha.iloc[-1]
    label_end(ax, yrs[-1], share.net_ha.iloc[-1], "Net additions", C["corridor"], dx=8, dy=-6 if up else 6)
    label_end(ax, yrs[-1], share.new_ha.iloc[-1], "New land", C["corridor_rest"], dx=8, dy=6 if up else -6, weight="normal")
    for p in PER:
        a, b = D.PERIODS[p]
        m = per[p].net_ha
        ax.plot([a - 0.35, b + 0.35], [m] * 2, color=C["corridor"], lw=5, alpha=0.2, solid_capstyle="butt", zorder=2)
        ax.text((a + b) / 2, 104, f"{D.period_label(p)}", ha="center", va="bottom", fontsize=8, color=INK2)
        ax.text((a + b) / 2, 103, f"net {m:.0f}% · new {per[p].new_ha:.0f}%", ha="center", va="top", fontsize=8.5,
                color=INK, fontweight="medium")
    ax.set_ylim(0, 112); ax.set_xlim(2004.5, 2026.8); ax.set_yticks(range(0, 101, 20)); ax.set_ylabel("% of additions")
    style_axes(ax); ax.set_xticks(yrs[::2])
    finish_figure(fig, f"{SRC}. Corridor = land tagged corridor tenure (D.L. 1100 polygon, INGEMMET, referential, minus "
                       "native communities), in any zone. Period values = sum over the period's years of corridor additions "
                       "divided by the sum of all additions. Inside the corridor mining can be legal; outside it is "
                       "presumed illegal. Description.", OUT / "fig_v2_corridor_share.png")
    return share, per


# --------------------------------------------------------------------------- entry point
def run(reg):
    print("\n== v3 descriptive layers (raster registry, net additions) ==")
    if not rz.OUT_ZONE.exists():
        warnings.warn("raster_layers: zone_year.csv missing; skipping"); return
    z, g = load()
    ru = Z.region_units().set_index(["unit", "year"]).mining_ha
    import checks
    checks.check("Raster v3: Tambopata buffer zone mining 2025, ha (course table 20,730)", ru["tambopata_bz", 2025], 20730, tol=60)
    checks.check("Raster v3: Tambopata reserve mining 2025, ha (platform 777)", ru["tambopata_nr", 2025], 777, tol=5)
    checks.check("Raster v3: Madre de Dios mining 2025, ha (course table 112,622)", ru["mdd", 2025], 112622, tol=300)
    checks.save()
    for u, nm in (("tambopata_bz", "tambopatabufferzone"), ("tambopata_nr", "tambopatareserve"), ("mdd", "madrededios")):
        reg.add(f"v2_check_{nm}_2025", ru[u, 2025], "ha", f"Mining area (stock) 2025, {D.UNIT_NAME[u]}, raster "
                "(publisher check)", "description", SRC, measure="stock", zone=u, period="2025")
    fig_zone_map()
    fig_stream(g)
    fig_parts(g)
    sk, side = fig_sankey(g)
    rb = fig_road_bands()
    sh, shp = fig_corridor_share(z)
    g.reset_index().round(1).to_csv(OUT / "v2_group_year.csv", index=False)
    # Period means by display group (Madre de Dios part). Units already in definitions.UNITS are registered by peru.py
    # (e.g. lapampa_pre_net); here only the groups that are not reporting units, and the shares / bands.
    for grp in ("Amarakaeri buffer zone", "Other buffer zones", "Reserves and parks"):
        d = g.xs(grp, level="grp")
        for p in PER:
            Z.register_parts(reg, f"v2_{GKEY[grp]}_mdd_{p}", {m: pmean(d[D.COLS[m]], p) for m in MEAS},
                             f"{GKEY[grp]} (Madre de Dios part)", D.period_label(p), "mean per year", source=SRC)
    for p in PER:
        lab = D.period_label(p)
        reg.add(f"v2_remined_share_{p}", sk[p].remined_ha.sum() / sk[p].values.sum(), "share",
                f"Re-mined land as a share of land newly mined or re-mined (gross inflow), Madre de Dios, {lab}",
                "description", SRC, measure="remined", zone="mdd", period=lab)
        for k in ("net", "new"):
            reg.add(f"v2_corridor_share_{p}_{k}", shp[p][D.COLS[k]] / 100, "share",
                    f"Share of Madre de Dios {D.MEASURE_NAME[k].lower()} on legal-corridor land (D.L. 1100 tenure, native "
                    f"communities excluded), {lab}: period sum / period sum", "description", SRC, measure=k, zone="mdd",
                    period=lab)
        d = rb[p]
        for side_, sel in (("north", d.index >= 0), ("south", d.index < 0)):
            Z.register_parts(reg, f"v2_road_{side_}_{p}", {m: d.loc[sel, D.COLS[m]].sum() for m in MEAS},
                             f"road bands 0-30 km {side_} of the highway, La Pampa longitudes", lab,
                             "sum over 1-km bands of the mean per year", source=SRC)
            v = {m: d.loc[sel, D.COLS[m]].sum() for m in MEAS}
            assert abs(v["net"] - (v["new"] + v["remined"] - v["stopped"])) < 0.01
    ex = [y for y in range(D.PERIODS["later"][0], D.PERIODS["later"][1] + 1) if y != D.LATER_EX]
    for k in ("net", "new"):
        cor = z[z.tenure == "corridor"].groupby("year")[D.COLS[k]].sum()
        tot = z.groupby("year")[D.COLS[k]].sum()
        reg.add(f"v2_corridor_share_later_ex2023_{k}", cor.loc[ex].sum() / tot.loc[ex].sum(), "share",
                f"Same share of {D.MEASURE_NAME[k].lower()}, later years without the 2023 spike year (2022, 2024, 2025)",
                "description", SRC, measure=k, zone="mdd", period="2022, 2024, 2025")
    print(g["net_ha"].unstack("grp").loc[2014:].round(0).to_string())
