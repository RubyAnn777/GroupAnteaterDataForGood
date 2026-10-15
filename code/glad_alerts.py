"""Plan v2, step S6: quarterly timing from UMD GLAD-L forest-loss alerts (Landsat), Madre de Dios, 2017-2026.

WHY: MapBiomas is annual. GLAD-L dates every forest-loss pixel to the day, so we can see WHEN clearing stopped in
La Pampa and started across the road, around February 2019.
Data: public bucket earthenginepartners-hansen (no key): alertDateYY tiles (uint16 day of year in year YY, 0 = none),
2017 (alert/2017), 2018-20 (GLADalert/<y>/final, Landsat Collection 1), 2021-26 (GLADalert/C2/..., Collection 2;
2026 = 'current', to the update date). Tiles 080W_20S_070W_10S and 070W_20S_060W_10S cover Madre de Dios.
Each alert pixel (0.00025 deg, ~27 m) gets the registry zone (definitions.ZONES), the Madre de Dios flag and the
MapBiomas first-mined year of the 30 m pixel that contains it (floor of the inverse transform), from
data_intermediate/zones_mdd.tif. "Mining-related" (fixed 2026-10-15, no look-ahead) = the pixel is first mapped as
mining by MapBiomas no later than the year AFTER the alert (clearing shows in GLAD before the annual map catches the
pit); an alert in 2017 on land first mined in 2024 no longer counts. The MapBiomas maps end in 2025, so alerts of
2025 count only if mined that year and alerts of 2026 only on land mined before (right-censored). Madre de Dios part only.
MEASURE: forest-loss alert area (ha), its own product. It is NOT net additions (no "stopped" state exists in alerts)
and is kept only as an independent check of TIMING; never compare its hectares with net additions.
Limits: alerts need forest (re-mining old scars never alerts); clouds bunch alerts in the dry season (use quarters and
same-quarter comparisons); Collection 1 -> 2 break at 2021; UMD: alerts are for timing, not area. DESCRIPTION only.
Output: data_intermediate/glad_zone_quarter.csv (year, quarter, zone slug, lag = first-mined year minus alert year,
clipped to -2..3, 99 = never mined, ha); output/fig_v2_glad_quarterly.png.
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
import definitions as D
from raster_layers import GROUPS, group_of

ZC = {"La Pampa sector": C["lapampa"], "Corridor across the road": C["corridor"], "Rest of mining corridor": C["corridor_rest"],
      "Native communities": C["native"]}

RAW = ROOT / "data_raw" / "glad_alerts"
INTER = ROOT / "data_intermediate"
OUT_CSV = ROOT / "data_intermediate" / "glad_zone_quarter.csv"
TILES = ("080W_20S_070W_10S", "070W_20S_060W_10S")
SRC = "UMD GLAD-L forest-loss alerts (Landsat; C1 2017-20, C2 2021-26) x MapBiomas Peru Col 4 mining mask x zone registry; mining-related = first mapped as mining by the year after the alert"


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
    from raster_layers import zone_raster
    zone, first, _, zt, mdd = zone_raster()
    inv = ~zt
    recs = []
    for (y, t), f in sorted(files().items()):
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
        z = zone[zr, zc]; fy = first[zr, zc].astype(int)
        keep = (z > 0) & mdd[zr, zc]
        ha = (abs(wt.a) * 111320 * np.cos(np.radians(lat))) * (abs(wt.e) * 110574) / 1e4
        date = pd.to_datetime(f"{y}-01-01") + pd.to_timedelta(doy[keep] - 1, unit="D")
        lag = np.where(fy[keep] > 0, np.clip(fy[keep] - date.year.values, -2, 3), 99)
        df = pd.DataFrame({"year": date.year, "quarter": date.quarter, "zone": [D.CODE_ZONE[c] for c in z[keep]],
                           "lag": lag, "ha": ha[keep]})
        recs.append(df.groupby(["year", "quarter", "zone", "lag"]).ha.sum().reset_index())
        print(f"  {f.name}: {keep.sum():,} alert pixels in Madre de Dios zones")
    out = pd.concat(recs).groupby(["year", "quarter", "zone", "lag"]).ha.sum().reset_index()
    out.to_csv(OUT_CSV, index=False)


def run(reg):
    print("\n== v2 GLAD-L quarterly alerts ==")
    if not OUT_CSV.exists():
        if not (rz.OUT_FULL.exists() and files()):
            warnings.warn("glad_alerts: inputs missing; skipping"); return
        build()
    d = pd.read_csv(OUT_CSV)
    d["group"] = d.zone.map(group_of)
    d["mining"] = d.lag <= 1                       # first mapped as mining by the year after the alert (99 = never)
    m = d[d.mining].groupby(["year", "quarter", "group"]).ha.sum().unstack("group").fillna(0)
    idx = pd.MultiIndex.from_product([range(2017, 2027), range(1, 5)], names=["year", "quarter"])
    m = m.reindex(idx).fillna(0)
    last = d[["year", "quarter"]].drop_duplicates().sort_values(["year", "quarter"]).iloc[-1]
    m = m.loc[: (int(last.year), int(last.quarter))]
    m.round(1).to_csv(OUT / "v2_glad_quarterly_mining.csv")
    x = np.array([y + (q - 0.5) / 4 for y, q in m.index])
    show = ["La Pampa sector", "Corridor across the road", "Rest of mining corridor", "Native communities"]
    q_ = m["La Pampa sector"]
    pre, mid = q_.loc[pd.IndexSlice[2017:D.REF_YEAR, :]].mean(), q_.loc[(D.FIRST_POST, 2):(2020, 4)].mean()
    fig, axes = plt.subplots(len(show), 1, figsize=(9, 8.2), sharex=True, gridspec_kw={"hspace": 0.55})
    q19 = q_.loc[pd.IndexSlice[D.FIRST_POST, :]].mean()
    headline(fig, ("La Pampa kept clearing forest through 2019" if q19 >= 0.75 * pre else "La Pampa's clearing fell in 2019")
             + f": {q19:,.0f} ha per quarter vs {pre:,.0f} in 2017–18",
             "Forest-loss alerts (GLAD-L) on land mapped as mining by the next year, ha per quarter, Madre de Dios zones, "
             "2017–2026.\nAlert area is a timing signal, not net additions. Each panel has its own scale.")
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
                       "years. Alerts need standing forest, so returns to old pits never appear. Mining-related = first mapped as mining "
                       "by the year after the alert (no look-ahead). Description.",
                  OUT / "fig_v2_glad_quarterly.png")
    ann = m.groupby(level="year").sum()
    for gname in show:
        key = "".join(ch for ch in gname.lower() if ch.isalnum())[:18]
        for y in range(2017, 2026):
            reg.add(f"glad_mining_{key}_{y}", ann.loc[y, gname], "ha", f"GLAD-L forest-loss alerts on land first mapped "
                    f"as mining by the next year, {gname}, {y} (alert area, a timing signal; not net additions)",
                    "description", SRC, measure="glad_alerts", zone=GROUPS[gname][0], period=str(y))
    q = m["La Pampa sector"]
    reg.add("glad_lapampa_2017_2018_mean", q.loc[pd.IndexSlice[2017:D.REF_YEAR, :]].mean(), "ha/quarter",
            "La Pampa sector, mining-related GLAD-L alerts per quarter, mean of the 8 quarters of 2017-2018", "description",
            SRC, measure="glad_alerts", zone="lapampa", period="2017Q1-2018Q4")
    reg.add("glad_lapampa_2019_mean", q.loc[pd.IndexSlice[D.FIRST_POST, :]].mean(), "ha/quarter",
            "La Pampa sector, mining-related GLAD-L alerts per quarter, mean of the 4 quarters of 2019", "description",
            SRC, measure="glad_alerts", zone="lapampa", period="2019Q1-Q4")
    reg.add("glad_lapampa_2019q2_2020q4_mean", q.loc[(D.FIRST_POST, 2):(2020, 4)].mean(), "ha/quarter",
            "La Pampa sector, mining-related GLAD-L alerts per quarter, 2019Q2-2020Q4 mean (a quarterly description "
            "window, not a treatment period)", "description", SRC, measure="glad_alerts", zone="lapampa",
            period="2019Q2-2020Q4")
    s2_check(reg)
    print(ann.round(0).to_string())


def s2_check(reg):
    """Sentinel-2 alerts (GLAD-S2, 10 m, ~5-day revisit) in the western La Pampa sector (70.15-70.00 W; the only part
    inside the downloaded tile): monthly hectares in 2019, to test whether 2019 Landsat alerts are just cloud delay."""
    import rasterio
    from rasterio.windows import from_bounds
    f = RAW / "S2alert_alertDate_080W_20S_070W_10S.tif"
    if not f.exists():                     # git-ignored tile: re-register the values saved on the last full run
        cache = INTER / "raw_only_numbers.csv"
        if cache.exists():
            for r in pd.read_csv(cache).query("id.str.startswith('s2_lp_west_')").itertuples():
                reg.add(r.id, r.value, r.unit, r.description + " (saved from the last run with the raw tile)", "description",
                        r.source_data, measure="glad_alerts", zone="lapampa (70.15-70.00 W box)", period={"s2_lp_west_2019_mar_sep_ha": "Mar-Sep 2019", "s2_lp_west_2019_aug_ha": "Aug 2019"}.get(r.id, "Mar-Sep 2020"))
        return
    with rasterio.open(f) as r:
        a = r.read(1, window=from_bounds(-70.15, -13.06, -70.0, -12.88, r.transform)); tr = r.transform
    v = a[a > 0].astype(int)
    lat = -12.97
    pix_ha = (abs(tr.a) * 111320 * np.cos(np.radians(lat))) * (abs(tr.e) * 110574) / 1e4
    d = pd.to_datetime("2018-12-31") + pd.to_timedelta(v, unit="D")
    s = pd.Series(pix_ha, index=d).resample("MS").sum()
    s19 = s.loc["2019-01":"2019-12"]
    reg.add("s2_lp_west_2019_mar_sep_ha", s19.loc["2019-03":"2019-09"].sum(), "ha", "GLAD-S2 alerts, western La Pampa sector, Mar-Sep 2019", "description", "UMD GLAD-S2 alerts", measure="glad_alerts", zone="lapampa (70.15-70.00 W box)", period="Mar-Sep 2019")
    reg.add("s2_lp_west_2019_aug_ha", s19.loc["2019-08"].sum(), "ha", "GLAD-S2 alerts, western La Pampa sector, August 2019", "description", "UMD GLAD-S2 alerts", measure="glad_alerts", zone="lapampa (70.15-70.00 W box)", period="Aug 2019")
    reg.add("s2_lp_west_2020_mar_sep_ha", s.loc["2020-03":"2020-09"].sum(), "ha", "GLAD-S2 alerts, western La Pampa sector, Mar-Sep 2020", "description", "UMD GLAD-S2 alerts", measure="glad_alerts", zone="lapampa (70.15-70.00 W box)", period="Mar-Sep 2020")
    save_raw_only([r for k, r in reg.rows.items() if k.startswith("s2_lp_west_")])


def save_raw_only(rows):
    """Keep numbers that need git-ignored raw files in data_intermediate/raw_only_numbers.csv (committed), so a
    fresh clone still registers them."""
    f = INTER / "raw_only_numbers.csv"
    new = pd.DataFrame(rows)[["id", "value", "unit", "description", "source_data"]]
    old = pd.read_csv(f) if f.exists() else new.iloc[:0]
    pd.concat([old[~old.id.isin(new.id)], new]).sort_values("id").to_csv(f, index=False)
