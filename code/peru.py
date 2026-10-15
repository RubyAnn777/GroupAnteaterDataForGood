"""Peru core analysis (Operation Mercurio, Feb 2019) on ONE outcome and ONE zone registry (plan v3).

Outcome: net mining additions (ha/yr) = new land + re-mined - stopped, MapBiomas Peru Collection 4 rasters, our pixel
accounting (raster_zones.py). Zones: definitions.UNITS (region partition) and the national buffer-zone panel, both
read through zonedata.py. Treatment: start of Mercurio, first treated year 2019, reference 2018 (definitions.py).
Every comparison is registered for net AND its three parts; the parts add up (net = new + re-mined - stopped)
because means, differences and the event-study coefficients are linear.

  describe          levels + net additions table (course step), period means of net and parts for every unit
  compare           2x2 (Tambopata BZ vs Amarakaeri BZ): main, placebo (fake 2016 start), persistence, 2014-18 base
  displacement      where Madre de Dios's net additions went: the department's zones sum to its total
  event study       national buffer-zone panel, pool A (Madre de Dios-linked) and pool B (all zones with pre-2019
                    mining), placebo in space (raw, scaled, and in pre-years), placebo in time on Tambopata alone
All results are DESCRIPTION (one treated unit; see docs/methods/14_synthesis.md).
"""
from __future__ import annotations
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pyfixest as pf

from common import (OUT, x_of, style_axes, add_event_markers, set_year_ticks, finish_figure, EVENT_TITLE_PAD,
                    SRC_PRICE, headline, label_end, callout, placebo_rank, period_band, C, INK, INK2, MUTED)
import definitions as D
import zonedata as Z

T, A = D.TREATED_ZONE, "amarakaeri_bz"
Y0, Y1 = D.YEARS
SRC = D.SOURCE
MEAS = ["net"] + D.PARTS
PART_C = {m: C[m] for m in D.PARTS}


def _w(df, m):
    return Z.wide(df, D.COLS[m])


# ----------------------------------------------------------------------------- describe
def describe(reg):
    ru = Z.region_units()
    units = ["tambopata_bz", "lapampa", "tambopata_bz_rest", "amarakaeri_bz", "corridor_across", "corridor_rest",
             "communities", "tambopata_nr", "rest_mdd", "mdd"]
    # course step: levels (stock) and annual additions, by unit and year
    t = ru[ru.unit.isin(units) & ru.year.between(Y0, Y1)].copy()
    t["unit_name"] = t.unit.map(D.UNIT_NAME)
    t[["unit", "unit_name", "year", "mining_ha", "net_ha", "new_ha", "remined_ha", "stopped_ha"]].round(1).rename(
        columns={"mining_ha": "mining_stock_ha"}).to_csv(OUT / "peru_levels_and_additions.csv", index=False)
    rows = []
    for u in units:
        d = ru[ru.unit == u].set_index("year")
        for p in D.PERIODS:
            vals = {m: Z.period_mean(d[D.COLS[m]], p) for m in MEAS}
            Z.register_parts(reg, f"{u}_{p}", vals, u, D.period_label(p), "mean per year")
            rows.append(dict(unit=u, period=D.period_label(p), **{m: vals[m] for m in MEAS}))
        ex = [y for y in range(*D.PERIODS["later"]) if y != D.LATER_EX] + [D.PERIODS["later"][1]]
        Z.register_parts(reg, f"{u}_later_ex2023", {m: d.loc[ex, D.COLS[m]].mean() for m in MEAS}, u,
                         "2022, 2024, 2025", "mean per year, without the 2023 MapBiomas spike year")
        reg.add(f"{u}_stock_2025", d.loc[2025, "mining_ha"], "ha", f"Mining area (stock), {D.UNIT_NAME[u]}, 2025",
                "description", SRC, measure="stock", zone=u, period="2025")
        for y in (2018, 2019, 2020, 2021, 2023, 2025):
            Z.register_parts(reg, f"{u}_{y}", {m: d.loc[y, D.COLS[m]] for m in MEAS}, u, str(y), "that year")
    pm = pd.DataFrame(rows)
    pm.round(1).to_csv(OUT / "peru_period_means.csv", index=False)
    # what "stopped" is made of (V3-5): water, forest, other; back within two years
    st = ru[ru.unit.isin(["tambopata_bz", "lapampa", "amarakaeri_bz", "corridor_across"])].set_index("year")
    srows = []
    for u, d in st.groupby("unit"):
        for p in ("pre", "during", "later"):
            a, b = D.PERIODS[p]
            s = d.loc[a:b]
            stopped = s.stopped_ha.sum()
            rec = dict(unit=u, period=D.period_label(p), stopped_ha_yr=s.stopped_ha.mean(),
                       to_water=s.stopped_to_water_ha.sum() / stopped, to_forest=s.stopped_to_forest_ha.sum() / stopped,
                       to_natural=s.stopped_to_natural_ha.sum() / stopped, to_bare=s.stopped_to_bare_ha.sum() / stopped,
                       to_other=s.stopped_to_other_ha.sum() / stopped)
            ok = s.stopped_back_2y_ha.notna()
            rec["back_within_2y"] = s.stopped_back_2y_ha[ok].sum() / s.stopped_ha[ok].sum() if ok.any() else np.nan
            srows.append(rec)
            for k in ("to_water", "to_forest", "to_bare", "back_within_2y"):
                reg.add(f"{u}_{p}_stopped_share_{k}", rec[k], "share",
                        f"Share of stopped land (left the mining class), {D.UNIT_NAME[u]}, {D.period_label(p)}: "
                        f"{'is mining again within 2 years' if k.startswith('back') else 'land became ' + k[3:]}",
                        "description", SRC, measure="stopped", zone=u, period=D.period_label(p))
    pd.DataFrame(srows).round(3).to_csv(OUT / "peru_stopped_split.csv", index=False)
    # tenure inside the Tambopata buffer zone (Kotsimba, corridor): where its mining sits
    ten = Z.tenure_split("tambopata_bz")
    ten = ten[ten.year == 2025].set_index("tenure").mining_ha
    for k, v in ten.items():
        reg.add(f"tambopata_bz_stock_2025_tenure_{k}", v, "ha", f"Mining area (stock) 2025 inside the Tambopata buffer "
                f"zone on land tagged '{k}' (corridor = D.L. 1100; kotsimba / community = native communities)",
                "description", SRC, measure="stock", zone="tambopata_bz", period="2025")
    return ru, pm


# ----------------------------------------------------------------------------- compare (2x2)
def did(ru, treated, control, pre, post, m):
    w = _w(ru, m)
    dt = Z.period_mean(w[treated], post) - Z.period_mean(w[treated], pre)
    dc = Z.period_mean(w[control], post) - Z.period_mean(w[control], pre)
    return dt, dc, dt - dc


def compare(ru, reg):
    designs = {
        "main": (D.PERIODS["pre"], D.PERIODS["during"], "2016–18 vs 2019–21"),
        "base2014": (D.PERIODS["pre_long"], D.PERIODS["during"], "2014–18 vs 2019–21"),
        "placebo": (D.PLACEBO_PERIODS["pre"], D.PLACEBO_PERIODS["during"], "fake start 2016: 2013–15 vs 2016–18"),
        "persistence": (D.PERIODS["pre"], D.PERIODS["later"], "2016–18 vs 2022–25 (later years)"),
    }
    rows = []
    for k, (pre, post, note) in designs.items():
        vals, ch_t, ch_c = {}, {}, {}
        for m in MEAS:
            ch_t[m], ch_c[m], vals[m] = did(ru, T, A, pre, post, m)
            rows.append(dict(design=k, note=note, measure=m, change_tambopata_bz=ch_t[m],
                             change_amarakaeri_bz=ch_c[m], did=vals[m]))
        Z.register_parts(reg, f"did_{k}", vals, T, note, "difference in differences, Tambopata buffer zone minus "
                         "Amarakaeri buffer zone (less treated: Mercurio II covered all of Madre de Dios)")
        Z.register_parts(reg, f"did_{k}_chg_tambopata", ch_t, T, note, "change in the period mean")
        Z.register_parts(reg, f"did_{k}_chg_amarakaeri", ch_c, A, note, "change in the period mean")
        assert abs(vals["net"] - (vals["new"] + vals["remined"] - vals["stopped"])) < 0.01
    tab = pd.DataFrame(rows)
    tab.round(1).to_csv(OUT / "peru_did_table.csv", index=False)
    # how much of the fall in net additions is each part (shares of the Tambopata change, main window)
    ch = tab[(tab.design == "main")].set_index("measure").change_tambopata_bz
    for m in D.PARTS:
        reg.add(f"tambopata_bz_fall_share_{m}", D.SIGN[m] * ch[m] / ch["net"], "share",
                f"Share of the fall in net additions, Tambopata buffer zone, 2016–18 to 2019–21, that comes from "
                f"{D.MEASURE_NAME[m].lower()} (shares add to 1)", "description", SRC, measure=m, zone=T,
                period="2016–18 vs 2019–21")
    # How much of the fall is stopping? A RANGE, not one number (referee 2, 2026-10-15): (a) raw change in stopped land;
    # (b) without stopped land that is mining again within two years (flicker or brief pauses); (c) only stopping in
    # excess of the 2016-18 stopping rate per hectare of existing mining; (d) the stopped part of the DiD.
    for u in (T, "lapampa"):
        d = ru[ru.unit == u].set_index("year")
        pre, dur = D.PERIODS["pre"], D.PERIODS["during"]
        fall = Z.period_mean(d.net_ha, pre) - Z.period_mean(d.net_ha, dur)
        rate = d.stopped_ha / d.mining_ha.shift(1)
        perm = d.stopped_ha - d.stopped_back_2y_ha
        excess = (d.stopped_ha - Z.period_mean(rate, pre) * d.mining_ha.shift(1))
        variants = {
            "raw": (Z.period_mean(d.stopped_ha, dur) - Z.period_mean(d.stopped_ha, pre)) / fall,
            "excl_back2y": (Z.period_mean(perm, dur) - Z.period_mean(perm, pre)) / fall,
            "excess_rate": Z.period_mean(excess, dur) / fall,
        }
        if u == T:
            variants["did"] = did(ru, T, A, pre, dur, "stopped")[2] / -did(ru, T, A, pre, dur, "net")[2]
        for k, v in variants.items():
            reg.add(f"{u}_stopped_share_of_fall_{k}", v, "share", f"Share of the fall in net additions, "
                    f"{D.UNIT_NAME[u]}, 2016–18 to 2019–21, attributable to stopped land, variant '{k}' (raw change; "
                    "excluding land mined again within 2 years; excess over the 2016–18 stopping rate per ha of "
                    "existing mining; stopped part of the DiD vs Amarakaeri)", "description", SRC, measure="stopped",
                    zone=u, period="2016–18 vs 2019–21")
        vals = list(variants.values())
        reg.add(f"{u}_stopped_share_of_fall_min", min(vals), "share", f"Smallest of the stopped-share variants, "
                f"{D.UNIT_NAME[u]}", "description", SRC, measure="stopped", zone=u, period="2016–18 vs 2019–21")
        reg.add(f"{u}_stopped_share_of_fall_max", max(vals), "share", f"Largest of the stopped-share variants, "
                f"{D.UNIT_NAME[u]}", "description", SRC, measure="stopped", zone=u, period="2016–18 vs 2019–21")
        ex = excess.loc[dur[0]:dur[1]]
        reg.add(f"{u}_excess_stopped_share_in_2019", ex.loc[dur[0]] / ex.sum(), "share", f"Share of 2019–21 excess "
                f"stopping (over the 2016–18 rate) that falls in 2019, {D.UNIT_NAME[u]}", "description", SRC,
                measure="stopped", zone=u, period="2019–21")
        reg.add(f"{u}_stopping_rate_pre", Z.period_mean(rate, pre), "share", f"Stopped land as a share of the previous "
                f"year's mining area, mean 2016–18, {D.UNIT_NAME[u]}", "description", SRC, measure="stopped", zone=u,
                period="2016–18")
        reg.add(f"{u}_stopping_rate_2019", rate.loc[dur[0]], "share", f"Stopped land as a share of the previous year's "
                f"mining area, 2019, {D.UNIT_NAME[u]}", "description", SRC, measure="stopped", zone=u, period="2019")
    # how it came back: re-mined land as a share of land added (new + re-mined), later years, with and without 2023
    d = ru[ru.unit == T].set_index("year")
    a, b = D.PERIODS["later"]
    for k, yrs_ in (("", list(range(a, b + 1))), ("_ex2023", [y for y in range(a, b + 1) if y != D.LATER_EX])):
        rem, new = d.loc[yrs_, "remined_ha"].sum(), d.loc[yrs_, "new_ha"].sum()
        reg.add(f"tambopata_bz_later{k}_remined_share_added", rem / (rem + new), "share", "Re-mined land as a share of "
                "land added (new land + re-mined), Tambopata buffer zone, 2022–25" + (" without 2023" if k else ""),
                "description", SRC, measure="remined", zone=T, period="2022–25" + (" ex 2023" if k else ""))
    # placebo in time on Tambopata alone: every 2019-21 year below every 2011-18 year?
    w = _w(ru, "net")[T]
    a, b = D.PERIODS["during"]
    reg.add("tambopata_bz_net_max_during", w.loc[a:b].max(), "ha/yr", "Largest yearly net addition, Tambopata buffer "
            "zone, 2019–21", "description", SRC, measure="net", zone=T, period="2019–21")
    reg.add("tambopata_bz_net_min_2011_18", w.loc[2011:2018].min(), "ha/yr", "Smallest yearly net addition, Tambopata "
            "buffer zone, 2011–18", "description", SRC, measure="net", zone=T, period="2011–18")
    print("\n2x2 (ha/yr):\n", tab.pivot_table(index="design", columns="measure", values="did").round(0).to_string())
    return tab


# ----------------------------------------------------------------------------- displacement
def displacement(ru, reg):
    """Madre de Dios's net additions by zone (only the parts inside the department), so the zones sum to the total."""
    z = pd.read_csv(Z.INTER / "zone_year.csv")
    z = z[z.in_mdd == 1].groupby(["year", "zone"], as_index=False)[["net_ha", "new_ha", "remined_ha", "stopped_ha"]].sum()
    tot = z.groupby("year")[["net_ha"]].sum()
    mdd = ru[ru.unit == "mdd"].set_index("year")
    assert (tot.net_ha - mdd.net_ha).abs().max() < 0.01
    rows = []
    for zk, d in z.groupby("zone"):
        d = d.set_index("year")
        for p in ("pre", "during", "later"):
            rows.append(dict(zone=zk, zone_name=D.ZONE_NAME[zk], period=D.period_label(p),
                             **{m: Z.period_mean(d[D.COLS[m]], p) for m in MEAS}))
    t = pd.DataFrame(rows)
    t.round(1).to_csv(OUT / "peru_displacement_by_zone.csv", index=False)
    piv = t.pivot_table(index="zone", columns="period", values="net")
    chg = piv[D.period_label("during")] - piv[D.period_label("pre")]
    for zk, v in chg.items():
        reg.add(f"mdd_part_{zk}_net_change_during", v, "ha/yr", f"Change in mean net additions 2016–18 to 2019–21, "
                f"{D.ZONE_NAME[zk]} (part inside Madre de Dios)", "description", SRC, measure="net", zone=zk,
                period="2016–18 vs 2019–21")
    out = chg.drop(["lapampa", "tambopata_bz_rest"]).clip(lower=0).sum()
    reg.add("mdd_rise_elsewhere_vs_tambopata_fall", out / -chg[["lapampa", "tambopata_bz_rest"]].sum(), "ratio",
            "Sum of increases in mean net additions in other Madre de Dios zones, divided by the Tambopata buffer "
            "zone's fall (2016–18 to 2019–21). Above 1: not all of the rise can be miners who left.",
            "description", SRC, measure="net", zone="mdd", period="2016–18 vs 2019–21")
    print("\nDisplacement, change in mean net additions 2016-18 -> 2019-21 (ha/yr):\n", chg.round(0).to_string())
    return t


# ----------------------------------------------------------------------------- event study (national panel)
def beta(wide: pd.DataFrame, treated: str) -> pd.Series:
    """One treated unit, equal weights: b_k = (y_T,k - mean_c y_c,k) - (y_T,ref - mean_c y_c,ref)."""
    w = wide.loc[Y0:Y1]
    gap = w[treated] - w.drop(columns=treated).mean(axis=1)
    return (gap - gap.loc[D.REF_YEAR]).drop(D.REF_YEAR)


def pools():
    bz = Z.bz_panel()
    net = Z.wide(bz, "net_ha")
    a, b = D.PERIODS["pre_long"]
    nz = net.loc[a:b].abs().sum() > 0
    poolB = sorted(nz[nz].index)                                    # every buffer zone with pre-2019 mining
    poolA = [u for u in ("tambopata_bz", "amarakaeri_bz", "bahuaja_bz") if u in poolB]   # Madre de Dios-linked
    return bz, poolA, poolB


def event_study(reg):
    bz, poolA, poolB = pools()
    n = len(poolB)
    W = {m: Z.wide(bz, D.COLS[m]) for m in MEAS}
    bA = {m: beta(W[m][poolA], T) for m in MEAS}
    bB = {m: beta(W[m][poolB], T) for m in MEAS}
    # pyfixest check: the saturated TWFE equals the closed form (net, pool B)
    d = W["net"].loc[Y0:Y1, poolB].reset_index().melt(id_vars="year", var_name="unit", value_name="y")
    ks = [k for k in range(Y0, Y1 + 1) if k != D.REF_YEAR]
    for k in ks:
        d[f"d{k}"] = ((d.year == k) & (d.unit == T)).astype(int)
    fit = pf.feols("y ~ " + " + ".join(f"d{k}" for k in ks) + " | unit + year", data=d)
    assert np.allclose([fit.coef()[f"d{k}"] for k in ks], bB["net"].values, atol=1e-4)
    for k in ks:
        assert abs(bB["net"][k] - (bB["new"][k] + bB["remined"][k] - bB["stopped"][k])) < 0.01
    pd.DataFrame({f"{p}_{m}": b[m] for p, b in (("poolA", bA), ("poolB", bB)) for m in MEAS}).rename_axis("year") \
        .round(2).to_csv(OUT / "peru_event_study.csv")
    for k in range(2014, 2026):
        if k == D.REF_YEAR:
            continue
        Z.register_parts(reg, f"es_poolB_{k}", {m: bB[m][k] for m in MEAS}, T, str(k),
                         f"event-study coefficient (ref {D.REF_YEAR}), Tambopata buffer zone vs {n-1} buffer zones "
                         "with pre-2019 mining, equal weights; point estimate only")
        Z.register_parts(reg, f"es_poolA_{k}", {m: bA[m][k] for m in MEAS}, T, str(k),
                         f"event-study coefficient (ref {D.REF_YEAR}), Tambopata vs Amarakaeri and Bahuaja-Sonene "
                         "buffer zones")
    # pooled-reference version (review D-S3-2): reference = mean of 2014-18 instead of 2018 alone
    w = W["net"].loc[Y0:Y1, poolB]
    gap = w[T] - w.drop(columns=T).mean(axis=1)
    a, b = D.PERIODS["pre_long"]; c, e = D.PERIODS["during"]
    pooled = gap.loc[c:e].mean() - gap.loc[a:b].mean()
    reg.add("es_poolB_pooledref_during_net", pooled, "ha/yr", "Mean event-study gap 2019–21 minus mean gap 2014–18, "
            f"Tambopata buffer zone vs {n-1} buffer zones (pooled reference)", "description", SRC, measure="net",
            zone=T, period="2019–21 vs 2014–18")

    # placebo in space: each zone in turn, Tambopata removed from the donors; raw and scaled by own pre mean
    noT = [u for u in poolB if u != T]
    pre = W["net"].loc[a:b, poolB].mean()

    def stat(u, yrs, units):
        bb = beta(W["net"][units], u)
        return bb.loc[yrs[0]:yrs[1]].mean()
    real = stat(T, D.PERIODS["during"], poolB)
    fake = {u: stat(u, D.PERIODS["during"], noT) for u in noT}
    rank_raw = placebo_rank(real, fake.values())
    big = [u for u in poolB if pre[u] > D.MIN_PRE_HA]
    rank_sc = placebo_rank(real / pre[T], [fake[u] / pre[u] for u in big if u != T])
    reg.add("placebo_space_rank_raw", rank_raw, "rank", f"Rank of the Tambopata buffer zone among {n} buffer zones "
            "(1 = most negative) in the mean 2019–21 event-study coefficient on net additions, each zone treated in "
            "turn. Measures size as much as effect: see the pre-year ranks.", "description", SRC, measure="net",
            zone=T, period="2019–21")
    reg.add("placebo_space_n", n, "count", "Buffer zones in the placebo pool (pre-2019 mining)", "description", SRC)
    reg.add("placebo_space_rank_scaled", rank_sc, "rank", f"Same rank with each zone's coefficient divided by its own "
            f"mean net additions 2014–18, zones above {D.MIN_PRE_HA:g} ha/yr only ({len(big)} zones)", "description",
            SRC, measure="net", zone=T, period="2019–21")
    reg.add("placebo_space_n_scaled", len(big), "count", "Zones in the scaled placebo pool", "description", SRC)
    # review X1: the same raw rank in pre-years (fake event years 2014, 2015, 2016, 2017: single-year coefficient)
    for y in (2014, 2015, 2016, 2017):
        r = placebo_rank(beta(W["net"][poolB], T)[y], [beta(W["net"][noT], u)[y] for u in noT])
        reg.add(f"placebo_space_rank_raw_preyear_{y}", r, "rank", f"Raw placebo-in-space rank of the Tambopata buffer "
                f"zone's {y} coefficient (before Mercurio): rank 1 here shows the raw rank measures size",
                "description", SRC, measure="net", zone=T, period=str(y))
    print(f"Placebo in space (net): rank {rank_raw}/{n} raw, {rank_sc}/{len(big)} scaled")
    a_, b_ = D.PERIODS["during"]
    reg.add("es_poolB_min_during_net", bB["net"].loc[a_:b_].min(), "ha/yr", "Lowest yearly event-study coefficient "
            f"2019–21 (ref {D.REF_YEAR}), Tambopata buffer zone vs {n-1} buffer zones, net additions (figure title)",
            "description", SRC, measure="net", zone=T, period="2019–21")
    fig_event_study(bB, bA, W, poolB, n)
    return bB


# ----------------------------------------------------------------------------- figures
def fig_event_study(bB, bA, W, poolB, n):
    yrs = sorted(bB["net"].index)
    fig, (ax, ax2) = plt.subplots(2, 1, figsize=(9, 7.6), sharex=True,
                                  gridspec_kw={"height_ratios": [1.4, 1], "hspace": 0.38})
    lo = bB["net"].loc[D.PERIODS["during"][0]:D.PERIODS["during"][1]].min()
    headline(fig, f"Net additions in the Tambopata buffer zone fell to {lo:,.0f} ha below the comparison in 2019–21"
             .replace("-", "−"),
             f"Event-study coefficient vs {n-1} Peruvian buffer zones with mining, relative to {D.REF_YEAR}, "
             "and its three parts (ha/yr)")
    ax.axhline(0, color=INK2, lw=0.9)
    for m, c, lw in (("new", PART_C["new"], 1.4), ("remined", PART_C["remined"], 1.4)):
        ax.plot(x_of(yrs), bB[m].loc[yrs], color=c, lw=lw, marker="o", ms=3.5, mec="white", alpha=0.9)
        label_end(ax, yrs[-1], bB[m].loc[yrs[-1]], D.MEASURE_NAME[m].split(" (")[0], c, weight="normal")
    ax.plot(x_of(yrs), -bB["stopped"].loc[yrs], color=PART_C["stopped"], lw=1.4, marker="o", ms=3.5, mec="white")
    label_end(ax, yrs[-1], -bB["stopped"].loc[yrs[-1]], "− Stopped", PART_C["stopped"], weight="normal")
    ax.plot(x_of(yrs), bB["net"].loc[yrs], color=INK, lw=2.4, marker="o", ms=5.5, mec="white", zorder=5)
    label_end(ax, yrs[-1], bB["net"].loc[yrs[-1]], "Net additions", INK, dy=10)
    ax.scatter([D.REF_YEAR], [0], s=40, facecolors="white", edgecolors=INK, lw=1.1, zorder=6)
    ax.set_ylabel("ha/yr vs comparison, relative to 2018")
    ax.set_title("Net = new + re-mined − stopped (one treated zone: no confidence intervals)", pad=EVENT_TITLE_PAD)
    add_event_markers(ax, label=True)
    xs = x_of(range(Y0, Y1 + 1))
    for u, c, nm in ((T, C["lapampa"], "Tambopata buffer zone"), (A, C["buffer"], "Amarakaeri buffer zone")):
        ax2.plot(xs, W["net"].loc[Y0:Y1, u], color=c, marker="o", mec="white", mew=0.8)
        label_end(ax2, Y1, W["net"].loc[Y1, u], nm, c, dx=8)
    ax2.set_ylabel("Net additions, ha/yr")
    ax2.set_title("What the coefficients are made of: net additions in the two Madre de Dios buffer zones")
    add_event_markers(ax2)
    for a_ in (ax, ax2):
        style_axes(a_)
    ax2.set_xlim(Y0 - 0.6, Y1 + 0.6)
    set_year_ticks(ax2, range(Y0, Y1 + 1))
    finish_figure(fig, f"{SRC}. Equal-weight comparison of {n-1} buffer zones with pre-2019 mining. Description, "
                  "not causal.", OUT / "fig_peru_event_study.png", event_note=True)


def fig_additions(ru, pack):
    """Net additions of the Tambopata buffer zone as stacked parts, Amarakaeri, and the department."""
    pr = pack["prices"].set_index("year")["gold"]
    yrs = list(range(Y0, Y1 + 1)); xs = x_of(yrs)
    W = {m: _w(ru, m) for m in MEAS}
    fig, axes = plt.subplots(3, 1, figsize=(9, 9), sharex=True, gridspec_kw={"height_ratios": [1.6, 1.2, 0.8], "hspace": 0.4})
    a1, a2, a3 = axes
    headline(fig, "Tambopata's net additions fell in 2019–21 because new land halved and stopped land doubled",
             "Net mining additions (ha/yr) = new land + re-mined − stopped, MapBiomas rasters, 2014–2025")
    period_band(a1, D.PERIODS["during"][0] - 0.5, D.PERIODS["during"][1] + 0.5, "Mercurio and what followed (2019–21)")
    for m, sgn in (("new", 1), ("remined", 1), ("stopped", -1)):
        bottom = W["new"].loc[yrs, T] if m == "remined" else 0
        a1.bar(xs, sgn * W[m].loc[yrs, T], bottom=bottom, color=PART_C[m], width=0.7, alpha=0.85,
               label=("− " if sgn < 0 else "") + D.MEASURE_NAME[m])
    a1.plot(xs, W["net"].loc[yrs, T], color=INK, marker="o", mec="white", lw=2.2, label="Net additions")
    a1.legend(loc="upper left", ncol=2, fontsize=8, frameon=False)
    a1.set_ylabel("ha/yr"); a1.set_title("Tambopata buffer zone: net and its parts", pad=EVENT_TITLE_PAD)
    for u, c in ((A, C["buffer"]), ("corridor_across", C["corridor"]), ("lapampa", C["lapampa"])):
        a2.plot(xs, W["net"].loc[yrs, u], color=c, marker="o", mec="white", mew=0.8)
        label_end(a2, Y1, W["net"].loc[Y1, u], D.UNIT_NAME[u], c, dx=8)
    a2.set_ylabel("Net additions, ha/yr"); a2.set_title("La Pampa sector, Amarakaeri buffer zone, corridor across the road")
    a3.plot(xs, W["net"].loc[yrs, "mdd"], color=INK, marker="o", mec="white")
    label_end(a3, Y1, W["net"].loc[Y1, "mdd"], "Madre de Dios", INK, dx=8)
    a3.set_ylabel("Net additions, ha/yr"); a3.set_title("The whole department (no fall)")
    for i, a in enumerate(axes):
        style_axes(a); add_event_markers(a, label=(i == 0))
    a3.set_xlim(Y0 - 0.6, Y1 + 0.6); set_year_ticks(a3, yrs)
    finish_figure(fig, f"{SRC}. River dredging and mercury are invisible. Description.", OUT / "fig_peru_additions.png",
                  event_note=True)


# ----------------------------------------------------------------------------- entry point
def run(pack, reg):
    print("\n== Peru core analysis (v3: net additions, raster registry) ==")
    ru, pm = describe(reg)
    did_tab = compare(ru, reg)
    disp = displacement(ru, reg)
    es = event_study(reg)
    gp = pack["prices"].set_index("year")["gold"]
    for yr in (2018, 2022, 2023, 2025):
        reg.add(f"gold_price_{yr}", gp[yr], "USD/oz", f"Gold price, annual mean, nominal, {yr} ({SRC_PRICE})",
                "description", "prices_annual.csv", measure="price", zone="world", period=str(yr))
    reg.add("gold_price_ratio_2025_2018", gp[2025] / gp[2018], "ratio", "Gold price 2025 divided by 2018",
            "description", "prices_annual.csv", measure="price", zone="world", period="2018-2025")
    fig_additions(ru, pack)
    return dict(units=ru, period_means=pm, did=did_tab, displacement=disp, event=es)
