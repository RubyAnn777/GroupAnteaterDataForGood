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

from common import (ROOT, OUT, style_axes, finish_figure, headline, label_end, callout, period_band,
                    add_event_markers, PERU_EVENTS, EVENT_TITLE_PAD, C, INK, INK2, MUTED, AXIS, SURFACE)
import raster_zones as rz
from raster_layers import GROUPS

# zone colours by family (orange = Tambopata BZ, blue = corridor, green = protected, raspberry = native, grey = rest)
ZC = {"La Pampa sector": C["lapampa"], "Corridor across the road": C["corridor"], "Rest of mining corridor": C["corridor_rest"],
      "Native communities": C["native"], "Rest of Tambopata buffer zone": C["lapampa_tint"], "Other buffer zones": C["buffer_tint"],
      "Reserves and parks": C["reserve"], "Rest of Madre de Dios": C["other"]}
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
    yrs = [y for y in a.index if 2019 <= y <= 2025]
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(9, 4.0), gridspec_kw={"wspace": 0.45})
    headline(fig, "AMW: north of the road took most new mining in 2020–22, then La Pampa came back",
             "Amazon Mining Watch (AMW) gold-mining scars on the same zones, 2019–2025 (2025 provisional)")
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
    z = pd.read_csv(rz.OUT_ZONE)
    z["group"] = z.code.map({c: g for g, cs in GROUPS.items() for c in cs})
    w = z.groupby(["year", "group"]).remined_ha.sum().unstack().reindex(columns=list(GROUPS)).fillna(0).loc[2010:2025]
    tot = w.sum(axis=1)
    p_ = {"2016_18": (2016, 2018), "2022_25": (2022, 2025)}
    m0, m1 = (tot.loc[a:b].mean() for a, b in p_.values())
    cs = ((w["Corridor across the road"] + w["Rest of mining corridor"]) / tot).loc[2022:2025].mean()
    fig, (a1, a2) = plt.subplots(2, 1, figsize=(9, 7.0), sharex=True, gridspec_kw={"height_ratios": [1.4, 1], "hspace": 0.3})
    headline(fig, f"Returns to old pits nearly tripled after 2019, mostly inside the corridor",
             f"Old pits mined again each year, by zone, Madre de Dios. Mean {m0:,.0f} ha/yr (2016–18) → {m1:,.0f} ha/yr (2022–25); "
             f"{cs:.0%} in the corridor 2022–25")
    a1.stackplot(w.index, w.T.values, colors=[ZC[c] for c in w.columns], edgecolor=SURFACE, linewidth=0.8)
    _stack_labels(a1, w, w.index[-1], min_share=0.1)
    pk = tot.idxmax()
    callout(a1, pk, tot[pk], f"{tot[pk]:,.0f} ha in {pk}", dy=8, arrow=False)
    a1.set_ylim(0, tot.max() * 1.12); style_axes(a1)
    a1.set_title("Hectares per year", pad=EVENT_TITLE_PAD)
    sh = w.div(tot, axis=0) * 100
    a2.stackplot(sh.index, sh.T.values, colors=[ZC[c] for c in sh.columns], edgecolor=SURFACE, linewidth=0.8)
    a2.set_ylim(0, 100); style_axes(a2)
    a2.set_title("Share of the year's returns to old pits (%)")
    _stack_labels(a2, sh, sh.index[-1], min_share=0.04, total=100)
    mid = sh.loc[2021, "La Pampa sector"] + sh.loc[2021, "Corridor across the road"] / 2
    callout(a2, 2021, mid, "Corridor across the road", dx=10, dy=34, ha="left")
    a2.set_xticks(list(w.index)); a2.set_xticklabels([f"'{str(y)[2:]}" for y in w.index])
    a1.set_xlim(w.index[0], w.index[-1] + 2.9)               # right gutter for the direct labels
    for ax in (a1, a2):
        ax.spines["bottom"].set_bounds(w.index[0], w.index[-1])
    for ax in (a1, a2):
        add_event_markers(ax, label=ax is a1)
        for ln in ax.lines[-len(PERU_EVENTS):]:
            ln.set_zorder(3)                                       # draw the event lines over the stack
    finish_figure(fig, f"{SRC_R}. Return to old pits = mining on pixels mined in an earlier year but not the year before; "
                       "includes some year-to-year map flicker. Labels at the right name the bands of 2025. Description.",
                  OUT / "fig_v2_stream_remined.png", event_note=True)
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
    from matplotlib.colors import LinearSegmentedColormap
    from matplotlib.lines import Line2D
    cmap = LinearSegmentedColormap.from_list("risk", ["#f4f2ee", "#b8c3c5", "#5d7479", "#1f2d33"])
    fig = plt.figure(figsize=(9, 6.9))
    ax = fig.add_axes([0.02, 0.2, 0.96, 0.68])
    headline(fig, "New mining is predicted where mining already is",
             f"Chance of first-time mining in 2026–28 per 1-km cell. Held-out AUC {au_sp:.2f}, vs {au_b:.2f} for 'mining nearby' alone. Prediction.")
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
    fig.text(0.012, 0.008, "Source: " + SRC_R + ". Logit on 1-km cells: distance to highway and rivers, gold-bearing land, mining "
             "nearby, zone. Trained on 2018 → 2019–21,\ntested on 2022–25 in held-out 10-km blocks, applied to 2025 features. "
             "It misses the 2025 reserve incursion (river access, not in the model). Prediction, not a causal map.",
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
    z = pd.read_csv(rz.OUT_ZONE)
    lp = z[z.code == 7].set_index("year").new_land_ha.loc[2008:2025]
    tot = z.groupby("year").new_land_ha.sum().loc[2008:2025]
    fig, (a0, a1, a2) = plt.subplots(3, 1, figsize=(9, 7.6), sharex=True,
                                     gridspec_kw={"height_ratios": [1.35, 1, 1], "hspace": 0.32})
    headline(fig, "La Pampa dipped once, in 2020–21. The 2012 laws left no mark.",
             "Events by type (top) against land mined for the first time each year (hectares). Shaded: 2012–13 and 2019–21.")
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
    for ax, ser, col, title in ((a1, lp, C["lapampa"], "La Pampa sector"), (a2, tot, C["other"], "All of Madre de Dios")):
        for x0, x1 in ((2012, 2013), (2019, 2021)):
            period_band(ax, x0 - 0.5, x1 + 0.5)
        ax.bar(ser.index, ser.values, color=col, width=0.72, zorder=2)
        ax.set_ylim(0, ser.max() * 1.15); style_axes(ax); ax.set_title(title)
    callout(a1, 2020.5, lp.loc[2020:2021].max(), f"{lp.loc[2020:2021].mean():,.0f} ha/yr\n2020–21", dy=26)
    callout(a1, 2012.5, lp.loc[2012:2013].max(), f"{lp.loc[2012:2013].mean():,.0f} ha/yr\n2012–13", dy=14)
    for ax in (a0, a1, a2):
        ax.set_xlim(2007.4, 2025.8)
    a2.set_xticks(range(2008, 2026)); a2.set_xticklabels([f"'{str(y)[2:]}" for y in range(2008, 2026)])
    finish_figure(fig, f"Sources: {SRC_R}; dates from MAAP #130/#241, Asner & Tupayachi (2017), D.L. 1100/1105 (2012), Forbidden "
                       "Stories (2017 gang takeover), official government calendars. Filled dots = enforcement. Description.",
                  OUT / "fig_v2_timeline.png")
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
    fig, (a1, a2) = plt.subplots(2, 1, figsize=(9, 6.0), sharex=True, gridspec_kw={"hspace": 0.35})
    headline(fig, "Declared gold “fell” in 2020 because the series changed. Mapped mining kept growing.",
             "Top: official gold output, Madre de Dios (tonnes). Bottom: land mined for the first time (hectares).")
    a1.bar(yrs, d.tonnes, color=C["gold"], width=0.72); style_axes(a1); a1.set_title("Official gold series (tonnes)")
    a1.axvline(2019.5, color=INK, ls=(0, (3, 2)), lw=1.0)
    a1.text(2019.62, d.tonnes.max() * 0.95, "From 2020: artisanal\nestimate dropped", fontsize=8, color=INK, va="top")
    a2.bar(yrs, d.corridor_new, color=C["corridor"], width=0.72)
    a2.bar(yrs, d.outside_new, bottom=d.corridor_new, color=C["other"], width=0.72)
    a2.bar(yrs, [0] * len(yrs), bottom=d.corridor_new, color=SURFACE, width=0.72, edgecolor=SURFACE, linewidth=1.2)
    label_end(a2, yrs[-1] + 0.4, d.corridor_new.iloc[-1] / 2, "Inside the\ncorridor", C["corridor"], dx=6)
    label_end(a2, yrs[-1] + 0.4, d.corridor_new.iloc[-1] + d.outside_new.iloc[-1] / 2, "Outside", C["other"], dx=6)
    style_axes(a2); a2.set_title("Land mined for the first time (ha)")
    a2.set_xticks(yrs); a2.set_xticklabels([f"'{str(y)[2:]}" for y in yrs])
    finish_figure(fig, f"Sources: BCRP (source MINEM) declared gold production, Madre de Dios; {SRC_R}. Two panels, two units. "
                       "Until 2019 the official series includes MINEM's estimate of artisanal gold; from 2020 only declared output. The 2020 "
                       "break is a definition change, not a production fall. Description.", OUT / "fig_v2_declared_vs_mapped.png")
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
