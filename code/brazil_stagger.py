"""Brazil (backup slides only): staggered operations across indigenous territories, measured with Amazon Mining Watch.

MEASURE: AMW new area (union of detected patches clipped to each territory, area-weighted; first detection year).
It is comparable to first-time mining, NOT to net additions, and is a different product from MapBiomas: never put in
one series with Collection 10.1 (brazil.py) or Collection 11 (brazil_v2.py, the Brazil headline in net additions).
Why AMW here at all: one uniform source for every territory, to 2025 (2025 provisional; 2018 = stock, excluded).
Dates: the ONE rule R* in brazil_v2 (first VERIFIED operation against mining 2021-25 from operations_coded.csv; Jan-Jun
treats that year, Jul-Dec the next; unverified snippets are context). Groups from brazil_v2.BRAZIL (Munduruku = the
complex Munduruku + Sai-Cinza). Removals of non-mining invaders (Apyterewa, Trincheira Bacaja) are dropped.
Comparison per operation: ln(mean of first treated year..2025) - ln(mean of the 3 years before), treated minus pool.
Pool = Brazilian territories with AMW mining, outside the groups, with no verified operation 2021-25. Most pool
territories were never searched ("not searched" is not "no operation"); the pool is reported with and without
Aripuana (AMW-only mining, unsearched, next to the Mar 2025 Golden Border targets; review card 12, D-S12-6).
Reading (card 12): the big territories boomed and then fell after 2022; operations arrived at the peak, and Munduruku
was already falling before its operation, so these data cannot separate the operations from the end of the boom.
All DESCRIPTION: few treated territories, no standard errors.
"""
from __future__ import annotations
import warnings
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from matplotlib.lines import Line2D

from common import ROOT, OUT, style_axes, finish_figure, headline, C, INK, INK2, MUTED, AXIS
from brazil_v2 import BRAZIL, first_verified, first_treat_year, month_label, non_mining_units, verdict

INTER = ROOT / "data_intermediate"
SRC = ("Amazon Mining Watch (Earth Genome) new area x FUNAI territories, area-weighted (data_intermediate/"
       "amw_candidates_*.csv); operations: data_intermediate/operations_coded.csv, rule R* (brazil_v2)")
MEASURE = "amw_new_area"
GROUPS = BRAZIL["groups"]
_FO = first_verified()
OP_YM = {k: _FO[BRAZIL["group_date"].get(k, v[0])] for k, v in GROUPS.items()}
OP_YEAR = {k: first_treat_year(v) for k, v in OP_YM.items()}          # R*: Jul-Dec -> next year
POOL = "No verified operation (pool)"
ARIPUANA = "Aripuanã"
COL = {"Yanomami": C["lapampa"], "Munduruku": C["corridor"], "Kayapó": C["buffer"], "Sararé": C["twin"], POOL: C["other"]}
YRS = list(range(2019, 2026))


def load():
    u = pd.read_csv(INTER / "amw_candidates_units.csv").set_index("unit_id")
    w = pd.read_csv(INTER / "amw_candidates_year.csv").pivot(index="year", columns="unit_id", values="new_ha").fillna(0)
    br = [c for c in w if c.startswith("BR-TI-") and c not in non_mining_units()]
    in_groups = {c for v in GROUPS.values() for c in v}
    pool = sorted(c for c in br if c not in in_groups and c not in _FO.index)
    g = pd.DataFrame({k: w[[c for c in v if c in w]].sum(axis=1) for k, v in GROUPS.items()})
    g[POOL] = w[pool].sum(axis=1)
    ari = [c for c in pool if u.loc[c, "name"] == ARIPUANA]
    g[POOL + " ex Aripuanã"] = w[[c for c in pool if c not in ari]].sum(axis=1)
    return g.loc[YRS], u, pool, w


def stacked(g):
    rows = []
    a0, a1 = BRAZIL["boom"][0], BRAZIL["boom"][0] + 2
    for k, y in OP_YEAR.items():
        pre, post = list(range(y - 3, y)), list(range(y, 2026))
        lt = np.log(g.loc[post, k].mean() / g.loc[pre, k].mean())
        lp = np.log(g.loc[post, POOL].mean() / g.loc[pre, POOL].mean())
        lx = np.log(g.loc[post, POOL + " ex Aripuanã"].mean() / g.loc[pre, POOL + " ex Aripuanã"].mean())
        half = g.loc[a0:a1, k].mean() / 2
        below = [yy for yy in YRS if yy >= 2022 and g.loc[yy, k] < half]
        rows.append(dict(group=k, op_year=y, pre=f"{pre[0]}-{pre[-1]}", post=f"{post[0]}-{post[-1]}",
                         treated_pre=g.loc[pre, k].mean(), treated_post=g.loc[post, k].mean(),
                         treated_change_pct=100 * (np.exp(lt) - 1), pool_change_pct=100 * (np.exp(lp) - 1),
                         pool_ex_aripuana_change_pct=100 * (np.exp(lx) - 1), gap_log_points=lt - lp,
                         gap_log_points_ex_aripuana=lt - lx, first_year_below_half=below[0] if below else np.nan))
    return pd.DataFrame(rows)


def figure(g, s):
    fig, axes = plt.subplots(1, 5, figsize=(13, 4.0), sharex=True)
    headline(fig, "Brazil: mining boomed, then fell after 2022; operations arrived at the peak",
             "AMW new area per year, ha (comparable to first-time mining, not to net additions), 2019–2025. Munduruku was "
             "already falling before its operation;\nthe pool is mostly unsearched territories and its rise is one "
             "territory (Aripuanã). Our data cannot separate the operations from the end of the boom.")
    for ax, k in zip(axes, list(GROUPS) + [POOL]):
        for y in YRS:
            prov = y == 2025
            ax.bar(y, g.loc[y, k], 0.75, color=COL[k], alpha=0.45 if prov else 1, hatch="///" if prov else None,
                   edgecolor=COL[k] if prov else "white", linewidth=0.5)
        if k == POOL:
            ax.bar(YRS, g.loc[YRS, POOL + " ex Aripuanã"], 0.75, color="none", edgecolor=INK2, hatch="....", lw=0)
        ax.axvline(int(BRAZIL["emergency"][:4]) - 0.5, color=AXIS, ls=(0, (3, 2)), lw=0.9)   # Jan 2023 (context)
        if k in OP_YEAR:
            ax.axvline(OP_YEAR[k] - 0.5, color=INK, lw=1.3)
            ax.annotate(month_label(OP_YM[k]), (OP_YEAR[k] - 0.5, 1), xycoords=("data", "axes fraction"),
                        xytext=(3, -3), textcoords="offset points", fontsize=7, va="top", color=INK2)
            r = s.set_index("group").loc[k]
            sub = f"3 yrs before → after: {r.treated_change_pct:+.0f}%"
        else:
            sub = f"2019: {g.loc[2019, k]:,.0f} ha; 2025: {g.loc[2025, k]:,.0f} ha"
        ax.set_title(f"{k}\n{sub}", loc="left", fontsize=8.5)
        style_axes(ax)
        ax.set_xticks(YRS); ax.set_xticklabels([f"'{str(y)[2:]}" for y in YRS], fontsize=7.5)
    axes[0].set_ylabel("AMW new area, ha")
    fig.legend(handles=[Line2D([], [], color=INK, lw=1.3, label="Territory's first verified operation (rule R*), drawn "
                               "before its first treated year"),
                        Line2D([], [], color=AXIS, ls="--", label="Jan 2023: Yanomami emergency, new federal government"),
                        Patch(facecolor="white", edgecolor=INK2, hatch="....", label="Pool without Aripuanã"),
                        Patch(facecolor="#bbbbbb", hatch="///", edgecolor="#888888", label="2025 provisional")],
               loc="lower center", ncol=2, fontsize=8, frameon=False, bbox_to_anchor=(0.5, 0.11))
    finish_figure(fig, f"Source: {SRC}. Y-axes differ. Pool = territories with AMW mining and no verified operation "
                       "2021-25; most were never searched (not searched is not the same as none). AMW = mining scars on "
                       "land; no river dredges. Description.", OUT / "fig_brazil_stagger.png", rect_bottom=0.24)


def _add(reg, id, v, desc, zone, period, unit="ha"):
    reg.add(id, v, unit, desc + ". Measure: AMW new area (comparable to first-time mining, not to net additions)",
            "description", SRC, measure=MEASURE, zone=zone, period=period)


def run(reg):
    print("\n== Brazil: staggered operations (AMW, rule R*) ==")
    if not (INTER / "amw_candidates_year.csv").exists():
        warnings.warn("brazil_stagger: intermediates missing; skipping"); return
    g, u, pool, w = load()
    s = stacked(g)
    g.round(1).to_csv(OUT / "brazil_stagger_amw.csv")
    s.round(3).to_csv(OUT / "brazil_stagger_summary.csv", index=False)
    print(g.round(0).to_string()); print(s.round(2).to_string(index=False))
    key = {"Yanomami": "yan", "Munduruku": "mun", "Kayapó": "kay", "Sararé": "sar"}
    for _, r in s.iterrows():
        k = key[r.group]
        per = f"{r.pre} vs {r.post}"
        reg.add(f"bs_{k}_change_pct", r.treated_change_pct, "percent",
                f"AMW new area {r.group}: mean {r.post} vs mean {r.pre} (first treated year {r.op_year}, rule R*)",
                "description", SRC, measure=MEASURE, zone=f"br_{k}", period=per)
        reg.add(f"bs_{k}_pool_change_pct", r.pool_change_pct, "percent",
                f"Same windows, pool ({len(pool)} territories, mostly unsearched)", "description", SRC,
                measure=MEASURE, zone="br_pool", period=per)
        reg.add(f"bs_{k}_pool_ex_aripuana_change_pct", r.pool_ex_aripuana_change_pct, "percent",
                "Same windows, pool without Aripuanã (AMW-only mining, unsearched)", "description", SRC,
                measure=MEASURE, zone="br_pool_ex_aripuana", period=per)
        reg.add(f"bs_{k}_gap_logpts", r.gap_log_points, "log points", f"{r.group} minus pool, ln change", "description",
                SRC, measure=MEASURE, zone=f"br_{k}", period=per)
        reg.add(f"bs_{k}_gap_logpts_ex_aripuana", r.gap_log_points_ex_aripuana, "log points",
                f"{r.group} minus pool without Aripuanã, ln change", "description", SRC, measure=MEASURE,
                zone=f"br_{k}", period=per)
        if not np.isnan(r.first_year_below_half):
            reg.add(f"bs_{k}_first_below_half", r.first_year_below_half, "year",
                    f"First year from 2022 with AMW new area below half the 2019-21 mean, {r.group}", "description", SRC)
    for y in (2019, 2022, 2023, 2024, 2025):
        prov = " (PROVISIONAL)" if y == 2025 else ""
        _add(reg, f"bs_pool_new_ha_{y}", g.loc[y, POOL], f"AMW new area {y}, pool{prov}", "br_pool", str(y))
        for k, kk in (("Yanomami", "yan"), ("Sararé", "sar")):
            _add(reg, f"bs_{kk}_new_ha_{y}", g.loc[y, k], f"AMW new area {y}, {k}{prov}", f"br_{kk}", str(y))
    reg.add("bs_pool_n", len(pool), "count", "Territories in the pool (AMW mining, no verified operation 2021-25)",
            "description", SRC)
    v = verdict(BRAZIL["dating_window"]).reindex(pool)
    reg.add("bs_pool_n_unsearched", int(v.isna().sum()), "count", "... of which never searched for operations",
            "description", SRC)
    top = w[pool].loc[2023:2025].sum().sort_values(ascending=False)
    reg.add("bs_pool_top_share_2023_25", top.iloc[0] / top.sum(), "share",
            f"Share of pool AMW new area 2023-25 in its largest territory ({u.loc[top.index[0], 'name']})", "description",
            SRC, measure=MEASURE, zone="br_pool", period="2023-2025")
    figure(g, s)
    return s
