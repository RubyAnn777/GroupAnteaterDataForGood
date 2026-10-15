"""Amazon Mining Watch (AMW) by zone, on the v3 zone registry (plan v3; robustness, NOT the core analysis).

MEASURE (a DIFFERENT measure from the outcome): "AMW new area" = area of the union of AMW patches first detected in
year t, minus land already covered by earlier detections (overlap-free). It is comparable to FIRST-TIME mining
(new land), NOT to net additions: AMW has no "stopped" or "re-mined" state and no history before 2018. Every number
here is registered with measure="amw_new_area" and is never put in one sentence with net additions.

ZONES = the v3 registry (definitions.ZONES), not our own polygons. The AMW patches are rasterized on the registry grid
(data_intermediate/zones_mdd.tif: band 1 = zone code, band 3 = tenure; the MapBiomas Peru Col 4 raster window) and
each 30-m pixel takes the zone code of the registry, so a patch that straddles a boundary is split by AREA (v2 used
the patch centroid, its own precedence with buffer zones before the corridor, no community zones, and a lon/lat box
reaching into Cusco, Puno, Bolivia and Acre). Only pixels inside the registry region (zone > 0) count. For each pixel
the first detection year is the earliest onset of any patch covering it, so yearly areas are overlap-free.
The crosswalk v2 -> v3 (how much AMW area changes zone) is written to data_intermediate/amw_zone_crosswalk_v2_v3.csv.

DISTANCE BANDS replace v2's rings around a data-derived La Pampa centre: distance from the registry's La Pampa sector
(zone 3) on the same grid, bands inside / 0-10 / 10-25 / 25-50 km, registry region only; reported as DENSITY (ha of
AMW new area per km2 of land per year), not shares (shares follow area; review card 13, D-S13-4).

BRAZIL (outside the Peru registry): AMW new area inside and 0-10 / 10-25 / 25-50 km outside the Yanomami, Munduruku
(complex: Munduruku + Sai-Cinza, brazil_v2.BRAZIL) and Kayapo territories, area-weighted (patch geometry clipped to
each ring), periods from brazil_v2.BRAZIL.

How to read AMW: a model of mining SCARS on land (Sentinel-2, 480 m patches; upper bound on area); onset 2018 is a
STOCK; 2025-26 onsets are PROVISIONAL (2026 part-year); it cannot see river dredging or mercury, nor legality.
Inputs (big, git-ignored): data_raw/amw/amazon_basin_detections.geojson, data_raw/funai/tis_poligonais.geojson,
data_raw/sernanp, data_raw/ingemmet (crosswalk only), data_intermediate/zones_mdd.tif. Outputs (small, committed):
data_intermediate/amw_zone_year.csv, amw_rings_year.csv, amw_zone_crosswalk_v2_v3.csv, sernanp_mineria_ilegal_summary.csv;
output/fig_map_madre_de_dios.png, fig_map_yanomami.png, fig_spatial_rings.png; numbers sp_*.
Without the big inputs the intermediates are read instead (map figures skipped).
"""
from __future__ import annotations
import time
import warnings

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from matplotlib.lines import Line2D

from common import (ROOT, OUT, style_axes, add_event_markers, set_year_ticks, finish_figure, headline, C, INK, INK2,
                    MUTED, AXIS, EVENT_TITLE_PAD)
import definitions as D

RAW = ROOT / "data_raw"
INTER = ROOT / "data_intermediate"
INTER.mkdir(exist_ok=True)
AMW_FILE = RAW / "amw/amazon_basin_detections.geojson"
FUNAI_FILE = RAW / "funai/tis_poligonais.geojson"
ZONES_TIF = INTER / "zones_mdd.tif"
Z_FILE, RINGS_FILE = INTER / "amw_zone_year.csv", INTER / "amw_rings_year.csv"
XWALK_FILE = INTER / "amw_zone_crosswalk_v2_v3.csv"

CRS_AREA = "ESRI:102033"                    # South America Albers Equal Area Conic (Brazil rings, v2 crosswalk)
YEARS = list(range(2018, 2027))
PROVISIONAL = {2025, 2026}
MEASURE = "amw_new_area"
MEASURE_TXT = ("AMW new area (union of detected patches, first detection year; comparable to first-time mining, "
               "not to net additions)")
SRC_AMW = "Amazon Mining Watch (Earth Genome), model 48px_v4.10b ensemble, updated 2026-10-03, CC-BY-4.0"
SRC = SRC_AMW + " x v3 zone registry (data_intermediate/zones_mdd.tif)"
NOTE_AMW = ("AMW is a model of mining scars on land (480 m patches, upper bound), not MapBiomas hectares; 2018 is a stock, "
            "2025-26 provisional; cannot see river dredging or mercury. Description only.")
PERIOD_COLS = [("2018 (stock)", (2018, 2018), "#c9c6be"), ("2019–21", D.PERIODS["during"], C["gold"]),
               ("2022–24", (2022, 2024), C["lapampa"]), ("2025–26 (prov.)", (2025, 2026), "#7a2e14")]
BANDS = {1: "La Pampa sector", 2: "0-10 km", 3: "10-25 km", 4: "25-50 km"}
BAND_EDGES = ((2, 0, 10), (3, 10, 25), (4, 25, 50))
RING_EDGES = ((0, 10), (10, 25), (25, 50))   # km, Brazil territories

# v2 zones, kept ONLY to measure how much AMW area changes zone (crosswalk); never used for results.
V2_ORDER = ["Tambopata NR", "Bahuaja-Sonene NP", "Amarakaeri RC", "Tambopata BZ", "Bahuaja-Sonene BZ", "Amarakaeri BZ",
            "Mining corridor (DL 1100)", "Other ANP and BZ", "Other Madre de Dios box"]
V2_BOX = (-72.6, -14.6, -68.6, -10.5)
V2_SAME = {   # v2 zone -> registry zones that count as "the same zone"
    "Tambopata NR": {"tambopata_nr"}, "Bahuaja-Sonene NP": {"other_anp"}, "Amarakaeri RC": {"other_anp"},
    "Tambopata BZ": {"lapampa", "tambopata_bz_rest"}, "Bahuaja-Sonene BZ": {"bahuaja_bz"},
    "Amarakaeri BZ": {"amarakaeri_bz"}, "Mining corridor (DL 1100)": {"corridor_across", "corridor_rest"},
    "Other ANP and BZ": {"other_anp", "other_bz"}, "Other Madre de Dios box": {"rest_mdd"},
}


def _gpd():
    import geopandas as gpd
    return gpd


# --------------------------------------------------------------------------- shared helpers (also used elsewhere)
def yearly_new_ha(patches) -> dict[int, float]:
    """Hectares per onset year, overlap-free: area(union of that year's patches) minus area already covered by
    earlier years. `patches` must be in CRS_AREA (used by v2_extra)."""
    from shapely.ops import unary_union
    seen, out = None, {}
    for y in sorted(patches.onset_year.unique()):
        u = unary_union(patches.loc[patches.onset_year == y].geometry.values)
        new = u if seen is None else u.difference(seen)
        out[int(y)] = new.area / 1e4
        seen = u if seen is None else seen.union(u)
    return out


def yearly_new_ha_in(patches, geom) -> dict[int, float]:
    """Area-weighted version: as yearly_new_ha, but only the part of each patch inside `geom` counts (CRS_AREA)."""
    from shapely.ops import unary_union
    seen, out = None, {}
    for y in sorted(patches.onset_year.unique()):
        u = unary_union(patches.loc[patches.onset_year == y].geometry.values).intersection(geom)
        new = u if seen is None else u.difference(seen)
        out[int(y)] = new.area / 1e4
        seen = u if seen is None else seen.union(u)
    return out


def _row_ha(t, h, r0=0):
    import raster_zones as rz                       # one pixel-area formula for the package (geodesic, WGS84)
    return rz.row_area(t, h, r0)


# --------------------------------------------------------------------------- v2 zones (crosswalk only)
def _v2_zone_codes(p4326):
    """The v2 assignment (own polygons, centroid, buffer zones before corridor, lon/lat box): code 1..9 = V2_ORDER."""
    gpd = _gpd()
    from shapely.ops import unary_union
    from shapely.geometry import box
    anp = gpd.read_file(RAW / "sernanp/anp_definitivas.geojson").to_crs(CRS_AREA)
    za = gpd.read_file(RAW / "sernanp/zonas_amortiguamiento.geojson").to_crs(CRS_AREA)
    cor = gpd.read_file(RAW / "ingemmet/corredor_minero_madre_de_dios_DL1100.geojson").to_crs(CRS_AREA)
    g = lambda df, code: unary_union(df[df.anp_codi == code].geometry)
    named = ["RN09", "PN08", "RC03"]
    raw = {"Tambopata NR": g(anp, "RN09"), "Bahuaja-Sonene NP": g(anp, "PN08"), "Amarakaeri RC": g(anp, "RC03"),
           "Tambopata BZ": g(za, "RN09"), "Bahuaja-Sonene BZ": g(za, "PN08"), "Amarakaeri BZ": g(za, "RC03"),
           "Mining corridor (DL 1100)": unary_union(cor.geometry),
           "Other ANP and BZ": unary_union(list(anp[~anp.anp_codi.isin(named)].geometry) +
                                           list(za[~za.anp_codi.isin(named)].geometry))}
    zones, taken = {}, None
    for name in V2_ORDER[:-1]:
        gm = raw[name] if taken is None else raw[name].difference(taken)
        zones[name] = gm
        taken = gm if taken is None else taken.union(gm)
    cent = p4326.to_crs(CRS_AREA).geometry.centroid
    code = np.zeros(len(p4326), np.uint8)
    inbox = cent.within(gpd.GeoSeries([box(*V2_BOX)], crs=4326).to_crs(CRS_AREA).iloc[0]).values
    code[inbox] = len(V2_ORDER)                                 # "Other Madre de Dios box"
    for i, name in enumerate(V2_ORDER[:-1]):
        hit = (code == len(V2_ORDER)) & cent.within(zones[name]).values
        code[hit] = i + 1
    return code


# --------------------------------------------------------------------------- Peru: registry
def build_peru(amw):
    """Rasterize AMW patches on the registry grid (area-weighted) -> zone-year, band-year, crosswalk tables."""
    import rasterio
    import rasterio.windows
    from rasterio.features import rasterize
    from scipy.ndimage import distance_transform_edt
    gpd = _gpd()
    r = rasterio.open(ZONES_TIF)
    t, H, W = r.transform, r.height, r.width
    zone = r.read(1).astype(np.uint8); ten = r.read(3).astype(np.uint8)
    mdd = gpd.read_file(RAW / "geoboundaries/geoBoundaries-PER-ADM1.geojson").to_crs(4326)
    mdd = rasterize([(mdd[mdd.shapeName == "Madre de Dios"].geometry.union_all(), 1)], out_shape=(H, W), transform=t,
                    fill=0, dtype="uint8")
    # distance bands from the La Pampa sector (zone 3), on the grid (metres per pixel at the sector's latitude)
    rows, cols = np.where(zone == D.ZONE_CODE["lapampa"])
    m = int(0.55 / abs(t.e))
    R0, R1, C0, C1 = max(rows.min() - m, 0), min(rows.max() + m, H), max(cols.min() - m, 0), min(cols.max() + m, W)
    lat_c = t.f + (rows.mean() + 0.5) * t.e
    dy, dx = abs(t.e) * 110574, abs(t.a) * 111320 * np.cos(np.radians(lat_c))
    dist = distance_transform_edt(zone[R0:R1, C0:C1] != D.ZONE_CODE["lapampa"], sampling=(dy, dx)) / 1e3
    band = np.zeros((H, W), np.uint8)
    sub = np.zeros(dist.shape, np.uint8)
    sub[dist == 0] = 1
    for code, a, b in BAND_EDGES:
        sub[(dist > a) & (dist <= b)] = code
    band[R0:R1, C0:C1] = sub
    band[zone == 0] = 0
    del dist, sub
    # patches: earliest onset wins per pixel (rasterize burns in order, last wins -> sort descending)
    l, b_, rr, tt = r.bounds
    p = amw.cx[l:rr, b_:tt].copy()
    p = p.sort_values("onset_year", ascending=False)
    p["v2"] = _v2_zone_codes(p)
    K = len(YEARS) + 1
    nz, nb = len(D.ZONES) + 1, len(BANDS) + 1
    acc_z = np.zeros(nz * 4 * 2 * K); acc_b = np.zeros(nb * K); acc_x = np.zeros((len(V2_ORDER) + 1) * nz * K)
    land_b = np.zeros(nb); land_z = np.zeros(nz)
    step = 1500
    sidx = p.sindex
    from shapely.geometry import box
    for r0 in range(0, H, step):
        h = min(step, H - r0)
        tw = rasterio.windows.transform(rasterio.windows.Window(0, r0, W, h), t)
        bb = box(t.c, t.f + (r0 + h) * t.e, t.c + W * t.a, t.f + r0 * t.e)
        q = p.iloc[sidx.query(bb, predicate="intersects")].sort_values("onset_year", ascending=False)
        if len(q):
            first = rasterize(zip(q.geometry, q.onset_year.astype(int)), out_shape=(h, W), transform=tw, fill=0,
                              dtype="int16")
            old = rasterize(zip(q.geometry, q.v2.astype(int)), out_shape=(h, W), transform=tw, fill=0, dtype="uint8")
        else:
            first = np.zeros((h, W), np.int16); old = np.zeros((h, W), np.uint8)
        pix = np.broadcast_to(_row_ha(t, h, r0)[:, None], (h, W))
        zz, tn, md, bd = zone[r0:r0 + h], ten[r0:r0 + h], mdd[r0:r0 + h], band[r0:r0 + h]
        land_b += np.bincount(bd.ravel(), weights=pix.ravel(), minlength=nb)
        land_z += np.bincount(zz.ravel(), weights=pix.ravel(), minlength=nz)
        sel = (first > 0) & (zz > 0)
        if not sel.any():
            continue
        yi = (first[sel] - YEARS[0] + 1).astype(np.int64)
        w = pix[sel]
        kz = ((zz[sel].astype(np.int64) * 4 + tn[sel]) * 2 + md[sel]) * K + yi
        acc_z += np.bincount(kz, weights=w, minlength=acc_z.size)
        acc_b += np.bincount(bd[sel].astype(np.int64) * K + yi, weights=w, minlength=acc_b.size)
        acc_x += np.bincount((old[sel].astype(np.int64) * nz + zz[sel]) * K + yi, weights=w, minlength=acc_x.size)
    rows_z = []
    A = acc_z.reshape(nz, 4, 2, K)
    for zk, (zc, zname, grp) in D.ZONES.items():
        for tc in range(4):
            for mi in (0, 1):
                if A[zc, tc, mi].sum() == 0:
                    continue
                for i, y in enumerate(YEARS):
                    rows_z.append(dict(zone=zk, zone_name=zname, tenure=D.TENURE[tc], in_mdd=mi, year=y,
                                       new_ha=round(A[zc, tc, mi, i + 1], 2), is_stock=y == 2018,
                                       provisional=y in PROVISIONAL))
    ztab = pd.DataFrame(rows_z)
    Bm = acc_b.reshape(nb, K)
    btab = pd.DataFrame([dict(region="La Pampa sector band", unit=BANDS[bc], year=y, new_ha=round(Bm[bc, i + 1], 2),
                              land_km2=round(land_b[bc] / 100, 2), is_stock=y == 2018, provisional=y in PROVISIONAL)
                         for bc in BANDS for i, y in enumerate(YEARS)])
    X = acc_x.reshape(len(V2_ORDER) + 1, nz, K)
    xrows = []
    for oc in range(len(V2_ORDER) + 1):
        for zc in range(nz):
            for i, y in enumerate(YEARS):
                v = X[oc, zc, i + 1]
                if v > 0:
                    xrows.append(dict(v2_zone=V2_ORDER[oc - 1] if oc else "outside v2 box",
                                      v3_zone=D.CODE_ZONE.get(zc, "outside registry"), year=y, ha=round(v, 2)))
    xw = pd.DataFrame(xrows)
    # v2 area OUTSIDE the registry region (box reaching into Cusco, Puno, Bolivia, Acre): from the patch vectors
    pv = amw.cx[V2_BOX[0]:V2_BOX[2], V2_BOX[1]:V2_BOX[3]].to_crs(CRS_AREA)
    box_tot = yearly_new_ha(pv)
    xw.attrs["v2_box_total"] = box_tot
    pd.DataFrame([dict(year=y, ha=v) for y, v in box_tot.items()]).to_csv(INTER / "amw_v2_box_total_year.csv",
                                                                            index=False)
    return ztab, btab, xw, dict(zone=zone, mdd=mdd, transform=t, bounds=r.bounds)


# --------------------------------------------------------------------------- Brazil rings (area-weighted)
def build_brazil(amw):
    gpd = _gpd()
    from shapely.ops import unary_union
    from brazil_v2 import BRAZIL
    ti = gpd.read_file(FUNAI_FILE)
    rows, geoms = [], {}
    for g, names in BRAZIL["funai_names"].items():
        sel = ti[ti.terrai_nome.isin(names)].to_crs(CRS_AREA)
        assert set(sel.terrai_nome) == set(names), (g, names)
        tg = unary_union(sel.geometry)
        bb = gpd.GeoSeries([tg.buffer(55e3)], crs=CRS_AREA).to_crs(4326).total_bounds
        p = amw.cx[bb[0]:bb[2], bb[1]:bb[3]].to_crs(CRS_AREA)
        rings = {"inside": tg}
        for a, b in RING_EDGES:
            rings[f"{a}-{b} km"] = tg.buffer(b * 1e3).difference(tg.buffer(a * 1e3) if a else tg)
        for nm, geom in rings.items():
            ha = yearly_new_ha_in(p, geom) if len(p) else {}
            for y in YEARS:
                rows.append(dict(region=f"{g} TI ring", unit=nm, year=y, new_ha=round(ha.get(y, 0.0), 2),
                                 land_km2=round(geom.area / 1e6, 2), is_stock=y == 2018, provisional=y in PROVISIONAL))
        geoms[g] = (tg, p)
    return pd.DataFrame(rows), geoms


# --------------------------------------------------------------------------- SERNANP illegal-mining layer
def mineria_ilegal_summary():
    """SERNANP 'mineria_ilegal' (179 features, no date field: not an enforcement time series). By type x status, and
    how many fall inside the registry region (Madre de Dios + the Tambopata and Amarakaeri buffer zones)."""
    gpd = _gpd()
    import rasterio
    import rasterio.windows
    m = gpd.read_file(RAW / "sernanp/mineria_ilegal.geojson")
    m["ha"] = m.to_crs(CRS_AREA).area / 1e4
    c = m.to_crs(CRS_AREA).geometry.centroid.to_crs(4326)
    with rasterio.open(ZONES_TIF) as r:
        inside = [((r.bounds.left < x < r.bounds.right) and (r.bounds.bottom < y < r.bounds.top))
                  and next(r.sample([(x, y)], indexes=1))[0] > 0 for x, y in zip(c.x, c.y)]
    m["in_registry_region"] = inside
    s = (m.groupby(["idtipact", "estado"]).agg(n=("objectid", "size"), polygon_ha=("ha", "sum"),
                                              n_in_registry_region=("in_registry_region", "sum")).round(1).reset_index())
    s.to_csv(INTER / "sernanp_mineria_ilegal_summary.csv", index=False)
    return s


# --------------------------------------------------------------------------- figures
def fig_map_mdd(amw, grid):
    """AMW patches by first-detection period over the registry zones."""
    gpd = _gpd()
    from matplotlib.colors import ListedColormap
    z = grid["zone"][::6, ::6]
    t = grid["transform"]
    ext = (t.c, t.c + grid["zone"].shape[1] * t.a, t.f + grid["zone"].shape[0] * t.e, t.f)
    grp = np.zeros(z.shape, np.uint8)
    fills = {1: ("protected land (reserves, parks)", "#d7e8cf", ["tambopata_nr", "other_anp"]),
             2: ("Tambopata buffer zone", "#f3d3bd", ["lapampa", "tambopata_bz_rest"]),
             3: ("other buffer zones (Amarakaeri, ...)", "#e3eedb", ["amarakaeri_bz", "bahuaja_bz", "other_bz"]),
             4: ("mining corridor outside buffer zones", "#cfe0ee", ["corridor_across", "corridor_rest"]),
             5: ("native communities", "#efd0de", ["communities"]),
             6: ("rest of Madre de Dios", "#eeece6", ["rest_mdd"])}
    for k, (_, _, zs) in fills.items():
        grp[np.isin(z, [D.ZONE_CODE[s] for s in zs])] = k
    cmap = ListedColormap(["#fbfaf7"] + [v[1] for v in fills.values()])
    fig, ax = plt.subplots(figsize=(9, 6.6))
    headline(fig, "Madre de Dios: AMW new mining area by first-detection period, on the zone registry",
             "Measure: AMW new area (union of detected patches; comparable to first-time mining, not to net\n"
             "additions), by first-detection year. Zones: the v3 registry (definitions.ZONES) on the MapBiomas grid.")
    ax.imshow(grp, extent=ext, cmap=cmap, vmin=0, vmax=6, interpolation="nearest", zorder=0)
    for lab, (a, b), col in PERIOD_COLS:
        d = amw[(amw.onset_year >= a) & (amw.onset_year <= b)].cx[ext[0]:ext[1], ext[2]:ext[3]]
        if len(d):
            d.plot(ax=ax, color=col, linewidth=0, zorder=2)
    for x in D.LP_LON:
        ax.axvline(x, color=INK2, lw=0.6, ls=(0, (3, 2)), zorder=3)
    ax.text(np.mean(D.LP_LON), -12.42, "La Pampa sector\n(longitudes)", ha="center", fontsize=7.5, color=INK2)
    ax.set_xlim(-71.5, -68.7); ax.set_ylim(-13.4, -11.95)
    ax.set_aspect(1 / np.cos(np.radians(-12.7)))
    ax.set_xticks([]); ax.set_yticks([]); ax.set_xlabel(""); ax.set_ylabel("")
    for s in ax.spines.values():
        s.set_visible(False)
    h = [Patch(color=c, label=f"AMW onset {l}") for l, _, c in PERIOD_COLS] + \
        [Patch(color=v[1], label=v[0]) for v in fills.values()]
    ax.legend(handles=h, loc="upper center", bbox_to_anchor=(0.5, -0.01), ncol=3, fontsize=7.5, frameon=False)
    finish_figure(fig, f"Source: {SRC_AMW}; zone registry from SERNANP, INGEMMET (D.L. 1100), native-community "
                       "and geoBoundaries polygons on the MapBiomas Peru Col 4 grid (raster_zones.py). " + NOTE_AMW,
                  OUT / "fig_map_madre_de_dios.png")


def fig_map_br(geoms):
    gpd = _gpd()
    fig, axes = plt.subplots(1, 3, figsize=(12, 5.0))
    headline(fig, "Brazil: AMW new mining area inside and around three indigenous territories",
             "Measure: AMW new area (union of detected patches; comparable to first-time mining, not to net additions).\n"
             "Munduruku = Munduruku + Sai-Cinza (one complex). Rings 10 / 25 / 50 km outside each territory.")
    for ax, (g, (tg, p)) in zip(axes, geoms.items()):
        p4 = p.to_crs(4326)
        for lab, (a, b), col in PERIOD_COLS:
            d = p4[(p4.onset_year >= a) & (p4.onset_year <= b)]
            if len(d):
                d.plot(ax=ax, color=col, linewidth=0, zorder=2)
        gpd.GeoSeries([tg], crs=CRS_AREA).to_crs(4326).boundary.plot(ax=ax, color=C["reserve"], lw=1.3, zorder=3)
        for r_ in (10, 25, 50):
            gpd.GeoSeries([tg.buffer(r_ * 1e3)], crs=CRS_AREA).to_crs(4326).boundary.plot(
                ax=ax, color=MUTED, ls="--", lw=0.5, zorder=4)
        bb = gpd.GeoSeries([tg.buffer(55e3)], crs=CRS_AREA).to_crs(4326).total_bounds
        ax.set_xlim(bb[0], bb[2]); ax.set_ylim(bb[1], bb[3]); ax.set_aspect(1 / np.cos(np.radians((bb[1] + bb[3]) / 2)))
        ax.set_title(g, fontsize=9.5); ax.set_xticks([]); ax.set_yticks([]); ax.set_xlabel(""); ax.set_ylabel("")
        for s in ax.spines.values():
            s.set_visible(False)
    axes[1].legend(handles=[Patch(color=c, label=f"AMW onset {l}") for l, _, c in PERIOD_COLS] +
                   [Line2D([], [], color=MUTED, ls="--", lw=0.6, label="10 / 25 / 50 km outside")],
                   loc="upper center", bbox_to_anchor=(0.5, -0.02), ncol=5, fontsize=7.5, frameon=False)
    finish_figure(fig, f"Source: {SRC_AMW}; FUNAI tis_poligonais (WFS, accessed 2026-10). " + NOTE_AMW,
                  OUT / "fig_map_yanomami.png")


def fig_bands(btab):
    """AMW new area density by distance band from the La Pampa sector, 2019 onward (2018 is a stock)."""
    d = btab[btab.year >= 2019].copy()
    d["dens"] = d.new_ha / d.land_km2
    fig, axes = plt.subplots(2, 2, figsize=(9, 6.0), sharex=True)
    a0, b0 = D.PERIODS["during"]
    headline(fig, "AMW new mining area per km² of land, by distance from the La Pampa sector",
             "Measure: AMW new area (comparable to first-time mining, not to net additions), ha per km² of land per year,\n"
             "registry region only, 2019–2026 (hollow = provisional; 2026 part-year).")
    for ax, (bc, nm) in zip(axes.ravel(), BANDS.items()):
        s = d[d.unit == nm].sort_values("year")
        ok, pv = s[~s.provisional], s[s.provisional]
        col = C["lapampa"] if bc == 1 else C["other"] if bc == 4 else C["lapampa_tint"]
        ax.plot(ok.year, ok.dens, "-o", color=col, lw=2, ms=4, mec="white")
        if len(pv):
            ax.plot([ok.year.iloc[-1]] + list(pv.year), [ok.dens.iloc[-1]] + list(pv.dens), color=col, lw=1.2, ls=":")
            ax.plot(pv.year, pv.dens, "o", mfc="white", color=col, ms=4.5)
        ax.set_ylim(0, None); style_axes(ax, fmt=False); set_year_ticks(ax, range(2019, 2027), short=True)
        ax.set_xlim(2018.4, 2026.6)
        ax.set_title(nm if bc == 1 else f"{nm} from the sector ({s.land_km2.iloc[0]:,.0f} km² of land)", fontsize=9.5)
        add_event_markers(ax)
    for ax in axes[:, 0]:
        ax.set_ylabel("ha per km² per year")
    finish_figure(fig, f"Source: {SRC}. Distance on the registry grid from zone 3 (La Pampa sector = Tambopata buffer "
                       f"zone between {D.LP_LON[0]} and {D.LP_LON[1]}). " + NOTE_AMW,
                  OUT / "fig_spatial_rings.png", event_note=True)


# --------------------------------------------------------------------------- numbers
def _add(reg, id, v, unit, desc, zone, period):
    reg.add(id, v, unit, f"{desc}. Measure: {MEASURE_TXT}", "description", SRC, measure=MEASURE, zone=zone,
            period=period)


def register(reg, z, b, rb, xw):
    zz = z.groupby(["zone", "year"]).new_ha.sum()
    get = lambda zs, ys: float(sum(zz.get((s, y), 0.0) for s in zs for y in ys))
    nr, bz = ["tambopata_nr"], D.UNITS["tambopata_bz"]
    for y in (2019, 2024, 2025, 2026):
        _add(reg, f"sp_amw_tambopata_nr_new_ha_{y}", get(nr, [y]), "ha",
             f"AMW new area first detected in {y} inside Tambopata National Reserve" +
             (" (PROVISIONAL)" if y in PROVISIONAL else ""), "tambopata_nr", str(y))
    _add(reg, "sp_amw_tambopata_nr_new_ha_2019_2024", get(nr, range(2019, 2025)), "ha",
         "AMW new area inside Tambopata National Reserve, sum of onsets 2019-2024 (confirmed)", "tambopata_nr", "2019-2024")
    _add(reg, "sp_amw_tambopata_nr_new_ha_2025_2026", get(nr, [2025, 2026]), "ha",
         "AMW new area inside Tambopata National Reserve, onsets 2025 + 2026 (PROVISIONAL)", "tambopata_nr", "2025-2026")
    _add(reg, "sp_amw_tambopata_bz_new_ha_2019_2024", get(bz, range(2019, 2025)), "ha",
         "AMW new area in the Tambopata buffer zone (official polygon, whole), onsets 2019-2024", "tambopata_bz",
         "2019-2024")
    _add(reg, "sp_amw_tambopata_bz_stock_2018", get(bz, [2018]), "ha",
         "AMW area detected by 2018 (stock when the series starts), Tambopata buffer zone", "tambopata_bz", "2018")
    # distance bands: density, not shares
    bb = b.set_index(["unit", "year"])
    for pk in ("during", "later"):
        a0, b0 = D.PERIODS[pk]
        for bc, nm in BANDS.items():
            land = bb.loc[(nm, 2019), "land_km2"]
            v = np.mean([bb.loc[(nm, y), "new_ha"] for y in range(a0, b0 + 1)]) / land
            key = {1: "in", 2: "0_10", 3: "10_25", 4: "25_50"}[bc]
            reg.add(f"sp_lp_band_{key}_density_{pk}", v, "ha/km2/yr",
                    f"AMW new area per km² of land per year, {nm}" + ("" if bc == 1 else " from the La Pampa sector") +
                    f", {a0}-{b0}" + (" (2025 provisional)" if pk == "later" else "") + f". Measure: {MEASURE_TXT}",
                    "description", SRC, measure=MEASURE, zone=f"lapampa_band_{key}", period=f"{a0}-{b0}")
    # crosswalk v2 -> v3, onsets 2019-2024 (confirmed)
    x = xw[xw.year.between(2019, 2024)]
    inreg = x[x.v3_zone != "outside registry"]
    same = inreg.apply(lambda r: r.v3_zone in V2_SAME.get(r.v2_zone, set()), axis=1)
    box_tot = sum(v for y, v in xw.attrs.get("v2_box_total", {}).items() if 2019 <= y <= 2024)
    in_v2box = inreg[inreg.v2_zone != "outside v2 box"].ha.sum()
    _add(reg, "sp_xwalk_v2_box_ha_2019_2024", box_tot, "ha", "v2 'Madre de Dios box' total AMW new area, onsets 2019-24",
         "v2_box", "2019-2024")
    _add(reg, "sp_xwalk_registry_ha_2019_2024", inreg.ha.sum(), "ha",
         "v3 registry region total AMW new area, onsets 2019-24 (area-weighted)", "registry_region", "2019-2024")
    reg.add("sp_xwalk_v2_box_outside_registry_share", 1 - in_v2box / box_tot, "share",
            "Share of the v2 box's AMW new area 2019-24 that lies OUTSIDE the v3 registry region (Puno, Cusco outside "
            "Amarakaeri, Bolivia, Acre ...)", "description", SRC, measure="share", zone="v2_box", period="2019-2024")
    reg.add("sp_xwalk_changed_zone_share", inreg.ha[~same].sum() / inreg.ha.sum(), "share",
            "Share of the registry region's AMW new area 2019-24 whose v3 zone differs from its v2 zone (centroid, own "
            "precedence, no community zones)", "description", SRC, measure="share", zone="registry_region",
            period="2019-2024")
    yb = rb[rb.region == "Yanomami TI ring"].set_index(["unit", "year"]).new_ha
    from brazil_v2 import BRAZIL
    for pk in ("boom", "later"):
        a0, b0 = BRAZIL[pk]
        _add(reg, f"sp_yanomami_inside_new_ha_{pk}", sum(yb[("inside", y)] for y in range(a0, b0 + 1)), "ha",
             f"AMW new area inside the Yanomami territory, sum of onsets {a0}-{b0}" + (" (2025 provisional)" if b0 >= 2025 else ""),
             "br_yanomami", f"{a0}-{b0}")
        _add(reg, f"sp_yanomami_outside_0_50km_new_ha_{pk}",
             sum(yb[(u, y)] for u in ("0-10 km", "10-25 km", "25-50 km") for y in range(a0, b0 + 1)), "ha",
             f"AMW new area 0-50 km outside the Yanomami territory, sum of onsets {a0}-{b0}", "br_yanomami_0_50km",
             f"{a0}-{b0}")


# --------------------------------------------------------------------------- entry point
def run(reg):
    t0 = time.time()
    have_raw = AMW_FILE.exists() and FUNAI_FILE.exists() and ZONES_TIF.exists()
    if have_raw:
        gpd = _gpd()
        amw = gpd.read_file(AMW_FILE)[["onset_year", "status", "geometry"]]
        print(f"spatial: AMW loaded ({len(amw)} patches) in {time.time()-t0:.0f}s")
        ztab, btab, xw, grid = build_peru(amw)
        rtab, geoms = build_brazil(amw)
        ztab.to_csv(Z_FILE, index=False)
        pd.concat([btab, rtab]).to_csv(RINGS_FILE, index=False)
        xw.to_csv(XWALK_FILE, index=False)
        mineria_ilegal_summary()
        fig_map_mdd(amw, grid); fig_map_br(geoms)
        del grid
    else:
        if not (Z_FILE.exists() and RINGS_FILE.exists() and XWALK_FILE.exists()):
            warnings.warn("spatial: raw inputs AND intermediates missing; skipping spatial step"); return
        warnings.warn("spatial: big raw inputs missing; using committed intermediates, skipping map figures")
        ztab = pd.read_csv(Z_FILE)
        allr = pd.read_csv(RINGS_FILE)
        btab, rtab = allr[allr.region == "La Pampa sector band"], allr[allr.region != "La Pampa sector band"]
        xw = pd.read_csv(XWALK_FILE)
        bt = INTER / "amw_v2_box_total_year.csv"
        if bt.exists():
            xw.attrs["v2_box_total"] = dict(pd.read_csv(bt).values)
    fig_bands(btab)
    register(reg, ztab, btab, rtab, xw)
    print(f"spatial: done in {time.time()-t0:.0f}s")


if __name__ == "__main__":
    from common import Numbers
    r = Numbers(); run(r)
    print(pd.DataFrame(r.rows.values())[["id", "value", "unit", "zone", "period"]].to_string())
