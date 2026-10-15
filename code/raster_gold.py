"""Was there gold left? A depletion proxy per registry zone. DESCRIPTION only (plan v3 zones).

Nobody publishes how much gold is left in the ground. Proxy: gold in Madre de Dios is alluvial (river gravels and old
terraces), so "gold-bearing land" = these geology units of the INGEMMET 1:100,000 map (GEOCATMIN, layer 6):
  strict = Qh-al (alluvial deposit), Q-al, Q-alfl, Q-fl (fluvial deposit)
  broad  = strict + NQ-md/s (Madre de Dios Formation, upper member: holds the gold-bearing terraces)
Validation (registered): the share of all land ever mined (1985-2025) in Madre de Dios that lies on these units.
Depletion of a zone in year Y = gold-bearing land already mined (first mapped as mining) by Y / gold-bearing land in
the zone. This is a STOCK concept on first-time mining (land once mined stays "used"); it is not an additions measure.
If La Pampa still had most of its gold-bearing land unmined in 2018, "miners left because the gold ran out" is unlikely.
Limits: geology is a 1:100k map (coarse); gold grade varies inside a unit; already-mined land can be re-mined.
Inputs: data_intermediate/zones_mdd.tif (registry zone code, first-mined year, tenure; raster_zones.py);
data_raw/ingemmet/geologia_100k_mdd_tiles/*.geojson.
Outputs: data_intermediate/gold_depletion.csv (zone x definition), cell_gold.csv (per 1-km cell of cell_attr.csv:
gold-bearing share, share of it mined by 2018), output/v2_gold_depletion.csv.
"""
from __future__ import annotations
import glob
import warnings
import numpy as np
import pandas as pd

from common import ROOT, OUT
import definitions as D
import raster_zones as rz

GEOL = ROOT / "data_raw" / "ingemmet" / "geologia_100k_mdd_tiles"
OUT_CSV = ROOT / "data_intermediate" / "gold_depletion.csv"
OUT_CELL = ROOT / "data_intermediate" / "cell_gold.csv"
STRICT = {"Qh-al", "Q-al", "Q-alfl", "Q-fl"}
BROAD_EXTRA = {"NQ-md/s"}
SRC = "INGEMMET GEOCATMIN geology 1:100k (layer 6) x MapBiomas Peru Col 4 rasters (first year mined), zone registry"
YEARS = (D.REF_YEAR, D.YEARS[1])
REPORT = ["mdd", "lapampa", "tambopata_bz_rest", "corridor_across", "corridor_rest", "amarakaeri_bz", "communities",
          "tambopata_bz_kotsimba"]


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
    from raster_layers import zone_raster, pixel_ha
    zone, first, ten, t, mdd = zone_raster()
    geo = geology_mask(t, zone.shape)
    pix = pixel_ha(t, zone.shape)
    inz = zone > 0
    kots = list(D.TENURE.values()).index("kotsimba")
    units = {"mdd": inz & mdd, **{k: zone == c for k, c in D.ZONE_CODE.items()},
             "tambopata_bz_kotsimba": np.isin(zone, [D.ZONE_CODE[s] for s in D.UNITS["tambopata_bz"]]) & (ten == kots)}
    rows = []
    for name, gm in (("strict", geo == 1), ("broad", geo >= 1)):
        for u, um in units.items():
            ever = um & (first > 0)
            rows.append(dict(unit=u, definition=name, area_ha=pix[um].sum(), gold_land_ha=pix[gm & um].sum(),
                             mined_ever_ha=pix[ever].sum(), mined_ever_on_gold_ha=pix[ever & gm].sum(),
                             **{f"gold_mined_by_{y}_ha": pix[gm & ever & (first <= y)].sum() for y in YEARS}))
    d = pd.DataFrame(rows)
    for y in YEARS:
        d[f"depleted_share_{y}"] = d[f"gold_mined_by_{y}_ha"] / d.gold_land_ha
        d[f"gold_left_{y}_ha"] = d.gold_land_ha - d[f"gold_mined_by_{y}_ha"]
    d["mining_on_gold_share"] = d.mined_ever_on_gold_ha / d.mined_ever_ha
    d.to_csv(OUT_CSV, index=False)
    # per 1-km cell (same ids as cell_attr.csv: raster_zones.cell_key on the same grid and region)
    cell, sub = rz.cell_key(t, zone.shape, inz)
    k = cell.ravel(); n = int(cell.max()) + 1
    w_ = pix.ravel(); gb = (geo >= 1).ravel()
    area = np.bincount(k, weights=w_, minlength=n)
    gold = np.bincount(k, weights=w_ * gb, minlength=n)
    m18 = ((first > 0) & (first <= D.REF_YEAR)).ravel()
    gold_m18 = np.bincount(k, weights=w_ * gb * m18, minlength=n)
    cc = pd.DataFrame({"cell": np.arange(n), "gold_share": gold / np.where(area > 0, area, np.nan),
                       "gold_depleted_2018": gold_m18 / np.where(gold > 0, gold, np.nan)})
    cc[cc.cell > 0].round(4).to_csv(OUT_CELL, index=False)


def run(reg):
    print("\n== gold-left proxy (zone registry) ==")
    if not (OUT_CSV.exists() and OUT_CELL.exists()):
        if not (rz.OUT_FULL.exists() and GEOL.exists()):
            warnings.warn("raster_gold: inputs missing; skipping"); return
        build()
    d = pd.read_csv(OUT_CSV)
    d.round(3).to_csv(OUT / "v2_gold_depletion.csv", index=False)
    print(d[["unit", "definition", "gold_land_ha", "depleted_share_2018", "gold_left_2018_ha", "depleted_share_2025",
             "mining_on_gold_share"]].round(2).to_string(index=False))
    name = lambda u: D.UNIT_NAME.get(u, D.ZONE_NAME.get(u, "Kotsimba land inside the Tambopata buffer zone"))
    for _, r in d[d.unit.isin(REPORT)].iterrows():
        nm = name(r.unit)
        reg.add(f"gold_{r.definition}_{r.unit}_depleted_2018", r.depleted_share_2018, "share",
                f"Share of gold-bearing land ({r.definition}) already mined (first mapped as mining) by 2018, {nm}",
                "description", SRC, measure="stock", zone=r.unit, period="by 2018")
        reg.add(f"gold_{r.definition}_{r.unit}_left_2018_ha", r.gold_left_2018_ha, "ha",
                f"Gold-bearing land ({r.definition}) never mapped as mining by 2018, {nm}", "description", SRC,
                measure="gold-bearing land never mined", zone=r.unit, period="2018")
        reg.add(f"gold_{r.definition}_{r.unit}_depleted_2025", r.depleted_share_2025, "share",
                f"Share of gold-bearing land ({r.definition}) mined by 2025, {nm}", "description", SRC,
                measure="stock", zone=r.unit, period="by 2025")
        if r.unit == "mdd":
            land_share = r.gold_land_ha / r.area_ha
            reg.add(f"gold_{r.definition}_land_share_mdd", land_share, "share",
                    f"Share of Madre de Dios covered by {r.definition} gold-bearing units (validation baseline)",
                    "description", SRC, measure="geology", zone="mdd", period="map")
            reg.add(f"gold_{r.definition}_lift", r.mining_on_gold_share / land_share, "ratio",
                    f"Lift: share of mining on {r.definition} units divided by their share of the department "
                    "(1 = no better than random)", "description", SRC, measure="stock", zone="mdd", period="1985-2025")
            reg.add(f"gold_{r.definition}_validation", r.mining_on_gold_share, "share",
                    f"Validation: share of all land ever mined 1985-2025 in Madre de Dios that lies on {r.definition} "
                    "gold-bearing units", "description", SRC, measure="stock", zone="mdd", period="1985-2025")
    return d
