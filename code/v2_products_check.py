"""Why do MapBiomas and Amazon Mining Watch (AMW) disagree on the corridor after 2021? (review question, 12 Oct 2026)

Hypothesis: AMW flags a 480 m patch once (its onset year) and never counts it again, so new mining that fills in
already-flagged patches is invisible to AMW, while MapBiomas counts every new 30 m pixel. Test: for every MapBiomas
pixel first mined in year t, is it inside an AMW patch whose onset is BEFORE t? If most corridor pixels mined in
2022-25 fall in patches flagged earlier, the disagreement is about densification, not about a real fall.
Output: data_intermediate/products_overlap_v2.csv; numbers pc_*. DESCRIPTION.
"""
from __future__ import annotations
import warnings
import numpy as np
import pandas as pd

from common import ROOT
import raster_zones as rz
from raster_layers import GROUPS

OUT_CSV = ROOT / "data_intermediate" / "products_overlap_v2.csv"
SRC = "MapBiomas Peru Col 4 rasters (first-mined year) x Amazon Mining Watch patches (onset year), zones v2"


def build():
    import geopandas as gpd, rasterio
    from rasterio.features import rasterize
    from spatial import AMW_FILE
    with rasterio.open(rz.OUT_FULL) as r:
        zone, first, t = r.read(1), r.read(2), r.transform
    amw = gpd.read_file(AMW_FILE)[["onset_year", "geometry"]].cx[rz.BBOX[0]:rz.BBOX[2], rz.BBOX[1]:rz.BBOX[3]]
    amw = amw.sort_values("onset_year", ascending=False)          # earliest onset burned last -> wins
    onset = rasterize([(g, int(y)) for g, y in zip(amw.geometry, amw.onset_year)], out_shape=zone.shape,
                      transform=t, fill=0, dtype="int16")
    lat = t.f + (np.arange(zone.shape[0]) + 0.5) * t.e
    pix = np.broadcast_to(((abs(t.a) * 111320 * np.cos(np.radians(lat))) * (abs(t.e) * 110574) / 1e4)[:, None], zone.shape)
    m = (first >= 2019) & (zone > 0)
    df = pd.DataFrame({"year": first[m], "code": zone[m], "onset": onset[m], "ha": pix[m]})
    df["where"] = np.select([df.onset == 0, df.onset < df.year, df.onset >= df.year],
                            ["outside AMW", "inside earlier AMW patch", "inside same/later AMW patch"], default="other")
    out = df.groupby(["year", "code", "where"]).ha.sum().reset_index()
    out.to_csv(OUT_CSV, index=False)


def run(reg):
    print("\n== MapBiomas vs AMW: densification check ==")
    if not OUT_CSV.exists():
        from spatial import AMW_FILE
        if not (AMW_FILE.exists() and rz.OUT_FULL.exists()):
            warnings.warn("v2_products_check: inputs missing; skipping"); return
        build()
    d = pd.read_csv(OUT_CSV)
    d["group"] = d.code.map({c: g for g, cs in GROUPS.items() for c in cs})
    for g in ("Rest of mining corridor", "Corridor across the road", "La Pampa sector"):
        key = "".join(ch for ch in g.lower() if ch.isalnum())[:16]
        for p, (a, b) in {"2019_21": (2019, 2021), "2022_25": (2022, 2025)}.items():
            s = d[(d.group == g) & d.year.between(a, b)].groupby("where").ha.sum()
            share = s.get("inside earlier AMW patch", 0) / s.sum()
            reg.add(f"pc_{key}_in_earlier_patch_{p}", share, "share",
                    f"{g}: share of MapBiomas first-time mining {p.replace('_', '-')} that lies inside an AMW patch flagged in an EARLIER year (invisible to AMW as new)",
                    "description", SRC)
            print(g, p, round(share, 3))
