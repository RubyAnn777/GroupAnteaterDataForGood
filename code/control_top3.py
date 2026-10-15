"""Ruby's twin design, final version: the rule-based twins pooled, with the pre-2019 checks (review card 10).

Twins = every area that passes all four rules of control_select.py when verified operations after 2021 are allowed
(R2b), with operation status from the ONE dating rule R* (brazil_v2): an unverified report (Munduruku, May 2021
snippet) is context and does not exclude a twin; SENSITIVITY: count unverified reports (the area becomes "unclear"
and drops out). The number of twins is read from the data, never hard-coded; ids are top3_* for continuity only.
Treated unit = the official whole Tambopata buffer zone (registry), on every side:
  P1 pre-2019 paths: mining area (stock) index 2018 = 100; Tambopata from the MapBiomas Peru Collection 4 rasters on
     the v3 registry (control_select.tambopata_index), each twin from MapBiomas Amazonía Collection 6 statistics
     (a DIFFERENT collection: compared as growth rates of indices, never subtracted level-on-level). Yearly log-growth
     difference 2010-2018 regressed on a constant (mean growth gap) and on a trend, Newey-West errors. Card 10:
     Tambopata's growth was CONVERGING on the twins' before 2019 (the slope test), so the paths are not parallel.
  P2 2019-21 (definitions.PERIODS["during"]): AMW new area as % of own 2018 AMW area (comparable to first-time mining,
     NOT to net additions); Tambopata vs each twin and vs the twins' mean (headline, D-S10-2). Welch t on 3 values.
     No later-years comparison: the twins had their own operations from 2023.
All DESCRIPTION (one treated area, few twins, two products, two collections).
"""
from __future__ import annotations
import warnings
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from common import ROOT, OUT, style_axes, finish_figure, headline, label_end, callout, period_band, C, INK, INK2, AXIS
import definitions as D

INTER = ROOT / "data_intermediate"
TU = "PE-BZ-RN09"
# AMW candidate id -> MapBiomas Amazonía Col 6 geocode(s) (checked by name, 2026-10-15)
COL6_GEOCODE = {"RAISG-434": [4443], "RAISG-512": [4442], "BR-TI-29801": [3770], "BR-TI-23001": [3731]}
SHORT = {"RAISG-434": "Amanã NF", "RAISG-512": "Tapajós APA", "BR-TI-29801": "Munduruku TI", "BR-TI-23001": "Kayapó TI"}
TWIN_COLS = [C["twin"], "#3e3290", "#a79ce6", "#8a7fd0"]          # violet family, fixed order by fit
SRC = ("MapBiomas Peru Col 4 rasters, v3 registry (Tambopata buffer zone) and MapBiomas Amazonía Col 6 (twins) before "
       "2019; Amazon Mining Watch new area (area-weighted) from 2019; operations rule R* (brazil_v2)")
DURING = list(range(D.PERIODS["during"][0], D.PERIODS["during"][1] + 1))


# DEPRECATED (kept only so the not-yet-migrated slides_figures.s08_twins does not crash): the v2 two-twin set and
# colours. New code uses slide_data() / control_select.twins(); the twin list is no longer hard-coded.
TWINS = {"RAISG-434": ("Amana National Forest", 4443), "RAISG-512": ("Tapajos protection area", 4442)}
TCOL = {"Amana National Forest": C["twin"], "Munduruku territory": "#a79ce6", "Tapajos protection area": "#3e3290"}


def slide_data(count_unverified=False) -> dict:
    """Everything a slide needs, from the ONE twin rule: ids, short names, colours, pre-2019 index (Tambopata from the
    Peru Col 4 raster registry, twins from Amazonía Col 6), 2019-21 AMW paces, and the largest pre-trend slope p."""
    import control_select as cs
    w = pd.read_csv(INTER / "amw_candidates_year.csv").pivot(index="unit_id", columns="year", values="new_ha").fillna(0)
    m = pd.read_csv(INTER / "mb_amazonia_col6_mining.csv")
    ids, _ = cs.twins(count_unverified)
    idx = {TU: cs.tambopata_index(2009, 2023)}
    for uid in ids:
        s = twin_index(uid, m)
        if s is not None:
            idx[uid] = s
    I = pd.DataFrame(idx).loc[2009:2023]
    t = tests(w, I, [i for i in ids if i in I])
    return dict(ids=ids, short={TU: "Tambopata BZ", **{u: SHORT.get(u, u) for u in ids}},
                color={TU: C["lapampa"], **{u: TWIN_COLS[k % len(TWIN_COLS)] for k, u in enumerate(ids)}},
                index=I, pace={u: 100 * w.loc[u, DURING].mean() / w.loc[u, 2018] for u in [TU] + ids},
                pretrend_p_max=float(t.pre_trend_p.max()), tests=t,
                source_index="MapBiomas Peru Col 4 rasters, v3 registry (Tambopata) / MapBiomas Amazonía Col 6 (twins)",
                source_pace="Amazon Mining Watch new area, area-weighted (comparable to first-time mining, not net)")


def twin_index(uid, m):
    gc = COL6_GEOCODE.get(uid)
    s = m[m.geocode.isin(gc)].groupby("year").mining_ha.sum() if gc else pd.Series(dtype=float)
    return 100 * s / s.loc[D.REF_YEAR] if len(s) else None


def tests(w, I, ids):
    import statsmodels.api as sm
    from scipy import stats
    gr = np.log(I).diff().loc[2010:D.REF_YEAR]
    sh_t = 100 * w.loc[TU, DURING] / w.loc[TU, 2018]
    rows = []
    for uid in ids:
        dg = (gr[TU] - gr[uid]).dropna()
        r1 = sm.OLS(dg, np.ones(len(dg))).fit(cov_type="HAC", cov_kwds={"maxlags": 1})
        r2 = sm.OLS(dg, sm.add_constant(np.arange(len(dg)))).fit(cov_type="HAC", cov_kwds={"maxlags": 1})
        sh_c = 100 * w.loc[uid, DURING] / w.loc[uid, 2018]
        tt = stats.ttest_ind(sh_t.values, sh_c.values, equal_var=False)
        rows.append(dict(unit_id=uid, twin=SHORT.get(uid, uid), pre_growth_diff=r1.params.iloc[0],
                         pre_growth_p=r1.pvalues.iloc[0], pre_trend_slope=r2.params.iloc[1], pre_trend_p=r2.pvalues.iloc[1],
                         tam_during=sh_t.mean(), twin_during=sh_c.mean(), during_gap=sh_t.mean() - sh_c.mean(),
                         during_p=tt.pvalue))
    return pd.DataFrame(rows)


def run(reg):
    import control_select as cs
    print("\n== Rule-based twins, pooled (rule R*) ==")
    w = pd.read_csv(INTER / "amw_candidates_year.csv").pivot(index="unit_id", columns="year", values="new_ha").fillna(0)
    m = pd.read_csv(INTER / "mb_amazonia_col6_mining.csv")
    ids, _ = cs.twins()
    ids_s, _ = cs.twins(count_unverified=True)
    ids = [i for i in ids if i in COL6_GEOCODE] + [i for i in ids if i not in COL6_GEOCODE]
    missing = [i for i in ids if i not in COL6_GEOCODE]
    if missing:
        warnings.warn(f"control_top3: no Col 6 geocode for twins {missing}; pre-2019 test skipped for them")
    idx = {TU: cs.tambopata_index(2009, 2023)}
    for uid in ids:
        s = twin_index(uid, m)
        if s is not None:
            idx[uid] = s
    I = pd.DataFrame(idx).loc[2009:2023]
    t = tests(w, I, [i for i in ids if i in I])
    pace = {uid: 100 * w.loc[uid, DURING].mean() / w.loc[uid, 2018] for uid in ids}
    tam_d = 100 * w.loc[TU, DURING].mean() / w.loc[TU, 2018]
    pooled = float(np.mean(list(pace.values())))
    pooled_s = float(np.mean([pace[i] for i in ids_s])) if ids_s else np.nan
    t.round(4).to_csv(OUT / "control_top3_tests.csv", index=False)
    print("twins (R*):", ids, " sensitivity (unverified counts):", ids_s)
    print(t.round(3).to_string(index=False))
    per = f"{DURING[0]}-{DURING[-1]}"
    kw = dict(measure="amw_pace", zone="tambopata_bz", period=per)
    for _, r in t.iterrows():
        key = r.twin.split()[0].lower().replace("ã", "a").replace("á", "a").replace("ó", "o")
        for c in ("pre_growth_diff", "pre_growth_p", "pre_trend_p", "twin_during", "during_gap"):
            pre = c.startswith("pre")
            reg.add(f"top3_{key}_{c}", r[c], "p-value" if c.endswith("_p") else ("log points/yr" if "growth" in c else
                    "% of 2018 AMW area"), f"Twin {r.twin}: {c} " + ("(2010-18 log growth of the mining-area index, Peru "
                    "Col 4 raster vs Amazonía Col 6)" if pre else f"(AMW new area, % of own 2018 AMW area, {per})"),
                    "description", SRC, measure="stock" if pre else "amw_pace", zone="tambopata_bz",
                    period="2010-2018" if pre else per)
    reg.add("top3_n_twins", len(ids), "count", "Rule-based twins under rule R* (pass all rules with R2b)", "description", SRC)
    reg.add("top3_n_twins_excl_unverified", len(ids_s), "count", "Sensitivity: twins if an unverified report makes an "
            "area 'unclear'", "description", SRC)
    reg.add("top3_tam_during", tam_d, "% of 2018 AMW area", f"Tambopata BZ AMW new area per year {per}, % of own 2018 "
            "AMW area (comparable to first-time mining, not to net additions)", "description", SRC, **kw)
    reg.add("top3_pooled_during", pooled, "% of 2018 AMW area", f"Mean of the {len(ids)} twins' paces, same measure",
            "description", SRC, **kw)
    reg.add("top3_ratio", tam_d / pooled, "ratio", f"HEADLINE: Tambopata's {per} pace as a share of the mean of the "
            f"{len(ids)} rule-based twins' paces (AMW; description, never 'share of its counterfactual')",
            "description", SRC, **kw)
    reg.add("top3_ratio_excl_unverified", tam_d / pooled_s, "ratio", f"Sensitivity: same, twins excluding areas with an "
            f"unverified report ({len(ids_s)} twins)", "description", SRC, **kw)
    reg.add("top3_ratio_min", min(tam_d / v for v in pace.values()), "ratio", "Lowest Tambopata/twin pace ratio across twins",
            "description", SRC, **kw)
    reg.add("top3_ratio_max", max(tam_d / v for v in pace.values()), "ratio", "Highest Tambopata/twin pace ratio across twins",
            "description", SRC, **kw)
    reg.add("top3_below_all", float(all(tam_d < v for v in pace.values())), "flag",
            f"1 = Tambopata below every twin in {per}", "description", SRC, **kw)
    figure(I, w, ids, pace, tam_d, pooled)
    return t


def figure(I, w, ids, pace, tam_d, pooled):
    n = len(ids)
    word = {1: "The twin", 2: "Both twins"}.get(n, f"All {n} twins")
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(9, 4.6), gridspec_kw={"wspace": 0.6})
    headline(fig, f"{word} added AMW new area faster than Tambopata in {DURING[0]}–{str(DURING[-1])[2:]}",
             "Left: mining area (stock), index 2018 = 100, each from its own MapBiomas collection. Right: AMW new area\n"
             "per year, % of own 2018 AMW area (comparable to first-time mining, not to net additions).")
    col = {TU: C["lapampa"], **{u: TWIN_COLS[k % len(TWIN_COLS)] for k, u in enumerate(ids)}}
    short = {TU: "Tambopata BZ", **{u: SHORT.get(u, u) for u in ids}}

    def spread(ax, items, gap):
        items = sorted(items, key=lambda e: e[1]); ys = [e[1] for e in items]
        for j in range(1, len(ys)):
            ys[j] = max(ys[j], ys[j - 1] + gap)
        for (x, y, lab), yy in zip(items, ys):
            ax.annotate(lab, xy=(x, y), xytext=(x + 0.35 * (ax.get_xlim()[1] - ax.get_xlim()[0]) / 12, yy), textcoords="data",
                        va="center", fontsize=7.5, color=INK, fontweight="semibold", annotation_clip=False,
                        arrowprops=dict(arrowstyle="-", color=AXIS, lw=0.6, shrinkA=0, shrinkB=3))
    for c in I.columns:
        a1.plot(I.index, I[c], color=col[c], lw=2.4 if c == TU else 1.8, zorder=4 if c == TU else 3)
    a1.axvline(D.REF_YEAR + 0.5, color=INK, lw=1); a1.axhline(100, color=AXIS, lw=0.8); style_axes(a1)
    a1.set_xlim(2008.6, 2023.4); a1.set_ylim(0, I.max().max() * 1.08)
    spread(a1, [(I.index[-1], I[c].dropna().iloc[-1], short[c]) for c in I.columns], 0.08 * a1.get_ylim()[1])
    a1.set_ylabel("Index, 2018 = 100"); a1.set_xticks(range(2009, 2024, 3))
    a1.set_title("Mining area, 2009–2023 (two collections)", pad=8)
    yrs = list(range(D.FIRST_POST, 2026))
    period_band(a2, DURING[0] - 0.5, DURING[-1] + 0.5, "Mercurio and what\nfollowed (2019–21)")
    sh = {TU: 100 * w.loc[TU, yrs] / w.loc[TU, 2018], **{u: 100 * w.loc[u, yrs] / w.loc[u, 2018] for u in ids}}
    for u, ser in sh.items():
        a2.plot(yrs, ser.values, "-", color=col[u], lw=2.4 if u == TU else 1.8, zorder=3)
        a2.plot(yrs, ser.values, "o", color=col[u], ms=4, mec="white", mew=0.8, zorder=4)
    style_axes(a2); a2.set_xlim(2018.6, 2025.4)
    a2.set_ylim(0, max(float(v.max()) for v in sh.values()) * 1.1)
    spread(a2, [(2025, float(v.iloc[-1]), short[k]) for k, v in sh.items()], 0.08 * a2.get_ylim()[1])
    a2.text(0.97, 0.6, f"2019–21 mean pace\nTambopata: {tam_d:.0f}%\ntwins’ mean: {pooled:.0f}%", transform=a2.transAxes,
            ha="right", va="center", fontsize=7.5, color=INK2, linespacing=1.3)
    a2.set_ylabel("% of own 2018 AMW area"); a2.set_xticks(yrs); a2.set_xticklabels([f"'{str(y)[2:]}" for y in yrs])
    a2.set_title("AMW new area, 2019–2025", pad=8)
    finish_figure(fig, f"{SRC}. Left: each line from its own collection, side by side, never subtracted; Tambopata's "
                       "growth was converging on the twins' before 2019 (not parallel). Right: 2025 provisional; twins "
                       "had their own operations from 2023. Twins pass all rules if verified operations after 2021 are "
                       "allowed. Description.", OUT / "fig_control_top3.png")
