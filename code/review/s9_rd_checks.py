"""Review session S9 (docs/methods/09_spatial_rd.md): read-only checks of the spatial RD (A8, code/v2_rdd.py) and the
road fake-date test (A9, code/v2_tests.py:35-60, code/placebo_explainer.py).

Run from the repo root:  uv run python code/review/s9_rd_checks.py   (writes nothing; ~10 min)
Needs data_intermediate/zones_v2_mdd_full.tif (git-ignored but present here) for T5/T6/T8b; the rest uses the
committed rdd_units_v2.csv / rdd_unit_year_v2.csv / road_band_year_v2.csv / cell_*_v2.csv.

T1  reproduce the headline road and reserve diff-in-disc (rdrobust, mserd, triangular, CR1 by 2-km segment)
T2  constant-gap assumption: yearly gap at the road (fixed h) and the choice of PRE window
T3  timing: 2019 alone vs 2020-21; later years with and without 2023
T4  fake start years: road as coded; reserve pool padded from 1998 vs from 2007
T5  running variable: latitude offset vs true perpendicular distance (UTM 19S), rebuild and rerun
T6  depletion and geology across the road: share mined by 2018, at-risk denominator, gold proxy
T7  inference and bandwidth: CR1 vs CR3, 4-km and 6-km segment clusters, fixed h, donut (own and fixed h)
T8  reserve edge: the 2017 invasion, PRE windows, share within 1 km without 2017, river distance
T9  A9 road fake-date test (north share): +-30 km as coded vs +-15 km, which start years are "clean", two-sided
"""
import sys, io, contextlib, warnings
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "code"))
import v2_rdd as R                      # noqa: E402
import raster_zones as rz               # noqa: E402
import v2_tests                         # noqa: E402
from common import placebo_rank        # noqa: E402

warnings.filterwarnings("ignore")
pd.set_option("display.width", 200)


def rd(y, x, cl, w, h=None, c=0.0, vce="hc1"):
    from rdrobust import rdrobust
    with contextlib.redirect_stdout(io.StringIO()):
        r = rdrobust(y=np.asarray(y, float), x=np.asarray(x, float), c=c, h=h, cluster=np.asarray(cl),
                     weights=np.asarray(w, float), vce=vce)
    return dict(est=float(r.coef.iloc[0, 0]), lo=float(r.ci.iloc[2, 0]), hi=float(r.ci.iloc[2, 1]),
                p=float(r.pv.iloc[2, 0]), h=float(r.bws.iloc[0, 0]), n=int(r.N_h[0] + r.N_h[1]))


def fmt(r):
    return f"{r['est']:+.3f} [{r['lo']:+.2f}, {r['hi']:+.2f}] p={r['p']:.3f} h={r['h']:.2f} n={r['n']}"


per = R.per
data = {b: R.load(b) for b in ("road", "reserve")}

# ------------------------------------------------------------------ T1
print("T1 reproduce")
H = {}
for b, (u, rate) in data.items():
    x, cl, w = u.x_km.values, u.seg.values, u.area_ha.values
    d = per(rate, 2019, 2021) - per(rate, 2014, 2018)
    r = rd(d, x, cl, w); H[b] = r["h"]
    print(f"  {b:8s} did 2019-21 vs 2014-18: {fmt(r)}  clusters={len(np.unique(cl[np.abs(x) <= r['h']]))} (all {len(np.unique(cl))})")
    print(f"  {b:8s} did 2022-25 vs 2014-18: {fmt(rd(per(rate, 2022, 2025) - per(rate, 2014, 2018), x, cl, w))}")

# ------------------------------------------------------------------ T2
print("\nT2a yearly gap at the road (levels, fixed h = headline h)")
u, rate = data["road"]; x, cl, w = u.x_km.values, u.seg.values, u.area_ha.values; h = H["road"]
yr = {y: rd(rate[y], x, cl, w, h=h) for y in range(2005, 2026)}
print("  " + "  ".join(f"{y}:{v['est']:+.2f}" for y, v in yr.items()))
pre_g = np.array([yr[y]["est"] for y in range(2005, 2019)])
print(f"  pre-2019 yearly gaps 2005-18: mean {pre_g.mean():+.2f}, sd {pre_g.std(ddof=1):.2f}, min {pre_g.min():+.2f}, max {pre_g.max():+.2f}")
print("T2b PRE window choice (POST 2019-21), mserd bandwidth re-chosen each time")
for b in ("road", "reserve"):
    u_, rate_ = data[b]; x_, cl_, w_ = u_.x_km.values, u_.seg.values, u_.area_ha.values
    for pre in [(2014, 2018), (2009, 2013), (2016, 2018), (2011, 2018), (2009, 2018), (2017, 2018), (2014, 2016)]:
        r = rd(per(rate_, 2019, 2021) - per(rate_, *pre), x_, cl_, w_)
        print(f"  {b:8s} pre {pre}: {fmt(r)}")

# ------------------------------------------------------------------ T3
print("\nT3 timing at the road (PRE 2014-18, mserd)")
for post in [(2019, 2019), (2020, 2020), (2021, 2021), (2020, 2021), (2019, 2021), (2022, 2022), (2023, 2023),
             (2022, 2025)]:
    r = rd(per(rate, *post) - per(rate, 2014, 2018), x, cl, w)
    rf = rd(per(rate, *post) - per(rate, 2014, 2018), x, cl, w, h=h)
    print(f"  post {post}: {fmt(r)}   | fixed h {h:.2f}: {rf['est']:+.3f} p={rf['p']:.3f}")
late_ex = rate[[2022, 2024, 2025]].mean(axis=1) - per(rate, 2014, 2018)
print(f"  post 2022,2024,2025 (no 2023): {fmt(rd(late_ex, x, cl, w))}")

# ------------------------------------------------------------------ T4
print("\nT4 fake start years (statistic = mean(s..s+2) - mean(s-5..s-1), fixed headline h)")
for b in ("road", "reserve"):
    u_, rate_ = data[b]; x_, cl_, w_ = u_.x_km.values, u_.seg.values, u_.area_ha.values; h_ = H[b]
    real = rd(per(rate_, 2019, 2021) - per(rate_, 2014, 2018), x_, cl_, w_)["est"]
    fk = pd.Series({s: rd(per(rate_, s, s + 2) - per(rate_, s - 5, s - 1), x_, cl_, w_, h=h_)["est"]
                    for s in range(1998, 2017)})
    near = np.abs(x_) <= h_
    mined = rate_.loc[near].mul(w_[near], axis=0).sum()
    first = int(mined[mined > 0].index.min())
    print(f"  {b}: first year with mining within h = {first}; real {real:+.3f}")
    print("   fakes: " + "  ".join(f"{s}:{v:+.2f}" for s, v in fk.items()))
    for lo in (first, 2007, 2008):
        f = fk.loc[max(lo, first):]
        rk = placebo_rank(-abs(real), -f.abs()); n = len(f) + 1
        rk_signed = 1 + int((f >= real).sum()) if real > 0 else 1 + int((f <= real).sum())
        print(f"   pool from {max(lo, first)}: two-sided rank {rk} of {n} (p={rk / n:.2f}); one-sided rank {rk_signed}; "
              f"largest |fake| {f.abs().max():.3f} in {f.abs().idxmax()}; real/largest = {abs(real) / f.abs().max():.3f}")

# ------------------------------------------------------------------ T5 / T6 rebuild from the zone raster
print("\nT5 running variable: rebuild the road units with (a) the coded latitude offset, (b) perpendicular distance")


def rebuild():
    import rasterio, geopandas as gpd, shapely
    from rasterio.windows import from_bounds
    from shapely.ops import unary_union
    from pyproj import Transformer
    r = rasterio.open(rz.OUT_FULL)
    wnd = from_bounds(*rz.STUDY, r.transform).round_offsets().round_lengths()
    z = r.read(1, window=wnd); first = r.read(2, window=wnd); t = r.window_transform(wnd)
    lat = t.f + (np.arange(z.shape[0]) + 0.5) * t.e
    lon = t.c + (np.arange(z.shape[1]) + 0.5) * t.a
    dy = abs(t.e) * 110574
    pix_ha = np.broadcast_to(((abs(t.a) * 111320 * np.cos(np.radians(lat))) * dy / 1e4)[:, None], z.shape)
    roads = gpd.read_file(rz.RAW / "raisg/vias_nacionales_mdd_box.geojson")
    ioh = roads[roads.sigla == "PE-30C"].to_crs(4326)
    d_lat = rz.signed_road_km(t, z.shape, ioh, rz.LP_LON)
    seg = ((lon - rz.LP_LON[0]) * 111320 * np.cos(np.radians(lat.mean())) / 1000 // R.SEG_KM).astype(int)
    seg = np.broadcast_to(seg[None, :], z.shape)
    # perpendicular distance in UTM 19S for every pixel with a latitude offset (restricted to |offset| <= 15 km)
    cand = ~np.isnan(d_lat) & (np.abs(d_lat) <= 15) & np.isin(z, (5, 7))
    rr, cc = np.nonzero(cand)
    tr = Transformer.from_crs(4326, 32719, always_xy=True)
    X, Y = tr.transform(lon[cc], lat[rr])
    from scipy.spatial import cKDTree
    from shapely.geometry import box
    line = unary_union(ioh.geometry).intersection(box(rz.LP_LON[0] - 0.3, -13.6, rz.LP_LON[1] + 0.3, -12.1))
    line = shapely.ops.transform(lambda a, b, c=None: tr.transform(a, b), line)
    # densify the road to 10-m spacing and take the nearest vertex (error < 5 m; shapely.distance is too slow here)
    pts = np.vstack([np.array([g.interpolate(s_).coords[0] for s_ in np.arange(0, g.length, 10.0)])
                     for g in getattr(line, "geoms", [line])])
    dist = cKDTree(pts).query(np.c_[X, Y])[0] / 1000
    d_perp = np.full(z.shape, np.nan, np.float32)
    d_perp[rr, cc] = np.sign(d_lat[rr, cc]) * dist + (d_lat[rr, cc] == 0) * dist
    out = {}
    for name, d in (("lat", d_lat), ("perp", d_perp)):
        m = ~np.isnan(d) & (np.abs(d) <= R.MAX_KM) & (((d < 0) & (z == 7)) | ((d >= 0) & (z == 5)))
        b_ = np.floor(d[m] / R.BIN_KM).astype(int)
        key = seg[m].astype(np.int64) * 1000 + (b_ + 500)
        codes, uniq = pd.factorize(key)
        a = np.bincount(codes, weights=pix_ha[m])
        xs = np.bincount(codes, weights=d[m] * pix_ha[m]) / a
        f = first[m]
        new = {y: np.bincount(codes, weights=pix_ha[m] * (f == y), minlength=len(uniq)) for y in range(1985, 2026)}
        uu = pd.DataFrame({"seg": uniq // 1000, "x_km": xs, "area_ha": a})
        p = pd.DataFrame(new)
        keep = uu.area_ha >= 5
        out[name] = (uu[keep].reset_index(drop=True), p[keep].reset_index(drop=True))
    ratio = (np.abs(d_lat[rr, cc]) / np.maximum(dist, 1e-6))
    ok = np.abs(d_lat[rr, cc]) <= 10
    return out, ratio[ok], np.abs(d_lat[rr, cc])[ok]


reb, ratio, absd = rebuild()
print(f"  latitude offset / perpendicular distance (pixels within 10 km): median {np.median(ratio):.3f}, "
      f"p90 {np.quantile(ratio, .9):.3f}, max {ratio.max():.2f}; within 1 km of the road: median "
      f"{np.median(ratio[absd <= 1]):.3f}, p90 {np.quantile(ratio[absd <= 1], .9):.3f}")
for name, (uu, p) in reb.items():
    rt = p.loc[:, 1986:2025].div(uu.area_ha, axis=0) * 100
    xx, cc_, ww = uu.x_km.values, uu.seg.values, uu.area_ha.values
    print(f"  [{name}] units {len(uu)}  did 2019-21: {fmt(rd(per(rt, 2019, 2021) - per(rt, 2014, 2018), xx, cc_, ww))}")
    print(f"  [{name}]          did 2022-25: {fmt(rd(per(rt, 2022, 2025) - per(rt, 2014, 2018), xx, cc_, ww))}")
    print(f"  [{name}]          2019 only  : {fmt(rd(rt[2019] - per(rt, 2014, 2018), xx, cc_, ww))}")
    print(f"  [{name}]          2020-21    : {fmt(rd(per(rt, 2020, 2021) - per(rt, 2014, 2018), xx, cc_, ww))}")
    print(f"  [{name}]          donut 0.5  : {fmt(rd((per(rt, 2019, 2021) - per(rt, 2014, 2018))[np.abs(xx) >= .5], xx[np.abs(xx) >= .5], cc_[np.abs(xx) >= .5], ww[np.abs(xx) >= .5]))}")
    hh = rd(per(rt, 2019, 2021) - per(rt, 2014, 2018), xx, cc_, ww)["h"]
    fk = pd.Series({s: rd(per(rt, s, s + 2) - per(rt, s - 5, s - 1), xx, cc_, ww, h=hh)["est"] for s in range(2008, 2017)})
    real = rd(per(rt, 2019, 2021) - per(rt, 2014, 2018), xx, cc_, ww)["est"]
    print(f"  [{name}]          fake starts 2008-16 two-sided rank {placebo_rank(-abs(real), -fk.abs())} of {len(fk) + 1}; "
          f"largest |fake| {fk.abs().max():.2f} ({fk.abs().idxmax()})")

print("\nT6 depletion and geology across the road (coded latitude offset)")
uu, p = reb["lat"]
xx, cc_, ww = uu.x_km.values, uu.seg.values, uu.area_ha.values
check = (p.loc[:, 1986:2025].sum().sum(), data["road"][1].mul(data["road"][0].area_ha, axis=0).sum().sum() / 100)
print(f"  rebuild check: first-time ha 1986-2025 rebuilt {check[0]:.1f} vs committed {check[1]:.1f}")
cum = p.cumsum(axis=1)
for hh in (H["road"], 1.0, 5.0):
    for side, msk in (("south", (xx < 0) & (xx >= -hh)), ("north", (xx >= 0) & (xx <= hh))):
        print(f"  within {hh:.2f} km, {side}: share of land first-mined by 2018 {cum.loc[msk, 2018].sum() / ww[msk].sum():.3f}, "
              f"by 2013 {cum.loc[msk, 2013].sum() / ww[msk].sum():.3f}")
at_risk = (uu.area_ha.values[:, None] - cum.shift(1, axis=1).fillna(0).values)
ar = pd.DataFrame(p.values / np.maximum(at_risk, 1e-9) * 100, columns=p.columns).clip(upper=100)
print(f"  at-risk denominator did 2019-21: {fmt(rd(per(ar, 2019, 2021) - per(ar, 2014, 2018), xx, cc_, ww))}")
print(f"  at-risk denominator did 2022-25: {fmt(rd(per(ar, 2022, 2025) - per(ar, 2014, 2018), xx, cc_, ww))}")
ca = pd.read_csv(ROOT / "data_intermediate/cell_attr_v2.csv").merge(pd.read_csv(ROOT / "data_intermediate/cell_gold_v2.csv"), on="cell")
nr = ca[(ca.lon.between(*rz.LP_LON)) & ca.zone.isin([5, 7])]
print(f"  road_km in cell_attr: min {ca.road_km.min():.1f} (unsigned if >= 0)")
nr6 = nr[nr.road_km.abs() <= 6]
print(f"  cells zone 5/7 in LP_LON within 6 km: {len(nr6)}; gold_share unique {sorted(nr6.gold_share.round(3).unique())[:8]}; "
      f"by zone mean gold_depleted_2018 {nr6.groupby('zone').gold_depleted_2018.mean().round(3).to_dict()}")

# ------------------------------------------------------------------ T7
print("\nT7 inference and bandwidth (road, PRE 2014-18, POST 2019-21)")
d = per(rate, 2019, 2021) - per(rate, 2014, 2018)
for lab, cl2, vce in (("CR1 2-km", cl, "hc1"), ("CR3 2-km", cl, "cr3"), ("CR2 2-km", cl, "cr2"),
                      ("CR1 4-km", cl // 2, "hc1"), ("CR1 6-km", cl // 3, "hc1"), ("CR3 4-km", cl // 2, "cr3")):
    r = rd(d, x, cl2, w, vce=vce)
    print(f"  {lab}: {fmt(r)} clusters {len(np.unique(cl2))}")
for hh in (1.0, 1.5, 2.0, 2.45, 3.0, 4.0, 5.0):
    print(f"  fixed h {hh}: {fmt(rd(d, x, cl, w, h=hh))}")
for dn in (0.25, 0.5, 0.75):
    k = np.abs(x) >= dn
    print(f"  donut {dn} km, fixed h {h:.2f}: {fmt(rd(d[k], x[k], cl[k], w[k], h=h))};  own mserd h: {fmt(rd(d[k], x[k], cl[k], w[k]))}")
print("  unweighted (no area weights):", fmt(rd(d, x, cl, np.ones_like(w))))

# ------------------------------------------------------------------ T8
print("\nT8 reserve edge")
u2, rate2 = data["reserve"]; x2 = u2.x_km.values
ha = rate2.mul(u2.area_ha, axis=0) / 100
ins = ha[x2 > 0]
byy = ins.loc[:, 2000:2025].sum()
print("  first-time ha inside the reserve (reserve units), by year: " + "  ".join(f"{y}:{v:.0f}" for y, v in byy.items() if v > 0.5))
print(f"  2017 share of 2000-25 inside: {byy[2017] / byy.sum():.3f} ({byy[2017]:.0f} of {byy.sum():.0f} ha)")
tot = ins.loc[:, 2000:2025].sum(axis=1); tot_ex = ins.loc[:, 2000:2025].drop(columns=2017).sum(axis=1)
xi = x2[x2 > 0]
print(f"  share within 1 km: all {tot[xi <= 1].sum() / tot.sum():.3f}; excl. 2017 {tot_ex[xi <= 1].sum() / tot_ex.sum():.3f}")
out_side = ha[x2 < 0].loc[:, 2000:2025].sum()
print(f"  outside (buffer-zone) side first-time ha 2014-18 / 2019-21 per yr: {out_side.loc[2014:2018].mean():.0f} / {out_side.loc[2019:2021].mean():.0f}")
cy = pd.read_csv(ROOT / "data_intermediate/cell_year_v2.csv.gz")
cyy = cy[cy.year.between(2000, 2025)].groupby("cell").new_land_ha.sum()
c1 = ca[ca.zone == 1].assign(new=lambda q: q.cell.map(cyy).fillna(0))
print(f"  reserve-majority cells: first-time ha 2000-25 {c1.new.sum():.0f}; share in cells with river_km <= 1: "
      f"{c1.loc[c1.river_km <= 1, 'new'].sum() / c1.new.sum():.3f} (cells with river_km<=1: {(c1.river_km <= 1).mean():.2f} of reserve cells)")

# ------------------------------------------------------------------ T9
print("\nT9 A9 road fake-date test: north share of first-time mined land, La Pampa longitudes")
b = pd.read_csv(rz.OUT_BAND)
wb = b.pivot_table(index="year", columns="km_from_road", values="new_land_ha", aggfunc="sum").fillna(0)
for lab, cols in (("+-30 km (as coded)", list(wb.columns)), ("+-15 km (as documented)", [c for c in wb if -15 <= c <= 14]),
                  ("+-5 km", [c for c in wb if -5 <= c <= 4]), ("+-2 km", [c for c in wb if -2 <= c <= 1])):
    ww_ = wb[cols]
    share = (ww_[[c for c in cols if c >= 0]].sum(axis=1) / ww_.sum(axis=1)).loc[2005:2025]
    s, rank, n = v2_tests.shift_test(share)
    clean = s[(s.index <= 2013) | (s.index >= 2022) | (s.index == 2019)]
    strict = s[(s.index <= 2013) | (s.index == 2019)]
    rc = int(clean.rank(ascending=False)[2019]); rs = int(strict.rank(ascending=False)[2019])
    two = int(clean.abs().rank(ascending=False)[2019])
    print(f"  {lab}: share 2016-18 {share.loc[2016:2018].mean():.3f} -> 2019-21 {share.loc[2019:2021].mean():.3f}; "
          f"shift 2019 {s[2019]:+.3f}; clean(<=2013,2022,2019) rank {rc} of {len(clean)}; "
          f"strict(<=2013,2019) rank {rs} of {len(strict)}; two-sided clean rank {two} of {len(clean)}")
    print("     shifts: " + "  ".join(f"{k}:{v:+.2f}" for k, v in s.items()))
