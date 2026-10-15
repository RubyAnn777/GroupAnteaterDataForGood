"""The ONLY way modules read mining by zone (plan v3). Built from raster_zones.py outputs; definitions in definitions.py.

  region_units()   long table: year x reporting unit (definitions.UNITS + "mdd") x {stock, net, new, remined, stopped,
                   stopped splits}; ha (stock) and ha/yr (flows).
  bz_panel()       long table: year x Peruvian buffer zone (whole, official SERNANP polygon) x same columns.
                   The treated unit is named definitions.TREATED_ZONE ("tambopata_bz"); others by SERNANP code.
  wide(df, col)    year x unit table of one column (e.g. "net_ha").
  tenure_split()   year x unit x tenure (corridor / Kotsimba / community / none) for any unit.
  period_mean(...) mean over a definitions.PERIODS window, asserting complete years.
No module may build zones from the statistics workbook or from its own polygons; tests/test_definitions.py checks.
"""
from __future__ import annotations
from functools import lru_cache

import numpy as np
import pandas as pd

from common import ROOT
import definitions as D

INTER = ROOT / "data_intermediate"
FLOWS = ["net_ha", "new_ha", "remined_ha", "stopped_ha", "from_forest_ha", "stopped_to_water_ha",
         "stopped_to_forest_ha", "stopped_to_natural_ha", "stopped_to_other_ha", "stopped_back_1y_ha",
         "stopped_back_2y_ha"]
COLS = ["mining_ha"] + FLOWS


@lru_cache(maxsize=None)
def _zone_year() -> pd.DataFrame:
    z = pd.read_csv(INTER / "zone_year.csv")
    assert set(z.zone) <= set(D.ZONES), "unknown zone in zone_year.csv"
    return z


def _sum(df: pd.DataFrame, by: list[str]) -> pd.DataFrame:
    return df.groupby(by, as_index=False)[COLS].sum(min_count=1)


@lru_cache(maxsize=None)
def region_units() -> pd.DataFrame:
    """Every reporting unit in definitions.UNITS plus 'mdd' (all zones inside the Madre de Dios polygon)."""
    z = _zone_year()
    out = [_sum(z[z.zone.isin(zs)], ["year"]).assign(unit=u) for u, zs in D.UNITS.items()]
    out.append(_sum(z[z.in_mdd == 1], ["year"]).assign(unit="mdd"))
    d = pd.concat(out, ignore_index=True)
    d.loc[d.year == d.year.min(), FLOWS] = np.nan
    return d[["year", "unit"] + COLS]


@lru_cache(maxsize=None)
def bz_panel() -> pd.DataFrame:
    """All Peruvian buffer zones with mapped mining, whole; unit = 'tambopata_bz', 'amarakaeri_bz', 'bahuaja_bz' or
    the SERNANP code. Same accounting as region_units (asserted equal for the two focal zones in raster_zones)."""
    b = pd.read_csv(INTER / "bz_year.csv")
    inv = {v: k for k, v in D.BZ_CODE.items()}
    b["unit"] = b.bz_code.map(inv).fillna(b.bz_code)
    return b[["year", "unit", "bz_code", "bz_name"] + COLS]


def bz_name(unit: str) -> str:
    b = bz_panel()
    if unit in D.UNIT_NAME:
        return D.UNIT_NAME[unit]
    return b.loc[b.unit == unit, "bz_name"].iloc[0] + " buffer zone"


def wide(df: pd.DataFrame, col: str = "net_ha") -> pd.DataFrame:
    return df.pivot(index="year", columns="unit", values=col).sort_index()


def tenure_split(unit: str) -> pd.DataFrame:
    z = _zone_year()
    return _sum(z[z.zone.isin(D.UNITS[unit])], ["year", "tenure"])


def period_mean(s: pd.Series, key_or_years) -> float:
    y0, y1 = D.PERIODS[key_or_years] if isinstance(key_or_years, str) else key_or_years
    v = s.loc[y0:y1]
    assert len(v) == y1 - y0 + 1 and v.notna().all(), f"missing years in {y0}-{y1}"
    return float(v.mean())


def parts_table(df: pd.DataFrame, unit: str, periods=("pre", "during", "later")) -> pd.DataFrame:
    """Period means of net and its parts for one unit (rows = periods, cols = net/new/remined/stopped)."""
    d = df[df.unit == unit].set_index("year")
    return pd.DataFrame({p: {m: period_mean(d[D.COLS[m]], p) for m in ["net"] + D.PARTS} for p in periods}).T


def register_parts(reg, id_prefix: str, values: dict, unit: str, period: str, what: str, source: str = D.SOURCE,
                   claim: str = "description", value_unit: str = D.UNIT):
    """Register net and its parts with measure/zone/period filled in.
    values: {"net": x, "new": x, "remined": x, "stopped": x} (any subset). Ids: <id_prefix>_<measure>.
    `what` says what the number is (e.g. "mean over the period", "DiD vs Amarakaeri buffer zone")."""
    for m, v in values.items():
        reg.add(f"{id_prefix}_{m}", v, value_unit,
                f"{D.MEASURE_NAME[m]}, {D.UNIT_NAME.get(unit, unit)}, {period}: {what}", claim, source,
                measure=m, zone=unit, period=period)
