"""Plan v2, step S3b: was there gold left? A depletion proxy per zone. DESCRIPTION only.

Nobody publishes how much gold is left in the ground. Proxy: gold in Madre de Dios is alluvial (river gravels and old
terraces), so "gold-bearing land" = these geology units of the INGEMMET 1:100,000 map (GEOCATMIN, layer 6):
  strict = Qh-al (alluvial deposit), Q-al, Q-alfl, Q-fl (fluvial deposit)
  broad  = strict + NQ-md/s (Madre de Dios Formation, upper member: holds the gold-bearing terraces)
Validation (printed and registered): the share of all land ever mined (1985-2025) that lies on these units.
Depletion of a zone in year Y = gold-bearing land already mined by Y / gold-bearing land in the zone.
If La Pampa still had most of its gold-bearing land unmined in 2018, "miners left because the gold ran out" is unlikely.
Limits: geology is a 1:100k map (coarse); gold grade varies inside a unit; already-mined land can be re-mined.
Inputs: data_intermediate/zones_v2_mdd_full.tif (zone code + first-mined year, from raster_zones.py);
data_raw/ingemmet/geologia_100k_mdd_tiles/*.geojson. Output: data_intermediate/gold_depletion_v2.csv (+ output copy).
"""
from __future__ import annotations
import glob
import warnings
import numpy as np
import pandas as pd

from common import ROOT, OUT
import raster_zones as rz

GEOL = ROOT / "data_raw" / "ingemmet" / "geologia_100k_mdd_tiles"
OUT_CSV = ROOT / "data_intermediate" / "gold_depletion_v2.csv"
OUT_CELL = ROOT / "data_intermediate" / "cell_gold_v2.csv"
STRICT = {"Qh-al", "Q-al", "Q-alfl", "Q-fl"}
BROAD_EXTRA = {"NQ-md/s"}
SRC = ("INGEMMET GEOCATMIN geology 1:100k (layer 6) x MapBiomas Peru Col 4 rasters (first year mined), "
       "zones v2")
YEARS = (2018, 2025)
AREA_MDD_HA = 8_500_000.0      # placeholder, replaced in run() by the raster area of Madre de Dios


def geology_mask(transform, shape):
    import geopandas as gpd
    from rasterio.features import rasterize
    fs = sorted(glob.glob(str(GEOL / "*.geojson")))
    g = pd.concat([gpd.read_file(f) for f in fs]).drop_duplicates("OBJECTID")
    g = gpd.GeoDataFrame(g, crs=4326)
    cls = np.where(g.NAME.isin(STRICT), 1, np.where(g.NAME.isin(BROAD_EXTRA), 2, 0))
    shapes = [(geom, int(c)) for geom, c in zip(g.geometry, cls) if c > 0]
    return rasterize(shapes, out_shape=shape, transform=transform, fill=0, dtype="uint8")


def build():
    import rasterio
    with rasterio.open(rz.OUT_FULL) as r:
        zone, first, t = r.read(1), r.read(2), r.transform
    geo = geology_mask(t, zone.shape)
    lat = t.f + (np.arange(zone.shape[0]) + 0.5) * t.e
    pix = np.broadcast_to(((abs(t.a) * 111320 * np.cos(np.radians(lat))) * (abs(t.e) * 110574) / 1e4)[:, None], zone.shape)
    rows = []
    inz = zone > 0
    for name, gm in (("strict", geo == 1), ("broad", geo >= 1)):
        ever = (first > 0) & inz
        rows.append(dict(zone_code=0, unit="ALL Madre de Dios", definition=name,
                         gold_land_ha=pix[gm & inz].sum(), mined_ever_ha=pix[ever].sum(),
                         mined_ever_on_gold_ha=pix[ever & gm].sum(),
                         **{f"gold_mined_by_{y}_ha": pix[gm & inz & (first > 0) & (first <= y)].sum() for y in YEARS}))
        for c, nm in rz.ZONES.items():
            zz = zone == c
            rows.append(dict(zone_code=c, unit=nm, definition=name, gold_land_ha=pix[gm & zz].sum(),
                             mined_ever_ha=pix[zz & (first > 0)].sum(), mined_ever_on_gold_ha=pix[zz & (first > 0) & gm].sum(),
                             **{f"gold_mined_by_{y}_ha": pix[gm & zz & (first > 0) & (first <= y)].sum() for y in YEARS}))
    d = pd.DataFrame(rows)
    for y in YEARS:
        d[f"depleted_share_{y}"] = d[f"gold_mined_by_{y}_ha"] / d.gold_land_ha
        d[f"gold_left_{y}_ha"] = d.gold_land_ha - d[f"gold_mined_by_{y}_ha"]
    d["mining_on_gold_share"] = d.mined_ever_on_gold_ha / d.mined_ever_ha
    d.to_csv(OUT_CSV, index=False)
    # per 1-km cell: share of gold-bearing land (broad) and share already mined by 2018 (for the cell panel, v2_stats.py)
    cell, sub = rz.cell_key(t, zone.shape, zone > 0)
    k = cell.ravel(); n = int(cell.max()) + 1
    w_ = pix.ravel()
    gb = (geo >= 1).ravel()
    area = np.bincount(k, weights=w_, minlength=n)
    gold = np.bincount(k, weights=w_ * gb, minlength=n)
    m18 = ((first > 0) & (first <= 2018)).ravel()
    gold_m18 = np.bincount(k, weights=w_ * gb * m18, minlength=n)
    cc = pd.DataFrame({"cell": np.arange(n), "gold_share": gold / np.where(area > 0, area, np.nan),
                       "gold_depleted_2018": gold_m18 / np.where(gold > 0, gold, np.nan)})
    cc[cc.cell > 0].round(4).to_csv(OUT_CELL, index=False)


def run(reg):
    print("\n== v2 gold-left proxy ==")
    if not (OUT_CSV.exists() and OUT_CELL.exists()):
        if not (rz.OUT_FULL.exists() and GEOL.exists()):
            warnings.warn("raster_gold: inputs missing; skipping"); return
        build()
    global AREA_MDD_HA
    d = pd.read_csv(OUT_CSV)
    import rasterio
    with rasterio.open(rz.OUT_FULL) as r_:
        z_ = r_.read(1); t_ = r_.transform
    lat_ = t_.f + (np.arange(z_.shape[0]) + 0.5) * t_.e
    AREA_MDD_HA = float(((z_ > 0) * (((abs(t_.a) * 111320 * np.cos(np.radians(lat_))) * (abs(t_.e) * 110574) / 1e4)[:, None])).sum())
    d.round(3).to_csv(OUT / "v2_gold_depletion.csv", index=False)
    print(d[["unit", "definition", "gold_land_ha", "depleted_share_2018", "gold_left_2018_ha", "depleted_share_2025",
             "mining_on_gold_share"]].round(2).to_string(index=False))
    for _, r in d.iterrows():
        key = "".join(ch for ch in r.unit.lower() if ch.isalnum())[:18]
        if r.zone_code in (0, 5, 6, 7, 3, 9):
            reg.add(f"gold_{r.definition}_{key}_depleted_2018", r.depleted_share_2018, "share",
                    f"Share of gold-bearing land ({r.definition}) already mined by 2018, {r.unit}", "description", SRC)
            reg.add(f"gold_{r.definition}_{key}_left_2018_ha", r.gold_left_2018_ha, "ha",
                    f"Gold-bearing land ({r.definition}) not yet mined in 2018, {r.unit}", "description", SRC)
            reg.add(f"gold_{r.definition}_{key}_depleted_2025", r.depleted_share_2025, "share",
                    f"Share of gold-bearing land ({r.definition}) mined by 2025, {r.unit}", "description", SRC)
        if r.zone_code == 0:
            mdd_ha = d[(d.definition == r.definition) & (d.zone_code > 0)].gold_land_ha.sum() / r.gold_land_ha if False else None
            reg.add(f"gold_{r.definition}_land_share_mdd", r.gold_land_ha / AREA_MDD_HA, "share",
                    f"Share of Madre de Dios covered by {r.definition} gold-bearing units (validation baseline)", "description", SRC)
            reg.add(f"gold_{r.definition}_lift", r.mining_on_gold_share / (r.gold_land_ha / AREA_MDD_HA), "ratio",
                    f"Lift: share of mining on {r.definition} units divided by their share of the department (1 = no better than random)", "description", SRC)
            reg.add(f"gold_{r.definition}_validation", r.mining_on_gold_share, "share",
                    f"Validation: share of all land ever mined 1985-2025 in Madre de Dios that lies on {r.definition} gold-bearing units",
                    "description", SRC)
    return d
