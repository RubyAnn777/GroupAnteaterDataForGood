"""Plan v2, steps S4/S5/S7/S8: tests the team will ask for. DESCRIPTION unless stated.

  T1 Crossing the road, fake dates: north-of-road share of first-time mined land (La Pampa longitudes, 0-15 km),
     3 years after minus 3 years before, for every possible start year 2008-2022. Is the 2019 jump unusual?
  T2 Same for the zone pair "La Pampa sector" vs "Corridor across the road" (share of the pair's new land across the road).
  T3 The earlier wave (2012-13 decrees and interdictions; Asner & Tupayachi 2017): model M1 (zone + year effects, 15
     Peruvian buffer zones, course table) with Tambopata x 2012-13 and x 2014-16, data 2008-2016; rank vs fake places.
  T4 La Pampa boundary sensitivity: narrow / main / wide longitude windows.
  T5 Products disagree? Tambopata buffer zone 2016-18 vs 2019-21 in four measures (course table additions, raster
     additions, raster first-time mined land, AMW new area). Never subtracted from each other (rule 6).
  T6 Boundary dates: when each buffer zone was approved (SERNANP za_felea) and the corridor (D.L. 1100, 2012).
  T7 Presumed-illegal share: first-time mined land outside the corridor and outside native communities.
  T8 Enforcement intensity: MEF budget programme PP 0128 executed spending (devengado), Madre de Dios, 2015-2025
     (department level only; national units book under Lima, so a lower bound). Check: 2019 = 31,120,611 soles.
"""
from __future__ import annotations
import glob
import re
import warnings
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from common import (ROOT, OUT, style_axes, finish_figure, headline, label_end, callout, period_band,
                    add_event_markers, PERU_EVENTS, EVENT_TITLE_PAD, C, INK, INK2, MUTED, AXIS)
import raster_zones as rz
import peru_models as pm
import checks

SRC_R = "MapBiomas Peru Col 4 rasters, zones v2"
SRC_T = "peru_bufferzone_year.csv (MapBiomas Peru Col 4)"
SRC_MEF = "MEF Consulta Amigable, PP 0128 Reduccion de la mineria ilegal, devengado by Departamento (Meta)"


def shift_test(series_share: pd.Series, real=2019, k=3, starts=range(2008, 2023)):
    out = {}
    for t in starts:
        pre, post = series_share.loc[t - k:t - 1], series_share.loc[t:t + k - 1]
        if len(pre) == k and len(post) == k:
            out[t] = post.mean() - pre.mean()
    s = pd.Series(out)
    return s, int(s.rank(ascending=False)[real]), len(s)


def t1_t2(reg):
    b = pd.read_csv(rz.OUT_BAND)
    w = b.pivot_table(index="year", columns="km_from_road", values="new_land_ha", aggfunc="sum").fillna(0)
    north = w[[c for c in w if c >= 0]].sum(axis=1); tot = w.sum(axis=1)
    share = (north / tot).loc[2005:2025]
    s, rank, n = shift_test(share)
    # fix after review: windows of start years 2017-2021 overlap the real 2019 event (3 yrs either side), so the real
    # effect leaks into them. Clean comparison = start years whose windows do not overlap 2016-2021.
    clean = s[(s.index <= 2013) | (s.index >= 2022) | (s.index == 2019)]
    rank_c, n_c = int(clean.rank(ascending=False)[2019]), len(clean)
    reg.add("t1_road_shift_rank_clean", rank_c, "rank", "Rank of the 2019 move north among start years whose 3-year windows do not overlap the event (2008-13, 2022, and 2019)", "description", SRC_R)
    reg.add("t1_road_shift_n_clean", n_c, "count", "Start years in the clean comparison", "description", SRC_R)
    reg.add("t1_road_shift_ri_p_clean", rank_c / n_c, "p-value", "Randomization p-value with non-overlapping windows", "description", SRC_R)
    reg.add("t1_road_north_share_2016_18", share.loc[2016:2018].mean(), "share", "North-of-road share of first-time mined land (La Pampa longitudes, +-30 km), 2016-18", "description", SRC_R)
    reg.add("t1_road_north_share_2019_21", share.loc[2019:2021].mean(), "share", "Same, 2019-21", "description", SRC_R)
    reg.add("t1_road_shift_2019", s[2019], "share points", "Shift in north share, 3 yrs after minus 3 yrs before 2019", "description", SRC_R)
    reg.add("t1_road_shift_rank", rank, "rank", f"Rank of the 2019 shift among {n} possible start years 2008-2022 (1 = biggest move north)", "description", SRC_R)
    reg.add("t1_road_shift_n", n, "count", "Number of start years tested", "description", SRC_R)
    reg.add("t1_road_shift_ri_p", rank / n, "p-value", "Randomization (fake start dates) p-value of the 2019 move north = rank / number of start years", "description", SRC_R)
    reg.add("t1_road_shift_max_other", s.drop(2019).max(), "share points", "Largest shift north for any other start year", "description", SRC_R)
    reg.add("t1_road_shift_max_other_year", s.drop(2019).idxmax(), "year", "Start year of that largest other shift", "description", SRC_R)
    reg.add("t1_road_shift_2008", s[2008], "share points", "Shift north for start year 2008 (the Guacamayo boom north of the road)", "description", SRC_R)
    for y in (2008, 2010, 2015, 2018, 2021):
        reg.add(f"t1_road_north_share_{y}", share.loc[y], "share", f"North-of-road share of first-time mined land, {y}", "description", SRC_R)
    z = pd.read_csv(rz.OUT_ZONE).pivot(index="year", columns="unit", values="new_land_ha")
    pair = (z["Corridor across the road"] / (z["Corridor across the road"] + z["La Pampa sector"])).loc[2005:2025]
    s2, r2, n2 = shift_test(pair)
    reg.add("t2_pair_shift_2019", s2[2019], "share points", "Shift in the across-the-road share of the La Pampa / across-the-road pair, 2019", "description", SRC_R)
    reg.add("t2_pair_shift_rank", r2, "rank", f"Rank of that 2019 shift among {n2} start years", "description", SRC_R)
    fig, ax = plt.subplots(figsize=(9, 4.4))
    ttl = (f"No clean fake start date moves mining across the road as much as 2019" if rank_c == 1 else
           f"Fake start dates: 2019's move across the road ranks {rank_c} of {n_c}")
    headline(fig, ttl,
             "Change in the share of first-time mining north of the highway (La Pampa longitudes), 3 years after minus 3 before, % points")
    overlap = [t for t in s.index if 2016 <= t <= 2021 and t != 2019]
    cols = [C["corridor"] if t == 2019 else ("#d9d6cf" if t in overlap else C["other"]) for t in s.index]
    ax.bar(s.index, s.values * 100, color=cols, width=0.72)
    ax.axhline(0, color=INK2, lw=0.8)
    period_band(ax, min(overlap) - 0.5, max(overlap) + 0.5, None, color="#f4f2ed")
    ax.text(2018.5, 0.04, "Pale bars: windows overlap the real event", transform=ax.get_xaxis_transform(),
            ha="center", va="bottom", fontsize=7.5, color=INK2)
    callout(ax, 2019, s[2019] * 100, f"Real start 2019\n{s[2019] * 100:+.0f} pts", dx=-46, dy=10, ha="center")
    callout(ax, 2008, s[2008] * 100, "2008: the Guacamayo\nboom north of the road", dx=40, dy=12, ha="left")
    ax.text(0.01, 0.97, f"Clean start years (grey + 2019): rank {rank_c} of {n_c}, p = {rank_c / n_c:.2f}\n"
            f"All start years: rank {rank} of {n}, p = {rank / n:.2f}", transform=ax.transAxes, ha="left", va="top",
            fontsize=7.5, color=INK2, linespacing=1.4)
    ax.set_ylabel("% points")
    ax.set_xticks(list(s.index)); ax.set_xticklabels([f"'{str(t)[2:]}" for t in s.index])
    ax.set_xlabel("Fake (or real) start year")
    style_axes(ax)
    ax.set_ylim(min(s.min() * 100 * 1.15, -10), s.max() * 100 * 1.25)
    finish_figure(fig, f"{SRC_R}. Each bar: share of first-time mined land north of the highway (La Pampa longitudes, "
                       "within 15 km), mean of the 3 years from the start year minus mean of the 3 years before. Description.",
                  OUT / "fig_v2_road_placebo.png")
    return s, rank, n


def t3(pack, reg):
    ad = pm._zone_adds(pack)
    gold = pack["prices"].set_index("year")["gold"]
    pre = ad.loc[2008:2011].mean()
    pool = sorted(u for u in ad.columns if ad.loc[2008:2011, u].abs().sum() > 0)
    posts = {"wave": (2012, 2013), "rebound": (2014, 2016)}
    real = pm.fit(ad, pool, pm.TU, "M1", 2008, 2016, posts, gold)
    ranks = pd.Series({u: pm.fit(ad, pool, u, "M1", 2008, 2016, posts, gold)["post_wave"] for u in pool}).rank()
    t = ad[pm.TU]
    reg.add("t3_wave_m1_2012_13", real["post_wave"], "ha/yr", f"Tambopata BZ x 2012-13, M1 zone+year effects, {len(pool)} zones with 2008-11 mining, 2008-2016", "description", SRC_T)
    reg.add("t3_wave_m1_2014_16", real["post_rebound"], "ha/yr", "Tambopata BZ x 2014-16 (after the 2012-13 wave), same model", "description", SRC_T)
    reg.add("t3_wave_rank", ranks[pm.TU], "rank", f"Tambopata's rank among {len(pool)} zones for the 2012-13 coefficient (1 = biggest fall)", "description", SRC_T)
    reg.add("t3_wave_n", len(pool), "count", "Zones in the 2012-13 wave model", "description", SRC_T)
    for y in range(2010, 2016):
        reg.add(f"t3_tam_add_{y}", t.loc[y], "ha", f"Tambopata BZ annual addition {y} (course table)", "description", SRC_T)
    return real, ranks[pm.TU], len(pool)


def t4(reg):
    s = pd.read_csv(rz.OUT_SENS)
    main = pd.read_csv(rz.OUT_ZONE).assign(definition="main")
    d = pd.concat([s, main])
    d = d[d.unit.isin(["La Pampa sector", "Corridor across the road"])]
    rows = []
    for (df_, u), g in d.groupby(["definition", "unit"]):
        g = g.set_index("year").new_land_ha
        rows.append(dict(definition=df_, unit=u, p2016_18=g.loc[2016:2018].mean(), p2019_21=g.loc[2019:2021].mean(), p2022_25=g.loc[2022:2025].mean()))
    t = pd.DataFrame(rows); t.round(0).to_csv(OUT / "v2_lapampa_sensitivity.csv", index=False)
    for _, r in t.iterrows():
        key = "lp" if r.unit.startswith("La Pampa") else "across"
        reg.add(f"t4_{key}_{r.definition}_change", r.p2019_21 / r.p2016_18 - 1, "share", f"{r.unit}, {r.definition} boundary: change in first-time mined land 2016-18 -> 2019-21", "description", SRC_R)
    return t


def t5(pack, reg):
    ad = pm._zone_adds(pack)[pm.TU]
    off = pd.read_csv(rz.OUT_OFF); o = off[off.unit == "Tambopata buffer zone"].set_index("year")
    amw = pd.read_csv(ROOT / "data_intermediate" / "amw_candidates_year.csv")
    a = amw[amw.unit_id == "PE-BZ-RN09"].set_index("year").new_ha
    rows = [("Course table: net addition (MapBiomas Peru Col 4)", ad.loc[2016:2018].mean(), ad.loc[2019:2021].mean(), ad.loc[2022:2025].mean()),
            ("Raster: net addition (same product, SERNANP boundary)", o.mining_ha.diff().loc[2016:2018].mean(), o.mining_ha.diff().loc[2019:2021].mean(), o.mining_ha.diff().loc[2022:2025].mean()),
            ("Raster: land mined for the first time", o.new_land_ha.loc[2016:2018].mean(), o.new_land_ha.loc[2019:2021].mean(), o.new_land_ha.loc[2022:2025].mean()),
            ("Raster: return to old pits", o.remined_ha.loc[2016:2018].mean(), o.remined_ha.loc[2019:2021].mean(), o.remined_ha.loc[2022:2025].mean()),
            ("Amazon Mining Watch: new area (480 m patches; 2018 = stock)", np.nan, a.loc[2019:2021].mean(), a.loc[2022:2025].mean())]
    t = pd.DataFrame(rows, columns=["measure", "2016-18", "2019-21", "2022-25"])
    t.round(0).to_csv(OUT / "v2_products_tambopata.csv", index=False)
    for i, r in t.iterrows():
        for c in ("2016-18", "2019-21", "2022-25"):
            if not np.isnan(r[c]):
                reg.add(f"t5_m{i}_{c.replace('-', '_')}", r[c], "ha/yr", f"Tambopata buffer zone, {r.measure}, mean {c}", "description", "see measure")
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
    w = z.pivot(index="year", columns="code", values="new_land_ha").fillna(0)
    illegal = w.drop(columns=[c for c in (3, 4, 5, 6) if c in w]).sum(axis=1) / w.sum(axis=1)
    for p, (a, b) in {"2016_18": (2016, 2018), "2019_21": (2019, 2021), "2022_25": (2022, 2025)}.items():
        reg.add(f"t7_presumed_illegal_share_{p}", illegal.loc[a:b].mean(), "share",
                f"Share of first-time mined land outside the legal corridor AND outside native communities (presumed illegal), {p}", "description", SRC_R)
    illegal.round(3).to_csv(OUT / "v2_presumed_illegal_share.csv")
    return illegal


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
    z = pd.read_csv(rz.OUT_ZONE).groupby("year").new_land_ha.sum().loc[2015:2025]
    fig, (a1, a2) = plt.subplots(2, 1, figsize=(9, 5.8), sharex=True, gridspec_kw={"hspace": 0.45})
    headline(fig, "Enforcement money spiked in 2019 and faded; first-time mining kept growing",
             "Madre de Dios, 2015–2025. Two measures, two units: side by side, never one as the cause of the other.")
    sm = s / 1e6
    a1.bar(s.index, sm.values, color=INK2, width=0.68)
    pk = int(sm.idxmax())
    callout(a1, pk, sm[pk], f"{sm[pk]:.1f} M", dy=4, arrow=False)
    callout(a1, s.index[-1], sm.iloc[-1], f"{sm.iloc[-1]:.1f} M", dy=4, arrow=False)
    a1.set_ylim(0, sm.max() * 1.22); style_axes(a1)
    a2.bar(z.index, z.values, color=C["other"], width=0.68)
    a2.set_title("Land mined for the first time, all of Madre de Dios, hectares")
    pz = int(z.idxmax())
    callout(a2, pz, z[pz], f"{z[pz]:,.0f} ha", dy=4, arrow=False)
    callout(a2, 2019, z[2019], f"{z[2019]:,.0f} ha", dy=4, arrow=False)
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
    print(f"T1 road shift 2019 = {s[2019]:.3f}, rank {rank}/{n}")
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
    w = n.pivot_table(index="year", columns="depth", values="new_land_ha", aggfunc="sum", observed=False).loc[2008:2025]
    mean_depth = (n.assign(x=(n.km_from_road + 0.5) * n.new_land_ha).groupby("year").x.sum()
                  / n.groupby("year").new_land_ha.sum()).loc[2008:2025]
    X = sm.add_constant(pd.DataFrame({"post2019": (mean_depth.index >= 2019).astype(float),
                                      "trend": mean_depth.index - 2008.0}, index=mean_depth.index))
    m = sm.OLS(mean_depth, X).fit(cov_type="HAC", cov_kwds={"maxlags": 2})
    reg.add("t9_depth_post2019", m.params["post2019"], "km", "Mean depth north of the highway of first-time mined land: break after 2019 net of trend (Newey-West)", "description", SRC_R)
    reg.add("t9_depth_post2019_p", m.pvalues["post2019"], "p-value", "p-value of that break", "description", SRC_R)
    for y in (2016, 2018, 2020, 2022, 2025):
        reg.add(f"t9_depth_{y}", mean_depth.loc[y], "km", f"Mean depth north of the highway of first-time mined land, {y}", "description", SRC_R)
    sh = w.div(w.sum(axis=1), axis=0) * 100
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(9, 4.4), gridspec_kw={"wspace": 0.42})
    headline(fig, "After 2019 new mining north of La Pampa started nearer the road, then pushed deeper",
             "First-time mining north of the highway, La Pampa longitudes, 2008–2025")
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
