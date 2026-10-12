"""Plan v2, step S6: quarterly timing from UMD GLAD-L forest-loss alerts (Landsat), Madre de Dios, 2017-2026.

WHY: MapBiomas is annual. GLAD-L dates every forest-loss pixel to the day, so we can see WHEN clearing stopped in
La Pampa and started across the road, around February 2019.
Data: public bucket earthenginepartners-hansen (no key): alertDateYY tiles (uint16 day of year in year YY, 0 = none),
2017 (alert/2017), 2018-20 (GLADalert/<y>/final, Landsat Collection 1), 2021-26 (GLADalert/C2/..., Collection 2;
2026 = 'current', to the update date). Tiles 080W_20S_070W_10S and 070W_20S_060W_10S cover Madre de Dios.
Each alert pixel (0.00025 deg, ~27 m) gets the zone and the MapBiomas first-mined year of the 30 m pixel it falls in
(nearest), from data_intermediate/zones_v2_mdd_full.tif. "Mining-related" = the pixel is mapped as mining by
MapBiomas in some year 1985-2025.
Limits: alerts need forest (re-mining old scars never alerts); clouds bunch alerts in the dry season (use quarters and
same-quarter comparisons); Collection 1 -> 2 break at 2021; UMD: alerts are for timing, not area. DESCRIPTION only.
Output: data_intermediate/glad_zone_quarter_v2.csv; output/fig_v2_glad_quarterly.png.
"""
from __future__ import annotations
import datetime as dt
import glob
import warnings
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from common import ROOT, OUT, style_axes, finish_figure, headline, C, INK, INK2, MUTED, AXIS
import raster_zones as rz
from raster_layers import GROUPS

ZC = {"La Pampa sector": C["lapampa"], "Corridor across the road": C["corridor"], "Rest of mining corridor": C["corridor_rest"],
      "Native communities": C["native"]}

RAW = ROOT / "data_raw" / "glad_alerts"
OUT_CSV = ROOT / "data_intermediate" / "glad_zone_quarter_v2.csv"
TILES = ("080W_20S_070W_10S", "070W_20S_060W_10S")
SRC = "UMD GLAD-L forest-loss alerts (Landsat; C1 2017-20, C2 2021-26) x MapBiomas Peru Col 4 mining mask x zones v2"


def files():
    out = {}
    for t in TILES:
        for y in range(2017, 2027):
            yy = str(y)[2:]
            pat = [f"alert_2017_GLADalert_alertDate17_{t}.tif"] if y == 2017 else \
                  [f"GLADalert_{y}_final_alertDate{yy}_{t}.tif", f"GLADalert_C2_{y}_final_alertDate{yy}_{t}.tif",
                   f"GLADalert_C2_current_alertDate{yy}_{t}.tif"]
            hit = [RAW / p for p in pat if (RAW / p).exists()]
            if hit:
                out[(y, t)] = hit[0]
    return out


def build():
    import rasterio
    from rasterio.windows import from_bounds, Window
    with rasterio.open(rz.OUT_FULL) as r:
        zone, first, zt = r.read(1), r.read(2), r.transform
    inv = ~zt
    recs = []
    fl = files()
    for (y, t), f in sorted(fl.items()):
        with rasterio.open(f) as r:
            w = from_bounds(*rz.BBOX, r.transform).round_offsets().round_lengths()
            w = w.intersection(Window(0, 0, r.width, r.height))
            a = r.read(1, window=w); wt = r.window_transform(w)
        rr, cc = np.nonzero(a)
        doy = a[rr, cc].astype(int)
        lon = wt.c + (cc + 0.5) * wt.a; lat = wt.f + (rr + 0.5) * wt.e
        zc, zr = inv * (lon, lat)
        zr = np.floor(zr).astype(int); zc = np.floor(zc).astype(int)
        ok = (zr >= 0) & (zr < zone.shape[0]) & (zc >= 0) & (zc < zone.shape[1])
        zr, zc, doy, lat = zr[ok], zc[ok], doy[ok], lat[ok]
        z = zone[zr, zc]; mined = first[zr, zc] > 0
        keep = z > 0
        ha = (abs(wt.a) * 111320 * np.cos(np.radians(lat))) * (abs(wt.e) * 110574) / 1e4
        date = np.array([dt.date(y, 1, 1) + dt.timedelta(days=int(d) - 1) for d in doy[keep]])
        q = np.array([(d.month - 1) // 3 + 1 for d in date])
        df = pd.DataFrame({"year": [d.year for d in date], "quarter": q, "code": z[keep],
                           "mining": mined[keep], "ha": ha[keep]})
        g = df.groupby(["year", "quarter", "code", "mining"]).ha.sum().reset_index()
        g["file"] = f.name
        recs.append(g)
        print(f"  {f.name}: {keep.sum():,} alert pixels in Madre de Dios zones")
    out = pd.concat(recs).groupby(["year", "quarter", "code", "mining"]).ha.sum().reset_index()
    out.to_csv(OUT_CSV, index=False)


def run(reg):
    print("\n== v2 GLAD-L quarterly alerts ==")
    if not OUT_CSV.exists():
        if not (rz.OUT_FULL.exists() and files()):
            warnings.warn("glad_alerts: inputs missing; skipping"); return
        build()
    d = pd.read_csv(OUT_CSV)
    d["group"] = d.code.map({c: g for g, cs in GROUPS.items() for c in cs})
    m = d[d.mining].groupby(["year", "quarter", "group"]).ha.sum().unstack("group").fillna(0)
    idx = pd.MultiIndex.from_product([range(2017, 2027), range(1, 5)], names=["year", "quarter"])
    m = m.reindex(idx).fillna(0)
    last = d[["year", "quarter"]].drop_duplicates().sort_values(["year", "quarter"]).iloc[-1]
    m = m.loc[: (int(last.year), int(last.quarter))]
    m.round(1).to_csv(OUT / "v2_glad_quarterly_mining.csv")
    x = np.array([y + (q - 0.5) / 4 for y, q in m.index])
    show = ["La Pampa sector", "Corridor across the road", "Rest of mining corridor", "Native communities"]
    q_ = m["La Pampa sector"]
    pre, mid = q_.loc[pd.IndexSlice[2017:2018, :]].mean(), q_.loc[(2019, 2):(2020, 4)].mean()
    fig, axes = plt.subplots(len(show), 1, figsize=(9, 8.2), sharex=True, gridspec_kw={"hspace": 0.55})
    headline(fig, "La Pampa kept clearing forest through 2019. Across the road, clearing rose from mid-2019.",
             "Forest-loss alerts (GLAD-L) on mapped mining land, hectares per quarter. Each panel has its own scale.")
    for k, (ax, gname) in enumerate(zip(axes, show)):
        ax.bar(x, m[gname], width=0.2, color=ZC[gname], zorder=2)
        ax.axvline(2019 + 1 / 12, color=INK, lw=1.1, zorder=1)
        ax.axvline(2021, color=AXIS, ls=(0, (3, 2)), lw=0.9, zorder=1)
        ax.set_title(gname)
        ax.set_ylim(0, m[gname].max() * 1.12)
        style_axes(ax)
        if k == 0:
            ax.annotate("Mercurio, Feb 2019", xy=(2019 + 1 / 12, 1.0), xycoords=("data", "axes fraction"), xytext=(4, -2),
                        textcoords="offset points", fontsize=8, color=INK, fontweight="semibold", va="top")
            ax.annotate("data version break", xy=(2021, 1.0), xycoords=("data", "axes fraction"), xytext=(4, -2),
                        textcoords="offset points", fontsize=7.5, color=INK2, va="top")
            ax.text(1.0, 1.04, f"Mean per quarter: {pre:,.0f} ha (2017–18) vs {mid:,.0f} ha (Q2 2019–Q4 2020)",
                    transform=ax.transAxes, ha="right", va="bottom", fontsize=8, color=INK2)
    axes[-1].set_xticks(range(2017, 2027))
    axes[-1].set_xlim(2017, x.max() + 0.25)
    finish_figure(fig, f"{SRC}. Alerts bunch in the dry season (Q3) because of clouds; compare the same quarter across "
                       "years. Alerts need standing forest, so returns to old pits never appear. Description.",
                  OUT / "fig_v2_glad_quarterly.png")
    ann = m.groupby(level="year").sum()
    for gname in show:
        key = "".join(ch for ch in gname.lower() if ch.isalnum())[:18]
        for y in range(2017, 2026):
            reg.add(f"glad_mining_{key}_{y}", ann.loc[y, gname], "ha", f"GLAD-L forest-loss alerts on mapped mining land, {gname}, {y}", "description", SRC)
    q = m["La Pampa sector"]
    reg.add("glad_lapampa_q1_2017_2019_mean", q.loc[pd.IndexSlice[2017:2018, :]].mean(), "ha/quarter",
            "La Pampa sector, mining-related GLAD-L alerts per quarter, 2017-2018 mean", "description", SRC)
    reg.add("glad_lapampa_2019q2_2020q4_mean", q.loc[(2019, 2):(2020, 4)].mean(), "ha/quarter",
            "La Pampa sector, mining-related GLAD-L alerts per quarter, 2019Q2-2020Q4 mean", "description", SRC)
    s2_check(reg)
    print(ann.round(0).to_string())


def s2_check(reg):
    """Sentinel-2 alerts (GLAD-S2, 10 m, ~5-day revisit) in the western La Pampa sector (70.15-70.00 W; the only part
    inside the downloaded tile): monthly hectares in 2019, to test whether 2019 Landsat alerts are just cloud delay."""
    import rasterio
    from rasterio.windows import from_bounds
    f = RAW / "S2alert_alertDate_080W_20S_070W_10S.tif"
    if not f.exists():
        return
    with rasterio.open(f) as r:
        a = r.read(1, window=from_bounds(-70.15, -13.06, -70.0, -12.88, r.transform)); tr = r.transform
    v = a[a > 0].astype(int)
    lat = -12.97
    pix_ha = (abs(tr.a) * 111320 * np.cos(np.radians(lat))) * (abs(tr.e) * 110574) / 1e4
    d = pd.to_datetime("2018-12-31") + pd.to_timedelta(v, unit="D")
    s = pd.Series(pix_ha, index=d).resample("MS").sum()
    s19 = s.loc["2019-01":"2019-12"]
    reg.add("s2_lp_west_2019_mar_sep_ha", s19.loc["2019-03":"2019-09"].sum(), "ha", "GLAD-S2 alerts, western La Pampa sector, Mar-Sep 2019", "description", "UMD GLAD-S2 alerts")
    reg.add("s2_lp_west_2019_aug_ha", s19.loc["2019-08"].sum(), "ha", "GLAD-S2 alerts, western La Pampa sector, August 2019", "description", "UMD GLAD-S2 alerts")
    reg.add("s2_lp_west_2020_mar_sep_ha", s.loc["2020-03":"2020-09"].sum(), "ha", "GLAD-S2 alerts, western La Pampa sector, Mar-Sep 2020", "description", "UMD GLAD-S2 alerts")
