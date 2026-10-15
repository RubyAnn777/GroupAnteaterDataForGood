"""Correction (2026-10-12): Madre de Dios gold in the official series = declared output + an ESTIMATE for artisanal
miners until 2019; from 2020 the estimate is no longer in the files. This module rebuilds both parts from the
Ministry of Energy and Mines (MINEM) yearly production files, so the correction is citable.

Raw: data_raw/minem_produccion/5472883-*.7z|zip (gob.pe, 'Producción minera'), exactly as downloaded.
  2001-2020: one zip per year inside the 7z, sheet ORO (grams fine); producer rows have department in column 6
             ('Madre De Dios') and the annual total in the last numeric column; the estimate block starts with
             'PRODUCTORES ARTESANALES 1/' ('1/. Cifras Estimadas') and has a row 'MADRE DE DIOS'.
  2021-2026: 'Producción metálica' / 'Producción Minera' workbook; gold rows filtered by mineral and department.
Check (review D-S1-3, 2026-10-15): EVERY year 2001-2025, MINEM declared + estimate vs the central bank series (BCRP
RD15556DA, read directly with peru_production.load_bcrp, no order dependency), within 2%; the table is written to
output/minem_vs_bcrp.csv and the mismatching years are listed (and registered as a count). They match in 2005-14,
2017-19 (2012 and 2019 asserted); they do NOT match in 2001-04, 2015-16 (the old docstring's "2016 matches exactly" was false:
MINEM 17,569 kg vs BCRP 16,223 kg) nor from 2020 (MINEM files 10-50% above BCRP). Rule: for DECLARED output after
2020 we cite the BCRP series (gold_bcrp_declared_*_kg); the MINEM files are used only for the split declared vs
estimate up to 2019.
Output: data_intermediate/minem_mdd_gold.csv (year, declared_kg, estimate_kg, total_kg); numbers gold_minem_*, gold_bcrp_*.
"""
from __future__ import annotations
import io
import re
import warnings
import zipfile

import numpy as np
import pandas as pd

from common import ROOT, OUT
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
    from peru_production import load_bcrp
    b = load_bcrp()[0].set_index("year").grams / 1000
    d["bcrp_kg"] = b.reindex(d.index)
    d["rel_diff"] = (d.total_kg - d.bcrp_kg) / d.bcrp_kg
    d["match_2pct"] = d.rel_diff.abs() <= 0.02
    d.round(4).to_csv(OUT / "minem_vs_bcrp.csv")
    for y, r in d.iterrows():
        checks.check_documented(f"MINEM Madre de Dios gold {y}, declared + estimate vs BCRP, kg (within 2%?)",
                                r.total_kg, r.bcrp_kg, "OK" if r.match_2pct else "MISMATCH")
    bad = d.index[~d.match_2pct].tolist()
    print(f"MINEM vs BCRP: {int(d.match_2pct.sum())} of {len(d)} years match within 2%; mismatches: {bad}")
    checks.check("MINEM Madre de Dios gold 2019, declared + artisanal estimate, kg (BCRP 2019 series)", d.loc[2019, "total_kg"], b[2019], tol=0.02 * b[2019])
    checks.check("MINEM Madre de Dios gold 2012, all declared, kg (BCRP 2012 series)", d.loc[2012, "total_kg"], b[2012], tol=0.02 * b[2012])
    checks.save()
    reg.add("gold_minem_bcrp_n_match", int(d.match_2pct.sum()), "count", f"Years 2001-2025 in which MINEM declared + "
            f"estimate equals the BCRP series within 2% (mismatches: {', '.join(map(str, bad))})", "description", SRC)
    for y in range(2020, 2026):
        reg.add(f"gold_bcrp_declared_{y}_kg", b[y], "kg", f"Declared gold output, Madre de Dios, {y}: BCRP series "
                "RD15556DA (source MINEM); from 2020 the official series holds declared output only. Cite this, not the "
                "MINEM file value", "description", "BCRP series RD15556DA (original source MINEM)",
                measure="gold_kg", zone="mdd", period=str(y))
    for y in (2014, 2015, 2016, 2018, 2019, 2020, 2021, 2024, 2025):
        if y in d.index:
            note = "" if y < 2020 else "; from 2020 the MINEM file differs from BCRP: cite gold_bcrp_declared_*_kg"
            reg.add(f"gold_minem_declared_{y}_kg", d.loc[y, "declared_kg"], "kg", f"Gold declared by producers in Madre de Dios, {y} (MINEM file){note}", "description", SRC,
                    measure="gold_kg", zone="mdd", period=str(y))
            reg.add(f"gold_minem_estimate_{y}_kg", d.loc[y, "estimate_kg"], "kg", f"MINEM estimate of artisanal gold, Madre de Dios, {y} (0 = not in the file)", "description", SRC,
                    measure="gold_kg", zone="mdd", period=str(y))
    last_est = d.index[d.estimate_kg > 0].max()
    figure(d, b)
    reg.add("gold_minem_last_estimate_year", last_est, "year", "Last year in which MINEM's files include the artisanal estimate for Madre de Dios", "description", SRC)
    return d


def figure(d, bcrp):
    import matplotlib.pyplot as plt
    from common import OUT, style_axes, finish_figure, headline, callout, period_band, C, INK, INK2
    yrs = list(range(2010, 2026)); d = d.loc[yrs]
    dec, est = d.declared_kg / 1000, d.estimate_kg / 1000
    fig, ax = plt.subplots(figsize=(9, 4.6))
    headline(fig, "Official gold 'fell' in 2020 because the ministry stopped adding its artisanal estimate",
             "Madre de Dios gold in the official series, tonnes per year: what producers declared plus MINEM's estimate")
    period_band(ax, 2014.5, 2019.5, "2015–19: artisanal output\ncounted as an estimate")
    ax.bar(yrs, dec, color=C["gold"], width=0.72)
    ax.bar(yrs, est, bottom=dec, color="#ecd59a", width=0.72)
    for x, lab in ((2014.5, "2015: artisanal output\nmoves to an estimate"), (2019.5, "2020: estimate no longer\nin the files")):
        ax.axvline(x, color=INK, lw=1.1, zorder=0.5)
    ax.text(2019.7, 24, "2020: estimate no longer in the files.\nWhat remains is declared output only\n"
            f"(central bank): {bcrp[2020] / 1000:.1f} t (2020) → {bcrp[2025] / 1000:.1f} t (2025).", fontsize=8, color=INK,
            va="top", ha="left", linespacing=1.35)
    from matplotlib.patches import Patch
    ax.plot(yrs[-6:], [bcrp[y] / 1000 for y in yrs[-6:]], "o", color=INK, ms=3.5, zorder=4)
    ax.set_ylim(0, 29); ax.set_ylabel("tonnes"); style_axes(ax)
    ax.set_xticks(yrs); ax.set_xticklabels([f"'{str(y)[2:]}" for y in yrs])
    from matplotlib.lines import Line2D
    ax.legend(handles=[Patch(color=C["gold"], label="Declared by producers (MINEM files)"),
                       Patch(color="#ecd59a", label="Ministry estimate for artisanal miners"),
                       Line2D([], [], marker="o", ls="", color=INK, ms=4, label="Central bank series, 2020–25 (cite)")],
              loc="upper left", bbox_to_anchor=(0.0, 1.0), fontsize=8, handlelength=1.2, borderaxespad=0.2)
    finish_figure(fig, f"{SRC}; BCRP series RD15556DA. Both parts sum to the central bank series in 2005-14 and 2017-19 "
                       "(within 2%; every year listed in output/minem_vs_bcrp.csv), not in 2001-04, 2015-16 nor from 2020, when the "
                       "MINEM files run above the central bank: for declared output after 2020 we cite the central bank "
                       "(dots). Description.",
                  OUT / "fig_peru_gold_definition.png")
