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
  S2 event study for La Pampa and the corridor across the road (year coefficients, pooled 2014-18 = 0) + joint pre-trend test
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

from common import (ROOT, OUT, style_axes, finish_figure, headline, callout, period_band, add_event_markers, EVENT_TITLE_PAD,
                    C, INK, INK2, MUTED, AXIS, GRID)
import raster_zones as rz

INTER = ROOT / "data_intermediate"
SRC = "MapBiomas Peru Col 4 rasters, 1-km cells (raster_zones.py), zones v2; clustered by 10-km blocks"
FOCAL = {7: "La Pampa sector", 5: "Corridor across the road", 9: "Amarakaeri BZ (extra buffer zone)",
         8: "Rest of Tambopata BZ", 3: "Kotsimba", 1: "Tambopata reserve"}
PER = {"during": (2019, 2021), "after": (2022, 2025)}
Y0, Y1 = 2010, 2025          # event studies use 2010-2025; the DiD uses 2014-2025 (baseline 2014-18 = labels)
CLEAN_DROP = (4, 6)          # reference cells dropped in the clean spec: other native communities, rest of the legal corridor


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


def _demean2(M, a, b, iters=50):
    """Two-way within transformation (cell and year) by alternating projections."""
    M = M.astype(float).copy()
    ia, ib = pd.factorize(a)[0], pd.factorize(b)[0]
    na, nb = ia.max() + 1, ib.max() + 1
    ca, cb = np.bincount(ia, minlength=na)[:, None], np.bincount(ib, minlength=nb)[:, None]
    for _ in range(iters):
        ma = np.zeros((na, M.shape[1])); np.add.at(ma, ia, M); M -= (ma / ca)[ia]
        mb = np.zeros((nb, M.shape[1])); np.add.at(mb, ib, M); M -= (mb / cb)[ib]
    return M


def wild_cluster_bootstrap(d, outcome, rhs, term, cluster, reps=999, seed=1):
    """Restricted wild cluster bootstrap (WCR, Rademacher), after removing cell and year fixed effects (FWL).
    Returns the two-sided p-value for H0: coefficient on `term` = 0, with CRV1 t-statistics."""
    Z = _demean2(np.column_stack([d[outcome].values] + [d[c].values for c in rhs]), d.cell.values, d.year.values)
    y, X = Z[:, 0], Z[:, 1:]
    k = rhs.index(term)
    g = pd.factorize(d[cluster].values)[0]; G = g.max() + 1
    def tstat(yv):
        XtX_inv = np.linalg.pinv(X.T @ X); bhat = XtX_inv @ X.T @ yv; e = yv - X @ bhat
        sc = np.zeros((G, X.shape[1])); np.add.at(sc, g, X * e[:, None])
        V = XtX_inv @ (sc.T @ sc) @ XtX_inv * G / (G - 1)
        return bhat[k] / np.sqrt(V[k, k])
    t0 = tstat(y)
    Xr = np.delete(X, k, axis=1)
    br = np.linalg.lstsq(Xr, y, rcond=None)[0]; fit_r = Xr @ br; u_r = y - fit_r
    rng = np.random.default_rng(seed); ts = np.empty(reps)
    for i in range(reps):
        w = rng.choice([-1.0, 1.0], size=G)
        ts[i] = tstat(fit_r + w[g] * u_r)
    return float(np.mean(np.abs(ts) >= abs(t0)))


def zone_did(d, outcome="new_land_ha", gold=False, poisson=False, clean=True):
    """Clean (main, after the critical review): reference = cells outside the named zones AND outside the legal corridor
    and native communities (displacement targets), years 2014-2025 so the baseline is 2014-18. clean=False reproduces
    the earlier, contaminated reference (rest of corridor + communities included)."""
    d = d[d.year >= 2014]
    if clean:
        d = d[~((d.focal == "reference") & d.zone.isin(CLEAN_DROP))]
    d = d.copy()
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
    """Event study with the POOLED 2014-18 period as reference (not the single high year 2018); clean reference cells;
    joint pre-trend test on the 2010-13 leads."""
    dd = d[(d.focal == zone_name) | ((d.focal == "reference") & ~d.zone.isin(CLEAN_DROP))].copy()
    dd["treat"] = (dd.focal == zone_name).astype(int)
    yrs = [y for y in range(Y0, Y1 + 1) if not 2014 <= y <= 2018]
    for y in yrs:
        dd[f"ev_{y}"] = ((dd.year == y) & (dd.treat == 1)).astype(int)
    f = pf.feols(f"{outcome} ~ {' + '.join(f'ev_{y}' for y in yrs)} | cell + year", data=dd, vcov={"CRV1": "block"})
    t = f.tidy().reset_index()
    t["year"] = t.Coefficient.str.extract(r"(\d{4})").astype(int)
    base = pd.DataFrame({"Coefficient": [f"ref_{y}" for y in range(2014, 2019)], "Estimate": 0.0, "Std. Error": 0.0,
                         "Pr(>|t|)": np.nan, "2.5%": 0.0, "97.5%": 0.0, "year": range(2014, 2019)})
    t = pd.concat([t, base], ignore_index=True).sort_values("year")
    pre = [c for c in f.coef().index if any(str(y) in c for y in range(2010, 2014))]
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


def _p(v):
    return "p < 0.01" if v < 0.005 else f"p = {v:.2f}"


def _signed(v):
    return "0.0" if abs(v) < 0.05 else f"{v:+.1f}".replace("-", "−")


ZONE_COL = {"La Pampa sector": C["lapampa"], "Corridor across the road": C["corridor"],
            "Amarakaeri BZ (extra buffer zone)": C["buffer"], "Rest of Tambopata BZ": C["lapampa_tint"],
            "Kotsimba": C["native"], "Tambopata reserve": C["reserve"]}


def fig_zone(t):
    m = t[t.spec == "S1 main"].copy()
    m["zone"] = m.term.str.rsplit("_", n=1).str[0]; m["per"] = m.term.str.rsplit("_", n=1).str[1]
    names = {"".join(ch for ch in z.lower() if ch.isalnum())[:14]: z for z in FOCAL.values()}
    m["zone"] = m.zone.map(names)
    fig, ax = plt.subplots(figsize=(9, 5.2))
    lp_p = float(m[(m.zone == "La Pampa sector") & (m.per == "during")]["Pr(>|t|)"].iloc[0])
    headline(fig, "La Pampa fell" + (" (CI includes zero)" if lp_p >= 0.05 else "") + "; the corridor across the road rose",
             "Change in first-time mining vs 2014–18, ha per cell per year, relative to clean comparison cells (95% CI)")
    zones = list(FOCAL.values()); ys = np.arange(len(zones))
    for j, p in enumerate(("during", "after")):
        mm = m[m.per == p].set_index("zone").reindex(zones)
        y = ys + (j - 0.5) * 0.34
        cols = [ZONE_COL[z] for z in zones]
        ax.hlines(y, mm["2.5%"], mm["97.5%"], colors=cols, lw=2.2 if p == "during" else 1.4, alpha=1 if p == "during" else 0.55)
        ax.scatter(mm.Estimate, y, s=42, zorder=3, color=cols if p == "during" else "white", edgecolors=cols, linewidths=1.6)
        for z, yy, e, hi, pv in zip(zones, y, mm.Estimate, mm["97.5%"], mm["Pr(>|t|)"]):
            ax.annotate(f"{'2019–21' if p == 'during' else '2022–25'}  {_signed(e)}  ({_p(pv)})", xy=(hi, yy), xytext=(6, 0),
                        textcoords="offset points", va="center", fontsize=7.5, color=INK if p == "during" else INK2)
    ax.axvline(0, color=INK2, lw=0.9)
    ax.set_yticks(ys); ax.set_yticklabels(zones); ax.invert_yaxis()
    ax.tick_params(axis="y", length=0, labelsize=9, labelcolor=INK)
    ax.spines[["top", "right", "left"]].set_visible(False)
    ax.xaxis.grid(True, color=GRID, lw=0.6); ax.set_axisbelow(True)
    lo, hi = m["2.5%"].min(), m["97.5%"].max()
    ax.set_xlim(lo - 0.15, hi + 1.55)
    ax.set_xlabel("← less first-time mining          ha per 1-km cell per year          more →")
    ax.text(1.0, 1.02, "●  2019–21 (operation years)     ○  2022–25", transform=ax.transAxes, ha="right",
            va="bottom", fontsize=8, color=INK2)
    finish_figure(fig, f"{SRC}. OLS with cell and year fixed effects, errors clustered by 10-km block. "
                       "Reference = cells outside the named zones, the corridor and native communities; baseline 2014–18. Description.",
                  OUT / "fig_v2_stats_zones.png")


def fig_event(ev):
    fig, axes = plt.subplots(1, 2, figsize=(9, 4.4), sharey=True, gridspec_kw={"wspace": 0.12})
    headline(fig, "Year by year: La Pampa fell from 2020; the corridor across the road rose from 2019",
             "Event study per 1-km cell: first-time mining vs the 2014–18 mean (= 0), ha per cell per year, 95% CI")
    for ax, (nm, (t, w)) in zip(axes, ev.items()):
        c_ = C["lapampa"] if nm.startswith("La Pampa") else C["corridor"]
        period_band(ax, 2013.5, 2018.5, "reference\n2014–18 = 0")
        ax.fill_between(t.year, t["2.5%"], t["97.5%"], color=c_, alpha=0.16, lw=0)
        ax.plot(t.year, t.Estimate, "-", color=c_, lw=2.2)
        ax.plot(t.year, t.Estimate, "o", color=c_, ms=4.5, mec="white", mew=1)
        ax.axhline(0, color=INK2, lw=0.8)
        pv = float(w["pvalue"])
        style_axes(ax, fmt=False)
        ax.set_xlim(2009.5, 2025.5); ax.set_xticks(range(2010, 2026, 3))
        pad = add_event_markers(ax, label=True)
        ax.set_title(f"{nm}\nPre-trend test 2010–13: {_p(pv)}" + (", fails" if pv < 0.05 else ", passes"),
                     pad=pad, fontsize=9.5)
    finish_figure(fig, f"{SRC}. Event study with cell and year fixed effects; reference = the pooled 2014–18 period (shaded); "
                       "comparison cells exclude the legal corridor and native communities; joint test that the 2010–13 leads are zero. "
                       "Description.", OUT / "fig_v2_stats_event.png", event_note=True)


def run(reg):
    print("\n== v2 statistics (1-km cell panel) ==")
    if not (rz.OUT_CELL.exists() and (INTER / "cell_gold_v2.csv").exists()):
        warnings.warn("v2_stats: inputs missing; skipping"); return
    d = panel()
    print(f"panel: {d.cell.nunique():,} cells x {d.year.nunique()} years, {d.block.nunique()} clusters")
    specs = [("S1 main", zone_did(d)), ("S1 + gold x year FE", zone_did(d, gold=True)),
             ("S1 returns to old pits", zone_did(d, outcome="remined_ha")),
             ("S1 Poisson (PPML)", zone_did(d, poisson=True)),
             ("S1 contaminated reference", zone_did(d, clean=False))]
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
        tag = {"S1 main": "main", "S1 + gold x year FE": "gold", "S1 returns to old pits": "remine", "S1 Poisson (PPML)": "ppml",
               "S1 contaminated reference": "contam"}[s]
        co, se, pv = f.coef(), f.se(), f.pvalue()
        for term in co.index:
            reg.add(f"st_{tag}_{term}", co[term], "ha/cell-yr" if tag != "ppml" else "log points",
                    f"{s}: {term}", "description", SRC)
            reg.add(f"st_{tag}_{term}_p", pv[term], "p-value", f"{s}: p-value of {term} (CRV1 by 10-km block)", "description", SRC)
    # wild cluster bootstrap (Rademacher, 999 draws): few clusters contain the treated zones
    main = specs[0][1]
    # cache keyed by a hash of its inputs (the bootstrap panel, draws, seed): any change in the inputs recomputes it
    import hashlib
    WCB_REPS, WCB_SEED = 999, 1
    cache = INTER / "wcb_cache_v2.csv"
    dm = d[d.year >= 2014]
    dm = dm[~((dm.focal == "reference") & dm.zone.isin(CLEAN_DROP))].copy()
    rhs = []
    for z in FOCAL.values():
        key = "".join(ch for ch in z.lower() if ch.isalnum())[:14]
        for p_ in PER:
            dm[f"{key}_{p_}"] = ((dm.focal == z) & (dm[f"post_{p_}"] == 1)).astype(int); rhs.append(f"{key}_{p_}")
    cols = ["cell", "year", "block", "new_land_ha"] + rhs
    h = hashlib.sha256(pd.util.hash_pandas_object(dm[cols].sort_values(["cell", "year"]), index=False).values.tobytes()
                       + f"|{WCB_REPS}|{WCB_SEED}".encode()).hexdigest()[:16]
    c_ = pd.read_csv(cache) if cache.exists() else None
    if c_ is not None and "input_hash" in c_ and (c_.input_hash.astype(str) == h).all():
        wcb = c_.set_index("term").p
    else:
        print("wild cluster bootstrap: inputs changed or no cache, recomputing (~30 s)")
        wcb = {term: wild_cluster_bootstrap(dm, "new_land_ha", rhs, term, "block", reps=WCB_REPS, seed=WCB_SEED)
               for term in ("lapampasector_during", "corridoracross_during")}
        pd.DataFrame({"term": list(wcb), "p": list(wcb.values()), "input_hash": h}).to_csv(cache, index=False)
        wcb = pd.Series(wcb)
    for term, key in (("lapampasector_during", "lp"), ("corridoracross_during", "across")):
        if term in wcb:
            reg.add(f"st_wcb_{key}_p", float(wcb[term]), "p-value", f"Wild cluster bootstrap p-value (WCR, 999 Rademacher draws, 10-km blocks, after removing cell and year effects), {term}", "description", SRC)
    dm = d[d.year >= 2014]
    for z, key in (("La Pampa sector", "lp"), ("Corridor across the road", "across")):
        reg.add(f"st_clusters_{key}", dm[dm.focal == z].block.nunique(), "count", f"10-km clusters containing {z} cells", "description", SRC)
    reg.add("st_n_ref_cells_clean", d[(d.focal == "reference") & ~d.zone.isin(CLEAN_DROP)].cell.nunique(), "count", "Reference cells in the clean spec", "description", SRC)
    for nm, (tt, w) in ev.items():
        key = "lp" if nm.startswith("La Pampa") else "across"
        reg.add(f"st_event_{key}_pretrend_p", float(w["pvalue"]), "p-value", f"Joint pre-trend test (2010-13 leads, 2014-18 pooled reference), {nm}", "description", SRC)
        for _, r in tt.iterrows():
            if r.year in (2012, 2019, 2020, 2021, 2023):
                reg.add(f"st_event_{key}_{r.year}", r.Estimate, "ha/cell-yr", f"Event study {nm}, {r.year} vs the pooled 2014-18 mean", "description", SRC)
                reg.add(f"st_event_{key}_{r.year}_p", r["Pr(>|t|)"], "p-value", f"Event study {nm}, {r.year}, p-value", "description", SRC)
    for term in g.coef().index:
        reg.add(f"st_grad_{term}", g.coef()[term], "ha/cell-yr", f"Road gradient: {term} (ref: south 10-30 km)", "description", SRC)
        reg.add(f"st_grad_{term}_p", g.pvalue()[term], "p-value", f"Road gradient: p-value of {term}", "description", SRC)
    return t
