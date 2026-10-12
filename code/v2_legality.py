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

from common import ROOT, OUT, style_axes, finish_figure
import raster_zones as rz

LAYER = ROOT / "data_raw" / "amw_github" / "illegality_v2_areas_simplified.geojson"
OUT_CSV = ROOT / "data_intermediate" / "legality_year_v2.csv"
LEVELS = {1: "Low (active concession)", 2: "Medium (concession not verified)", 3: "High (outside any concession)",
          4: "Very high (strict protected area)", 0: "Not classified"}
COL = {1: "#1baf7a", 2: "#eda100", 3: "#eb6834", 4: "#b3261e", 0: "#b9b8b2"}
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


def run(reg):
    print("\n== v2 legality levels ==")
    if not OUT_CSV.exists():
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
    c = d[d.corridor].groupby("level").ha.sum(); c = c / c.sum()
    reg.add("leg_corridor_low_share", c.get(1, 0), "share", "Inside the legal corridor: share of first-time mining (1986-2025) in active concessions (Low)", "description", SRC)
    reg.add("leg_corridor_highish_share", c.get(2, 0) + c.get(3, 0), "share", "Inside the legal corridor: share in Medium or High (no verified active concession)", "description", SRC)
    fig, ax = plt.subplots(figsize=(10, 4.2))
    ax.stackplot(sh.index, (sh * 100).T.values, colors=[COL[c_] for c_ in sh.columns], labels=[LEVELS[c_] for c_ in sh.columns],
                 edgecolor="white", linewidth=0.5)
    ax.axvline(2018.5, color="black", lw=1.2); ax.set_ylim(0, 100); style_axes(ax)
    ax.set_ylabel("% of first-time mining"); ax.set_xticks(list(sh.index)); ax.tick_params(axis="x", labelsize=8)
    ax.legend(fontsize=7.5, frameon=False, loc="upper left", bbox_to_anchor=(1.0, 1.0))
    ax.set_title("Legality of new mining in Madre de Dios: the presumed-illegal share fell after 2019", loc="left", fontsize=10.5, fontweight="bold")
    finish_figure(fig, f"Source: {SRC}. Today's concessions applied to all years; 'not classified' = outside the layer. "
                       "Description.", OUT / "fig_v2_legality.png", rect_bottom=0.1)
    print((sh * 100).round(0).loc[2014:].to_string())
