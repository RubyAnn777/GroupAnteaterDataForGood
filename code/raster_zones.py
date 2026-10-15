"""Plan v3: ONE zone registry on the MapBiomas grid and ONE pixel accounting (net = new + re-mined - stopped).

Every zone number in the package comes from the tables written here; the definitions live in definitions.py.

WHY: the course tables only exist for whole buffer zones and departments. The MapBiomas Peru Collection 4 rasters
(30 m, 1985-2025, the SAME product as the course tables) let us count mining inside any boundary, on one grid, and
split each year's net addition into new land, re-mined land and stopped land.

REGION PARTITION (exclusive, first match wins; definitions.ZONES), over Madre de Dios + the WHOLE Tambopata and
Amarakaeri buffer zones (Amarakaeri reaches into Cusco: Camanti):
   1 Tambopata National Reserve   2 Other protected areas            (SERNANP ANP interiors)
   3 La Pampa sector              4 Rest of Tambopata buffer zone    (official SERNANP BZ RN09, kept whole)
   5 Amarakaeri buffer zone       6 Bahuaja-Sonene buffer zone       7 Other buffer zones
   8 Corridor across the road     9 Rest of the mining corridor      (D.L. 1100, outside every buffer zone)
  10 Native communities          11 Rest of Madre de Dios
Buffer zones come before corridor and communities, so each official buffer zone stays whole (v2 carved Kotsimba,
31,568 ha, out of the Tambopata BZ: different land from the publisher's). Corridor and community land inside a zone
is a TENURE tag (0 none, 1 corridor, 2 Kotsimba, 3 other community), crossed with every zone, so we can still split.
BZ overlaps: Tambopata first, then Amarakaeri (MapBiomas gives the 42,310-ha Tambopata/Bahuaja-Sonene overlap to
Tambopata). `in_mdd` flags pixels inside the Madre de Dios polygon, so department totals sum the same zones.

NATIONAL BUFFER-ZONE PANEL: every SERNANP buffer zone that MapBiomas maps with mining, each kept whole (overlaps:
Tambopata, Amarakaeri, then SERNANP code order), same accounting. Used by every zone design (DiD, event study,
models, synthetic control, SDID). Tambopata and Amarakaeri must equal the region partition exactly (asserted).
Reconciliation with the publisher's statistics workbook: bz_reconciliation.csv (check, not data).

PIXEL ACCOUNTING per key and year t (mining = class 30):
  mining_ha   stock at t
  new_ha      mining at t, never mining before                         (first-time mining)
  remined_ha  mining at t, not at t-1, mining in some year before t-1  (return to old scars)
  stopped_ha  mining at t-1, not at t, split by what the land is at t: water (33), forest (3-6),
              non-forest vegetation, natural bare land (23 sand banks), other (farming, urban, anthropic bare), and whether it is mining again
              in t+1 or t+2 (classifier flicker or re-entry; censored for the last two years)
  net_ha      = new + remined - stopped = stock(t) - stock(t-1)     (identity asserted)
  from_forest_ha  mining at t, forest at t-1

Inputs (big, git-ignored): data_raw/mapbiomas_peru_raster/*.tif, data_raw/sernanp, data_raw/ingemmet, data_raw/raisg
(roads), data_raw/geoboundaries, data_intermediate/native_communities_mdd.geojson (committed subset).
Outputs (committed): data_intermediate/zone_year.csv, zone_year_lp_alt.csv, road_band_year.csv, bz_year.csv,
bz_reconciliation.csv, cell_year.csv.gz, cell_attr.csv, zones_window.tif; zones_mdd.tif (git-ignored, big).
"""
from __future__ import annotations
import time
import warnings

import numpy as np
import pandas as pd

from common import ROOT, DATA
import definitions as D

RAW = ROOT / "data_raw"
INTER = ROOT / "data_intermediate"
RASTER = RAW / "mapbiomas_peru_raster" / "peru_coverage-col4_{y}.tif"
YEARS = list(range(1985, 2026))
# MapBiomas Peru Col 4 legend (LEGEND_CODE sheet of the publisher's statistics workbook):
MINING, FOREST, WATER = 30, (3, 4, 5, 6), (33, 31, 34)                 # 4.2 mining; 1.x forest; 5.x water bodies
NATURAL = (11, 12, 13, 29, 32, 50, 51, 66, 70, 82)  # 2.x non-forest natural vegetation (incl. 51 flooded grassland)
BARE = (22, 23, 52, 61, 68, 92)                     # 4.x natural bare land: 23 beach / sand bank, 68 other, rock, salt
# everything else ("other"): farming (9, 15, 18, 21, 40), urban (24), other anthropic bare (25), not observed (27)
BBOX = (-72.45, -13.40, -68.60, -9.85)            # Madre de Dios envelope; contains both focal buffer zones whole
WINDOW = (-70.35, -13.12, -69.65, -12.72)           # map window for figures
STUDY = (-70.65, -13.30, -69.30, -12.40)            # 1-km cell panel window
CELL_PX = 33                                        # 33 x 30 m ~ 1 km cells
BAND_KM = 30                                        # road bands -30..+30 km
NT = 4                                              # tenure codes 0..3

OUT_ZONE = INTER / "zone_year.csv"
OUT_ALT = INTER / "zone_year_lp_alt.csv"
OUT_BAND = INTER / "road_band_year.csv"
OUT_BZ = INTER / "bz_year.csv"
OUT_REC = INTER / "bz_reconciliation.csv"
OUT_CELL = INTER / "cell_year.csv.gz"
OUT_CELLATTR = INTER / "cell_attr.csv"
OUT_WIN = INTER / "zones_window.tif"                # small: zone, first-mined year, tenure (La Pampa window, maps)
OUT_FULL = INTER / "zones_mdd.tif"                  # big, git-ignored: zone, first-mined year, tenure (region)
OUTPUTS = (OUT_ZONE, OUT_ALT, OUT_BAND, OUT_BZ, OUT_REC, OUT_CELL, OUT_CELLATTR, OUT_WIN)
CATS = ["mining_ha", "new_ha", "remined_ha", "stopped_ha", "from_forest_ha", "stopped_to_water_ha",
        "stopped_to_forest_ha", "stopped_to_natural_ha", "stopped_to_bare_ha", "stopped_to_other_ha"]
LOOK = ["stopped_back_1y_ha", "stopped_back_2y_ha"]


# --------------------------------------------------------------------------- layers and grid
def layers():
    """All boundary layers in EPSG:4326 (geometries made valid)."""
    import geopandas as gpd
    fix = lambda g: g.assign(geometry=g.geometry.make_valid())
    anp = fix(gpd.read_file(RAW / "sernanp/anp_definitivas.geojson").to_crs(4326))
    za = fix(gpd.read_file(RAW / "sernanp/zonas_amortiguamiento.geojson").to_crs(4326))
    cor = fix(gpd.read_file(RAW / "ingemmet/corredor_minero_madre_de_dios_DL1100.geojson").to_crs(4326))
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
    return dict(anp=anp, za=za, cor=cor.geometry.union_all(), ioh=ioh, ti=fix(ti), mdd=mdd)


def window_for(bounds, r):
    from rasterio.windows import from_bounds, Window
    w = from_bounds(*bounds, r.transform).round_offsets().round_lengths()
    return w.intersection(Window(0, 0, r.width, r.height))


def pixel_ha(lat, dlon_deg, dlat_deg):
    """Area (ha) of a small lon/lat cell centred at `lat` on the WGS84 ellipsoid: M(lat) N(lat) cos(lat) dlon dlat,
    with M, N the meridional and prime-vertical radii. Exact to < 1e-6 for 30-m pixels (checked against
    pyproj.Geod). A spherical formula was 0.065% low (referee 2, 2026-10-15); with this, the publisher's Tambopata
    buffer zone 2025 (20,730.0 ha) is matched."""
    a, e2 = 6378137.0, 6.69437999014e-3
    phi = np.radians(np.asarray(lat, float))
    w = 1 - e2 * np.sin(phi) ** 2
    M = a * (1 - e2) / w ** 1.5
    N = a / np.sqrt(w)
    return M * N * np.cos(phi) * np.radians(abs(dlon_deg)) * np.radians(abs(dlat_deg)) / 1e4


def row_area(t, h, r0=0):
    """ha per pixel for each row of a raster window with transform t (rows r0 .. r0+h-1)."""
    lat = t.f + (np.arange(r0, r0 + h) + 0.5) * t.e
    return pixel_ha(lat, t.a, t.e)


def rasterizer(shape, t):
    from rasterio.features import rasterize
    def R(geoms):
        geoms = [g for g in geoms if g is not None and not g.is_empty]
        if not geoms:
            return np.zeros(shape, bool)
        return rasterize([(g, 1) for g in geoms], out_shape=shape, transform=t, fill=0, dtype="uint8").astype(bool)
    return R


def bz_order(za) -> list[str]:
    """SERNANP buffer-zone codes in precedence order (definitions.BZ_PRIORITY first, then code order)."""
    rest = sorted(c for c in za.anp_codi.unique() if c not in D.BZ_PRIORITY)
    return D.BZ_PRIORITY + rest


def signed_road_km(t, shape, ioh, lon_win):
    """Signed distance (km) to the Interoceanic Highway for pixels inside lon_win; north of the road positive."""
    from shapely.ops import unary_union
    from shapely.geometry import LineString
    line = unary_union(ioh.geometry)
    lon = t.c + (np.arange(shape[1]) + 0.5) * t.a; lat = t.f + (np.arange(shape[0]) + 0.5) * t.e
    cmask = (lon >= lon_win[0]) & (lon <= lon_win[1])
    rmask = (lat >= -13.45) & (lat <= -12.25)
    out = np.full(shape, np.nan, np.float32)
    road_lat = []
    for x in lon[cmask]:
        v = LineString([(x, -13.5), (x, -12.3)]).intersection(line)
        pts = [p for p in getattr(v, "geoms", [v]) if not p.is_empty]
        road_lat.append(np.mean([p.y for p in pts]) if pts else np.nan)
    road_lat = np.array(road_lat)
    out[np.ix_(rmask, cmask)] = ((lat[rmask][:, None] - road_lat[None, :]) * 110.574).astype(np.float32)
    return out


# --------------------------------------------------------------------------- region partition
def build_region(L, t, shape):
    """Zone code (definitions.ZONES), tenure code, in_mdd flag; plus road distance and the La Pampa alternatives."""
    R = rasterizer(shape, t)
    anp, za, ti = L["anp"], L["za"], L["ti"]
    mdd = R([L["mdd"]])
    tbz = R(za[za.anp_codi == "RN09"].geometry)
    abz = R(za[za.anp_codi == "RC03"].geometry) & ~tbz
    region = mdd | tbz | abz
    tnr = R(anp[anp.anp_codi == "RN09"].geometry)
    oanp = R(anp[anp.anp_codi != "RN09"].geometry)
    bbz = R(za[za.anp_codi == "PN08"].geometry)
    obz = R(za[~za.anp_codi.isin(["RN09", "RC03", "PN08"])].geometry)
    kots = R(ti[ti.LEVEL_2 == "Kotsimba"].geometry)
    comm = R(ti[ti.LEVEL_2 != "Kotsimba"].geometry)
    cor = R([L["cor"]])
    dist = signed_road_km(t, shape, L["ioh"], (STUDY[0], STUDY[2]))
    lon = t.c + (np.arange(shape[1]) + 0.5) * t.a

    def lp_cols(win):
        m = np.zeros(shape, bool); m[:, (lon >= win[0]) & (lon <= win[1])] = True; return m

    def zone_map(win):
        lpc = lp_cols(win)
        across = cor & lpc & (dist > 0) & (dist <= D.ACROSS_KM)
        z = np.zeros(shape, np.uint8)
        order = [("tambopata_nr", tnr), ("other_anp", oanp), ("lapampa", tbz & lpc), ("tambopata_bz_rest", tbz),
                 ("amarakaeri_bz", abz), ("bahuaja_bz", bbz & mdd), ("other_bz", obz & mdd),
                 ("corridor_across", across & mdd), ("corridor_rest", cor & mdd), ("communities", (kots | comm) & mdd),
                 ("rest_mdd", mdd)]
        assert [k for k, _ in order] == list(D.ZONES), "partition order must follow definitions.ZONES"
        for k, m in order:
            z[(z == 0) & m & region] = D.ZONE_CODE[k]
        assert ((z > 0) == region).all()
        return z

    ten = np.zeros(shape, np.uint8)
    ten[cor] = 1; ten[comm] = 3; ten[kots] = 2                     # communities before corridor
    zones = {"main": zone_map(D.LP_LON), **{k: zone_map(v) for k, v in D.LP_ALT.items()}}
    return zones, ten, mdd, region, dist, lp_cols(D.LP_LON)


# --------------------------------------------------------------------------- accounting
class Accountant:
    """Streams the 41 yearly rasters once over a window and accumulates every category per key (np.bincount)."""

    def __init__(self, keys: dict[str, np.ndarray], row_ha: np.ndarray):
        self.keys = keys
        self.n = {k: int(v.max()) + 1 for k, v in keys.items()}
        self.pix = np.broadcast_to(row_ha[:, None], next(iter(keys.values())).shape)
        self.rows = {k: {} for k in keys}

    def add(self, y, cat, m):
        for k, km in self.keys.items():
            v = np.bincount(km[m].ravel(), weights=self.pix[m].ravel(), minlength=self.n[k])
            self.rows[k].setdefault(y, {})[cat] = v

    def run(self, read):
        shape = self.pix.shape
        prev = np.zeros(shape, bool); ever = np.zeros(shape, bool); before_prev = np.zeros(shape, bool)
        prev_forest = np.zeros(shape, bool)
        stop1 = None; stop2 = None                       # stopped at t-1; stopped at t-2 and not back at t-1
        first = np.zeros(shape, np.int16)
        for y in YEARS:
            t0 = time.time()
            a = read(y)
            mine = a == MINING
            self.add(y, "mining_ha", mine)
            if y > YEARS[0]:
                stopped = prev & ~mine
                self.add(y, "new_ha", mine & ~ever)
                self.add(y, "remined_ha", mine & ~prev & before_prev)
                self.add(y, "stopped_ha", stopped)
                self.add(y, "from_forest_ha", mine & prev_forest)
                water = np.isin(a, WATER); forest = np.isin(a, FOREST); nat = np.isin(a, NATURAL)
                bare = np.isin(a, BARE)
                self.add(y, "stopped_to_water_ha", stopped & water)
                self.add(y, "stopped_to_forest_ha", stopped & forest)
                self.add(y, "stopped_to_natural_ha", stopped & nat)
                self.add(y, "stopped_to_bare_ha", stopped & bare)
                self.add(y, "stopped_to_other_ha", stopped & ~water & ~forest & ~nat & ~bare)
                if stop1 is not None:
                    self.add(y - 1, "stopped_back_1y_ha", stop1 & mine)
                if stop2 is not None:
                    self.add(y - 2, "stopped_back_2y_ha", stop2 & mine)
                stop2 = (stop1 & ~mine) if stop1 is not None else None
                stop1 = stopped
            first[(first == 0) & mine] = y
            before_prev |= prev
            ever |= mine
            prev, prev_forest = mine, np.isin(a, FOREST)
            if (y % 5 == 0) or y == YEARS[-1]:
                print(f"  raster {y}: {time.time()-t0:.1f}s")
        return first

    def tidy(self, key: str, labels: dict[int, dict]) -> pd.DataFrame:
        out = []
        for y, rec in sorted(self.rows[key].items()):
            for code, attrs in labels.items():
                d = {"year": y, **attrs}
                for c in CATS + LOOK:
                    d[c] = (float(rec[c][code]) if code < len(rec[c]) else 0.0) if c in rec else np.nan
                out.append(d)
        df = pd.DataFrame(out)
        # back-in-2-years includes back-in-1-year; censored for the last years
        df["stopped_back_2y_ha"] = df["stopped_back_1y_ha"] + df["stopped_back_2y_ha"]
        df.loc[df.year > YEARS[-1] - 1, "stopped_back_1y_ha"] = np.nan
        df.loc[df.year > YEARS[-1] - 2, "stopped_back_2y_ha"] = np.nan
        df.loc[df.year == YEARS[0], [c for c in CATS + LOOK if c != "mining_ha"]] = np.nan
        df["net_ha"] = df.new_ha + df.remined_ha - df.stopped_ha
        return df


def check_identity(df: pd.DataFrame, by: list[str]):
    d = df.sort_values(by + ["year"])
    diff = d.groupby(by).mining_ha.diff()
    resid = (diff - d.net_ha).abs().max()
    assert resid < 1e-6, f"accounting identity fails: {resid}"
    parts = d[["stopped_to_water_ha", "stopped_to_forest_ha", "stopped_to_natural_ha", "stopped_to_bare_ha",
               "stopped_to_other_ha"]].sum(axis=1)
    assert ((parts - d.stopped_ha).abs().fillna(0) < 1e-6).all(), "stopped split does not add up"


# --------------------------------------------------------------------------- builders
def build_region_tables(L):
    import rasterio
    r = rasterio.open(str(RASTER).format(y=2025))
    w = window_for(BBOX, r); t = r.window_transform(w); shape = (int(w.height), int(w.width))
    t0 = time.time()
    zones, ten, mdd, region, dist, lpc = build_region(L, t, shape)
    print(f"raster_zones: region partition built ({time.time()-t0:.0f}s), grid {shape}")
    # combined key: zone x tenure x in_mdd  -> code*8 + tenure*2 + in_mdd
    def key(z):
        k = z.astype(np.uint16) * (NT * 2) + ten.astype(np.uint16) * 2 + mdd.astype(np.uint16)
        k[z == 0] = 0
        return k
    band = np.zeros(shape, np.uint8)
    ok = lpc & mdd & ~np.isnan(dist) & (np.abs(dist) < BAND_KM)
    band[ok] = (np.floor(dist[ok]).astype(np.int16) + BAND_KM + 1).astype(np.uint8)   # -30..29 -> 1..60
    cell, sub = cell_key(t, shape, region)
    keys = {"main": key(zones["main"]), "narrow": key(zones["narrow"]), "wide": key(zones["wide"]),
            "band": band, "cell": cell}
    acc = Accountant(keys, row_area(t, shape[0]))
    first = acc.run(lambda y: rasterio.open(str(RASTER).format(y=y)).read(1, window=w))

    labs = {}
    for zk, (zc, zname, grp) in D.ZONES.items():
        for tc in range(NT):
            for m in (0, 1):
                labs[zc * NT * 2 + tc * 2 + m] = dict(zone=zk, zone_name=zname, group=grp, tenure=D.TENURE[tc], in_mdd=m)
    z = acc.tidy("main", labs)
    z = z[z.groupby(["zone", "tenure", "in_mdd"]).mining_ha.transform("max") > 0]   # drop never-mined combinations
    check_identity(z, ["zone", "tenure", "in_mdd"])
    z.round(4).to_csv(OUT_ZONE, index=False)
    alt = pd.concat([acc.tidy(k, labs).assign(definition=k) for k in ("narrow", "wide")])
    alt = alt.groupby(["definition", "year", "zone"], as_index=False)[CATS + LOOK + ["net_ha"]].sum(min_count=1)
    alt.round(4).to_csv(OUT_ALT, index=False)
    b = acc.tidy("band", {i + BAND_KM + 1: dict(km_from_road=i) for i in range(-BAND_KM, BAND_KM)})
    check_identity(b, ["km_from_road"]); b.round(4).to_csv(OUT_BAND, index=False)
    c = acc.tidy("cell", {i: dict(cell=i) for i in range(1, int(cell.max()) + 1)})
    c = c[c.groupby("cell").mining_ha.transform("max") > 0]
    c[["year", "cell", "mining_ha", "new_ha", "remined_ha", "stopped_ha", "net_ha"]].round(3).to_csv(
        OUT_CELL, index=False, compression="gzip")
    cell_attributes(cell, sub, t, zones["main"], ten, dist, row_area(t, shape[0])).to_csv(OUT_CELLATTR, index=False)
    write_rasters(t, w, zones["main"], first, ten)
    return z


def build_bz_panel(L):
    """Every SERNANP buffer zone with mapped mining, kept whole (overlaps by bz_order), one window each."""
    import rasterio
    za = L["za"]
    wb = pd.read_csv(DATA / "peru_bufferzone_year.csv")
    name = lambda s: __import__("unicodedata").normalize("NFKD", str(s)).encode("ascii", "ignore").decode().lower().replace("-", " ").strip()
    mined = {name(n) for n in wb[wb.mining_ha > 0].buffer_zone.unique()}
    order = bz_order(za)
    out = []
    r = rasterio.open(str(RASTER).format(y=2025))
    for code in order:
        g = za[za.anp_codi == code]
        if name(g.anp_nomb.iloc[0]) not in mined:
            continue
        geom = g.geometry.union_all()
        w = window_for(geom.bounds, r); t = r.window_transform(w); shape = (int(w.height), int(w.width))
        R = rasterizer(shape, t)
        m = R([geom])
        for hi in order[: order.index(code)]:                        # minus higher-priority buffer zones
            m &= ~R(za[za.anp_codi == hi].geometry)
        print(f"raster_zones: buffer zone {code} {g.anp_nomb.iloc[0]} ({shape[0]}x{shape[1]})")
        acc = Accountant({"bz": m.astype(np.uint8)}, row_area(t, shape[0]))
        acc.run(lambda y: rasterio.open(str(RASTER).format(y=y)).read(1, window=w))
        out.append(acc.tidy("bz", {1: dict(bz_code=code, bz_name=g.anp_nomb.iloc[0])}))
    bz = pd.concat(out)
    check_identity(bz, ["bz_code"])
    bz.round(4).to_csv(OUT_BZ, index=False)
    return bz


def reconcile(bz: pd.DataFrame, z: pd.DataFrame):
    """Check (not data): our raster stock per buffer zone vs the publisher's statistics workbook, every year."""
    import unicodedata
    n = lambda s: unicodedata.normalize("NFKD", str(s)).encode("ascii", "ignore").decode().lower().replace("-", " ").strip()
    wb = pd.read_csv(DATA / "peru_bufferzone_year.csv")
    wb = wb.assign(k=wb.buffer_zone.map(n)).groupby(["k", "year"], as_index=False).mining_ha.sum()
    names = bz.groupby("bz_code").bz_name.first().map(n)
    names = names[~names.duplicated(keep=False)]                       # drop ambiguous names (de Calipuy)
    rec = bz.assign(k=bz.bz_code.map(names)).dropna(subset=["k"]).merge(wb, on=["k", "year"], suffixes=("_raster", "_workbook"))
    rec["diff_ha"] = rec.mining_ha_raster - rec.mining_ha_workbook
    rec["net_raster"] = rec.groupby("bz_code").mining_ha_raster.diff()
    rec["net_workbook"] = rec.groupby("bz_code").mining_ha_workbook.diff()
    rec[["bz_code", "bz_name", "year", "mining_ha_raster", "mining_ha_workbook", "diff_ha", "net_raster",
         "net_workbook"]].round(3).to_csv(OUT_REC, index=False)
    # the region partition and the national panel must be the same land for the two focal zones
    for unit, code in (("tambopata_bz", "RN09"), ("amarakaeri_bz", "RC03")):
        a = z[z.zone.isin(D.UNITS[unit])].groupby("year").mining_ha.sum()
        b = bz[bz.bz_code == code].set_index("year").mining_ha
        assert (a - b).abs().max() < 0.01, f"{unit}: region partition != national panel"
    return rec


def cell_key(t, shape, region):
    """1-km cells (CELL_PX x CELL_PX pixels) inside STUDY and the region; id 1..n, 0 outside."""
    from rasterio.windows import from_bounds
    sub = from_bounds(*STUDY, t).round_offsets().round_lengths()
    r0, c0, h, w_ = int(sub.row_off), int(sub.col_off), int(sub.height), int(sub.width)
    nc = (w_ + CELL_PX - 1) // CELL_PX
    rr, cc = np.mgrid[0:h, 0:w_]
    k = np.zeros(shape, np.int32)
    k[r0:r0 + h, c0:c0 + w_] = (rr // CELL_PX) * nc + cc // CELL_PX + 1
    k[~region] = 0
    return k, (r0, c0, h, w_, nc)


def cell_attributes(cell, sub, t, zone, ten, dist, row_ha):
    """Per cell: centre lon/lat, majority zone (slug), majority tenure, mean signed road distance (km, N > 0),
    mean distance to the nearest river or lake pixel in 2018 (class 33, km), area (ha)."""
    import rasterio
    import rasterio.windows as rw
    from scipy.ndimage import distance_transform_edt
    r0, c0, h, w_, nc = sub
    sl = (slice(r0, r0 + h), slice(c0, c0 + w_))
    with rasterio.open(str(RASTER).format(y=2018)) as r:
        full = window_for(BBOX, r)
        a = r.read(1, window=rw.Window(full.col_off + c0, full.row_off + r0, w_, h))
    dr_km = distance_transform_edt(~(a == 33)) * 0.030
    k = cell[sl].ravel(); n = int(cell.max()) + 1
    pix = np.broadcast_to(row_ha[r0:r0 + h, None], (h, w_)).ravel()
    cnt = np.bincount(k, minlength=n).astype(float); cnt[cnt == 0] = np.nan
    d = dist[sl].ravel(); dd = np.where(np.isnan(d), 0, d)
    road = np.bincount(k, weights=dd, minlength=n) / np.bincount(k, weights=(~np.isnan(d)).astype(float), minlength=n)
    riv = np.bincount(k, weights=dr_km.ravel(), minlength=n) / cnt
    area = np.bincount(k, weights=pix, minlength=n)
    def majority(lab, m):
        zc = np.bincount(k * m + lab[sl].ravel().astype(np.int64), minlength=n * m).reshape(n, m)
        return zc
    zc = majority(zone, 16); zc[:, 0] = 0
    tc = majority(ten, NT)
    ids = np.arange(n)
    rows_, cols_ = (ids - 1) // nc, (ids - 1) % nc
    lon = t.c + (c0 + (cols_ + 0.5) * CELL_PX) * t.a
    lat = t.f + (r0 + (rows_ + 0.5) * CELL_PX) * t.e
    out = pd.DataFrame({"cell": ids, "lon": lon, "lat": lat, "zone": [D.CODE_ZONE.get(c, "") for c in zc.argmax(axis=1)],
                        "tenure": [D.TENURE[c] for c in tc.argmax(axis=1)],
                        "road_km": road, "river_km": riv, "area_ha": area})
    return out[(out.cell > 0) & (out.area_ha > 0)].round(4)


def write_rasters(t, w, zone, first, ten):
    import rasterio
    from rasterio.windows import from_bounds
    sub = from_bounds(*WINDOW, t).round_offsets().round_lengths()
    r0, c0 = int(sub.row_off), int(sub.col_off)
    sl = (slice(r0, r0 + int(sub.height)), slice(c0, c0 + int(sub.width)))
    for path, s, tt in ((OUT_WIN, sl, rasterio.windows.transform(sub, t)), (OUT_FULL, (slice(None), slice(None)), t)):
        zz = zone[s]
        prof = dict(driver="GTiff", height=zz.shape[0], width=zz.shape[1], count=3, dtype="int16", crs="EPSG:4326",
                    transform=tt, compress="deflate", tiled=True, blockxsize=512, blockysize=512)
        with rasterio.open(path, "w", **prof) as dst:
            dst.write(zz.astype(np.int16), 1); dst.write(first[s], 2); dst.write(ten[s].astype(np.int16), 3)
            dst.update_tags(band1="zone code (definitions.ZONES)", band2="first year mapped as mining (0 = never)",
                            band3="tenure (0 none, 1 corridor, 2 Kotsimba, 3 community)")


def build():
    t0 = time.time()
    L = layers()
    z = build_region_tables(L)
    bz = build_bz_panel(L)
    reconcile(bz, z)
    print(f"raster_zones: done in {time.time()-t0:.0f}s")


def run():
    if all(p.exists() for p in OUTPUTS):
        return
    if not (RAW / "mapbiomas_peru_raster/peru_coverage-col4_2025.tif").exists():
        warnings.warn("raster_zones: rasters and intermediates missing; skipping"); return
    build()


if __name__ == "__main__":
    build()
