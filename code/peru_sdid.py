"""Synthetic difference-in-differences (Arkhangelsky, Athey, Hirshberg, Imbens & Wager 2021, AER) for Tambopata.

WHY: plain DiD (model M1) weighs all 14 other buffer zones equally; the synthetic twin (peru_synth.py) must copy
Tambopata's LEVEL, which no mix of smaller zones can. SDID sits between the two: unit weights make the comparison
zones' pre-2019 TREND (not level) match Tambopata's, a free intercept absorbs the level gap, and time weights pick
the pre-years that best predict the post-period for the comparison zones.

PANEL: the same as peru_models.py: 15 Peruvian buffer zones with mining additions in 2014-18 (MapBiomas Peru
Collection 4, pack table), outcome = annual addition to mining area. Pre = 2014-2018 (same window as M1, so SDID's
"uniform weights" special case equals M1 exactly; asserted). Each post block is estimated on its own:
2019-21 ("during") and 2022-25 ("after"). Scaled version = M4: outcome / own 2014-18 mean addition, zones with
mean > 10 ha/yr. Sensitivity: pre = 2011-2018.
ESTIMATOR (own implementation, paper Algorithm 1):
  zeta = (N_tr * T_post)^(1/4) * sd(first differences of control outcomes, pre-period)
  unit weights:  min_{w0, w>=0, sum w=1}  sum_t<=T0 (w0 + sum_i w_i Y_it - Y_tr,t)^2 + zeta^2 * T0 * ||w||^2
  time weights:  min_{l0, l>=0, sum l=1}  sum_i (l0 + sum_t l_t Y_it - mean_post Y_i)^2 + (1e-6 sd)^2 * N0 * ||l||^2
  tau = [mean_post Y_tr - sum_t l_t Y_tr,t] - sum_i w_i [mean_post Y_i - sum_t l_t Y_it]
DiD = uniform unit and time weights; SC = unit weights without intercept or penalty and no time weights (paper eq. 2).
INFERENCE: placebo in space (paper's "placebo variance" for one treated unit): each control zone plays treated,
Tambopata removed; rank Tambopata (1 = biggest fall); p = rank / n; placebo SE = sd of the placebo estimates.
All results are DESCRIPTION (one treated zone).
"""
from __future__ import annotations
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import minimize

from common import OUT, style_axes, finish_figure, headline, label_end, period_band, SRC_MAPBIOMAS, C, INK, INK2, GRID, AXIS, MUTED
from peru_models import _zone_adds, fit as m_fit, TU

SRC = "peru_bufferzone_year.csv (MapBiomas Peru Collection 4)"
PRE = (2014, 2018)
POSTS = {"during": (2019, 2021), "after": (2022, 2025)}


def _proj_simplex(v):
    """Euclidean projection onto the probability simplex (Duchi et al. 2008)."""
    u = np.sort(v)[::-1]; css = np.cumsum(u)
    k = np.nonzero(u * np.arange(1, len(v) + 1) > (css - 1))[0][-1]
    return np.maximum(v - (css[k] - 1) / (k + 1), 0)


def _simplex_ls(A, b, pen, intercept=True, iters=20000, tol=1e-12):
    """min_{c, w in simplex} ||c + A w - b||^2 + pen * ||w||^2 (c free if intercept). A: rows x weights.
    Accelerated projected gradient (FISTA); the problem is convex, so this reaches the global minimum."""
    n = A.shape[1]
    if intercept:                                            # the free intercept = demean rows over the fit dimension
        A = A - A.mean(axis=0); b = b - b.mean()
    L = 2 * (np.linalg.norm(A, 2) ** 2 + pen)
    w = z = np.full(n, 1 / n); tk = 1.0
    for _ in range(iters):
        w_new = _proj_simplex(z - (2 * A.T @ (A @ z - b) + 2 * pen * z) / L)
        t_new = (1 + np.sqrt(1 + 4 * tk ** 2)) / 2
        z = w_new + (tk - 1) / t_new * (w_new - w)
        if np.abs(w_new - w).max() < tol:
            w = w_new; break
        w, tk = w_new, t_new
    return w


def sdid(Y: pd.DataFrame, treated: str, pre, post, method="sdid"):
    """Y: years x units. Returns tau and the weights."""
    pre_y = list(range(pre[0], pre[1] + 1)); post_y = list(range(post[0], post[1] + 1))
    co = [u for u in Y.columns if u != treated]
    Yc_pre, Yc_post = Y.loc[pre_y, co].to_numpy(), Y.loc[post_y, co].to_numpy()
    yt_pre, yt_post = Y.loc[pre_y, treated].to_numpy(), Y.loc[post_y, treated].to_numpy()
    N0, T0 = len(co), len(pre_y)
    if method == "did":
        w, lam = np.full(N0, 1 / N0), np.full(T0, 1 / T0)
    elif method == "sc":
        w, lam = _simplex_ls(Yc_pre, yt_pre, 0.0, intercept=False), np.zeros(T0)
    else:
        sigma = np.std(np.diff(Yc_pre, axis=0), ddof=1)
        zeta = (1 * len(post_y)) ** 0.25 * sigma
        w = _simplex_ls(Yc_pre, yt_pre, zeta ** 2 * T0)                     # rows = pre years, cols = control units
        lam = _simplex_ls(Yc_pre.T, Yc_post.mean(axis=0), (1e-6 * sigma) ** 2 * N0)   # rows = units, cols = pre years
    tau = (yt_post.mean() - lam @ yt_pre) - (w @ Yc_post.mean(axis=0) - w @ (Yc_pre.T @ lam))
    return dict(tau=float(tau), w=pd.Series(w, index=co), lam=pd.Series(lam, index=pre_y))


def placebo(Y, method, pre, post, real):
    others = [u for u in Y.columns if u != TU]
    Yp = Y[others]
    est = np.array([sdid(Yp, u, pre, post, method)["tau"] for u in others])
    allv = np.append(est, real)
    return int((allv <= real).sum()), len(allv), est


def run(pack, reg):
    print("\n== Synthetic difference-in-differences (SDID) ==")
    ad = _zone_adds(pack)
    pre_mean = ad.loc[2014:2018].mean()
    poolB = sorted(u for u in ad.columns if ad.loc[2014:2018, u].abs().sum() > 0)
    pool_big = sorted(u for u in poolB if pre_mean[u] > 10)
    assert len(poolB) == 15 and TU in pool_big
    gold = pack["prices"].set_index("year")["gold"]
    panels = {"ha": ad[poolB], "scaled": ad[pool_big] / pre_mean[pool_big]}
    # check: uniform weights = model M1 / M4 on the same years
    for k, P in panels.items():
        did = sdid(P, TU, PRE, POSTS["during"], "did")["tau"]
        m = m_fit(ad, poolB if k == "ha" else pool_big, TU, "M1" if k == "ha" else "M4", 2014, 2021,
                  {"during": POSTS["during"]}, gold)["post_during"]
        assert np.isclose(did, m, atol=1e-6), f"SDID-DiD != peru_models ({k}): {did} vs {m}"
    rows, keep = [], {}
    for k, P in panels.items():
        for per, post in POSTS.items():
            for meth in ("did", "sc", "sdid"):
                r = sdid(P, TU, PRE, post, meth)
                rank, n, est = placebo(P, meth, PRE, post, r["tau"])
                rows.append(dict(scale=k, period=per, method=meth, tau=r["tau"], rank=rank, n=n, p=rank / n,
                                 placebo_se=est.std(ddof=1), placebo_min=est.min(), placebo_max=est.max()))
                keep[(k, per, meth)] = (r, est)
    # sensitivity: longer pre-period
    for k, P in panels.items():
        r = sdid(P, TU, (2011, 2018), POSTS["during"], "sdid")
        rank, n, est = placebo(P, "sdid", (2011, 2018), POSTS["during"], r["tau"])
        rows.append(dict(scale=k, period="during_pre2011", method="sdid", tau=r["tau"], rank=rank, n=n, p=rank / n,
                         placebo_se=est.std(ddof=1), placebo_min=est.min(), placebo_max=est.max()))
    res = pd.DataFrame(rows)
    res.round(4).to_csv(OUT / "peru_sdid.csv", index=False)
    print(res.round(2).to_string(index=False))
    w = keep[("ha", "during", "sdid")][0]["w"].sort_values(ascending=False)
    lam = keep[("ha", "during", "sdid")][0]["lam"]
    print("unit weights (ha, during):\n", w[w > 0.005].round(3).to_string())
    print("time weights (ha, during):\n", lam.round(3).to_string())

    names = {"did": "plain DiD (equal weights)", "sc": "synthetic control", "sdid": "synthetic DiD"}
    for r in rows:
        u = "ha/yr" if r["scale"] == "ha" else "share of own 2014-18 mean (1 = one normal year)"
        per = {"during": "2019-21", "after": "2022-25", "during_pre2011": "2019-21, pre-period 2011-18"}[r["period"]]
        base = f"sdid_{r['method']}_{r['scale']}_{r['period']}"
        lab = f"{names[r['method']]}, Tambopata BZ vs {r['n'] - 1} buffer zones, {per}, {u}"
        reg.add(base, r["tau"], u, f"Estimate: {lab}. One treated zone: description.", "description", SRC)
        reg.add(base + "_rank", r["rank"], "rank", f"Placebo-in-space rank (1 = biggest fall), {lab}", "description", SRC)
        reg.add(base + "_n", r["n"], "count", f"Zones in the placebo ranking, {lab}", "description", SRC)
        reg.add(base + "_p", r["p"], "p-value", f"Placebo p = rank / n, {lab}", "description", SRC)
        reg.add(base + "_se", r["placebo_se"], u, f"Placebo standard error (sd of placebo estimates), {lab}", "description", SRC)
    reg.add("sdid_top_weight", w.iloc[0], "share", f"Largest SDID unit weight (ha, 2019-21): {w.index[0].replace('|', ' ')}", "description", SRC)
    reg.add("sdid_n_weighted", int((w > 0.01).sum()), "count", "Comparison zones with SDID unit weight > 1% (ha, 2019-21)", "description", SRC)
    reg.add("sdid_lambda_2018", lam.loc[2018], "share", "SDID time weight on 2018 (ha, 2019-21)", "description", SRC)
    _figure(panels["ha"], keep, res)
    return res


def _figure(Y, keep, res):
    r, est = keep[("ha", "during", "sdid")]
    w, lam = r["w"], r["lam"]
    rr = res.set_index(["scale", "period", "method"])
    s_d, s_s = rr.loc[("ha", "during", "sdid")], rr.loc[("scaled", "during", "sdid")]
    years = list(range(2014, 2026))
    tam = Y.loc[years, TU]
    synth = Y.loc[years, w.index] @ w
    shift = float(lam @ (Y.loc[lam.index, TU] - synth.loc[lam.index]))   # the free intercept, on the time-weighted pre-years
    fig = plt.figure(figsize=(9, 4.8))
    a1 = fig.add_axes([0.075, 0.2, 0.56, 0.58]); a2 = fig.add_axes([0.75, 0.2, 0.22, 0.58])
    first = "biggest fall" if s_d["rank"] == 1 else f"rank {int(s_d['rank'])} of {int(s_d['n'])}"
    headline(fig, f"Synthetic DiD: {s_d['tau']:+,.0f} ha/yr in 2019–21, the {first}; scaled to size, rank {int(s_s['rank'])} of {int(s_s['n'])}".replace("-", "−").replace("the rank", "rank"),
             "Left: annual additions to mining area, Tambopata BZ vs the weighted comparison zones (shifted to Tambopata’s level).\n"
             "Right: the same estimate when each other zone is ‘treated’ instead.")
    period_band(a1, 2018.5, 2021.5, "Mercurio years")
    a1.bar(lam.index, lam.values * 0.18 * max(tam.max(), 1), bottom=0, width=0.6, color=GRID, zorder=1)
    a1.plot(years, synth + shift, color=C["twin"], lw=2, ls=(0, (4, 2)), zorder=3)
    a1.plot(years, tam, color=C["lapampa"], lw=2.2, zorder=4)
    a1.plot(years, tam, "o", color=C["lapampa"], ms=4, mec="white", mew=0.8, zorder=5)
    up = tam.iloc[-1] >= (synth + shift).iloc[-1]
    label_end(a1, years[-1], tam.iloc[-1], "Tambopata BZ", C["lapampa"], dy=10 if up else -10)
    label_end(a1, years[-1], (synth + shift).iloc[-1], "Synthetic DiD\ncomparison", C["twin"], weight="normal",
              dy=-14 if up else 14)
    a1.annotate("grey bars: time weights", (lam.idxmax(), lam.max() * 0.18 * tam.max()), xytext=(0, 6),
                textcoords="offset points", ha="center", fontsize=7, color=MUTED)
    style_axes(a1); a1.set_xlim(2013.5, 2025.5); a1.set_xticks(years[::2])
    a1.set_ylabel("ha per year")
    a1.set_title("Tambopata vs its synthetic-DiD comparison", fontsize=9.5)
    # right: placebo strip
    yy = np.random.default_rng(1).uniform(-0.25, 0.25, len(est))
    a2.scatter(est, yy, s=28, color=C["other"], edgecolor="white", lw=0.6, zorder=2)
    a2.scatter([r["tau"]], [0], s=70, color=C["lapampa"], edgecolor="white", lw=1, zorder=3)
    a2.annotate(f"Tambopata\n{r['tau']:+,.0f}".replace("-", "−"), (r["tau"], 0), xytext=(0, 14), textcoords="offset points",
                ha="center", va="bottom", fontsize=8, color=INK, fontweight="semibold")
    a2.axvline(0, color=INK2, lw=0.8)
    a2.set_ylim(-1, 1); a2.set_yticks([])
    for sp in ("top", "right", "left"): a2.spines[sp].set_visible(False)
    a2.xaxis.grid(True, color=GRID, lw=0.6)
    a2.xaxis.set_major_formatter(plt.FuncFormatter(lambda v, p: f"{v:+,.0f}".replace("-", "−") if v else "0"))
    a2.set_title("Placebo zones (grey)", fontsize=9.5)
    a2.set_xlabel("2019–21 estimate, ha/yr")
    a2.text(0.5, 0.04, f"rank {int(s_d['rank'])} of {int(s_d['n'])}, p = {s_d['p']:.2f}", ha="center", fontsize=8,
            color=INK2, transform=a2.transAxes)
    finish_figure(fig, f"{SRC_MAPBIOMAS}. Synthetic DiD (Arkhangelsky et al. 2021): unit weights match the comparison zones’ "
                       "pre-2019 trend (2014–18), a free intercept absorbs the level gap, time weights pick the pre-years. "
                       "One treated zone: placebo ranks, no confidence interval. Description.", OUT / "fig_sdid.png")
