"""Synthetic control for the Tambopata buffer zone (Operation Mercurio, Feb 2019). DESCRIPTION, not causal.

Data (plan v3): national raster panel of Peruvian buffer zones, whole official SERNANP polygons (zonedata.bz_panel),
outcome = NET mining additions (ha/yr) = new land + re-mined - stopped, MapBiomas Peru Collection 4 rasters.
NET ONLY: the weights depend on the outcome, so new land / re-mined / stopped would each need their own fit and their
gaps would not add up to the net gap.
Method: weights w >= 0, sum w = 1, minimise the pre-period sum of squared gaps. Solver: the accelerated projected
gradient (FISTA) of peru_sdid._simplex_ls, no intercept, no penalty. The problem is convex, so it reaches the global
minimum (the earlier SLSQP multi-start could stop early; review D-S6-6). No covariates.
Fit window = definitions.PERIODS["pre_long"] (2014-18) and donors from pool B (as M1-M4 and SDID, review D-S6-5),
so ranks are comparable across designs.
In-space placebo (Abadie, Diamond & Hainmueller 2010 style): re-run for every donor as if it were treated (donor
pool = the other donors; Tambopata excluded). Two statistics, both registered: the post/pre RMSPE ratio (rank 1 =
largest, two-sided) and the one-sided 2019-21 gap divided by the pre-RMSPE (rank 1 = most negative).

Donor pools (pool B = buffer zones with non-zero net additions 2014-18; Tambopata always out)
  core : excludes Amarakaeri and Bahuaja-Sonene (possible spillover recipients, partly treated)
  ext  : also includes them
Outcomes
  add   : net additions, ha/yr
  addsc : net additions / own mean net addition 2014-18 (1 = a normal year); zones above definitions.MIN_PRE_HA

Caveat to read first: Tambopata's pre-2019 level (~1,600 ha/yr) exceeds every donor, so no convex combination can
reproduce it (convex-hull problem). The fit statistics below document this; the gap is NOT a credible counterfactual
gap. The figure is kept only to show why synthetic control fails here.
"""
from __future__ import annotations
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from common import (OUT, x_of, style_axes, add_event_markers, set_year_ticks, finish_figure,
                    EVENT_TITLE_PAD, headline, label_end, C, INK, INK2, MUTED, placebo_rank)
import definitions as D
import zonedata as Z
from peru_models import _zone_adds, pools
from peru_sdid import _simplex_ls

TAM_U, AMA_U, BAH_U = D.TREATED_ZONE, "amarakaeri_bz", "bahuaja_bz"
FIT = list(range(D.PERIODS["pre_long"][0], D.REF_YEAR + 1))
POST = list(range(D.FIRST_POST, D.YEARS[1] + 1))
SRC = D.SOURCE


def fit_weights(Y0: np.ndarray, y: np.ndarray) -> np.ndarray:
    """Y0: (T_pre, J) donors, y: (T_pre,) treated. Simplex-constrained least squares (convex; FISTA, global optimum)."""
    w = np.clip(_simplex_ls(Y0, y, 0.0, intercept=False, iters=200000, tol=1e-14), 0, None)
    return w / w.sum()


def outcome(ad: pd.DataFrame, kind: str):
    """Return (panel DataFrame year x unit, fit years, scale Series or None)."""
    P = ad.loc[FIT[0]:POST[-1]]
    if kind == "add":
        return P, FIT, None
    if kind == "addsc":
        s = ad.loc[FIT[0]:FIT[-1]].mean()
        return P / s, FIT, s
    raise ValueError(kind)


def donor_pool(ad: pd.DataFrame, pool: str, kind: str) -> list[str]:
    poolB, big, _, _ = pools(ad)
    names = [u for u in (big if kind == "addsc" else poolB) if u != TAM_U]
    if pool == "core":
        names = [u for u in names if u not in (AMA_U, BAH_U)]
    return names


def rmspe(gap: pd.Series, years) -> float:
    return float(np.sqrt(np.mean(np.square(gap.loc[years]))))

DUR, LAT = D.PERIODS["during"], D.PERIODS["later"]


def synth_one(P: pd.DataFrame, fit: list[int], treated: str, donors: list[str]):
    w = fit_weights(P.loc[fit, donors].values, P.loc[fit, treated].values)
    synth = pd.Series(P[donors].values @ w, index=P.index)
    gap = P[treated] - synth
    post = [y for y in POST if y in P.index]
    pre = rmspe(gap, fit)
    ratio = rmspe(gap, post) / max(pre, 1e-9)
    std_gap = float(gap.loc[DUR[0]:DUR[1]].mean()) / max(pre, 1e-9)      # one-sided: 2019-21 gap / pre-RMSPE
    return dict(w=pd.Series(w, index=donors), synth=synth, gap=gap, pre=pre, post=rmspe(gap, post), ratio=ratio,
                std_gap=std_gap)


def run_spec(ad, pool, kind):
    P, fit, scale = outcome(ad, kind)
    donors = donor_pool(ad, pool, kind)
    main = synth_one(P, fit, TAM_U, donors)
    plac = {}
    for d in donors:
        others = [x for x in donors if x != d]
        if len(others) < 2:
            continue
        plac[d] = synth_one(P, fit, d, others)
    ratios = pd.Series({TAM_U: main["ratio"], **{d: r["ratio"] for d, r in plac.items()}})
    rank = int((ratios > main["ratio"]).sum() + 1)       # 1 = largest ratio
    rank_gap = placebo_rank(main["std_gap"], [r["std_gap"] for r in plac.values()])   # 1 = most negative
    lo, hi = P.loc[fit, donors].min(axis=1), P.loc[fit, donors].max(axis=1)
    outside = int(((P.loc[fit, TAM_U] > hi) | (P.loc[fit, TAM_U] < lo)).sum())
    return dict(P=P, fit=fit, scale=scale, donors=donors, main=main, plac=plac, ratios=ratios,
                rank=rank, rank_gap=rank_gap, n=len(ratios), outside=outside, n_fit=len(fit))


def register(reg, key, r):
    m, P = r["main"], r["P"]
    sc = r["scale"][TAM_U] if r["scale"] is not None else 1.0
    unit = "ha/yr" if r["scale"] is None else "ha/yr (scaled fit, multiplied back by Tambopata's own 2014-18 mean)"
    tam, gap = P[TAM_U] * sc, m["gap"] * sc
    fitp = f"{FIT[0]}-{str(FIT[-1])[2:]}"
    desc = lambda s: (f"Synthetic control [{key}], net mining additions, Tambopata buffer zone vs {len(r['donors'])} "
                      f"donor buffer zones, fit {fitp}: {s}. Net only (weights depend on the outcome). Description.")
    kw = dict(measure="net", zone=TAM_U)
    reg.add(f"synth_{key}_n_donors", len(r["donors"]), "units", desc("donor units"), "description", SRC)
    reg.add(f"synth_{key}_pre_rmspe", m["pre"] * sc, unit, desc("pre-period RMSPE of the fit"), "description", SRC,
            period=fitp, **kw)
    reg.add(f"synth_{key}_pre_mean_tam", float(tam.loc[r["fit"]].mean()), unit, desc("Tambopata mean over the fit "
            "window"), "description", SRC, period=fitp, **kw)
    reg.add(f"synth_{key}_pre_mean_synth", float((m["synth"] * sc).loc[r["fit"]].mean()), unit,
            desc("synthetic mean over the fit window"), "description", SRC, period=fitp, **kw)
    reg.add(f"synth_{key}_hull_years_outside", r["outside"], f"years of {r['n_fit']}",
            desc("fit-window years where Tambopata lies outside the donors' min-max range (convex-hull problem)"),
            "description", SRC)
    reg.add(f"synth_{key}_gap_during", float(gap.loc[DUR[0]:DUR[1]].mean()), unit,
            desc("mean gap Tambopata minus synthetic (a misfit, NOT an effect)"), "description", SRC,
            period=D.period_label("during"), **kw)
    reg.add(f"synth_{key}_gap_later", float(gap.loc[LAT[0]:LAT[1]].mean()), unit, desc("mean gap, later years"),
            "description", SRC, period=D.period_label("later"), **kw)
    ex = [y for y in range(LAT[0], LAT[1] + 1) if y != D.LATER_EX]
    reg.add(f"synth_{key}_gap_later_ex2023", float(gap.loc[ex].mean()), unit, desc("mean gap, later years without "
            "2023"), "description", SRC, period="2022, 2024, 2025", **kw)
    reg.add(f"synth_{key}_ratio", m["ratio"], "ratio", desc("post/pre RMSPE ratio, Tambopata"), "description", SRC)
    reg.add(f"synth_{key}_rank", r["rank"], f"rank (1 = largest ratio) of {r['n']}", desc("rank of Tambopata's "
            "post/pre RMSPE ratio among Tambopata + placebo donors (two-sided)"), "description", SRC)
    reg.add(f"synth_{key}_rank_gap", r["rank_gap"], f"rank (1 = most negative) of {r['n']}", desc("rank of "
            "Tambopata's 2019-21 gap / pre-RMSPE among Tambopata + placebo donors (one-sided)"), "description", SRC)
    reg.add(f"synth_{key}_n_units_ranked", r["n"], "units", desc("units in the placebo ranking"), "description", SRC)
    reg.add(f"synth_{key}_pvalue_rank", r["rank"] / r["n"], "share", desc("ratio rank / N (low power with this N; "
            "the fit fails, so not evidence)"), "description", SRC)
    w = m["w"].sort_values(ascending=False)
    for i, (u, v) in enumerate(w.head(3).items(), 1):
        reg.add(f"synth_{key}_w{i}", v, "weight", desc(f"weight #{i}: {Z.bz_name(u)}"), "description", SRC)


def fig(res):
    keyA, keyB = ("core", "add"), ("core", "addsc")
    fig_, axes = plt.subplots(2, 2, figsize=(11, 8.6), sharex="col", gridspec_kw={"hspace": 0.42, "wspace": 0.42})
    out = res[keyA]["outside"]
    headline(fig_, f"No mix of other zones matches Tambopata before 2019 ({out} of {res[keyA]['n_fit']} fit years "
                   "outside their range), so the gap is a misfit",
             f"Synthetic control on net mining additions (new + re-mined − stopped), Tambopata buffer zone vs core donor "
             f"buffer zones, fit {FIT[0]}–{str(FIT[-1])[2:]}, {FIT[0]}–{POST[-1]}.\nLeft: ha/yr. Right: scaled to each "
             "zone's own 2014–18 mean (1 = a normal year).")
    for col, (key, ttl, ylab) in enumerate([
            (keyA, "A. Net additions", "Net additions, ha/yr"),
            (keyB, "B. Net additions relative to own 2014–18 mean", "index (1 = normal year)")]):
        r = res[key]; P = r["P"]; m = r["main"]
        yrs = list(P.index); x = x_of(yrs)
        a, b = axes[0, col], axes[1, col]
        for d, pr in r["plac"].items():
            b.plot(x, pr["gap"], color="#d6d3cc", linewidth=0.8, zorder=1)
        a.axvspan(min(r["fit"]) - 0.5, max(r["fit"]) + 0.5, color="#efece5", zorder=0, lw=0)
        a.plot(x, P[TAM_U], color=C["lapampa"], marker="o", markersize=4, mec="white", mew=0.8, linewidth=2)
        a.plot(x, m["synth"], color=C["twin"], linewidth=2, linestyle=(0, (4, 2)))
        label_end(a, yrs[-1], P[TAM_U].iloc[-1], "Tambopata BZ", C["lapampa"], dx=6, dy=6)
        label_end(a, yrs[-1], m["synth"].iloc[-1], "Synthetic", C["twin"], dx=6, dy=-6)
        a.set_title(ttl + "  (shaded: fit window)", pad=EVENT_TITLE_PAD)
        a.set_ylabel(ylab)
        b.plot(x, m["gap"], color=C["lapampa"], linewidth=2.2, zorder=3)
        b.axhline(0, color=INK2, linewidth=0.8)
        label_end(b, yrs[-1], m["gap"].iloc[-1], "Tambopata gap", C["lapampa"], dx=6)
        b.set_title(f"Gap: Tambopata minus synthetic (grey: {len(r['plac'])} placebo donors)", pad=20)
        b.set_ylabel(ylab)
        if col == 1:
            lim = max(3.0, float(m["gap"].abs().max()) * 1.2); b.set_ylim(-lim, lim)
        b.text(0.0, 1.02, f"Pre-fit error {m['pre']:,.2f}{' ha/yr' if col == 0 else ''} · ratio rank {r['rank']} of "
               f"{r['n']} · gap rank {r['rank_gap']} of {r['n']}", transform=b.transAxes, ha="left", va="bottom",
               fontsize=7.5, color=INK2)
        b.set_xlim(yrs[0] - 0.6, yrs[-1] + 0.6)
        for ax in (a, b):
            style_axes(ax, fmt=(col == 0))
        add_event_markers(a, label=True); add_event_markers(b)
        set_year_ticks(b, yrs, short=True)
    finish_figure(fig_, f"{SRC}. Donors: buffer zones with non-zero net additions 2014–18, excluding Tambopata, "
                        "Amarakaeri and Bahuaja-Sonene. Weights >= 0, sum to 1 (convex solver, global optimum). "
                        "Tambopata's pre-2019 level exceeds every donor (convex-hull problem): the gap is a description "
                        "of a misfit, not a causal estimate. Net only. River dredging and mercury are invisible.",
                  OUT / "fig_peru_synth.png", event_note=True)


def run(pack, reg):
    print("\n== Peru synthetic control (v3: net additions, raster buffer-zone panel) ==")
    ad = _zone_adds()
    res, rows, wrows = {}, [], []
    for pool in ("core", "ext"):
        for kind in ("add", "addsc"):
            r = run_spec(ad, pool, kind); res[(pool, kind)] = r
            key = f"{pool}_{kind}"
            register(reg, key, r)
            m = r["main"]; sc = r["scale"][TAM_U] if r["scale"] is not None else 1.0
            top = ", ".join(f"{u} {v:.2f}" for u, v in m["w"].sort_values(ascending=False).head(3).items())
            print(f"{key:11s} donors={len(r['donors']):2d} preRMSPE={m['pre']*sc:9.1f} outside={r['outside']}/{r['n_fit']} "
                  f"gap_during={float((m['gap']*sc).loc[DUR[0]:DUR[1]].mean()):9.1f} "
                  f"ratio={m['ratio']:.2f} rank={r['rank']}/{r['n']} gaprank={r['rank_gap']}  top: {top}")
            for y in r["P"].index:
                rows.append(dict(spec=key, year=y, tambopata=r["P"].loc[y, TAM_U], synthetic=m["synth"].loc[y],
                                 gap=m["gap"].loc[y]))
            for u, v in m["w"].items():
                wrows.append(dict(spec=key, donor=u, weight=v))
    pd.DataFrame(rows).round(3).to_csv(OUT / "peru_synth_paths.csv", index=False)
    pd.DataFrame(wrows).round(4).to_csv(OUT / "peru_synth_weights.csv", index=False)
    fig(res)
    return res


if __name__ == "__main__":
    from common import Numbers, load_pack
    reg = Numbers(); run(load_pack(), reg)
