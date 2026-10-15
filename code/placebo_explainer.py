"""One picture of how our placebo tests work: the real result against the same analysis run where nothing happened.

Rows (all recomputed with the modules' own functions, so the numbers equal the ones in numbers.csv):
  1  Fake places, hectares (model M1): each of the other 14 buffer zones gets the "operation" in turn.
  2  Fake places, scaled to size (model M4): same, outcome in units of each zone's normal pre-2019 year.
  3  Fake start years at the road (T1): the north-of-road share's 3-year jump for every start year whose window
     doesn't touch 2016-21.
Rank of the real result among all = randomization p-value (rank / number of results). DESCRIPTION.
"""
from __future__ import annotations
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from common import OUT, finish_figure, headline, C, INK, INK2, MUTED, GRID, AXIS
import peru_models as pm
import raster_zones as rz
import v2_tests


def fake_places(pack, model):
    ad = pm._zone_adds(pack)
    gold = pack["prices"].set_index("year")["gold"]
    pre = ad.loc[2014:2018].mean()
    pool = sorted(u for u in ad.columns if ad.loc[2014:2018, u].abs().sum() > 0)
    if model == "M4":
        pool = [u for u in pool if pre[u] > 10]
    REAL = {"during": (2019, 2021), "after": (2022, 2025)}
    real = pm.fit(ad, pool, pm.TU, model, 2014, 2025, REAL, gold)["post_during"]
    fakes = {u: pm.fit(ad, [v for v in pool if v != pm.TU], u, model, 2014, 2025, REAL, gold)["post_during"]
             for u in pool if u != pm.TU}
    return real, pd.Series(fakes)


def fake_years():
    b = pd.read_csv(rz.OUT_BAND)
    w = b.pivot_table(index="year", columns="km_from_road", values="new_land_ha", aggfunc="sum").fillna(0)
    share = (w[[c for c in w if c >= 0]].sum(axis=1) / w.sum(axis=1)).loc[2005:2025]
    s, _, _ = v2_tests.shift_test(share)
    clean = s[(s.index <= 2013) | (s.index >= 2022) | (s.index == 2019)]
    return clean[2019], clean.drop(2019)


def run(pack, reg):
    rows = []
    r1, f1 = fake_places(pack, "M1"); rows.append(("Fake places, in hectares", "ha per year, 2019–21 gap", r1, f1, "low"))
    r4, f4 = fake_places(pack, "M4"); rows.append(("Fake places, scaled to each zone's size", "normal pre-2019 years", r4, f4, "low"))
    ry, fy = fake_years(); rows.append(("Fake start years at the road", "jump in the north-of-road share", ry, fy, "high"))
    fig, axs = plt.subplots(3, 1, figsize=(9, 5.6), gridspec_kw=dict(hspace=1.25))
    headline(fig, "A placebo asks: does the real result stand out from fakes?",
             "Same analysis, run where nothing happened. Grey = each fake, orange = the real one. "
             "Rank among all = p-value")
    for ax, (title, unit, real, fakes, tail) in zip(axs, rows):
        allv = pd.concat([fakes, pd.Series({"real": real})])
        rank = int((allv <= real).sum()) if tail == "low" else int((allv >= real).sum())
        n = len(allv)
        rng = np.random.default_rng(1)
        ax.scatter(fakes.values, rng.uniform(-0.18, 0.18, len(fakes)), s=34, color=C["other"], lw=0, zorder=2)
        ax.scatter([real], [0], s=80, color=C["lapampa"], lw=1.5, edgecolor="white", zorder=3)
        ax.annotate(f"real: rank {rank} of {n}  →  p = {rank / n:.2f}", (real, 0), xytext=(0, 13), textcoords="offset points",
                    ha="center", va="bottom", fontsize=8.5, color=INK, fontweight="semibold")
        ax.axvline(0, color=AXIS, lw=0.9, zorder=1)
        lo, hi = min(allv.min(), 0), max(allv.max(), 0)
        pad = (hi - lo) * 0.08
        ax.set_xlim(lo - pad, hi + pad); ax.set_ylim(-0.5, 0.75)
        ax.set_yticks([])
        for sp in ("top", "right", "left"): ax.spines[sp].set_visible(False)
        ax.xaxis.grid(True, color=GRID, lw=0.6); ax.set_axisbelow(True)
        ax.set_title(title, fontsize=10)
        ax.text(1.0, 1.08, unit, transform=ax.transAxes, ha="right", va="bottom", fontsize=8, color=INK2)
        fmt = (lambda v, p: f"{v:,.0f}".replace("-", "−")) if abs(hi - lo) > 20 else (lambda v, p: f"{v:,.1f}".replace("-", "−"))
        ax.xaxis.set_major_formatter(plt.FuncFormatter(fmt))
        key = {"Fake places, in hectares": "m1", "Fake places, scaled to each zone's size": "m4", "Fake start years at the road": "road"}[title]
        reg.add(f"plc_{key}_rank", rank, "rank", f"Rank of the real result among real + fakes, {title}", "description", "placebo_explainer.py")
        reg.add(f"plc_{key}_n", n, "count", f"Results compared (real + fakes), {title}", "description", "placebo_explainer.py")
    finish_figure(fig, "Sources: peru_bufferzone_year.csv (MapBiomas Peru Col 4) for rows 1–2; MapBiomas Peru Col 4 rasters "
                       "for row 3. Fake places: Tambopata removed from each fake's comparison pool. Fake start years: only "
                       "windows that don't touch 2016–21. Description.", OUT / "fig_placebo_explainer.png")


if __name__ == "__main__":
    from common import Numbers, load_pack
    reg = Numbers(); run(load_pack(), reg)
    print({k: v["value"] for k, v in reg.rows.items()})
