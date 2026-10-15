"""Spatial regression discontinuity at two borders: the road and the reserve border. DESCRIPTION (plan v3).

DESIGN (difference in discontinuities, Grembi, Nannicini & Troiano 2016): a border splits land into two legal regimes.
A plain spatial RD compares land just on either side, but at a road the border also changes access, and at the reserve
border the Malinowski River runs along it. Those stay fixed over time, so we take the CHANGE in the gap: the gap at the
border in 2019-21 minus the gap in 2014-18 (definitions.PERIODS "during" vs "pre_long"). What is left is what changed
at the border around Mercurio (and COVID, which arrived in the second year).

  Road border    La Pampa longitudes (definitions.LP_LON). South = registry zone "lapampa" (Tambopata buffer zone);
                 north = registry zone "corridor_across" (legal corridor within 10 km north of the road).
                 RUNNING VARIABLE (main) = the north-south offset to the Interoceanic Highway at the pixel's longitude,
                 km (raster_zones.signed_road_km: (pixel latitude - road latitude) x 110.574; north > 0). It is NOT the
                 perpendicular distance: where the road runs at an angle the offset overstates the distance (review
                 D-S9-3: median 8%). Sensitivity "roadperp": the true perpendicular distance, UTM 19S, road densified at
                 10 m, same sign and sides.
  Reserve border Tambopata National Reserve (zone "tambopata_nr") vs the Tambopata buffer zone (zones "lapampa" +
                 "tambopata_bz_rest", Kotsimba included since v3), inside the cell-panel window (STUDY), only stretches
                 where the land outside is the buffer zone. Running variable = Euclidean distance to the reserve edge
                 (km, inside > 0).

Unit = a 250-m distance bin within a ~2-km segment along the border (segment = cluster). OUTCOME (definitions.OUTCOME):
NET mining additions as % of the unit's area per year = new + re-mined - stopped, from our own restream of the MapBiomas
Peru Col 4 rasters with the RD units as keys (raster_zones.Accountant). Estimation: rdrobust (Calonico, Cattaneo &
Titiunik), local linear, triangular kernel, robust bias-corrected CI, errors clustered by segment (vce="hc1" with
cluster= is CR1). The headline bandwidth is MSE-optimal for NET; the three parts are then estimated at that SAME fixed
bandwidth, so their conventional estimates add up to net (asserted); their robust CIs do not add up.
Checks: 2019 alone; placebo start years (same statistic, fixed bandwidth); placebo borders; bandwidths 1/2/3/5 km and a
0.5-km donut; perpendicular distance.

READING: displacement breaks the RD's "no spillover" assumption. If miners move from south to north, the gap opens
from both sides, so the road estimate is deterrence + displacement: the size of the swing at the border, not the net
effect of Mercurio. It is a description of the border, labelled so.
"""
from __future__ import annotations
import warnings
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from common import (ROOT, OUT, style_axes, finish_figure, headline, period_band, C, INK, MUTED, AXIS, placebo_rank)
import definitions as D
import zonedata as Z
import raster_zones as rz

INTER = ROOT / "data_intermediate"
OUT_UNITS = INTER / "rdd_units.csv"               # border, unit, seg, x_km, area_ha
OUT_UY = INTER / "rdd_unit_year.csv"              # border, unit, year, mining/net/new/remined/stopped ha (non-zero)
SRC = f"{D.SOURCE}, restreamed by RD unit; SERNANP, RAISG road; rdrobust"
BIN_KM, SEG_KM, MAX_KM = 0.25, 2.0, 10.0
PRE, POST, LATE = (D.PERIODS[k] for k in ("pre_long", "during", "later"))
MEAS = ["net"] + D.PARTS
BORDERS = {"road": dict(name="the road", left="south (La Pampa)", right="north (corridor)"),
           "roadperp": dict(name="the road (perpendicular distance)", left="south (La Pampa)", right="north (corridor)"),
           "reserve": dict(name="the reserve border", left="outside (buffer zone)", right="inside (reserve)")}
UNIT = "% of land per year"


# --------------------------------------------------------------------------- build (restream the rasters by RD unit)
def _perp_km(t, shape, ioh, cand, sign):
    """Perpendicular distance (km) to the road for the pixels in `cand`, UTM 19S, road densified at 10 m."""
    import shapely
    from shapely.ops import unary_union
    from shapely.geometry import box
    from pyproj import Transformer
    from scipy.spatial import cKDTree
    rr, cc = np.nonzero(cand)
    lat = t.f + (rr + 0.5) * t.e; lon = t.c + (cc + 0.5) * t.a
    tr = Transformer.from_crs(4326, 32719, always_xy=True)
    X, Y = tr.transform(lon, lat)
    line = unary_union(ioh.geometry).intersection(box(D.LP_LON[0] - 0.3, -13.6, D.LP_LON[1] + 0.3, -12.1))
    line = shapely.ops.transform(lambda a, b, c=None: tr.transform(a, b), line)
    pts = np.vstack([np.array([g.interpolate(s_).coords[0] for s_ in np.arange(0, g.length, 10.0)])
                     for g in getattr(line, "geoms", [line])])
    out = np.full(shape, np.nan, np.float32)
    out[rr, cc] = np.where(sign[rr, cc] >= 0, 1, -1) * cKDTree(pts).query(np.c_[X, Y])[0] / 1000
    return out


def build():
    import rasterio
    from rasterio.windows import from_bounds, bounds as wbounds
    from scipy.ndimage import distance_transform_edt
    zr = rasterio.open(rz.OUT_FULL)
    w = from_bounds(*rz.STUDY, zr.transform).round_offsets().round_lengths()
    z = zr.read(1, window=w); t = zr.window_transform(w)
    lat = t.f + (np.arange(z.shape[0]) + 0.5) * t.e
    lon = t.c + (np.arange(z.shape[1]) + 0.5) * t.a
    dy = abs(t.e) * 110574; dx = abs(t.a) * 111320 * np.cos(np.radians(lat.mean()))
    pix_ha = rz.row_area(t, z.shape[0])
    rows, cols = np.mgrid[0:z.shape[0], 0:z.shape[1]]
    L = rz.layers()
    zc = D.ZONE_CODE
    south, north = z == zc["lapampa"], z == zc["corridor_across"]
    # road: latitude offset (main) and perpendicular distance (sensitivity)
    d_road = rz.signed_road_km(t, z.shape, L["ioh"], D.LP_LON)
    cand = ~np.isnan(d_road) & (np.abs(d_road) <= 15) & (south | north)
    d_perp = _perp_km(t, z.shape, L["ioh"], cand, d_road)
    seg_road = ((lon - D.LP_LON[0]) * 111320 * np.cos(np.radians(lat.mean())) / 1000 // SEG_KM).astype(int)
    seg_road = np.broadcast_to(seg_road[None, :], z.shape)
    # reserve: distance to the edge of the Tambopata NR, inside > 0; outside = Tambopata buffer zone
    tnr = z == zc["tambopata_nr"]; bz = np.isin(z, [zc[s] for s in D.UNITS["tambopata_bz"]])
    d_in = distance_transform_edt(tnr, sampling=(dy, dx)) / 1000
    d_out = distance_transform_edt(~tnr, sampling=(dy, dx)) / 1000
    d_bz = distance_transform_edt(~bz, sampling=(dy, dx)) / 1000
    d_res = np.where(tnr, d_in, -d_out)
    seg_res = (rows * dy / 1000 // SEG_KM).astype(int) * 10000 + (cols * dx / 1000 // SEG_KM).astype(int)
    designs = {
        "road": (d_road, ~np.isnan(d_road) & (np.abs(d_road) <= MAX_KM) & (((d_road < 0) & south) | ((d_road >= 0) & north)), seg_road),
        "roadperp": (d_perp, ~np.isnan(d_perp) & (np.abs(d_perp) <= MAX_KM) & (((d_perp < 0) & south) | ((d_perp >= 0) & north)), seg_road),
        "reserve": (d_res, (np.abs(d_res) <= MAX_KM) & ((tnr & (d_bz - d_in < 0.2)) | bz), seg_res),
    }
    keys, units = {}, []
    pix = np.broadcast_to(pix_ha[:, None], z.shape)
    for name, (d, m, seg) in designs.items():
        b = np.floor(d[m] / BIN_KM).astype(int)
        key = seg[m].astype(np.int64) * 1000 + (b + 500)
        codes, uniq = pd.factorize(key)
        a = np.bincount(codes, weights=pix[m])
        xs = np.bincount(codes, weights=d[m] * pix[m]) / a
        units.append(pd.DataFrame({"border": name, "unit": np.arange(len(uniq)), "seg": uniq // 1000, "x_km": xs,
                                   "area_ha": a}))
        k = np.zeros(z.shape, np.int32); k[m] = codes + 1
        keys[name] = k
    mb = rasterio.open(str(rz.RASTER).format(y=2025))
    wm = from_bounds(*wbounds(w, zr.transform), mb.transform).round_offsets().round_lengths()
    assert np.allclose(tuple(mb.window_transform(wm))[:6], tuple(t)[:6], atol=1e-9), "grids differ"
    acc = rz.Accountant(keys, pix_ha)
    acc.run(lambda y: rasterio.open(str(rz.RASTER).format(y=y)).read(1, window=wm))
    uy = []
    for name in designs:
        n = int(keys[name].max())
        tb = acc.tidy(name, {i + 1: dict(unit=i) for i in range(n)})
        rz.check_identity(tb, ["unit"])
        tb = tb[(tb[["mining_ha", "new_ha", "remined_ha", "stopped_ha"]].abs().sum(axis=1) > 0)]
        uy.append(tb[["unit", "year", "mining_ha", "net_ha", "new_ha", "remined_ha", "stopped_ha"]].assign(border=name))
    pd.concat(units).round(5).to_csv(OUT_UNITS, index=False)
    pd.concat(uy).round(5).to_csv(OUT_UY, index=False)
    print(f"Saved {OUT_UNITS.relative_to(ROOT)}, {OUT_UY.relative_to(ROOT)}")


def load(border):
    u = pd.read_csv(OUT_UNITS); u = u[(u.border == border) & (u.area_ha >= 5)].set_index("unit")
    uy = pd.read_csv(OUT_UY); uy = uy[uy.border == border]
    rates = {}
    for m in MEAS:
        p = uy.pivot_table(index="unit", columns="year", values=D.COLS[m], aggfunc="sum")
        p = p.reindex(index=u.index, columns=range(1986, 2026)).fillna(0)
        rates[m] = p.div(u.area_ha, axis=0) * 100          # % of the unit's land per year
    return u, rates


# --------------------------------------------------------------------------- estimation
def rd(y, x, cl, w, h=None, c=0.0):
    """Local linear RD (triangular kernel). est = conventional estimate (linear in y for a given h); CI and p robust
    bias-corrected."""
    from rdrobust import rdrobust
    import io, contextlib
    with warnings.catch_warnings(), contextlib.redirect_stdout(io.StringIO()):
        warnings.simplefilter("ignore")
        r = rdrobust(y=np.asarray(y, float), x=np.asarray(x, float), c=c, h=h, cluster=np.asarray(cl),
                     weights=np.asarray(w, float), vce="hc1")       # hc1 + cluster = CR1 cluster-robust
    return dict(est=float(r.coef.iloc[0, 0]), ci_lo=float(r.ci.iloc[2, 0]), ci_hi=float(r.ci.iloc[2, 1]),
                p=float(r.pv.iloc[2, 0]), h=float(r.bws.iloc[0, 0]), n_l=int(r.N_h[0]), n_r=int(r.N_h[1]))


def per(rate, y0, y1):
    return rate.loc[:, y0:y1].mean(axis=1)


def parts_at(rates, x, cl, w, h, post, pre=PRE):
    """Net and its three parts at ONE fixed bandwidth h; the conventional estimates add up (asserted)."""
    out = {m: rd(per(rates[m], *post) - per(rates[m], *pre), x, cl, w, h=h) for m in MEAS}
    s = out["new"]["est"] + out["remined"]["est"] - out["stopped"]["est"]
    assert abs(out["net"]["est"] - s) < 1e-3, f"RD parts do not add up: {out['net']['est']} vs {s}"
    return out


def analyse(border, reg):
    u, rates = load(border)
    rate = rates["net"]
    x, cl, w = u.x_km.values, u.seg.values, u.area_ha.values
    pre, post, late = per(rate, *PRE), per(rate, *POST), per(rate, *LATE)
    lab = BORDERS[border]["name"]; side = f"{BORDERS[border]['right']} minus {BORDERS[border]['left']}"
    zone = {"road": "road border, La Pampa longitudes (lapampa | corridor_across)",
            "roadperp": "road border, La Pampa longitudes, perpendicular distance",
            "reserve": "Tambopata reserve edge (tambopata_nr | Tambopata buffer zone)"}[border]
    S = SRC

    def add(id_, v, unit, desc, measure="net", period=""):
        reg.add(f"rd_{border}_{id_}", v, unit, desc, "description", S, measure=measure, zone=zone, period=period)

    out = {"did": rd(post - pre, x, cl, w)}
    h = out["did"]["h"]
    parts = parts_at(rates, x, cl, w, h, POST)
    assert abs(parts["net"]["est"] - out["did"]["est"]) < 1e-9
    one = parts_at(rates, x, cl, w, h, (D.FIRST_POST, D.FIRST_POST))          # 2019 alone (review D-S9-2)
    Z.register_parts(reg, f"rd_{border}_did", {m: parts[m]["est"] for m in MEAS}, zone, "2019–21 vs 2014–18",
                     f"difference in discontinuities at {lab} ({side}), bandwidth {h:.2f} km (MSE-optimal for net; parts "
                     "at the same bandwidth)", source=S, value_unit=UNIT)
    Z.register_parts(reg, f"rd_{border}_did2019", {m: one[m]["est"] for m in MEAS}, zone, "2019 vs 2014–18",
                     f"difference in discontinuities at {lab}, 2019 alone, bandwidth {h:.2f} km", source=S, value_unit=UNIT)
    add("did_net_p", out["did"]["p"], "p-value", f"Robust bias-corrected p-value (CR1 by 2-km segment, MSE-optimal h "
        f"and bias bandwidth) of rd_{border}_did_net", "net", "2019–21 vs 2014–18")
    for m in MEAS:
        add(f"did_{m}_p_fixedh", parts[m]["p"], "p-value", f"Robust p-value of rd_{border}_did_{m} at the fixed "
            f"bandwidth h = b = {h:.2f} km (the run in which the parts add up)", m, "2019–21 vs 2014–18")
        add(f"did2019_{m}_p", one[m]["p"], "p-value", f"Robust p-value of rd_{border}_did2019_{m}", m, "2019 vs 2014–18")
    add("did_net_lo", out["did"]["ci_lo"], UNIT, "95% robust CI low, net, 2019–21 vs 2014–18", period="2019–21 vs 2014–18")
    add("did_net_hi", out["did"]["ci_hi"], UNIT, "95% robust CI high, net, 2019–21 vs 2014–18", period="2019–21 vs 2014–18")
    add("did_h", h, "km", "MSE-optimal bandwidth for net, 2019–21 vs 2014–18 (parts use it too)")
    add("did_n", out["did"]["n_l"] + out["did"]["n_r"], "count", "Units (250-m bins x 2-km segments) inside the bandwidth")
    fake = None
    if border == "roadperp":
        npre, npost = PRE[1] - PRE[0] + 1, POST[1] - POST[0] + 1
        fake = pd.Series({s_: rd(per(rate, s_, s_ + npost - 1) - per(rate, s_ - npre, s_ - 1), x, cl, w, h=h)["est"]
                          for s_ in range(2008, PRE[1] - npost + 2)})
        rank = placebo_rank(-abs(out["did"]["est"]), -fake.abs())
        add("fake_rank", rank, "rank", f"Two-sided rank of the real change among fake start years "
            f"{fake.index.min()}-{fake.index.max()} plus 2019 (net, perpendicular distance)")
        add("fake_n", len(fake) + 1, "count", "Start years in that comparison")
        return dict(u=u, rates=rates, out=out, parts=parts, h=h)
    out["level_pre"], out["level_post"], out["level_late"] = rd(pre, x, cl, w), rd(post, x, cl, w), rd(late, x, cl, w)
    out["did_late"] = rd(late - pre, x, cl, w)
    late_parts = parts_at(rates, x, cl, w, out["did_late"]["h"], LATE)
    Z.register_parts(reg, f"rd_{border}_didlater", {m: late_parts[m]["est"] for m in MEAS}, zone, "2022–25 vs 2014–18",
                     f"difference in discontinuities at {lab}, later years, bandwidth {out['did_late']['h']:.2f} km",
                     source=S, value_unit=UNIT)
    add("didlater_net_p", out["did_late"]["p"], "p-value", "Robust p-value of the later-years change (net)",
        period="2022–25 vs 2014–18")
    ex = [y for y in range(LATE[0], LATE[1] + 1) if y != D.LATER_EX]
    ex_r = rd(rate[ex].mean(axis=1) - pre, x, cl, w, h=out["did_late"]["h"])
    add("didlater_ex2023_net", ex_r["est"], UNIT, "Change in the gap, later years without 2023 (2022, 2024, 2025) vs "
        "2014–18, same bandwidth", period="2022, 2024, 2025 vs 2014–18")
    for k, nm in (("level_pre", "2014–18"), ("level_post", "2019–21"), ("level_late", "2022–25")):
        add(f"{k}_net", out[k]["est"], UNIT, f"Gap at {lab} ({side}), net additions, {nm}, local linear RD", period=nm)
        add(f"{k}_net_p", out[k]["p"], "p-value", f"Robust bias-corrected p-value, {nm}", period=nm)
    sens = {f"h{int(hh)}": rd(post - pre, x, cl, w, h=hh) for hh in (1.0, 2.0, 3.0, 5.0)}
    don = np.abs(x) >= 0.5
    sens["donut"] = rd((post - pre)[don], x[don], cl[don], w[don], h=h)
    for k, r_ in sens.items():
        add(f"sens_{k}_net", r_["est"], UNIT, f"Diff-in-disc 2019–21 vs 2014–18 (net), sensitivity {k}",
            period="2019–21 vs 2014–18")
        add(f"sens_{k}_net_p", r_["p"], "p-value", f"Robust p-value, sensitivity {k}", period="2019–21 vs 2014–18")
    sp = [v["p"] for v in sens.values()]
    add("sens_p_min", min(sp), "p-value", "Smallest robust p-value across bandwidths 1, 2, 3, 5 km and a 0.5-km donut "
        "(net)", period="2019–21 vs 2014–18")
    add("sens_p_max", max(sp), "p-value", "Largest robust p-value across the same runs (net)", period="2019–21 vs 2014–18")
    # placebo start years: same statistic (3 years from the start minus the 5 before), fixed h; windows end by 2018
    npre, npost = PRE[1] - PRE[0] + 1, POST[1] - POST[0] + 1
    near_h = np.abs(x) <= h
    mined = rates["new"].loc[near_h].mul(w[near_h], axis=0).sum()
    first_yr = max(int(mined[mined > 0].index.min()), 1986 + npre)
    fake = pd.Series({s_: rd(per(rate, s_, s_ + npost - 1) - per(rate, s_ - npre, s_ - 1), x, cl, w, h=h)["est"]
                      for s_ in range(first_yr, PRE[1] - npost + 2)})
    real = out["did"]["est"]
    rank = placebo_rank(-abs(real), -fake.abs()); n = len(fake) + 1
    fk = (f"same statistic as rd_{border}_did_net (3 years from the start minus the 5 before, bandwidth {h:.2f} km), "
          f"fake start years {fake.index.min()}-{fake.index.max()} (windows end by 2018), plus the real 2019")
    add("fake_rank", rank, "rank", f"Rank of the real change in the gap (absolute size; 1 = largest) among the {fk}")
    add("fake_n", n, "count", f"Start years in the placebo comparison: {fk}")
    add("fake_p", rank / n, "p-value", f"Randomization p-value = rank / n, two-sided, {fk}")
    add("fake_max_abs", fake.abs().max(), UNIT, f"Largest placebo change in the gap (absolute), {fk}")
    add("fake_first_year", fake.index.min(), "year", "First fake start year in the placebo comparison")
    pb = {}
    for c in (-4.0, -3.0, -2.0, 2.0, 3.0, 4.0):
        sd = (x < 0) if c < 0 else (x >= 0)
        pb[c] = rd((post - pre)[sd], x[sd], cl[sd], w[sd], h=min(h, abs(c) - 0.25), c=c)
    add("pb_max_abs", max(abs(v["est"]) for v in pb.values()), UNIT, "Largest estimate at a fake border inside one side "
        "(net)", period="2019–21 vs 2014–18")
    add("pb_n_sig", sum(v["p"] < 0.05 for v in pb.values()), "count", "Fake borders with p < 0.05 (of 6)")
    yearly = {yy: rd(rate[yy], x, cl, w, h=h) for yy in range(2008, 2026)}
    near = np.abs(x) <= h

    def side_mean(s, right):
        m = near & ((x >= 0) if right else (x < 0))
        return float(np.average(s[m], weights=w[m]))
    for m in ("net", "new"):
        for p, (a, b) in (("pre", PRE), ("post", POST), ("late", LATE)):
            s = per(rates[m], a, b)
            for sd, r in (("l", False), ("r", True)):
                add(f"mean_{p}_{sd}_{m}", side_mean(s, r), UNIT, f"Mean {D.MEASURE_NAME[m].lower()} within the bandwidth, "
                    f"{a}–{str(b)[2:]}, {BORDERS[border]['left' if sd == 'l' else 'right']}", m, f"{a}–{str(b)[2:]}")
    if border == "reserve":           # how deep do miners go inside? new land inside, by depth, 2000-25
        ha = rates["new"].loc[:, 2000:2025].mul(u.area_ha, axis=0).sum(axis=1) / 100
        inside = ha[x > 0]
        for km in (1, 2):
            reg.add(f"rd_reserve_inside_share_{km}km", inside[x[x > 0] <= km].sum() / inside.sum(), "share",
                    f"Share of new land (first-time mining) inside the reserve (border stretches next to the buffer "
                    f"zone, 2000-25) within {km} km of the edge", "description", SRC, measure="new",
                    zone="tambopata_nr", period="2000-2025")
    return dict(u=u, rates=rates, out=out, parts=parts, one=one, sens=sens, fake=fake, pb=pb, yearly=yearly, h=h)


# --------------------------------------------------------------------------- figure
def binned(rate_s, u, nbins_km=0.5):
    d = pd.DataFrame({"x": u.x_km, "y": rate_s, "w": u.area_ha})
    d["b"] = (np.floor(d.x / nbins_km) + 0.5) * nbins_km
    return d.groupby("b").apply(lambda q: pd.Series({"y": np.average(q.y, weights=q.w)}), include_groups=False).y


def local_fit(rate_s, u, h, side):
    x, y, w = u.x_km.values, np.asarray(rate_s), u.area_ha.values
    m = (x >= 0) if side == "r" else (x < 0)
    m &= np.abs(x) <= h
    k = w[m] * np.clip(1 - np.abs(x[m]) / h, 0, None)
    A = np.c_[np.ones(m.sum()), x[m]]
    beta = np.linalg.lstsq(A * np.sqrt(k)[:, None], y[m] * np.sqrt(k), rcond=None)[0]
    xs = np.linspace(0, h, 20) * (1 if side == "r" else -1)
    return xs, beta[0] + beta[1] * xs


def figure(res):
    fig, axs = plt.subplots(2, 2, figsize=(11, 8.4), gridspec_kw=dict(width_ratios=[1.05, 1], hspace=0.5, wspace=0.22))
    road, resv = res["road"], res["reserve"]
    rdid, rp = road["out"]["did"]["est"], road["out"]["did"]["p"]
    sdid, sp_ = resv["out"]["did"]["est"], resv["out"]["did"]["p"]
    f = lambda v: f"{v:+.1f}".replace("-", "−")
    headline(fig, f"Road: the gap rose {f(rdid)} pts in 2019–21 (p = {rp:.2f}). Reserve edge: no measurable change "
                  f"({f(sdid)}, p = {sp_:.2f})",
             "Net mining additions (new + re-mined − stopped), % of land per year, by distance from each border (left), "
             "and the gap at the border each year (right). Dashed = 2014–18, solid = 2019–21")
    cols = {"road": (C["lapampa"], C["corridor"]), "reserve": (C["lapampa"], C["reserve"])}
    lims = {"road": 6, "reserve": 4}
    for row, (bn, r_) in enumerate((("road", road), ("reserve", resv))):
        ax = axs[row, 0]; style_axes(ax, fmt=False)
        cl, cr = cols[bn]; lim = lims[bn]; u = r_["u"]; h = r_["h"]
        for (y0, y1), alpha, lw, ls in ((PRE, 0.45, 1.6, (0, (3, 2))), (POST, 1.0, 2.2, "-")):
            s = per(r_["rates"]["net"], y0, y1)
            b = binned(s, u)
            b = b[(b.index > -lim) & (b.index < lim)]
            for sd, col in (("l", cl), ("r", cr)):
                bb = b[b.index < 0] if sd == "l" else b[b.index >= 0]
                ax.scatter(bb.index, bb.values, s=16 if alpha == 1 else 12, color=col, alpha=alpha, lw=0, zorder=3)
                xs, ys = local_fit(s, u, min(h, lim), sd)
                ax.plot(xs, ys, color=col, alpha=max(alpha, 0.85), lw=lw, ls=ls, zorder=4)
        ax.axvline(0, color=INK, lw=1); ax.axhline(0, color=AXIS, lw=0.8)
        ax.set_xlim(-lim, lim + 1.3)
        ax.set_xlabel(f"km from {BORDERS[bn]['name']}   ← {BORDERS[bn]['left']}  ·  {BORDERS[bn]['right']} →")
        ax.set_ylabel("Net additions, % of land / yr")
        ax.set_title("A  The road: La Pampa's side vs the corridor's side" if bn == "road" else
                     "C  The reserve edge: inside vs the buffer zone outside", fontsize=10)
        ax = axs[row, 1]; style_axes(ax, fmt=False)
        yy = r_["yearly"]
        xs = np.array(list(yy)); est = np.array([v["est"] for v in yy.values()])
        lo = np.array([v["ci_lo"] for v in yy.values()]); hi = np.array([v["ci_hi"] for v in yy.values()])
        period_band(ax, POST[0] - 0.5, POST[1] + 0.5, "2019–21")
        ax.axhline(0, color=AXIS, lw=0.9)
        ax.vlines(xs, lo, hi, color=MUTED, lw=1.1, zorder=2)
        ax.scatter(xs, est, s=22, color=cr, zorder=3, lw=0)
        ax.set_xlim(2007.3, 2025.7); ax.set_xticks(range(2009, 2026, 4))
        ax.set_ylabel(f"gap at the border\n({'north − south' if bn == 'road' else 'inside − outside'}), % of land / yr")
        d_, p_ = r_["out"]["did"]["est"], r_["out"]["did"]["p"]
        ax.set_title(("B  " if bn == "road" else "D  ") + f"Change in the gap, 2019–21 vs 2014–18: {f(d_)} pts (p = {p_:.2f})",
                     fontsize=10)
    finish_figure(fig, f"{SRC}. Units: 250-m bins in 2-km segments along each border; local linear fits, triangular kernel, "
                       f"bandwidth MSE-optimal for net (road {road['h']:.1f} km, reserve {resv['h']:.1f} km); 95% robust "
                       "bias-corrected intervals, CR1 errors clustered by segment. Road: La Pampa longitudes, north-south "
                       "offset to the road. Description: displacement opens the road gap from both sides, so it measures "
                       "the swing, not the net effect.", OUT / "fig_v2_rdd.png")


def run(reg):
    if not (OUT_UNITS.exists() and OUT_UY.exists()):
        if not (rz.OUT_FULL.exists() and (rz.RAW / "raisg/vias_nacionales_mdd_box.geojson").exists()
                and (rz.RAW / "mapbiomas_peru_raster/peru_coverage-col4_2025.tif").exists()):
            warnings.warn("v2_rdd: zone raster, road layer or MapBiomas rasters missing; skipping"); return
        build()
    res = {b: analyse(b, reg) for b in BORDERS}
    figure(res)
    rows = []
    for b, r_ in res.items():
        for m, v in r_["parts"].items():
            rows.append(dict(border=b, spec=f"did_{m}_fixed_h", **v))
        if b == "roadperp":
            continue
        for m, v in r_["one"].items():
            rows.append(dict(border=b, spec=f"did2019_{m}_fixed_h", **v))
        for k, v in {**r_["out"], **{f"sens_{k}": v for k, v in r_["sens"].items()},
                     **{f"fake_border_{c:+.0f}km": v for c, v in r_["pb"].items()}}.items():
            rows.append(dict(border=b, spec=f"{k}_net", **v))
    pd.DataFrame(rows).round(4).to_csv(OUT / "table_rdd.csv", index=False)


if __name__ == "__main__":
    from common import Numbers
    reg = Numbers(); run(reg)
    for k, v in reg.rows.items():
        print(k, round(v["value"], 3))
