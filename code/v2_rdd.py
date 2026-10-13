"""Spatial regression discontinuity at two legal borders: the road and the reserve border. DESCRIPTION.

DESIGN (difference in discontinuities, Grembi, Nannicini & Troiano 2016): a border splits land into two legal regimes.
A plain spatial RD compares land just on either side, but at a road the border also changes access, and at the reserve
border the Malinowski River runs along it. Those stay fixed over time, so we take the CHANGE in the gap: the gap at the
border after Mercurio minus the gap before. What's left is what changed at the border in 2019.

  Road border    La Pampa longitudes (LP_LON). Running variable = signed km to the Interoceanic Highway (north > 0).
                 South = La Pampa sector (Tambopata buffer zone, the target); north = legal corridor across the road.
  Reserve border Tambopata National Reserve vs its buffer zone, inside the cell-panel window (STUDY), only stretches
                 where the land outside is the buffer zone. Running variable = signed km to the reserve edge (inside > 0).

Unit = a 250-m distance bin within a ~2-km segment along the border (segment = cluster). Outcome = land mined for the
first time, % of the unit's area per year (MapBiomas Peru Col 4, first-mined year from raster_zones). Estimation:
rdrobust (Calonico, Cattaneo & Titiunik) on the period-mean outcome (levels) and on its change (post minus pre),
local linear, triangular kernel, MSE-optimal bandwidth, robust bias-corrected CI, errors clustered by segment
(vce="hc1" with cluster= is CR1 in rdrobust).
Checks: placebo start years (the same diff-in-disc for every fake start, fixed bandwidth), placebo borders (fake
cut-offs inside one side only), bandwidth and donut sensitivity.

READING: displacement breaks the RD's "no spillover" assumption. If miners move from south to north, the gap opens
from both sides, so the road estimate is deterrence + displacement: the size of the swing at the border, not the net
effect of Mercurio. It is a description of the border, labelled so.
"""
from __future__ import annotations
import warnings
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from common import (ROOT, OUT, style_axes, finish_figure, headline, label_end, callout, period_band, C, INK, INK2,
                    MUTED, GRID, AXIS, placebo_rank)
import raster_zones as rz

INTER = ROOT / "data_intermediate"
OUT_UNITS = INTER / "rdd_units_v2.csv"            # border, unit, seg, x_km, area_ha
OUT_UY = INTER / "rdd_unit_year_v2.csv"           # border, unit, year, new_ha (non-zero rows only)
SRC = "MapBiomas Peru Col 4 rasters (first-time mined land), SERNANP, MTC/RAISG road; rdrobust"
BIN_KM, SEG_KM, MAX_KM = 0.25, 2.0, 10.0
PRE, POST, LATE = (2014, 2018), (2019, 2021), (2022, 2025)
BORDERS = {"road": dict(name="the road", left="south (La Pampa)", right="north (corridor)"),
           "reserve": dict(name="the reserve border", left="outside (buffer zone)", right="inside (reserve)")}


# --------------------------------------------------------------------------- build (from the zone raster)
def build():
    import rasterio
    from rasterio.windows import from_bounds
    from scipy.ndimage import distance_transform_edt
    r = rasterio.open(rz.OUT_FULL)
    w = from_bounds(*rz.STUDY, r.transform).round_offsets().round_lengths()
    z = r.read(1, window=w); first = r.read(2, window=w); t = r.window_transform(w)
    lat = t.f + (np.arange(z.shape[0]) + 0.5) * t.e
    lon = t.c + (np.arange(z.shape[1]) + 0.5) * t.a
    dy = abs(t.e) * 110574; dx = abs(t.a) * 111320 * np.cos(np.radians(lat.mean()))
    pix_ha = np.broadcast_to(((abs(t.a) * 111320 * np.cos(np.radians(lat))) * dy / 1e4)[:, None], z.shape)
    rows, cols = np.mgrid[0:z.shape[0], 0:z.shape[1]]
    L = rz.layers()
    # road: signed km, La Pampa longitudes, south side = La Pampa sector (7), north side = corridor across (5)
    d_road = rz.signed_road_km(t, z.shape, L["ioh"], rz.LP_LON)
    m_road = ~np.isnan(d_road) & (np.abs(d_road) <= MAX_KM) & (((d_road < 0) & (z == 7)) | ((d_road >= 0) & (z == 5)))
    seg_road = ((lon - rz.LP_LON[0]) * 111320 * np.cos(np.radians(lat.mean())) / 1000 // SEG_KM).astype(int)
    seg_road = np.broadcast_to(seg_road[None, :], z.shape)
    # reserve: signed km to the edge of the Tambopata NR (zone 1), inside > 0; outside = Tambopata buffer zone (7, 8);
    # inside pixels kept only where the nearest land outside is buffer zone (not another protected area)
    tnr, bz = z == 1, np.isin(z, (7, 8))
    d_in = distance_transform_edt(tnr, sampling=(dy, dx)) / 1000
    d_out = distance_transform_edt(~tnr, sampling=(dy, dx)) / 1000
    d_bz = distance_transform_edt(~bz, sampling=(dy, dx)) / 1000
    d_res = np.where(tnr, d_in, -d_out)
    m_res = (np.abs(d_res) <= MAX_KM) & ((tnr & (d_bz - d_in < 0.2)) | bz)
    # segment along the reserve border = the 2-km square the pixel sits in (squares are clusters)
    seg_res = (rows * dy / 1000 // SEG_KM).astype(int) * 10000 + (cols * dx / 1000 // SEG_KM).astype(int)
    units, uy = [], []
    for name, d, m, seg in (("road", d_road, m_road, seg_road), ("reserve", d_res, m_res, seg_res)):
        b = np.floor(d[m] / BIN_KM).astype(int)
        s = seg[m]
        key = s.astype(np.int64) * 1000 + (b + 500)
        codes, uniq = pd.factorize(key)
        a = np.bincount(codes, weights=pix_ha[m])
        xs = np.bincount(codes, weights=d[m] * pix_ha[m]) / a
        u = pd.DataFrame({"border": name, "unit": np.arange(len(uniq)), "seg": uniq // 1000,
                          "x_km": xs, "area_ha": a})
        f = first[m]
        for y in range(1986, 2026):
            k = f == y
            if k.any():
                v = np.bincount(codes[k], weights=pix_ha[m][k], minlength=len(uniq))
                nz = np.nonzero(v)[0]
                uy.append(pd.DataFrame({"border": name, "unit": nz, "year": y, "new_ha": v[nz]}))
        units.append(u)
    pd.concat(units).round(4).to_csv(OUT_UNITS, index=False)
    pd.concat(uy).round(4).to_csv(OUT_UY, index=False)
    print(f"Saved {OUT_UNITS.relative_to(ROOT)}, {OUT_UY.relative_to(ROOT)}")


def load(border):
    u = pd.read_csv(OUT_UNITS); u = u[(u.border == border) & (u.area_ha >= 5)].set_index("unit")
    uy = pd.read_csv(OUT_UY); uy = uy[uy.border == border]
    p = uy.pivot_table(index="unit", columns="year", values="new_ha", aggfunc="sum")
    p = p.reindex(index=u.index, columns=range(1986, 2026)).fillna(0)
    rate = p.div(u.area_ha, axis=0) * 100          # % of the unit's land mined for the first time, per year
    return u, rate


# --------------------------------------------------------------------------- estimation
def rd(y, x, cl, w, h=None, c=0.0):
    """Local linear RD (triangular kernel). Returns dict(est, ci_lo, ci_hi, p, h, n_l, n_r). Robust bias-corrected."""
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


def analyse(border, reg):
    u, rate = load(border)
    x, cl, w = u.x_km.values, u.seg.values, u.area_ha.values
    pre, post, late = per(rate, *PRE), per(rate, *POST), per(rate, *LATE)
    out = {}
    out["level_pre"] = rd(pre, x, cl, w)
    out["level_post"] = rd(post, x, cl, w)
    out["level_late"] = rd(late, x, cl, w)
    out["did"] = rd(post - pre, x, cl, w)
    out["did_late"] = rd(late - pre, x, cl, w)
    h = out["did"]["h"]
    # sensitivity: fixed bandwidths and a 0.5-km donut
    sens = {f"h{int(hh)}": rd(post - pre, x, cl, w, h=hh) for hh in (1.0, 2.0, 3.0, 5.0)}
    don = np.abs(x) >= 0.5
    sens["donut"] = rd((post - pre)[don], x[don], cl[don], w[don], h=h)
    # placebo start years (fixed after referee Q4, 13 Oct 2026): the SAME statistic as the headline (mean of 3 years
    # from the start minus mean of the 5 years before, bandwidth h; start 2019 = rd_*_did exactly), shifted to fake
    # start years. Candidates: the fake start year has first-time mining near the border (within h), and the whole
    # fake window (s-5 .. s+2) ends by 2018, so it never touches the treated years 2019-21.
    npre, npost = PRE[1] - PRE[0] + 1, POST[1] - POST[0] + 1
    near_h = np.abs(x) <= h
    mined = rate.loc[near_h].mul(w[near_h], axis=0).sum()
    first_yr = int(mined[mined > 0].index.min())
    fake = pd.Series({s_: rd(per(rate, s_, s_ + npost - 1) - per(rate, s_ - npre, s_ - 1), x, cl, w, h=h)["est"]
                      for s_ in range(first_yr, PRE[1] - npost + 2)})          # last start: s + 2 = 2018
    real = out["did"]["est"]
    rank = placebo_rank(-abs(real), -fake.abs()); n = len(fake) + 1          # two-sided: rank by absolute size
    clean = fake
    # placebo borders: fake cut-offs inside one side only (data from that side)
    pb = {}
    for c in (-4.0, -3.0, -2.0, 2.0, 3.0, 4.0):
        side = (x < 0) if c < 0 else (x >= 0)
        pb[c] = rd((post - pre)[side], x[side], cl[side], w[side], h=min(h, abs(c) - 0.25), c=c)
    # gap at the border by year (fixed bandwidth h, levels)
    yearly = {yy: rd(rate[yy], x, cl, w, h=h) for yy in range(2008, 2026)}
    # side means near the border (within h), for plain-language numbers
    near = np.abs(x) <= h
    def side_mean(s, right):
        m = near & ((x >= 0) if right else (x < 0))
        return float(np.average(s[m], weights=w[m]))
    sm = {f"{p}_{side}": side_mean(v, side == "r") for p, v in (("pre", pre), ("post", post), ("late", late))
          for side in ("l", "r")}
    lab = BORDERS[border]["name"]
    if border == "reserve":           # how deep do miners go inside? first-time mined ha inside, by depth, 2000-25
        ha = rate.loc[:, 2000:2025].mul(u.area_ha, axis=0).sum(axis=1) / 100
        inside = ha[x > 0]
        for km in (1, 2):
            reg.add(f"rd_reserve_inside_share_{km}km", inside[x[x > 0] <= km].sum() / inside.sum(), "share",
                    f"Share of first-time mined land inside the reserve (border stretches next to the buffer zone, 2000-25) within {km} km of the edge",
                    "description", SRC)
    S = SRC
    def add(id_, v, unit, desc):
        reg.add(f"rd_{border}_{id_}", v, unit, desc, "description", S)
    for k, nm in (("level_pre", "2014-18"), ("level_post", "2019-21"), ("level_late", "2022-25")):
        r_ = out[k]
        add(f"{k}", r_["est"], "% of land per year", f"Gap at {lab} ({BORDERS[border]['right']} minus {BORDERS[border]['left']}), first-time mined land, {nm}, local linear RD")
        add(f"{k}_lo", r_["ci_lo"], "% of land per year", f"95% robust CI low, {nm}")
        add(f"{k}_hi", r_["ci_hi"], "% of land per year", f"95% robust CI high, {nm}")
        add(f"{k}_p", r_["p"], "p-value", f"Robust bias-corrected p-value (CR1, clustered by 2-km segment), {nm}")
    for k, nm in (("did", "2019-21 vs 2014-18"), ("did_late", "2022-25 vs 2014-18")):
        r_ = out[k]
        add(k, r_["est"], "% of land per year", f"Difference in discontinuities at {lab}: change in the gap, {nm}")
        add(f"{k}_lo", r_["ci_lo"], "% of land per year", f"95% robust CI low, {nm}")
        add(f"{k}_hi", r_["ci_hi"], "% of land per year", f"95% robust CI high, {nm}")
        add(f"{k}_p", r_["p"], "p-value", f"Robust bias-corrected p-value (CR1 errors clustered by 2-km segment), {nm}")
        add(f"{k}_h", r_["h"], "km", f"MSE-optimal bandwidth, {nm}")
        add(f"{k}_n", r_["n_l"] + r_["n_r"], "count", f"Units (250-m bins x 2-km segments) inside the bandwidth, {nm}")
    for k, r_ in sens.items():
        add(f"sens_{k}", r_["est"], "% of land per year", f"Diff-in-disc 2019-21, sensitivity {k}")
        add(f"sens_{k}_p", r_["p"], "p-value", f"Robust bias-corrected p-value (CR1, clustered by segment), sensitivity {k}")
    fk = (f"same statistic as rd_{border}_did (3 years from the start minus the 5 before, bandwidth {h:.2f} km), "
          f"fake start years {fake.index.min()}-{fake.index.max()} (first year with first-time mining near the border "
          f"to the last whose window ends by 2018, so no fake window touches 2019-21), plus the real 2019")
    add("fake_rank", rank, "rank", f"Rank of the real change in the gap (absolute size; 1 = largest) among the {fk}")
    add("fake_n", n, "count", f"Start years in the placebo comparison (fakes + the real 2019): {fk}")
    add("fake_p", rank / n, "p-value", f"Randomization p-value = rank / n, two-sided (absolute size), {fk}")
    add("fake_max_abs", clean.abs().max(), "% of land per year", f"Largest placebo change in the gap (absolute), {fk}")
    add("fake_first_year", fake.index.min(), "year", "First fake start year in the placebo comparison (first year with first-time mining within the bandwidth)")
    sp = [v["p"] for v in sens.values()]
    add("sens_p_min", min(sp), "p-value", "Smallest robust p-value across the sensitivity runs (fixed bandwidth 1, 2, 3, 5 km and 0.5-km donut; errors clustered by segment, CR1)")
    add("sens_p_max", max(sp), "p-value", "Largest robust p-value across the same sensitivity runs (h1, h2, h3, h5, donut)")
    add("pb_max_abs", max(abs(v["est"]) for v in pb.values()), "% of land per year", "Largest estimate at a fake border inside one side")
    add("pb_n_sig", sum(v["p"] < 0.05 for v in pb.values()), "count", "Fake borders with p < 0.05 (of 6)")
    for k, v in sm.items():
        add(f"mean_{k}", v, "% of land per year", f"Mean first-time mined share within the bandwidth, {k} (l = {BORDERS[border]['left']}, r = {BORDERS[border]['right']})")
    return dict(u=u, rate=rate, out=out, sens=sens, fake=fake, clean=clean, pb=pb, yearly=yearly, h=h, sm=sm)


# --------------------------------------------------------------------------- figure
def binned(rate_s, u, nbins_km=0.5):
    d = pd.DataFrame({"x": u.x_km, "y": rate_s, "w": u.area_ha})
    d["b"] = (np.floor(d.x / nbins_km) + 0.5) * nbins_km
    g = d.groupby("b").apply(lambda q: pd.Series({"y": np.average(q.y, weights=q.w)}), include_groups=False)
    return g.y


def local_fit(rate_s, u, h, side):
    x, y, w = u.x_km.values, np.asarray(rate_s), u.area_ha.values
    m = (x >= 0) if side == "r" else (x < 0)
    m &= np.abs(x) <= h
    k = w[m] * np.clip(1 - np.abs(x[m]) / h, 0, None)
    A = np.c_[np.ones(m.sum()), x[m]]
    beta = np.linalg.lstsq(A * np.sqrt(k)[:, None], y[m] * np.sqrt(k), rcond=None)[0]
    xs = np.linspace(0, h, 20) * (1 if side == "r" else -1)
    return xs, beta[0] + beta[1] * xs


def figure(res, reg):
    fig, axs = plt.subplots(2, 2, figsize=(11, 8.4), gridspec_kw=dict(width_ratios=[1.05, 1], hspace=0.5, wspace=0.22))
    road, resv = res["road"], res["reserve"]
    g_road = reg.get("rd_road_did"); g_res = reg.get("rd_reserve_did")
    headline(fig, "After Mercurio, mining jumped across the road; at the reserve edge nothing changed",
             "Land mined for the first time (% of land per year) by distance from each border (left), and the step at "
             "the border in each year (right). Dashed = 2014–18, solid = 2019–21")
    cols = {"road": (C["lapampa"], C["corridor"]), "reserve": (C["lapampa"], C["reserve"])}
    lims = {"road": 6, "reserve": 4}
    for row, (bn, r_) in enumerate((("road", road), ("reserve", resv))):
        ax = axs[row, 0]; style_axes(ax, fmt=False)
        cl, cr = cols[bn]; lim = lims[bn]; u = r_["u"]
        h = r_["h"]
        for per_, (y0, y1), alpha, lw, ls in (("2014–18", PRE, 0.45, 1.6, (0, (3, 2))), ("2019–21", POST, 1.0, 2.2, "-")):
            s = per(r_["rate"], y0, y1)
            b = binned(s, u)
            b = b[(b.index > -lim) & (b.index < lim)]
            for side, col in (("l", cl), ("r", cr)):
                bb = b[b.index < 0] if side == "l" else b[b.index >= 0]
                ax.scatter(bb.index, bb.values, s=16 if alpha == 1 else 12, color=col, alpha=alpha, lw=0, zorder=3)
                xs, ys = local_fit(s, u, min(h, lim), side)
                ax.plot(xs, ys, color=col, alpha=max(alpha, 0.85), lw=lw, ls=ls, zorder=4)   # dashed pre fit stays legible
        ax.axvline(0, color=INK, lw=1)
        ax.set_xlim(-lim, lim + 1.3)
        ax.set_ylim(bottom=0)
        ax.set_xlabel(f"km from {BORDERS[bn]['name']}   ← {BORDERS[bn]['left']}  ·  {BORDERS[bn]['right']} →")
        ax.set_ylabel("% of land mined for the first time / yr")
        ax.set_title(("A  The road: the north side overtook the south" if bn == "road" else
                      "C  The reserve: mining spills about 1 km inside, then stops"), fontsize=10)
        # yearly gap
        ax = axs[row, 1]; style_axes(ax, fmt=False)
        yy = r_["yearly"]
        xs = np.array(list(yy)); est = np.array([v["est"] for v in yy.values()])
        lo = np.array([v["ci_lo"] for v in yy.values()]); hi = np.array([v["ci_hi"] for v in yy.values()])
        period_band(ax, 2018.5, 2021.5, "2019–21")
        ax.axhline(0, color=AXIS, lw=0.9)
        ax.vlines(xs, lo, hi, color=MUTED, lw=1.1, zorder=2)
        ax.scatter(xs, est, s=22, color=cr, zorder=3, lw=0)
        ax.set_xlim(2007.3, 2025.7)
        ax.set_xticks(range(2009, 2026, 4))
        ax.set_ylabel(f"gap at the border\n({'north − south' if bn == 'road' else 'inside − outside'}), % of land / yr")
        did = reg.get(f"rd_{bn}_did"); p = reg.get(f"rd_{bn}_did_p")
        ax.set_title(("B  " if bn == "road" else "D  ") + f"Step change, 2019–21 vs 2014–18: {did:+.1f} pts (p = {p:.2f})",
                     fontsize=10)
    finish_figure(fig, f"{SRC}. Units: 250-m bins in 2-km segments along each border; local linear fits, triangular kernel, "
                       f"bandwidth chosen by rdrobust (road {road['h']:.1f} km, reserve {resv['h']:.1f} km); 95% robust "
                       "bias-corrected intervals, CR1 errors clustered by segment. Road: La Pampa longitudes only. Description: "
                       "displacement opens the road gap from both sides, so it measures the swing, not the net effect.",
                  OUT / "fig_v2_rdd.png")


def run(reg):
    if not (OUT_UNITS.exists() and OUT_UY.exists()):
        if not rz.OUT_FULL.exists() or not (rz.RAW / "raisg/vias_nacionales_mdd_box.geojson").exists():
            warnings.warn("v2_rdd: zone raster or road layer missing; skipping"); return
        build()
    res = {b: analyse(b, reg) for b in BORDERS}
    figure(res, reg)
    rows = []
    for b, r_ in res.items():
        for k, v in {**r_["out"], **{f"sens_{k}": v for k, v in r_["sens"].items()},
                     **{f"fake_border_{c:+.0f}km": v for c, v in r_["pb"].items()}}.items():
            rows.append(dict(border=b, spec=k, **v))
    pd.DataFrame(rows).round(4).to_csv(OUT / "table_rdd.csv", index=False)


if __name__ == "__main__":
    from common import Numbers
    reg = Numbers(); run(reg)
    for k, v in reg.rows.items():
        print(k, round(v["value"], 3))
