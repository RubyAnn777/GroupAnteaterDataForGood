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
                    set_year_ticks, finish_figure, EVENT_TITLE_PAD, SRC_MAPBIOMAS, SRC_PRICE,
                    headline, label_end, callout, placebo_rank, C, INK, INK2, MUTED, AXIS)

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
    # extra series numbers (text quotes)
    for yr in (2022, 2023, 2024, 2025):
        reg.add(f"add_tambopata_{yr}", adds.loc[yr, TAM], "ha", f"Annual addition to mining area, Tambopata BZ, {yr}", "description", SRC)
    reg.add("mean_add_tambopata_2022_25_ex2023", adds.loc[[2022, 2024, 2025], TAM].mean(), "ha/yr",
            "Mean annual addition, Tambopata BZ, 2022, 2024 and 2025 (2023 excluded: a year in which every unit spiked)", "description", SRC)
    reg.add("mean_add_amarakaeri_2014_18", period_mean(adds[AMA], 2014, 2018), "ha/yr", "Mean annual addition, Amarakaeri BZ, 2014-18", "description", SRC)
    reg.add("mean_add_tambopata_2014_18", period_mean(adds[TAM], 2014, 2018), "ha/yr", "Mean annual addition, Tambopata BZ, 2014-18", "description", SRC)
    dt_b, dc_b, d_b = did(TAM, AMA, (2014, 2018), (2019, 2021))
    reg.add("did_main_base_2014_18", d_b, "ha/yr",
            "DiD of mean annual additions, Tambopata minus Amarakaeri, baseline 2014-18 vs 2019-21 (longer baseline than the main 2016-18; "
            "shows sensitivity to Amarakaeri's low 2016-18 level). Descriptive; not causal.", "description", SRC)
    reg.add("add_amarakaeri_2023", adds.loc[2023, AMA], "ha", "Annual addition to mining area, Amarakaeri BZ, 2023", "description", SRC)
    reg.add("add_rest_mdd_2023", adds.loc[2023, "Rest of Madre de Dios"], "ha", "Annual addition to mining area, rest of Madre de Dios (dept. minus MdD buffer-zone rows), 2023", "description", SRC)
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
    noTU = [v for v in poolB if v != TU]          # fixed 12 Oct 2026: Tambopata is not a control for the fake zones
    ph = {u: beta_by_formula(ad_all[noTU], u) for u in noTU}
    ph_df = pd.DataFrame(ph)
    real = beta_by_formula(ad_all[poolB], TU)
    # summary statistic: mean beta over 2019-2021 (and 2019-2025), more negative = bigger relative drop
    stat = {u: beta_by_formula(ad_all[noTU], u).loc[2019:2021].mean() for u in noTU}
    stat[TU] = real.loc[2019:2021].mean()
    stat_sc = {}      # scale-free version: divide by the unit's own mean addition 2014-18 (relative change vs controls)
    for u in poolB:
        base = ad_all[u].loc[2014:2018].mean()
        stat_sc[u] = stat[u] / base if base > 0 else np.nan
    st = pd.DataFrame({"mean_beta_2019_21_ha": stat, "scaled_by_own_pre_mean": stat_sc})
    st["rank_raw_most_negative_first"] = st["mean_beta_2019_21_ha"].rank()
    st["rank_scaled_most_negative_first"] = st["scaled_by_own_pre_mean"].rank()
    st.round(3).to_csv(OUT / "peru_placebo_in_space.csv")
    n = len(poolB)
    rank_raw = placebo_rank(stat[TU], [stat[u] for u in noTU])
    rank_sc = placebo_rank(stat_sc[TU], [stat_sc[u] for u in noTU])     # NaN (no pre-mining) never counts
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
    reg.add("placebo_space_rank_scaled", rank_sc, "rank", f"Rank of Tambopata among {n} buffer zones (1 = most negative) "
            f"when each zone's mean event-study beta 2019-21 is divided by its own mean addition 2014-18 (full pool B, "
            f"each unit treated in turn). Zones with tiny pre-2019 means get huge ratios, so this rank is noisy; the "
            f"cleaner scale-free test is M4 (zones > 10 ha/yr only, model_m4_rank).", "description", SRC)
    reg.add("placebo_space_n_units", n, "count", "Number of units in the placebo-in-space donor pool B", "description", SRC)

    for yr in (2016, 2019, 2023, 2024, 2025):
        reg.add(f"eventstudy_band_min_{yr}", es.loc[yr, "placebo_min"], "ha", f"Placebo-in-space band (pool B, each other zone treated in turn): minimum event-study coefficient {yr}", "description", SRC)
        reg.add(f"eventstudy_band_max_{yr}", es.loc[yr, "placebo_max"], "ha", f"Placebo-in-space band (pool B): maximum event-study coefficient {yr}", "description", SRC)
    placebo_restricted(pack, reg)

    # ---- figure
    fig, (ax, ax2) = plt.subplots(2, 1, figsize=(9, 7.6), sharex=True, gridspec_kw={"height_ratios": [1.5, 1], "hspace": 0.35})
    headline(fig, "Tambopata dropped below every placebo zone in 2019–22, then came back",
             "Event-study coefficient: Tambopata's annual mining addition vs comparison zones, relative to 2018 (ha per year)")
    yrs = sorted(bA.index)
    ax.fill_between(x_of(es.index), es["placebo_min"], es["placebo_max"], color="#e6e3dc", lw=0, zorder=1)
    ax.axhline(0, color=INK2, linewidth=0.9, zorder=2)
    ax.plot(x_of(yrs), bB.loc[yrs], color=C["other"], marker="o", markersize=4, mec="white", mew=0.8, linewidth=1.4, zorder=3)
    ax.plot(x_of(yrs), bA.loc[yrs], color=C["lapampa"], marker="o", markersize=6, mec="white", mew=1.0, linewidth=2.2, zorder=4)
    ax.scatter([2018], [0], s=46, facecolors="white", edgecolors=INK, linewidths=1.2, zorder=5)
    callout(ax, 2018, 0, "2018 = reference\n(0 by design)", dy=48, dx=-70, ha="center")
    label_end(ax, yrs[-1], bA.loc[yrs[-1]], "Tambopata vs Madre\nde Dios zones (main)", C["lapampa"], dx=8, dy=-16)
    label_end(ax, yrs[-1], bB.loc[yrs[-1]], "vs all Peru buffer\nzones with mining", C["other"], dx=8, dy=14, weight="normal")
    lo = bA.loc[2019:2022].idxmin()
    callout(ax, lo, bA[lo], f"Lowest:\n{bA[lo]:,.0f} ha in {lo}".replace("-", "−"), dy=-12, dx=7, ha="left",
            arrow=False)                                  # right of the point, clear of the Restauración line
    ax.text(2013.8, -3400, "Grey band: coefficients if each other\nbuffer zone had been 'treated' instead",
            fontsize=7.5, color=INK2, va="bottom")
    ax.set_ylabel("ha per year vs 2018")
    ax.set_title("Coefficients (one treated unit, so no confidence intervals: the band is the test)", pad=EVENT_TITLE_PAD)
    ax.set_ylim(-3600, None)
    add_event_markers(ax, label=True)
    # bottom: the raw additions of the treated unit and main control (what the coefficients are made of)
    xs = x_of(range(Y0, Y1 + 1))
    ax2.plot(xs, ad_all.loc[Y0:Y1, TU], color=C["lapampa"], marker="o", mec="white", mew=0.8)
    ax2.plot(xs, ad_all.loc[Y0:Y1, "Amarakaeri|Reserva Comunal"], color=C["buffer"], marker="o", mec="white", mew=0.8)
    label_end(ax2, Y1, ad_all.loc[Y1, TU], "Tambopata", C["lapampa"], dx=8)
    label_end(ax2, Y1, ad_all.loc[Y1, "Amarakaeri|Reserva Comunal"], "Amarakaeri", C["buffer"], dx=8)
    ax2.set_ylabel("ha per year")
    ax2.set_title("What the coefficients are made of: annual mining additions")
    add_event_markers(ax2)
    for a in (ax, ax2):
        style_axes(a)
    ax2.set_xlim(Y0 - 0.6, Y1 + 0.6)
    set_year_ticks(ax2, range(Y0, Y1 + 1))
    note = ("One treated unit: clustered standard errors are not informative (Conley & Taber 2011), so no CIs are drawn; "
            "the placebo band is the alternative. Description, not causal.")
    finish_figure(fig, f"{SRC_MAPBIOMAS}. {note}", OUT / "fig_peru_event_study.png", event_note=True)
    return bA, bB, rank_raw, rank_sc, n

def placebo_restricted(pack, reg, thresh=10.0):
    """Placebo-in-space with a meaningful donor pool: buffer zones with mean 2014-18 additions > `thresh` ha/yr AND
    rows in Amazon-biome departments (same department-based filter as peru_robust). Tambopata is ranked among
    donors + itself on the mean event-study beta 2019-21 (1 = most negative). Description only; minimum p = 1/n."""
    zb, pe = pack["zb"], pack["pe"]
    amz = set(pe.loc[pe["biome"] == "Amazonía", "department"])
    zr = zb[zb["department"].isin(amz)]
    zr = zr.assign(unit=zr["buffer_zone"] + "|" + zr["pa_category"])
    ad = zr.groupby(["unit", "year"])["mining_ha"].sum().unstack("unit").diff()
    TU = "Tambopata|Reserva Nacional"
    pre = ad.loc[2014:2018].mean()
    pool = sorted(u for u in pre.index if pre[u] > thresh)
    assert TU in pool
    stat = {u: peru_beta(ad[[v for v in pool if v != TU]], u).loc[2019:2021].mean() for u in pool if u != TU}
    stat[TU] = peru_beta(ad[pool], TU).loc[2019:2021].mean()
    st = pd.DataFrame({"mean_beta_2019_21_ha": stat, "mean_add_2014_18_ha": pre[pool]})
    st["rank_most_negative_first"] = st["mean_beta_2019_21_ha"].rank()
    st["role"] = np.where(st.index == TU, "treated (real)", "donor")
    st.round(2).to_csv(OUT / "peru_placebo_in_space_restricted.csv")
    n = len(pool)
    rk = placebo_rank(stat[TU], [stat[u] for u in pool if u != TU])
    donors = "; ".join(u.split("|")[0] for u in pool if u != TU)
    print(f"Placebo-in-space RESTRICTED (mean 2014-18 > {thresh:g} ha/yr, Amazon-biome departments): n={n}, Tambopata rank {rk}/{n}; donors: {donors}")
    reg.add("placebo_space_rank_restricted", rk, "rank",
            f"Rank of Tambopata among {n} buffer zones (itself + {n-1} donors with mean 2014-18 additions > {thresh:g} ha/yr in Amazon-biome departments; "
            f"1 = most negative) in mean event-study beta 2019-21. Donors: {donors}. See output/peru_placebo_in_space_restricted.csv", "description", SRC)
    reg.add("placebo_space_n_restricted", n, "count", f"Number of units (Tambopata + donors) in the restricted placebo-in-space pool; minimum possible rank share is 1/{n}", "description", SRC)

def peru_beta(wide, treated):
    return beta_by_formula(wide, treated)

# ----------------------------------------------------------------------------- figures
def fig_additions(adds, pack):
    pr = pack["prices"].set_index("year")["gold"]
    yrs = list(range(Y0, Y1 + 1)); xs = x_of(yrs)
    fig, axes = plt.subplots(3, 1, figsize=(9, 8.6), sharex=True, gridspec_kw={"height_ratios": [1.4, 1.4, 0.9], "hspace": 0.35})
    a1, a2, a3 = axes
    headline(fig, "Tambopata fell after Mercurio; Madre de Dios as a whole did not",
             "New mining area each year (annual addition, ha), 2014–2025, and the gold price")
    for u, c in [(TAM, C["lapampa"]), (AMA, C["buffer"]), (BAH, C["twin"])]:
        a1.plot(xs, adds.loc[yrs, u], marker="o", color=c, mec="white", mew=0.8)
        label_end(a1, Y1, adds.loc[Y1, u], u, c, dx=8)
    a1.set_ylabel("ha per year")
    a1.set_title("Three buffer zones", pad=EVENT_TITLE_PAD)
    a1.set_ylim(None, 4800)
    a2.plot(xs, adds.loc[yrs, "Madre de Dios total"], marker="o", color=INK, mec="white", mew=0.8)
    a2.plot(xs, adds.loc[yrs, "Rest of Madre de Dios"], marker="o", color=C["corridor"], mec="white", mew=0.8, lw=1.6)
    label_end(a2, Y1, adds.loc[Y1, "Madre de Dios total"], "Madre de Dios\ntotal", INK, dx=8)
    label_end(a2, Y1, adds.loc[Y1, "Rest of Madre de Dios"], "Rest of department\n(incl. legal corridor)", C["corridor"], dx=8)
    a2.set_ylabel("ha per year"); a2.set_ylim(0, None)
    a2.set_title("The whole department")
    a3.plot(xs, pr.loc[yrs], color=C["gold"], marker="o", mec="white", mew=0.8)
    label_end(a3, Y1, pr.loc[Y1], f"Gold\n${pr.loc[Y1]:,.0f}/oz", C["gold"], dx=8)
    a3.set_ylabel("$ per troy oz"); a3.set_ylim(0, None)
    a3.set_title("Gold price (nominal, annual mean)")
    for i, a in enumerate(axes):
        style_axes(a); add_event_markers(a, label=(i == 0))
    a3.set_xlim(Y0 - 0.6, Y1 + 0.6)
    set_year_ticks(a3, yrs)
    finish_figure(fig, f"{SRC_MAPBIOMAS}; {SRC_PRICE}. Additions = change in area classified as mining; "
                       "river dredging and mercury are invisible. Description.", OUT / "fig_peru_additions.png", event_note=True)

def fig_displacement(adds):
    yrs = list(range(Y0, Y1 + 1)); xs = x_of(yrs)
    fig, (a1, a2) = plt.subplots(2, 1, figsize=(9, 7.2), sharex=True, gridspec_kw={"hspace": 0.35})
    headline(fig, "The three buffer zones fell in 2019–21; the department total kept rising",
             "New mining area each year (annual addition, ha). Did mining stop, or move?")
    bottom_pos = np.zeros(len(yrs)); bottom_neg = np.zeros(len(yrs))
    for u, c in [(TAM, C["lapampa"]), (AMA, C["buffer"]), (BAH, C["twin"])]:
        v = adds.loc[yrs, u].values
        pos, neg = np.where(v > 0, v, 0), np.where(v < 0, v, 0)
        a1.bar(xs, pos, bottom=bottom_pos, color=c, width=0.72, edgecolor="white", linewidth=0.8)
        a1.bar(xs, neg, bottom=bottom_neg, color=c, width=0.72, edgecolor="white", linewidth=0.8)
        bottom_pos += pos; bottom_neg += neg
    a1.plot(xs, adds.loc[yrs, "Three buffer zones (sum)"], color=INK, marker="o", markersize=4, mec="white", mew=0.8, linewidth=1.2)
    # direct labels: one legend row above the plot (stack labels would collide at the year ends)
    from matplotlib.patches import Patch
    from matplotlib.lines import Line2D
    a1.legend(handles=[Patch(color=C["lapampa"], label=TAM), Patch(color=C["buffer"], label=AMA),
                       Patch(color=C["twin"], label=BAH), Line2D([], [], color=INK, marker="o", ms=4, lw=1.2, label="Sum of the three")],
              loc="upper left", ncol=4, fontsize=8, handlelength=1.2, columnspacing=1.2, frameon=True,
              facecolor="#fbfaf7", edgecolor="none", framealpha=1).set_zorder(10)
    a1.set_ylabel("ha per year")
    a1.set_title("Three buffer zones (stacked)", pad=EVENT_TITLE_PAD)
    a1.set_ylim(None, a1.get_ylim()[1] * 1.15)
    a2.bar(xs, adds.loc[yrs, "Madre de Dios total"], color="#d9d6cf", width=0.72)
    a2.plot(xs, adds.loc[yrs, "Rest of Madre de Dios"], color=C["corridor"], marker="o", mec="white", mew=0.8, linewidth=1.8)
    callout(a2, 2023, adds.loc[2023, "Madre de Dios total"], "Department total (bars)", dx=-58, dy=-4, ha="right")
    label_end(a2, Y1, adds.loc[Y1, "Rest of Madre de Dios"], "Rest of department\n(incl. legal corridor)", C["corridor"], dx=8, dy=-14)
    a2.set_ylabel("ha per year")
    a2.set_title("All of Madre de Dios")
    for i, a in enumerate((a1, a2)):
        style_axes(a); add_event_markers(a, label=(i == 0))
    a2.set_xlim(Y0 - 0.6, Y1 + 0.6)
    set_year_ticks(a2, yrs)
    finish_figure(fig, f"{SRC_MAPBIOMAS}. Description only; MapBiomas cannot separate legal from illegal mining.",
                  OUT / "fig_peru_displacement.png", event_note=True)

# ----------------------------------------------------------------------------- entry point
def run(pack, reg):
    print("\n== Peru core analysis ==")
    levels, adds, lv_w = build_series(pack)
    adds.loc[Y0:Y1].round(1).to_csv(OUT / "peru_additions_all_units.csv")
    pm, did_tab = describe_and_compare(levels, adds, reg)
    print("\nPeriod means (ha/yr):\n", pm.round(0).to_string())
    res = run_event_study(adds, lv_w, pack, reg)
    gp = pack["prices"].set_index("year")["gold"]
    for yr in (2018, 2022, 2023, 2025):
        reg.add(f"gold_price_{yr}", gp[yr], "USD/oz", f"Gold price, annual mean, nominal, {yr} ({SRC_PRICE})", "description", "prices_annual.csv")
    reg.add("gold_price_ratio_2025_2018", gp[2025] / gp[2018], "ratio", "Gold price 2025 divided by 2018 (nominal annual means)", "description", "prices_annual.csv")
    reg.add("gold_price_pct_change_2022_2023", 100 * (gp[2023] / gp[2022] - 1), "%", "Gold price change 2022 to 2023 (nominal annual means)", "description", "prices_annual.csv")
    fig_additions(adds, pack)
    fig_displacement(adds)
    import peru_robust
    peru_robust.run(pack, reg, series=(levels, adds, lv_w))
    return dict(levels=levels, adds=adds, period_means=pm, did=did_tab, event=res)
