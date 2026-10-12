"""Correction (2026-10-12): Madre de Dios gold in the official series = declared output + an ESTIMATE for artisanal
miners until 2019; from 2020 the estimate is no longer in the files. This module rebuilds both parts from the
Ministry of Energy and Mines (MINEM) yearly production files, so the correction is citable.

Raw: data_raw/minem_produccion/5472883-*.7z|zip (gob.pe, 'Producción minera'), exactly as downloaded.
  2001-2020: one zip per year inside the 7z, sheet ORO (grams fine); producer rows have department in column 6
             ('Madre De Dios') and the annual total in the last numeric column; the estimate block starts with
             'PRODUCTORES ARTESANALES 1/' ('1/. Cifras Estimadas') and has a row 'MADRE DE DIOS'.
  2021-2026: 'Producción metálica' / 'Producción Minera' workbook; gold rows filtered by mineral and department.
Check: 2016 declared + estimate = BCRP 2016 (16,223 kg, central bank series used in peru_production.py).
Output: data_intermediate/minem_mdd_gold.csv (year, declared_kg, estimate_kg, total_kg); numbers gold_minem_*.
"""
from __future__ import annotations
import io
import re
import warnings
import zipfile

import numpy as np
import pandas as pd

from common import ROOT
import checks

RAW = ROOT / "data_raw" / "minem_produccion"
OUT_CSV = ROOT / "data_intermediate" / "minem_mdd_gold.csv"
SRC = "MINEM, Producción minera (gob.pe 5472883), yearly gold files; Madre de Dios rows"


def _num(row):
    v = pd.to_numeric(row, errors="coerce").dropna()
    return v


def parse_sheet(x: pd.DataFrame) -> tuple[float, float]:
    """Return (declared grams, estimated artisanal grams) for Madre de Dios from one year's gold sheet."""
    s = x.astype(str)
    is_mdd = s.apply(lambda c: c.str.strip().str.lower().eq("madre de dios")).any(axis=1)
    is_gold = s.apply(lambda c: c.str.strip().str.lower().isin(["oro", "au"])).any(axis=1)
    est_start = s.apply(lambda c: c.str.contains("PRODUCTORES ARTESANALES", case=False, na=False)).any(axis=1)
    est_rows = []
    if est_start.any():
        i0 = est_start.idxmax()
        blk = x.loc[i0 + 1:i0 + 8]
        for i, r in blk.iterrows():
            if r.astype(str).str.strip().str.upper().eq("MADRE DE DIOS").any():
                est_rows.append(i)
    est = sum(_num(x.loc[i]).iloc[-1] for i in est_rows) if est_rows else 0.0
    dec_rows = x.index[is_mdd & is_gold & ~x.index.isin(est_rows)]
    dec = 0.0
    for i in dec_rows:
        v = _num(x.loc[i])
        months = v.iloc[-13:-1] if len(v) >= 13 else v
        tot = v.iloc[-1]
        if len(v) >= 13 and abs(months.sum() - tot) > 1 + 1e-3 * abs(tot):
            warnings.warn(f"row {i}: months do not add to total")
        dec += tot
    return dec, est


def _is_metal(name: str) -> bool:
    n = name.lower()
    return ("producción metálica" in n or "produccion metalica" in n or "producción minera" in n) and "no met" not in n


def year_sheets():
    import py7zr, tempfile
    out = {}
    with tempfile.TemporaryDirectory() as td:
        with py7zr.SevenZipFile(RAW / "5472883-2001-2020.7z") as z:
            z.extractall(td)
        for y in range(2001, 2021):
            zf = zipfile.ZipFile(f"{td}/{y}.zip")
            names = zf.namelist()
            gold = [n for n in names if n.upper().startswith("ORO")]
            if gold:
                out[y] = pd.read_excel(io.BytesIO(zf.read(gold[0])), header=None)
            else:
                met = [n for n in names if "met" in n.lower()]
                out[y] = pd.read_excel(io.BytesIO(zf.read(met[0])), header=None)
        for f in sorted(RAW.glob("5472883-20*")):
            m = re.search(r"5472883-(\d{4})\.", f.name)
            if not m or int(m.group(1)) < 2021:
                continue
            y = int(m.group(1))
            if f.suffix == ".7z":
                with py7zr.SevenZipFile(f) as z:
                    z.extractall(f"{td}/{y}")
                import glob
                cand = [p for p in glob.glob(f"{td}/{y}/*") if _is_metal(p)]
                xl = pd.ExcelFile(cand[0])
            else:
                zf = zipfile.ZipFile(f)
                n = [n for n in zf.namelist() if _is_metal(n)][0]
                xl = pd.ExcelFile(io.BytesIO(zf.read(n)))
            sh = [s for s in xl.sheet_names if "oro" in s.lower()] or xl.sheet_names
            out[y] = pd.concat([xl.parse(s, header=None) for s in sh], ignore_index=True)
    return out


def build():
    rows = []
    for y, x in sorted(year_sheets().items()):
        dec, est = parse_sheet(x)
        rows.append(dict(year=y, declared_kg=dec / 1000, estimate_kg=est / 1000, total_kg=(dec + est) / 1000))
    pd.DataFrame(rows).to_csv(OUT_CSV, index=False)


def run(reg):
    print("\n== MINEM gold, Madre de Dios (declared vs estimated) ==")
    if not OUT_CSV.exists():
        if not RAW.exists():
            warnings.warn("peru_gold_minem: raw files missing; skipping"); return
        build()
    d = pd.read_csv(OUT_CSV).set_index("year")
    print(d.loc[2010:].round(0).to_string())
    b = pd.read_csv(ROOT / "output" / "peru_production_vs_area.csv").set_index("year").tonnes * 1000
    d["bcrp_kg"] = b.reindex(d.index)
    checks.check("MINEM Madre de Dios gold 2019, declared + artisanal estimate, kg (BCRP 2019 series)", d.loc[2019, "total_kg"], b[2019], tol=0.02 * b[2019])
    checks.check("MINEM Madre de Dios gold 2012, all declared, kg (BCRP 2012 series)", d.loc[2012, "total_kg"], b[2012], tol=0.02 * b[2012])
    checks.save()
    for y in (2014, 2015, 2016, 2018, 2019, 2020, 2021, 2024, 2025):
        if y in d.index:
            reg.add(f"gold_minem_declared_{y}_kg", d.loc[y, "declared_kg"], "kg", f"Gold declared by producers in Madre de Dios, {y} (MINEM)", "description", SRC)
            reg.add(f"gold_minem_estimate_{y}_kg", d.loc[y, "estimate_kg"], "kg", f"MINEM estimate of artisanal gold, Madre de Dios, {y} (0 = not in the file)", "description", SRC)
    last_est = d.index[d.estimate_kg > 0].max()
    figure(d)
    reg.add("gold_minem_last_estimate_year", last_est, "year", "Last year in which MINEM's files include the artisanal estimate for Madre de Dios", "description", SRC)
    return d


def figure(d):
    import matplotlib.pyplot as plt
    from common import OUT, style_axes, finish_figure
    yrs = list(range(2010, 2026)); d = d.loc[yrs]
    fig, ax = plt.subplots(figsize=(10, 4.2))
    ax.bar(yrs, d.declared_kg / 1000, color="#b07a00", width=0.72, label="Declared by producers")
    ax.bar(yrs, d.estimate_kg / 1000, bottom=d.declared_kg / 1000, color="#ead7a8", width=0.72, label="Ministry estimate for artisanal miners")
    for x, lab in ((2014.5, "2015: artisanal output\nmoves to an estimate"), (2019.5, "2020: estimate\ndropped")):
        ax.axvline(x, color="#b3261e", ls="--", lw=1.2)
        ax.text(x + 0.1, 24.8, lab, fontsize=7.5, color="#b3261e", va="top")
    ax.set_ylim(0, 25.5); ax.set_ylabel("Gold, tonnes"); style_axes(ax); ax.set_xticks(yrs); ax.tick_params(axis="x", labelsize=8)
    ax.legend(fontsize=8, frameon=False, loc="upper right")
    ax.set_title("The official gold series for Madre de Dios changed definition twice; it is not a production series",
                 loc="left", fontsize=10.5, fontweight="bold")
    finish_figure(fig, f"Source: {SRC}. Total of both parts = the central bank series (checked for 2012 and 2019). Description.",
                  OUT / "fig_peru_gold_definition.png", rect_bottom=0.12)
