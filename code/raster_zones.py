"""Plan v2, steps S1-S2: one zone map on the MapBiomas grid, and yearly pixel accounting per zone (Madre de Dios).

WHY: the course tables only exist for whole buffer zones and departments. The MapBiomas Peru Collection 4 rasters
(30 m, 1985-2025, the SAME product as the course tables) let us count mining inside any boundary we choose, on one grid.
Check: the raster reproduces the published totals (Tambopata BZ 2025, Tambopata NR 2025, Madre de Dios 2025).

ZONES (exclusive; each pixel gets the FIRST zone in this order that contains it):
   1 Tambopata NR (reserve)              SERNANP ANP RN09
   2 Other reserves and parks            other SERNANP ANP (Bahuaja-Sonene, Amarakaeri RC, Manu, ...)
   3 Kotsimba (native community)         MapBiomas Amazonia / RAISG territories
   4 Other native communities            same layer (Peru, inside Madre de Dios)
   5 Corridor across the road            D.L. 1100 corridor (INGEMMET), north of the Interoceanic Highway, within
                                          ACROSS_KM of the road and inside the La Pampa longitudes (opposite La Pampa)
   6 Rest of the mining corridor         D.L. 1100 corridor
   7 La Pampa sector                     Tambopata BZ (RN09) inside the La Pampa longitudes (LP_LON)
   8 Rest of Tambopata buffer zone       Tambopata BZ (RN09)
   9 Amarakaeri buffer zone              SERNANP ZA RC03
  10 Bahuaja-Sonene buffer zone          SERNANP ZA PN08 (the part not already in the Tambopata BZ)
  11 Other buffer zones                  other SERNANP ZA
  12 Rest of Madre de Dios               department polygon (geoBoundaries ADM1)
La Pampa and the "across the road" corridor have NO official boundary: we use a longitude window (LP_LON) chosen
from the map of first-mined years (docs: PLAN_v2 S1) and report two alternatives (LP_ALT) as sensitivity.
Communities come before the corridor: MAAP #208 reports community mining separately (some concessions lie inside).

PIXEL ACCOUNTING per zone and year t (a pixel is "mining" if class == 30):
  mining_ha        mining area at t
  new_land_ha      mining at t, never mining in any earlier year (first ever)        -> expansion onto new land
  remined_ha       mining at t, not at t-1, but mining in some year before t-1        -> return to old scars
  stopped_ha       mining at t-1, not at t                                             -> abandoned or regrown (or reclass.)
  from_forest_ha   mining at t, forest (classes 3,4,5,6) at t-1                        -> forest lost to mining
Identity (asserted): mining(t) - mining(t-1) = new_land + remined - stopped.
The course measure "additions" = mining(t) - mining(t-1); new_land and remined split it, which answers Ruby's
re-mining question: additions can be small while miners return to old pits.

ROAD BANDS (crossing the road): inside the La Pampa longitudes, every pixel gets its signed distance to the
Interoceanic Highway (km; north positive), in 1-km bands -15..+15. Counted per year like the zones.

Inputs (big, git-ignored): data_raw/mapbiomas_peru_raster/*.tif, data_raw/sernanp, data_raw/ingemmet, data_raw/raisg
(roads), data_raw/mapbiomas_amazonia/INDIGENOUS_TERRITORIES.zip, data_raw/geoboundaries.
Outputs (small, committed): data_intermediate/zone_year_v2.csv, road_band_year_v2.csv, official_unit_year_v2.csv,
zones_v2_lapampa_window.tif (zone codes + first-mined year, La Pampa window, for maps).
"""
from __future__ import annotations
import time
import warnings

import numpy as np
import pandas as pd

from common import ROOT

RAW = ROOT / "data_raw"
INTER = ROOT / "data_intermediate"
RASTER = RAW / "mapbiomas_peru_raster" / "peru_coverage-col4_{y}.tif"
YEARS = list(range(1985, 2026))
MINING, FOREST = 30, (3, 4, 5, 6)
BBOX = (-72.45, -13.40, -68.60, -9.85)            # Madre de Dios department envelope (lon/lat)
LP_LON = (-70.15, -69.80)                           # La Pampa longitudes (main definition)
LP_ALT = {"narrow": (-70.10, -69.85), "wide": (-70.20, -69.75)}
ACROSS_KM = 10.0
WINDOW = (-70.35, -13.12, -69.65, -12.72)           # map window for figures
STUDY = (-70.65, -13.30, -69.30, -12.40)            # 1-km cell panel window (La Pampa, corridor, Amarakaeri edge, reserve)
CELL_PX = 33                                        # 33 x 30 m ~ 1 km cells
BAND_KM = 30                                        # road bands -30..+30 km
ZONES = {1: "Tambopata reserve", 2: "Other reserves and parks", 3: "Kotsimba (native community)",
         4: "Other native communities", 5: "Corridor across the road", 6: "Rest of mining corridor",
         7: "La Pampa sector", 8: "Rest of Tambopata buffer zone", 9: "Amarakaeri buffer zone",
         10: "Bahuaja-Sonene buffer zone", 11: "Other buffer zones", 12: "Rest of Madre de Dios"}
OUT_ZONE = INTER / "zone_year_v2.csv"
OUT_BAND = INTER / "road_band_year_v2.csv"
OUT_OFF = INTER / "official_unit_year_v2.csv"
OUT_SENS = INTER / "zone_year_v2_lapampa_alt.csv"
OUT_WIN = INTER / "zones_v2_lapampa_window.tif"
OUT_CELL = INTER / "cell_year_v2.csv.gz"            # 1-km cell x year accounting (study window)
OUT_CELLATTR = INTER / "cell_attr_v2.csv"            # cell centre, majority zone, road and river distance
OUT_FULL = INTER / "zones_v2_mdd_full.tif"        # full grid: band 1 zone code, band 2 first-mined year (git-ignored)


def layers():
    """All boundary layers in EPSG:4326."""
    import geopandas as gpd
    anp = gpd.read_file(RAW / "sernanp/anp_definitivas.geojson").to_crs(4326)
    za = gpd.read_file(RAW / "sernanp/zonas_amortiguamiento.geojson").to_crs(4326)
    cor = gpd.read_file(RAW / "ingemmet/corredor_minero_madre_de_dios_DL1100.geojson").to_crs(4326)
    roads = gpd.read_file(RAW / "raisg/vias_nacionales_mdd_box.geojson")
    ioh = roads[roads.sigla == "PE-30C"].to_crs(4326)                     # Interoceanic Highway (IIRSA Sur)
    dep = gpd.read_file(RAW / "geoboundaries/geoBoundaries-PER-ADM1.geojson").to_crs(4326)
    mdd = dep[dep.shapeName == "Madre de Dios"].geometry.union_all()
    ti_zip, ti_mdd = RAW / "mapbiomas_amazonia/INDIGENOUS_TERRITORIES.zip", INTER / "native_communities_mdd.geojson"
    if ti_zip.exists():                    # 59 MB, git-ignored; the Madre de Dios subset is committed as ti_mdd
        ti = gpd.read_file("zip://" + str(ti_zip)).to_crs(4326)
        ti = ti[ti.geometry.intersects(mdd) & ti.LEVEL_1.eq("Comunidad Nativa")]
        ti.to_file(ti_mdd, driver="GeoJSON")
    else:
        ti = gpd.read_file(ti_mdd)
    return dict(anp=anp, za=za, cor=cor.geometry.union_all(), ioh=ioh, ti=ti, mdd=mdd)


def grid():
    import rasterio
    from rasterio.windows import from_bounds
    r = rasterio.open(str(RASTER).format(y=2025))
    from rasterio.windows import Window
    w = from_bounds(*BBOX, r.transform).round_offsets().round_lengths()
    w = w.intersection(Window(0, 0, r.width, r.height))          # the national raster ends at lon -68.64
    t = r.window_transform(w)
    lat = t.f + (np.arange(w.height) + 0.5) * t.e
    row_ha = (abs(t.a) * 111320 * np.cos(np.radians(lat))) * (abs(t.e) * 110574) / 1e4   # ha per pixel, by row
    return w, t, row_ha


def signed_road_km(t, shape, ioh, lon_win):
    """Signed distance (km) to the Interoceanic Highway for pixels inside lon_win; north of the road positive.
    Equal-area metres via ESRI:102033; sign from the road's latitude at the pixel's longitude."""
    import geopandas as gpd
    from shapely.ops import unary_union
    from shapely.geometry import LineString
    line = unary_union(ioh.geometry)
    cols = np.arange(shape[1]); rows = np.arange(shape[0])
    lon = t.c + (cols + 0.5) * t.a; lat = t.f + (rows + 0.5) * t.e
    cmask = (lon >= lon_win[0]) & (lon <= lon_win[1])
    rmask = (lat >= -13.45) & (lat <= -12.25)
    out = np.full(shape, np.nan, np.float32)
    # road latitude at each longitude (northern-most crossing is irrelevant here: the road runs W-E in this window)
    xs = lon[cmask]
    road_lat = []
    for x in xs:
        v = LineString([(x, -13.5), (x, -12.3)]).intersection(line)
        pts = [p for p in getattr(v, "geoms", [v]) if not p.is_empty]
        road_lat.append(np.mean([p.y for p in pts]) if pts else np.nan)
    road_lat = np.array(road_lat)
    la = lat[rmask][:, None]
    out[np.ix_(rmask, cmask)] = ((la - road_lat[None, :]) * 110.574).astype(np.float32)   # km, N positive
    return out


def build_zones(L, w, t):
    from rasterio.features import rasterize
    from shapely.geometry import box
    shape = (w.height, w.width)
    R = lambda geoms: rasterize([(g, 1) for g in geoms if g is not None and not g.is_empty], out_shape=shape,
                                transform=t, fill=0, dtype="uint8").astype(bool)
    anp, za, ti = L["anp"], L["za"], L["ti"]
    mdd = R([L["mdd"]])
    tnr = R(anp[anp.anp_codi == "RN09"].geometry)
    oanp = R(anp[anp.anp_codi != "RN09"].geometry)
    kots = R(ti[ti.LEVEL_2 == "Kotsimba"].geometry)
    comm = R(ti[ti.LEVEL_2 != "Kotsimba"].geometry)
    cor = R([L["cor"]])
    tbz = R(za[za.anp_codi == "RN09"].geometry)
    abz = R(za[za.anp_codi == "RC03"].geometry)
    bbz = R(za[za.anp_codi == "PN08"].geometry)
    obz = R(za[~za.anp_codi.isin(["RN09", "RC03", "PN08"])].geometry)
    dist = signed_road_km(t, shape, L["ioh"], (STUDY[0], STUDY[2]))
    lon = t.c + (np.arange(shape[1]) + 0.5) * t.a
    def lp_cols(win):
        m = np.zeros(shape, bool); m[:, (lon >= win[0]) & (lon <= win[1])] = True; return m
    def zone_map(win):
        lpc = lp_cols(win)
        across = cor & lpc & (dist > 0) & (dist <= ACROSS_KM)
        z = np.zeros(shape, np.uint8)
        order = [(1, tnr), (2, oanp), (3, kots), (4, comm), (5, across), (6, cor), (7, tbz & lpc), (8, tbz),
                 (9, abz), (10, bbz), (11, obz), (12, mdd)]
        for code, m in order:
            z[(z == 0) & m & mdd] = code
        return z
    zones = {"main": zone_map(LP_LON), **{k: zone_map(v) for k, v in LP_ALT.items()}}
    official = {"Tambopata buffer zone": tbz, "Tambopata reserve": tnr, "Amarakaeri buffer zone": abz,
                "Madre de Dios": mdd}
    lpc = lp_cols(LP_LON)
    band = np.full(shape, -99, np.int16)
    ok = lpc & mdd & ~np.isnan(dist) & (np.abs(dist) <= BAND_KM)
    band[ok] = np.floor(dist[ok]).astype(np.int16)                         # -30..29: band k = [k, k+1) km
    return zones, official, band, dist, mdd


def account(keys: dict[str, np.ndarray], row_ha, w):
    """Stream the 41 rasters once; per key map, per year: mining, new_land, remined, stopped, from_forest (ha)."""
    import rasterio
    shape = (w.height, w.width)
    prev = np.zeros(shape, bool); ever = np.zeros(shape, bool); before_prev = np.zeros(shape, bool)
    first = np.zeros(shape, np.int16)
    prev_forest = np.zeros(shape, bool)
    rows = {k: [] for k in keys}
    pix = np.broadcast_to(row_ha[:, None], shape)
    for y in YEARS:
        t0 = time.time()
        with rasterio.open(str(RASTER).format(y=y)) as r:
            a = r.read(1, window=w)
        mine = a == MINING
        forest = np.isin(a, FOREST)
        if y == YEARS[0]:
            cats = {"mining_ha": mine}
        else:
            new_land = mine & ~ever
            remined = mine & ~prev & before_prev
            cats = {"mining_ha": mine, "new_land_ha": new_land, "remined_ha": remined, "stopped_ha": prev & ~mine,
                    "from_forest_ha": mine & prev_forest}
        for k, km in keys.items():
            nk = int(km.max()) + 1
            rec = {"year": y}
            for c, m in cats.items():
                rec[c] = np.bincount(km[m].ravel(), weights=pix[m].ravel(), minlength=nk)
            rows[k].append(rec)
        first[(first == 0) & mine] = y
        before_prev |= prev          # mined in some year <= t-1 ... becomes "before t-1" next year
        ever |= mine
        prev, prev_forest = mine, forest
        print(f"  raster {y}: {time.time()-t0:.1f}s")
    return rows, first


def cell_key(t, shape, mdd):
    """1-km cells (CELL_PX x CELL_PX pixels) inside STUDY and Madre de Dios; id 1..n, 0 outside."""
    from rasterio.windows import from_bounds
    sub = from_bounds(*STUDY, t).round_offsets().round_lengths()
    r0, c0, h, w_ = int(sub.row_off), int(sub.col_off), int(sub.height), int(sub.width)
    nc = (w_ + CELL_PX - 1) // CELL_PX
    rr, cc = np.mgrid[0:h, 0:w_]
    k = np.zeros(shape, np.int32)
    k[r0:r0 + h, c0:c0 + w_] = (rr // CELL_PX) * nc + cc // CELL_PX + 1
    k[~mdd] = 0
    return k, (r0, c0, h, w_, nc)


def cell_attributes(cell, sub, t, zone, dist, row_ha):
    """Per cell: centre lon/lat, majority zone, mean signed road distance (km, N > 0), mean distance to the nearest
    river or lake pixel in 2018 (MapBiomas class 33, km), area (ha)."""
    import rasterio
    from scipy.ndimage import distance_transform_edt
    r0, c0, h, w_, nc = sub
    sl = (slice(r0, r0 + h), slice(c0, c0 + w_))
    # read the 2018 class map for the study window
    import rasterio.windows as rw
    with rasterio.open(str(RASTER).format(y=2018)) as r:
        full = rw.from_bounds(*BBOX, r.transform).round_offsets().round_lengths()
        a = r.read(1, window=rw.Window(full.col_off + c0, full.row_off + r0, w_, h))
    river = a == 33
    dr_km = distance_transform_edt(~river) * 0.030
    k = cell[sl].ravel(); n = int(cell.max()) + 1
    pix = np.broadcast_to(row_ha[r0:r0 + h, None], (h, w_)).ravel()
    cnt = np.bincount(k, minlength=n).astype(float); cnt[cnt == 0] = np.nan
    d = dist[sl].ravel(); dd = np.where(np.isnan(d), 0, d)
    road = np.bincount(k, weights=dd, minlength=n) / np.bincount(k, weights=(~np.isnan(d)).astype(float), minlength=n)
    riv = np.bincount(k, weights=dr_km.ravel(), minlength=n) / cnt
    area = np.bincount(k, weights=pix, minlength=n)
    z = zone[sl].ravel().astype(np.int64)
    zc = np.bincount(k * 16 + z, minlength=n * 16).reshape(n, 16); zc[:, 0] = 0
    maj = zc.argmax(axis=1)
    ids = np.arange(n)
    rows_, cols_ = (ids - 1) // nc, (ids - 1) % nc
    lon = t.c + (c0 + (cols_ + 0.5) * CELL_PX) * t.a
    lat = t.f + (r0 + (rows_ + 0.5) * CELL_PX) * t.e
    out = pd.DataFrame({"cell": ids, "lon": lon, "lat": lat, "zone": maj, "road_km": road, "river_km": riv, "area_ha": area})
    return out[(out.cell > 0) & (out.area_ha > 0)].round(4)


def tidy(rows, labels):
    out = []
    for rec in rows:
        n = len(rec["mining_ha"])
        for code in range(n):
            if code not in labels:
                continue
            d = {"year": rec["year"], "code": code, "unit": labels[code]}
            for c in ("mining_ha", "new_land_ha", "remined_ha", "stopped_ha", "from_forest_ha"):
                d[c] = float(rec[c][code]) if c in rec else np.nan
            out.append(d)
    return pd.DataFrame(out)


def build():
    import rasterio
    t0 = time.time()
    L = layers()
    w, t, row_ha = grid()
    zones, official, band, dist, mdd = build_zones(L, w, t)
    cell, sub = cell_key(t, band.shape, mdd)
    print(f"raster_zones: zones built ({time.time()-t0:.0f}s), grid {w.height}x{w.width}")
    off = np.zeros(band.shape, np.uint8)            # official units overlap -> account them one by one below
    keys = {"main": zones["main"], "narrow": zones["narrow"], "wide": zones["wide"],
            "band": (band + BAND_KM + 1).clip(0).astype(np.uint8),   # band -30..29 -> 1..60, outside -> 0
            "cell": cell}
    for i, (nm, m) in enumerate(official.items(), start=1):
        keys[f"off_{i}"] = m.astype(np.uint8)
    rows, first = account(keys, row_ha, w)
    z = tidy(rows["main"], ZONES)
    # identity check
    z = z.sort_values(["code", "year"])
    add = z.groupby("code").mining_ha.diff()
    resid = (add - (z.new_land_ha + z.remined_ha - z.stopped_ha)).abs().max()
    assert resid < 1e-6, f"accounting identity fails: {resid}"
    z.to_csv(OUT_ZONE, index=False)
    sens = pd.concat([tidy(rows[k], ZONES).assign(definition=k) for k in ("narrow", "wide")])
    sens.to_csv(OUT_SENS, index=False)
    b = tidy(rows["band"], {i + BAND_KM + 1: f"{i}" for i in range(-BAND_KM, BAND_KM)})
    b["km_from_road"] = b.unit.astype(int)
    b.to_csv(OUT_BAND, index=False)
    cells = tidy(rows["cell"], {i: i for i in range(1, int(cell.max()) + 1)}).rename(columns={"code": "cell"}).drop(columns="unit")
    cells = cells[cells.groupby("cell").mining_ha.transform("max") > 0]           # keep cells that ever had mining
    cells.round(3).to_csv(OUT_CELL, index=False, compression="gzip")
    cell_attributes(cell, sub, t, zones["main"], dist, row_ha).to_csv(OUT_CELLATTR, index=False)
    offs = []
    for i, nm in enumerate(official, start=1):
        offs.append(tidy(rows[f"off_{i}"], {1: nm}))
    pd.concat(offs).to_csv(OUT_OFF, index=False)
    # small window raster for maps: band 1 = zone code, band 2 = first-mined year
    from rasterio.windows import from_bounds
    sub = from_bounds(*WINDOW, t).round_offsets().round_lengths()
    r0, c0 = int(sub.row_off), int(sub.col_off)
    zz = zones["main"][r0:r0 + int(sub.height), c0:c0 + int(sub.width)]
    ff = first[r0:r0 + int(sub.height), c0:c0 + int(sub.width)]
    prof = dict(driver="GTiff", height=zz.shape[0], width=zz.shape[1], count=2, dtype="int16", crs="EPSG:4326",
                transform=rasterio.windows.transform(sub, t), compress="deflate")
    with rasterio.open(OUT_WIN, "w", **prof) as dst:
        dst.write(zz.astype(np.int16), 1); dst.write(ff, 2)
    prof = dict(driver="GTiff", height=w.height, width=w.width, count=2, dtype="int16", crs="EPSG:4326", transform=t,
                compress="deflate", tiled=True, blockxsize=512, blockysize=512)
    with rasterio.open(OUT_FULL, "w", **prof) as dst:
        dst.write(zones["main"].astype(np.int16), 1); dst.write(first, 2)
    print(f"raster_zones: done in {time.time()-t0:.0f}s")


def run():
    if all(p.exists() for p in (OUT_ZONE, OUT_BAND, OUT_OFF, OUT_SENS, OUT_WIN, OUT_FULL, OUT_CELL, OUT_CELLATTR)):
        return
    if not (RAW / "mapbiomas_peru_raster/peru_coverage-col4_2025.tif").exists():
        warnings.warn("raster_zones: rasters and intermediates missing; skipping"); return
    build()


if __name__ == "__main__":
    build()
