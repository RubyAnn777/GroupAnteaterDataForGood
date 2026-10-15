"""INPE DETER mining alerts (class MINERACAO) per month for EVERY Brazilian indigenous territory (FUNAI polygons).

Extends brazil_deter.py (three territories) to all territories. Context only: no module reads it at present
(brazil_stagger.py uses AMW; the Brazil headline is brazil_v2.py, Collection 11 net additions). Munduruku and
Sai-Cinza are kept as separate FUNAI codes here; the package's one complex is defined in brazil_v2.BRAZIL. Alert polygons are intersected with territory
polygons in EPSG:5880 (equal area); area goes to the month of view_date. DETER = alerts of NEW or expanded mining
(not a stock), few-ha minimum, cloud gaps, no river dredges. Never added to or subtracted from MapBiomas or AMW.
Inputs: data_raw/inpe_deter/deter_amz_mineracao.geojson (committed), data_raw/funai/tis_poligonais.geojson (big).
Output (committed): data_intermediate/deter_ti_month.csv  (terrai_codigo, terrai_nome, ym, km2), months with alerts only.
"""
from __future__ import annotations
import warnings
import pandas as pd
from common import ROOT

OUT_FILE = ROOT / "data_intermediate" / "deter_ti_month.csv"
DETER = ROOT / "data_raw" / "inpe_deter" / "deter_amz_mineracao.geojson"
FUNAI = ROOT / "data_raw" / "funai" / "tis_poligonais.geojson"

def build():
    import geopandas as gpd
    d = gpd.read_file(DETER)
    d["ym"] = pd.to_datetime(d["view_date"]).dt.to_period("M").astype(str)
    d = d.to_crs(5880); d["geometry"] = d.geometry.buffer(0)
    t = gpd.read_file(FUNAI)[["terrai_codigo", "terrai_nome", "geometry"]].to_crs(5880)
    t = t.dissolve("terrai_codigo", aggfunc="first").reset_index(); t["geometry"] = t.geometry.buffer(0)
    j = gpd.overlay(d[["ym", "geometry"]], t, how="intersection")
    j["km2"] = j.area / 1e6
    out = j.groupby(["terrai_codigo", "terrai_nome", "ym"], as_index=False).km2.sum()
    out.to_csv(OUT_FILE, index=False)
    print(f"brazil_deter_all: {out.terrai_codigo.nunique()} territories with alerts -> {OUT_FILE.relative_to(ROOT)}")

def run():
    if DETER.exists() and FUNAI.exists():
        if not OUT_FILE.exists():
            build()
    elif not OUT_FILE.exists():
        warnings.warn("brazil_deter_all: inputs and intermediate missing; skipping")

if __name__ == "__main__":
    build()
