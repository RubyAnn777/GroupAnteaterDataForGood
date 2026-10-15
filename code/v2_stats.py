"""1-km cell panel: zone x period DiD, event studies, road gradient, depletion (hazard). DESCRIPTION (plan v3).

WHY: the zone-level comparisons have one treated unit, so no standard errors. Cutting the same pixels into 1-km cells
gives ~14,000 units per year. We estimate how mining additions changed in each registry zone, or each distance band
from the highway, relative to comparison cells, with cell and year fixed effects and standard errors clustered by
10 x 10 km blocks (nearby cells share shocks). With one road and few blocks containing the target, these p-values are
descriptive, not a test of Mercurio.

Panel: every 1-km cell of data_intermediate/cell_attr.csv (lon 70.65-69.30 W, lat 13.30-12.40 S, inside the study
region), years definitions.PANEL_YEARS (2011-2025). Cells never mined stay in with zeros (selecting ever-mined cells
would select on the outcome). Each cell takes its MAJORITY registry zone and tenure (cell_attr.csv).
OUTCOME (definitions.OUTCOME): net additions, ha per cell-year = new + re-mined - stopped. The OLS designs are linear,
so each is also run for the three parts and the coefficients add up (asserted). Non-linear versions keep their own
measure: Poisson (PPML) and the hazard (at-risk) outcome use NEW LAND (first-time mining) only, labelled so.
Periods: definitions.PERIODS: reference = pooled 2014-18 ("pre_long"), "during" 2019-21 (Mercurio and what followed),
"later" 2022-25 (later years; also without 2023).
Focal zones: La Pampa sector, corridor across the road, rest of the Tambopata BZ, Amarakaeri BZ (whole), Tambopata
National Reserve. Comparison cells ("against comparison cells with little mining"): cells outside the focal zones,
outside the rest of the corridor and the native communities (displacement targets) and with tenure "none": other
protected areas, other buffer zones, rest of Madre de Dios. They hold almost no mining, so a focal coefficient is close
to the focal zone's own before/after change; it is NOT a clean counterfactual. A second version keeps every non-focal
cell ("all other cells", includes the corridor and communities).

  S1 zone x period DiD:  y_ct = a_c + g_t + sum_z sum_p b_zp [zone = z][period = p]   (+ gold-bearing bin x year FE)
  S2 event study for La Pampa and the corridor across the road (year coefficients; pooled 2014-18 = 0) + joint test
     that the 2011-13 leads are zero (2010-13 registered as a sensitivity: the 2010 lead decides La Pampa's test)
  S3 distance-to-highway gradient (bands south/north x period), La Pampa longitudes (definitions.LP_LON)
  S4 depletion: zone-level hazard (new land / land not yet mined at t-1), cell hazard OLS, 2018-depletion bin x year
     FE, and La Pampa cells by 2018 depletion tercile (review D-S8-3)
"""
from __future__ import annotations
import warnings
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pyfixest as pf

from common import (ROOT, OUT, style_axes, finish_figure, headline, period_band, add_event_markers, C, INK, INK2,
                    GRID)
import definitions as D
import zonedata as Z
import raster_zones as rz

INTER = ROOT / "data_intermediate"
GOLD = INTER / "cell_gold.csv"
WCB_CACHE = INTER / "wcb_cache.csv"
SRC = f"{D.SOURCE}, 1-km cells (raster_zones.py), majority registry zone; errors clustered by 10-km blocks"
FOCAL = {"lapampa": "La Pampa sector", "corridor_across": "Corridor across the road",
         "tambopata_bz_rest": "Rest of Tambopata buffer zone", "amarakaeri_bz": "Amarakaeri buffer zone",
         "tambopata_nr": "Tambopata National Reserve"}
CLEAN_ZONES = ("other_anp", "bahuaja_bz", "other_bz", "rest_mdd")      # comparison cells: these zones, tenure "none"
PER = ("during", "later")
MEAS = ["net"] + D.PARTS
Y0, Y1 = D.PANEL_YEARS
B0 = D.PERIODS["pre_long"][0]                                          # the DiD sample starts with the reference


def _cells_per_row() -> int:
    import rasterio
    from rasterio.windows import from_bounds
    with rasterio.open(rz.OUT_FULL) as r:
        sub = from_bounds(*rz.STUDY, r.transform).round_offsets().round_lengths()
    return (int(sub.width) + rz.CELL_PX - 1) // rz.CELL_PX


def panel(y0=None):
    a = pd.read_csv(rz.OUT_CELLATTR)
    a = a.merge(pd.read_csv(GOLD), on="cell", how="left")
    y = pd.read_csv(rz.OUT_CELL)
    # land ever mapped as mining by the end of each year (stock 1985 + new land since): for the hazard outcome
    y = y.sort_values(["cell", "year"])
    y["ever_ha"] = y.groupby("cell").new_ha.cumsum().fillna(0) + y.groupby("cell").mining_ha.transform("first")
    idx = pd.MultiIndex.from_product([a.cell, range(Y0 if y0 is None else y0, Y1 + 1)], names=["cell", "year"])
    ever_lag = y.assign(year=y.year + 1).set_index(["cell", "year"]).ever_ha.reindex(idx).fillna(0).values
    y = y.set_index(["cell", "year"]).reindex(idx).fillna(0).reset_index()
    y["ever_lag_ha"] = ever_lag
    d = y.merge(a, on="cell")
    nc = _cells_per_row()
    r_, c_ = (d.cell - 1) // nc, (d.cell - 1) % nc
    d["block"] = (r_ // 10) * 1000 + (c_ // 10)                                      # 10 x 10 km blocks
    d["focal"] = d.zone.where(d.zone.isin(FOCAL), "reference")
    d["clean"] = (d.focal != "reference") | (d.zone.isin(CLEAN_ZONES) & (d.tenure == "none"))
    for p in PER:
        a0, a1 = D.PERIODS[p]
        d[f"post_{p}"] = d.year.between(a0, a1).astype(int)
    d["gold_share"] = d.gold_share.fillna(0)
    d["gold_bin"] = pd.cut(d.gold_share, [-0.01, 0.25, 0.75, 1.01], labels=["low", "mid", "high"]).astype(str)
    d["at_risk"] = d.area_ha - d.ever_lag_ha
    d["hazard_pct"] = np.where(d.at_risk > 1, 100 * d.new_ha / d.at_risk.clip(lower=1e-9), np.nan)
    e18 = y[y.year == D.REF_YEAR].set_index("cell").ever_lag_ha + y[y.year == D.REF_YEAR].set_index("cell").new_ha
    d["share18"] = d.cell.map((e18 / a.set_index("cell").area_ha).clip(0, 1))
    return d


def did_sample(d, clean=True):
    d = d[d.year >= B0]
    if clean:
        d = d[d.clean]
    d = d.copy()
    rhs = []
    for z in FOCAL:
        for p in PER:
            d[f"{z}_{p}"] = ((d.focal == z) & (d[f"post_{p}"] == 1)).astype(int); rhs.append(f"{z}_{p}")
    return d, rhs


def zone_did(d, outcome="net_ha", gold=False, poisson=False, clean=True, fe_extra="", weights=None):
    dd, rhs = did_sample(d, clean)
    if outcome == "hazard_pct":
        dd = dd.dropna(subset=["hazard_pct"])
    fe = "cell + year" + (" + gold_bin^year" if gold else "") + fe_extra
    return (pf.fepois if poisson else pf.feols)(f"{outcome} ~ {' + '.join(rhs)} | {fe}", data=dd,
                                                vcov={"CRV1": "block"}, **({"weights": weights} if weights else {}))


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
    M = _demean2(np.column_stack([d[outcome].values] + [d[c].values for c in rhs]), d.cell.values, d.year.values)
    y, X = M[:, 0], M[:, 1:]
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


def tidy_coef(f, label, measure):
    t = f.tidy().reset_index().rename(columns={"Coefficient": "term"})
    t["spec"] = label; t["measure"] = measure
    return t[["spec", "measure", "term", "Estimate", "Std. Error", "Pr(>|t|)", "2.5%", "97.5%"]]


def event(d, zone, outcome="net_ha", y0=None):
    """Event study, POOLED 2014-18 reference (definitions.PERIODS['pre_long']), comparison cells; joint pre-trend test
    on the leads before the reference (2011-13; y0 = 2010 adds one lead year, the v2 window, as a sensitivity)."""
    y0 = Y0 if y0 is None else y0
    dd = d[((d.focal == zone) | ((d.focal == "reference") & d.clean)) & (d.year >= y0)].copy()
    dd["treat"] = (dd.focal == zone).astype(int)
    r0, r1 = D.PERIODS["pre_long"]
    yrs = [y for y in range(y0, Y1 + 1) if not r0 <= y <= r1]
    for y in yrs:
        dd[f"ev_{y}"] = ((dd.year == y) & (dd.treat == 1)).astype(int)
    f = pf.feols(f"{outcome} ~ {' + '.join(f'ev_{y}' for y in yrs)} | cell + year", data=dd, vcov={"CRV1": "block"})
    t = f.tidy().reset_index()
    t["year"] = t.Coefficient.str.extract(r"(\d{4})").astype(int)
    base = pd.DataFrame({"Coefficient": [f"ref_{y}" for y in range(r0, r1 + 1)], "Estimate": 0.0, "Std. Error": 0.0,
                         "Pr(>|t|)": np.nan, "2.5%": 0.0, "97.5%": 0.0, "year": range(r0, r1 + 1)})
    t = pd.concat([t, base], ignore_index=True).sort_values("year").set_index("year")
    names = list(f.coef().index)
    pre = [f"ev_{y}" for y in range(y0, r0)]
    R = np.zeros((len(pre), len(names)))
    for i, c in enumerate(pre):
        R[i, names.index(c)] = 1
    return t, f.wald_test(R=R)


GRAD_BINS = [-30, -10, -5, 0, 5, 10, 20, 30]
GRAD_LAB = ["S 10-30", "S 5-10", "S 0-5", "N 0-5", "N 5-10", "N 10-20", "N 20-30"]


def gradient(d, outcome="net_ha"):
    """Road gradient on the La Pampa longitudes (definitions.LP_LON), reference band south 10-30 km, all cells there."""
    dd = d[d.lon.between(*D.LP_LON) & d.road_km.notna() & (d.year >= B0)].copy()
    dd["band"] = pd.cut(dd.road_km, GRAD_BINS, labels=GRAD_LAB).astype(str)
    rhs = []
    for b in GRAD_LAB[1:]:
        for p in PER:
            col = f"b_{b.replace(' ', '').replace('-', '_')}_{p}"
            dd[col] = ((dd.band == b) & (dd[f"post_{p}"] == 1)).astype(int); rhs.append(col)
    return pf.feols(f"{outcome} ~ {' + '.join(rhs)} | cell + year", data=dd, vcov={"CRV1": "block"})


def _p(v):
    return "p < 0.01" if v < 0.005 else f"p = {v:.2f}"


def _signed(v):
    return "0.0" if abs(v) < 0.05 else f"{v:+.1f}".replace("-", "−")


ZONE_COL = {"lapampa": C["lapampa"], "corridor_across": C["corridor"], "amarakaeri_bz": C["buffer"],
            "tambopata_bz_rest": C["lapampa_tint"], "tambopata_nr": C["reserve"]}


def fig_zone(fits):
    co, ci, pv = fits["net"].coef(), fits["net"].confint(), fits["net"].pvalue()
    zones = list(FOCAL)
    lp, ac = co["lapampa_during"], co["corridor_across_during"]
    fig, ax = plt.subplots(figsize=(9, 5.2))
    headline(fig, f"Per 1-km cell, 2019–21: La Pampa {_signed(lp)} ha/yr ({_p(pv['lapampa_during'])}), "
                  f"across the road {_signed(ac)} ({_p(pv['corridor_across_during'])})",
             "Change in net mining additions vs 2014–18, ha per 1-km cell per year, relative to comparison cells with "
             "little mining (95% CI)")
    ys = np.arange(len(zones))
    for j, p in enumerate(PER):
        y = ys + (j - 0.5) * 0.34
        cols = [ZONE_COL[z] for z in zones]
        est = [co[f"{z}_{p}"] for z in zones]
        lo = [ci.loc[f"{z}_{p}"].iloc[0] for z in zones]; hi = [ci.loc[f"{z}_{p}"].iloc[1] for z in zones]
        ax.hlines(y, lo, hi, colors=cols, lw=2.2 if p == "during" else 1.4, alpha=1 if p == "during" else 0.55)
        ax.scatter(est, y, s=42, zorder=3, color=cols if p == "during" else "white", edgecolors=cols, linewidths=1.6)
        for z, yy, e, h in zip(zones, y, est, hi):
            ax.annotate(f"{D.period_label(p)}  {_signed(e)}  ({_p(pv[f'{z}_{p}'])})", xy=(h, yy), xytext=(6, 0),
                        textcoords="offset points", va="center", fontsize=7.5, color=INK if p == "during" else INK2)
    ax.axvline(0, color=INK2, lw=0.9)
    ax.set_yticks(ys); ax.set_yticklabels([FOCAL[z] for z in zones]); ax.invert_yaxis()
    ax.tick_params(axis="y", length=0, labelsize=9, labelcolor=INK)
    ax.spines[["top", "right", "left"]].set_visible(False)
    ax.xaxis.grid(True, color=GRID, lw=0.6); ax.set_axisbelow(True)
    lo, hi = ci.iloc[:, 0].min(), ci.iloc[:, 1].max()
    ax.set_xlim(lo - 0.15, hi + 1.55)
    ax.set_xlabel("← fewer net additions          ha per 1-km cell per year          more →")
    ax.text(1.0, 1.02, "●  2019–21 (Mercurio and what followed)     ○  2022–25 (later years)", transform=ax.transAxes,
            ha="right", va="bottom", fontsize=8, color=INK2)
    finish_figure(fig, f"{SRC}. OLS with cell and year fixed effects. Comparison cells: other protected areas, other buffer "
                       "zones and rest of Madre de Dios with no corridor or community tenure (they hold almost no mining, so "
                       "each coefficient is close to the zone's own change); reference period 2014–18. Description.",
                  OUT / "fig_v2_stats_zones.png")


def fig_event(ev, ev10):
    fig, axes = plt.subplots(1, 2, figsize=(9, 4.4), sharey=True, gridspec_kw={"wspace": 0.12})
    t_lp = ev["lapampa"]["net"][0]
    first_neg = [y for y in range(D.FIRST_POST, Y1 + 1) if t_lp.loc[y, "97.5%"] < 0]
    t_ac = ev["corridor_across"]["net"][0]
    first_pos = [y for y in range(D.FIRST_POST, Y1 + 1) if t_ac.loc[y, "2.5%"] > 0]
    headline(fig, "Net additions per cell: La Pampa " +
             (f"clearly below 2014–18 from {first_neg[0]}" if first_neg else "never clearly below 2014–18") +
             "; across the road " + (f"clearly above from {first_pos[0]}" if first_pos else "never clearly above"),
             "Event study per 1-km cell: net mining additions vs the 2014–18 mean (= 0), ha per cell per year, 95% CI")
    for ax, z in zip(axes, ("lapampa", "corridor_across")):
        t, w = ev[z]["net"]
        c_ = ZONE_COL[z]
        r0, r1 = D.PERIODS["pre_long"]
        period_band(ax, r0 - 0.5, r1 + 0.5, "reference\n2014–18 = 0")
        ax.fill_between(t.index, t["2.5%"], t["97.5%"], color=c_, alpha=0.16, lw=0)
        ax.plot(t.index, t.Estimate, "-", color=c_, lw=2.2)
        ax.plot(t.index, t.Estimate, "o", color=c_, ms=4.5, mec="white", mew=1)
        ax.axhline(0, color=INK2, lw=0.8)
        pv = float(w["pvalue"])
        style_axes(ax, fmt=False)
        ax.set_xlim(Y0 - 0.5, Y1 + 0.5); ax.set_xticks(range(Y0, Y1 + 1, 2))
        pad = add_event_markers(ax, label=True)
        p10 = float(ev10[z]["net"]["pvalue"])
        verdict = lambda q: "rejected" if q < 0.05 else "not rejected"
        ax.set_title(f"{FOCAL[z]}\nPre-trend test, leads 2011–13: {_p(pv)} ({verdict(pv)})\nwith 2010 added: {_p(p10)} ({verdict(p10)})",
                     pad=pad, fontsize=9)
    finish_figure(fig, f"{SRC}. Event study with cell and year fixed effects; reference = the pooled 2014–18 period "
                       "(shaded); comparison cells with little mining (no corridor or community tenure); joint test that "
                       "the 2011–13 leads are zero. With the 2010 lead added (the v2 window) the test gives p = "
                       f"{float(ev10['lapampa']['net']['pvalue']):.3f} for La Pampa and "
                       f"{float(ev10['corridor_across']['net']['pvalue']):.3f} across the road. Description.",
                  OUT / "fig_v2_stats_event.png", event_note=True)


def _assert_parts(co):
    for t in co["net"].index:
        s = co["new"][t] + co["remined"][t] - co["stopped"][t]
        assert abs(co["net"][t] - s) < 0.01, f"parts do not add up for {t}: {co['net'][t]} vs {s}"


def depletion(d, reg):
    """S4 (review D-S8-3): hazard = new land / land not yet mined at t-1. New land only (an absorbing outcome)."""
    rows = []
    dm, _ = did_sample(d)
    for z in list(FOCAL) + ["reference"]:
        s = dm[dm.focal == z]
        hz = {p: 100 * s[s.year.between(*D.PERIODS[p])].new_ha.sum() / s[s.year.between(*D.PERIODS[p])].at_risk.sum()
              for p in ("pre_long", "during", "later")}
        rows.append(dict(zone=z, **hz, ratio_during=hz["during"] / hz["pre_long"]))
        nm = FOCAL.get(z, "comparison cells")
        for p, v in hz.items():
            reg.add(f"st_hazard_{z}_{p}", v, "% per year", f"Zone-level hazard: new land (first-time mining) as % of the "
                    f"land not yet mined at the end of the year before, {nm} cells, {D.period_label(p)} (sum / sum)",
                    "description", SRC, measure="new", zone=z, period=D.period_label(p))
        reg.add(f"st_hazard_{z}_ratio_during", hz["during"] / hz["pre_long"], "ratio",
                f"Zone-level hazard 2019–21 divided by 2014–18, {nm} cells (new land)", "description", SRC,
                measure="new", zone=z, period="2019–21 vs 2014–18")
    pd.DataFrame(rows).round(4).to_csv(OUT / "v2_stats_hazard_zones.csv", index=False)
    # La Pampa cells by how used-up they were in 2018 (none / terciles of cells with some mining by 2018)
    lp = dm[dm.focal == "lapampa"].copy()
    cells = lp.drop_duplicates("cell").set_index("cell").share18
    cut = np.quantile(cells[cells > 0], [1 / 3, 2 / 3])
    q = pd.Series(np.select([cells <= 0, cells <= cut[0], cells <= cut[1]], ["none", "low", "mid"], "high"),
                  index=cells.index)
    lp["tq"] = lp.cell.map(q)
    trows = []
    for k in ("none", "low", "mid", "high"):
        s = lp[lp.tq == k]
        rec = dict(tercile=k, cells=s.cell.nunique(), share18=cells[q == k].mean())
        for p in ("pre_long", "during", "later"):
            ss = s[s.year.between(*D.PERIODS[p])]
            for m in MEAS:
                rec[f"{m}_{p}"] = ss[D.COLS[m]].mean()
            rec[f"hazard_{p}"] = 100 * ss.new_ha.sum() / ss.at_risk.sum()
        trows.append(rec)
        lab = f"La Pampa cells, 2018 depletion group '{k}' (none mined by 2018, or tercile of cells with some mining)"
        reg.add(f"st_lp_tq_{k}_cells", rec["cells"], "count", f"Cells in {lab}", "description", SRC)
        reg.add(f"st_lp_tq_{k}_share18", rec["share18"], "share", f"Mean share of cell area mapped as mining by 2018, {lab}",
                "description", SRC, measure="stock", zone="lapampa", period="2018")
        for p in ("pre_long", "during"):
            Z.register_parts(reg, f"st_lp_tq_{k}_{p}", {m: rec[f"{m}_{p}"] for m in MEAS}, "lapampa",
                             D.period_label(p), f"mean per cell-year, {lab}", source=SRC, value_unit="ha/cell-yr")
            reg.add(f"st_lp_tq_{k}_hazard_{p}", rec[f"hazard_{p}"], "% per year", f"Hazard (new land / land not yet "
                    f"mined), {lab}, {D.period_label(p)}", "description", SRC, measure="new", zone="lapampa",
                    period=D.period_label(p))
    pd.DataFrame(trows).round(4).to_csv(OUT / "v2_stats_lapampa_terciles.csv", index=False)
    # cell-level hazard OLS (unweighted) and new land with 2018-depletion bin x year FE
    fh = zone_did(d, "hazard_pct")
    dd = d.copy()
    dd["dep_bin"] = pd.cut(dd.share18, [-0.001, 0, 0.05, 0.2, 1.0], labels=["0", "0-5%", "5-20%", ">20%"]).astype(str)
    fb = {m: zone_did(dd, D.COLS[m], fe_extra=" + dep_bin^year") for m in MEAS}
    _assert_parts({m: f.coef() for m, f in fb.items()})
    for z in ("lapampa", "corridor_across"):
        t = f"{z}_during"
        reg.add(f"st_hazard_ols_{t}", fh.coef()[t], "% points per year", f"Cell hazard OLS (new land / unmined land, "
                f"%), {FOCAL[z]} 2019–21 vs 2014–18, cell + year FE, comparison cells", "description", SRC,
                measure="new", zone=z, period="2019–21 vs 2014–18")
        reg.add(f"st_hazard_ols_{t}_p", fh.pvalue()[t], "p-value", f"p-value (CRV1, 10-km blocks) of st_hazard_ols_{t}",
                "description", SRC)
        Z.register_parts(reg, f"st_depbin_{t}", {m: fb[m].coef()[t] for m in MEAS}, z, "2019–21 vs 2014–18",
                         "cell DiD with 2018-depletion bin x year fixed effects, ha per cell-year", source=SRC,
                         value_unit="ha/cell-yr")
        reg.add(f"st_depbin_{t}_net_p", fb["net"].pvalue()[t], "p-value", f"p-value (CRV1) of st_depbin_{t}_net",
                "description", SRC)
    n_ref_dep = dm[(dm.focal == "reference") & (dm.share18 > 0)].cell.nunique()
    reg.add("st_n_ref_cells_depleted18", n_ref_dep, "count", "Comparison cells with any mining by 2018 (the depletion-bin "
            "control rests on these)", "description", SRC)
    return pd.DataFrame(rows), pd.DataFrame(trows)


def run(reg):
    print("\n== cell panel (v3: net additions, registry zones) ==")
    if not (rz.OUT_CELL.exists() and GOLD.exists()):
        warnings.warn("v2_stats: inputs missing (cell_year.csv.gz / cell_gold.csv); skipping"); return
    d = panel()
    print(f"panel: {d.cell.nunique():,} cells x {d.year.nunique()} years, {d.block.nunique()} clusters")
    main = {m: zone_did(d, D.COLS[m]) for m in MEAS}
    _assert_parts({m: f.coef() for m, f in main.items()})
    contam = {m: zone_did(d, D.COLS[m], clean=False) for m in MEAS}
    _assert_parts({m: f.coef() for m, f in contam.items()})
    gold = zone_did(d, "net_ha", gold=True)
    ppml = zone_did(d, "new_ha", poisson=True)
    t = pd.concat([*(tidy_coef(f, "S1 main", m) for m, f in main.items()),
                   *(tidy_coef(f, "S1 all other cells", m) for m, f in contam.items()),
                   tidy_coef(gold, "S1 + gold-bearing bin x year FE", "net"),
                   tidy_coef(ppml, "S1 Poisson (PPML), new land only", "new")])
    ev = {z: {m: event(d, z, D.COLS[m]) for m in MEAS} for z in ("lapampa", "corridor_across")}
    d10 = panel(y0=2010)
    ev10 = {z: {m: event(d10, z, D.COLS[m], y0=2010)[1] for m in ("net", "new")} for z in ("lapampa", "corridor_across")}
    fig_event(ev, ev10)
    grad = {m: gradient(d, D.COLS[m]) for m in MEAS}
    _assert_parts({m: f.coef() for m, f in grad.items()})
    t = pd.concat([t, *(tidy_coef(f, "S3 road gradient", m) for m, f in grad.items())])
    t.round(4).to_csv(OUT / "v2_stats_coefficients.csv", index=False)
    print(t[(t.spec == "S1 main") & (t.measure == "net")].round(3).to_string(index=False))
    fig_zone(main)
    dm, rhs = did_sample(d)
    reg.add("st_n_cells", d.cell.nunique(), "count", "1-km cells in the statistical panel", "description", SRC)
    reg.add("st_n_clusters", d.block.nunique(), "count", "10-km clusters", "description", SRC)
    reg.add("st_n_ref_cells_clean", dm[dm.focal == "reference"].cell.nunique(), "count",
            "Comparison cells (other protected areas, other buffer zones, rest of Madre de Dios; tenure none)",
            "description", SRC)
    for z in ("lapampa", "corridor_across"):
        reg.add(f"st_clusters_{z}", dm[dm.focal == z].block.nunique(), "count", f"10-km clusters containing {FOCAL[z]} "
                "cells", "description", SRC)
    vu = "ha/cell-yr"
    against = {"main": "against comparison cells with little mining", "allcells": "against all other cells (incl. the "
               "corridor and communities)"}
    for tag, fits in (("main", main), ("allcells", contam)):
        for term in fits["net"].coef().index:
            z, p = term.rsplit("_", 1)
            Z.register_parts(reg, f"st_{tag}_{term}", {m: fits[m].coef()[term] for m in MEAS}, z,
                             f"{D.period_label(p)} vs 2014–18", f"cell DiD coefficient, ha per cell-year, {against[tag]}",
                             source=SRC, value_unit=vu)
            reg.add(f"st_{tag}_{term}_net_p", fits["net"].pvalue()[term], "p-value", f"p-value (CRV1, 10-km blocks) of "
                    f"st_{tag}_{term}_net", "description", SRC)
    for term in ("lapampa_during", "corridor_across_during"):
        z = term.rsplit("_", 1)[0]
        reg.add(f"st_gold_{term}_net", gold.coef()[term], vu, f"Net additions, {FOCAL[z]}, 2019–21 vs 2014–18: cell DiD "
                "with gold-bearing bin x year fixed effects", "description", SRC, measure="net", zone=z,
                period="2019–21 vs 2014–18")
        reg.add(f"st_gold_{term}_net_p", gold.pvalue()[term], "p-value", f"p-value of st_gold_{term}_net", "description", SRC)
        reg.add(f"st_ppml_{term}_new", ppml.coef()[term], "log points", f"New land (first-time mining), {FOCAL[z]}, "
                "2019–21 vs 2014–18: Poisson (PPML) cell DiD, log points (non-linear: no net version, net can be "
                "negative)", "description", SRC, measure="new", zone=z, period="2019–21 vs 2014–18")
        reg.add(f"st_ppml_{term}_new_p", ppml.pvalue()[term], "p-value", f"p-value of st_ppml_{term}_new", "description", SRC)
    # wild cluster bootstrap (net), cache keyed by a hash of the inputs
    import hashlib
    REPS, SEED = 999, 1
    cols = ["cell", "year", "block", "net_ha"] + rhs
    h = hashlib.sha256(pd.util.hash_pandas_object(dm[cols].sort_values(["cell", "year"]), index=False).values.tobytes()
                       + f"|{REPS}|{SEED}|net".encode()).hexdigest()[:16]
    c_ = pd.read_csv(WCB_CACHE) if WCB_CACHE.exists() else None
    if c_ is not None and "input_hash" in c_ and (c_.input_hash.astype(str) == h).all():
        wcb = c_.set_index("term").p
    else:
        print("wild cluster bootstrap: inputs changed or no cache, recomputing")
        wcb = pd.Series({term: wild_cluster_bootstrap(dm, "net_ha", rhs, term, "block", reps=REPS, seed=SEED)
                         for term in ("lapampa_during", "corridor_across_during")})
        pd.DataFrame({"term": wcb.index, "p": wcb.values, "input_hash": h}).to_csv(WCB_CACHE, index=False)
    for term in wcb.index:
        reg.add(f"st_wcb_{term}_net_p", float(wcb[term]), "p-value", f"Wild cluster bootstrap p-value (WCR, {REPS} "
                f"Rademacher draws, 10-km blocks, after removing cell and year effects), st_main_{term}_net",
                "description", SRC)
    for z, e in ev.items():
        t_, w = e["net"]
        reg.add(f"st_event_{z}_pretrend_net_p", float(w["pvalue"]), "p-value", f"Joint test that the 2011-13 leads are "
                f"zero (2014-18 pooled reference), net additions, {FOCAL[z]}", "description", SRC)
        reg.add(f"st_event_{z}_pretrend_new_p", float(e["new"][1]["pvalue"]), "p-value", f"Same joint test for new land "
                f"(first-time mining), {FOCAL[z]}", "description", SRC)
        for m in ("net", "new"):
            reg.add(f"st_event_{z}_pretrend2010_{m}_p", float(ev10[z][m]["pvalue"]), "p-value", f"Sensitivity: the "
                    f"same joint test with leads 2010-13 (panel from 2010, the v2 window), {D.MEASURE_NAME[m].lower()}, "
                    f"{FOCAL[z]}. The 2010 lead decides the test for La Pampa", "description", SRC)
        for y in (2012, 2019, 2020, 2021, 2023):
            Z.register_parts(reg, f"st_event_{z}_{y}", {m: e[m][0].loc[y, "Estimate"] for m in MEAS}, z,
                             f"{y} vs 2014–18", "event-study coefficient per cell, pooled 2014–18 reference",
                             source=SRC, value_unit=vu)
            reg.add(f"st_event_{z}_{y}_net_p", t_.loc[y, "Pr(>|t|)"], "p-value", f"p-value of st_event_{z}_{y}_net",
                    "description", SRC)
    ls = "La Pampa longitudes (definitions.LP_LON), all cells, ref: south 10-30 km"
    for term in grad["net"].coef().index:
        b_, p = term.rsplit("_", 1)
        Z.register_parts(reg, f"st_grad_{term}", {m: grad[m].coef()[term] for m in MEAS}, f"road band {b_[2:]}",
                         f"{D.period_label(p)} vs 2014–18", f"road gradient coefficient per cell, {ls}", source=SRC,
                         value_unit=vu)
        reg.add(f"st_grad_{term}_net_p", grad["net"].pvalue()[term], "p-value", f"p-value of st_grad_{term}_net",
                "description", SRC)
    hz, tq = depletion(d, reg)
    print(hz.round(3).to_string(index=False)); print(tq.round(2).to_string(index=False))
    return t
