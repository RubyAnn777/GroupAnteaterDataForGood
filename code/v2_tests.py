"""Tests the team asked for (plan v3: net additions, zone registry, one treatment). DESCRIPTION unless stated.

Outcome: net mining additions (new + re-mined - stopped), MapBiomas Peru Col 4 rasters, our pixel accounting; shares
and ratios say which measure they use. Zones: definitions.ZONES via zonedata.py; windows: definitions.PERIODS.

  T1 Crossing the road, fake dates: share of land added north of the highway (La Pampa longitudes, all 1-km bands
     -30..+30 km), 3 years from the start year minus the 3 before, for every start year 2008-2022. Run on new land
     (first-time mining; the share is stable because new land is never negative) and on net additions.
  T2 Same for the registry pair La Pampa sector vs corridor across the road.
  T3 Asner & Tupayachi (2017) report a dip in La Pampa's mining in 2012-13 (decrees and interdictions). NOT a treatment
     in our design: we only check whether OUR data show that pattern. Zone + year effects on the national buffer-zone
     panel (raster net additions, zonedata.bz_panel), Tambopata BZ x 2012-13 and x 2014-16, data 2008-2016; placebo
     in space with Tambopata removed from every placebo's comparison pool; common.placebo_rank.
  T4 La Pampa boundary sensitivity: narrow / main / wide longitude windows (zone_year_lp_alt.csv), net and parts.
  T5 Products: Tambopata buffer zone, net additions and parts (raster, same as peru.py) vs Amazon Mining Watch new
     area (480 m patches; no "stopped" state, so never compared with net in one number).
  T6 Boundary dates: when each buffer zone was approved (SERNANP za_felea) and the corridor (D.L. 1100, 2012).
  T7 Presumed-illegal share: additions on land with tenure "none" (outside the corridor and native communities), net
     and new land, ratio of period sums.
  T8 Enforcement intensity: MEF budget programme PP 0128 executed spending (devengado), Madre de Dios, 2015-2025
     (department level only; national units book under Lima, so a lower bound). Check: 2019 = 31,120,611 soles.
  T9 Depth of new land north of the highway (new-land-weighted mean distance; a ratio, so new land only).
"""
from __future__ import annotations
import glob
import re
import warnings
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pyfixest as pf

from common import (ROOT, OUT, style_axes, finish_figure, headline, label_end, callout, period_band, placebo_rank,
                    add_event_markers, PERU_EVENTS, EVENT_TITLE_PAD, C, INK, INK2, MUTED, AXIS)
import definitions as D
import zonedata as Z
import raster_zones as rz
import checks

SRC_R = f"{D.SOURCE}, zone registry"
SRC_MEF = "MEF Consulta Amigable, PP 0128 Reduccion de la mineria ilegal, devengado by Departamento (Meta)"
MEAS = ["net"] + D.PARTS
PER = ("pre", "during", "later")
REAL = D.FIRST_POST


def shift_test(series_share: pd.Series, real=REAL, k=3, starts=range(2008, 2023)):
    """Mean of the k years from each start year minus the k before. Returns (shifts, rank of the real start among all
    start years, n). Rank 1 = biggest move north (common.placebo_rank on the negated shifts)."""
    out = {}
    for t in starts:
        pre, post = series_share.loc[t - k:t - 1], series_share.loc[t:t + k - 1]
        if len(pre) == k and len(post) == k:
            out[t] = post.mean() - pre.mean()
    s = pd.Series(out)
    return s, placebo_rank(-s[real], -s.drop(real)), len(s)


def _clean(s: pd.Series, k=3) -> pd.Series:
    """Start years whose windows do not overlap the real one (real +- k years), plus the real start."""
    return s[(s.index <= REAL - 2 * k) | (s.index >= REAL + k) | (s.index == REAL)]


def t1_t2(reg):
    b = pd.read_csv(rz.OUT_BAND)
    res = {}
    for m in ("new", "net"):
        w = b.pivot_table(index="year", columns="km_from_road", values=D.COLS[m], aggfunc="sum").fillna(0)
        north = w[[c for c in w if c >= 0]].sum(axis=1); tot = w.sum(axis=1)
        share = (north / tot).loc[2005:2025]
        s, rank, n = shift_test(share)
        cl = _clean(s); rank_c = placebo_rank(-cl[REAL], -cl.drop(REAL)); n_c = len(cl)
        res[m] = (share, s, rank, n, rank_c, n_c)
        kw = dict(measure=m, zone="road bands, La Pampa longitudes, -30..+30 km")
        nm = D.MEASURE_NAME[m].lower()
        reg.add(f"t1_road_shift_rank_clean_{m}", rank_c, "rank", f"Rank of the 2019 move north ({nm}) among start years "
                "whose 3-year windows do not overlap the event (2008-13, 2022, and 2019); 1 = biggest", "description",
                SRC_R, **kw, period="start years 2008-2022")
        reg.add(f"t1_road_shift_n_clean_{m}", n_c, "count", "Start years in the clean comparison", "description", SRC_R)
        reg.add(f"t1_road_shift_ri_p_clean_{m}", rank_c / n_c, "p-value", f"Randomization p-value, non-overlapping "
                f"windows ({nm})", "description", SRC_R, **kw, period="start years 2008-2022")
        reg.add(f"t1_road_shift_2019_{m}", s[REAL], "share points", f"Shift in the north-of-road share of {nm}, 3 yrs "
                "from 2019 minus 3 yrs before", "description", SRC_R, **kw, period="2019-21 vs 2016-18")
        reg.add(f"t1_road_shift_rank_{m}", rank, "rank", f"Rank of the 2019 shift ({nm}) among {n} start years "
                "2008-2022 (1 = biggest move north)", "description", SRC_R, **kw, period="start years 2008-2022")
        reg.add(f"t1_road_shift_ri_p_{m}", rank / n, "p-value", f"Randomization p-value, all start years ({nm})",
                "description", SRC_R, **kw, period="start years 2008-2022")
        for p in PER:
            a, c = D.PERIODS[p]
            v = north.loc[a:c].sum() / tot.loc[a:c].sum()
            reg.add(f"t1_road_north_share_{p}_{m}", v, "share", f"North-of-road share of {nm} (La Pampa longitudes, "
                    f"-30..+30 km), {D.period_label(p)}, period sum / period sum", "description", SRC_R, **kw,
                    period=D.period_label(p))
        for y in (2008, 2010, 2015, 2018, 2021):
            reg.add(f"t1_road_north_share_{y}_{m}", share.loc[y], "share", f"North-of-road share of {nm}, {y}",
                    "description", SRC_R, **kw, period=str(y))
    s = res["new"][1]
    reg.add("t1_road_shift_max_other_new", s.drop(REAL).max(), "share points", "Largest shift north of new land for any "
            "other start year", "description", SRC_R, measure="new", zone="road bands", period="start years 2008-2022")
    reg.add("t1_road_shift_max_other_year_new", s.drop(REAL).idxmax(), "year", "Start year of that largest other shift",
            "description", SRC_R)
    ru = Z.region_units()
    for m in ("new", "net"):
        z = Z.wide(ru, D.COLS[m])
        pair = (z["corridor_across"] / (z["corridor_across"] + z["lapampa"])).loc[2005:2025]
        s2, r2, n2 = shift_test(pair)
        kw = dict(measure=m, zone="corridor_across / (corridor_across + lapampa)", period="2019-21 vs 2016-18")
        reg.add(f"t2_pair_shift_2019_{m}", s2[REAL], "share points", f"Shift in the across-the-road share of the La "
                f"Pampa / across-the-road pair ({D.MEASURE_NAME[m].lower()}), 2019", "description", SRC_R, **kw)
        reg.add(f"t2_pair_shift_rank_{m}", r2, "rank", f"Rank of that 2019 shift among {n2} start years", "description",
                SRC_R, **kw)
    share, s, rank, n, rank_c, n_c = res["new"]
    sn = res["net"]
    fig, ax = plt.subplots(figsize=(9, 4.4))
    ttl = (f"No clean fake start date moves new land across the road as much as 2019" if rank_c == 1 else
           f"Fake start dates: 2019's move of new land across the road ranks {rank_c} of {n_c}")
    headline(fig, ttl, "Change in the share of new land (first-time mining) north of the highway, La Pampa longitudes, "
                       "3 years from the start minus 3 before, % points")
    overlap = [t for t in s.index if REAL - 3 <= t <= REAL + 2 and t != REAL]
    cols = [C["corridor"] if t == REAL else ("#d9d6cf" if t in overlap else C["other"]) for t in s.index]
    ax.bar(s.index, s.values * 100, color=cols, width=0.72)
    ax.axhline(0, color=INK2, lw=0.8)
    period_band(ax, min(overlap) - 0.5, max(overlap) + 0.5, None, color="#f4f2ed")
    ax.text(REAL - 0.5, 0.04, "Pale bars: windows overlap the real event", transform=ax.get_xaxis_transform(),
            ha="center", va="bottom", fontsize=7.5, color=INK2)
    callout(ax, REAL, s[REAL] * 100, f"Real start 2019\n{s[REAL] * 100:+.0f} pts", dx=-46, dy=10, ha="center")
    callout(ax, 2008, s[2008] * 100, "2008: the Guacamayo\nboom north of the road", dx=40, dy=12, ha="left")
    ax.text(0.01, 0.97, f"New land, clean start years (grey + 2019): rank {rank_c} of {n_c}, p = {rank_c / n_c:.2f}; "
            f"all: rank {rank} of {n}\nNet additions: clean rank {sn[4]} of {sn[5]}; all: rank {sn[2]} of {sn[3]}",
            transform=ax.transAxes, ha="left", va="top", fontsize=7.5, color=INK2, linespacing=1.4)
    ax.set_ylabel("% points")
    ax.set_xticks(list(s.index)); ax.set_xticklabels([f"'{str(t)[2:]}" for t in s.index])
    ax.set_xlabel("Fake (or real) start year")
    style_axes(ax)
    ax.set_ylim(min(s.min() * 100 * 1.15, -10), s.max() * 100 * 1.25)
    finish_figure(fig, f"{SRC_R}. Each bar: share of new land north of the highway (La Pampa longitudes, all 1-km bands "
                       "from 30 km south to 30 km north), mean of the 3 years from the start year minus mean of the 3 years "
                       "before. Description.", OUT / "fig_v2_road_placebo.png")
    return s, rank, n


def t3(pack, reg):
    """Asner & Tupayachi (2017)'s 2012-13 pattern, checked in our data (raster net additions, national BZ panel)."""
    bz = Z.bz_panel()
    W = {m: Z.wide(bz, D.COLS[m]).loc[2008:2016] for m in MEAS}
    pool = sorted(u for u in W["net"].columns if W["net"].loc[2008:2011, u].abs().sum() > 0)
    T = D.TREATED_ZONE

    def fit(units, treated, m="net"):
        d = W[m][units].reset_index().melt(id_vars="year", var_name="unit", value_name="y")
        d["w1213"] = (d.unit.eq(treated) & d.year.between(2012, 2013)).astype(int)
        d["w1416"] = (d.unit.eq(treated) & d.year.between(2014, 2016)).astype(int)
        f = pf.feols("y ~ w1213 + w1416 | unit + year", data=d)
        return f.coef()
    real = {m: fit(pool, T, m) for m in MEAS}
    for k in ("w1213", "w1416"):
        assert abs(real["net"][k] - (real["new"][k] + real["remined"][k] - real["stopped"][k])) < 0.01
    noT = [u for u in pool if u != T]
    fake = [fit(noT, u)["w1213"] for u in noT]
    rank = placebo_rank(real["net"]["w1213"], fake)
    lab = "Asner & Tupayachi (2017)'s reported 2012-13 dip, checked in our data (not a treatment in our design)"
    Z.register_parts(reg, "t3_asner_2012_13", {m: real[m]["w1213"] for m in MEAS}, T, "2012–13 vs 2008–11",
                     f"zone + year effects, {len(pool)} buffer zones with 2008-11 mining, data 2008-2016: {lab}", source=SRC_R)
    Z.register_parts(reg, "t3_asner_2014_16", {m: real[m]["w1416"] for m in MEAS}, T, "2014–16 vs 2008–11",
                     "same model, Tambopata buffer zone x 2014-16", source=SRC_R)
    reg.add("t3_asner_rank", rank, "rank", f"Rank of the Tambopata buffer zone's 2012-13 coefficient (net) among "
            f"{len(pool)} zones, each treated in turn with Tambopata removed from the comparison (1 = most negative)",
            "description", SRC_R, measure="net", zone=T, period="2012–13 vs 2008–11")
    reg.add("t3_asner_n", len(pool), "count", "Buffer zones in the 2012-13 check", "description", SRC_R)
    t = W["net"][T]
    for y in range(2010, 2016):
        reg.add(f"t3_tam_net_{y}", t.loc[y], "ha/yr", f"Net mining additions, Tambopata buffer zone, {y}", "description",
                SRC_R, measure="net", zone=T, period=str(y))
    return real["net"], rank, len(pool)


def t4(reg):
    alt = pd.read_csv(rz.OUT_ALT)
    ru = Z.region_units()
    main = ru[ru.unit.isin(["lapampa", "corridor_across"])].rename(columns={"unit": "zone"}).assign(definition="main")
    d = pd.concat([alt[alt.zone.isin(["lapampa", "corridor_across"])], main])
    rows = []
    for (df_, u), g in d.groupby(["definition", "zone"]):
        g = g.set_index("year")
        rec = dict(definition=df_, zone=u)
        for p in ("pre", "during", "later"):
            for m in MEAS:
                rec[f"{m}_{p}"] = Z.period_mean(g[D.COLS[m]], p)
        rows.append(rec)
        win = D.LP_LON if df_ == "main" else D.LP_ALT[df_]
        for p in ("pre", "during"):
            Z.register_parts(reg, f"t4_{u}_{df_}_{p}", {m: rec[f"{m}_{p}"] for m in MEAS}, u, D.period_label(p),
                             f"mean per year, La Pampa longitude window '{df_}' {win} (boundary sensitivity)", source=SRC_R)
        for m in ("net", "new"):
            reg.add(f"t4_{u}_{df_}_change_{m}", rec[f"{m}_during"] / rec[f"{m}_pre"] - 1, "share",
                    f"{D.ZONE_NAME[u]}, '{df_}' window {win}: relative change in {D.MEASURE_NAME[m].lower()}, 2016–18 "
                    "to 2019–21", "description", SRC_R, measure=m, zone=u, period="2016–18 vs 2019–21")
    t = pd.DataFrame(rows); t.round(0).to_csv(OUT / "v2_lapampa_sensitivity.csv", index=False)
    return t


def t5(pack, reg):
    ru = Z.region_units()
    o = ru[ru.unit == D.TREATED_ZONE].set_index("year")
    amw = pd.read_csv(ROOT / "data_intermediate" / "amw_candidates_year.csv")
    a = amw[amw.unit_id == "PE-BZ-RN09"].set_index("year").new_ha
    rows = [(f"Raster: {D.MEASURE_NAME[m]}", *(Z.period_mean(o[D.COLS[m]], p) for p in PER)) for m in MEAS]
    rows.append(("Amazon Mining Watch: new area (480 m patches; 2018 = stock; no 'stopped' state)", np.nan,
                 Z.period_mean(a, "during"), Z.period_mean(a, "later")))
    t = pd.DataFrame(rows, columns=["measure"] + [D.period_label(p) for p in PER])
    t.round(0).to_csv(OUT / "v2_products_tambopata.csv", index=False)
    for p in ("during", "later"):
        reg.add(f"t5_amw_tambopata_bz_{p}", Z.period_mean(a, p), "ha/yr", f"Amazon Mining Watch new area, Tambopata "
                f"buffer zone, mean {D.period_label(p)} (another product: not net additions)", "description",
                "Amazon Mining Watch (amw_candidates_year.csv)", measure="amw_new_area", zone=D.TREATED_ZONE,
                period=D.period_label(p))
    return t


def t6(reg):
    import geopandas as gpd
    za = gpd.read_file(ROOT / "data_raw/sernanp/zonas_amortiguamiento.geojson")
    for code, nm in (("RN09", "tambopata"), ("RC03", "amarakaeri"), ("PN08", "bahuajasonene")):
        r = za[za.anp_codi == code].iloc[0]
        y = pd.to_datetime(r.za_felea, unit="ms").year if pd.notna(r.za_felea) else np.nan
        reg.add(f"t6_bz_approved_{nm}", y, "year", f"Year the current {nm} buffer zone was approved (SERNANP za_felea, {r.za_balea})", "description", "SERNANP zonas_amortiguamiento")


def t7(reg):
    z = pd.read_csv(rz.OUT_ZONE)
    z = z[z.in_mdd == 1]
    out = {}
    for m in ("net", "new"):
        tot = z.groupby("year")[D.COLS[m]].sum()
        ill = z[z.tenure == "none"].groupby("year")[D.COLS[m]].sum()
        out[m] = ill / tot
        for p in PER:
            a, b = D.PERIODS[p]
            reg.add(f"t7_presumed_illegal_share_{p}_{m}", ill.loc[a:b].sum() / tot.loc[a:b].sum(), "share",
                    f"Share of Madre de Dios {D.MEASURE_NAME[m].lower()} on land outside the legal corridor AND outside "
                    f"native communities (tenure 'none', presumed illegal), {D.period_label(p)}, period sum / period sum",
                    "description", SRC_R, measure=m, zone="mdd", period=D.period_label(p))
    pd.DataFrame(out).round(3).to_csv(OUT / "v2_presumed_illegal_share.csv")
    return out["net"]


def mef_series():
    rows = {}
    for f in sorted(glob.glob(str(ROOT / "data_raw/enforcement_peru/mef_pp0128/*.html"))):
        y = int(re.search(r"(\d{4})\.html$", f).group(1))
        for t in pd.read_html(f):
            hit = t[t.apply(lambda r: r.astype(str).str.contains("MADRE DE DIOS").any(), axis=1)]
            if len(hit):
                # columns: 1 name | 2 PIA | 3 PIM | 4 certificacion | 5 compromiso anual | 6 atencion compromiso mensual
                #          | 7 DEVENGADO | 8 girado | 9 avance %   (checked against the Consulta Amigable screen, 2019)
                rows[y] = float(str(hit.iloc[0][7]).replace(",", ""))
                break
    return pd.Series(rows)


def t8(reg):
    s = mef_series()
    if s.empty:
        warnings.warn("v2_tests: MEF pages missing"); return
    checks.check("MEF PP 0128 devengado, Madre de Dios, 2019, soles (Consulta Amigable screen 31,120,611)", s[2019], 31120611, tol=1)
    checks.save()
    s = s.loc[2015:2025]
    for y, v in s.items():
        reg.add(f"t8_pp0128_mdd_{y}", v, "soles", f"PP 0128 executed spending (devengado) booked in Madre de Dios, {y} (lower bound)", "description", SRC_MEF)
    zz = pd.read_csv(rz.OUT_ZONE)
    z = zz[zz.in_mdd == 1].groupby("year").net_ha.sum().loc[2015:2025]
    fig, (a1, a2) = plt.subplots(2, 1, figsize=(9, 5.8), sharex=True, gridspec_kw={"hspace": 0.45})
    sm = s / 1e6
    pk = int(sm.idxmax())
    grew = z.loc[D.PERIODS["later"][0]:].mean() > z.loc[D.PERIODS["pre"][0]:D.PERIODS["pre"][1]].mean()
    headline(fig, f"Enforcement money peaked in {pk} and faded; net mining additions " + ("kept growing" if grew else "fell"),
             "Madre de Dios, 2015–2025. Two measures, two units: side by side, never one as the cause of the other.")
    a1.bar(s.index, sm.values, color=INK2, width=0.68)
    callout(a1, pk, sm[pk], f"{sm[pk]:.1f} M", dy=4, arrow=False)
    callout(a1, s.index[-1], sm.iloc[-1], f"{sm.iloc[-1]:.1f} M", dy=4, arrow=False)
    a1.set_ylim(0, sm.max() * 1.22); style_axes(a1)
    a2.bar(z.index, z.values, color=C["other"], width=0.68)
    a2.set_title("Net mining additions (new + re-mined − stopped), all of Madre de Dios, ha/yr")
    pz = int(z.idxmax())
    callout(a2, pz, z[pz], f"{z[pz]:,.0f} ha", dy=4, arrow=False)
    callout(a2, D.FIRST_POST, z[D.FIRST_POST], f"{z[D.FIRST_POST]:,.0f} ha", dy=4, arrow=False)
    a2.set_ylim(0, z.max() * 1.18); style_axes(a2)
    a2.set_xticks(list(s.index))
    for ax in (a1, a2):
        add_event_markers(ax, label=ax is a1)
    a1.set_title("Anti-illegal-mining spending (PP 0128, executed), million soles", pad=EVENT_TITLE_PAD)
    finish_figure(fig, f"Sources: {SRC_MEF} (lower bound: national units book spending under Lima); {SRC_R}. Description.",
                  OUT / "fig_v2_enforcement_spending.png", event_note=True)
    return s


def run(pack, reg):
    print("\n== v2 tests (fake dates, 2012 wave, sensitivity, products, boundaries, illegal share, spending) ==")
    if not rz.OUT_ZONE.exists():
        warnings.warn("v2_tests: intermediates missing; skipping"); return
    s, rank, n = t1_t2(reg)
    print(f"T1 road shift 2019 (new land) = {s[REAL]:.3f}, rank {rank}/{n}")
    real, r3, n3 = t3(pack, reg); print("T3", real, r3, n3)
    print(t4(reg).round(0).to_string(index=False))
    print(t5(pack, reg).round(0).to_string(index=False))
    t6(reg); il = t7(reg); print("T7", il.loc[2014:].round(2).to_dict())
    print("T8", t8(reg))
    print("T9 depth break", t9_depth(reg).params.round(2).to_dict())
    return s


def t9_depth(reg):
    """Meeting 12 Oct: how deep into the legal zone does new mining go? North side of the highway, La Pampa longitudes,
    first-time mined land by depth band (0-10, 10-20, 20-30 km), and the mean depth per year; break after 2019 tested
    with OLS + Newey-West errors (trend + post-2019 dummy, 2008-2025)."""
    import statsmodels.api as sm
    b = pd.read_csv(rz.OUT_BAND)
    n = b[b.km_from_road >= 0].copy()
    n["depth"] = pd.cut(n.km_from_road, [-1, 9, 19, 29], labels=["0-10 km", "10-20 km", "20-30 km"])
    w = n.pivot_table(index="year", columns="depth", values="new_ha", aggfunc="sum", observed=False).loc[2008:2025]
    mean_depth = (n.assign(x=(n.km_from_road + 0.5) * n.new_ha).groupby("year").x.sum()
                  / n.groupby("year").new_ha.sum()).loc[2008:2025]
    X = sm.add_constant(pd.DataFrame({"post2019": (mean_depth.index >= D.FIRST_POST).astype(float),
                                      "trend": mean_depth.index - 2008.0}, index=mean_depth.index))
    m = sm.OLS(mean_depth, X).fit(cov_type="HAC", cov_kwds={"maxlags": 2})
    kw = dict(measure="new", zone="road bands north, La Pampa longitudes")
    reg.add("t9_depth_post2019", m.params["post2019"], "km", "Mean distance north of the highway of new land (first-time "
            "mining; a weighted ratio, so new land only): break after 2019 net of trend (Newey-West)", "description",
            SRC_R, **kw, period="2008-2025")
    reg.add("t9_depth_post2019_p", m.pvalues["post2019"], "p-value", "p-value of that break", "description", SRC_R)
    for y in (2016, 2018, 2020, 2022, 2025):
        reg.add(f"t9_depth_{y}", mean_depth.loc[y], "km", f"Mean distance north of the highway of new land, {y}",
                "description", SRC_R, **kw, period=str(y))
    sh = w.div(w.sum(axis=1), axis=0) * 100
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(9, 4.4), gridspec_kw={"wspace": 0.42})
    near = mean_depth.loc[D.FIRST_POST:2021].mean() < mean_depth.loc[2016:D.REF_YEAR].mean()
    headline(fig, "After 2019 new land north of La Pampa was mined " + ("nearer the road at first" if near else
             "deeper in the corridor") + f"; break {m.params['post2019']:+.1f} km",
             "New land (first-time mining) north of the highway, La Pampa longitudes, 2008–2025 (ha/yr by band; mean "
             "distance, km)")
    cols = [C["corridor_rest"], C["corridor"], "#184f95"]
    a1.stackplot(w.index, w.T.values, colors=cols, edgecolor="white", linewidth=0.8)
    cum = w.cumsum(axis=1).loc[2025]
    for i, col in enumerate(w.columns):
        lo = 0 if i == 0 else cum.iloc[i - 1]
        label_end(a1, 2025, (lo + cum.iloc[i]) / 2, str(col), cols[i], dx=5, fontsize=8)
    style_axes(a1); a1.set_xlim(2008, 2025)
    a2.plot(mean_depth.index, mean_depth.values, "-", color=C["corridor"], lw=2.2)
    a2.plot(mean_depth.index, mean_depth.values, "o", color=C["corridor"], ms=4.5, mec="white", mew=1)
    style_axes(a2, fmt=False)
    y20 = mean_depth.loc[2020]
    pv = m.pvalues['post2019']
    callout(a2, 2020, y20, f"Break after 2019: {m.params['post2019']:+.1f} km\nnet of trend ({'p < 0.01' if pv < 0.01 else f'p = {pv:.2f}'})",
            dx=8, dy=-26, ha="left")
    a2.set_ylim(mean_depth.min() - 4.5, mean_depth.max() + 2)
    a2.set_xlim(2007.5, 2025.5)
    for a_, t_ in ((a1, "Hectares per year, by distance band"), (a2, "Mean distance north of the highway, km")):
        a_.set_xticks(range(2008, 2026, 4)); a_.set_xticklabels([str(t) for t in range(2008, 2026, 4)])
        a_.set_title(t_, pad=add_event_markers(a_, label=True))
    finish_figure(fig, f"{SRC_R}. La Pampa longitudes only; first-time mining (new land). Break test: OLS of mean distance "
                       "on a trend and a post-2019 dummy, Newey-West errors, 2008–2025 (18 years). Description.",
                  OUT / "fig_v2_depth.png", event_note=True)
    return m
