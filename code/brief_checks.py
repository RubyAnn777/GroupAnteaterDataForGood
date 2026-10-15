"""Register the source checks the brief cites (part 2) as numbers, so they appear in output/numbers.csv and in
output/brief_numbers.csv in order of appearance. Values come from output/checks.csv (written by checks.py and the
modules' own checks during this run); nothing is typed in by hand. One check per dataset; `ours` = our number,
`pub` = the publisher's number. Run at the end of main.py, after every module has written its checks.
"""
from __future__ import annotations
import pandas as pd

from common import OUT

# id -> (start of the checks.csv label, measure, zone, period, description)
CHECKS = {
    "chk_tbz_2025": ("Raster v3: Tambopata buffer zone mining 2025", "stock", "tambopata_bz", "2025",
                     "MapBiomas Peru Col 4 rasters, our zone registry vs the publisher's buffer-zone statistics"),
    "chk_tnr_2025": ("Raster v3: Tambopata reserve mining 2025", "stock", "tambopata_nr", "2025",
                     "MapBiomas Peru Col 4 rasters vs the MapBiomas Peru platform (protected areas)"),
    "chk_mdd_2025": ("Raster v3: Madre de Dios mining 2025", "stock", "mdd", "2025",
                     "MapBiomas Peru Col 4 rasters vs the publisher's department statistics"),
    "chk_gold_aug2026": ("Gold price, August 2026", "price", "world", "Aug 2026", "World Bank Pink Sheet"),
    "chk_mb_amazonia_2023": ("MapBiomas Amazonia Col 6, mining area whole region 2023", "stock", "Amazon", "2023",
                             "MapBiomas Amazonía Col 6 statistics vs factsheet (0.78 Mha)"),
    "chk_br_ti_2025": ("Brazil publisher check (course card, MapBiomas Brazil Col 11)", "stock",
                       "Brazil indigenous lands", "2025", "MapBiomas Brazil Col 11, artisanal mining in indigenous lands"),
    "chk_kayapo_2025": ("MapBiomas Brazil Col 11 raster: Kayapo mining 2025", "stock", "Kayapó", "2025",
                        "MapBiomas Brazil Col 11 rasters vs platform"),
    "chk_bcrp_2019": ("MINEM Madre de Dios gold 2019, declared + artisanal estimate", "gold_kg", "mdd", "2019",
                      "MINEM yearly files rebuilt vs the central bank (BCRP) series"),
    "chk_pp0128_2019": ("MEF PP 0128 devengado, Madre de Dios, 2019", "soles", "mdd", "2019",
                        "MEF Consulta Amigable, programme 0128 spending"),
    "chk_amw_tbz_2018": ("AMW Tambopata BZ 2018 stock: polygon clip vs registry raster", "amw_new_area",
                         "tambopata_bz", "2018 stock", "Amazon Mining Watch: polygon clip vs our registry raster "
                         "(internal; AMW publishes no zone totals)"),
}


def run(reg):
    c = pd.read_csv(OUT / "checks.csv")
    for k, (lab, measure, zone, period, desc) in CHECKS.items():
        hit = c[c.label.str.startswith(lab)]
        assert len(hit) >= 1, f"check not found: {lab}"
        r = hit.iloc[-1]
        assert bool(r.ok) if "ok" in r and pd.notna(r.ok) else True, f"check failed: {lab}"
        unit = "ha" if measure in ("stock", "amw_new_area") else {"price": "USD/oz", "gold_kg": "kg", "soles": "soles"}[measure]
        for side, v in (("ours", r.value), ("pub", r.expected)):
            reg.add(f"{k}_{side}", float(v), unit, f"Source check ({'our number' if side == 'ours' else 'publisher'}): "
                    f"{desc}; {r.label}", "description", "output/checks.csv", measure=measure, zone=zone, period=period)
