"""Legality levels (MAAP #235 / Amazon Mining Watch) for every pixel of first-time mining in Madre de Dios.

Layer: Amazon Mining Watch GitHub repo (earthrise-media/mining-detector), illegality_v2_areas_simplified.geojson,
field illegality: 1 Low (inside an active concession), 2 Medium (concession not verified as active), 3 High
(outside any concession), 4 Very high (protected area without any resource use). MAAP #235 defines the levels.
The layer reproduces the INGEMMET cadastre (docs/overnight/notes/legality_data.md): Low = titled rights, Medium =
blocked/extinct/in process, High = outside every right.
Method: rasterize the levels onto the MapBiomas grid (data_intermediate/zones_v2_mdd_full.tif) and cross them with the
year each pixel was first mapped as mining (1985-2025). Output: first-time mining by level and year.
Limits: TODAY's concessions applied to past years (a concession granted in 2022 makes 2018 mining look "Low");
pixels outside the layer = "not classified". DESCRIPTION.
"""
from __future__ import annotations
import warnings
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from common import ROOT, OUT, style_axes, finish_figure, headline, label_end, add_event_markers, PERU_EVENTS, INK, INK2, SURFACE
import raster_zones as rz

LAYER = ROOT / "data_raw" / "amw_github" / "illegality_v2_areas_simplified.geojson"
OUT_CSV = ROOT / "data_intermediate" / "legality_year_v2.csv"
CADASTRE = sorted((ROOT / "data_raw" / "ingemmet" / "catastro_minero_wgs84_L0_mdd_bbox").glob("chunk_*.geojson"))
OUT_TC = ROOT / "data_intermediate" / "legality_year_v2_timeconsistent.csv"
LEVELS = {1: "Low (active concession)", 2: "Medium (concession not verified)", 3: "High (outside any concession)",
          4: "Very high (strict protected area)", 0: "Not classified"}
COL = {1: "#e4e1da", 2: "#b3b9b6", 3: "#5d7479", 4: "#1f2d33", 0: "#f1efea"}   # one-hue ordinal ramp: low -> very high presumption of illegality
SRC = "Amazon Mining Watch / MAAP #235 legality layer (GitHub earthrise-media/mining-detector) x MapBiomas Peru Col 4 first-mined year"


def build():
    import geopandas as gpd, rasterio
    from rasterio.features import rasterize
    with rasterio.open(rz.OUT_FULL) as r:
        zone, first, t = r.read(1), r.read(2), r.transform
    g = gpd.read_file(LAYER, bbox=rz.BBOX)
    g = g[g.illegality.notna() & g.geometry.notna()].sort_values("illegality")   # higher levels burned last -> win on overlaps
    lev = rasterize([(geom, int(v)) for geom, v in zip(g.geometry, g.illegality)], out_shape=zone.shape,
                    transform=t, fill=0, dtype="uint8")
    lat = t.f + (np.arange(zone.shape[0]) + 0.5) * t.e
    pix = np.broadcast_to(((abs(t.a) * 111320 * np.cos(np.radians(lat))) * (abs(t.e) * 110574) / 1e4)[:, None], zone.shape)
    m = (first >= 1986) & (zone > 0)
    df = pd.DataFrame({"year": first[m], "level": lev[m], "corridor": np.isin(zone[m], [5, 6]), "ha": pix[m]})
    out = df.groupby(["year", "level", "corridor"]).ha.sum().reset_index()
    out.to_csv(OUT_CSV, index=False)
    # time-consistent version (critical review): a pixel counts as "inside a concession" only if a concession covering it
    # had been FILED (FEC_DENU) by the year the pixel was first mined; otherwise Low/Medium -> High.
    if CADASTRE:
        c = pd.concat([gpd.read_file(f)[["FEC_DENU", "geometry"]] for f in CADASTRE])
        c = c[c.FEC_DENU.notna()]
        c["fy"] = pd.to_datetime(c.FEC_DENU, unit="ms").dt.year
        c = c.sort_values("fy", ascending=False)                 # earliest filing burned last -> wins
        fy = rasterize([(g_, int(y)) for g_, y in zip(c.geometry, c.fy)], out_shape=zone.shape, transform=t, fill=0, dtype="int16")
        f_ = fy[m]; lv = lev[m].copy()
        later = np.isin(lv, [1, 2]) & ((f_ == 0) | (f_ > first[m]))
        lv[later] = 3
        tc = pd.DataFrame({"year": first[m], "level": lv, "ha": pix[m]}).groupby(["year", "level"]).ha.sum().reset_index()
        tc.to_csv(OUT_TC, index=False)


def run(reg):
    print("\n== v2 legality levels ==")
    if not (OUT_CSV.exists() and OUT_TC.exists()):
        if not (LAYER.exists() and rz.OUT_FULL.exists()):
            warnings.warn("v2_legality: inputs missing; skipping"); return
        build()
    d = pd.read_csv(OUT_CSV)
    w = d.groupby(["year", "level"]).ha.sum().unstack().fillna(0).reindex(columns=[1, 2, 3, 4, 0], fill_value=0).loc[2010:2025]
    sh = w.div(w.sum(axis=1), axis=0)
    for p, (a, b) in {"2016_18": (2016, 2018), "2019_21": (2019, 2021), "2022_25": (2022, 2025)}.items():
        s = w.loc[a:b].sum(); s = s / s.sum()
        for k, nm in (("low", 1), ("medium", 2), ("high", 3), ("veryhigh", 4)):
            reg.add(f"leg_{k}_share_{p}", s[nm], "share", f"Share of first-time mining in Madre de Dios at legality level {LEVELS[nm]}, {p}", "description", SRC)
        reg.add(f"leg_illegal_share_{p}", s[3] + s[4], "share", f"Share of first-time mining at High or Very high presumption of illegality, {p}", "description", SRC)
    if OUT_TC.exists():
        tc = pd.read_csv(OUT_TC).groupby(["year", "level"]).ha.sum().unstack().fillna(0)
        for p, (a, b) in {"2016_18": (2016, 2018), "2019_21": (2019, 2021), "2022_25": (2022, 2025)}.items():
            s_ = tc.loc[a:b].sum(); s_ = s_ / s_.sum()
            reg.add(f"leg_tc_illegal_share_{p}", s_.get(3, 0) + s_.get(4, 0), "share", f"Time-consistent: High + Very high share of first-time mining (concession filed by the mining year), {p}", "description", SRC)
            reg.add(f"leg_tc_medium_share_{p}", s_.get(2, 0), "share", f"Time-consistent: Medium share, {p}", "description", SRC)
    c = d[d.corridor].groupby("level").ha.sum(); c = c / c.sum()
    reg.add("leg_corridor_low_share", c.get(1, 0), "share", "Inside the legal corridor: share of first-time mining (1986-2025) in active concessions (Low)", "description", SRC)
    reg.add("leg_corridor_highish_share", c.get(2, 0) + c.get(3, 0), "share", "Inside the legal corridor: share in Medium or High (no verified active concession)", "description", SRC)
    ill = {p: (lambda t: (t[3] + t[4]) / t.sum())(w.loc[a:b].sum()) for p, (a, b) in
           {"2016–18": (2016, 2018), "2019–21": (2019, 2021), "2022–25": (2022, 2025)}.items()}
    cols = [c_ for c_ in sh.columns if sh[c_].max() > 0]                  # "not classified" is empty here
    fig, ax = plt.subplots(figsize=(9, 4.6))
    headline(fig, f"Presumed-illegal new mining fell from {ill['2016–18']:.0%} to {ill['2022–25']:.0%} of the total",
             "First-time mining in Madre de Dios by MAAP legality level, share of each year's hectares (%). "
             f"High + Very high: {' → '.join(f'{v:.0%}' for v in ill.values())}")
    ax.stackplot(sh.index, (sh[cols] * 100).T.values, colors=[COL[c_] for c_ in cols], edgecolor=SURFACE, linewidth=0.8)
    ax.set_ylim(0, 100); ax.set_xlim(sh.index[0], sh.index[-1]); style_axes(ax)
    last = sh.index[-1]; cum = 0.0
    for c_ in cols:
        v = sh.loc[last, c_] * 100
        if v >= 4:
            label_end(ax, last, cum + v / 2, LEVELS[c_], COL[c_], dx=8, fontsize=8)
        elif c_ == 4:
            label_end(ax, last, cum + v / 2 + 2, LEVELS[c_], COL[c_], dx=8, fontsize=8, va="bottom")
        cum += v
    add_event_markers(ax, label=True, events=[PERU_EVENTS[0]])
    ax.lines[-1].set_zorder(3); ax.lines[-1].set_color(SURFACE); ax.lines[-1].set_linewidth(1.3)   # visible on the dark band
    ax.set_title("Share of first-time mining (%)", pad=16)
    ax.set_xticks(list(sh.index)); ax.set_xticklabels([f"'{str(y)[2:]}" for y in sh.index])
    finish_figure(fig, f"{SRC}. Today's concessions applied to all years (a time-consistent version using filing dates gives the "
                       "same fall). Description.", OUT / "fig_v2_legality.png")
    print((sh * 100).round(0).loc[2014:].to_string())
