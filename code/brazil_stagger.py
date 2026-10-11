"""Brazil, more effort: staggered operations across indigenous territories, measured ONE way (Amazon Mining Watch).

Why AMW here: it is one uniform source for every territory and runs to 2025 (MapBiomas per territory stops in 2024).
Operations differ by territory and year (hand-coded from opened sources in data_intermediate/operations_coded.csv;
searches: docs/overnight/notes/brazil_ti_interventions.csv). That staggering is the design:
  * if operations cause the falls, each territory should fall AFTER its own operation, not before;
  * territories with no dated operation show what happened without one (the 'no-operation pool').
Groups: Yanomami (Feb 2023), Munduruku complex = Munduruku + Sai-Cinza (Ibama Aug 2023; removal Nov 2024),
Kayapó (Sep 2024; removal May 2025), Sararé (Sep 2024), pool = Brazilian territories with AMW mining and no operation
dated 2022-2025 in our searches (not searched is NOT the same as none: caveat).
Outcome: AMW new mining area by first-detection year, 2019-2025 (2025 provisional; 2018 = stock, excluded).
Comparison per operation: ln(mean of op year..2025) - ln(mean of the 3 years before), treated minus pool, same years.
All DESCRIPTION: few treated territories, no standard errors, operations searched only 2022-2025.
"""
from __future__ import annotations
import warnings
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from matplotlib.lines import Line2D

from common import ROOT, OUT, style_axes, finish_figure

INTER = ROOT / "data_intermediate"
SRC = ("Amazon Mining Watch (Earth Genome) patches x FUNAI territories (data_intermediate/amw_candidates_*.csv); "
       "operations: data_intermediate/operations_coded.csv")
GROUPS = {"Yanomami": ["BR-TI-50901"], "Munduruku + Sai-Cinza": ["BR-TI-29801", "BR-TI-40901"],
          "Kayapó": ["BR-TI-23001"], "Sararé": ["BR-TI-42101"]}
OP = {"Yanomami": 2023 + 1 / 12, "Munduruku + Sai-Cinza": 2023 + 7 / 12, "Kayapó": 2024 + 8 / 12, "Sararé": 2024 + 8 / 12}
OP_YEAR = {k: int(v) for k, v in OP.items()}
POOL = "No operation found (pool)"
COL = {"Yanomami": "#eb6834", "Munduruku + Sai-Cinza": "#2a78d6", "Kayapó": "#1baf7a", "Sararé": "#6250d6", POOL: "#7d7c78"}   # dataviz reference palette, validated
YRS = list(range(2019, 2026))


def load():
    u = pd.read_csv(INTER / "amw_candidates_units.csv").set_index("unit_id")
    w = pd.read_csv(INTER / "amw_candidates_year.csv").pivot(index="year", columns="unit_id", values="new_ha")
    ops = pd.read_csv(INTER / "operations_coded.csv").set_index("unit_id")
    br = [c for c in w if c.startswith("BR-TI-")]
    in_groups = {c for v in GROUPS.values() for c in v}
    dated = {c for c in br if c in ops.index and ops.loc[c, "verdict_2017_2025"] == "yes"
             and str(ops.loc[c, "first_op_2017_2025"]) >= "2022"}
    pool = sorted(c for c in br if c not in in_groups and c not in dated)
    g = pd.DataFrame({k: w[v].sum(axis=1) for k, v in GROUPS.items()})
    g[POOL] = w[pool].sum(axis=1)
    return g.loc[YRS], u, pool, w


def stacked(g):
    rows = []
    for k, y in OP_YEAR.items():
        pre, post = list(range(y - 3, y)), list(range(y, 2026))
        lt = np.log(g.loc[post, k].mean() / g.loc[pre, k].mean())
        lp = np.log(g.loc[post, POOL].mean() / g.loc[pre, POOL].mean())
        half = g.loc[2019:2021, k].mean() / 2
        below = [yy for yy in YRS if yy >= 2022 and g.loc[yy, k] < half]
        rows.append(dict(group=k, op_year=y, pre=f"{pre[0]}-{pre[-1]}", post=f"{post[0]}-{post[-1]}",
                         treated_pre=g.loc[pre, k].mean(), treated_post=g.loc[post, k].mean(),
                         treated_change_pct=100 * (np.exp(lt) - 1), pool_change_pct=100 * (np.exp(lp) - 1),
                         gap_log_points=lt - lp, first_year_below_half=below[0] if below else np.nan))
    return pd.DataFrame(rows)


def figure(g, s):
    fig, axes = plt.subplots(1, 5, figsize=(13, 3.9), sharex=True)
    for ax, k in zip(axes, list(GROUPS) + [POOL]):
        for y in YRS:
            prov = y == 2025
            ax.bar(y, g.loc[y, k], 0.75, color=COL[k], alpha=0.45 if prov else 1, hatch="///" if prov else None,
                   edgecolor=COL[k] if prov else "white", linewidth=0.5)
        ax.axvline(2022.5, color="#9aa5a8", ls="--", lw=0.9)          # Jan 2023: new federal government
        if k in OP:
            ax.axvline(OP[k] - 0.5, color="black", lw=1.4)             # bars sit on integer years; op month -> x
            ax.annotate("own\noperation", (OP[k] - 0.5, ax.get_ylim()[1] * 0.97), xytext=(3, 0), textcoords="offset points",
                        fontsize=7, va="top")
            r = s.set_index("group").loc[k]
            sub = f"after vs 3 yrs before: {r.treated_change_pct:+.0f}%"
        else:
            sub = f"2019: {g.loc[2019, k]:,.0f} ha; 2025: {g.loc[2025, k]:,.0f} ha"
        ax.set_title(f"{k}\n{sub}", loc="left", fontsize=8.5)
        style_axes(ax)
        ax.set_xticks(YRS); ax.set_xticklabels([f"'{str(y)[2:]}" for y in YRS], fontsize=7.5)
    axes[0].set_ylabel("New mining detected (ha)")
    fig.legend(handles=[Line2D([], [], color="black", lw=1.4, label="Territory's own operation (first dated)"),
                        Line2D([], [], color="#9aa5a8", ls="--", label="Jan 2023: new federal government"),
                        Patch(facecolor="#bbbbbb", hatch="///", edgecolor="#888888", label="2025 provisional")],
               loc="lower center", ncol=3, fontsize=8, frameon=False, bbox_to_anchor=(0.5, 0.1))
    fig.suptitle("Brazil: the big territories fell from 2022, Munduruku even before its operation; where no operation came, mining grew",
                 x=0.01, ha="left", fontsize=11, fontweight="bold")
    finish_figure(fig, f"Source: {SRC}. Y-axes differ. Pool = territories with mining and no operation dated 2022-25 in our "
                       "searches (not searched is not the same as none). AMW = mining scars on land; no river dredges. Description.",
                  OUT / "fig_brazil_stagger.png", rect_bottom=0.2, event_note=False)


def run(reg):
    print("\n== Brazil: staggered operations (AMW) ==")
    if not (INTER / "amw_candidates_year.csv").exists():
        warnings.warn("brazil_stagger: intermediates missing; skipping"); return
    g, u, pool, w = load()
    s = stacked(g)
    g.round(1).to_csv(OUT / "brazil_stagger_amw.csv")
    s.round(3).to_csv(OUT / "brazil_stagger_summary.csv", index=False)
    print(g.round(0).to_string()); print(s.round(2).to_string(index=False))
    for _, r in s.iterrows():
        k = {"Yanomami": "yan", "Munduruku + Sai-Cinza": "mun", "Kayapó": "kay", "Sararé": "sar"}[r.group]
        reg.add(f"bs_{k}_change_pct", r.treated_change_pct, "percent",
                f"AMW new mining {r.group}: mean {r.post} vs mean {r.pre} (operation year {r.op_year})", "description", SRC)
        reg.add(f"bs_{k}_pool_change_pct", r.pool_change_pct, "percent",
                f"Same windows, no-operation pool ({len(pool)} territories)", "description", SRC)
        reg.add(f"bs_{k}_gap_logpts", r.gap_log_points, "log points", f"{r.group} minus pool, ln change", "description", SRC)
        if not np.isnan(r.first_year_below_half):          # Sarare never fell below half: no number
            reg.add(f"bs_{k}_first_below_half", r.first_year_below_half, "year",
                    f"First year from 2022 with AMW new area below half the 2019-21 mean, {r.group}", "description", SRC)
    for y in (2019, 2022, 2023, 2024, 2025):
        reg.add(f"bs_pool_new_ha_{y}", g.loc[y, POOL], "ha", f"AMW new mining {y}, no-operation pool" +
                (" (PROVISIONAL)" if y == 2025 else ""), "description", SRC)
        for k, kk in (("Yanomami", "yan"), ("Sararé", "sar")):
            reg.add(f"bs_{kk}_new_ha_{y}", g.loc[y, k], "ha", f"AMW new mining {y}, {k}" + (" (PROVISIONAL)" if y == 2025 else ""),
                    "description", SRC)
    reg.add("bs_pool_n", len(pool), "count", "Territories in the no-operation pool", "description", SRC)
    top = w[pool].loc[2023:2025].sum().sort_values(ascending=False)
    reg.add("bs_pool_top_share_2023_25", top.iloc[0] / top.sum(), "share",
            f"Share of pool new mining 2023-25 in its largest territory ({u.loc[top.index[0], 'name']})", "description", SRC)
    figure(g, s)
    return s
