"""Extract the mining rows (class 30 = '4.3 Minería') from MapBiomas Amazonía Collection 6.0 statistics.

Raw files (~260 MB each, git-ignored, URLs in DOWNLOAD_LOG.csv):
  data_raw/mapbiomas_amazonia/statistics_amazonia_col6_protected.xlsx   sheet COVER_PA     (protected areas, 9 countries)
  data_raw/mapbiomas_amazonia/statistics_amazonia_col6_indigenous.xlsx  sheet COVERAGE_IT  (indigenous territories)
One row = territory x class; years 1985..2023 as columns; a territory without a class-30 row has 0 ha mining.
Output (small, committed): data_intermediate/mb_amazonia_col6_mining.csv (one row per territory with mining, long by year).
Used ONLY to show the twins' pre-2019 paths (control_select / control_top3), as an index (2018 = 100). Plan v3:
Collection 6 is a DIFFERENT collection (and a different product, statistics tables, from our Peru Col 4 raster
accounting): every figure and number built from it says "Amazonía Col 6", it is never added to, subtracted from or
spliced with MapBiomas Peru Collection 4 numbers (agent.md rules 6-7), and Tambopata's own path always comes from the
Peru Col 4 rasters on the v3 registry, never from this file. Publisher check (RAISG mining 2023 vs factsheet 0.78 Mha)
is asserted in checks.run_new_data_checks().
"""
from __future__ import annotations
import warnings
import pandas as pd
from common import ROOT

RAW = ROOT / "data_raw" / "mapbiomas_amazonia"
OUT_FILE = ROOT / "data_intermediate" / "mb_amazonia_col6_mining.csv"
CHECK_FILE = ROOT / "data_intermediate" / "mb_amazonia_col6_check.csv"   # publisher check (factsheet p.3)
FILES = {"protected area": ("statistics_amazonia_col6_protected.xlsx", "COVER_PA"),
         "indigenous territory": ("statistics_amazonia_col6_indigenous.xlsx", "COVERAGE_IT")}
MINING = 30
COLLECTION = "MapBiomas Amazonía Collection 6 (statistics)"     # label for every use of this file

def build():
    parts = []
    for kind, (fn, sheet) in FILES.items():
        d = pd.read_excel(RAW / fn, sheet_name=sheet, engine="openpyxl")
        ycols = [c for c in d.columns if str(c).isdigit()]
        m = d[d["class"] == MINING]
        assert not m.duplicated("geocode").any(), "one class-30 row per territory expected"
        m = m[["geocode", "territory_level_1", "territory_level_2", "territory_level_3", "category"] + ycols]
        long = m.melt(id_vars=["geocode", "territory_level_1", "territory_level_2", "territory_level_3", "category"],
                      var_name="year", value_name="mining_ha")
        long["year"] = long["year"].astype(int); long["kind"] = kind
        parts.append(long)
    out = pd.concat(parts, ignore_index=True)
    out.to_csv(OUT_FILE, index=False)
    # Publisher check: Factsheet Col 6.0 p.3 prints mining = 0.78 Mha for the whole RAISG Amazon in 2023.
    # The region total sits in sheet TRANS_PA, unit category LIMITERAISG, transitions INTO class 30 for 2022->2023.
    tr = pd.read_excel(RAW / FILES["protected area"][0], sheet_name="TRANS_PA", engine="openpyxl")
    v = tr[(tr["category"] == "LIMITERAISG") & (tr["class_to"] == MINING)]["p2022_2023"].sum()
    pd.DataFrame([{"what": "RAISG Amazon mining area 2023, ha (TRANS_PA, LIMITERAISG, class_to 30, p2022_2023)",
                   "value": v, "publisher": "0.78 Mha (Factsheet MapBiomas Amazonia Col 6.0, p.3)"}]).to_csv(CHECK_FILE, index=False)
    print(f"control_mb_amazonia: {out.geocode.nunique()} territories with mining -> {OUT_FILE.relative_to(ROOT)}")

def run():
    if all((RAW / f).exists() for f, _ in FILES.values()):
        if not (OUT_FILE.exists() and CHECK_FILE.exists()):
            build()
    elif not OUT_FILE.exists():
        warnings.warn("control_mb_amazonia: raw files and intermediate missing; skipping")

if __name__ == "__main__":
    build()
