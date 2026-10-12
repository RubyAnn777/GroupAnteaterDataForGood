"""Plan v2 extras (meeting 12 Oct 2026 + Ruby's review). DESCRIPTION unless labelled prediction.

  E1 AMW robustness: Amazon Mining Watch new area per v2 zone and per road band (same zones, another satellite
     product). AMW starts in 2018 (stock), so only 2019+ comparisons.
  E2 Returns to old pits by zone: the stream / share charts duplicated for re-mining.
  E3 Zone profile: what each zone offers a miner: legality, distance to the highway and to rivers, gold-bearing land,
     depletion by 2018, cost type (tax vs enforcement risk; qualitative, from docs/overnight/notes/qualitative_background.md).
  E4 Where enforcement would protect most (PREDICTION): a logit on 1-km cells, trained on features of 2018 to predict
     first-time mining in 2019-21, tested out of sample on 2022-25 (features of 2021), then risk for 2026-28 (features of
     2025). Map of high-risk cells outside the legal corridor.
  E5 Timeline: enforcement waves, elections, decrees, COVID, spending, and growth of new mining (2008-2025), for the
     "political cycle" question (compare 2012-13 with 2019-21).
  E6 Declared gold output vs mapped mining: tonnes declared in Madre de Dios against first-time mined land inside
     and outside the legal corridor (the "mining legally, declaring nothing" hypothesis).
"""
from __future__ import annotations
import warnings
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

from common import ROOT, OUT, style_axes, finish_figure
import raster_zones as rz
from raster_layers import GROUPS, COL

INTER = ROOT / "data_intermediate"
SRC_R = "MapBiomas Peru Col 4 rasters, zones v2"
SRC_AMW = "Amazon Mining Watch (Earth Genome) onset patches x zones v2"
AMW_OUT = INTER / "amw_v2_zone_year.csv"
AMW_BAND = INTER / "amw_v2_band_year.csv"


# ------------------------------------------------------------------ E1 AMW robustness
def amw_build():
    import geopandas as gpd, rasterio
    from spatial import AMW_FILE, yearly_new_ha, CRS_AREA
    amw = gpd.read_file(AMW_FILE)[["onset_year", "geometry"]]
    amw = amw.cx[rz.BBOX[0]:rz.BBOX[2], rz.BBOX[1]:rz.BBOX[3]].copy()
    c = amw.geometry.centroid
    with rasterio.open(rz.OUT_FULL) as r:
        zone = r.read(1); inv = ~r.transform
    col, row = inv * (c.x.values, c.y.values)
    row, col = np.floor(row).astype(int), np.floor(col).astype(int)
    ok = (row >= 0) & (row < zone.shape[0]) & (col >= 0) & (col < zone.shape[1])
    amw = amw[ok].copy(); amw["code"] = zone[row[ok], col[ok]]
    amw = amw[amw.code > 0]
    amw["group"] = amw.code.map({c_: g for g, cs in GROUPS.items() for c_ in cs})
    a = amw.to_crs(CRS_AREA)
    rows = []
    for g, d in a.groupby("group"):
        for y, v in yearly_new_ha(d).items():
            rows.append({"group": g, "year": y, "new_ha": v})
    pd.DataFrame(rows).to_csv(AMW_OUT, index=False)
    # road bands: signed distance from the cell table (nearest 1-km cell)
    ca = pd.read_csv(rz.OUT_CELLATTR)
    from scipy.spatial import cKDTree
    tree = cKDTree(ca[["lon", "lat"]].values)
    cc = a.to_crs(4326).geometry.centroid
    dd, ii = tree.query(np.c_[cc.x, cc.y])
    a["road_km"] = ca.road_km.values[ii]; a["lon"] = cc.x.values
    sel = a[(dd < 0.01) & a.lon.between(*rz.LP_LON) & a.road_km.between(-30, 30)].copy()
    sel["side"] = np.where(sel.road_km >= 0, "north", "south")
    rows = []
    for s, d in sel.groupby("side"):
        for y, v in yearly_new_ha(d).items():
            rows.append({"side": s, "year": y, "new_ha": v})
    pd.DataFrame(rows).to_csv(AMW_BAND, index=False)


def e1(reg):
    if not AMW_OUT.exists():
        from spatial import AMW_FILE
        if not AMW_FILE.exists():
            warnings.warn("v2_extra: AMW raw file and intermediates missing"); return
        amw_build()
    a = pd.read_csv(AMW_OUT).pivot(index="year", columns="group", values="new_ha").fillna(0)
    b = pd.read_csv(AMW_BAND).pivot(index="year", columns="side", values="new_ha").fillna(0)
    for g in ("La Pampa sector", "Corridor across the road", "Rest of mining corridor"):
        key = "".join(ch for ch in g.lower() if ch.isalnum())[:16]
        for p, (x, y) in {"2019_21": (2019, 2021), "2022_25": (2022, 2025)}.items():
            reg.add(f"amw_v2_{key}_{p}", a.loc[x:y, g].mean(), "ha/yr", f"AMW new area per year, {g}, {p.replace('_', '-')}", "description", SRC_AMW)
    nshare = b["north"] / b.sum(axis=1)
    for y in (2019, 2020, 2021, 2023):
        reg.add(f"amw_v2_north_share_{y}", nshare.loc[y], "share", f"AMW: north-of-road share of new area, La Pampa longitudes, {y}", "description", SRC_AMW)
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(12, 3.8))
    yrs = [y for y in a.index if 2019 <= y <= 2025]
    for g in ("La Pampa sector", "Corridor across the road"):
        a1.plot(yrs, a.loc[yrs, g], "o-", color=COL[g], label=g, lw=2)
    a1.set_ylabel("AMW new area (ha)"); style_axes(a1); a1.legend(fontsize=8, frameon=False)
    a1.set_title("AMW, same zones", loc="left", fontsize=9.5)
    a2.plot(yrs, nshare.loc[yrs] * 100, "o-", color="#2a78d6", lw=2)
    a2.set_ylim(0, 100); a2.set_ylabel("% of new area north of the road"); style_axes(a2)
    a2.set_title("AMW, La Pampa longitudes: share north of the highway", loc="left", fontsize=9.5)
    fig.suptitle("Robustness: a second satellite product (Amazon Mining Watch) on the same zones", x=0.01, ha="left", fontsize=11, fontweight="bold")
    finish_figure(fig, f"Source: {SRC_AMW}. AMW = gold-mining scars in 480 m squares (hectares run large); 2018 is the "
                       "starting stock, so no pre-2019 comparison; 2025 provisional. Description.", OUT / "fig_v2_amw_robustness.png", rect_bottom=0.12)


# ------------------------------------------------------------------ E2 returns to old pits by zone
def e2(reg):
    z = pd.read_csv(rz.OUT_ZONE)
    z["group"] = z.code.map({c: g for g, cs in GROUPS.items() for c in cs})
    w = z.groupby(["year", "group"]).remined_ha.sum().unstack().reindex(columns=list(GROUPS)).fillna(0).loc[2010:2025]
    tot = w.sum(axis=1)
    fig, (a1, a2) = plt.subplots(2, 1, figsize=(11, 6.8), sharex=True, gridspec_kw={"height_ratios": [1.4, 1]})
    a1.stackplot(w.index, w.T.values, colors=[COL[c] for c in w.columns], edgecolor="white", linewidth=0.6, labels=list(w.columns))
    for y in w.index:
        a1.text(y, tot[y] * 1.02, f"{tot[y] / 1000:.1f}k", ha="center", fontsize=7, color="#52514e")
    a1.axvline(2018.5, color="black", lw=1.2); style_axes(a1); a1.legend(fontsize=7.5, frameon=False, ncol=2, loc="upper left")
    a1.set_ylabel("Old pits mined again (ha)")
    sh = w.div(tot, axis=0) * 100
    a2.stackplot(sh.index, sh.T.values, colors=[COL[c] for c in sh.columns], edgecolor="white", linewidth=0.6)
    a2.set_ylim(0, 100); a2.axvline(2018.5, color="black", lw=1.2); style_axes(a2)
    a2.set_ylabel("Share of the year's\nreturns to old pits (%)"); a2.set_xticks(list(w.index))
    a2.set_xticklabels([f"'{str(y)[2:]}" for y in w.index], fontsize=8)
    fig.suptitle("Returns to old pits each year, by zone (same layout as the first-time mining chart)", x=0.01, ha="left", fontsize=11, fontweight="bold")
    finish_figure(fig, f"Source: {SRC_R}. Return to old pits = mining on pixels mined in an earlier year but not the year before; "
                       "includes some year-to-year map flicker. Description.", OUT / "fig_v2_stream_remined.png", rect_bottom=0.08)
    cor = (w["Corridor across the road"] + w["Rest of mining corridor"]) / tot
    for p, (a, b) in {"2016_18": (2016, 2018), "2019_21": (2019, 2021), "2022_25": (2022, 2025)}.items():
        reg.add(f"rm_corridor_share_{p}", cor.loc[a:b].mean(), "share", f"Share of returns to old pits inside the legal corridor, {p}", "description", SRC_R)
        reg.add(f"rm_lapampa_share_{p}", (w["La Pampa sector"] / tot).loc[a:b].mean(), "share", f"Share of returns to old pits in the La Pampa sector, {p}", "description", SRC_R)


# ------------------------------------------------------------------ E3 zone profile
COST = {"La Pampa sector": "enforcement risk (illegal; operations 2019-20)", "Corridor across the road": "taxes, permits, competition (legal if titled)",
        "Rest of mining corridor": "taxes, permits, competition", "Native communities": "community consent; mixed legality",
        "Rest of Tambopata buffer zone": "enforcement risk (illegal)", "Other buffer zones": "enforcement risk (illegal)",
        "Reserves and parks": "highest enforcement risk; no road", "Rest of Madre de Dios": "mixed; far from deposits"}
LEGAL = {"La Pampa sector": "illegal", "Corridor across the road": "legal if titled", "Rest of mining corridor": "legal if titled",
         "Native communities": "depends on concession", "Rest of Tambopata buffer zone": "illegal", "Other buffer zones": "illegal",
         "Reserves and parks": "illegal", "Rest of Madre de Dios": "illegal outside concessions"}


def e3(reg):
    a = pd.read_csv(rz.OUT_CELLATTR).merge(pd.read_csv(INTER / "cell_gold_v2.csv"), on="cell", how="left")
    a["group"] = a.zone.map({c: g for g, cs in GROUPS.items() for c in cs})
    w = lambda d, c: np.average(d[c].dropna(), weights=d.loc[d[c].notna(), "area_ha"]) if d[c].notna().any() else np.nan
    rows = []
    for g in GROUPS:
        d = a[a.group == g]
        if d.empty:
            continue
        rows.append(dict(zone=g, legal_status=LEGAL[g], main_cost=COST[g], area_km2=d.area_ha.sum() / 100,
                         km_to_highway=w(d.assign(r=d.road_km.abs()), "r"), km_to_river=w(d, "river_km"),
                         gold_bearing_share=w(d, "gold_share"), gold_mined_by_2018=w(d, "gold_depleted_2018")))
    t = pd.DataFrame(rows); t.round(2).to_csv(OUT / "v2_zone_profile.csv", index=False)
    for _, r in t.iterrows():
        key = "".join(ch for ch in r.zone.lower() if ch.isalnum())[:16]
        for c in ("km_to_highway", "km_to_river", "gold_bearing_share"):
            if pd.notna(r[c]):
                reg.add(f"zp_{key}_{c}", r[c], "km" if "km" in c else "share", f"Zone profile (study window): {r.zone}, {c}", "description", SRC_R)
    return t


# ------------------------------------------------------------------ E4 risk model (prediction)
def e4(reg):
    import statsmodels.api as sm
    a = pd.read_csv(rz.OUT_CELLATTR).merge(pd.read_csv(INTER / "cell_gold_v2.csv"), on="cell", how="left")
    y = pd.read_csv(rz.OUT_CELL)
    idx = pd.MultiIndex.from_product([a.cell, range(2010, 2026)], names=["cell", "year"])
    y = y.set_index(["cell", "year"]).reindex(idx).fillna(0)
    stock = y.mining_ha.unstack(); new = y.new_land_ha.unstack()
    a = a.set_index("cell")
    # neighbourhood mining within ~3 km (sum over the 7x7 block of cells)
    nc = int(np.ceil((rz.STUDY[2] - rz.STUDY[0]) / (rz.CELL_PX * 0.000269495)))
    def neigh(s):
        r_, c_ = (s.index - 1) // nc, (s.index - 1) % nc
        g = pd.Series(s.values, index=pd.MultiIndex.from_arrays([r_, c_]))
        out = np.zeros(len(s))
        for dr in range(-3, 4):
            for dc in range(-3, 4):
                out += g.reindex(pd.MultiIndex.from_arrays([r_ + dr, c_ + dc])).fillna(0).values
        return out
    def feats(yr):
        X = pd.DataFrame(index=a.index)
        X["road_abs_km"] = a.road_km.abs().fillna(60).clip(upper=60)
        X["north"] = (a.road_km > 0).astype(float)
        X["river_km"] = a.river_km.clip(upper=30)
        X["gold_share"] = a.gold_share.fillna(0)
        X["mined_share"] = (stock[yr] / a.area_ha).clip(0, 1)
        X["neigh_mining_km2"] = neigh(stock[yr]) / 100
        for g in ("Reserves and parks", "Native communities", "La Pampa sector", "Rest of Tambopata buffer zone", "Other buffer zones"):
            X[f"z_{g[:12]}"] = a.zone.isin(GROUPS[g]).astype(float)
        X["corridor"] = a.zone.isin([5, 6]).astype(float)
        return sm.add_constant(X)
    y_train = (new.loc[:, 2019:2021].sum(axis=1) > 1).astype(int)
    y_test = (new.loc[:, 2022:2025].sum(axis=1) > 1).astype(int)
    m = sm.Logit(y_train, feats(2018)).fit(disp=0)
    p_test = m.predict(feats(2021))
    def auc(y, p):
        r = pd.Series(p).rank().values; n1 = y.sum(); n0 = len(y) - n1
        return (r[y.values == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0)
    au = auc(y_test, p_test)
    # critical review: spatial hold-out + a naive benchmark. Train on a random half of the 10-km blocks (2018 -> 2019-21),
    # test on the OTHER blocks (2021 -> 2022-25); benchmark = mining within ~3 km only.
    nc_ = int(np.ceil((rz.STUDY[2] - rz.STUDY[0]) / (rz.CELL_PX * 0.000269495)))
    blk = ((a.index - 1) // nc_ // 10) * 1000 + ((a.index - 1) % nc_ // 10)
    rng = np.random.default_rng(0); ub = np.unique(blk); tr_b = set(rng.choice(ub, size=len(ub) // 2, replace=False))
    tr = np.isin(blk, list(tr_b)); te = ~tr
    X18, X21 = feats(2018), feats(2021)
    m_sp = sm.Logit(y_train[tr], X18[tr]).fit(disp=0)
    au_sp = auc(y_test[te], m_sp.predict(X21[te]))
    bcols = ["const", "neigh_mining_km2"]
    m_b = sm.Logit(y_train[tr], X18.loc[tr, bcols]).fit(disp=0)
    au_b = auc(y_test[te], m_b.predict(X21.loc[te, bcols]))
    reg.add("risk_auc_spatial_holdout", au_sp, "AUC", "Out-of-sample AUC on held-out 10-km blocks (train on half the blocks, 2018 -> 2019-21; test on the others, 2021 -> 2022-25)", "prediction", SRC_R)
    reg.add("risk_auc_benchmark", au_b, "AUC", "Same hold-out, benchmark model with only 'mining within ~3 km'", "prediction", SRC_R)
    risk = m.predict(feats(2025))
    a["risk_2026_28"] = risk.values
    reg.add("risk_auc_2022_25", au, "AUC", "Out-of-sample AUC: logit trained on 2018 features -> 2019-21 first-time mining, tested on 2021 features -> 2022-25", "prediction", SRC_R)
    hi = a[(a.risk_2026_28 > 0.5) & ~a.zone.isin([5, 6])]
    reg.add("risk_hi_cells_outside_corridor", len(hi), "count", "1-km cells outside the legal corridor with predicted risk > 50% of first-time mining in 2026-28", "prediction", SRC_R)
    for g in ("Reserves and parks", "La Pampa sector", "Rest of Tambopata buffer zone", "Native communities"):
        key = "".join(ch for ch in g.lower() if ch.isalnum())[:16]
        reg.add(f"risk_hi_cells_{key}", int(hi.zone.isin(GROUPS[g]).sum()), "count", f"High-risk cells (>50%) in {g}, 2026-28", "prediction", SRC_R)
    pd.DataFrame({"term": m.params.index, "coef": m.params.values, "p": m.pvalues.values}).round(4).to_csv(OUT / "v2_risk_logit.csv", index=False)
    a.reset_index()[["cell", "lon", "lat", "zone", "risk_2026_28"]].round(4).to_csv(OUT / "v2_risk_cells.csv", index=False)
    # map
    import geopandas as gpd
    L = rz.layers()
    fig, ax = plt.subplots(figsize=(10, 6.6))
    sc = ax.scatter(a.lon, a.lat, c=a.risk_2026_28, cmap="OrRd", s=7, marker="s", vmin=0, vmax=1, linewidths=0)
    plt.colorbar(sc, ax=ax, label="Predicted chance of first-time mining 2026-28")
    gpd.GeoSeries([L["cor"]], crs=4326).boundary.plot(ax=ax, color="#2a78d6", lw=1)
    L["anp"].boundary.plot(ax=ax, color="#008300", lw=1.2)
    L["za"].boundary.plot(ax=ax, color="#1baf7a", lw=0.8, ls="--")
    L["ioh"].plot(ax=ax, color="black", lw=1.5)
    ax.set_xlim(rz.STUDY[0], rz.STUDY[2]); ax.set_ylim(rz.STUDY[1], rz.STUDY[3]); ax.set_aspect(1 / np.cos(np.radians(-12.9)))
    ax.set_title(f"Where new mining is most likely next (prediction; held-out-blocks AUC {au_sp:.2f} vs {au_b:.2f} for 'mining nearby' alone)", loc="left", fontsize=10, fontweight="bold")
    ax.legend(handles=[Patch(edgecolor="#2a78d6", facecolor="none", label="Legal mining corridor"),
                       Patch(edgecolor="#008300", facecolor="none", label="Reserves and parks"),
                       Patch(edgecolor="#1baf7a", facecolor="none", ls="--", label="Buffer zones")], fontsize=8, loc="lower left")
    finish_figure(fig, f"Source: {SRC_R}. Logit on 1-km cells: distance to highway and rivers, gold-bearing land, mining "
                       "nearby, zone. Trained to predict 2019-21 from 2018, tested on 2022-25 in held-out 10-km blocks, applied to 2025 "
                       "features. It misses the reserve incursion (river access, not captured). Prediction, not a causal map.", OUT / "fig_v2_risk_map.png", rect_bottom=0.08)


# ------------------------------------------------------------------ E5 timeline
EVENTS = [(2009, "Interdictions begin", "enf"), (2011.6, "Humala takes office", "pol"), (2012.2, "D.L. 1100/1105:\ncorridor, illegal mining defined", "law"),
          (2016.6, "Kuczynski takes office", "pol"), (2017, "Gang takeover\nof La Pampa", "ctx"), (2018.2, "Vizcarra takes office", "pol"),
          (2019.1, "Operation Mercurio", "enf"), (2020.2, "COVID-19", "ctx"), (2021.1, "Plan Restauracion", "enf"),
          (2021.6, "Castillo takes office", "pol"), (2023.3, "State of emergency", "enf"), (2025.5, "Navy posts withdrawn", "enf")]
ECOL = {"enf": "#0b0b0b", "pol": "#6250d6", "law": "#52514e", "ctx": "#9aa5a8"}


def e5(reg):
    z = pd.read_csv(rz.OUT_ZONE)
    lp = z[z.code == 7].set_index("year").new_land_ha.loc[2008:2025]
    tot = z.groupby("year").new_land_ha.sum().loc[2008:2025]
    sp = pd.Series({int(k.split("_")[-1]): v for k, v in []})
    fig, (a0, a1) = plt.subplots(2, 1, figsize=(11.5, 6.4), sharex=True, gridspec_kw={"height_ratios": [1, 1.4]})
    for i, (x, lab, k) in enumerate(EVENTS):
        a0.axvline(x, color=ECOL[k], lw=1.2, alpha=0.8)
        a0.text(x + 0.05, 0.92 - 0.16 * (i % 5), lab, fontsize=7, color=ECOL[k], va="top")
    a0.set_yticks([]); [a0.spines[s].set_visible(False) for s in ("left", "top", "right")]
    a0.set_title("Enforcement (black), presidents (violet), laws (dark grey), context (light grey)", loc="left", fontsize=9.5)
    a1.bar(lp.index, lp.values, color="#eb6834", width=0.7, label="La Pampa sector")
    a1.plot(tot.index, tot.values / 5, "o-", color="#3d3c39", lw=1.5, ms=3, label="All Madre de Dios ÷ 5")
    for x0, x1 in ((2012, 2013), (2019, 2021)):
        a1.axvspan(x0 - 0.5, x1 + 0.5, color="#f3e3c2", alpha=0.6, zorder=0)
    a1.set_ylabel("Land mined for the\nfirst time (ha)"); style_axes(a1); a1.legend(fontsize=8, frameon=False, loc="upper left")
    a1.set_xticks(range(2008, 2026)); a1.tick_params(axis="x", labelsize=8)
    fig.suptitle("One dip in La Pampa: 2020-21. The 2012-13 wave left no mark there", x=0.01, ha="left", fontsize=11, fontweight="bold")
    finish_figure(fig, f"Sources: {SRC_R}; dates from MAAP #130/#241, Asner & Tupayachi (2017), D.L. 1100/1105 (2012), Forbidden "
                       "Stories (2017 gang takeover), official government calendars. Shaded = the two dips. Total divided by 5 to share "
                       "the axis with La Pampa. Description.", OUT / "fig_v2_timeline.png", rect_bottom=0.1)
    for y in (2011, 2012, 2013, 2014, 2018, 2019, 2020, 2021):
        reg.add(f"tl_lp_newland_{y}", lp.loc[y], "ha", f"La Pampa sector, land mined for the first time, {y}", "description", SRC_R)
    reg.add("tl_dip_2012_13", lp.loc[2012:2013].mean() / lp.loc[2010:2011].mean() - 1, "share",
            "La Pampa first-time mining 2012-13 vs 2010-11 (relative change)", "description", SRC_R)
    reg.add("tl_dip_2020_21", lp.loc[2020:2021].mean() / lp.loc[2017:2018].mean() - 1, "share",
            "La Pampa first-time mining 2020-21 vs 2017-18 (relative change)", "description", SRC_R)


# ------------------------------------------------------------------ E6 declared output vs mapped mining
def e6(reg):
    import statsmodels.api as sm
    p = pd.read_csv(OUT / "peru_production_vs_area.csv").set_index("year")
    z = pd.read_csv(rz.OUT_ZONE)
    cor = z[z.code.isin([5, 6])].groupby("year").new_land_ha.sum()
    out = z[~z.code.isin([5, 6])].groupby("year").new_land_ha.sum()
    yrs = list(range(2010, 2026))
    d = pd.DataFrame({"tonnes": p.tonnes.reindex(yrs), "corridor_new": cor.reindex(yrs), "outside_new": out.reindex(yrs)})
    d["ha_per_tonne_mapped"] = (d.corridor_new + d.outside_new) / d.tonnes
    fig, (a1, a2) = plt.subplots(2, 1, figsize=(10, 5.8), sharex=True)
    a1.bar(yrs, d.tonnes, color="#eda100", width=0.7); a1.set_ylabel("Declared gold\n(tonnes)"); style_axes(a1)
    a1.set_title("The official gold series breaks in 2020 because it dropped its artisanal estimate; mapped mining kept growing", loc="left", fontsize=10.5, fontweight="bold")
    a1.axvline(2019.5, color="#b3261e", ls="--", lw=1.2); a1.text(2019.6, a1.get_ylim()[1] * 0.9, "artisanal estimate\ndropped from series", fontsize=7.5, color="#b3261e", va="top")
    a2.bar(yrs, d.corridor_new, color="#2a78d6", width=0.7, label="Inside the legal corridor")
    a2.bar(yrs, d.outside_new, bottom=d.corridor_new, color="#b9b8b2", width=0.7, label="Outside")
    a2.set_ylabel("Land mined for the\nfirst time (ha)"); style_axes(a2); a2.legend(fontsize=8, frameon=False)
    a2.set_xticks(yrs); a2.tick_params(axis="x", labelsize=8)
    finish_figure(fig, f"Sources: BCRP (source MINEM) declared gold production, Madre de Dios; {SRC_R}. Two panels, two units. "
                       "Until 2019 the official series includes MINEM's estimate of artisanal gold; from 2020 only declared output. The 2020 "
                       "break is a definition change, not a production fall. Description.", OUT / "fig_v2_declared_vs_mapped.png", rect_bottom=0.1)
    X = sm.add_constant(pd.DataFrame({"post2019": (d.index >= 2019).astype(float), "trend": np.array(yrs) - 2010.0}, index=d.index))
    m = sm.OLS(np.log(d.tonnes), X).fit(cov_type="HAC", cov_kwds={"maxlags": 2})
    reg.add("dec_log_tonnes_post2019", m.params["post2019"], "log points", "Official gold series, log tonnes: break after 2019 net of trend (OLS, Newey-West). ARTEFACT: series drops the artisanal estimate from 2020", "description", "BCRP/MINEM")
    reg.add("dec_log_tonnes_post2019_p", m.pvalues["post2019"], "p-value", "p-value of that break", "description", "BCRP/MINEM")
    for y in (2016, 2018, 2021, 2025):
        reg.add(f"dec_t_per_1000ha_new_{y}", 1000 * d.tonnes[y] / (d.corridor_new[y] + d.outside_new[y]), "t per 1000 ha",
                f"Declared tonnes per 1,000 ha of first-time mined land, {y}", "description", "BCRP/MINEM; MapBiomas rasters")
    d.round(2).to_csv(OUT / "v2_declared_vs_mapped.csv")


def run(reg):
    print("\n== v2 extras ==")
    if not rz.OUT_ZONE.exists():
        warnings.warn("v2_extra: intermediates missing"); return
    e1(reg); e2(reg); print(e3(reg).round(2).to_string(index=False)); e4(reg); e5(reg); e6(reg)
