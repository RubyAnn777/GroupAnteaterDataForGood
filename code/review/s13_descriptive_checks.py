"""Review session S13 (docs/methods/13_descriptive_predictive.md): read-only checks of the descriptive and
predictive building blocks (displacement sums, corridor share, inside the reserve, AMW zones, legality, gold proxy,
GLAD alerts, declared gold, risk map E4, economics).

Run from the repo root:  uv run python code/review/s13_descriptive_checks.py   (writes nothing; ~1 min)
Reads data/, data_intermediate/ (incl. the git-ignored zones_v2_mdd_full.tif if present), data_raw/ (ANP workbook,
SERNANP / INGEMMET / RAISG / geoBoundaries layers, BCRP), output/numbers.csv, docs/overnight/notes/economics_sources.md.
T1 displacement sums (workbook): reproduce, partition check, counterfactual trend, leakage ratio
T2 raster displacement: first-time mining by group, corridor share (mean of shares vs share of sums, 2005-09 level)
T3 inside the reserve: ANP series, 2017 transitions, raster first-time 2017, share metric
T4 AMW zone geometry: box vs department, BZ x corridor overlaps, ring areas vs ring shares, TNR products side by side
T5 legality: reproduce shares, one-directional correction, within vs between corridor decomposition
T6 gold proxy: strict vs broad, where La Pampa's mining sits, ranking reversal
T7 GLAD: reproduce La Pampa series, 2021 collection break across zones and on non-mining land
T8 declared gold: MINEM vs BCRP for the economics denominator
T9 risk map E4: reproduce AUCs, block-split seeds, other benchmarks, hard cells, calibration, threshold, regime shift,
   road distance error
T10 economics: reproduce, without 2023, pit depth, BCRP denominator, parameter sources present
"""
import re
import numpy as np, pandas as pd
import warnings
warnings.filterwarnings("ignore")
pd.set_option("display.width", 200)
N = pd.read_csv("output/numbers.csv").set_index("id").value
P3 = {"2016-18": (2016, 2018), "2019-21": (2019, 2021), "2022-25": (2022, 2025)}
pm = lambda s: pd.Series({k: s.loc[a:b].mean() for k, (a, b) in P3.items()})

# ------------------------------------------------------------------ T1 displacement sums (workbook)
print("=" * 30, "T1 displacement sums (statistics workbooks)")
zb = pd.read_csv("data/peru_bufferzone_year.csv"); pe = pd.read_csv("data/peru_department_year.csv")
zb["unit"] = zb.buffer_zone + "|" + zb.pa_category
lv = zb.groupby(["unit", "year"]).mining_ha.sum().unstack("unit")
T, A, B = "Tambopata|Reserva Nacional", "Amarakaeri|Reserva Comunal", "Bahuaja-Sonene|Parque Nacional"
mdd = pe[(pe.department == "Madre de Dios") & (pe.biome == "Amazonía")].groupby("year").mining_ha.sum()
bz_mdd = zb[zb.department == "Madre de Dios"].groupby("year").mining_ha.sum()
three_mdd = zb[(zb.department == "Madre de Dios") & zb.unit.isin([T, A, B])].groupby("year").mining_ha.sum()
L = pd.DataFrame({"MdD total": mdd, "Three BZ (all depts, as coded)": lv[[T, A, B]].sum(axis=1),
                  "Three BZ (MdD rows only)": three_mdd, "Rest of MdD": mdd - bz_mdd, "Tambopata BZ": lv[T]})
ad = L.diff()
print(pd.DataFrame({u: pm(ad[u]) for u in ad}).T.round(0).to_string())
print("ids: displacement_mdd_total_chg_2019_21 =", round(N["displacement_mdd_total_chg_2019_21_vs_2016_18"]),
      "| three_bz", round(N["displacement_three_bz_sum_chg_2019_21_vs_2016_18"]), "| rest", round(N["displacement_rest_mdd_chg_2019_21_vs_2016_18"]))
gap = (L["Three BZ (all depts, as coded)"] + L["Rest of MdD"] - L["MdD total"])
print("partition gap (three BZ as coded + rest - MdD total), ha:", gap.loc[[2016, 2018, 2021, 2025]].round(0).to_dict(),
      "= mining of Amarakaeri BZ in Cusco + Bahuaja-Sonene BZ in Puno + Tambopata BZ in Puno")
tot = ad["MdD total"]
# counterfactual trend: linear trend of MdD additions 2010-18, extrapolated
yrs = np.arange(2010, 2019); b = np.polyfit(yrs, tot.loc[2010:2018].values, 1)
pred = np.polyval(b, np.arange(2019, 2022)).mean()
print(f"MdD total additions: linear trend 2010-18 slope {b[0]:.0f} ha/yr per yr; extrapolated 2019-21 mean {pred:,.0f} "
      f"vs observed {tot.loc[2019:2021].mean():,.0f} ha/yr")
chg = pd.Series({s: tot.loc[s:s + 2].mean() - tot.loc[s - 3:s - 1].mean() for s in range(1990, 2017)})
print("historical change in MdD 3-yr mean additions vs the previous 3 yrs (start s, windows ending by 2018):")
print("  ", chg.round(0).astype(int).to_dict())
print(f"  real 2019-21 vs 2016-18 = {tot.loc[2019:2021].mean() - tot.loc[2016:2018].mean():+,.0f}; "
      f"share of earlier changes >= it: {(chg >= tot.loc[2019:2021].mean() - tot.loc[2016:2018].mean()).mean():.2f}")
print("MdD total additions by year 2010-2025:", tot.loc[2010:2025].round(0).astype(int).to_dict())
fall = -(pm(ad["Tambopata BZ"])["2019-21"] - pm(ad["Tambopata BZ"])["2016-18"])
rise = pm(ad["Rest of MdD"])["2019-21"] - pm(ad["Rest of MdD"])["2016-18"]
print(f"naive leakage ratio (rest-of-MdD rise / Tambopata fall), 2019-21: {rise:,.0f} / {fall:,.0f} = {rise / fall:.2f}")

# ------------------------------------------------------------------ T2 raster displacement (first-time mining)
print("=" * 30, "T2 raster displacement (first-time mining, MapBiomas Col 4 rasters)")
z = pd.read_csv("data_intermediate/zone_year_v2.csv")
G = {"La Pampa sector": [7], "Corridor across the road": [5], "Rest of mining corridor": [6], "Native communities": [3, 4],
     "Rest of Tambopata BZ": [8], "Other BZs": [9, 10, 11], "Reserves and parks": [1, 2], "Rest of MdD": [12]}
z["group"] = z.code.map({c: g for g, cs in G.items() for c in cs})
w = z.groupby(["year", "group"]).new_land_ha.sum().unstack().reindex(columns=list(G)).fillna(0)
tab = pd.DataFrame({g: pm(w[g]) for g in G}).T
tab.loc["Total"] = pm(w.sum(axis=1))
tab["chg 19-21"] = tab["2019-21"] - tab["2016-18"]; tab["chg 22-25"] = tab["2022-25"] - tab["2016-18"]
print(tab.round(0).to_string())
cor = w["Corridor across the road"] + w["Rest of mining corridor"]
sh = cor / w.sum(axis=1) * 100
print("corridor share, mean of yearly shares:", pm(sh).round(1).to_dict(), "| ids", [round(N[f"v2_corridor_share_{k}"], 1) for k in ("2016_18", "2019_21", "2022_25")])
print("corridor share, share of period sums:", pd.Series({k: cor.loc[a:b].sum() / w.loc[a:b].sum().sum() * 100 for k, (a, b) in P3.items()}).round(1).to_dict())
print("corridor share 2005-09 mean:", round(sh.loc[2005:2009].mean(), 1), "| 2010-13:", round(sh.loc[2010:2013].mean(), 1),
      "| 2014-18:", round(sh.loc[2014:2018].mean(), 1), "| yearly 2010-2025:", sh.loc[2010:2025].round(0).astype(int).to_dict())
yrs = np.arange(2010, 2019); rc = w["Rest of mining corridor"]
b = np.polyfit(yrs, rc.loc[2010:2018].values, 1)
print(f"rest of corridor first-time: trend 2010-18 slope {b[0]:.0f} ha/yr per yr; extrapolated 2019-21 {np.polyval(b, np.arange(2019, 2022)).mean():,.0f} "
      f"vs observed {rc.loc[2019:2021].mean():,.0f}; 2010-18 by year {rc.loc[2010:2018].round(0).astype(int).to_dict()}")

# ------------------------------------------------------------------ T3 inside the reserve
print("=" * 30, "T3 inside Tambopata National Reserve")
f = "data_raw/mapbiomas_peru/MAPBIOMAS-PERU-LULC-COL4-AREAS-PROTEGIDAS.xlsx"
cv = pd.read_excel(f, sheet_name="COVERAGE_4")
yc = [f"y{y}" for y in range(2010, 2026)]
tnr = cv[(cv.territory_level_2_1 == "Tambopata") & (cv.class_level_4 == "4.2. Minería")][yc].sum()
tnr.index = range(2010, 2026); tadd = tnr.diff()
print("level 2025", round(tnr[2025], 1), "| additions 2011-25:", tadd.loc[2011:].round(0).astype(int).to_dict())
print("territory names matching 'Tambopata' in COVERAGE_4:", cv[cv.territory_level_2_1.str.contains("Tambopata", na=False)][["territory_level_2_1", "territory_level_3_1"]].drop_duplicates().values.tolist())
tr = pd.read_excel(f, sheet_name="TRANSITION_4")
print("territory_level_2 names matching 'Tambopata' in TRANSITION_4:", sorted(tr[tr.territory_level_2.str.contains("Tambopata", na=False)].territory_level_2.unique()))
t = tr[tr.territory_level_2 == "Tambopata"]
into = t[(t.class_level_2_to == "4.2. Minería") & (t.class_from != 30)].groupby("class_level_2_from").p2016_2017.sum()
print("2016->17 inflow into mining by origin class, ha:", into[into > 0.5].round(1).sort_values(ascending=False).to_dict(), "| total", round(into.sum(), 1))
r1 = z[z.code == 1].set_index("year")
print("raster zone 1 (Tambopata reserve) first-time / re-mined / net, 2015-2025:")
print(r1.loc[2015:2025, ["new_land_ha", "remined_ha", "stopped_ha", "mining_ha"]].round(0).T.to_string())
nr, comb = tadd, tadd + ad["Tambopata BZ"]
for k, (a, b) in P3.items():
    print(f"  {k}: NR mean add {nr.loc[a:b].mean():7.1f}  BZ+NR {comb.loc[a:b].mean():8.1f}  'share' {nr.loc[a:b].mean() / comb.loc[a:b].mean():6.3f}")

# ------------------------------------------------------------------ T4 AMW zone geometry
print("=" * 30, "T4 AMW zones (spatial.py) geometry")
import geopandas as gpd
from shapely.geometry import box
from shapely.ops import unary_union
CRS = "ESRI:102033"
dep = gpd.read_file("data_raw/geoboundaries/geoBoundaries-PER-ADM1.geojson").to_crs(CRS)
mddg = dep[dep.shapeName == "Madre de Dios"].geometry.union_all(); peru = dep.geometry.union_all()
bx = gpd.GeoSeries([box(-72.6, -14.6, -68.6, -10.5)], crs=4326).to_crs(CRS).iloc[0]
print(f"MDD_BOX {bx.area / 1e6:,.0f} km2; Madre de Dios {mddg.area / 1e6:,.0f} km2; box outside MdD {bx.difference(mddg).area / 1e6:,.0f} km2 "
      f"({bx.difference(mddg).area / bx.area:.0%}); outside Peru {bx.difference(peru).area / 1e6:,.0f} km2; "
      f"MdD outside box {mddg.difference(bx).area / 1e6:,.0f} km2")
print("  box overlap by department (km2):", {r.shapeName: round(r.geometry.intersection(bx).area / 1e6) for r in dep.itertuples() if r.geometry.intersection(bx).area > 1e8})
anp = gpd.read_file("data_raw/sernanp/anp_definitivas.geojson").to_crs(CRS)
za = gpd.read_file("data_raw/sernanp/zonas_amortiguamiento.geojson").to_crs(CRS)
corr = gpd.read_file("data_raw/ingemmet/corredor_minero_madre_de_dios_DL1100.geojson").to_crs(CRS).geometry.union_all()
g = lambda df, c: unary_union(df[df.anp_codi == c].geometry)
for nm, c in (("Tambopata BZ", "RN09"), ("Amarakaeri BZ", "RC03"), ("Bahuaja-Sonene BZ", "PN08")):
    zz = g(za, c)
    print(f"  {nm}: {zz.area / 1e6:,.0f} km2, of which in the D.L. 1100 corridor {zz.intersection(corr).area / 1e6:,.0f} km2 "
          f"(spatial.py assigns it to the BZ; raster_zones.py to the corridor)")
print("  ring areas 0-10 / 10-25 / 25-50 km (km2):", [round(np.pi * (b_ ** 2 - a_ ** 2)) for a_, b_ in ((0, 10), (10, 25), (25, 50))],
      "-> area shares", [round(100 * (b_ ** 2 - a_ ** 2) / 2500, 1) for a_, b_ in ((0, 10), (10, 25), (25, 50))])
for lab in ("2019_21", "2022_24"):
    s = [N[f"sp_lp_ring_{k}km_share_{lab}"] for k in ("0_10", "10_25", "25_50")]
    a_ = [4.0, 21.0, 75.0]
    print(f"  AMW ring shares {lab}: {[round(x, 1) for x in s]}  density relative to the 50-km disc: {[round(x / y, 2) for x, y in zip(s, a_)]}")
amw = pd.read_csv("data_intermediate/amw_zone_year.csv")
aw = amw.pivot(index="year", columns="unit", values="new_ha")
print("AMW new ha by zone, 2019-2026 (2018 = stock):"); print(aw.loc[2019:2026].round(0).astype(int).T.to_string())
print("Tambopata NR side by side: MapBiomas ANP net add 2025", round(tadd[2025]), "| raster first-time 2025", round(r1.loc[2025, "new_land_ha"]),
      "| AMW 2025", aw.loc[2025, "Tambopata NR"], "(prov.) | AMW 2026", aw.loc[2026, "Tambopata NR"], "(prov., part-year) | MAAP #241 ~500 ha H2 2025-Feb 2026")
print("  AMW 2019-24 sum", round(aw.loc[2019:2024, "Tambopata NR"].sum()), "vs MapBiomas ANP net adds 2019-24 sum", round(tadd.loc[2019:2024].sum()),
      "vs raster first-time 2019-24 sum", round(r1.loc[2019:2024, "new_land_ha"].sum()))

# ------------------------------------------------------------------ T5 legality
print("=" * 30, "T5 legality layer (v2_legality.py)")
lg = pd.read_csv("data_intermediate/legality_year_v2.csv"); tc = pd.read_csv("data_intermediate/legality_year_v2_timeconsistent.csv")
def shares(d, by=None):
    out = {}
    for k, (a, b) in P3.items():
        s = d[d.year.between(a, b)].groupby("level").ha.sum(); s = s / s.sum()
        out[k] = s.get(3, 0) + s.get(4, 0)
    return pd.Series(out)
print("High+Very high share, today's concessions:", shares(lg).round(3).to_dict(), "| time-consistent:", shares(tc).round(3).to_dict())
print("T7 (outside corridor and communities):", {k: round(N[f"t7_presumed_illegal_share_{k}"], 3) for k in ("2016_18", "2019_21", "2022_25")})
for k, (a, b) in P3.items():
    o = lg[lg.year.between(a, b)].groupby("level").ha.sum(); n_ = tc[tc.year.between(a, b)].groupby("level").ha.sum()
    print(f"  {k}: ha by level today {o.round(0).astype(int).to_dict()} -> time-consistent {n_.round(0).astype(int).to_dict()}"
          f" (Low+Medium moved to High: {(o.get(1, 0) + o.get(2, 0) - n_.get(1, 0) - n_.get(2, 0)):,.0f} ha; moved down: 0 by construction)")
print("within / between decomposition (today's concessions):")
rows = []
for k, (a, b) in P3.items():
    d = lg[lg.year.between(a, b)]
    for cflag, nm in ((True, "corridor"), (False, "outside")):
        s = d[d.corridor == cflag].groupby("level").ha.sum()
        rows.append(dict(period=k, part=nm, ha_share=d[d.corridor == cflag].ha.sum() / d.ha.sum(), illegal=(s.get(3, 0) + s.get(4, 0)) / s.sum()))
dd = pd.DataFrame(rows).pivot(index="period", columns="part")
print(dd.round(3).to_string())
w0, w2 = dd.loc["2016-18"], dd.loc["2022-25"]
within = (w0.ha_share * (w2.illegal - w0.illegal)).sum(); between = ((w2.ha_share - w0.ha_share) * w0.illegal).sum()
print(f"  change 2016-18 -> 2022-25 {shares(lg)['2022-25'] - shares(lg)['2016-18']:+.3f} = within {within:+.3f} + mix {between:+.3f} + interaction")

# ------------------------------------------------------------------ T6 gold proxy
print("=" * 30, "T6 gold-left proxy (raster_gold.py)")
gd = pd.read_csv("data_intermediate/gold_depletion_v2.csv")
gd["on_gold_share_of_mined"] = gd.mined_ever_on_gold_ha / gd.mined_ever_ha
cols = ["unit", "definition", "gold_land_ha", "mined_ever_ha", "on_gold_share_of_mined", "depleted_share_2018", "depleted_share_2025"]
print(gd[gd.zone_code.isin([0, 3, 5, 6, 7, 9])][cols].round(3).to_string(index=False))
print("lift strict / broad:", round(N["gold_strict_lift"], 2), round(N["gold_broad_lift"], 2), "| validation", round(N["gold_strict_validation"], 2), round(N["gold_broad_validation"], 2))

# ------------------------------------------------------------------ T7 GLAD
print("=" * 30, "T7 GLAD-L alerts (glad_alerts.py)")
gl = pd.read_csv("data_intermediate/glad_zone_quarter_v2.csv")
gl["group"] = gl.code.map({c: g for g, cs in G.items() for c in cs})
ann = gl.groupby(["year", "mining", "group"]).ha.sum().unstack(["mining", "group"]).fillna(0)
print("La Pampa, mining-land alerts by year:", ann[(True, "La Pampa sector")].round(0).astype(int).to_dict())
print("ratio 2021 / mean(2020, 2022) by group (C1 -> C2 break in 2021):")
for m_ in (True, False):
    r = {g_: round(ann.loc[2021, (m_, g_)] / ann.loc[[2020, 2022], (m_, g_)].mean(), 2) for g_ in G if (m_, g_) in ann and ann.loc[[2020, 2022], (m_, g_)].mean() > 50}
    print(f"  {'mining land' if m_ else 'non-mining land'}: {r}")
allg = gl.groupby(["year", "mining"]).ha.sum().unstack()
print("all MdD alerts by year, mining / non-mining land:", allg.round(0).astype(int).T.to_dict())
print("quarters present in last year:", sorted(gl[gl.year == gl.year.max()].quarter.unique()), "year", gl.year.max())

# ------------------------------------------------------------------ T8 declared gold
print("=" * 30, "T8 declared gold (MINEM files vs BCRP)")
mn = pd.read_csv("data_intermediate/minem_mdd_gold.csv").set_index("year")
bc = pd.read_csv("output/peru_production_vs_area.csv").set_index("year").tonnes * 1000
cmp_ = pd.DataFrame({"minem_total_kg": mn.total_kg, "bcrp_kg": bc}).loc[2014:2025]
cmp_["minem_over_bcrp"] = cmp_.minem_total_kg / cmp_.bcrp_kg - 1
print(cmp_.round(3).to_string())

# ------------------------------------------------------------------ T9 risk map E4
print("=" * 30, "T9 risk map E4 (v2_extra.py e4)")
import statsmodels.api as sm
warnings.simplefilter("ignore")
a = pd.read_csv("data_intermediate/cell_attr_v2.csv").merge(pd.read_csv("data_intermediate/cell_gold_v2.csv"), on="cell", how="left")
y = pd.read_csv("data_intermediate/cell_year_v2.csv.gz")
idx = pd.MultiIndex.from_product([a.cell, range(2010, 2026)], names=["cell", "year"])
y = y.set_index(["cell", "year"]).reindex(idx).fillna(0)
stock = y.mining_ha.unstack(); new = y.new_land_ha.unstack(); a = a.set_index("cell")
STUDY = (-70.65, -13.30, -69.30, -12.40); nc = int(np.ceil((STUDY[2] - STUDY[0]) / (33 * 0.000269495)))
def neigh(s):
    r_, c_ = (s.index - 1) // nc, (s.index - 1) % nc
    gg = pd.Series(s.values, index=pd.MultiIndex.from_arrays([r_, c_])); out = np.zeros(len(s))
    for dr in range(-3, 4):
        for dc in range(-3, 4):
            out += gg.reindex(pd.MultiIndex.from_arrays([r_ + dr, c_ + dc])).fillna(0).values
    return out
ZG = {"Reserves and parks": [1, 2], "Native communities": [3, 4], "La Pampa sector": [7], "Rest of Tambopata buffer zone": [8], "Other buffer zones": [9, 10, 11]}
def feats(yr, road=None):
    X = pd.DataFrame(index=a.index)
    X["road_abs_km"] = (a.road_km.abs() if road is None else road).fillna(60).clip(upper=60)
    X["north"] = (a.road_km > 0).astype(float); X["river_km"] = a.river_km.clip(upper=30)
    X["gold_share"] = a.gold_share.fillna(0); X["mined_share"] = (stock[yr] / a.area_ha).clip(0, 1)
    X["neigh_mining_km2"] = neigh(stock[yr]) / 100
    for g_ in ZG: X[f"z_{g_[:12]}"] = a.zone.isin(ZG[g_]).astype(float)
    X["corridor"] = a.zone.isin([5, 6]).astype(float)
    return sm.add_constant(X)
def auc(yv, p):
    r = pd.Series(np.asarray(p)).rank().values; yv = np.asarray(yv); n1 = yv.sum(); n0 = len(yv) - n1
    return (r[yv == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0)
def ap(yv, p):   # average precision
    o = np.argsort(-np.asarray(p)); yv = np.asarray(yv)[o]; tp = np.cumsum(yv)
    return (tp / np.arange(1, len(yv) + 1))[yv == 1].mean()
ytr = (new.loc[:, 2019:2021].sum(axis=1) > 1).astype(int); yte = (new.loc[:, 2022:2025].sum(axis=1) > 1).astype(int)
X18, X21 = feats(2018), feats(2021)
m = sm.Logit(ytr, X18).fit(disp=0); p_all = m.predict(X21)
blk = ((a.index - 1) // nc // 10) * 1000 + ((a.index - 1) % nc // 10)
def split(seed):
    rng = np.random.default_rng(seed); ub = np.unique(blk); trb = set(rng.choice(ub, size=len(ub) // 2, replace=False))
    tr_ = np.isin(blk, list(trb)); return tr_, ~tr_
tr_, te = split(0)
msp = sm.Logit(ytr[tr_], X18[tr_]).fit(disp=0); psp = msp.predict(X21[te])
bc_ = ["const", "neigh_mining_km2"]; mb = sm.Logit(ytr[tr_], X18.loc[tr_, bc_]).fit(disp=0); pb = mb.predict(X21.loc[te, bc_])
print(f"reproduce: AUC full-sample {auc(yte, p_all):.4f} (id {N['risk_auc_2022_25']:.4f}); hold-out {auc(yte[te], psp):.4f} (id {N['risk_auc_spatial_holdout']:.4f}); "
      f"benchmark {auc(yte[te], pb):.4f} (id {N['risk_auc_benchmark']:.4f})")
print(f"cells {len(a):,}; positives train {ytr.sum()} ({ytr.mean():.1%}), test {yte.sum()} ({yte.mean():.1%}); hold-out test cells {te.sum():,}")
# benchmarks without any model
yt = yte[te]
bm = {"neigh mining 2021 (raw)": X21.loc[te, "neigh_mining_km2"], "own mined share 2021": X21.loc[te, "mined_share"],
      "first-time >1 ha in 2019-21 (persistence)": ytr[te] + 1e-6 * X21.loc[te, "neigh_mining_km2"],
      "first-time ha in 2019-21 (persistence, continuous)": new.loc[a.index[te], 2019:2021].sum(axis=1)}
for k, v in bm.items():
    print(f"  benchmark {k:52s} AUC {auc(yt, v):.3f}  AP {ap(yt, v):.3f}")
print(f"  full model (hold-out)                                         AUC {auc(yt, psp):.3f}  AP {ap(yt, psp):.3f}  (base rate {yt.mean():.3f})")
print(f"  logit benchmark (neigh only, hold-out)                        AUC {auc(yt, pb):.3f}  AP {ap(yt, pb):.3f}")
gains = []
for s in range(50):
    tr_s, te_s = split(s)
    try:
        p1 = sm.Logit(ytr[tr_s], X18[tr_s]).fit(disp=0).predict(X21[te_s]); p2 = sm.Logit(ytr[tr_s], X18.loc[tr_s, bc_]).fit(disp=0).predict(X21.loc[te_s, bc_])
        gains.append((auc(yte[te_s], p1), auc(yte[te_s], p2)))
    except Exception:
        pass
gg = pd.DataFrame(gains, columns=["full", "bench"]); gg["gain"] = gg.full - gg.bench
print(f"50 block splits: full AUC {gg.full.min():.3f}-{gg.full.max():.3f} (median {gg.full.median():.3f}); bench {gg.bench.min():.3f}-{gg.bench.max():.3f}; "
      f"gain {gg.gain.min():+.3f} to {gg.gain.max():+.3f} (median {gg.gain.median():+.3f}; share > 0: {(gg.gain > 0).mean():.2f}); n = {len(gg)}")
hard = te & (X21.neigh_mining_km2.values > 0)
print(f"hard cells (hold-out, some mining within ~3 km in 2021): n = {hard.sum()}, positives {yte[hard].mean():.1%}; "
      f"AUC full {auc(yte[hard], msp.predict(X21[hard])):.3f} vs bench {auc(yte[hard], mb.predict(X21.loc[hard, bc_])):.3f}")
q = pd.qcut(psp, 10, labels=False, duplicates="drop")
cal = pd.DataFrame({"pred": psp.values, "obs": yt.values, "q": q}).groupby("q").mean()
print("calibration on hold-out (deciles of predicted risk; trained on a 3-yr outcome, tested on a 4-yr outcome):")
print("  ", cal.round(3).T.to_string().replace("\n", "\n   "))
print(f"  mean predicted {psp.mean():.3f} vs observed {yt.mean():.3f}")
hi_ = psp > 0.5
print(f"threshold 0.5 on hold-out: flagged {hi_.sum()} cells, precision {yt[hi_].mean():.2f}, recall {yt[hi_].sum() / yt.sum():.2f}")
# regime shift: train before Mercurio (2014 features -> 2015-17), test on 2018 -> 2019-21; compare La Pampa coefficient
y_pre = (new.loc[:, 2015:2017].sum(axis=1) > 1).astype(int)
m_pre = sm.Logit(y_pre, feats(2014)).fit(disp=0)
print(f"regime shift: model trained 2014 -> 2015-17 predicts 2018 -> 2019-21 with AUC {auc(ytr, m_pre.predict(X18)):.3f}; "
      f"La Pampa dummy coef pre {m_pre.params['z_La Pampa sec']:+.2f} vs 2019-21-trained {m.params['z_La Pampa sec']:+.2f}; "
      f"reserves dummy {m_pre.params['z_Reserves and']:+.2f} vs {m.params['z_Reserves and']:+.2f}")
lp = a.zone.isin([7]).values
print(f"  La Pampa cells: mean predicted 2019-21 risk by the pre-Mercurio model {m_pre.predict(X18)[lp].mean():.2f} vs observed {ytr[lp].mean():.2f}")
ap_ = a.copy(); ap_["risk"] = m.predict(feats(2025)).values
hi = ap_[(ap_.risk > 0.5) & ~ap_.zone.isin([5, 6])]
print("high-risk (>0.5) cells outside corridor by zone:", hi.zone.value_counts().sort_index().to_dict(), "total", len(hi))
res = a.zone.isin([1, 2]).values
print(f"reserve cells: n {res.sum()}, with >1 ha first-time 2022-25: {yte[res].sum()}, max predicted 2026-28 risk {ap_.risk[res].max():.3f}")
# road distance: coded |road_km| (vertical latitude difference) vs true distance to the highway
roads = gpd.read_file("data_raw/raisg/vias_nacionales_mdd_box.geojson"); ioh = roads[roads.sigla == "PE-30C"].to_crs(CRS).geometry.union_all()
pts = gpd.GeoSeries(gpd.points_from_xy(a.lon, a.lat), crs=4326).to_crs(CRS)
true_km = pts.distance(ioh).values / 1e3
err = a.road_km.abs().values - true_km
print(f"road distance: coded |road_km| minus true distance, km: median {np.nanmedian(err):.2f}, share of cells off by > 2 km {np.nanmean(np.abs(err) > 2):.2%}, "
      f"> 5 km {np.nanmean(np.abs(err) > 5):.2%}; NaN coded {np.isnan(a.road_km.values).sum()}")
big = np.abs(err) > 5
if big.any():
    print(f"  cells off by > 5 km: lon {a.lon[big].min():.2f} to {a.lon[big].max():.2f}, lat {a.lat[big].min():.2f} to {a.lat[big].max():.2f}; "
          f"median coded {np.nanmedian(a.road_km.abs().values[big]):.1f} vs true {np.median(true_km[big]):.1f} km")
    print("  by lon bin (share of cells off > 2 km):", pd.Series(np.abs(err) > 2).groupby(pd.cut(a.lon.values, np.arange(-70.7, -69.25, 0.1))).mean().round(2).to_dict())
wide = a.lon.between(-70.20, -69.75).values
print(f"  inside the 'wide' La Pampa window (-70.20..-69.75, used by v2_stats road bands): share off > 2 km {np.mean(np.abs(err[wide]) > 2):.2%}")
zp = pd.DataFrame({"zone": a.zone.values, "coded": a.road_km.abs().values, "true": true_km, "w": a.area_ha.values})
zp["group"] = zp.zone.map({c: g for g, cs in G.items() for c in cs})
print("  zone profile km to highway (area-weighted), coded vs true:",
      {g_: (round(np.average(d.coded, weights=d.w), 1), round(np.average(d.true, weights=d.w), 1)) for g_, d in zp.groupby("group")})
mt = sm.Logit(ytr[tr_], feats(2018, pd.Series(true_km, index=a.index))[tr_]).fit(disp=0)
print(f"  hold-out AUC with true road distance: {auc(yt, mt.predict(feats(2021, pd.Series(true_km, index=a.index))[te])):.4f} (coded: {auc(yt, psp):.4f})")

# ------------------------------------------------------------------ T10 economics
print("=" * 30, "T10 economics (v2_economics.py)")
zt = z.groupby("year")[["new_land_ha", "remined_ha"]].sum()
pr = pd.read_csv("data/prices_annual.csv").set_index("year")
gcol = [c for c in pr.columns if "gold" in c.lower()][0]
yrs_all, yrs_ex = [2022, 2023, 2024, 2025], [2022, 2024, 2025]
for lab, ys in (("2022-25", yrs_all), ("2022-25 without 2023", yrs_ex)):
    nh = zt.loc[ys, "new_land_ha"].mean()
    print(f"  {lab}: first-time {nh:,.0f} ha/yr -> gold {nh * 1.6 / 1000:.1f}-{nh * 1.9 / 1000:.1f} t/yr; 5-m pits (x2): {nh * 3.2 / 1000:.1f}-{nh * 3.8 / 1000:.1f} t/yr")
print("  ids gold_t:", round(N["eco_gold_t_lo_2022_25"], 2), round(N["eco_gold_t_hi_2022_25"], 2), "| declared share", round(N["eco_declared_share_lo"], 3), round(N["eco_declared_share_hi"], 3))
dec_b = bc.loc[2022:2025].mean()
print(f"  declared, BCRP 2022-25 mean {dec_b:,.0f} kg vs MINEM {mn.loc[2022:2025, 'declared_kg'].mean():,.0f} kg -> share {dec_b / (N['eco_gold_t_hi_2022_25'] * 1000):.3f}-{dec_b / (N['eco_gold_t_lo_2022_25'] * 1000):.3f}")
print("  enforcement share of gold value:", round(N["eco_spend_share_of_value"], 5), "| tax wedge", N["eco_tax_share_value_lo"], N["eco_tax_share_value_hi"])
src = open("docs/overnight/notes/economics_sources.md", encoding="utf-8").read()
for k, pat in {"yield 1.6-1.9 (Cuadro 3)": r"Cuadro 3", "margin 11/23.9/36.8": r"36\.8", "income tax 29.5": r"29[.,]5", "Hg 2.4-2.8": r"2\.4 a 2\.8",
               "social 81,000-364,000": r"81,000 and US\$364,000", "social 1.2-1.8 M": r"1,2 mill"}.items():
    print(f"  source for {k:28s} present in economics_sources.md: {bool(re.search(pat, src))}")
import os
print("  CSF 2023 PDF present:", os.path.exists("data_raw/literature/CSF_2023_Metodologia_Valorizacion_Mineria_Ilegal_Oro_Peru.pdf"))
