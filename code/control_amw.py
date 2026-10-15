"""Step 2 of the rule-based control search (Ruby's design): did satellites detect mining in each candidate area?

For EVERY Peruvian protected area (SERNANP ANP), every Peruvian buffer zone (SERNANP zona de amortiguamiento), every
Brazilian indigenous territory (FUNAI) and the RAISG national protected areas of the other countries, the overlap-free
AMW new area per onset year INSIDE the area (spatial.yearly_new_ha_in: each patch clipped to the polygon, i.e.
AREA-weighted; v2 counted whole patches by centroid). Also each area's size, centre and distance to the treated site.
Plan v3: the treated unit is the official, whole Tambopata buffer zone polygon (SERNANP ZA RN09 = registry units
lapampa + tambopata_bz_rest); its AMW series here is checked against the registry raster (control_select.py). Distance
"to La Pampa" = to the registry's La Pampa sector (Tambopata buffer zone between definitions.LP_LON), not v2's
data-derived point. MEASURE: AMW new area (comparable to first-time mining, not to net additions).

Inputs (big, git-ignored): data_raw/amw, data_raw/sernanp, data_raw/funai (+ data_raw/raisg if present, see PANAMAZON).
Outputs (small, committed): data_intermediate/amw_candidates_units.csv, amw_candidates_year.csv.
If the big inputs are missing, nothing is recomputed; control_select.py reads the committed intermediates.
AMW = mining scars on land (480 m patches, upper bound); 2018 = stock present when the series starts. Description only.
"""
from __future__ import annotations
import time
import warnings

import numpy as np
import pandas as pd

from common import ROOT
from spatial import AMW_FILE, FUNAI_FILE, RAW, INTER, CRS_AREA, YEARS, yearly_new_ha_in
import definitions as D

UNITS_FILE = INTER / "amw_candidates_units.csv"
YEAR_FILE = INTER / "amw_candidates_year.csv"
TU = "PE-BZ-RN09"                  # treated unit: official whole Tambopata buffer zone (registry: lapampa + rest)
RAISG_PARTS = sorted((RAW / "raisg").glob("anp_nacionales_part*.geojson"))   # pan-Amazon national protected areas (RAISG)


def _units():
    """GeoDataFrame of candidate areas: unit_id, country, kind, name, geometry (CRS_AREA)."""
    import geopandas as gpd
    anp = gpd.read_file(RAW / "sernanp/anp_definitivas.geojson").to_crs(CRS_AREA)
    za = gpd.read_file(RAW / "sernanp/zonas_amortiguamiento.geojson").to_crs(CRS_AREA)
    ti = gpd.read_file(FUNAI_FILE).to_crs(CRS_AREA)
    a = anp.dissolve("anp_codi", aggfunc="first").reset_index()
    a = gpd.GeoDataFrame({"unit_id": "PE-ANP-" + a.anp_codi, "country": "Peru", "kind": "protected area",
                          "name": a.anp_nomb + " (" + a.anp_cate + ")"}, geometry=a.geometry, crs=CRS_AREA)
    z = za.dissolve("anp_codi", aggfunc="first").reset_index()
    z = gpd.GeoDataFrame({"unit_id": "PE-BZ-" + z.anp_codi, "country": "Peru", "kind": "buffer zone",
                          "name": z.anp_nomb + " buffer zone"}, geometry=z.geometry, crs=CRS_AREA)
    t = ti.dissolve("terrai_codigo", aggfunc="first").reset_index()
    t = gpd.GeoDataFrame({"unit_id": "BR-TI-" + t.terrai_codigo.astype(str), "country": "Brazil", "kind": "indigenous territory",
                          "name": t.terrai_nome}, geometry=t.geometry, crs=CRS_AREA)
    parts = [a, z, t]
    if RAISG_PARTS:          # other Amazon countries + Brazilian conservation units; Peru comes from SERNANP above
        r = pd.concat([gpd.read_file(f) for f in RAISG_PARTS], ignore_index=True)
        assert r.objectid.is_unique
        r = r[~r.pais.isin(["Perú", ""]) & r.pais.notna()].to_crs(CRS_AREA)
        parts.append(gpd.GeoDataFrame({"unit_id": "RAISG-" + r.objectid.astype(str), "country": r.pais.replace({"Brasil": "Brazil"}),
                                       "kind": "protected area", "name": r.nombre + " (" + r.categoria + ")"},
                                      geometry=r.geometry.values, crs=CRS_AREA))
    u = pd.concat(parts, ignore_index=True)
    u["geometry"] = u.geometry.buffer(0)
    return gpd.GeoDataFrame(u, geometry="geometry", crs=CRS_AREA)


def lapampa_sector():
    """Registry La Pampa sector as a polygon: official Tambopata buffer zone between definitions.LP_LON (CRS_AREA)."""
    import geopandas as gpd
    from shapely.geometry import box
    za = gpd.read_file(RAW / "sernanp/zonas_amortiguamiento.geojson").to_crs(4326)
    g = za[za.anp_codi == "RN09"].geometry.make_valid().union_all().intersection(box(D.LP_LON[0], -20, D.LP_LON[1], 0))
    return gpd.GeoSeries([g], crs=4326).to_crs(CRS_AREA).iloc[0]


def build():
    import geopandas as gpd
    t0 = time.time()
    amw = gpd.read_file(AMW_FILE)[["onset_year", "geometry"]].to_crs(CRS_AREA)
    units = _units()
    hit = gpd.sjoin(amw, units[["unit_id", "geometry"]], predicate="intersects", how="inner")
    print(f"control_amw: {len(amw)} patches, {len(units)} areas, {len(hit)} patch-area hits ({time.time()-t0:.0f}s)")

    lp = lapampa_sector()
    yano = units.loc[units.name.eq("Yanomami") & units.country.eq("Brazil"), "geometry"].iloc[0]
    c4326 = units.geometry.centroid.to_crs(4326)
    info = pd.DataFrame({"unit_id": units.unit_id, "country": units.country, "kind": units.kind, "name": units.name,
                         "area_km2": (units.geometry.area / 1e6).round(1),
                         "lon": c4326.x.round(4), "lat": c4326.y.round(4),
                         "dist_la_pampa_km": (units.geometry.distance(lp) / 1e3).round(1),
                         "dist_yanomami_km": (units.geometry.distance(yano) / 1e3).round(1)})
    rows = []
    geom = units.set_index("unit_id").geometry
    for uid, idx in hit.groupby("unit_id").groups.items():
        ha = yearly_new_ha_in(amw.loc[idx], geom[uid])
        if sum(ha.values()) < 0.05:
            continue
        for y in YEARS:
            rows.append({"unit_id": uid, "year": y, "new_ha": round(ha.get(y, 0.0), 1),
                         "n_patches_touching": int((amw.loc[idx].onset_year == y).sum())})
    yr = pd.DataFrame(rows)
    info.to_csv(UNITS_FILE, index=False)
    yr.to_csv(YEAR_FILE, index=False)
    print(f"control_amw: {yr.unit_id.nunique()} areas with AMW mining; saved intermediates ({time.time()-t0:.0f}s)")


def run():
    if UNITS_FILE.exists() and YEAR_FILE.exists():
        return                                   # 5-minute spatial join: rebuild only when the intermediates are deleted
    if AMW_FILE.exists() and FUNAI_FILE.exists():
        build()
    elif not (UNITS_FILE.exists() and YEAR_FILE.exists()):
        warnings.warn("control_amw: raw inputs and intermediates missing; skipping")
    else:
        warnings.warn("control_amw: raw inputs missing; using committed intermediates")


if __name__ == "__main__":
    import sys
    sys.path.insert(0, str(ROOT / "code"))
    run()
