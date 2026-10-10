"""Synthetic control for the Tambopata buffer zone (Operation Mercurio, Feb 2019). DESCRIPTION, not causal.

Data: MapBiomas Peru Collection 4, class 4.2 Minería, buffer-zone annual additions (ha), via peru.build_series.
Method: weights w >= 0, sum w = 1, minimise the pre-period sum of squared gaps (scipy SLSQP). No covariates.
In-space placebo (Abadie, Diamond & Hainmueller 2010 style): re-run for every donor as if it were treated
(donor pool = the other donors; Tambopata excluded), compare post/pre RMSPE ratios, rank Tambopata.

Donor pools (eligible = mean |addition| 2010-18 >= 1 ha, i.e. non-zero pre-2019 mining; Tambopata always out)
  core : excludes Amarakaeri and Bahuaja-Sonene (possible spillover recipients, partly treated, see agent.md §10)
  ext  : also includes them (they are the only donors with comparable size, but contaminated by design)
Outcomes
  add   : annual addition, ha, fit 2010-18
  addsc : annual addition / own mean |addition| 2014-18 (unit-free; donors need a 2014-18 scale >= 5 ha), fit 2010-18
  cum   : cumulative additions since the 2013 level, ha, fit 2014-18 (smoother; 2013 = 0 for every unit)

Caveat to read first: Tambopata's pre-2019 level (~1,600 ha/yr) exceeds every core donor, so no convex
combination can reproduce it (convex-hull problem). The fit statistics below document this; a poor pre-fit
means the gap is NOT a credible counterfactual gap. Only the ratio-style comparisons are informative.
"""
from __future__ import annotations
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import minimize

from common import (OUT, x_of, style_axes, add_event_markers, set_year_ticks, finish_figure,
                    EVENT_TITLE_PAD, SRC_MAPBIOMAS)
import peru

TAM_U, AMA_U, BAH_U = "Tambopata|Reserva Nacional", "Amarakaeri|Reserva Comunal", "Bahuaja-Sonene|Parque Nacional"
PRE_END, POST = 2018, list(range(2019, 2026))
SRC = "peru_bufferzone_year.csv"

def fit_weights(Y0: np.ndarray, y: np.ndarray) -> np.ndarray:
    """Y0: (T_pre, J) donors, y: (T_pre,) treated. Simplex-constrained least squares."""
    J = Y0.shape[1]
    f = lambda w: float(np.sum((y - Y0 @ w) ** 2))
    g = lambda w: -2 * Y0.T @ (y - Y0 @ w)
    best = None
    starts = [np.full(J, 1 / J)] + [np.eye(J)[k] for k in range(J)]      # uniform + every vertex
    for w0 in starts:
        r = minimize(f, w0, jac=g, bounds=[(0, 1)] * J, method="SLSQP",
                     constraints=[{"type": "eq", "fun": lambda w: w.sum() - 1, "jac": lambda w: np.ones(J)}],
                     options={"maxiter": 300, "ftol": 1e-12})
        if best is None or r.fun < best.fun - 1e-9:
            best = r
    w = np.clip(best.x, 0, None)
    return w / w.sum()

def outcome(lw: pd.DataFrame, kind: str):
    """Return (panel DataFrame year x unit, fit years, scale Series or None)."""
    a = lw.diff()
    if kind == "add":
        return a.loc[2010:2025], list(range(2010, 2019)), None
    if kind == "addsc":
        s = a.loc[2014:2018].abs().mean()
        return a.loc[2010:2025] / s, list(range(2010, 2019)), s
    if kind == "cum":
        return (lw.loc[2013:2025] - lw.loc[2013]), list(range(2014, 2019)), None
    raise ValueError(kind)

def donor_pool(lw: pd.DataFrame, pool: str, kind: str) -> list[str]:
    a = lw.diff()
    elig = a.loc[2010:2018].abs().mean() >= 1.0
    names = [u for u in lw.columns if elig[u] and u != TAM_U]
    if pool == "core":
        names = [u for u in names if u not in (AMA_U, BAH_U)]
    if kind == "addsc":
        s = a.loc[2014:2018].abs().mean()
        names = [u for u in names if s[u] >= 5.0]
    return names

def rmspe(gap: pd.Series, years) -> float:
    return float(np.sqrt(np.mean(np.square(gap.loc[years]))))

def synth_one(P: pd.DataFrame, fit: list[int], treated: str, donors: list[str]):
    w = fit_weights(P.loc[fit, donors].values, P.loc[fit, treated].values)
    synth = pd.Series(P[donors].values @ w, index=P.index)
    gap = P[treated] - synth
    post = [y for y in POST if y in P.index]
    pre = rmspe(gap, fit)
    ratio = rmspe(gap, post) / max(pre, 1e-9)
    return dict(w=pd.Series(w, index=donors), synth=synth, gap=gap, pre=pre, post=rmspe(gap, post), ratio=ratio)

def run_spec(lw, pool, kind):
    P, fit, scale = outcome(lw, kind)
    donors = donor_pool(lw, pool, kind)
    main = synth_one(P, fit, TAM_U, donors)
    plac = {}
    for d in donors:
        others = [x for x in donors if x != d]
        if len(others) < 2:
            continue
        plac[d] = synth_one(P, fit, d, others)
    ratios = pd.Series({TAM_U: main["ratio"], **{d: r["ratio"] for d, r in plac.items()}})
    rank = int((ratios > main["ratio"]).sum() + 1)       # 1 = largest ratio
    lo, hi = P.loc[fit, donors].min(axis=1), P.loc[fit, donors].max(axis=1)
    outside = int(((P.loc[fit, TAM_U] > hi) | (P.loc[fit, TAM_U] < lo)).sum())
    return dict(P=P, fit=fit, scale=scale, donors=donors, main=main, plac=plac, ratios=ratios,
                rank=rank, n=len(ratios), outside=outside, n_fit=len(fit))

def _short(u): return u.split("|")[0]

def register(reg, key, r):
    m, P = r["main"], r["P"]
    sc = r["scale"][TAM_U] if r["scale"] is not None else 1.0
    unit = "ha" if r["scale"] is None else "ha (unscaled back by Tambopata's own 2014-18 mean |addition|)"
    tam = P[TAM_U] * sc
    gap = m["gap"] * sc
    desc = lambda s: f"Synthetic control [{key}]: {s}"
    reg.add(f"synth_{key}_n_donors", len(r["donors"]), "units", desc("donor units"), "description", SRC)
    reg.add(f"synth_{key}_pre_rmspe", m["pre"] * sc, unit, desc("pre-period RMSPE of Tambopata fit"), "description", SRC)
    reg.add(f"synth_{key}_pre_mean_tam", float(tam.loc[r["fit"]].mean()), unit, desc("Tambopata mean over fit window"), "description", SRC)
    reg.add(f"synth_{key}_pre_mean_synth", float((m["synth"] * sc).loc[r["fit"]].mean()), unit, desc("synthetic mean over fit window"), "description", SRC)
    reg.add(f"synth_{key}_hull_years_outside", r["outside"], f"years of {r['n_fit']}",
            desc("fit-window years where Tambopata lies outside the donors' min-max range (convex-hull problem)"), "description", SRC)
    reg.add(f"synth_{key}_gap_2019_21", float(gap.loc[2019:2021].mean()), unit, desc("mean gap Tambopata minus synthetic 2019-21 (description of a gap, NOT an effect)"), "description", SRC)
    reg.add(f"synth_{key}_gap_2022_25", float(gap.loc[2022:2025].mean()), unit, desc("mean gap Tambopata minus synthetic 2022-25"), "description", SRC)
    reg.add(f"synth_{key}_ratio", m["ratio"], "ratio", desc("post/pre RMSPE ratio, Tambopata"), "description", SRC)
    reg.add(f"synth_{key}_rank", r["rank"], f"rank (1 = largest ratio) of {r['n']}", desc("rank of Tambopata ratio among Tambopata + placebo donors"), "description", SRC)
    reg.add(f"synth_{key}_n_units_ranked", r["n"], "units", desc("units in the placebo ranking"), "description", SRC)
    reg.add(f"synth_{key}_pvalue_rank", r["rank"] / r["n"], "share", desc("rank/N (exact permutation p-value analogue; low power with this N)"), "description", SRC)
    w = m["w"].sort_values(ascending=False)
    for i, (u, v) in enumerate(w.head(3).items(), 1):
        reg.add(f"synth_{key}_w{i}", v, "weight", desc(f"weight #{i}: {_short(u)}"), "description", SRC)

def fig(res):
    keyA, keyB = ("core", "add"), ("core", "addsc")
    fig_, axes = plt.subplots(2, 2, figsize=(11, 7.5), sharex="col")
    for col, (key, ttl, ylab) in enumerate([
            (keyA, "A. Annual additions (ha), core donors", "New mining area in the year (ha)"),
            (keyB, "B. Additions / own 2014-18 mean (index), core donors", "Additions relative to own 2014-18 mean")]):
        r = res[key]; P = r["P"]; m = r["main"]
        yrs = list(P.index); x = x_of(yrs)
        a, b = axes[0, col], axes[1, col]
        for d, pr in r["plac"].items():
            b.plot(x, pr["gap"], color="#BBBBBB", linewidth=0.8, zorder=1)
        a.plot(x, P[TAM_U], color="#B07A00", marker="o", linewidth=2, label="Tambopata buffer zone")
        a.plot(x, m["synth"], color="#234A76", marker="s", markersize=4, linewidth=2, linestyle="--", label="Synthetic Tambopata")
        a.axvspan(min(r["fit"]) - 0.5, max(r["fit"]) + 0.5, color="#F2F2F2", zorder=0)
        a.legend(fontsize=8, frameon=False, loc="upper left")
        a.set_title(ttl, loc="left", fontsize=10, pad=EVENT_TITLE_PAD)
        a.set_ylabel(ylab)
        b.plot(x, m["gap"], color="#B07A00", linewidth=2.2, zorder=3, label="Tambopata gap")
        b.plot([], [], color="#BBBBBB", linewidth=1, label=f"Placebo gaps ({len(r['plac'])} donors)")
        b.axhline(0, color="black", linewidth=0.6)
        b.set_ylabel("Gap: Tambopata minus synthetic" + (" (ha)" if col == 0 else " (index)"))
        b.legend(fontsize=8, frameon=False, loc="upper left")
        if col == 1:
            lim = max(3.0, float(m["gap"].abs().max()) * 1.2); b.set_ylim(-lim, lim)
        b.text(0.99, 0.02, f"pre-RMSPE {m['pre']:.2f}{' ha' if col == 0 else ''}; ratio rank {r['rank']} of {r['n']};\n"
               f"Tambopata outside donor range in {r['outside']} of {r['n_fit']} fit years",
               transform=b.transAxes, ha="right", va="bottom", fontsize=7.5, color="#333333",
               bbox=dict(facecolor="white", edgecolor="none", alpha=0.85))
        for i, ax in enumerate((a, b)):
            style_axes(ax); add_event_markers(ax, label=(i == 0 and True))
        set_year_ticks(b, yrs)
    finish_figure(fig_, f"Source: {SRC_MAPBIOMAS}, buffer-zone rows. Shaded = fit window (2010-18). Donors: buffer zones with non-zero "
                        "pre-2019 additions, excluding Tambopata, Amarakaeri and Bahuaja-Sonene. Weights >= 0, sum to 1. "
                        "Tambopata's pre-2019 level exceeds every donor, so the fit is poor (convex-hull problem): the gap is a "
                        "description, not a causal estimate. River dredging and mercury are invisible.",
                  OUT / "fig_peru_synth.png", event_note=True)

def run(pack, reg):
    print("\n== Peru synthetic control ==")
    _, _, lw = peru.build_series(pack)
    res, rows, wrows = {}, [], []
    for pool in ("core", "ext"):
        for kind in ("add", "addsc", "cum"):
            r = run_spec(lw, pool, kind); res[(pool, kind)] = r
            key = f"{pool}_{kind}"
            register(reg, key, r)
            m = r["main"]; sc = r["scale"][TAM_U] if r["scale"] is not None else 1.0
            top = ", ".join(f"{_short(u)} {v:.2f}" for u, v in m["w"].sort_values(ascending=False).head(3).items())
            print(f"{key:11s} donors={len(r['donors']):2d} preRMSPE={m['pre']*sc:9.1f} outside={r['outside']}/{r['n_fit']} "
                  f"gap19-21={float((m['gap']*sc).loc[2019:2021].mean()):9.1f} gap22-25={float((m['gap']*sc).loc[2022:2025].mean()):9.1f} "
                  f"ratio={m['ratio']:.2f} rank={r['rank']}/{r['n']}  top: {top}")
            for y in r["P"].index:
                rows.append(dict(spec=key, year=y, tambopata=r["P"].loc[y, TAM_U], synthetic=m["synth"].loc[y], gap=m["gap"].loc[y]))
            for u, v in m["w"].items():
                wrows.append(dict(spec=key, donor=u, weight=v))
    pd.DataFrame(rows).round(3).to_csv(OUT / "peru_synth_paths.csv", index=False)
    pd.DataFrame(wrows).round(4).to_csv(OUT / "peru_synth_weights.csv", index=False)
    fig(res)
    return res
