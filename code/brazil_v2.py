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
DESCRIPTION; few treated territories; operation searches cover 2021-2025 only.
"""
from __future__ import annotations
import warnings
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pyfixest as pf

from common import ROOT, OUT, style_axes, finish_figure
import checks
import brazil_raster as br

INTER = ROOT / "data_intermediate"
SRC = "MapBiomas Brazil Collection 11 rasters (class 30 mining) x FUNAI territories; operations: data_intermediate/operations_coded.csv"


def load():
    d = pd.read_csv(br.OUT_CSV)
    ops = pd.read_csv(INTER / "operations_coded.csv").set_index("unit_id")
    first = {}
    for uid in d.unit_id.unique():
        if uid in ops.index and ops.loc[uid, "verdict_2017_2025"] == "yes":
            fo = str(ops.loc[uid, "first_op_2021_2025"])          # first operation INSIDE 2021-2025 (fix: Kayapo 2024-09)
            if fo[:4].isdigit() and int(fo[:4]) >= 2021:
                first[uid] = int(fo[:4]) + (1 if int(fo[5:7]) >= 7 else 0)   # operation in H2 -> first treated year = next year
    # Sai-Cinza follows Munduruku (same complex; Op. Mundurukania 2021)
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
    reg.add("brv2_twfe_treat_p", twfe.pvalue()["treat"], "p-value", "TWFE p-value (clustered by territory)", "description", SRC)
    reg.add("brv2_did2s_treat", g[0], "log points", "Two-stage DiD (Gardner), same outcome", "description", SRC)
    reg.add("brv2_did2s_treat_p", g[2], "p-value", "did2s p-value", "description", SRC)
    reg.add("brv2_ri_p", pval, "p-value", "Randomization inference: share of 2,000 shuffles of operation dates/territories with an effect <= the real one", "description", SRC)
    reg.add("brv2_n_units", p.unit_id.nunique(), "count", "Territories in the Brazil panel", "description", SRC)
    reg.add("brv2_n_treated", int((p.groupby("unit_id").first_treat.first() > 0).sum()), "count", "Territories with an operation 2021-2025", "description", SRC)
    print(f"TWFE {twfe.coef()['treat']:.3f} (p {twfe.pvalue()['treat']:.3f}); did2s {g[0]:.3f} (p {g[2]:.3f}); RI p {pval:.3f}")
    # B2 figure: first-time mining and old pits, four treated territories + pool
    w = d.pivot_table(index="year", columns="unit", values="new_land_ha").loc[2010:2025]
    r = d.pivot_table(index="year", columns="unit", values="remined_ha").loc[2010:2025]
    show = [("Yanomami", 2023 + 1 / 12), ("Munduruku", 2021 + 4 / 12), ("Kayapó", 2024 + 8 / 12), ("Sararé", 2024 + 8 / 12)]
    fig, axes = plt.subplots(1, 4, figsize=(13, 3.8), sharex=True)
    for ax, (nm, op) in zip(axes, show):
        ax.bar(w.index, w[nm], color="#3d3c39", width=0.75, label="First-time mining")
        ax.bar(r.index, r[nm], bottom=w[nm], color="#b9b8b2", width=0.75, label="Return to old pits")
        ax.axvline(op - 0.5, color="black", lw=1.4)
        ax.set_title(nm, loc="left", fontsize=9.5); style_axes(ax)
        ax.set_xticks(range(2010, 2026, 3)); ax.tick_params(axis="x", labelsize=7.5)
    axes[0].set_ylabel("ha per year"); axes[0].legend(fontsize=7.5, frameon=False, loc="upper left")
    fig.suptitle(f"Brazil, same pixel method as Peru: falls after operations (staggered DiD {twfe.coef()['treat']:+.2f} log points, "
                 f"randomization p = {pval:.2f})", x=0.01, ha="left", fontsize=10.5, fontweight="bold")
    finish_figure(fig, f"Source: {SRC}. Black line = the territory's own first operation. Description.",
                  OUT / "fig_brazil_v2_pixels.png", rect_bottom=0.12)
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
