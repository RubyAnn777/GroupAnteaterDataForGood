"""Peru core analysis (Operation Mercurio, Feb 2019), pack data only.

Everything here is MapBiomas Peru Collection 4, class 4.2 Minería (all mining, legal + illegal;
cannot see river dredging or mercury). Rules: annual ADDITIONS, aggregate first, buffer zones identified
by buffer_zone + pa_category, department work with biome == "Amazonía".

Units
  Tambopata BZ (targeted), Amarakaeri BZ (main comparison), Bahuaja-Sonene BZ, "rest of Madre de Dios", MdD total.
  A buffer zone is summed over ALL departments it touches (the starter's definition, reproduces the card:
  1,640 -> 163 and 289 -> 574). agent.md §10's 1,638 / 284 use only the Madre de Dios rows (Amarakaeri has a
  small Cusco row, Tambopata a tiny Puno row).
  Rest of MdD = MdD department total (Amazonía) minus every buffer-zone row whose department is Madre de Dios.
  Both come from MapBiomas Peru Col 4, so the subtraction is allowed (rule 6 forbids mixing sources).
  Caveat: the department total is Amazonía biome only while buffer-zone rows carry no biome; MdD's Andes biome
  area is small, and rest-of-MdD is checked to be > 0 in every year. It includes the legal mining corridor.
"""
from __future__ import annotations
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pyfixest as pf

from common import (OUT, BZ_KEY, additions, period_mean, x_of, style_axes, add_event_markers,
                    set_year_ticks, finish_figure, EVENT_TITLE_PAD, SRC_MAPBIOMAS, SRC_PRICE)

TAM, AMA, BAH = "Tambopata", "Amarakaeri", "Bahuaja-Sonene"
Y0, Y1 = 2014, 2025
PERIODS = {"2016-18": (2016, 2018), "2019-21": (2019, 2021), "2022-25": (2022, 2025)}
SRC = "peru_bufferzone_year.csv, peru_department_year.csv"

# ----------------------------------------------------------------------------- build the series
def build_series(pack):
    """Return (levels, adds): wide tables (index year; columns = units) of mining_ha and annual additions."""
    zb, pe = pack["zb"], pack["pe"]
    zb = zb.assign(unit=zb["buffer_zone"] + "|" + zb["pa_category"])
    # buffer-zone level per unit-year, summed over departments (aggregate first)
    bz = zb.groupby("unit", as_index=False).size()[["unit"]]
    lv = zb.groupby(["unit", "year"], as_index=False)["mining_ha"].sum()
    lv_w = lv.pivot(index="year", columns="unit", values="mining_ha")
    assert lv_w.notna().all().all()
    # MdD department total, Amazonía biome only (rule 4), one row per year
    mdd = (pe[(pe["department"] == "Madre de Dios") & (pe["biome"] == "Amazonía")]
           .groupby("year")["mining_ha"].sum())
    # all buffer-zone rows in MdD, summed over zones
    bz_in_mdd = zb[zb["department"] == "Madre de Dios"].groupby("year")["mining_ha"].sum()
    rest = mdd - bz_in_mdd
    assert (rest > 0).all(), "rest of MdD must stay positive"
    levels = pd.DataFrame({
        TAM: lv_w["Tambopata|Reserva Nacional"],
        AMA: lv_w["Amarakaeri|Reserva Comunal"],
        BAH: lv_w["Bahuaja-Sonene|Parque Nacional"],
        "Rest of Madre de Dios": rest,
        "Madre de Dios total": mdd,
    })
    levels["Three buffer zones (sum)"] = levels[[TAM, AMA, BAH]].sum(axis=1)
    adds = levels.diff()           # one row per year already, so differencing is safe
    return levels, adds, lv_w

# ----------------------------------------------------------------------------- phase 3a: describe + compare
def describe_and_compare(levels, adds, reg):
    units = [TAM, AMA, BAH, "Rest of Madre de Dios", "Madre de Dios total", "Three buffer zones (sum)"]
    # annual additions 2014-2025 (table)
    adds.loc[Y0:Y1, units].round(1).to_csv(OUT / "peru_additions_2014_2025.csv")
    # period means
    pm = pd.DataFrame({p: {u: period_mean(adds[u], *yrs) for u in units} for p, yrs in PERIODS.items()})
    pm.round(1).to_csv(OUT / "peru_period_means.csv")
    slug = {TAM: "tambopata", AMA: "amarakaeri", BAH: "bahuaja", "Rest of Madre de Dios": "rest_mdd",
            "Madre de Dios total": "mdd_total", "Three buffer zones (sum)": "three_bz_sum"}
    for u in units:
        for p in PERIODS:
            reg.add(f"mean_add_{slug[u]}_{p.replace('-', '_')}", pm.loc[u, p], "ha/yr",
                    f"Mean annual addition to mining area, {u}, {p}", "description", SRC)

    # 2x2 DiD (main: Tambopata vs Amarakaeri) -- description, not causal
    def did(t, c, pre, post):
        dt = period_mean(adds[t], *post) - period_mean(adds[t], *pre)
        dc = period_mean(adds[c], *post) - period_mean(adds[c], *pre)
        return dt, dc, dt - dc
    rows = []
    for name, (pre, post, note) in {
        "main_2016-18_vs_2019-21": ((2016, 2018), (2019, 2021), "Main: Tambopata vs Amarakaeri"),
        "placebo_2013-15_vs_2016-18": ((2013, 2015), (2016, 2018), "Placebo: fake operation in 2016 (no real-treatment years in window)"),
        "persistence_2016-18_vs_2022-25": ((2016, 2018), (2022, 2025), "Persistence: 2016-18 vs 2022-25"),
    }.items():
        dt, dc, d = did(TAM, AMA, pre, post)
        rows.append(dict(design=name, note=note, pre=f"{pre[0]}-{pre[1]}", post=f"{post[0]}-{post[1]}",
                         tambopata_pre=period_mean(adds[TAM], *pre), tambopata_post=period_mean(adds[TAM], *post),
                         amarakaeri_pre=period_mean(adds[AMA], *pre), amarakaeri_post=period_mean(adds[AMA], *post),
                         change_tambopata=dt, change_amarakaeri=dc, did_ha_per_yr=d))
        k = name.split("_")[0]
        reg.add(f"did_{k}", d, "ha/yr",
                f"DiD of mean annual additions, Tambopata minus Amarakaeri, {note}. Descriptive contrast of "
                f"changes; not causal (spillovers, COVID, gold price, further enforcement waves).",
                "description", SRC)
        reg.add(f"did_{k}_tambopata_change", dt, "ha/yr", f"Change in Tambopata mean addition, {name}", "description", SRC)
        reg.add(f"did_{k}_amarakaeri_change", dc, "ha/yr", f"Change in Amarakaeri mean addition, {name}", "description", SRC)
    did_tab = pd.DataFrame(rows)
    did_tab.round(1).to_csv(OUT / "fig_peru_did_table.csv", index=False)   # "figure" = table (CSV)
    print("\nDiD table (ha/yr):\n", did_tab.drop(columns="note").round(0).to_string(index=False))

    # displacement: sum of the three zones + MdD total, before vs after
    disp = pm.loc[["Three buffer zones (sum)", "Rest of Madre de Dios", "Madre de Dios total"]].copy()
    disp["change_2019-21_vs_2016-18"] = disp["2019-21"] - disp["2016-18"]
    disp["change_2022-25_vs_2016-18"] = disp["2022-25"] - disp["2016-18"]
    disp.round(1).to_csv(OUT / "peru_displacement.csv")
    print("\nDisplacement (mean additions ha/yr):\n", disp.round(0).to_string())
    for u in disp.index:
        for c in ["change_2019-21_vs_2016-18", "change_2022-25_vs_2016-18"]:
            reg.add(f"displacement_{slug[u]}_{c.replace('-', '_').replace('change_', 'chg_')}", disp.loc[u, c], "ha/yr",
                    f"Change in mean annual addition, {u}: {c.replace('change_', '')}. If displacement were complete, "
                    f"the sum would not fall.", "description", SRC)
    return pm, did_tab

# ----------------------------------------------------------------------------- phase 3b: event study
def _panel(wide_adds: pd.DataFrame, treated: str) -> pd.DataFrame:
    d = wide_adds.loc[Y0:Y1].reset_index().melt(id_vars="year", var_name="unit", value_name="y")
    d["treated"] = (d["unit"] == treated).astype(int)
    for k in range(Y0, Y1 + 1):
        if k != 2018:                                  # omit 2018, the year before the operation
            d[f"d{k}"] = ((d["year"] == k) & (d["treated"] == 1)).astype(int)
    return d

def event_study(wide_adds: pd.DataFrame, treated: str) -> pd.Series:
    """y_it = a_i + g_t + sum_k b_k (treated_i x 1[t=k]) + e_it, k != 2018. Returns b_k (pyfixest)."""
    d = _panel(wide_adds, treated)
    ks = [k for k in range(Y0, Y1 + 1) if k != 2018]
    fit = pf.feols("y ~ " + " + ".join(f"d{k}" for k in ks) + " | unit + year", data=d, vcov={"CRV1": "unit"})
    return pd.Series({k: fit.coef()[f"d{k}"] for k in ks}).sort_index(), fit

def beta_by_formula(wide_adds: pd.DataFrame, treated: str) -> pd.Series:
    """With one treated unit and equal weights, the saturated event-study coefficient is
    b_k = (y_T,k - mean_c y_c,k) - (y_T,2018 - mean_c y_c,2018). Used for the placebo-in-space loop
    (and checked against pyfixest for the real treated unit)."""
    w = wide_adds.loc[Y0:Y1]
    gap = w[treated] - w.drop(columns=treated).mean(axis=1)
    return (gap - gap.loc[2018]).drop(2018)

def run_event_study(adds, lv_w, pack, reg):
    zb = pack["zb"]
    zb = zb.assign(unit=zb["buffer_zone"] + "|" + zb["pa_category"])
    lv_all = zb.groupby(["unit", "year"])["mining_ha"].sum().unstack("unit")
    ad_all = lv_all.diff()
    # Choice A (main): buffer zones that touch Madre de Dios AND have non-zero mining additions pre-2019
    # (2014-18): Tambopata, Amarakaeri, Bahuaja-Sonene. The other four MdD zones (Alto Purús, Purús, Manu,
    # Megantoni) have zero mining in every year, so they would only add all-zero controls.
    in_mdd = set(zb.loc[zb["department"] == "Madre de Dios", "unit"])
    nz = (ad_all.loc[2014:2018].abs().sum() > 0)
    poolA = sorted(u for u in in_mdd if nz[u])
    # Choice B (robustness + placebo-in-space donor pool): every Peruvian buffer zone with non-zero additions
    # in 2014-18, any department (buffer-zone table has no biome column, so some are not Amazonian).
    poolB = sorted(nz[nz].index)
    TU = "Tambopata|Reserva Nacional"
    assert TU in poolA and TU in poolB
    print(f"\nEvent-study pool A (MdD, nonzero pre-2019): {poolA}\nPool B (all Peru, nonzero pre-2019): {len(poolB)} zones")
    pd.Series(poolA).to_csv(OUT / "peru_event_pool_A.csv", index=False, header=["unit"])
    pd.Series(poolB).to_csv(OUT / "peru_event_pool_B.csv", index=False, header=["unit"])

    bA, fitA = event_study(ad_all[poolA], TU)
    bB, fitB = event_study(ad_all[poolB], TU)
    # sanity: closed-form equals pyfixest
    for b, p in [(bA, poolA), (bB, poolB)]:
        assert np.allclose(b.values, beta_by_formula(ad_all[p], TU).values, atol=1e-4), "event-study formula mismatch"
    seA = fitA.se(); pvA = fitA.pvalue()

    # placebo in space: give treatment to each non-Tambopata unit in pool B, same estimator
    ph = {u: beta_by_formula(ad_all[poolB], u) for u in poolB if u != TU}
    ph_df = pd.DataFrame(ph)
    real = beta_by_formula(ad_all[poolB], TU)
    # summary statistic: mean beta over 2019-2021 (and 2019-2025), more negative = bigger relative drop
    stat = {u: beta_by_formula(ad_all[poolB], u).loc[2019:2021].mean() for u in poolB}
    stat_sc = {}      # scale-free version: divide by the unit's own mean addition 2014-18 (relative change vs controls)
    for u in poolB:
        base = ad_all[u].loc[2014:2018].mean()
        stat_sc[u] = stat[u] / base if base > 0 else np.nan
    st = pd.DataFrame({"mean_beta_2019_21_ha": stat, "scaled_by_own_pre_mean": stat_sc})
    st["rank_raw_most_negative_first"] = st["mean_beta_2019_21_ha"].rank()
    st["rank_scaled_most_negative_first"] = st["scaled_by_own_pre_mean"].rank()
    st.round(3).to_csv(OUT / "peru_placebo_in_space.csv")
    n = len(poolB)
    rank_raw = int(st.loc[TU, "rank_raw_most_negative_first"])
    rank_sc = int(st.loc[TU, "rank_scaled_most_negative_first"])
    print(f"Placebo-in-space (pool B, n={n}): Tambopata rank {rank_raw}/{n} raw (1 = most negative), "
          f"{rank_sc}/{n} scaled")

    es = pd.DataFrame({"beta_poolA": bA, "se_poolA_clustered_NOT_INFORMATIVE": seA.rename(lambda s: int(s[1:])),
                       "beta_poolB": bB, "placebo_min": ph_df.min(axis=1), "placebo_max": ph_df.max(axis=1)})
    es.index.name = "year"
    es.round(2).to_csv(OUT / "peru_event_study.csv")

    for k in range(2019, 2026):
        reg.add(f"eventstudy_beta_poolA_{k}", bA[k], "ha", f"Event-study coefficient {k} (ref 2018), Tambopata vs "
                f"{len(poolA)-1} MdD-linked controls, outcome = annual addition. Point estimate only: one treated unit, "
                f"clustered SEs not informative.", "description", SRC)
        reg.add(f"eventstudy_beta_poolB_{k}", bB[k], "ha", f"Event-study coefficient {k} (ref 2018), Tambopata vs all Peru "
                f"buffer zones with pre-2019 mining ({n-1} controls).", "description", SRC)
    for k in range(2014, 2018):
        reg.add(f"eventstudy_pretrend_poolA_{k}", bA[k], "ha", f"Event-study pre-period coefficient {k} (ref 2018), pool A",
                "description", SRC)
    reg.add("placebo_space_rank_raw", rank_raw, "rank", f"Rank of Tambopata among {n} buffer zones (1 = most negative) in mean "
            f"event-study beta 2019-21, each unit treated in turn", "description", SRC)
    reg.add("placebo_space_rank_scaled", rank_sc, "rank", f"Same, scaled by each unit's own mean addition 2014-18", "description", SRC)
    reg.add("placebo_space_n_units", n, "count", "Number of units in the placebo-in-space donor pool B", "description", SRC)

    # ---- figure
    fig, (ax, ax2) = plt.subplots(2, 1, figsize=(8.5, 7), sharex=True, gridspec_kw={"height_ratios": [1.5, 1]})
    yrs = sorted(bA.index)
    ax.fill_between(x_of(es.index), es["placebo_min"], es["placebo_max"], color="#CFD8DC", alpha=0.7,
                    label="Range if treatment were given to each other buffer zone (pool B)", step=None)
    ax.plot(x_of(yrs), bB.loc[yrs], color="#7a9cc6", marker="s", markersize=5, linewidth=1.2,
            label="Tambopata vs all Peru buffer zones with mining (pool B)")
    ax.plot(x_of(yrs), bA.loc[yrs], color="#B03A2E", marker="o", markersize=7, linewidth=2,
            label="Tambopata vs MdD buffer zones (pool A, main)")
    ax.axhline(0, color="black", linewidth=0.8)
    ax.scatter([2018], [0], marker="o", facecolors="white", edgecolors="black", zorder=5, label="2018 = reference year (0 by construction)")
    ax.set_ylabel("Event-study coefficient\n(ha per year vs 2018)")
    ax.set_title("Tambopata buffer zone vs comparison zones: additions relative to 2018", loc="left", pad=EVENT_TITLE_PAD)
    ax.set_ylim(-3600, None)
    ax.legend(fontsize=7, frameon=True, facecolor="white", edgecolor="none", framealpha=0.95, loc="lower left").set_zorder(10)
    add_event_markers(ax, label=True)
    # bottom: the raw additions of the treated unit and main control (what the coefficients are made of)
    ax2.plot(x_of(range(Y0, Y1 + 1)), ad_all.loc[Y0:Y1, TU], color="#d9a441", marker="o", label="Tambopata")
    ax2.plot(x_of(range(Y0, Y1 + 1)), ad_all.loc[Y0:Y1, "Amarakaeri|Reserva Comunal"], color="#7a9cc6", marker="o", label="Amarakaeri")
    ax2.set_ylabel("Annual addition (ha)")
    ax2.legend(fontsize=7, frameon=False, loc="upper left")
    add_event_markers(ax2)
    for a in (ax, ax2):
        style_axes(a)
    set_year_ticks(ax2, range(Y0, Y1 + 1))
    note = ("One treated unit: standard errors clustered by unit are not informative (inference needs many treated clusters; "
            "Conley & Taber 2011), so no CIs are drawn.\nThe grey band is the placebo-in-space alternative. Descriptive; not causal.")
    finish_figure(fig, f"{note}\nSource: {SRC_MAPBIOMAS}.", OUT / "fig_peru_event_study.png", rect_bottom=0.08, event_note=True)
    return bA, bB, rank_raw, rank_sc, n

# ----------------------------------------------------------------------------- figures
def fig_additions(adds, pack):
    pr = pack["prices"].set_index("year")["gold"]
    yrs = list(range(Y0, Y1 + 1))
    fig, axes = plt.subplots(3, 1, figsize=(8.5, 8.5), sharex=True, gridspec_kw={"height_ratios": [1.4, 1.4, 1]})
    a1, a2, a3 = axes
    for u, c in [(TAM, "#d9a441"), (AMA, "#7a9cc6"), (BAH, "#6aa84f")]:
        a1.plot(x_of(yrs), adds.loc[yrs, u], marker="o", color=c, linewidth=2, label=f"{u} buffer zone")
    a1.set_ylabel("New mining area\nin the year (ha)")
    a1.set_title("Madre de Dios: new mining area each year, by buffer zone, and the gold price", loc="left", pad=EVENT_TITLE_PAD)
    a1.set_ylim(None, 4800)
    a1.legend(fontsize=8, frameon=False, loc="upper left", ncol=3)
    a2.plot(x_of(yrs), adds.loc[yrs, "Madre de Dios total"], marker="o", color="black", linewidth=2, label="Madre de Dios total")
    a2.plot(x_of(yrs), adds.loc[yrs, "Rest of Madre de Dios"], marker="o", color="#8E7CC3", linewidth=1.5,
            label="Rest of Madre de Dios (dept. minus buffer zones; incl. legal corridor)")
    a2.set_ylabel("New mining area\nin the year (ha)")
    a2.legend(fontsize=8, frameon=False, loc="upper left")
    a3.plot(x_of(yrs), pr.loc[yrs], color="#234A76", linewidth=2, marker="o")
    a3.set_ylabel("Gold price\n($ per troy oz)"); a3.set_ylim(0, None)
    for i, a in enumerate(axes):
        style_axes(a); add_event_markers(a, label=(i == 0))
    set_year_ticks(a3, yrs)
    finish_figure(fig, f"Sources: {SRC_MAPBIOMAS}; {SRC_PRICE}.\nAdditions = change in area classified as mining; "
                       "river dredging and mercury are invisible.", OUT / "fig_peru_additions.png", event_note=True)

def fig_displacement(adds):
    yrs = list(range(Y0, Y1 + 1))
    fig, (a1, a2) = plt.subplots(2, 1, figsize=(8.5, 6.5), sharex=True)
    bottom_pos = np.zeros(len(yrs)); bottom_neg = np.zeros(len(yrs))
    for u, c in [(TAM, "#d9a441"), (AMA, "#7a9cc6"), (BAH, "#6aa84f")]:
        v = adds.loc[yrs, u].values
        pos, neg = np.where(v > 0, v, 0), np.where(v < 0, v, 0)
        a1.bar(x_of(yrs), pos, bottom=bottom_pos, color=c, width=0.8, label=u)
        a1.bar(x_of(yrs), neg, bottom=bottom_neg, color=c, width=0.8)
        bottom_pos += pos; bottom_neg += neg
    a1.plot(x_of(yrs), adds.loc[yrs, "Three buffer zones (sum)"], color="black", marker="o", markersize=4, linewidth=1.2,
            label="Sum of the three buffer zones")
    a1.set_ylabel("New mining area (ha)")
    a1.set_title("Did the total fall, or did mining move? Three buffer zones vs all of Madre de Dios", loc="left", pad=EVENT_TITLE_PAD)
    a1.legend(fontsize=8, frameon=True, facecolor="white", edgecolor="none", framealpha=0.95, loc="upper left").set_zorder(10)
    a2.bar(x_of(yrs), adds.loc[yrs, "Madre de Dios total"], color="#B8B8B8", width=0.8, label="Madre de Dios total")
    a2.plot(x_of(yrs), adds.loc[yrs, "Rest of Madre de Dios"], color="#8E7CC3", marker="o", linewidth=1.8,
            label="Rest of Madre de Dios (incl. legal mining corridor)")
    a2.set_ylabel("New mining area (ha)")
    a2.legend(fontsize=8, frameon=True, facecolor="white", edgecolor="none", framealpha=0.95, loc="upper left").set_zorder(10)
    for i, a in enumerate((a1, a2)):
        style_axes(a); add_event_markers(a, label=(i == 0))
    set_year_ticks(a2, yrs)
    finish_figure(fig, f"Source: {SRC_MAPBIOMAS}. Description only; MapBiomas cannot separate legal from illegal mining.",
                  OUT / "fig_peru_displacement.png", event_note=True)

# ----------------------------------------------------------------------------- entry point
def run(pack, reg):
    print("\n== Peru core analysis ==")
    levels, adds, lv_w = build_series(pack)
    adds.loc[Y0:Y1].round(1).to_csv(OUT / "peru_additions_all_units.csv")
    pm, did_tab = describe_and_compare(levels, adds, reg)
    print("\nPeriod means (ha/yr):\n", pm.round(0).to_string())
    res = run_event_study(adds, lv_w, pack, reg)
    fig_additions(adds, pack)
    fig_displacement(adds)
    import peru_robust
    peru_robust.run(pack, reg, series=(levels, adds, lv_w))
    return dict(levels=levels, adds=adds, period_means=pm, did=did_tab, event=res)
