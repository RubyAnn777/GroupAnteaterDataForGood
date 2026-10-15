"""Brazil v2: the same pixel method as Peru (MapBiomas Brazil Col 11 rasters, brazil_raster.py) + statistical tests.

  B1 Check: Kayapo mining 2024 / 2025 vs the MapBiomas platform (Collection 11, FUNAI 2026): 17,632 / 18,573 ha.
  B2 First-time mining and returns to old pits per territory, 2010-2025, with each territory's own operation date.
  B3 Staggered difference-in-differences (territory-year panel, 2014-2025): territory and year fixed effects;
     treated after its own first operation (data_intermediate/operations_coded.csv). Estimators: TWFE and the
     two-stage DiD of Gardner (did2s, robust to staggered timing); errors clustered by territory.
     Outcome: log(1 + first-time mining ha).
  B4 Randomization inference: shuffle the operation years across the treated territories (and assign the actual
     dates to random territories) 2,000 times; p = share of shuffles with an effect at least as negative.
  B5 Displacement next door: Yanomami rings 0-10 km and 10-25 km outside the border, before vs after Feb 2023,
     relative to the no-operation pool.
DESCRIPTION; few treated territories; operation searches cover 2021-2025 only. One date per territory: first_operations().
"""
from __future__ import annotations
import warnings
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pyfixest as pf

from common import ROOT, OUT, style_axes, finish_figure, headline, label_end, C, INK, INK2, MUTED, AXIS
import checks
import brazil_raster as br

INTER = ROOT / "data_intermediate"
SRC = "MapBiomas Brazil Collection 11 rasters (class 30 mining) x FUNAI territories; operations: data_intermediate/operations_coded.csv"


# ONE treatment date per territory for the whole package (brazil_v2 and brazil_stagger), referee C9, 13 Oct 2026.
# RULE: the first VERIFIED operation inside the systematic search window 2021-2025 (operations_coded.csv, column
# first_op_2021_2025, verdict "yes"). Earlier operations (Kayapo Oct 2017, a 3-day Ibama raid) are listed but not
# coded as treatment: before 2021 no territory was searched, so coding the one we stumbled on would be asymmetric.
# Operations known only from search snippets do not count; the next verified one does:
UNVERIFIED = {   # unit_id: (unverified first operation, first verified operation in the window, reason)
    "BR-TI-29801": ("2021-05", "2023-08", "Op. Mundurukania May 2021 from search snippets only; Ibama from 2023-08-10"),
    "BR-TI-40901": ("2021-05", "2023-08", "Sai-Cinza: same Munduruku complex, May 2021 snippet only; dated with Munduruku"),
}
OTHER_OPS = {"BR-TI-23001": ("2017-10", "Ibama 3-day raid, before the 2021-25 search window")}   # shown, not coded
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def first_operations() -> pd.Series:
    """unit_id -> 'YYYY-MM' of the first verified operation 2021-2025 (the package-wide rule above)."""
    ops = pd.read_csv(INTER / "operations_coded.csv").set_index("unit_id")
    out = {}
    for uid, r in ops.iterrows():
        fo = str(r["first_op_2021_2025"])
        if r["verdict_2017_2025"] != "yes" or not fo[:4].isdigit() or int(fo[:4]) < 2021:
            continue
        out[uid] = UNVERIFIED[uid][1] if uid in UNVERIFIED else fo[:7]
    return pd.Series(out)


def month_label(ym: str) -> str:
    return f"{MONTHS[int(ym[5:7]) - 1]} {ym[:4]}"


def first_treat_year(ym: str) -> int:
    """Annual panel: an operation in Jan-Jun treats that year; Jul-Dec treats the next year (first full exposure)."""
    return int(ym[:4]) + (1 if int(ym[5:7]) >= 7 else 0)


def load():
    d = pd.read_csv(br.OUT_CSV)
    fo = first_operations()
    first = {uid: first_treat_year(fo[uid]) for uid in d.unit_id.unique() if uid in fo.index}
    d["first_treat"] = d.unit_id.map(first).fillna(0).astype(int)
    return d


def did(d, outcome="ln_new"):
    p = d[d.year.between(2014, 2025) & ~d.unit_id.str.startswith("Yanomami_ring")].copy()
    p["ln_new"] = np.log1p(p.new_land_ha.fillna(0))
    p["treat"] = ((p.first_treat > 0) & (p.year >= p.first_treat)).astype(int)
    twfe = pf.feols(f"{outcome} ~ treat | unit_id + year", data=p, vcov={"CRV1": "unit_id"})
    try:
        g = pf.did2s(p, yname=outcome, first_stage="~ 0 | unit_id + year", second_stage="~ treat", treatment="treat",
                     cluster="unit_id")
        g_coef, g_se, g_p = g.coef()["treat"], g.se()["treat"], g.pvalue()["treat"]
    except Exception as e:
        warnings.warn(f"did2s failed: {e}"); g_coef = g_se = g_p = np.nan
    return p, twfe, (g_coef, g_se, g_p)


def ri(p, reps=2000, seed=0):
    rng = np.random.default_rng(seed)
    real = pf.feols("ln_new ~ treat | unit_id + year", data=p).coef()["treat"]
    units = p.unit_id.unique(); fts = p.groupby("unit_id").first_treat.first()
    treated_dates = fts[fts > 0].values
    sims = []
    for _ in range(reps):
        fake = pd.Series(0, index=units)
        fake[rng.choice(units, size=len(treated_dates), replace=False)] = rng.permutation(treated_dates)
        q = p.assign(treat=((p.unit_id.map(fake) > 0) & (p.year >= p.unit_id.map(fake))).astype(int))
        sims.append(pf.feols("ln_new ~ treat | unit_id + year", data=q).coef()["treat"])
    sims = np.array(sims)
    return real, float((sims <= real).mean()), sims


def run(reg):
    print("\n== Brazil v2 (raster) ==")
    if not br.OUT_CSV.exists():
        warnings.warn("brazil_v2: brazil_raster_unit_year.csv missing; skipping"); return
    d = load()
    k = d[d.unit == "Kayapó"].set_index("year").mining_ha
    checks.check("MapBiomas Brazil Col 11 raster: Kayapo mining 2024, ha (platform 17,632)", k[2024], 17632, tol=400)
    checks.check("MapBiomas Brazil Col 11 raster: Kayapo mining 2025, ha (platform 18,573)", k[2025], 18573, tol=400)
    checks.save()
    for y in (2024, 2025):
        reg.add(f"brv2_kayapo_check_{y}", k[y], "ha", f"Kayapo mining {y}, Col 11 raster x FUNAI polygon (platform: {17632 if y == 2024 else 18573})", "description", SRC)
    p, twfe, g = did(d)
    real, pval, sims = ri(p)
    reg.add("brv2_twfe_treat", twfe.coef()["treat"], "log points", "Staggered DiD (TWFE), log(1+first-time mining), territory+year FE, 2014-2025", "description", SRC)
    reg.add("brv2_twfe_treat_p", twfe.pvalue()["treat"], "p-value", "TWFE p-value, two-sided (clustered by territory)", "description", SRC)
    reg.add("brv2_did2s_treat", g[0], "log points", "Two-stage DiD (Gardner), same outcome", "description", SRC)
    reg.add("brv2_did2s_treat_p", g[2], "p-value", "did2s p-value, TWO-SIDED, cluster-robust by territory", "description", SRC)
    reg.add("brv2_ri_p", pval, "p-value", "Randomization inference, ONE-SIDED, on the TWFE estimate (not did2s): share of 2,000 shuffles of operation dates/territories with a TWFE effect <= the real one (a large p = no sign of a fall)", "description", SRC)
    reg.add("brv2_n_units", p.unit_id.nunique(), "count", "Territories in the Brazil panel", "description", SRC)
    ft = p.groupby("unit_id").first_treat.first()
    reg.add("brv2_n_treated", int((ft > 0).sum()), "count", "Territories with a first verified operation 2021-2025 (package-wide rule, brazil_v2.first_operations)", "description", SRC)
    ops = pd.read_csv(INTER / "operations_coded.csv").set_index("unit_id")["verdict_2017_2025"]
    never = ft.index[ft == 0]
    v = ops.reindex(never)
    reg.add("brv2_never_n", len(never), "count", "'Never-treated' territories in the Brazil panel (no verified operation 2021-2025)", "description", SRC)
    reg.add("brv2_never_n_searched", int(v.eq("none").sum()), "count", "... of which searched for operations (2022-2025) with none found", "description", SRC)
    reg.add("brv2_never_n_unclear", int(v.eq("unclear").sum()), "count", "... of which searched, status unclear (undated operation)", "description", SRC)
    reg.add("brv2_never_n_unsearched", int(v.isna().sum()), "count", "... of which never searched (not in operations_coded.csv): 'no operation found' is NOT 'no operation'", "description", SRC)
    reg.add("brv2_n_treated_2025", int((ft == 2025).sum()), "count", "Treated territories whose first treated year is 2025 (one post year only)", "description", SRC)
    # sensitivity: Kayapo coded from its Oct 2017 raid (first treated 2018) instead of the 2021-25 rule
    pk = p.assign(first_treat=np.where(p.unit_id == "BR-TI-23001", 2018, p.first_treat))
    pk["treat"] = ((pk.first_treat > 0) & (pk.year >= pk.first_treat)).astype(int)
    tk = pf.feols("ln_new ~ treat | unit_id + year", data=pk, vcov={"CRV1": "unit_id"})
    reg.add("brv2_twfe_treat_kay2017", tk.coef()["treat"], "log points", "Sensitivity: TWFE with Kayapo treated from 2018 (its Oct 2017 raid) instead of 2025", "description", SRC)
    reg.add("brv2_twfe_treat_kay2017_p", tk.pvalue()["treat"], "p-value", "Sensitivity TWFE p-value, two-sided (clustered by territory)", "description", SRC)
    print(f"TWFE {twfe.coef()['treat']:.3f} (p {twfe.pvalue()['treat']:.3f}); did2s {g[0]:.3f} (p {g[2]:.3f}); RI p {pval:.3f}")
    # B2 figure: first-time mining and old pits, four treated territories + pool
    w = d.pivot_table(index="year", columns="unit", values="new_land_ha").loc[2010:2025]
    r = d.pivot_table(index="year", columns="unit", values="remined_ha").loc[2010:2025]
    fo = first_operations()
    uid = d.drop_duplicates("unit").set_index("unit").unit_id
    show = ["Yanomami", "Munduruku", "Kayapó", "Sararé"]
    fig, axes = plt.subplots(2, 2, figsize=(9, 6.2), sharex=True, gridspec_kw={"hspace": 0.55, "wspace": 0.25})
    axes = axes.ravel()
    headline(fig, "Brazil: mining did not fall right after each territory’s own operation",
             f"Mined land per year, ha (first-time mining + returns to old pits). Two-stage DiD {g[0]:+.2f} log points "
             f"(p = {g[2]:.2f}, two-sided); randomization p = {pval:.2f} (one-sided).")
    for i, (ax, nm) in enumerate(zip(axes, show)):
        ax.bar(w.index, w[nm], color=C["lapampa"], width=0.75)
        ax.bar(r.index, r[nm], bottom=w[nm], color=C["lapampa_tint"], width=0.75)
        ax.bar(w.index, [0] * len(w), bottom=w[nm], color="white", width=0.75, edgecolor="white", linewidth=1.0)
        ax.set_ylim(0, float((w[nm] + r[nm]).max()) * 1.22)
        u_ = uid[nm]
        lines = [(first_treat_year(fo[u_]) - 0.5, month_label(fo[u_]), True)]          # the coded treatment
        if u_ in UNVERIFIED:
            lines.append((first_treat_year(UNVERIFIED[u_][0]) - 0.5, month_label(UNVERIFIED[u_][0]) + "\n(unverified)", False))
        if u_ in OTHER_OPS:
            lines.append((first_treat_year(OTHER_OPS[u_][0]) - 0.5, month_label(OTHER_OPS[u_][0]) + "\n(3-day raid)", False))
        for x_, lab, coded in lines:
            ax.axvline(x_, color=INK if coded else AXIS, lw=1.1 if coded else 0.9, ls="-" if coded else (0, (3, 2)))
            ax.annotate(lab, xy=(x_, 1), xycoords=("data", "axes fraction"), xytext=(-4, -3),
                        textcoords="offset points", ha="right", va="top", fontsize=7.5, color=INK2 if coded else MUTED,
                        linespacing=1.1)
        ax.set_title(nm, pad=6); style_axes(ax)
        ax.set_xticks(range(2010, 2026, 3)); ax.set_xticklabels([f"'{str(y)[2:]}" for y in range(2010, 2026, 3)])
    from matplotlib.patches import Patch
    axes[1].legend(handles=[Patch(color=C["lapampa"], label="First-time mining"), Patch(color=C["lapampa_tint"], label="Return to old pits")],
                   loc="upper left", fontsize=8, frameon=False, handlelength=1.0, handleheight=0.9)
    axes[0].set_ylabel("ha per year"); axes[2].set_ylabel("ha per year")
    finish_figure(fig, f"{SRC}. Black line = the territory’s own first verified operation 2021–25, drawn before its first treated "
                       "year (Jan–Jun: that year; Jul–Dec: the next year). Dashed grey = earlier operations not coded as treatment. "
                       "Description.", OUT / "fig_brazil_v2_pixels.png")
    # B5 rings
    ring = d[d.unit.str.startswith("Yanomami ring")].pivot_table(index="year", columns="unit", values="new_land_ha")
    pre, post = ring.loc[2019:2022].mean(), ring.loc[2023:2025].mean()
    for u in ring.columns:
        key = "r0_10" if "0-10" in u else "r10_25"
        reg.add(f"brv2_{key}_pre", pre[u], "ha/yr", f"{u}: first-time mining per year 2019-22", "description", SRC)
        reg.add(f"brv2_{key}_post", post[u], "ha/yr", f"{u}: first-time mining per year 2023-25", "description", SRC)
    y = w["Yanomami"]
    reg.add("brv2_yan_new_2019_22", y.loc[2019:2022].mean(), "ha/yr", "Yanomami first-time mining per year 2019-22", "description", SRC)
    reg.add("brv2_yan_new_2023_25", y.loc[2023:2025].mean(), "ha/yr", "Yanomami first-time mining per year 2023-25", "description", SRC)
    reg.add("brv2_yan_remined_2023_25", r["Yanomami"].loc[2023:2025].mean(), "ha/yr", "Yanomami returns to old pits per year 2023-25", "description", SRC)
    d.round(2).to_csv(OUT / "brazil_v2_unit_year.csv", index=False)
    return d
