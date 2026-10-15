"""Review session S8 (docs/methods/08_cell_panel.md): read-only checks of the 1-km cell panel (attempt A7, v2_stats.py).

Run from the repo root:  uv run python code/review/s8_cell_panel_checks.py   (writes nothing; ~10 min, mostly bootstraps and Conley errors)
Reads data_intermediate/ (cell_year_v2.csv.gz, cell_attr_v2.csv, cell_gold_v2.csv, zones_v2_mdd_full.tif) and
output/numbers.csv. Not part of main.py.
T0  trace: cell outcome rebuilt from the full zone / first-mined-year raster
T1  reproduce the main zone x period DiD (and the regression sample's cluster count)
T2  the reference cells: zeros, ever-mining cells, and the DiD as a before/after
T3  PPML: what drives the coefficient
T4  placebo strips and sliding windows (spatial permutation) for "across the road" and for La Pampa
T5  event studies (La Pampa, across the road)
T6  depletion: at-risk (hazard) outcome, pre-treatment depletion bins x year, within-La Pampa dose split
T7  clustering: 10/20/30/50-km blocks (CRV1 and WCR) and Conley spatial HAC
T8  road gradient: reference band composition, out-of-range cells
T9  gold x year control, GLAD mask look-ahead (composition only), cell purity at zone edges
T10 multiple testing (Holm)
"""
import sys, warnings
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
warnings.filterwarnings("ignore")
import numpy as np, pandas as pd, pyfixest as pf, rasterio
from scipy.spatial import cKDTree
import v2_stats as vs, raster_zones as rz
pd.set_option("display.width", 200)

d = vs.panel()
FOC = vs.FOCAL
KEY = {z: "".join(ch for ch in z.lower() if ch.isalnum())[:14] for z in FOC.values()}
LP, AC = "La Pampa sector", "Corridor across the road"
num = pd.read_csv("output/numbers.csv").set_index("id").value


def add_blocks(df, km):
    nc = 152
    r_, c_ = (df.cell - 1) // nc, (df.cell - 1) % nc
    return (r_ // km) * 1000 + (c_ // km)


def main_sample(d, clean=True):
    dm = d[d.year >= 2014]
    if clean:
        dm = dm[~((dm.focal == "reference") & dm.zone.isin(vs.CLEAN_DROP))]
    dm = dm.copy(); rhs = []
    for z, k in KEY.items():
        for p in vs.PER:
            dm[f"{k}_{p}"] = ((dm.focal == z) & (dm[f"post_{p}"] == 1)).astype(int); rhs.append(f"{k}_{p}")
    return dm, rhs


def fit(dm, rhs, y="new_land_ha", fe="cell + year", cl="block", pois=False):
    return (pf.fepois if pois else pf.feols)(f"{y} ~ {' + '.join(rhs)} | {fe}", data=dm, vcov={"CRV1": cl})


# ---------------------------------------------------------------------------------------------------------------- T0
print("T0 trace: new_land_ha per cell-year vs pixels' first-mined year in zones_v2_mdd_full.tif")
with rasterio.open(rz.OUT_FULL) as r:
    zone, first, tr = r.read(1), r.read(2), r.transform
cellk, sub = rz.cell_key(tr, zone.shape, zone > 0)
lat = tr.f + (np.arange(zone.shape[0]) + 0.5) * tr.e
row_ha = (abs(tr.a) * 111320 * np.cos(np.radians(lat))) * (abs(tr.e) * 110574) / 1e4
K = cellk.ravel(); F = first.ravel(); W = np.broadcast_to(row_ha[:, None], zone.shape).ravel(); Z = zone.ravel()
inc = K > 0
K, F, W, Z = K[inc], F[inc], W[inc], Z[inc]
n = int(cellk.max()) + 1
pix = pd.DataFrame({"cell": K[F > 0], "first": F[F > 0], "ha": W[F > 0], "pz": Z[F > 0]})
tif_new = pix.groupby(["cell", "first"]).ha.sum()
cy = pd.read_csv(rz.OUT_CELL).set_index(["cell", "year"]).new_land_ha
j = pd.concat([cy, tif_new.rename_axis(["cell", "year"])], axis=1).fillna(0)
j = j[j.index.get_level_values(1) >= 1986]
print(f"  max |cell file - raster| = {(j.iloc[:, 0] - j.iloc[:, 1]).abs().max():.4f} ha (rounding to 3 dp); "
      f"panel {d.cell.nunique():,} cells x {d.year.nunique()} years; blocks nc = 152 in both files (v2_stats.py:50, raster_zones.py:218)")
area = np.bincount(K, weights=W, minlength=n)

# ---------------------------------------------------------------------------------------------------------------- T1
print("\nT1 reproduce S1 main (clean reference, 2014-25, CRV1 10-km blocks)")
dm, rhs = main_sample(d)
f_main = fit(dm, rhs)
t1 = pd.DataFrame({"coef": f_main.coef(), "p": f_main.pvalue(),
                   "numbers.csv": [num.get(f"st_main_{c}") for c in f_main.coef().index]})
print(t1.round(4).to_string())
print(f"  clusters: full panel {d.block.nunique()} (= st_n_clusters {num['st_n_clusters']:.0f}); regression sample {dm.block.nunique()}; "
      f"La Pampa blocks {dm[dm.focal == LP].block.nunique()}, across blocks {dm[dm.focal == AC].block.nunique()}")
f_c = fit(*main_sample(d, clean=False))
print(f"  contaminated reference: LP during {f_c.coef()['lapampasector_during']:.3f} (p {f_c.pvalue()['lapampasector_during']:.3f}), "
      f"across during {f_c.coef()['corridoracross_during']:.3f}")

# ---------------------------------------------------------------------------------------------------------------- T2
print("\nT2 the reference cells")
ref = dm[dm.focal == "reference"]
ever_ref = ref.groupby("cell").new_land_ha.max() > 0
print(f"  {ref.cell.nunique():,} cells; zero cell-years {100 * (ref.new_land_ha == 0).mean():.2f}%; cells with any first-time mining 2014-25: {ever_ref.sum()}")
print("  reference cells by zone:", ref.drop_duplicates("cell").zone.map(rz.ZONES).value_counts().to_dict())
per = {"pre": (2014, 2018), "during": (2019, 2021), "after": (2022, 2025)}
def means(s):
    return {p: s[s.year.between(a, b)].new_land_ha.mean() for p, (a, b) in per.items()}
rows = []
for nm in [LP, AC, "Kotsimba", "Tambopata reserve", "reference"]:
    s = dm[dm.focal == nm]; m = means(s)
    rows.append(dict(group=nm, cells=s.cell.nunique(), pre=m["pre"], during=m["during"], after=m["after"],
                     own_change_during=m["during"] - m["pre"], own_change_after=m["after"] - m["pre"]))
t2 = pd.DataFrame(rows).set_index("group")
t2["DiD_during"] = t2.own_change_during - t2.loc["reference", "own_change_during"]
t2["DiD_after"] = t2.own_change_after - t2.loc["reference", "own_change_after"]
print(t2.round(4).to_string())
print("  => regression coefficient = own change - reference change (exact, saturated balanced panel)")

# ---------------------------------------------------------------------------------------------------------------- T3
print("\nT3 PPML")
f_p = fit(dm, rhs, pois=True)
pos = dm.groupby("cell").new_land_ha.transform("sum") > 0
def tot(s, a, b): return s[s.year.between(a, b)].groupby("year").new_land_ha.sum().mean()
rr = dm[(dm.focal == "reference") & pos]
ref_lr = np.log(tot(rr, 2019, 2021) / tot(rr, 2014, 2018))
print(f"  PPML uses cells with any positive outcome 2014-25: {dm[pos].cell.nunique():,} of {dm.cell.nunique():,} "
      f"(reference: {rr.cell.nunique()}); reference total {tot(rr, 2014, 2018):.1f} -> {tot(rr, 2019, 2021):.1f} ha/yr, log ratio {ref_lr:+.2f}")
for nm in FOC.values():
    s = dm[dm.focal == nm]
    own = np.log(tot(s, 2019, 2021) / tot(s, 2014, 2018))
    print(f"  {nm:34s} own log change {own:+.2f}  - ref {ref_lr:+.2f} = {own - ref_lr:+.2f}   PPML {f_p.coef()[KEY[nm] + '_during']:+.2f}")
fpc = fit(*main_sample(d, clean=False), pois=True)
print(f"  PPML with the contaminated reference: LP during {fpc.coef()['lapampasector_during']:+.2f}, across during {fpc.coef()['corridoracross_during']:+.2f}")

# ---------------------------------------------------------------------------------------------------------------- T4
print("\nT4 placebo strips: corridor cells (zones 5-6) by position, mean first-time ha per cell-yr")
a = d.drop_duplicates("cell").set_index("cell")
def strip(mask, label):
    cells = a.index[mask]; s = d[d.cell.isin(cells)]
    m = means(s); print(f"  {label:58s} cells {len(cells):4d}  pre {m['pre']:.2f} during {m['during']:.2f} after {m['after']:.2f}  change {m['during'] - m['pre']:+.2f}")
cor = a.zone.isin([5, 6])
strip(a.zone == 5, "zone 5 'across the road' (official)")
strip(cor & a.lon.between(-70.15, -69.80) & a.road_km.between(0.001, 10), "corridor, LP longitudes, 0-10 km N (cell-level)")
strip(cor & (a.lon > -69.80) & a.road_km.between(0.001, 10), "corridor EAST of LP window, 0-10 km N")
strip(cor & (a.lon < -70.15) & a.road_km.between(0.001, 10), "corridor WEST of LP window, 0-10 km N")
strip(cor & a.road_km.gt(10), "corridor >10 km N of road (all longitudes)")
strip(cor & a.lon.between(-70.15, -69.80) & a.road_km.gt(10), "corridor >10 km N, LP longitudes")
ref_clean = (a.focal == "reference") & ~a.zone.isin(vs.CLEAN_DROP)

def window_did(cells, label):
    s = d[(d.year >= 2014) & (d.cell.isin(cells) | d.cell.isin(a.index[ref_clean]))].copy()
    s["w_during"] = (s.cell.isin(cells) & (s.post_during == 1)).astype(int)
    s["w_after"] = (s.cell.isin(cells) & (s.post_after == 1)).astype(int)
    f = pf.feols("new_land_ha ~ w_during + w_after | cell + year", data=s, vcov={"CRV1": "block"})
    return dict(window=label, cells=len(cells), during=f.coef()["w_during"], p=f.pvalue()["w_during"], after=f.coef()["w_after"])

print("\n  T4b sliding 0.35-degree windows, corridor cells 0-10 km north of the road vs clean reference (S1-style)")
rows = []
for s0 in np.round(np.arange(-70.65, -69.649, 0.05), 2):
    cells = a.index[cor & a.lon.between(s0, s0 + 0.35) & a.road_km.between(0.001, 10)]
    if len(cells) >= 30:
        r_ = window_did(cells, f"{s0:.2f}..{s0 + 0.35:.2f}")
        r_["overlaps_LP"] = (s0 < -69.80) and (s0 + 0.35 > -70.15); rows.append(r_)
t4b = pd.DataFrame(rows); print(t4b.round(3).to_string(index=False))
real = t4b[t4b.window == "-70.15..-69.80"].during.iloc[0]
cl = t4b[~t4b.overlaps_LP]
print(f"  real window {real:.3f}: rank {1 + (t4b.during > real).sum()} of {len(t4b)} (all windows); "
      f"rank {1 + (cl.during > real).sum()} of {len(cl) + 1} vs non-overlapping windows")

print("\n  T4c sliding 0.35-degree windows, Tambopata BZ cells (zones 7-8) as fake La Pampa")
tb = a.zone.isin([7, 8])
rows = []
for s0 in np.round(np.arange(-70.40, -69.649, 0.05), 2):
    cells = a.index[tb & a.lon.between(s0, s0 + 0.35)]
    if len(cells) >= 30:
        r_ = window_did(cells, f"{s0:.2f}..{s0 + 0.35:.2f}")
        r_["overlaps_LP"] = (s0 < -69.80) and (s0 + 0.35 > -70.15)
        r_["pre_mean"] = d[d.cell.isin(cells) & d.year.between(2014, 2018)].new_land_ha.mean(); rows.append(r_)
t4c = pd.DataFrame(rows); print(t4c.round(3).to_string(index=False))

# ---------------------------------------------------------------------------------------------------------------- T5
print("\nT5 event studies (pooled 2014-18 = 0)")
for nm in (LP, AC):
    t, w = vs.event(d, nm)
    t = t.set_index("year")
    print(f"  {nm}: pre-trend p = {float(w['pvalue']):.4f}")
    print("   ", {y: (round(t.loc[y, 'Estimate'], 2), round(t.loc[y, 'Pr(>|t|)'], 3)) for y in t.index if y < 2014 or y > 2018})

# ---------------------------------------------------------------------------------------------------------------- T6
print("\nT6 depletion")
years = range(2009, 2026)
ever_by = {}
fc = pix.groupby(["cell", "first"]).ha.sum().unstack(fill_value=0).reindex(columns=range(1985, 2026), fill_value=0).cumsum(axis=1)
for y in years:
    ever_by[y] = pd.Series(0.0, index=range(n)).add(fc[y], fill_value=0)
E = pd.DataFrame(ever_by)                                         # cell x year: area ever mined by end of year
areaS = pd.Series(area)
dd = d.copy()
dd["at_risk"] = (areaS.reindex(dd.cell).values - E.stack().reindex(list(zip(dd.cell, dd.year - 1))).values)
dd["share_lag"] = 1 - dd.at_risk / areaS.reindex(dd.cell).values
dd["hazard_pct"] = np.where(dd.at_risk > 1, 100 * dd.new_land_ha / dd.at_risk, np.nan)
sh18 = (E[2018] / areaS).reindex(a.index)
a["share18"] = sh18
for nm in (LP, AC, "Kotsimba"):
    c = a.index[a.focal == nm]
    print(f"  {nm}: mined share of cell area (mean over cells) 2013 {(E[2013] / areaS)[c].mean():.3f}, 2018 {sh18[c].mean():.3f}, "
          f"2021 {(E[2021] / areaS)[c].mean():.3f}; cells >50% mined in 2018: {(sh18[c] > 0.5).sum()} of {len(c)}")
dmh, rhs = main_sample(dd)
fh = fit(dmh.dropna(subset=["hazard_pct"]), rhs, y="hazard_pct")
print("  (a) hazard outcome = first-time ha / unmined ha at t-1, %:")
for k_ in ("lapampasector", "corridoracross", "kotsimba"):
    print(f"      {k_:16s} during {fh.coef()[k_ + '_during']:+.3f} (p {fh.pvalue()[k_ + '_during']:.3f})  after {fh.coef()[k_ + '_after']:+.3f} (p {fh.pvalue()[k_ + '_after']:.3f})")
for nm in (LP, AC):
    s = dmh[dmh.focal == nm]
    print(f"      {nm} raw hazard means %: pre {s[s.year.between(2014, 2018)].hazard_pct.mean():.3f} "
          f"during {s[s.year.between(2019, 2021)].hazard_pct.mean():.3f} after {s[s.year.between(2022, 2025)].hazard_pct.mean():.3f}")
fw = pf.feols(f"hazard_pct ~ {' + '.join(rhs)} | cell + year", data=dmh.dropna(subset=["hazard_pct"]), vcov={"CRV1": "block"}, weights="at_risk")
print(f"  (a2) same, weighted by unmined area at t-1: LP during {fw.coef()['lapampasector_during']:+.3f} (p {fw.pvalue()['lapampasector_during']:.3f}), "
      f"after {fw.coef()['lapampasector_after']:+.3f}; across during {fw.coef()['corridoracross_during']:+.3f} (p {fw.pvalue()['corridoracross_during']:.3f})")
print("  (a3) zone-level hazard = sum first-time ha / sum unmined ha at t-1, %, by period:")
for nm in (LP, AC, "Kotsimba", "reference"):
    s = dmh[dmh.focal == nm]
    hz = {p: 100 * s[s.year.between(a_, b_)].new_land_ha.sum() / s[s.year.between(a_, b_)].at_risk.sum() for p, (a_, b_) in per.items()}
    print(f"      {nm:26s} pre {hz['pre']:.3f} during {hz['during']:.3f} after {hz['after']:.3f}  (during/pre {hz['during'] / hz['pre']:.2f})")
bal = dmh.groupby("cell").at_risk.transform("min") > 1
fbal = fit(dmh[bal], rhs, y="hazard_pct")
lp_ = dmh[dmh.focal == LP]
print(f"  (a4) balanced cells (unmined > 1 ha every year): LP hazard during {fbal.coef()['lapampasector_during']:+.3f} (p {fbal.pvalue()['lapampasector_during']:.3f}); "
      f"LP cell-years dropped as fully mined: {100 * lp_.hazard_pct.isna().mean():.1f}%")
print("  (a5) La Pampa zone-level hazard by year, %:", lp_.groupby("year").apply(lambda q: 100 * q.new_land_ha.sum() / q.at_risk.sum()).round(2).to_dict())
dmh["dep_bin"] = pd.cut(a.share18.reindex(dmh.cell).values, [-0.001, 0, 0.05, 0.2, 1.0], labels=["0", "0-5%", "5-20%", ">20%"]).astype(str)
print("  reference cells per 2018 depletion bin:", dmh[dmh.focal == "reference"].drop_duplicates("cell").dep_bin.value_counts().to_dict(),
      "| La Pampa cells:", dmh[dmh.focal == LP].drop_duplicates("cell").dep_bin.value_counts().to_dict())
fb = fit(dmh, rhs, fe="cell + year + dep_bin^year")
print(f"  (b) + 2018-depletion-bin x year FE: LP during {fb.coef()['lapampasector_during']:+.3f} (p {fb.pvalue()['lapampasector_during']:.3f}), "
      f"after {fb.coef()['lapampasector_after']:+.3f}; across during {fb.coef()['corridoracross_during']:+.3f} (p {fb.pvalue()['corridoracross_during']:.3f})")
fl = fit(dmh, rhs + ["share_lag"])
print(f"  (c) + lagged cumulative mined share (bad control: affected by treatment): LP during {fl.coef()['lapampasector_during']:+.3f} "
      f"(p {fl.pvalue()['lapampasector_during']:.3f}); share_lag coef {fl.coef()['share_lag']:+.2f}")
print("  (d) within La Pampa, cells split by 2018 mined share (terciles of mined cells; first-time ha per cell-yr, and hazard %)")
lpc = dmh[dmh.focal == LP].copy()
sv = a.share18.reindex(lpc.cell).values
cut = np.quantile(a.share18[(a.focal == LP) & (a.share18 > 0)], [1 / 3, 2 / 3])
lpc["tq"] = np.select([sv <= 0, sv <= cut[0], sv <= cut[1]], ["0 none", "1 low", "2 mid"], "3 high")
for q, s in lpc.groupby("tq"):
    m = means(s); h = {p: s[s.year.between(a_, b_)].hazard_pct.mean() for p, (a_, b_) in per.items()}
    print(f"      {q:5s} cells {s.cell.nunique():3d} share18 {a.share18.reindex(s.cell.unique()).mean():.2f}  ha: pre {m['pre']:.2f} during {m['during']:.2f} "
          f"after {m['after']:.2f} ({100 * (m['during'] / m['pre'] - 1):+.0f}%) | hazard: pre {h['pre']:.2f} during {h['during']:.2f} ({100 * (h['during'] / h['pre'] - 1):+.0f}%)")

# ---------------------------------------------------------------------------------------------------------------- T7
print("\nT7 clustering")
for km in (10, 20, 30, 50):
    dmk = dm.copy(); dmk["blk"] = add_blocks(dmk, km)
    f = fit(dmk, rhs, cl="blk")
    print(f"  {km:2d}-km blocks: G = {dmk.blk.nunique():3d} (LP in {dmk[dmk.focal == LP].blk.nunique()}); "
          f"LP during p = {f.pvalue()['lapampasector_during']:.3f}; across during p = {f.pvalue()['corridoracross_during']:.4f}")
for km in (10, 20, 30):
    dmk = dm.copy(); dmk["blk"] = add_blocks(dmk, km)
    p_lp = vs.wild_cluster_bootstrap(dmk, "new_land_ha", rhs, "lapampasector_during", "blk", reps=999, seed=1)
    p_ac = vs.wild_cluster_bootstrap(dmk, "new_land_ha", rhs, "corridoracross_during", "blk", reps=999, seed=1)
    print(f"  WCR {km:2d}-km blocks (999 Rademacher): LP during p = {p_lp:.3f}; across during p = {p_ac:.3f}  (cache: {num['st_wcb_lp_p']:.3f}, {num['st_wcb_across_p']:.3f})")
# Conley: spatial HAC, scores summed over years within cell (any serial correlation), uniform/Bartlett kernel across cells
Zm = vs._demean2(np.column_stack([dm.new_land_ha.values] + [dm[c].values for c in rhs]), dm.cell.values, dm.year.values)
y_, X = Zm[:, 0], Zm[:, 1:]
XtXi = np.linalg.inv(X.T @ X); b = XtXi @ X.T @ y_; e = y_ - X @ b
ci = pd.factorize(dm.cell.values)
S = np.zeros((len(ci[1]), X.shape[1])); np.add.at(S, ci[0], X * e[:, None])
cc = a.loc[ci[1]]
xy = np.column_stack([cc.lon.values * 111.32 * np.cos(np.radians(12.85)), cc.lat.values * 110.574])
tree = cKDTree(xy)
from scipy.stats import norm
for cut in (10, 25, 50):
    for kern in ("uniform", "bartlett"):   # NB the uniform kernel is not positive semi-definite in 2-D: SEs can be nan or tiny
        M = np.zeros((X.shape[1], X.shape[1]))
        for i, nb in enumerate(tree.query_ball_point(xy, cut)):
            nb = np.asarray(nb)
            wgt = np.ones(len(nb)) if kern == "uniform" else 1 - np.linalg.norm(xy[nb] - xy[i], axis=1) / cut
            M += np.outer(S[i], wgt @ S[nb])
        V = XtXi @ M @ XtXi
        se = np.sqrt(np.diag(V)); p = 2 * norm.sf(np.abs(b / se))
        print(f"  Conley {cut:2d} km {kern:8s}: LP during {b[0]:+.3f} se {se[0]:.3f} p {p[0]:.3f} | across during {b[2]:+.3f} se {se[2]:.3f} p {p[2]:.4f}")

# ---------------------------------------------------------------------------------------------------------------- T8
print("\nT8 road gradient")
g, labels = vs.gradient(d)
gs = d[d.lon.between(*rz.LP_ALT["wide"]) & d.road_km.notna()].drop_duplicates("cell").copy()
gs["band"] = pd.cut(gs.road_km, [-30, -10, -5, 0, 5, 10, 20, 30], labels=labels).astype(str)
print("  cells per band:", gs.band.value_counts().to_dict())
print("  reference band 'S 10-30' cells by zone:", gs[gs.band == "S 10-30"].zone.map(rz.ZONES).value_counts().to_dict())
oor = gs.road_km.abs() > 30       # pd.cut gives NaN there, so these cells get no band dummy and join the omitted category
print(f"  out-of-range cells (|road| > 30 km) sharing the omitted category: {oor.sum()} of {len(gs)}", gs[oor].zone.map(rz.ZONES).value_counts().to_dict())
print("  published:", {k: round(v, 3) for k, v in g.coef().items() if "after" in k})
dg = d[d.lon.between(*rz.LP_ALT["wide"]) & d.road_km.between(-30, 30)].copy()
dg["band"] = pd.cut(dg.road_km, [-30, -10, -5, 0, 5, 10, 20, 30], labels=labels).astype(str)
for variant, sub_ in (("|road| <= 30 only", dg), ("|road| <= 30, ref band without La Pampa/Kotsimba cells", dg[~((dg.band == "S 10-30") & dg.zone.isin([3, 7]))])):
    sub_ = sub_.copy(); rr_ = []
    for b_ in labels[1:]:
        for p in vs.PER:
            col = f"b_{b_.replace(' ', '').replace('-', '_')}_{p}"; sub_[col] = ((sub_.band == b_) & (sub_[f"post_{p}"] == 1)).astype(int); rr_.append(col)
    f = pf.feols(f"new_land_ha ~ {' + '.join(rr_)} | cell + year", data=sub_, vcov={"CRV1": "block"})
    print(f"  {variant}: N10-20 after {f.coef()['b_N10_20_after']:+.3f} (p {f.pvalue()['b_N10_20_after']:.3f}); "
          f"N0-5 during {f.coef()['b_N0_5_during']:+.3f}; S0-5 during {f.coef()['b_S0_5_during']:+.3f}")

# ---------------------------------------------------------------------------------------------------------------- T9
print("\nT9 gold, GLAD mask, cell purity")
gb = d.drop_duplicates("cell")
print("  gold_bin shares (all cells):", gb.gold_bin.value_counts(normalize=True).round(3).to_dict(),
      "| regression-sample reference cells:", dm[dm.focal == 'reference'].drop_duplicates('cell').gold_bin.value_counts(normalize=True).round(3).to_dict())
print("  GLAD 'mining-related' mask = first-mined year > 0 in ANY year 1985-2025 (glad_alerts.py:71). Mask composition by first-mined year:")
for code, nm in ((7, LP), (5, AC), (6, "Rest of mining corridor")):
    s = pix[pix.pz == code]
    bins = pd.cut(s["first"], [1984, 2016, 2018, 2021, 2025], labels=["<=2016", "2017-18", "2019-21", "2022-25"])
    print(f"    {nm:26s}", (s.groupby(bins, observed=False).ha.sum() / s.ha.sum()).round(3).to_dict())
print("  cell purity: share of each focal cell's 2014-25 first-time mined land lying in pixels of the cell's own zone")
p14 = pix[pix["first"].between(2014, 2025)].merge(a[["zone"]], left_on="cell", right_index=True)
p14["own"] = p14.pz == p14.zone
for code, nm in ((7, LP), (5, AC)):
    s = p14[p14.zone == code]
    print(f"    {nm:26s} own-zone share {s[s.own].ha.sum() / s.ha.sum():.3f}; other zones:",
          (s[~s.own].groupby("pz").ha.sum() / s.ha.sum()).round(3).rename(rz.ZONES).to_dict())

# ---------------------------------------------------------------------------------------------------------------- T10
print("\nT10 multiple testing")
pv = f_main.pvalue().sort_values(); m_ = len(pv)
holm = np.minimum(1, np.maximum.accumulate([(m_ - i) * p for i, p in enumerate(pv.values)]))
print(pd.DataFrame({"p": pv.values, "holm": holm}, index=pv.index).round(4).to_string())
ids = [i for i in num.index if i.startswith("st_") and i.endswith("_p")]
print(f"  p-values registered from v2_stats: {len(ids)}; below 0.05: {(num[ids] < 0.05).sum()}")
