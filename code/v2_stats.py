"""Plan v2: statistical tests for every movement and comparison (1-km cell panel, Madre de Dios study window).

WHY: the zone-level comparisons have one treated unit, so no standard errors. Cutting the same pixels into 1-km
cells gives ~14,000 units per year. We can then estimate how new mining changed in each zone, or each distance band
from the highway, relative to the rest of the study window, with cell and year fixed effects, and standard errors
clustered by 10 x 10 km blocks (nearby cells share shocks; Bertrand, Duflo & Mullainathan 2004 style clustering).

Panel: every 1-km cell in the study window (lon 70.65-69.30 W, lat 13.30-12.40 S) inside Madre de Dios, 2010-2025.
Cells never mined stay in the panel with zeros (selecting only ever-mined cells would select on the outcome).
Outcome y = land mined for the first time (ha per cell-year); robustness: returns to old pits; PPML (Poisson) for the
many zeros; gold-bearing share x year fixed effects (cells richer in gold may follow the gold price differently).
Periods: pre 2014-18 (reference), during 2019-21, after 2022-25. Reference cells = cells outside the named zones
(mostly the rest of the mining corridor and communities far from La Pampa) - itself a possible displacement target,
so coefficients are RELATIVE movements.

  S1 zone x period DiD:  y_ct = a_c + g_t + sum_z sum_p b_zp [zone = z][period = p] (+ gold_share x year FE)
  S2 event study for La Pampa and the corridor across the road (year coefficients, 2018 = 0) + joint pre-trend test
  S3 distance-to-highway gradient (bands south/north x period), La Pampa longitudes
  S4 the "extra buffer zone" (Amarakaeri BZ, west of the corridor; Mercurio extension in 2020): 2020-21 vs pre
All coefficients are DESCRIPTION of relative changes; the one causal sentence stays conditional (see the brief).
"""
from __future__ import annotations
import warnings
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pyfixest as pf

from common import ROOT, OUT, style_axes, finish_figure
import raster_zones as rz

INTER = ROOT / "data_intermediate"
SRC = "MapBiomas Peru Col 4 rasters, 1-km cells (raster_zones.py), zones v2; clustered by 10-km blocks"
FOCAL = {7: "La Pampa sector", 5: "Corridor across the road", 9: "Amarakaeri BZ (extra buffer zone)",
         8: "Rest of Tambopata BZ", 3: "Kotsimba", 1: "Tambopata reserve"}
PER = {"during": (2019, 2021), "after": (2022, 2025)}
Y0, Y1 = 2010, 2025


def panel():
    a = pd.read_csv(rz.OUT_CELLATTR)
    g = pd.read_csv(INTER / "cell_gold_v2.csv")
    y = pd.read_csv(rz.OUT_CELL)
    a = a.merge(g, on="cell", how="left")
    idx = pd.MultiIndex.from_product([a.cell, range(Y0, Y1 + 1)], names=["cell", "year"])
    y = y[y.year.between(Y0, Y1)].set_index(["cell", "year"]).reindex(idx).fillna(0).reset_index()
    d = y.merge(a, on="cell")
    nc = int(np.ceil((rz.STUDY[2] - rz.STUDY[0]) / (rz.CELL_PX * 0.000269495)))       # cells per row
    r_, c_ = (d.cell - 1) // nc, (d.cell - 1) % nc
    d["block"] = (r_ // 10) * 1000 + (c_ // 10)                                       # 10 x 10 km blocks
    d["focal"] = d.zone.map(FOCAL).fillna("reference")
    for p, (a0, a1) in PER.items():
        d[f"post_{p}"] = d.year.between(a0, a1).astype(int)
    d["gold_share"] = d.gold_share.fillna(0)
    d["gold_bin"] = pd.cut(d.gold_share, [-0.01, 0.25, 0.75, 1.01], labels=["low", "mid", "high"]).astype(str)
    return d


def zone_did(d, outcome="new_land_ha", gold=False, poisson=False):
    rhs = []
    for z in FOCAL.values():
        key = "".join(ch for ch in z.lower() if ch.isalnum())[:14]
        for p in PER:
            col = f"{key}_{p}"
            d[col] = ((d.focal == z) & (d[f"post_{p}"] == 1)).astype(int)
            rhs.append(col)
    fe = "cell + year" + (" + gold_bin^year" if gold else "")
    fml = f"{outcome} ~ {' + '.join(rhs)} | {fe}"
    f = (pf.fepois if poisson else pf.feols)(fml, data=d, vcov={"CRV1": "block"})
    return f


def tidy_coef(f, label):
    t = f.tidy().reset_index().rename(columns={"Coefficient": "term"})
    t["spec"] = label
    return t[["spec", "term", "Estimate", "Std. Error", "Pr(>|t|)", "2.5%", "97.5%"]]


def event(d, zone_name, outcome="new_land_ha"):
    dd = d[(d.focal == zone_name) | (d.focal == "reference")].copy()
    dd["treat"] = (dd.focal == zone_name).astype(int)
    f = pf.feols(f"{outcome} ~ i(year, treat, ref=2018) | cell + year", data=dd, vcov={"CRV1": "block"})
    t = f.tidy().reset_index()
    t["year"] = t.Coefficient.str.extract(r"(\d{4})").astype(int)
    pre = [c for c in f.coef().index if any(str(y) in c for y in range(2010, 2018))]
    R = np.zeros((len(pre), len(f.coef()))); names = list(f.coef().index)
    for i, c in enumerate(pre):
        R[i, names.index(c)] = 1
    w = f.wald_test(R=R)
    return t, w


def gradient(d):
    dd = d[d.lon.between(*rz.LP_ALT["wide"]) & d.road_km.notna()].copy()
    bins = [-30, -10, -5, 0, 5, 10, 20, 30]
    labels = ["S 10-30", "S 5-10", "S 0-5", "N 0-5", "N 5-10", "N 10-20", "N 20-30"]
    dd["band"] = pd.cut(dd.road_km, bins, labels=labels).astype(str)
    rhs = []
    for b in labels:
        if b == "S 10-30":
            continue                                                     # reference band: south 10-30 km
        for p in PER:
            col = f"b_{b.replace(' ', '').replace('-', '_')}_{p}"
            dd[col] = ((dd.band == b) & (dd[f"post_{p}"] == 1)).astype(int); rhs.append(col)
    f = pf.feols(f"new_land_ha ~ {' + '.join(rhs)} | cell + year", data=dd, vcov={"CRV1": "block"})
    return f, labels


def fig_zone(t):
    m = t[t.spec == "S1 main"].copy()
    m["zone"] = m.term.str.rsplit("_", n=1).str[0]; m["per"] = m.term.str.rsplit("_", n=1).str[1]
    names = {"".join(ch for ch in z.lower() if ch.isalnum())[:14]: z for z in FOCAL.values()}
    m["zone"] = m.zone.map(names)
    fig, ax = plt.subplots(figsize=(9.5, 4.6))
    ys = np.arange(len(FOCAL))
    for j, (p, col) in enumerate((("during", "#eb6834"), ("after", "#2a78d6"))):
        mm = m[m.per == p].set_index("zone").reindex(list(FOCAL.values()))
        ax.errorbar(mm.Estimate, ys + (j - 0.5) * 0.28, xerr=[mm.Estimate - mm["2.5%"], mm["97.5%"] - mm.Estimate],
                    fmt="o", color=col, ms=6, capsize=3, label={"during": "2019-21 vs 2014-18", "after": "2022-25 vs 2014-18"}[p])
    ax.axvline(0, color="black", lw=0.8)
    ax.set_yticks(ys); ax.set_yticklabels(list(FOCAL.values()), fontsize=9); ax.invert_yaxis()
    ax.set_xlabel("Change in land mined for the first time, ha per 1-km cell per year (95% CI)")
    style_axes(ax); ax.xaxis.grid(True, color="#E8EEF0"); ax.yaxis.grid(False)
    ax.legend(fontsize=8, frameon=False, loc="lower right")
    ax.set_title("Per-cell change by zone, relative to the rest of the study area", loc="left", fontsize=10.5, fontweight="bold")
    finish_figure(fig, f"Source: {SRC}. OLS with cell and year fixed effects, errors clustered by 10-km block. "
                       "Reference = cells outside the named zones. Description.", OUT / "fig_v2_stats_zones.png", rect_bottom=0.12)


def fig_event(ev):
    fig, axes = plt.subplots(1, 2, figsize=(12, 4), sharey=False)
    for ax, (nm, (t, w)) in zip(axes, ev.items()):
        ax.fill_between(t.year, t["2.5%"], t["97.5%"], color="#9cc0ea", alpha=0.6, lw=0)
        ax.plot(t.year, t.Estimate, "o-", color="#2a78d6", ms=4)
        ax.axhline(0, color="black", lw=0.8); ax.axvline(2018.5, color="#0b0b0b", lw=1.2)
        ax.set_title(f"{nm}\npre-trend test 2010-17: p = {float(w['pvalue']):.2f}", loc="left", fontsize=9.5)
        style_axes(ax)
    axes[0].set_ylabel("ha per cell-year vs reference,\n2018 = 0 (95% CI)")
    fig.suptitle("Year by year, per 1-km cell: La Pampa fell from 2020, the corridor across the road rose from 2019",
                 x=0.01, ha="left", fontsize=11, fontweight="bold")
    finish_figure(fig, f"Source: {SRC}. Event study with cell and year fixed effects; joint F-test that all 2010-17 "
                       "coefficients are zero. Description.", OUT / "fig_v2_stats_event.png", rect_bottom=0.12)


def run(reg):
    print("\n== v2 statistics (1-km cell panel) ==")
    if not (rz.OUT_CELL.exists() and (INTER / "cell_gold_v2.csv").exists()):
        warnings.warn("v2_stats: inputs missing; skipping"); return
    d = panel()
    print(f"panel: {d.cell.nunique():,} cells x {d.year.nunique()} years, {d.block.nunique()} clusters")
    specs = [("S1 main", zone_did(d)), ("S1 + gold x year FE", zone_did(d, gold=True)),
             ("S1 returns to old pits", zone_did(d, outcome="remined_ha")),
             ("S1 Poisson (PPML)", zone_did(d, poisson=True))]
    t = pd.concat([tidy_coef(f, s) for s, f in specs])
    ev = {nm: event(d, nm) for nm in ("La Pampa sector", "Corridor across the road")}
    g, labels = gradient(d)
    tg = tidy_coef(g, "S3 road gradient")
    t = pd.concat([t, tg]); t.round(4).to_csv(OUT / "v2_stats_coefficients.csv", index=False)
    print(t[t.spec.isin(["S1 main", "S3 road gradient"])].round(3).to_string(index=False))
    fig_zone(t); fig_event(ev)
    reg.add("st_n_cells", d.cell.nunique(), "count", "1-km cells in the statistical panel", "description", SRC)
    reg.add("st_n_clusters", d.block.nunique(), "count", "10-km clusters", "description", SRC)
    for s, f in specs:
        tag = {"S1 main": "main", "S1 + gold x year FE": "gold", "S1 returns to old pits": "remine", "S1 Poisson (PPML)": "ppml"}[s]
        co, se, pv = f.coef(), f.se(), f.pvalue()
        for term in co.index:
            reg.add(f"st_{tag}_{term}", co[term], "ha/cell-yr" if tag != "ppml" else "log points",
                    f"{s}: {term}", "description", SRC)
            reg.add(f"st_{tag}_{term}_p", pv[term], "p-value", f"{s}: p-value of {term} (CRV1 by 10-km block)", "description", SRC)
    for nm, (tt, w) in ev.items():
        key = "lp" if nm.startswith("La Pampa") else "across"
        reg.add(f"st_event_{key}_pretrend_p", float(w["pvalue"]), "p-value", f"Joint pre-trend test 2010-17, {nm}", "description", SRC)
        for _, r in tt.iterrows():
            if r.year in (2016, 2019, 2020, 2021, 2023):
                reg.add(f"st_event_{key}_{r.year}", r.Estimate, "ha/cell-yr", f"Event study {nm}, {r.year} vs 2018", "description", SRC)
                reg.add(f"st_event_{key}_{r.year}_p", r["Pr(>|t|)"], "p-value", f"Event study {nm}, {r.year}, p-value", "description", SRC)
    for term in g.coef().index:
        reg.add(f"st_grad_{term}", g.coef()[term], "ha/cell-yr", f"Road gradient: {term} (ref: south 10-30 km)", "description", SRC)
        reg.add(f"st_grad_{term}_p", g.pvalue()[term], "p-value", f"Road gradient: p-value of {term}", "description", SRC)
    return t
