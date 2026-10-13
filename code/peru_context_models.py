"""Chapter "Context" as controls: do COVID and enforcement money change the 2019-21 Tambopata gap? DESCRIPTION.

Same panel as the model ladder (peru_models.py, M2): 15 Peruvian buffer zones, zone + year effects, plus each zone's
2014-18 mean addition x ln(gold price). Sample 2015-2025, because the spending series (MEF PP 0128) starts in 2015.

What the year effects already remove: anything that hits every zone in the same year (gold price level, COVID as a
national shock, presidents, national laws). What they can't remove is DIFFERENT exposure. So we add:
  K0  M2 on 2015-25 (the baseline for this sample)
  K1  K0 + COVID exposure: (zone's 2014-18 mean addition) x 1[2020-21]. Big mining zones may have reacted more to
      patrols leaving in 2020-21.
  K2  K0 + Madre de Dios x ln(PP 0128 spending booked in Madre de Dios). The three Madre de Dios zones (Tambopata,
      Amarakaeri, Bahuaja-Sonene) share the regional enforcement budget.
  K3  K1 + K2 together.
Caveat (written into the numbers): K2 controls for part of the treatment itself. Spending peaked in 2019 because of
Mercurio, so it soaks up some of the very effect we measure. With one treated zone and one spending series, money
and the operation can't be separated; a smaller gap in K2 means "money and the operation move together", not
"the operation didn't matter".
Inference: placebo in space (each other zone treated in turn, Tambopata removed from its pool), as in the ladder.
Dose: Tambopata's yearly gap (its addition minus the other zones' mean, minus the 2015-18 mean gap) against
ln(spending), 2015-2025: a correlation over 11 years, description only.
"""
from __future__ import annotations
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from common import OUT, style_axes, finish_figure, headline, label_end, C, INK, INK2, MUTED, GRID, AXIS
import peru_models as pm
import v2_tests

SRC = "peru_bufferzone_year.csv (MapBiomas Peru Col 4), prices_annual.csv, MEF PP 0128 devengado (Madre de Dios)"
MDD = {"Tambopata|Reserva Nacional", "Amarakaeri|Reserva Comunal", "Bahuaja-Sonene|Parque Nacional"}
MODELS = {"K0": "Gold price × size (M2), 2015–25",
          "K1": "+ COVID 2020–21 × size",
          "K2": "+ Madre de Dios × enforcement money",
          "K3": "+ both"}
Y0, Y1 = 2015, 2025
REAL = {"during": (2019, 2021), "after": (2022, 2025)}


def fit(ad, units, treated, model, gold, spend):
    d = ad.loc[Y0:Y1, units].reset_index().melt(id_vars="year", var_name="unit", value_name="y")
    pre = ad.loc[2014:2018, units].mean()
    X = {f"post_{k}": ((d.unit == treated) & d.year.between(*v)).astype(float) for k, v in REAL.items()}
    X["pre_x_lngold"] = d.unit.map(pre) * np.log(d.year.map(gold))
    if model in ("K1", "K3"):
        X["pre_x_covid"] = d.unit.map(pre) * d.year.between(2020, 2021)
    if model in ("K2", "K3"):
        X["mdd_x_lnspend"] = d.unit.isin(MDD) * np.log(d.year.map(spend))
    X = pd.DataFrame(X).astype(float)
    fe = pd.concat([pd.get_dummies(d.unit, dtype=float), pd.get_dummies(d.year, prefix="y", drop_first=True, dtype=float)], axis=1)
    b, *_ = np.linalg.lstsq(pd.concat([X, fe], axis=1).to_numpy(), d.y.to_numpy(), rcond=None)
    return dict(zip(X.columns, b[: X.shape[1]]))


def run(pack, reg):
    ad = pm._zone_adds(pack)
    gold = pack["prices"].set_index("year")["gold"]
    spend = v2_tests.mef_series().loc[Y0:Y1]
    assert len(spend) == Y1 - Y0 + 1, "PP 0128 series incomplete"
    pool = sorted(u for u in ad.columns if ad.loc[2014:2018, u].abs().sum() > 0)
    assert len(pool) == 15 and pm.TU in pool
    rows = []
    for m, lab in MODELS.items():
        real = fit(ad, pool, pm.TU, m, gold, spend)
        others = {u: fit(ad, [v for v in pool if v != pm.TU], u, m, gold, spend)["post_during"] for u in pool if u != pm.TU}
        others[pm.TU] = real["post_during"]
        rank = int(pd.Series(others).rank().loc[pm.TU])
        rows.append(dict(model=m, label=lab, during=real["post_during"], after=real["post_after"], rank=rank, n=len(pool),
                         covid=real.get("pre_x_covid", np.nan), spend=real.get("mdd_x_lnspend", np.nan)))
    res = pd.DataFrame(rows)
    res.round(3).to_csv(OUT / "peru_context_models.csv", index=False)
    for r in rows:
        k = r["model"].lower()
        d = f"{r['model']} ({r['label']}; 15 buffer zones, zone + year effects, 2015-25). Description: one treated zone"
        reg.add(f"ctx_{k}_during", r["during"], "ha/yr", f"Tambopata 2019-21 coefficient, {d}", "description", SRC)
        reg.add(f"ctx_{k}_after", r["after"], "ha/yr", f"Tambopata 2022-25 coefficient, {d}", "description", SRC)
        reg.add(f"ctx_{k}_rank", r["rank"], "rank", f"Tambopata's rank when each zone is treated in turn (1 = biggest fall), {d}", "description", SRC)
        reg.add(f"ctx_{k}_ri_p", r["rank"] / r["n"], "p-value", f"Randomization p-value, {d}", "description", SRC)
    reg.add("ctx_n", 15, "count", "Zones in the context models", "description", SRC)
    reg.add("ctx_k1_covid_coef", rows[1]["covid"], "ha per ha of pre mean", "K1: extra 2020-21 addition per hectare of a zone's 2014-18 mean addition (COVID exposure)", "description", SRC)
    reg.add("ctx_k2_spend_coef", rows[2]["spend"], "ha/yr per log-point", "K2: change in Madre de Dios zones' annual addition per 1.0 rise in ln(PP 0128 spending). Partly the treatment itself", "description", SRC)
    k0, k3 = rows[0]["during"], rows[3]["during"]
    reg.add("ctx_k3_vs_k0_share", k3 / k0, "share", "K3 2019-21 coefficient as a share of K0's: how much of the gap survives both controls", "description", SRC)
    # dose: Tambopata's yearly gap vs spending
    oth = [u for u in pool if u != pm.TU]
    gap = (ad.loc[Y0:Y1, pm.TU] - ad.loc[Y0:Y1, oth].mean(axis=1))
    gap = gap - gap.loc[2015:2018].mean()
    ls = np.log(spend)
    corr = float(np.corrcoef(ls, gap)[0, 1])
    slope = float(np.polyfit(ls, gap, 1)[0])
    reg.add("ctx_dose_corr", corr, "correlation", "Correlation, 2015-25, of Tambopata's yearly gap (its addition minus the other 14 zones' mean, net of the 2015-18 mean gap) with ln(PP 0128 spending in Madre de Dios). Description, 11 points", "description", SRC)
    reg.add("ctx_dose_slope", slope, "ha/yr per log-point", "Slope of that gap on ln(spending): ha/yr change in the gap per 1.0 rise in ln(spending) (~2.7x money)", "description", SRC)
    _figure(res, gap, spend, corr)
    return res


def _figure(res, gap, spend, corr):
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(10.5, 4.6), gridspec_kw=dict(width_ratios=[1.15, 1], wspace=0.35))
    keep = res.iloc[-1].during / res.iloc[0].during
    rk = int(res["rank"].max())
    headline(fig, f"Adding COVID and enforcement money keeps {keep:.0%} of the 2019–21 fall"
                  + ("; Tambopata still ranks first" if rk == 1 else f"; worst rank {rk} of 15"),
             "Left: Tambopata's 2019–21 gap (ha/yr) under each set of controls, rank among 15 zones. "
             "Right: the yearly gap against enforcement money")
    ys = np.arange(len(res))[::-1] * 1.0
    lo = min(res.during) * 1.12
    a1.barh(ys, res.during, 0.42, color=C["lapampa"])
    for y_, (_, r) in zip(ys, res.iterrows()):
        a1.text(lo, y_ + 0.33, f"{r.model}  {r.label}", ha="left", va="bottom", fontsize=8.5, color=INK)
        a1.annotate(f"{r.during:,.0f}".replace("-", "−") + f"  ·  rank {r['rank']} of {r.n}", (r.during, y_), xytext=(6, 0),
                    textcoords="offset points", ha="left", va="center", fontsize=8.5, color="white", fontweight="semibold")
    a1.set_yticks([])
    a1.axvline(0, color=INK2, lw=0.8)
    for sp in ("top", "right", "left"): a1.spines[sp].set_visible(False)
    a1.xaxis.grid(True, color=GRID, lw=0.6); a1.set_axisbelow(True)
    a1.set_xlim(lo, 0); a1.set_ylim(-0.5, ys.max() + 0.85)
    a1.xaxis.set_major_formatter(plt.FuncFormatter(lambda v, p: f"{v:,.0f}".replace("-", "−")))
    a1.set_xlabel("Tambopata minus other zones, 2019–21, ha per year")
    style_axes(a2)
    x = spend / 1e6
    a2.axhline(0, color=AXIS, lw=0.9)
    a2.scatter(x, gap, s=30, color=[C["lapampa"] if 2019 <= y <= 2021 else C["other"] for y in gap.index], zorder=3, lw=0)
    for y, xv, gv in zip(gap.index, x, gap):
        a2.annotate(str(y), (xv, gv), xytext=(5, 3), textcoords="offset points", fontsize=7.5, color=INK2)
    a2.set_xscale("log")
    from matplotlib.ticker import FuncFormatter, NullFormatter
    a2.xaxis.set_major_formatter(FuncFormatter(lambda v, p: f"{v:g}")); a2.xaxis.set_minor_formatter(NullFormatter())
    a2.set_xticks([1, 2, 5, 10, 20, 30])
    a2.set_xlabel("PP 0128 spending booked in Madre de Dios, million soles (log)")
    a2.set_ylabel("Tambopata's yearly gap, ha (net of 2015–18)")
    a2.set_title(f"{'Weak' if abs(corr) < 0.5 else 'Clear'} link: more money, {'slightly ' if abs(corr) < 0.5 else ''}bigger fall "
                 f"(r = {corr:.2f}, 11 years)".replace("-", "−"), fontsize=10)
    finish_figure(fig, f"Sources: {SRC}. Zone + year effects in every model. K2 and K3 control for money that rose BECAUSE "
                       "of Mercurio, so they absorb part of the effect. One treated zone: ranks, not confidence intervals. "
                       "Description.", OUT / "fig_peru_context_models.png")


if __name__ == "__main__":
    from common import Numbers, load_pack
    reg = Numbers(); run(load_pack(), reg)
    for k, v in reg.rows.items():
        print(k, round(v["value"], 3))
