"""Geographic-fit criterion for the rule-based control search: at what elevation is each area's mining?

La Pampa is lowland alluvial (river-terrace) gold mining. A 'geographic twin' should mine the same kind of terrain, not
high-Andean veins. For every candidate area with AMW mining, sample up to N patches (onset <= 2019, i.e. the mining that
existed when Mercurio began; else any onset), seed 0, and look up SRTM 90 m elevation of the patch centroids from the
public OpenTopoData API (no account). Raw API responses are saved unchanged in data_raw/opentopodata/.
Output (committed): data_intermediate/amw_candidates_elevation.csv (unit_id, n_points, median and p10/p90 elevation, m).
"""
from __future__ import annotations
import json
import time
import warnings
import urllib.request

import pandas as pd

from common import ROOT
from spatial import AMW_FILE, CRS_AREA
from control_amw import YEAR_FILE, _units

RAW = ROOT / "data_raw" / "opentopodata"
PTS_FILE = ROOT / "data_intermediate" / "amw_candidates_elev_points.csv"
OUT_FILE = ROOT / "data_intermediate" / "amw_candidates_elevation.csv"
API = "https://api.opentopodata.org/v1/srtm90m?locations="
N = 15

def sample_points():
    import geopandas as gpd
    amw = gpd.read_file(AMW_FILE)[["onset_year", "geometry"]].to_crs(CRS_AREA)
    cen = gpd.GeoDataFrame(amw[["onset_year"]], geometry=amw.geometry.centroid, crs=CRS_AREA)
    units = _units()
    keep = set(pd.read_csv(YEAR_FILE).unit_id)
    hit = gpd.sjoin(cen, units[units.unit_id.isin(keep)][["unit_id", "geometry"]], predicate="within")
    rows = []
    for uid, d in hit.groupby("unit_id"):
        early = d[d.onset_year <= 2019]
        s = (early if len(early) else d).sample(min(N, len(early) if len(early) else len(d)), random_state=0)
        ll = s.to_crs(4326).geometry
        rows += [{"unit_id": uid, "lon": round(p.x, 5), "lat": round(p.y, 5)} for p in ll]
    pts = pd.DataFrame(rows); pts.to_csv(PTS_FILE, index=False)
    return pts

def query(pts):
    RAW.mkdir(exist_ok=True)
    elev = []
    for i in range(0, len(pts), 100):
        f = RAW / f"srtm90m_batch{i // 100:03d}.json"
        if not f.exists():
            loc = "|".join(f"{r.lat},{r.lon}" for r in pts.iloc[i:i + 100].itertuples())
            with urllib.request.urlopen(API + loc, timeout=60) as r:
                f.write_bytes(r.read())
            time.sleep(1.2)                               # public API: max 1 call per second
        res = json.loads(f.read_text())["results"]
        elev += [x["elevation"] for x in res]
    return pts.assign(elev_m=elev)

def run():
    if OUT_FILE.exists():
        return
    if not AMW_FILE.exists():
        warnings.warn("control_elevation: AMW raw file missing and no intermediate; skipping"); return
    pts = pd.read_csv(PTS_FILE) if PTS_FILE.exists() else sample_points()
    e = query(pts)
    out = e.groupby("unit_id").elev_m.agg(n_points="size", elev_median_m="median",
                                          elev_p10_m=lambda s: s.quantile(.1), elev_p90_m=lambda s: s.quantile(.9)).round(0)
    out.to_csv(OUT_FILE)
    print(f"control_elevation: {len(out)} areas -> {OUT_FILE.relative_to(ROOT)}")

if __name__ == "__main__":
    run()
