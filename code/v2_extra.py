"""Extras (meeting 12 Oct 2026 + Ruby's review), plan v3. DESCRIPTION unless labelled prediction.

Outcome: net mining additions (new + re-mined - stopped) where a design allows; each section says its measure.
Zones: registry (definitions.ZONES; zone_year.csv, zones_mdd.tif, cell_attr.csv), Madre de Dios part.

  E1 AMW robustness: Amazon Mining Watch new area per registry zone and per road side (patch centroid in the zone
     raster, inside Madre de Dios). AMW has no "stopped" state, so it is NEW AREA, never net; AMW starts in 2018
     (stock), so only 2019+ comparisons.
  E2 Re-mined land by zone (one of the three parts of net additions), and its corridor share.
  E3 Zone profile: what each zone offers a miner: legality, distance to the highway and to rivers, gold-bearing land,
     depletion by 2018, cost type (tax vs enforcement risk; qualitative, from docs/overnight/notes/qualitative_background.md).
  E4 Where new land is likely to be mined (PREDICTION): a logit on 1-km cells, outcome = more than 1 ha of NEW LAND
     (first-time mining) in the window (a logit needs an event; net additions cannot be one), trained on features of
     2018 -> 2019-21, tested out of sample on 2022-25 (features of 2021), then risk for 2026-28 (features of 2025).
     Distance to the highway = true distance from the cell centre to the Interoceanic Highway (UTM 19S), not the
     north-south offset.
  E5 Timeline: events against net additions (with parts) in La Pampa and Madre de Dios, 2008-2025. 2012-13 is NOT an
     enforcement wave in our data; Asner & Tupayachi (2017) report a dip then, and we show whether our data have it.
  E6 Declared gold output vs land newly mined or re-mined (land worked, the flow that yields gold; not net additions),
     inside and outside the legal corridor (the "mining legally, declaring nothing" hypothesis).
"""
from __future__ import annotations
import warnings
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

from common import (ROOT, OUT, style_axes, finish_figure, headline, label_end, callout, period_band,
                    add_event_markers, PERU_EVENTS, EVENT_TITLE_PAD, C, INK, INK2, MUTED, AXIS, SURFACE)
import definitions as D
import zonedata as Z
import raster_zones as rz
from raster_layers import GROUPS, GKEY, group_of, COL as ZC_ALL

# zone colours by family (orange = Tambopata BZ, blue = corridor, green = protected, raspberry = native, grey = rest)
ZC = ZC_ALL
MERCURIO = [PERU_EVENTS[0]]


def _dots(ax, x, y, color, ms=4.5):
    ax.plot(x, y, "-", color=color, lw=2.2, zorder=3)
    ax.plot(x, y, "o", color=color, ms=ms, mec=SURFACE, mew=1.0, zorder=4)


def _stack_labels(ax, df, x, min_share=0.06, total=None):
    """Direct labels at the right edge of a stack, at the middle of each band that is wide enough."""
    v = df.loc[x]; tot = v.sum() if total is None else total
    cum = 0.0
    for g, val in v.items():
        if val / tot >= min_share:
            label_end(ax, x, cum + val / 2, g, ZC[g], dx=8, fontsize=8)
        cum += val

INTER = ROOT / "data_intermediate"
SRC_R = f"{D.SOURCE}, zone registry"
SRC_AMW = ("Amazon Mining Watch (Earth Genome) onset patches x zone registry (zones: area-weighted, spatial.py; "
           "road sides: patch centroid)")
AMW_OUT = INTER / "amw_registry_zone_year.csv"
AMW_BAND = INTER / "amw_registry_band_year.csv"
GOLD = INTER / "cell_gold.csv"
PER = ("pre", "during", "later")
CORRIDOR = "corridor"                                  # tenure tag (definitions.TENURE)


# ------------------------------------------------------------------ E1 AMW robustness
def amw_build():
    import geopandas as gpd, rasterio
    from spatial import AMW_FILE, yearly_new_ha, CRS_AREA
    amw = gpd.read_file(AMW_FILE)[["onset_year", "geometry"]]
    amw = amw.cx[rz.BBOX[0]:rz.BBOX[2], rz.BBOX[1]:rz.BBOX[3]].copy()
    c = amw.to_crs(32719).geometry.centroid.to_crs(4326)
    from raster_layers import zone_raster
    zone, _, _, t, mdd = zone_raster()
    inv = ~t
    col, row = inv * (c.x.values, c.y.values)
    row, col = np.floor(row).astype(int), np.floor(col).astype(int)
    ok = (row >= 0) & (row < zone.shape[0]) & (col >= 0) & (col < zone.shape[1])
    amw = amw[ok].copy(); amw["code"] = zone[row[ok], col[ok]]; amw["in_mdd"] = mdd[row[ok], col[ok]]
    amw = amw[(amw.code > 0) & amw.in_mdd]                 # clipped to the department (review P3)
    amw["group"] = amw.code.map(lambda c_: group_of(D.CODE_ZONE[int(c_)]))
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
    cc = a.geometry.centroid.to_crs(4326)
    dd, ii = tree.query(np.c_[cc.x, cc.y])
    a["road_km"] = ca.road_km.values[ii]; a["lon"] = cc.x.values
    sel = a[(dd < 0.01) & a.lon.between(*D.LP_LON) & a.road_km.between(-rz.BAND_KM, rz.BAND_KM)].copy()
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
    # zones: the ONE AMW zone table (spatial.py: patches rasterized on the registry grid, area-weighted, MdD part)
    z = pd.read_csv(INTER / "amw_zone_year.csv")
    z = z[(z.in_mdd == 1) & ~z.is_stock.astype(bool)]
    z["group"] = z.zone.map(group_of)
    a = z.groupby(["year", "group"]).new_ha.sum().unstack().fillna(0)
    b = pd.read_csv(AMW_BAND).pivot(index="year", columns="side", values="new_ha").fillna(0)
    for g in ("La Pampa sector", "Corridor across the road", "Rest of mining corridor"):
        z = GROUPS[g][0]
        for p in ("during", "later"):
            x, y = D.PERIODS[p]
            reg.add(f"amw_reg_{z}_{p}", a.loc[x:y, g].mean(), "ha/yr", f"AMW new area per year (another product: not "
                    f"net additions), {g}, {D.period_label(p)}", "description", SRC_AMW, measure="amw_new_area", zone=z,
                    period=D.period_label(p))
    nshare = b["north"] / b.sum(axis=1)
    for y in (2019, 2020, 2021, 2023):
        reg.add(f"amw_reg_north_share_{y}", nshare.loc[y], "share", f"AMW: north-of-road share of new area, La Pampa "
                f"longitudes, {y}", "description", SRC_AMW, measure="amw_new_area", zone="road sides, La Pampa longitudes",
                period=str(y))
    yrs = [y for y in a.index if 2019 <= y <= 2025]
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(9, 4.0), gridspec_kw={"wspace": 0.45})
    pk_ = (nshare.loc[yrs] * 100).idxmax()
    headline(fig, f"AMW, another product: north of the road peaked at {nshare[pk_]:.0%} of new area in {pk_}",
             "Amazon Mining Watch (AMW) new gold-mining area (not net additions), registry zones, ha/yr, 2019–2025 "
             "(2025 provisional)")
    for g, lab in (("La Pampa sector", "La Pampa"), ("Corridor across the road", "Across\nthe road")):
        _dots(a1, yrs, a.loc[yrs, g], ZC[g])
        label_end(a1, yrs[-1], a.loc[yrs[-1], g], lab, ZC[g], dx=7)
    a1.set_ylim(bottom=0); style_axes(a1)
    a1.set_title("New area per year (ha)")
    sh = nshare.loc[yrs] * 100
    _dots(a2, yrs, sh, C["corridor"])
    a2.axhline(50, color=AXIS, lw=0.8, ls=(0, (3, 2)), zorder=1)
    a2.text(yrs[0] - 0.3, 51, "half", fontsize=7.5, color=MUTED, va="bottom")
    pk = sh.idxmax()
    callout(a2, pk, sh[pk], f"{sh[pk]:.0f}% in {pk}", dy=-22)
    a2.set_ylim(0, 100); style_axes(a2)
    a2.set_title("Share north of the highway (%), La Pampa longitudes")
    for ax in (a1, a2):
        ax.set_xticks(yrs); ax.set_xticklabels([f"'{str(y)[2:]}" for y in yrs]); ax.set_xlim(yrs[0] - 0.4, yrs[-1] + 0.4)
    finish_figure(fig, f"{SRC_AMW}. AMW = gold-mining scars in 480 m squares (hectares run large); 2018 is the "
                       "starting stock, so no pre-2019 comparison; 2025 provisional. Description.", OUT / "fig_v2_amw_robustness.png")

# ------------------------------------------------------------------ E2 returns to old pits by zone
def e2(reg):
    """Re-mined land by zone group (one part of net additions), Madre de Dios part."""
    z = pd.read_csv(rz.OUT_ZONE)
    z = z[z.in_mdd == 1].copy()
    z["group"] = z.zone.map(group_of)
    w = z.groupby(["year", "group"]).remined_ha.sum().unstack().reindex(columns=list(GROUPS)).fillna(0).loc[2010:2025]
    tot = w.sum(axis=1)
    m0, m1 = (Z.period_mean(tot, p) for p in ("pre", "later"))
    cor_t = z[z.tenure == CORRIDOR].groupby("year").remined_ha.sum().reindex(w.index).fillna(0)
    cs = cor_t.loc[D.PERIODS["later"][0]:].sum() / tot.loc[D.PERIODS["later"][0]:].sum()
    fig, (a1, a2) = plt.subplots(2, 1, figsize=(9, 7.0), sharex=True, gridspec_kw={"height_ratios": [1.4, 1], "hspace": 0.3})
    headline(fig, f"Re-mined land rose {m1 / m0:.1f}-fold from 2016–18 to 2022–25; {cs:.0%} of it on corridor land",
             f"Re-mined land (one part of net additions: old pits mined again), by zone, Madre de Dios, ha/yr. Mean "
             f"{m0:,.0f} (2016–18) → {m1:,.0f} (2022–25)")
    a1.stackplot(w.index, w.T.values, colors=[ZC[c] for c in w.columns], edgecolor=SURFACE, linewidth=0.8)
    _stack_labels(a1, w, w.index[-1], min_share=0.1)
    pk = tot.idxmax()
    callout(a1, pk, tot[pk], f"{tot[pk]:,.0f} ha in {pk}", dy=8, arrow=False)
    a1.set_ylim(0, tot.max() * 1.12); style_axes(a1)
    a1.set_title("Hectares per year", pad=EVENT_TITLE_PAD)
    sh = w.div(tot, axis=0) * 100
    a2.stackplot(sh.index, sh.T.values, colors=[ZC[c] for c in sh.columns], edgecolor=SURFACE, linewidth=0.8)
    a2.set_ylim(0, 100); style_axes(a2)
    a2.set_title("Share of the year's re-mined land (%)")
    _stack_labels(a2, sh, sh.index[-1], min_share=0.04, total=100)
    a2.set_xticks(list(w.index)); a2.set_xticklabels([f"'{str(y)[2:]}" for y in w.index])
    a1.set_xlim(w.index[0], w.index[-1] + 2.9)               # right gutter for the direct labels
    for ax in (a1, a2):
        ax.spines["bottom"].set_bounds(w.index[0], w.index[-1])
    for ax in (a1, a2):
        add_event_markers(ax, label=ax is a1)
        for ln in ax.lines[-len(PERU_EVENTS):]:
            ln.set_zorder(3)
    finish_figure(fig, f"{SRC_R}. Madre de Dios part. Re-mined = mining on pixels mapped as mining in an earlier year but "
                       "not the year before; includes some year-to-year map flicker. Corridor share uses corridor tenure "
                       "(D.L. 1100, any zone). Labels at the right name the bands of 2025. Description.",
                  OUT / "fig_v2_stream_remined.png", event_note=True)
    for p in PER:
        a, b = D.PERIODS[p]
        kw = dict(measure="remined", zone="mdd", period=D.period_label(p))
        reg.add(f"rm_corridor_share_{p}", cor_t.loc[a:b].sum() / tot.loc[a:b].sum(), "share", f"Share of Madre de Dios "
                f"re-mined land on legal-corridor land (tenure), {D.period_label(p)}, period sum / period sum",
                "description", SRC_R, **kw)
        reg.add(f"rm_lapampa_share_{p}", w["La Pampa sector"].loc[a:b].sum() / tot.loc[a:b].sum(), "share",
                f"Share of Madre de Dios re-mined land in the La Pampa sector, {D.period_label(p)}", "description",
                SRC_R, **kw)


def true_road_km(a: pd.DataFrame) -> np.ndarray:
    """Distance (km) from each cell centre to the Interoceanic Highway (RAISG PE-30C), UTM 19S, road densified at 50 m.
    (cell_attr.road_km is the north-south offset and exists only inside the study window's latitudes.)"""
    import geopandas as gpd
    from shapely.ops import unary_union
    from scipy.spatial import cKDTree
    roads = gpd.read_file(rz.RAW / "raisg/vias_nacionales_mdd_box.geojson")
    line = unary_union(roads[roads.sigla == "PE-30C"].to_crs(32719).geometry)
    pts = np.vstack([np.array([g.interpolate(s_).coords[0] for s_ in np.arange(0, g.length, 50.0)])
                     for g in getattr(line, "geoms", [line])])
    xy = gpd.GeoSeries(gpd.points_from_xy(a.lon, a.lat), crs=4326).to_crs(32719)
    return cKDTree(pts).query(np.c_[xy.x, xy.y])[0] / 1000


# ------------------------------------------------------------------ E3 zone profile
COST = {"La Pampa sector": "enforcement risk (illegal; Mercurio from 2019 and the operations that followed)", "Corridor across the road": "taxes, permits, competition (legal if titled)",
        "Rest of mining corridor": "taxes, permits, competition", "Native communities": "community consent; mixed legality",
        "Rest of Tambopata buffer zone": "enforcement risk (illegal)",
        "Amarakaeri buffer zone": "enforcement risk (illegal outside corridor land)", "Other buffer zones": "enforcement risk (illegal)",
        "Reserves and parks": "highest enforcement risk; no road", "Rest of Madre de Dios": "mixed; far from deposits"}
LEGAL = {"La Pampa sector": "illegal", "Corridor across the road": "legal if titled", "Rest of mining corridor": "legal if titled",
         "Native communities": "depends on concession", "Rest of Tambopata buffer zone": "illegal",
         "Amarakaeri buffer zone": "illegal outside corridor land", "Other buffer zones": "illegal",
         "Reserves and parks": "illegal", "Rest of Madre de Dios": "illegal outside concessions"}


def e3(reg):
    a = pd.read_csv(rz.OUT_CELLATTR).merge(pd.read_csv(GOLD), on="cell", how="left")
    a["group"] = a.zone.map(group_of)
    a["road_true_km"] = true_road_km(a)
    w = lambda d, c: np.average(d[c].dropna(), weights=d.loc[d[c].notna(), "area_ha"]) if d[c].notna().any() else np.nan
    rows = []
    for g in GROUPS:
        d = a[a.group == g]
        if d.empty:
            continue
        rows.append(dict(zone=g, legal_status=LEGAL[g], main_cost=COST[g], area_km2=d.area_ha.sum() / 100,
                         km_to_highway=w(d, "road_true_km"), km_to_river=w(d, "river_km"),
                         gold_bearing_share=w(d, "gold_share"), gold_mined_by_2018=w(d, "gold_depleted_2018")))
    t = pd.DataFrame(rows); t.round(2).to_csv(OUT / "v2_zone_profile.csv", index=False)
    for _, r in t.iterrows():
        key = GKEY[r.zone]
        for c in ("km_to_highway", "km_to_river", "gold_bearing_share"):
            if pd.notna(r[c]):
                reg.add(f"zp_{key}_{c}", r[c], "km" if "km" in c else "share", f"Zone profile (1-km cells of the study "
                        f"window, majority zone): {r.zone}, {c}", "description", SRC_R, measure="profile", zone=key,
                        period="map")
    return t


# ------------------------------------------------------------------ E4 risk model (prediction)
Y_LAST = D.YEARS[1]
def e4(reg):
    import statsmodels.api as sm
    a = pd.read_csv(rz.OUT_CELLATTR).merge(pd.read_csv(GOLD), on="cell", how="left")
    a["road_true_km"] = true_road_km(a)
    a["group"] = a.zone.map(group_of)
    y = pd.read_csv(rz.OUT_CELL)
    idx = pd.MultiIndex.from_product([a.cell, range(2010, 2026)], names=["cell", "year"])
    y = y.set_index(["cell", "year"]).reindex(idx).fillna(0)
    stock = y.mining_ha.unstack(); new = y.new_ha.unstack()
    a = a.set_index("cell")
    # neighbourhood mining within ~3 km (sum over the 7x7 block of cells)
    from v2_stats import _cells_per_row
    nc = _cells_per_row()
    def neigh(s):
        r_, c_ = (s.index - 1) // nc, (s.index - 1) % nc
        g = pd.Series(s.values, index=pd.MultiIndex.from_arrays([r_, c_]))
        out = np.zeros(len(s))
        for dr in range(-3, 4):
            for dc in range(-3, 4):
                out += g.reindex(pd.MultiIndex.from_arrays([r_ + dr, c_ + dc])).fillna(0).values
        return out
    ZD = ("Reserves and parks", "Native communities", "La Pampa sector", "Rest of Tambopata buffer zone",
          "Amarakaeri buffer zone", "Other buffer zones")
    def feats(yr):
        X = pd.DataFrame(index=a.index)
        X["road_km"] = a.road_true_km.clip(upper=60)
        X["north"] = (a.road_km > 0).astype(float)
        X["river_km"] = a.river_km.clip(upper=30)
        X["gold_share"] = a.gold_share.fillna(0)
        X["mined_share"] = (stock[yr] / a.area_ha).clip(0, 1)
        X["neigh_mining_km2"] = neigh(stock[yr]) / 100
        for g in ZD:
            X[f"z_{GKEY[g]}"] = (a.group == g).astype(float)
        X["corridor"] = (a.tenure == CORRIDOR).astype(float)
        return sm.add_constant(X)
    d0, d1 = D.PERIODS["during"]; l0, l1 = D.PERIODS["later"]
    y_train = (new.loc[:, d0:d1].sum(axis=1) > 1).astype(int)
    y_test = (new.loc[:, l0:l1].sum(axis=1) > 1).astype(int)
    m = sm.Logit(y_train, feats(D.REF_YEAR)).fit(disp=0)
    p_test = m.predict(feats(d1))
    def auc(y, p):
        r = pd.Series(p).rank().values; n1 = y.sum(); n0 = len(y) - n1
        return (r[y.values == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0)
    au = auc(y_test, p_test)
    # spatial hold-out + a naive benchmark. Train on a random half of the 10-km blocks (2018 -> 2019-21), test on the
    # OTHER blocks (2021 -> 2022-25); benchmark = mining within ~3 km only.
    blk = ((a.index - 1) // nc // 10) * 1000 + ((a.index - 1) % nc // 10)
    rng = np.random.default_rng(0); ub = np.unique(blk); tr_b = set(rng.choice(ub, size=len(ub) // 2, replace=False))
    tr = np.isin(blk, list(tr_b)); te = ~tr
    X18, X21 = feats(D.REF_YEAR), feats(d1)
    m_sp = sm.Logit(y_train[tr], X18[tr]).fit(disp=0)
    au_sp = auc(y_test[te], m_sp.predict(X21[te]))
    bcols = ["const", "neigh_mining_km2"]
    m_b = sm.Logit(y_train[tr], X18.loc[tr, bcols]).fit(disp=0)
    au_b = auc(y_test[te], m_b.predict(X21.loc[te, bcols]))
    kw = dict(measure="new", zone="1-km cells, study window", period="train 2019-21, test 2022-25")
    reg.add("risk_auc_spatial_holdout", au_sp, "AUC", "Out-of-sample AUC on held-out 10-km blocks (train on half the "
            "blocks, 2018 -> new land > 1 ha in 2019-21; test on the others, 2021 -> 2022-25)", "prediction", SRC_R, **kw)
    reg.add("risk_auc_benchmark", au_b, "AUC", "Same hold-out, benchmark model with only 'mining within ~3 km'",
            "prediction", SRC_R, **kw)
    risk = m.predict(feats(Y_LAST))
    a["risk_2026_28"] = risk.values
    reg.add("risk_auc_2022_25", au, "AUC", "Out-of-sample AUC: logit trained on 2018 features -> new land > 1 ha in "
            "2019-21, tested on 2021 features -> 2022-25", "prediction", SRC_R, **kw)
    hi = a[(a.risk_2026_28 > 0.5) & (a.tenure != CORRIDOR)]
    kw2 = dict(measure="new", period="2026-28")
    reg.add("risk_hi_cells_outside_corridor", len(hi), "count", "1-km cells outside legal-corridor land (tenure) with "
            "predicted chance > 50% of more than 1 ha of new land in 2026-28", "prediction", SRC_R, zone="study window", **kw2)
    for g in ZD:
        reg.add(f"risk_hi_cells_{GKEY[g]}", int((hi.group == g).sum()), "count", f"High-risk cells (>50%) in {g}, "
                "2026-28. Reserves score low by construction: they held almost no mining in the training years, and the "
                "model has no river-access term for incursions such as the 2025 Malinowski one", "prediction", SRC_R,
                zone=GKEY[g], **kw2)
    pd.DataFrame({"term": m.params.index, "coef": m.params.values, "p": m.pvalues.values}).round(4).to_csv(OUT / "v2_risk_logit.csv", index=False)
    a.reset_index()[["cell", "lon", "lat", "zone", "risk_2026_28"]].round(4).to_csv(OUT / "v2_risk_cells.csv", index=False)
    # map
    import geopandas as gpd
    L = rz.layers()
    from matplotlib.colors import LinearSegmentedColormap
    from matplotlib.lines import Line2D
    cmap = LinearSegmentedColormap.from_list("risk", ["#f4f2ee", "#b8c3c5", "#5d7479", "#1f2d33"])
    fig = plt.figure(figsize=(9, 6.9))
    ax = fig.add_axes([0.02, 0.2, 0.96, 0.68])
    headline(fig, "New land is predicted where mining already is" + (f" (held-out AUC {au_sp:.2f} vs {au_b:.2f} for "
             "'mining nearby' alone)"),
             "Predicted chance of more than 1 ha of new land (first-time mining) per 1-km cell in 2026–28. Prediction.")
    ax.text(0.985, 0.03, f"{len(hi)} cells outside the corridor\nabove 50% risk", transform=ax.transAxes, ha="right", va="bottom",
            fontsize=9, color=INK, fontweight="medium", linespacing=1.3)
    sc = ax.scatter(a.lon, a.lat, c=a.risk_2026_28, cmap=cmap, s=14, marker="s", vmin=0, vmax=1, linewidths=0)
    gpd.GeoSeries([L["cor"]], crs=4326).boundary.plot(ax=ax, color=C["corridor"], lw=1.1)
    L["anp"].boundary.plot(ax=ax, color=C["reserve"], lw=1.3)
    L["za"].boundary.plot(ax=ax, color=C["buffer"], lw=0.9, ls="--")
    L["ioh"].plot(ax=ax, color=INK, lw=1.6)
    ax.set_xlim(rz.STUDY[0], rz.STUDY[2]); ax.set_ylim(rz.STUDY[1], rz.STUDY[3]); ax.set_aspect(1 / np.cos(np.radians(-12.9)))
    ax.set_xticks([]); ax.set_yticks([]); ax.set_xlabel(""); ax.set_ylabel("")
    for sp in ax.spines.values():
        sp.set_color(AXIS); sp.set_linewidth(0.6)
    cax = fig.add_axes([0.06, 0.135, 0.34, 0.022])
    cb = fig.colorbar(sc, cax=cax, orientation="horizontal")
    cb.outline.set_visible(False); cb.set_ticks([0, 0.25, 0.5, 0.75, 1]); cb.set_ticklabels(["0%", "25%", "50%", "75%", "100%"])
    cb.ax.tick_params(length=0, labelsize=8); cax.set_title("Predicted chance of first-time mining", fontsize=8.5, loc="left", color=INK2, pad=4)
    fig.legend(handles=[Line2D([], [], color=C["corridor"], lw=1.4, label="Legal mining corridor"),
                        Line2D([], [], color=C["reserve"], lw=1.4, label="Reserves and parks"),
                        Line2D([], [], color=C["buffer"], lw=1.2, ls=(0, (4, 2)), label="Buffer zones"),
                        Line2D([], [], color=INK, lw=1.6, label="Interoceanic Highway")],
               loc="lower left", bbox_to_anchor=(0.47, 0.105), ncol=2, fontsize=8.5, handlelength=2.2, columnspacing=1.4)
    fig.text(0.012, 0.008, "Source: " + SRC_R + ". Logit on 1-km cells: true distance to the highway, distance to rivers "
             "(2018), gold-bearing land, mining nearby, zone, corridor tenure. Trained on 2018 → 2019–21,\ntested on "
             "2022–25 in held-out 10-km blocks, applied to 2025 features. Reserves score low because they held almost no "
             "mining in training; river distance is in the model,\nbut not river access by boat, so the 2025 Malinowski "
             "incursion inside the reserve is not foreseen. Prediction, not a causal map.",
             fontsize=7, color=MUTED, va="bottom", linespacing=1.35)
    fig.savefig(OUT / "fig_v2_risk_map.png", dpi=170); plt.close(fig); print("Saved output/fig_v2_risk_map.png")

# ------------------------------------------------------------------ E5 timeline
LANES = ["Enforcement", "Presidents", "Laws", "Context"]
# (x, label, lane, label above?, horizontal alignment)
EVENTS = [(2009, "Interdictions begin", 0, True, "left"), (2019.1, "Operation Mercurio", 0, False, "left"),
          (2021.1, "Plan Restauración", 0, True, "center"), (2023.3, "State of emergency", 0, False, "center"),
          (2025.5, "Navy posts withdrawn", 0, True, "right"),
          (2011.6, "Humala", 1, True, "center"), (2016.6, "Kuczynski", 1, True, "center"), (2018.2, "Vizcarra", 1, False, "center"),
          (2021.6, "Castillo", 1, False, "center"),
          (2012.2, "D.L. 1100 / 1105: corridor; illegal mining defined", 2, True, "left"),
          (2017, "Gang takeover of La Pampa", 3, True, "center"), (2020.2, "COVID-19", 3, False, "center")]


def e5(reg):
    ru = Z.region_units()
    W = {m: Z.wide(ru, D.COLS[m]).loc[2008:2025] for m in ("net", "new", "remined", "stopped")}
    lp, tot = W["net"]["lapampa"], W["net"]["mdd"]
    fig, (a0, a1, a2) = plt.subplots(3, 1, figsize=(9, 7.6), sharex=True,
                                     gridspec_kw={"height_ratios": [1.35, 1, 1], "hspace": 0.32})
    c12 = lp.loc[2012:2013].mean() / lp.loc[2010:2011].mean() - 1
    headline(fig, f"La Pampa's net additions fell in {D.period_label('during')}; in 2012–13 they "
                  + ("rose" if c12 > 0 else "fell") + f" ({c12:+.0%} vs 2010–11)",
             "Events by type (top) against net mining additions (new + re-mined − stopped), ha/yr. Shaded: "
             "Mercurio and what followed (2019–21).")
    for i, lane in enumerate(LANES):
        y = len(LANES) - 1 - i
        a0.axhline(y, color=AXIS, lw=0.7, zorder=1)
        a0.text(2007.35, y, lane, ha="right", va="center", fontsize=8.5, color=INK2, fontweight="medium")
    for x, lab, lane, up, ha in EVENTS:
        y = len(LANES) - 1 - lane
        enf = lane == 0
        a0.plot(x, y, "o", ms=6.5 if enf else 5.5, color=INK if enf else SURFACE, mec=INK if enf else INK2, mew=1.3, zorder=3)
        a0.annotate(lab, xy=(x, y), xytext=(0, 7 if up else -7), textcoords="offset points", ha=ha,
                    va="bottom" if up else "top", fontsize=7.5, color=INK if enf else INK2,
                    fontweight="semibold" if enf else "normal")
    a0.set_ylim(-0.75, len(LANES) - 0.35); a0.set_yticks([])
    for sp in ("left", "top", "right", "bottom"):
        a0.spines[sp].set_visible(False)
    a0.tick_params(axis="x", length=0)
    d0, d1 = D.PERIODS["during"]
    for ax, ser, col, title in ((a1, lp, C["lapampa"], "La Pampa sector: net additions, ha/yr"),
                                (a2, tot, C["other"], "All of Madre de Dios: net additions, ha/yr")):
        period_band(ax, d0 - 0.5, d1 + 0.5)
        ax.bar(ser.index, ser.values, color=col, width=0.72, zorder=2)
        ax.axhline(0, color=INK2, lw=0.6)
        ax.set_ylim(min(0, ser.min() * 1.2), ser.max() * 1.15); style_axes(ax); ax.set_title(title)
    callout(a1, d0 + 1, lp.loc[d0:d1].max(), f"{lp.loc[d0:d1].mean():,.0f} ha/yr\n2019–21", dy=26)
    callout(a1, 2012.5, lp.loc[2012:2013].max(), f"{lp.loc[2012:2013].mean():,.0f} ha/yr\n2012–13", dy=14)
    for ax in (a0, a1, a2):
        ax.set_xlim(2007.4, 2025.8)
    a2.set_xticks(range(2008, 2026)); a2.set_xticklabels([f"'{str(y)[2:]}" for y in range(2008, 2026)])
    finish_figure(fig, f"Sources: {SRC_R}; dates from MAAP #130/#241, Asner & Tupayachi (2017; they report a 2012–13 dip "
                       "in La Pampa, which our data do not show), D.L. 1100/1105 (2012), Forbidden Stories (2017 gang "
                       "takeover), official government calendars. Filled dots = enforcement. Parts of net additions: "
                       "fig_v2_parts_by_zone.png. Description.", OUT / "fig_v2_timeline.png")
    for y in (2011, 2012, 2013, 2014, 2018, 2019, 2020, 2021):
        Z.register_parts(reg, f"tl_lp_{y}", {m: W[m]["lapampa"].loc[y] for m in W}, "lapampa", str(y), "that year",
                         source=SRC_R)
    for m in ("net", "new"):
        s_ = W[m]["lapampa"]
        reg.add(f"tl_lp_change_2012_13_vs_2010_11_{m}", s_.loc[2012:2013].mean() / s_.loc[2010:2011].mean() - 1, "share",
                f"La Pampa sector, {D.MEASURE_NAME[m].lower()}: 2012-13 mean vs 2010-11 mean, relative change (checks "
                "Asner & Tupayachi 2017's reported dip; not a treatment in our design)", "description", SRC_R,
                measure=m, zone="lapampa", period="2012-13 vs 2010-11")


# ------------------------------------------------------------------ E6 declared output vs mapped mining
def e6(reg):
    """Declared gold vs land WORKED (newly mined or re-mined): the flow that yields gold, so not net additions."""
    import statsmodels.api as sm
    p = pd.read_csv(OUT / "peru_production_vs_area.csv").set_index("year")
    z = pd.read_csv(rz.OUT_ZONE)
    z = z[z.in_mdd == 1].assign(worked=lambda q: q.new_ha + q.remined_ha)
    cor = z[z.tenure == CORRIDOR].groupby("year").worked.sum()
    out = z[z.tenure != CORRIDOR].groupby("year").worked.sum()
    yrs = list(range(2010, 2026))
    d = pd.DataFrame({"tonnes": p.tonnes.reindex(yrs), "corridor_worked": cor.reindex(yrs), "outside_worked": out.reindex(yrs)})
    fig, (a1, a2) = plt.subplots(2, 1, figsize=(9, 6.0), sharex=True, gridspec_kw={"hspace": 0.35})
    headline(fig, "Declared gold “fell” in 2020 because the series changed. Mapped mining kept growing.",
             "Top: official gold output, Madre de Dios (tonnes). Bottom: land newly mined or re-mined (land worked, "
             "ha/yr; not net additions).")
    a1.bar(yrs, d.tonnes, color=C["gold"], width=0.72); style_axes(a1); a1.set_title("Official gold series (tonnes)")
    a1.axvline(D.FIRST_POST + 0.5, color=INK, ls=(0, (3, 2)), lw=1.0)
    a1.text(D.FIRST_POST + 0.62, d.tonnes.max() * 0.95, "From 2020: artisanal\nestimate dropped", fontsize=8, color=INK, va="top")
    a2.bar(yrs, d.corridor_worked, color=C["corridor"], width=0.72)
    a2.bar(yrs, d.outside_worked, bottom=d.corridor_worked, color=C["other"], width=0.72)
    a2.bar(yrs, [0] * len(yrs), bottom=d.corridor_worked, color=SURFACE, width=0.72, edgecolor=SURFACE, linewidth=1.2)
    label_end(a2, yrs[-1] + 0.4, d.corridor_worked.iloc[-1] / 2, "Corridor\nland", C["corridor"], dx=6)
    label_end(a2, yrs[-1] + 0.4, d.corridor_worked.iloc[-1] + d.outside_worked.iloc[-1] / 2, "Outside", C["other"], dx=6)
    style_axes(a2); a2.set_title("Land newly mined or re-mined, Madre de Dios (ha/yr)")
    a2.set_xticks(yrs); a2.set_xticklabels([f"'{str(y)[2:]}" for y in yrs])
    finish_figure(fig, f"Sources: BCRP (source MINEM) declared gold production, Madre de Dios; {SRC_R}. Two panels, two units. "
                       "Until 2019 the official series includes MINEM's estimate of artisanal gold; from 2020 only declared output. The 2020 "
                       "break is a definition change, not a production fall. Corridor land = D.L. 1100 tenure. Description.",
                  OUT / "fig_v2_declared_vs_mapped.png")
    X = sm.add_constant(pd.DataFrame({"post2019": (d.index >= D.FIRST_POST).astype(float), "trend": np.array(yrs) - 2010.0}, index=d.index))
    m = sm.OLS(np.log(d.tonnes), X).fit(cov_type="HAC", cov_kwds={"maxlags": 2})
    reg.add("dec_log_tonnes_post2019", m.params["post2019"], "log points", "Official gold series, log tonnes: break after 2019 net of trend (OLS, Newey-West). ARTEFACT: series drops the artisanal estimate from 2020", "description", "BCRP/MINEM")
    reg.add("dec_log_tonnes_post2019_p", m.pvalues["post2019"], "p-value", "p-value of that break", "description", "BCRP/MINEM")
    for y in (2016, 2018, 2021, 2025):
        reg.add(f"dec_t_per_1000ha_worked_{y}", 1000 * d.tonnes[y] / (d.corridor_worked[y] + d.outside_worked[y]),
                "t per 1000 ha", f"Declared tonnes per 1,000 ha of land newly mined or re-mined (not net additions), "
                f"Madre de Dios, {y}", "description", "BCRP/MINEM; MapBiomas rasters", measure="new+remined", zone="mdd",
                period=str(y))
    d.round(2).to_csv(OUT / "v2_declared_vs_mapped.csv")


def run(reg):
    print("\n== v2 extras ==")
    if not rz.OUT_ZONE.exists():
        warnings.warn("v2_extra: intermediates missing"); return
    e1(reg); e2(reg); print(e3(reg).round(2).to_string(index=False)); e4(reg); e5(reg); e6(reg)
