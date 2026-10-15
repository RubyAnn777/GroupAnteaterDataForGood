"""Matching estimators for Tambopata's 2019-21 counterfactual: propensity score, Mahalanobis, coarsened exact
matching (CEM), entropy balancing and inverse-probability weighting, beside the rule-based twin (control_select.py).

WHY: the rule-based twin uses hand-set cut-offs (500 ha, 500 m, 1/5 size). Matching asks the same question with
standard estimators: which areas looked like Tambopata before 2019 but had no operation during Mercurio's years?

UNITS: the Amazon areas with Amazon Mining Watch (AMW) mining data (amw_candidates_*.csv, the 108 areas of the
1,174 screened that had any AMW mining). Treated = Tambopata buffer zone (PE-BZ-RN09).
COVARIATES (all 2018 or time-invariant, so they cannot be moved by Mercurio): log AMW mining stock 2018,
log median elevation of the mining, log area, Brazil, indigenous territory. Distance to La Pampa is NOT a covariate.
CONTROL POOL: no operation reported 2017-21 (verdict "none", or first operation 2022 or later; = rule R2b),
AMW stock 2018 >= MIN_STOCK, outside Madre de Dios (R3). Variants: without R3; with "unclear / not searched" areas
counted as no-operation.
PROPENSITY SCORE: logit of P(operation reported 2017-21) on the covariates, fitted on the areas whose operation
status we coded (operations_coded.csv), Tambopata included as treated. Small n: a light ridge penalty (L2_PS) keeps
the fit finite.
OUTCOME (same as the twin): AMW new mining per year as % of the area's own 2018 stock; 2019-21 mean and 2022-25 mean
(2025 provisional). Gap = Tambopata minus the matched controls (percentage points); ratio = Tambopata's pace as a
share of the controls' pace (the twin: 38%).
INFERENCE: placebo in space. Each control area in turn plays "treated" (Tambopata removed), the same estimator picks
its matches from the rest of the pool; Tambopata's rank among all gaps (1 = biggest slowdown) gives p = rank / n.

HONEST LIMIT: there is ONE treated area. With one treated unit a propensity score is just a one-dimensional distance:
"PS matching" = picking the controls whose predicted chance of an operation is closest to Tambopata's. It does not
balance anything in expectation. Entropy balancing and Mahalanobis matching say the same thing more directly.
All results are DESCRIPTION.
"""
from __future__ import annotations
import warnings

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import minimize

from common import ROOT, OUT, style_axes, finish_figure, headline, C, INK, INK2, MUTED, GRID, AXIS, placebo_rank

INTER = ROOT / "data_intermediate"
TU = "PE-BZ-RN09"
MDD_BOX = (-72.6, -14.6, -68.6, -10.5)                 # same as control_select.py
MIN_STOCK = 100.0                                     # ha of AMW mining by 2018 (a pool needs some mining to compare)
L2_PS = 0.1                                           # ridge penalty for the small-sample logit
CALIPER_SD = 0.25                                     # caliper: 0.25 SD of the logit propensity score in the pool
COVS = ["ln_stock", "ln_elev", "ln_area", "brazil", "indigenous"]
# Entropy balancing cannot match "not Brazil" AND Tambopata's stock at once (the non-Brazilian pool areas are all
# far smaller), so it balances the four other covariates; psm_ebal_imbalance_all_covs reports the failure.
EBAL_COVS = ["ln_stock", "ln_elev", "ln_area", "indigenous"]
EBAL_RIDGE = 1e-4
COV_LABEL = {"ln_stock": "log mining stock 2018", "ln_elev": "log elevation of mining", "ln_area": "log area",
             "brazil": "Brazil", "indigenous": "indigenous territory"}
DURING, AFTER = list(range(2019, 2022)), list(range(2022, 2026))
SRC = ("Amazon Mining Watch (AMW) x SERNANP / RAISG / FUNAI polygons; SRTM elevation (OpenTopoData); "
       "operations: data_intermediate/operations_coded.csv")


# --------------------------------------------------------------------------- data
def load() -> pd.DataFrame:
    u = pd.read_csv(INTER / "amw_candidates_units.csv").set_index("unit_id")
    w = pd.read_csv(INTER / "amw_candidates_year.csv").pivot(index="unit_id", columns="year", values="new_ha")
    e = pd.read_csv(INTER / "amw_candidates_elevation.csv").set_index("unit_id")
    ops = pd.read_csv(INTER / "operations_coded.csv").set_index("unit_id")
    t = u.join(w, how="inner").join(e[["elev_median_m"]], how="inner")
    t = t.rename(columns={2018: "stock_2018"})
    v = ops["verdict_2017_2025"].reindex(t.index).fillna("not searched")
    first = ops["first_op_2017_2025"].reindex(t.index).fillna("")
    t["verdict"] = v
    t["op_2017_21"] = v.isin(["yes", "treated"]) & (first < "2022")           # 2008-01 = ongoing since 2008: counts
    t["no_op_2017_21"] = v.eq("none") | (v.eq("yes") & (first >= "2022"))
    t["status_known"] = v.isin(["yes", "none", "treated"])
    t["in_mdd"] = (t.lon.between(MDD_BOX[0], MDD_BOX[2]) & t.lat.between(MDD_BOX[1], MDD_BOX[3])
                   & t.country.eq("Peru"))
    t["ln_stock"] = np.log1p(t.stock_2018)
    t["ln_elev"] = np.log(t.elev_median_m.clip(lower=20))
    t["ln_area"] = np.log(t.area_km2.clip(lower=0.1))
    t["brazil"] = t.country.eq("Brazil").astype(float)
    t["indigenous"] = t.kind.eq("indigenous territory").astype(float)
    pace = t[DURING + AFTER].div(t.stock_2018.where(t.stock_2018 > 0), axis=0) * 100
    t["pace_during"] = pace[DURING].mean(axis=1)
    t["pace_after"] = pace[AFTER].mean(axis=1)
    return t


def pool(t, r3=True, unknown_as_none=False) -> pd.Index:
    ok = t.no_op_2017_21 | (unknown_as_none & ~t.status_known)
    ok &= t.stock_2018 >= MIN_STOCK
    if r3:
        ok &= ~t.in_mdd
    return t.index[ok & (t.index != TU)]


# --------------------------------------------------------------------------- propensity score
def logit_fit(X: np.ndarray, d: np.ndarray, l2: float = L2_PS):
    """Ridge logit (intercept unpenalized). Returns coefficients and McFadden pseudo-R²."""
    Xc = np.column_stack([np.ones(len(X)), X])
    def nll(b):
        z = Xc @ b
        return np.sum(np.logaddexp(0, z) - d * z) + l2 * np.sum(b[1:] ** 2)
    def grad(b):
        p = 1 / (1 + np.exp(-(Xc @ b)))
        g = Xc.T @ (p - d); g[1:] += 2 * l2 * b[1:]
        return g
    b = minimize(nll, np.zeros(Xc.shape[1]), jac=grad, method="BFGS").x
    z = Xc @ b
    ll = np.sum(d * z - np.logaddexp(0, z))
    p0 = d.mean(); ll0 = len(d) * (p0 * np.log(p0) + (1 - p0) * np.log(1 - p0))
    return b, 1 - ll / ll0


def propensity(t) -> tuple[pd.Series, dict]:
    """Fit on areas with a coded operation status; predict the logit score for every area."""
    s = t[t.status_known]
    mu, sd = s[COVS].mean(), s[COVS].std().replace(0, 1)
    b, r2 = logit_fit(((s[COVS] - mu) / sd).to_numpy(), s.op_2017_21.astype(float).to_numpy())
    z = np.column_stack([np.ones(len(t)), ((t[COVS] - mu) / sd).to_numpy()]) @ b
    info = dict(n=len(s), n_treated=int(s.op_2017_21.sum()), pseudo_r2=r2, coef=dict(zip(["const"] + COVS, b)))
    return pd.Series(z, index=t.index, name="ps_logit"), info


# --------------------------------------------------------------------------- estimators: weights over the pool
def w_nn(score: pd.Series, tr, P, k=1, caliper=None):
    d = (score.loc[P] - score.loc[tr]).abs().sort_values()
    if caliper is not None and d.iloc[0] > caliper:
        return None                                               # no control within the caliper
    sel = d.index[:k] if caliper is None else d.index[:k][d.iloc[:k] <= max(caliper, d.iloc[0])]
    return pd.Series(1 / len(sel), index=sel)


def w_maha(t, tr, P, k=1):
    X = t.loc[P, COVS].to_numpy()
    S = np.cov(X, rowvar=False) + 1e-6 * np.eye(len(COVS))
    diff = X - t.loc[tr, COVS].to_numpy()
    d = pd.Series(np.einsum("ij,jk,ik->i", diff, np.linalg.inv(S), diff), index=P).sort_values()
    return pd.Series(1 / k, index=d.index[:k])


def cem_bins(t, area=False):
    """Coarsened strata: scale (stock >= 1/5 of Tambopata's) x lowland (< 500 m) - the cut-offs of rule R4.
    area=True adds a third bin (area >= 5,000 km²): then no pool area shares Tambopata's stratum."""
    big = t.stock_2018 >= 0.2 * t.loc[TU, "stock_2018"]
    b = big.astype(int).astype(str) + (t.elev_median_m < 500).astype(int).astype(str)
    return b + (t.area_km2 >= 5000).astype(int).astype(str) if area else b


def w_cem(t, tr, P, bins):
    m = P[bins.loc[P] == bins.loc[tr]]
    return pd.Series(1 / len(m), index=m) if len(m) else None


def w_ebal(t, tr, P, covs=None):
    covs = covs or EBAL_COVS
    """Entropy balancing (Hainmueller 2012): weights over the pool, closest to uniform in KL distance, whose
    weighted covariate means equal the treated area's. Dual: minimise log sum exp(λ'(x_i - x_t))."""
    from scipy.special import logsumexp, softmax
    X = t.loc[P, covs].to_numpy() - t.loc[tr, covs].to_numpy()
    sd = t.loc[P, covs].to_numpy().std(axis=0); sd[sd == 0] = 1; Xs = X / sd
    # a tiny ridge on the dual keeps λ finite when exact balance is impossible (placebo areas at the edge of the pool)
    l = minimize(lambda l: logsumexp(Xs @ l) + EBAL_RIDGE * l @ l, np.zeros(len(covs)),
                 jac=lambda l: softmax(Xs @ l) @ Xs + 2 * EBAL_RIDGE * l, method="BFGS", options=dict(maxiter=2000)).x
    ww = softmax(Xs @ l)
    imb = float(np.abs(ww @ Xs).max())                 # largest remaining gap, in pool SDs (0 = exact balance)
    return pd.Series(ww, index=P), imb


def w_ipw(score, tr, P):
    """ATT weights p/(1-p) = exp(logit score) for the controls, normalised. With one treated area this is a
    soft version of propensity matching: controls that 'should' have had an operation count more."""
    ww = np.exp(score.loc[P] - score.loc[P].max())
    return ww / ww.sum()


def weights(method, t, tr, P, score, bins):
    cal = CALIPER_SD * score.loc[P].std()
    if method == "ps_nn1":  return w_nn(score, tr, P, 1)
    if method == "ps_nn5":  return w_nn(score, tr, P, 5)
    if method == "maha1":   return w_maha(t, tr, P, 1)
    if method == "maha3":   return w_maha(t, tr, P, 3)
    if method == "cem":     return w_cem(t, tr, P, bins)
    if method == "ebal":    return w_ebal(t, tr, P)[0]
    if method == "ipw":     return w_ipw(score, tr, P)
    raise KeyError(method)


METHODS = {"ps_nn1": "Propensity score, nearest 1", "ps_nn5": "Propensity score, nearest 5",
           "maha1": "Mahalanobis, nearest 1", "maha3": "Mahalanobis, nearest 3", "cem": "Coarsened exact matching",
           "ebal": "Entropy balancing (closest)", "ipw": "Inverse-probability weighting"}


def estimate(method, t, tr, P, score, bins):
    w = weights(method, t, tr, P, score, bins)
    if w is None or w.sum() == 0:
        return None
    cd, ca = (w * t.loc[w.index, "pace_during"]).sum(), (w * t.loc[w.index, "pace_after"]).sum()
    return dict(ctl_during=cd, ctl_after=ca, gap_during=t.loc[tr, "pace_during"] - cd,
                gap_after=t.loc[tr, "pace_after"] - ca, w=w)


def placebo(method, t, P, score, bins, real_gap, col="gap_during"):
    """Each control as treated (Tambopata not in the pool); rank Tambopata's gap (1 = most negative)."""
    gaps = []
    for j in P:
        r = estimate(method, t, j, P.drop(j), score, bins)
        if r is not None:
            gaps.append(r[col])
    return placebo_rank(real_gap, gaps), len(gaps) + 1, np.array(gaps)


def smd(t, P, w):
    """Standardised mean difference, treated minus (weighted) controls, in pool SDs."""
    sd = t.loc[P, COVS].std().replace(0, 1)
    ctl = (t.loc[w.index, COVS].mul(w, axis=0)).sum()
    return (t.loc[TU, COVS] - ctl) / sd


# --------------------------------------------------------------------------- run
def run(reg):
    print("\n== Matching estimators (PSM, Mahalanobis, CEM, entropy balancing, IPW) ==")
    if not (INTER / "amw_candidates_units.csv").exists():
        warnings.warn("control_psm: intermediates missing; skipping"); return
    t = load()
    score, info = propensity(t)
    bins = cem_bins(t)
    P = pool(t)
    variants = {"main": P, "no_r3": pool(t, r3=False), "unknown_none": pool(t, unknown_as_none=True)}
    tam = t.loc[TU]

    # rule-based twin (control_select.py, relaxed rules) for the comparison row
    import control_select as cs
    u_, w_, e_, o_ = cs.load()
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")             # log(0) for areas without mining, inside control_select
        ft = cs.funnel(u_, w_, e_, o_)
    twin = (ft[ft.pass_strict].index.tolist() or ft[ft.pass_relaxed].index.tolist())[0]

    rows, bal = [], {"before (all pool, unweighted)": smd(t, P, pd.Series(1 / len(P), index=P))}
    rows.append(dict(method="twin", label="Rule-based twin (" + t.loc[twin, "name"].split(" (")[0] + ")",
                     ctl_during=t.loc[twin, "pace_during"], ctl_after=t.loc[twin, "pace_after"],
                     gap_during=tam.pace_during - t.loc[twin, "pace_during"],
                     gap_after=tam.pace_after - t.loc[twin, "pace_after"], n_ctl=1,
                     controls=t.loc[twin, "name"]))
    for m, lab in METHODS.items():
        r = estimate(m, t, TU, P, score, bins)
        if r is None:
            rows.append(dict(method=m, label=lab, n_ctl=0)); continue
        rank, n, g = placebo(m, t, P, score, bins, r["gap_during"])
        rank_a, n_a, _ = placebo(m, t, P, score, bins, r["gap_after"], "gap_after")
        top = r["w"].sort_values(ascending=False)
        rows.append(dict(method=m, label=lab, ctl_during=r["ctl_during"], ctl_after=r["ctl_after"],
                         gap_during=r["gap_during"], gap_after=r["gap_after"], n_ctl=int((r["w"] > 1e-3).sum()),
                         rank=rank, n_placebo=n, p=rank / n, rank_after=rank_a, p_after=rank_a / n_a,
                         plac_lo=g.min(), plac_hi=g.max(), plac_q10=np.quantile(g, 0.1), plac_q90=np.quantile(g, 0.9),
                         controls="; ".join(f"{t.loc[i, 'name'].split(' (')[0]} {v:.0%}" for i, v in top.head(4).items())))
        bal[lab] = smd(t, P, r["w"])
        for vk, VP in variants.items():
            if vk == "main":
                continue
            rv = estimate(m, t, TU, VP, score, bins)
            rows[-1][f"gap_during_{vk}"] = rv["gap_during"] if rv else np.nan
    res = pd.DataFrame(rows)
    res["ratio_during"] = tam.pace_during / res.ctl_during
    res.drop(columns=[c for c in res if c.startswith("w")], errors="ignore").round(3).to_csv(OUT / "psm_results.csv", index=False)
    b = pd.DataFrame(bal).T.rename(columns=COV_LABEL)
    b.round(3).to_csv(OUT / "table_psm_balance.csv")
    _, ebal_imb = w_ebal(t, TU, P)
    _, ebal_imb_all = w_ebal(t, TU, P, COVS)
    cal = CALIPER_SD * score.loc[P].std()
    nn_dist = (score.loc[P] - score.loc[TU]).abs().min()
    n_cem3 = int((cem_bins(t, area=True).loc[P] == cem_bins(t, area=True).loc[TU]).sum())
    supp = int((score.loc[P] >= score.loc[TU]).sum())
    print(f"PS logit: n = {info['n']} ({info['n_treated']} with operation), pseudo-R² = {info['pseudo_r2']:.2f}")
    print(res.drop(columns=["controls"]).round(2).to_string(index=False))
    print(b.round(2).to_string())

    # ---- numbers
    reg.add("psm_n_units", len(t), "count", "Amazon areas with AMW mining data and elevation (matching universe)", "description", SRC)
    reg.add("psm_n_pool", len(P), "count", f"Control pool: no operation reported 2017-21, AMW stock 2018 >= {MIN_STOCK:.0f} ha, outside Madre de Dios", "description", SRC)
    reg.add("psm_n_pool_unknown_none", len(variants["unknown_none"]), "count", "Control pool if areas with unclear / unsearched operation status count as no-operation", "description", SRC)
    reg.add("psm_n_pool_no_r3", len(variants["no_r3"]), "count", "Control pool without the outside-Madre-de-Dios rule", "description", SRC)
    reg.add("psm_ps_n", info["n"], "count", "Areas with coded operation status used to fit the propensity-score logit", "description", SRC)
    reg.add("psm_ps_n_treated", info["n_treated"], "count", "... of which with an operation reported 2017-21 (incl. Tambopata)", "description", SRC)
    reg.add("psm_ps_pseudo_r2", info["pseudo_r2"], "pseudo-R2", "McFadden pseudo-R2 of the propensity logit (ridge-penalised)", "description", SRC)
    reg.add("psm_ps_tam", 1 / (1 + np.exp(-score.loc[TU])), "probability", "Tambopata's predicted probability of an operation 2017-21", "description", SRC)
    reg.add("psm_ps_pool_max", 1 / (1 + np.exp(-score.loc[P].max())), "probability", "Highest predicted probability of an operation in the control pool", "description", SRC)
    reg.add("psm_tam_pace_during", tam.pace_during, "% of 2018 stock per yr", "Tambopata 2019-21 AMW new mining per year, % of own 2018 stock", "description", SRC)
    reg.add("psm_tam_pace_after", tam.pace_after, "% of 2018 stock per yr", "Tambopata 2022-25 AMW new mining per year, % of own 2018 stock (2025 provisional)", "description", SRC)
    reg.add("psm_ebal_max_imbalance", ebal_imb, "pool SD", "Entropy balancing (stock, elevation, area, indigenous): largest remaining covariate gap after weighting (0 = exact balance)", "description", SRC)
    reg.add("psm_ebal_imbalance_all_covs", ebal_imb_all, "pool SD", "Entropy balancing with the Brazil dummy too: largest remaining gap (> 0 = exact balance impossible)", "description", SRC)
    reg.add("psm_ps_nn1_within_caliper", float(nn_dist <= cal), "0/1", f"1 if the nearest control lies within {CALIPER_SD} SD of the logit propensity score (common support)", "description", SRC)
    reg.add("psm_ps_n_above_tam", supp, "count", "Pool areas with a propensity score at least Tambopata's (0 = Tambopata outside common support)", "description", SRC)
    reg.add("psm_cem3_n_matches", n_cem3, "count", "Coarsened exact matching with a third bin (area >= 5,000 km²): pool areas in Tambopata's stratum", "description", SRC)
    one = " ONE treated area: matching picks the closest controls, it does not balance anything in expectation. Description."
    for r in res.to_dict("records"):
        m = r["method"]
        if not r.get("n_ctl"):
            reg.add(f"psm_{m}_n_ctl", 0, "count", f"{r['label']}: no control found", "description", SRC); continue
        reg.add(f"psm_{m}_ctl_during", r["ctl_during"], "% of 2018 stock per yr", f"{r['label']}: matched controls' 2019-21 pace." + one, "description", SRC)
        reg.add(f"psm_{m}_gap_during", r["gap_during"], "pp", f"{r['label']}: Tambopata minus matched controls, 2019-21 pace." + one, "description", SRC)
        reg.add(f"psm_{m}_gap_after", r["gap_after"], "pp", f"{r['label']}: Tambopata minus matched controls, 2022-25 pace." + one, "description", SRC)
        reg.add(f"psm_{m}_ratio_during", r["ratio_during"], "ratio", f"{r['label']}: Tambopata's 2019-21 pace as a share of the matched controls'", "description", SRC)
        reg.add(f"psm_{m}_n_ctl", r["n_ctl"], "count", f"{r['label']}: controls with weight > 0.1%", "description", SRC)
        if m == "twin":
            continue
        reg.add(f"psm_{m}_rank", r["rank"], "rank", f"{r['label']}: Tambopata's rank among placebo gaps 2019-21 (1 = biggest slowdown)", "description", SRC)
        reg.add(f"psm_{m}_n_placebo", r["n_placebo"], "count", f"{r['label']}: areas in the placebo ranking (pool + Tambopata)", "description", SRC)
        reg.add(f"psm_{m}_p", r["p"], "p-value", f"{r['label']}: placebo-in-space p = rank / n, 2019-21", "description", SRC)
        reg.add(f"psm_{m}_p_after", r["p_after"], "p-value", f"{r['label']}: placebo-in-space p, 2022-25 gap", "description", SRC)
        for vk in ("no_r3", "unknown_none"):
            reg.add(f"psm_{m}_gap_during_{vk}", r.get(f"gap_during_{vk}", np.nan), "pp",
                    f"{r['label']}: 2019-21 gap with pool variant {vk}", "description", SRC)
    ok = res[res.method != "twin"].dropna(subset=["gap_during"])
    reg.add("psm_n_methods", len(ok), "count", "Matching estimators with a result", "description", SRC)
    reg.add("psm_n_methods_negative", int((ok.gap_during < 0).sum()), "count", "... of which show Tambopata slower than its matches in 2019-21", "description", SRC)
    reg.add("psm_n_methods_p10", int((ok.p <= 0.10).sum()), "count", "... of which with placebo p <= 0.10", "description", SRC)
    reg.add("psm_gap_during_min", ok.gap_during.min(), "pp", "Smallest (most negative) 2019-21 gap across matching estimators", "description", SRC)
    reg.add("psm_gap_during_max", ok.gap_during.max(), "pp", "Largest 2019-21 gap across matching estimators", "description", SRC)
    reg.add("psm_ratio_min", ok.ratio_during.min(), "ratio", "Lowest Tambopata/controls pace ratio across matching estimators", "description", SRC)
    reg.add("psm_ratio_max", ok.ratio_during.max(), "ratio", "Highest Tambopata/controls pace ratio across matching estimators", "description", SRC)
    reg.add("psm_p_min", ok.p.min(), "p-value", "Smallest placebo p across matching estimators", "description", SRC)
    reg.add("psm_p_max", ok.p.max(), "p-value", "Largest placebo p across matching estimators", "description", SRC)
    _figure(res, tam, reg.get("psm_p_min"), reg.get("psm_p_max"))
    return res


def _figure(res, tam, p_min, p_max):
    r = res.dropna(subset=["gap_during"]).reset_index(drop=True)
    est = r[r.method != "twin"]
    neg, n = int((est.gap_during < 0).sum()), len(est)
    sig = int((est.p <= 0.10).sum())
    title = ("All matches mined faster than Tambopata in 2019–21" if neg == n else
             f"{neg} of {n} matches mined faster than Tambopata in 2019–21")
    title += (f"; the gap is not unusual (placebo p {p_min:.2f}–{p_max:.2f})" if sig == 0
              else f"; {sig} of {n} pass the placebo test (p {p_min:.2f}–{p_max:.2f})")
    fig = plt.figure(figsize=(9, 4.9))
    # explicit axes: row labels on the left and rank notes on the right need fixed room (tight_layout ignores them)
    a1 = fig.add_axes([0.255, 0.2, 0.33, 0.6]); a2 = fig.add_axes([0.61, 0.2, 0.24, 0.6], sharey=a1)
    headline(fig, title, "New mining per year 2019–21, % of each area’s own 2018 mining (Amazon Mining Watch). "
             "Each row is one way to pick\nthe comparison areas from places with no operation in 2017–21.")
    y = np.arange(len(r))[::-1]
    # left: paces
    a1.axvline(tam.pace_during, color=C["lapampa"], lw=2, zorder=2)
    a1.annotate(f"Tambopata {tam.pace_during:.0f}%", (tam.pace_during, y.max() + 0.75), xytext=(4, 0),
                textcoords="offset points", fontsize=8.5, color=INK, fontweight="semibold", va="center",
                annotation_clip=False)
    for yy, (_, row) in zip(y, r.iterrows()):
        a1.plot([tam.pace_during, row.ctl_during], [yy, yy], color=GRID, lw=2, zorder=1)
        a1.plot(row.ctl_during, yy, "o", ms=8, color=C["twin"], mec="white", mew=1.2, zorder=3)
        a1.annotate(f"{row.ctl_during:.0f}%", (row.ctl_during, yy), xytext=(7, 0), textcoords="offset points",
                    va="center", fontsize=8, color=INK2)
    style_axes(a1, ygrid=False, fmt=False); a1.xaxis.grid(True, color=GRID, lw=0.6)
    a1.set_yticks(y); a1.set_yticklabels(r.label, fontsize=8.5, color=INK)
    a1.set_xlim(0, max(r.ctl_during.max(), tam.pace_during) * 1.25)
    a1.set_ylim(-0.7, y.max() + 1.3)
    a1.set_title("Pace: Tambopata vs matched areas", fontsize=9.5)
    a1.set_xlabel("% of own 2018 mining per year")
    a1.get_yticklabels()[0].set_fontweight("semibold")
    # right: gaps vs placebo ranges
    a2.axvline(0, color=INK2, lw=0.8)
    for yy, (_, row) in zip(y, r.iterrows()):
        if row.method != "twin":
            a2.plot([row.plac_lo, row.plac_hi], [yy, yy], color=GRID, lw=6, solid_capstyle="butt", zorder=1)
            a2.plot([row.plac_q10, row.plac_q90], [yy, yy], color=AXIS, lw=6, solid_capstyle="butt", zorder=1)
        a2.plot(row.gap_during, yy, "o", ms=8, color=C["lapampa"], mec="white", mew=1.2, zorder=3)
        txt = "no placebo" if row.method == "twin" else f"rank {int(row['rank'])}/{int(row.n_placebo)}, p = {row.p:.2f}"
        a2.annotate(txt, (1.0, yy), xycoords=("axes fraction", "data"), xytext=(6, 0), textcoords="offset points",
                    ha="left", va="center", fontsize=7.5, color=INK2, annotation_clip=False)
    lo = min(r.gap_during.min(), est.plac_q10.min()); hi = max(r.gap_during.max(), est.plac_q90.max())
    a2.set_xlim(lo - 0.25 * (hi - lo), hi + 0.25 * (hi - lo))       # full placebo ranges run off the edge
    style_axes(a2, ygrid=False, fmt=False); a2.xaxis.grid(True, color=GRID, lw=0.6)
    a2.xaxis.set_major_formatter(plt.FuncFormatter(lambda v, p: f"{v:+.0f}".replace("-", "−") if v else "0"))
    a2.set_title("Gap vs fake ‘treated’ areas", fontsize=9.5)
    a2.set_xlabel("Tambopata minus matches, percentage points")
    a2.tick_params(axis="y", length=0, labelleft=False)
    finish_figure(fig, f"{SRC}. Grey bars: gaps when each pool area plays ‘treated’ (light = full range, darker = "
                       "10th–90th percentile; the full range runs past the axis). One treated area: matching picks the closest areas; it does not balance "
                       "anything in expectation. Description.", OUT / "fig_psm.png")
