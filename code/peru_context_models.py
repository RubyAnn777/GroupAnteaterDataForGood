"""Chapter "Context" as controls: what COVID exposure and enforcement money do to the 2019-21 gap. DESCRIPTION.

Panel (plan v3): national raster panel of Peruvian buffer zones (zonedata.bz_panel), pool B (15 zones with non-zero
net additions 2014-18), outcome = NET mining additions (ha/yr) = new land + re-mined - stopped, MapBiomas Peru
Collection 4 rasters. Zone + year effects, plus each zone's 2014-18 mean net addition x ln(gold price) (model M2).
Sample starts in the first year of the spending series (MEF PP 0128, 2015) and ends in definitions.YEARS[1].

What the year effects remove: what changed in the AVERAGE comparison zone in each year (a few tens of ha, because the
comparison zones hold little mining). They do NOT remove shocks that scale with a zone's size. So we add:
  K0  M2 on this sample (the baseline)
  K1  K0 + COVID exposure: (zone's 2014-18 mean net addition) x 1[2020-21].
  K2  K0 + Madre de Dios x ln(PP 0128 spending booked in Madre de Dios).
  K3  K1 + K2 together.
The treated unit's post years are SATURATED (one dummy per year 2019-25; "during" = mean of the 2019-21 dummies,
"later" = mean of the 2022-25 dummies), so the COVID and money slopes are not fitted on Tambopata's own post-2019 path
(review card 05, within-bin identification).
BAD CONTROL: spending jumped in 2019 BECAUSE of Mercurio, so K2 and K3 control for part of the treatment itself
(a mediator). And the COVID and money terms move the gap in opposite directions; that K3 lands near K0 is the sum of
two shifts, NOT evidence of robustness. With one treated region and one spending series, money and the operation
cannot be separated, and the data cannot show whether more money meant a larger fall.
Additivity: all regressors are built from the NET pre mean and held fixed, so the coefficients are also estimated on
new land, re-mined and stopped (net = new + re-mined - stopped, asserted). Ranks: net only; the raw rank in hectares
measures size, so a size-relative rank is reported next to it.
"""
from __future__ import annotations
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from common import OUT, style_axes, finish_figure, headline, C, INK, INK2, GRID, AXIS, placebo_rank
import definitions as D
import zonedata as Z
import peru_models as pm
import v2_tests

SRC = f"{D.SOURCE}; prices_annual.csv; MEF PP 0128 devengado (Madre de Dios)"
MDD = {"tambopata_bz", "amarakaeri_bz", "bahuaja_bz"}       # the Madre de Dios-linked buffer zones (peru.pools pool A)
MODELS = {"K0": "Gold price × size (M2)",
          "K1": "+ COVID 2020–21 × size",
          "K2": "+ Madre de Dios × enforcement money",
          "K3": "+ both"}
PRE = D.PERIODS["pre_long"]
COVID = (2020, 2021)                                         # context years (COVID-19 reached Peru in March 2020)
MEAS = ["net"] + D.PARTS


def fit(ad, units, treated, model, gold, spend, y0, y1, pre):
    """OLS with zone and year dummies. `pre` = zone net pre means (held fixed for every part)."""
    d = ad.loc[y0:y1, units].reset_index().melt(id_vars="year", var_name="unit", value_name="y")
    X = {f"post_y{y}": ((d.unit == treated) & (d.year == y)).astype(float) for y in range(D.FIRST_POST, y1 + 1)}
    X["pre_x_lngold"] = d.unit.map(pre) * np.log(d.year.map(gold))
    if model in ("K1", "K3"):
        X["pre_x_covid"] = d.unit.map(pre) * d.year.between(*COVID)
    if model in ("K2", "K3"):
        X["mdd_x_lnspend"] = d.unit.isin(MDD) * np.log(d.year.map(spend))
    X = pd.DataFrame(X).astype(float)
    fe = pd.concat([pd.get_dummies(d.unit, dtype=float), pd.get_dummies(d.year, prefix="y", drop_first=True, dtype=float)], axis=1)
    b, *_ = np.linalg.lstsq(pd.concat([X, fe], axis=1).to_numpy(), d.y.to_numpy(), rcond=None)
    out = dict(zip(X.columns, b[: X.shape[1]]))
    for k in ("during", "later"):
        a, e = D.PERIODS[k]
        out[k] = float(np.mean([out[f"post_y{y}"] for y in range(a, e + 1)]))
    return out


def run(pack, reg):
    print("\n== Context models K0-K3 (v3: net additions, raster buffer-zone panel) ==")
    ad = pm._zone_adds()
    gold = pack["prices"].set_index("year")["gold"]
    spend_all = v2_tests.mef_series()
    y0, y1 = max(PRE[0], int(spend_all.index.min())), D.YEARS[1]
    spend = spend_all.loc[y0:y1]
    assert len(spend) == y1 - y0 + 1, "PP 0128 series incomplete"
    pool, big, _, pre = pm.pools(ad)
    T = pm.TU
    assert T in pool
    W = {m: pm._zone_adds(measure=m) for m in MEAS}
    yrs = f"{y0}–{str(y1)[2:]}"
    rows = []
    for m, lab in MODELS.items():
        real = {q: fit(W[q], pool, T, m, gold, spend, y0, y1, pre[pool]) for q in MEAS}
        for k in ("during", "later"):
            r = real
            assert abs(r["net"][k] - (r["new"][k] + r["remined"][k] - r["stopped"][k])) < 0.01
        noT = [v for v in pool if v != T]
        others = {u: fit(ad, noT, u, m, gold, spend, y0, y1, pre[noT])["during"] for u in noT}
        rank = placebo_rank(real["net"]["during"], others.values())
        rank_sc = placebo_rank(real["net"]["during"] / pre[T], [others[u] / pre[u] for u in big if u != T])
        rows.append(dict(model=m, label=lab, n=len(pool), rank=rank, rank_scaled=rank_sc, n_scaled=len(big),
                         covid=real["net"].get("pre_x_covid", np.nan), spend=real["net"].get("mdd_x_lnspend", np.nan),
                         **{f"{k}_{q}": real[q][k] for k in ("during", "later") for q in MEAS}))
    res = pd.DataFrame(rows)
    res.round(3).to_csv(OUT / "peru_context_models.csv", index=False)
    print(res[["model", "during_net", "later_net", "rank", "rank_scaled", "covid", "spend"]].round(2).to_string(index=False))
    for r in rows:
        k = r["model"].lower()
        d = (f"{r['model']} ({r['label']}; Tambopata buffer zone vs {r['n'] - 1} buffer zones, zone + year effects, "
             f"saturated post years, {yrs}); description, one treated zone")
        for key in ("during", "later"):
            Z.register_parts(reg, f"ctx_{k}_{key}", {q: r[f"{key}_{q}"] for q in MEAS}, T, D.period_label(key),
                             f"coefficient, {d}", source=SRC)
        kw = dict(measure="net", zone=T, period=D.period_label("during"))
        reg.add(f"ctx_{k}_rank", r["rank"], "rank", f"Raw placebo-in-space rank (1 = biggest fall; measures size as "
                f"much as effect), net additions 2019-21, {d}", "description", SRC, **kw)
        reg.add(f"ctx_{k}_rank_scaled", r["rank_scaled"], "rank", f"Size-relative rank (coefficient / own 2014-18 mean, "
                f"{r['n_scaled']} zones above {D.MIN_PRE_HA:g} ha/yr), net additions 2019-21, {d}", "description", SRC, **kw)
        reg.add(f"ctx_{k}_ri_p", r["rank"] / r["n"], "p-value", f"Raw rank / zones, never cite alone, {d}",
                "description", SRC, **kw)
    reg.add("ctx_n", len(pool), "count", "Zones in the context models", "description", SRC)
    reg.add("ctx_n_scaled", len(big), "count", "Zones in the size-relative ranking of the context models",
            "description", SRC)
    reg.add("ctx_k1_covid_coef", rows[1]["covid"], "ha per ha of pre mean", "K1: extra 2020-21 net addition per hectare "
            "of a zone's 2014-18 mean net addition (COVID exposure); identified by the comparison zones",
            "description", SRC, measure="net", zone="pool B", period="2020–21")
    reg.add("ctx_k2_spend_coef", rows[2]["spend"], "ha/yr per log-point", "K2: change in the Madre de Dios zones' net "
            "additions per 1.0 rise in ln(PP 0128 spending). A bad control: spending rose because of Mercurio",
            "description", SRC, measure="net", zone="Madre de Dios buffer zones", period=yrs)
    k0 = rows[0]["during_net"]
    for i, nm in ((1, "covid"), (2, "money")):
        reg.add(f"ctx_shift_{nm}_during_net", rows[i]["during_net"] - k0, "ha/yr", f"Net mining additions, Tambopata "
                f"buffer zone, 2019-21: K{i} coefficient minus K0 (how far the {nm} term moves the gap; positive = "
                "smaller fall)", "description", SRC, measure="net", zone=T, period=D.period_label("during"))
    reg.add("ctx_k3_vs_k0_share", rows[3]["during_net"] / k0, "share", "K3 2019-21 coefficient as a share of K0's. NOT "
            "a robustness check: the COVID and money terms move the gap in opposite directions (ctx_shift_*) and money "
            "is a bad control", "description", SRC, measure="net", zone=T, period=D.period_label("during"))
    # dose: Tambopata's yearly net gap vs spending (description; spending responds to mining, so not a dose-response)
    oth = [u for u in pool if u != T]
    gap = ad.loc[y0:y1, T] - ad.loc[y0:y1, oth].mean(axis=1)
    gap = gap - gap.loc[y0:D.REF_YEAR].mean()
    ls = np.log(spend)
    corr = float(np.corrcoef(ls, gap)[0, 1])
    slope = float(np.polyfit(ls, gap, 1)[0])
    reg.add("ctx_dose_corr", corr, "correlation", f"Correlation, {yrs}, of the Tambopata buffer zone's yearly gap in "
            f"net additions (minus the other {len(oth)} zones' mean, net of its {y0}-{D.REF_YEAR} mean) with "
            f"ln(PP 0128 spending in Madre de Dios). {len(gap)} points; money follows the operation, so not a "
            "dose-response", "description", SRC, measure="net", zone=T, period=yrs)
    reg.add("ctx_dose_slope", slope, "ha/yr per log-point", "Slope of that gap on ln(spending). Not a dose-response",
            "description", SRC, measure="net", zone=T, period=yrs)
    _figure(res, gap, spend, corr, yrs, len(oth))
    return res


def _figure(res, gap, spend, corr, yrs, n_oth):
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(10.5, 4.8), gridspec_kw=dict(width_ratios=[1.15, 1], wspace=0.35))
    sh_c = res.during_net.iloc[1] - res.during_net.iloc[0]
    sh_m = res.during_net.iloc[2] - res.during_net.iloc[0]
    headline(fig, f"The COVID term moves the 2019–21 gap by {sh_c:+,.0f} ha/yr, the money term by {sh_m:+,.0f}: "
                  "they offset, so K3 ≈ K0 proves nothing".replace("-", "−"),
             f"Left: Tambopata buffer zone's 2019–21 coefficient on net mining additions (new + re-mined − stopped), ha/yr, "
             f"vs {n_oth} buffer zones, {yrs}.\nRight: the yearly gap against enforcement money (money rose because of "
             "Mercurio: a bad control, not a dose)")
    ys = np.arange(len(res))[::-1] * 1.0
    lo = min(res.during_net) * 1.12
    a1.barh(ys, res.during_net, 0.42, color=C["lapampa"])
    for y_, (_, r) in zip(ys, res.iterrows()):
        a1.text(lo, y_ + 0.33, f"{r.model}  {r.label}", ha="left", va="bottom", fontsize=8.5, color=INK)
        a1.annotate(f"{r.during_net:,.0f}".replace("-", "−") + f"  ·  raw rank {r['rank']} of {r.n}, size-relative "
                    f"{r.rank_scaled} of {r.n_scaled}", (r.during_net, y_), xytext=(6, 0), textcoords="offset points",
                    ha="left", va="center", fontsize=8, color="white", fontweight="semibold")
    a1.set_yticks([])
    a1.axvline(0, color=INK2, lw=0.8)
    for sp in ("top", "right", "left"): a1.spines[sp].set_visible(False)
    a1.xaxis.grid(True, color=GRID, lw=0.6); a1.set_axisbelow(True)
    a1.set_xlim(lo, 0); a1.set_ylim(-0.5, ys.max() + 0.85)
    a1.xaxis.set_major_formatter(plt.FuncFormatter(lambda v, p: f"{v:,.0f}".replace("-", "−")))
    a1.set_xlabel("Net additions, Tambopata minus other zones, 2019–21, ha/yr")
    style_axes(a2)
    x = spend / 1e6
    a, b = D.PERIODS["during"]
    a2.axhline(0, color=AXIS, lw=0.9)
    a2.scatter(x, gap, s=30, color=[C["lapampa"] if a <= y <= b else C["other"] for y in gap.index], zorder=3, lw=0)
    for y, xv, gv in zip(gap.index, x, gap):
        a2.annotate(str(y), (xv, gv), xytext=(5, 3), textcoords="offset points", fontsize=7.5, color=INK2)
    a2.set_xscale("log")
    from matplotlib.ticker import FuncFormatter, NullFormatter
    a2.xaxis.set_major_formatter(FuncFormatter(lambda v, p: f"{v:g}")); a2.xaxis.set_minor_formatter(NullFormatter())
    a2.set_xticks([1, 2, 5, 10, 20, 30])
    a2.set_xlabel("PP 0128 spending booked in Madre de Dios, million soles (log)")
    a2.set_ylabel(f"Yearly gap in net additions, ha (net of {gap.index[0]}–{D.REF_YEAR})")
    a2.set_title(f"r = {corr:.2f} over {len(gap)} years; orange = 2019–21".replace("-", "−"), fontsize=10)
    finish_figure(fig, f"Sources: {SRC}. Zone + year effects and gold price × size in every model; Tambopata's post years "
                       "saturated. K2 and K3 control for money that rose BECAUSE of Mercurio, so they absorb part of the "
                       "effect. One treated zone: ranks, not confidence intervals. Description.",
                  OUT / "fig_peru_context_models.png")


if __name__ == "__main__":
    from common import Numbers, load_pack
    reg = Numbers(); run(load_pack(), reg)
    for k, v in reg.rows.items():
        print(k, round(v["value"], 3))
