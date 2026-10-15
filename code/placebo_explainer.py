"""One picture of how our placebo tests work: the real result against the same analysis run where nothing happened.

Rows (all recomputed with the modules' own functions, so the numbers equal the ones in numbers.csv):
  1  Fake places, hectares (model M1, net additions): each other buffer zone gets the "operation" in turn. In hectares
     this ranks SIZE as much as effect (Tambopata is the biggest zone; it ranks first in pre-years too, see peru.py).
  2  Fake places, scaled to size (model M4, net additions / own 2014-18 mean): the size-free version of row 1.
  3  Fake start years at the road: the 3-year jump in the share of FIRST-TIME mining (new land) north of the road, for
     every start year whose windows do not touch 2016-21. A share of new land, not net additions: a share of a
     quantity that can be negative is not defined, so this row stays on new land and says so.
Rank = 1 + number of fakes at least as extreme as the real result (common.placebo_rank). It shows whether the real
result stands out from the fakes; with one treated zone it is not a significance test. DESCRIPTION.
"""
from __future__ import annotations
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from common import OUT, finish_figure, headline, C, INK, INK2, GRID, AXIS, placebo_rank
import definitions as D
import peru_models as pm
import raster_zones as rz
import v2_tests

SRC_Z = D.SOURCE
ROAD_K = 3                                        # years in each window of the road shift test


def fake_places(pack, model):
    """Real 2019-21 coefficient (net additions) and the fakes, Tambopata removed from each fake's pool."""
    ad = pm._zone_adds()
    gold = pack["prices"].set_index("year")["gold"]
    poolB, big, _, _ = pm.pools(ad)
    pool = big if model == "M4" else poolB
    real = pm.fit(ad, pool, pm.TU, model, *pm.EST, pm.REAL, gold)["post_during"]
    noT = [v for v in pool if v != pm.TU]
    fakes = {u: pm.fit(ad, noT, u, model, *pm.EST, pm.REAL, gold)["post_during"] for u in noT}
    return real, pd.Series(fakes)


def fake_years():
    """North-of-road share of first-time mining (new land), La Pampa longitudes; 3-year jump around each start year."""
    b = pd.read_csv(rz.OUT_BAND)
    w = b.pivot_table(index="year", columns="km_from_road", values="new_ha", aggfunc="sum").fillna(0)
    share = (w[[c for c in w if c >= 0]].sum(axis=1) / w.sum(axis=1)).loc[2005:D.YEARS[1]]
    s, _, _ = v2_tests.shift_test(share, real=D.FIRST_POST, k=ROAD_K)
    lo, hi = D.PERIODS["pre"][0], D.PERIODS["during"][1]          # windows must not touch 2016-21
    clean = s[(s.index + ROAD_K - 1 < lo) | (s.index - ROAD_K > hi) | (s.index == D.FIRST_POST)]
    return clean[D.FIRST_POST], clean.drop(D.FIRST_POST)


def run(pack, reg):
    rows = []
    r1, f1 = fake_places(pack, "M1")
    rows.append(("m1", "Fake places, in hectares (ranks size as much as effect)", "net additions, ha/yr, 2019–21 gap",
                 r1, f1, "low"))
    r4, f4 = fake_places(pack, "M4")
    rows.append(("m4", "Fake places, scaled to each zone's size", "net additions in normal pre-2019 years, 2019–21 gap",
                 r4, f4, "low"))
    ry, fy = fake_years()
    rows.append(("road", "Fake start years at the road", "jump in the north-of-road share of new land (first-time mining)",
                 ry, fy, "high"))
    fig, axs = plt.subplots(3, 1, figsize=(9, 5.8), gridspec_kw=dict(hspace=1.25))
    ranks = {}
    for key, title, unit, real, fakes, tail in rows:
        sgn = 1 if tail == "low" else -1
        ranks[key] = (placebo_rank(sgn * real, sgn * fakes.values), len(fakes) + 1)
    headline(fig, f"Tambopata stands out from fake places only in hectares (rank {ranks['m1'][0]} of {ranks['m1'][1]}); "
                  f"relative to size it ranks {ranks['m4'][0]} of {ranks['m4'][1]}",
             "Same analysis, run where nothing happened. Grey = each fake, orange = the real one. Rows 1–2: net mining "
             "additions, Peruvian buffer zones;\nrow 3: first-time mining near the Interoceanic Highway (La Pampa "
             "longitudes). Rank 1 = the real result is the most extreme.")
    for ax, (key, title, unit, real, fakes, tail) in zip(axs, rows):
        rank, n = ranks[key]
        allv = pd.concat([fakes, pd.Series({"real": real})])
        rng = np.random.default_rng(1)
        ax.scatter(fakes.values, rng.uniform(-0.18, 0.18, len(fakes)), s=34, color=C["other"], lw=0, zorder=2)
        ax.scatter([real], [0], s=80, color=C["lapampa"], lw=1.5, edgecolor="white", zorder=3)
        ax.annotate(f"real: rank {rank} of {n}", (real, 0), xytext=(0, 13), textcoords="offset points",
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
        meas, zone, per = (("net", D.TREATED_ZONE, D.period_label("during")) if key != "road"
                           else ("new", "road bands, La Pampa longitudes", f"start {D.FIRST_POST}, {ROAD_K}-year windows"))
        reg.add(f"plc_{key}_rank", rank, "rank", f"Rank of the real result among real + fakes (1 = most extreme), {title}; "
                f"{unit}", "description", "placebo_explainer.py", measure=meas, zone=zone, period=per)
        reg.add(f"plc_{key}_n", n, "count", f"Results compared (real + fakes), {title}", "description",
                "placebo_explainer.py")
    finish_figure(fig, f"Sources: {SRC_Z}. Fake places: Tambopata removed from each fake's comparison pool. Fake start "
                       "years: only windows that don't touch 2016–21. One treated zone: a rank shows whether the real result "
                       "stands out, it is not a significance test. Description.", OUT / "fig_placebo_explainer.png")


if __name__ == "__main__":
    from common import Numbers, load_pack
    reg = Numbers(); run(load_pack(), reg)
    print({k: v["value"] for k, v in reg.rows.items()})
