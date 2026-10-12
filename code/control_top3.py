"""Ruby's twin design, final version: the THREE best rule-based twins, pooled, with statistical tests.

Twins = the areas that pass all rules when operations after 2021 are allowed (control_select.py, relaxed R2):
Amana National Forest, Munduruku Indigenous Territory, Tapajos Environmental Protection Area (all Brazil).
Tests
  P1 parallel pre-trends: MapBiomas mining area index (2018 = 100), Tambopata BZ (Peru Col 4) vs each twin (Amazonia
     Col 6), 2010-2018: regress the yearly log-growth difference on a constant (mean difference in growth) with
     Newey-West errors; and on a trend. Small n (8 years): read as a check, not proof.
  P2 during gap: AMW new area as % of own 2018 stock, 2019-21; Tambopata vs each twin and vs the pooled twin mean;
     Welch t-test on the 3 annual values each (very small n) and the simple rank (is Tambopata below every twin?).
All DESCRIPTION; the twins run in different collections before 2019 and are never subtracted level-on-level.
"""
from __future__ import annotations
import warnings
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from common import ROOT, OUT, style_axes, finish_figure

INTER = ROOT / "data_intermediate"
TU = "PE-BZ-RN09"
TWINS = {"RAISG-434": ("Amana National Forest", 4443), "BR-TI-29801": ("Munduruku territory", 3770),
         "RAISG-512": ("Tapajos protection area", 4442)}
TCOL = {"Amana National Forest": "#6250d6", "Munduruku territory": "#1baf7a", "Tapajos protection area": "#eda100"}
SRC = "MapBiomas Peru Col 4 (Tambopata) and MapBiomas Amazonia Col 6 (twins) before 2019; Amazon Mining Watch after 2019"


def run(reg):
    import statsmodels.api as sm
    from scipy import stats
    print("\n== Top-3 twins ==")
    w = pd.read_csv(INTER / "amw_candidates_year.csv").pivot(index="unit_id", columns="year", values="new_ha")
    m = pd.read_csv(INTER / "mb_amazonia_col6_mining.csv")
    zb = pd.read_csv(ROOT / "data" / "peru_bufferzone_year.csv")
    tam = zb[(zb.buffer_zone == "Tambopata") & (zb.pa_category == "Reserva Nacional")].groupby("year").mining_ha.sum()
    idx = {"Tambopata buffer zone": 100 * tam / tam.loc[2018]}
    for uid, (nm, gc) in TWINS.items():
        s = m[m.geocode == gc].groupby("year").mining_ha.sum()
        idx[nm] = 100 * s / s.loc[2018]
    I = pd.DataFrame(idx).loc[2009:2023]
    gr = np.log(I).diff().loc[2010:2018]                     # yearly log growth
    rows = []
    for nm in TWINS.values():
        nm = nm[0]
        dg = (gr["Tambopata buffer zone"] - gr[nm]).dropna()
        r1 = sm.OLS(dg, np.ones(len(dg))).fit(cov_type="HAC", cov_kwds={"maxlags": 1})
        r2 = sm.OLS(dg, sm.add_constant(np.arange(len(dg)))).fit(cov_type="HAC", cov_kwds={"maxlags": 1})
        sh_t = 100 * w.loc[TU, [2019, 2020, 2021]] / w.loc[TU, 2018]
        uid = [k for k, v in TWINS.items() if v[0] == nm][0]
        sh_c = 100 * w.loc[uid, [2019, 2020, 2021]] / w.loc[uid, 2018]
        tt = stats.ttest_ind(sh_t.values, sh_c.values, equal_var=False)
        rows.append(dict(twin=nm, pre_growth_diff=r1.params.iloc[0], pre_growth_p=r1.pvalues.iloc[0],
                         pre_trend_slope=r2.params.iloc[1], pre_trend_p=r2.pvalues.iloc[1],
                         tam_during=sh_t.mean(), twin_during=sh_c.mean(), during_gap=sh_t.mean() - sh_c.mean(), during_p=tt.pvalue))
    t = pd.DataFrame(rows)
    pooled_c = np.mean([100 * w.loc[k, [2019, 2020, 2021]].mean() / w.loc[k, 2018] for k in TWINS])
    tam_d = t.tam_during.iloc[0]
    t.round(4).to_csv(OUT / "control_top3_tests.csv", index=False)
    print(t.round(3).to_string(index=False))
    for _, r in t.iterrows():
        key = r.twin.split()[0].lower()
        for c in ("pre_growth_diff", "pre_growth_p", "pre_trend_p", "twin_during", "during_gap", "during_p"):
            reg.add(f"top3_{key}_{c}", r[c], "p-value" if c.endswith("_p") else ("log points/yr" if "growth" in c else "% of 2018 stock"),
                    f"Twin {r.twin}: {c}", "description", SRC)
    reg.add("top3_tam_during", tam_d, "% of 2018 stock", "Tambopata BZ AMW new area per year 2019-21, % of 2018 stock", "description", SRC)
    reg.add("top3_pooled_during", pooled_c, "% of 2018 stock", "Mean of the three twins, same measure", "description", SRC)
    reg.add("top3_ratio", tam_d / pooled_c, "ratio", "Tambopata's 2019-21 pace as a share of the pooled twins' pace", "description", SRC)
    med = np.median([100 * w.loc[k, [2019, 2020, 2021]].mean() / w.loc[k, 2018] for k in TWINS])
    reg.add("top3_median_during", med, "% of 2018 stock", "Median of the three twins (Munduruku's pace is extreme, so the median is the headline)", "description", SRC)
    reg.add("top3_median_ratio", tam_d / med, "ratio", "Tambopata's 2019-21 pace as a share of the median twin's pace", "description", SRC)
    reg.add("top3_below_all", float((t.during_gap < 0).all()), "flag", "1 = Tambopata below every one of the three twins in 2019-21", "description", SRC)
    # figure
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(12, 4.3))
    a1.plot(I.index, I["Tambopata buffer zone"], color="#eb6834", lw=2.4, label="Tambopata buffer zone")
    for nm in TCOL:
        a1.plot(I.index, I[nm], color=TCOL[nm], lw=1.6, label=nm)
    a1.axvline(2018.5, color="black", lw=1); a1.axhline(100, color="#888", lw=0.6); style_axes(a1)
    a1.set_ylabel("Mining area, 2018 = 100\n(MapBiomas, own collection)"); a1.legend(fontsize=7.5, frameon=False)
    a1.set_title("Before 2019: growth paths", loc="left", fontsize=9.5)
    yrs = list(range(2019, 2026))
    a2.plot(yrs, 100 * w.loc[TU, yrs] / w.loc[TU, 2018], "o-", color="#eb6834", lw=2.4, label="Tambopata buffer zone")
    for uid, (nm, _) in TWINS.items():
        a2.plot(yrs, 100 * w.loc[uid, yrs] / w.loc[uid, 2018], "o-", color=TCOL[nm], lw=1.6, ms=3, label=nm)
    a2.axvspan(2018.5, 2021.5, color="#f3e3c2", alpha=0.5, zorder=0); style_axes(a2)
    a2.set_ylabel("New mining per year, % of 2018 stock\n(Amazon Mining Watch)")
    a2.set_title("After 2019: pace of new mining", loc="left", fontsize=9.5)
    fig.suptitle("Three rule-based twins: similar growth before 2019, all faster than Tambopata in 2019-21",
                 x=0.01, ha="left", fontsize=11, fontweight="bold")
    finish_figure(fig, f"Sources: {SRC}. Left: each line from its own collection, side by side, never subtracted. Twins pass "
                       "all rules if operations after 2021 are allowed. Description.", OUT / "fig_control_top3.png", rect_bottom=0.1)
    return t
