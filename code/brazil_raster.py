"""Brazil, same pixel method as Peru v2: MapBiomas Brazil Collection 11 rasters (30 m, 1985-2025), cut to FUNAI
Indigenous Territories (TIs) and to rings around Yanomami, with new land / old pits / stopped accounting.

Data: public bucket mapbiomas-public, initiatives/brasil/collection11/lulc/coverage/brazil_coverage/
brazil_coverage-col11_<year>.tif (~750 MB each, Brazil-wide). We read only small windows over the network (GDAL
/vsicurl range requests), one window per territory, so nothing big is stored. Class 30 = mining (all mining).
Years read: 1985, 1990, 1995, 2000 and every year 2001-2025 ("first-ever mining" uses this history; mining that
appeared and vanished between the 5-year steps before 2001 is missed - a small effect for gold fronts after 2010).
Units READ: every TI in the AMW candidate list with >= 50 ha of AMW new area (data_intermediate/amw_candidates_*), plus
Yanomami rings 0-10 km and 10-25 km outside its border. This is only the list of windows to read. The ANALYSIS sample is
chosen in brazil_v2.load() on PRE-treatment MapBiomas Col 11 mining (2014-18), with Munduruku + Sai-Cinza merged into
one complex and non-mining removals dropped (review card 12, D-S12-2/8), because the AMW total includes post-treatment
years. The intermediate is not rebuilt when it exists (network reads); a rebuild after the 2026-10-15 area-weighted
AMW rebuild (control_amw.py) could add TIs near the 50-ha line, which the pre-2018 sample rule would drop again.
Outcome identity: net = new_land + remined - stopped = mining(t) - mining(t-1) for t >= 2002 (checked in brazil_v2).
Check: Kayapo mining 2024 and 2025 on the MapBiomas platform (Collection 11, FUNAI 2026 boundary): 17,632 and 18,573 ha.
Output: data_intermediate/brazil_raster_unit_year.csv (unit x year: mining, new_land, remined, stopped ha).
"""
from __future__ import annotations
import time
import warnings
from concurrent.futures import ThreadPoolExecutor

import numpy as np
import pandas as pd

from common import ROOT

INTER = ROOT / "data_intermediate"
OUT_CSV = INTER / "brazil_raster_unit_year.csv"
URL = "/vsicurl/https://storage.googleapis.com/mapbiomas-public/initiatives/brasil/collection11/lulc/coverage/brazil_coverage/brazil_coverage-col11_{y}.tif"
YEARS = [1985, 1990, 1995, 2000] + list(range(2001, 2026))
MINING = 30
FUNAI = ROOT / "data_raw" / "funai" / "tis_poligonais.geojson"


def units():
    import geopandas as gpd
    u = pd.read_csv(INTER / "amw_candidates_units.csv")
    y = pd.read_csv(INTER / "amw_candidates_year.csv")
    tot = y.groupby("unit_id").new_ha.sum()
    br = u[u.unit_id.str.startswith("BR-TI-") & u.unit_id.isin(tot[tot >= 50].index)]
    ti = gpd.read_file(FUNAI)
    ti["unit_id"] = "BR-TI-" + ti.terrai_codigo.astype(str)
    ti = ti[ti.unit_id.isin(br.unit_id)].dissolve("unit_id", aggfunc="first").reset_index()
    out = [(r.unit_id, r.terrai_nome, r.geometry) for r in ti.itertuples()]
    y_ = ti[ti.terrai_nome == "Yanomami"].to_crs("ESRI:102033").geometry.iloc[0]
    for a, b, nm in ((0, 10e3, "Yanomami ring 0-10 km"), (10e3, 25e3, "Yanomami ring 10-25 km")):
        ring = y_.buffer(b).difference(y_.buffer(a) if a else y_)
        out.append((nm.replace(" ", "_"), nm, gpd.GeoSeries([ring], crs="ESRI:102033").to_crs(4326).iloc[0]))
    return out


def read_window(y, bounds):
    import rasterio
    from rasterio.windows import from_bounds
    with rasterio.open(URL.format(y=y)) as r:
        w = from_bounds(*bounds, r.transform).round_offsets().round_lengths()
        return r.read(1, window=w) == MINING, r.window_transform(w)


def account_group(group):
    """group = list of (uid, name, geom) sharing one window (Yanomami + its rings); years streamed in batches of 4."""
    from rasterio.features import rasterize
    from shapely.ops import unary_union
    b = unary_union([g for _, _, g in group]).bounds
    t0 = time.time()
    state = None; rows = []
    for i in range(0, len(YEARS), 4):
        batch = YEARS[i:i + 4]
        with ThreadPoolExecutor(max_workers=4) as ex:
            res = list(ex.map(lambda y: read_window(y, b), batch))
        for y, (mine, t) in zip(batch, res):
            if state is None:
                shape = mine.shape
                masks = [rasterize([(g, 1)], out_shape=shape, transform=t, fill=0, dtype="uint8").astype(bool) for _, _, g in group]
                lat = t.f + (np.arange(shape[0]) + 0.5) * t.e
                pix = np.broadcast_to(((abs(t.a) * 111320 * np.cos(np.radians(lat))) * (abs(t.e) * 110574) / 1e4)[:, None], shape)
                state = dict(ever=np.zeros(shape, bool), before_prev=np.zeros(shape, bool), prev=None)
            prev = state["prev"]
            for (uid, nm, _), inside in zip(group, masks):
                m = mine & inside
                rec = {"unit_id": uid, "unit": nm, "year": y, "mining_ha": pix[m].sum()}
                if prev is not None and y > 2001:
                    pv = prev & inside
                    rec.update(new_land_ha=pix[m & ~state["ever"]].sum(), remined_ha=pix[m & ~pv & state["before_prev"]].sum(),
                               stopped_ha=pix[pv & ~m].sum())
                rows.append(rec)
            if prev is not None:
                state["before_prev"] |= prev
            state["ever"] |= mine; state["prev"] = mine
    print(f"  {[n for _, n, _ in group]}: {time.time()-t0:.0f}s, window {state['ever'].shape}", flush=True)
    return rows


def build():
    us = units()
    yan = [u for u in us if u[1].startswith("Yanomami")]
    rest = [u for u in us if not u[1].startswith("Yanomami")]
    rows = []
    for u in rest:
        rows += account_group([u])
        pd.DataFrame(rows).to_csv(OUT_CSV.with_suffix(".partial.csv"), index=False)
    rows += account_group(yan)
    pd.DataFrame(rows).to_csv(OUT_CSV, index=False)


def run():
    if not OUT_CSV.exists():
        if not FUNAI.exists():
            warnings.warn("brazil_raster: FUNAI polygons and intermediate missing; skipping"); return
        build()


if __name__ == "__main__":
    build()
