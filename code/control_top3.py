"""Ruby's twin design, final version: the best rule-based twins (two after the review; Munduruku dropped), pooled, with statistical tests.

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

from common import ROOT, OUT, style_axes, finish_figure, headline, label_end, callout, period_band, C, INK, INK2, AXIS

INTER = ROOT / "data_intermediate"
TU = "PE-BZ-RN09"
# Munduruku DROPPED after the critical review: our own search log records Op. Mundurukania in May 2021 (inside the
# 2017-21 window of the relaxed rule; snippet, unverified), and its AMW 2018 "stock" is too small to normalise by.
TWINS = {"RAISG-434": ("Amana National Forest", 4443), "RAISG-512": ("Tapajos protection area", 4442)}
TCOL = {"Amana National Forest": C["twin"], "Munduruku territory": "#a79ce6", "Tapajos protection area": "#3e3290"}   # twins = violet family
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
        for c in ("pre_growth_diff", "pre_growth_p", "pre_trend_p", "twin_during", "during_gap"):
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
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(9, 4.5), gridspec_kw={"wspace": 0.6})
    headline(fig, f"Both twins added new mining faster than Tambopata in 2019–21",
             "Left: mining area, index 2018 = 100 (MapBiomas, own collection). "
             "Right: new mining per year, % of own 2018 stock (Amazon Mining Watch).")
    short = {"Tambopata buffer zone": "Tambopata BZ", "Amana National Forest": "Amanã NF", "Tapajos protection area": "Tapajós APA"}
    def spread(ax, items, gap):
        items = sorted(items, key=lambda e: e[1]); ys = [e[1] for e in items]
        for j in range(1, len(ys)):
            ys[j] = max(ys[j], ys[j - 1] + gap)
        for (x, y, lab), yy in zip(items, ys):
            ax.annotate(lab, xy=(x, y), xytext=(x + 0.35 * (ax.get_xlim()[1] - ax.get_xlim()[0]) / 12, yy), textcoords="data",
                        va="center", fontsize=7.5, color=INK, fontweight="semibold", annotation_clip=False,
                        arrowprops=dict(arrowstyle="-", color=AXIS, lw=0.6, shrinkA=0, shrinkB=3))
    a1.plot(I.index, I["Tambopata buffer zone"], color=C["lapampa"], lw=2.4, zorder=4)
    for nm in [v[0] for v in TWINS.values()]:
        a1.plot(I.index, I[nm], color=TCOL[nm], lw=1.8, zorder=3)
    a1.axvline(2018.5, color=INK, lw=1); a1.axhline(100, color=AXIS, lw=0.8); style_axes(a1)
    a1.set_xlim(2008.6, 2023.4); a1.set_ylim(0, I.max().max() * 1.08)
    spread(a1, [(I.index[-1], I[c].iloc[-1], short[c]) for c in I.columns], 0.08 * a1.get_ylim()[1])
    a1.set_ylabel("Index, 2018 = 100"); a1.set_xticks(range(2009, 2024, 3))
    a1.set_title("Growth paths, 2009–2023", pad=8)
    yrs = list(range(2019, 2026))
    period_band(a2, 2018.5, 2021.5, "Operation years")
    sh = {"Tambopata buffer zone": 100 * w.loc[TU, yrs] / w.loc[TU, 2018]}
    for uid, (nm, _) in TWINS.items():
        sh[nm] = 100 * w.loc[uid, yrs] / w.loc[uid, 2018]
    for nm, ser in sh.items():
        col = C["lapampa"] if nm.startswith("Tambopata") else TCOL[nm]
        a2.plot(yrs, ser.values, "-", color=col, lw=2.4 if nm.startswith("Tambopata") else 1.8, zorder=3)
        a2.plot(yrs, ser.values, "o", color=col, ms=4, mec="white", mew=0.8, zorder=4)
    style_axes(a2); a2.set_xlim(2018.6, 2025.4)
    a2.set_ylim(0, max(float(v.max()) for v in sh.values()) * 1.1)
    spread(a2, [(2025, float(v.iloc[-1]), short[k]) for k, v in sh.items()], 0.08 * a2.get_ylim()[1])
    callout(a2, 2020, tam_d, f"Tambopata 2019–21: {tam_d:.0f}%\ntwins’ mean: {pooled_c:.0f}%", dy=-34, arrow=False, fontsize=7.5)
    a2.set_ylabel("% of own 2018 stock"); a2.set_xticks(yrs); a2.set_xticklabels([f"'{str(y)[2:]}" for y in yrs])
    a2.set_title("After 2019: pace of new mining", pad=8)
    finish_figure(fig, f"{SRC}. Left: each line from its own collection, side by side, never subtracted. Twins pass "
                       "all rules if operations after 2021 are allowed. Description.", OUT / "fig_control_top3.png")
    return t
