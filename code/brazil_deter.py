"""Brazil: INPE DETER-Amazonia mining alerts (class MINERACAO) inside three indigenous territories.

Rebuilds the scout's tables from the two committed raw files (data_raw/inpe_deter/): alert polygons are
intersected with FUNAI territory polygons in EPSG:5880 (Albers, equal area); the area of the intersection is
assigned to the month of `view_date`. Munduruku = Munduruku + Sai-Cinza + Munduruku-Taquara (the scout's choice;
Sai-Cinza has alerts from 2020). DETER is an alert system (new or expanded mining only, not the stock; minimum
mappable area of a few ha; cloud gaps; no river dredging). It is a different measurement from MapBiomas: never
add, subtract or splice the two. All claims here are DESCRIPTION.
"""
import json
import geopandas as gpd
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from common import ROOT, OUT, style_axes, finish_figure

RAW = ROOT / "data_raw" / "inpe_deter"
SCOUT_ANNUAL = ROOT / "docs" / "overnight" / "notes" / "deter_mining_ti_annual_km2.csv"
MUN = "Munduruku (incl. Sai-Cinza, Taquara)"
TERR = ["Yanomami", MUN, "Kayapó"]
SRC = "INPE TerraBrasilis, DETER-Amazonia class MINERACAO (WFS layer deter-amz:deter_amz, fetched 2026-10-10); FUNAI territory polygons"
LAST_MONTH = "2026-08"          # September 2026 is partial (data to 29 Sep) so it is left out of the figure

def build_tables():
    d = gpd.read_file(RAW / "deter_amz_mineracao.geojson")
    d["view_date"] = pd.to_datetime(d["view_date"])
    d["ym"] = d.view_date.dt.to_period("M").astype(str)
    d["year"] = d.view_date.dt.year
    t = gpd.read_file(RAW / "funai_tis_selected.geojson")[["terrai_nome", "geometry"]]
    t = t[t.terrai_nome.isin(["Yanomami", "Munduruku", "Kayapó", "Sai-Cinza", "Munduruku-Taquara"])].to_crs(5880)
    d5 = d.to_crs(5880)
    d5["geometry"] = d5.geometry.buffer(0)
    t["geometry"] = t.geometry.buffer(0)
    j = gpd.overlay(d5[["gid", "view_date", "ym", "year", "geometry"]], t, how="intersection")
    j["km2"] = j.area / 1e6
    j["ti"] = j.terrai_nome.replace({"Sai-Cinza": MUN, "Munduruku-Taquara": MUN, "Munduruku": MUN})
    full = pd.period_range("2016-08", "2026-09", freq="M").astype(str)
    mon = j.groupby(["ti", "ym"]).km2.sum().unstack(0).reindex(full, fill_value=0.0).fillna(0.0)[TERR]
    mon.index.name = "month"
    return d, mon, j

def run(pack, reg):
    d, mon, j = build_tables()
    ann_cal = j.groupby(["ti", "year"]).km2.sum().unstack(0).fillna(0.0)[TERR]
    ann_cal.index.name = "calendar_year"

    # check 1: annual tables equal the scout's (3 decimals)
    sc = pd.read_csv(SCOUT_ANNUAL, index_col=0)[TERR]
    diff = (ann_cal.round(3).reindex(sc.index).fillna(0) - sc).abs().max().max()
    assert diff < 2e-3, f"annual DETER table differs from the scout's by {diff}"
    print(f"DETER check OK: annual territory tables equal the scout's (max abs diff {diff:.4f} km2)")

    # check 2: biome-wide 2019 total vs the TerraBrasilis dashboard value (Amazonia biome) 105.40 km2
    db = json.load(open(RAW / "dashboard_deter-amazon-month_biome.json"))
    db = pd.DataFrame([f["properties"] for f in db["features"]])
    db = db[db.cl == "MINERACAO"].copy(); db["year"] = 2000 + db.y.astype(int)
    dash19 = db[db.year == 2019].ar.sum()
    wfs19 = d[d.year == 2019].areamunkm.sum()
    rel = abs(wfs19 - dash19) / dash19
    assert abs(dash19 - 105.40) < 0.01 and rel < 0.005, (dash19, wfs19, rel)
    print(f"DETER check OK: 2019 mining alerts WFS (Legal Amazon) {wfs19:.2f} km2 vs dashboard (Amazonia biome) "
          f"{dash19:.2f} km2, difference {100*rel:.2f}% (domain difference: Legal Amazon vs biome)")
    pd.DataFrame([dict(check="deter_2019_total_km2", ours=wfs19, publisher=dash19, rel_diff_pct=100 * rel,
                       note="ours = Legal Amazon WFS; publisher dashboard = Amazonia biome")]).to_csv(
        OUT / "brazil_deter_check.csv", index=False)

    # tables: km2 as published + ha; calendar year and Aug-Jul PRODES year (label = year in which it ends)
    mon_out = mon.copy()
    mon_out.columns = [c + " km2" for c in mon.columns]
    for c in TERR:
        mon_out[c + " ha"] = mon[c] * 100
    mon_out.to_csv(OUT / "brazil_deter_monthly.csv")
    mi = pd.PeriodIndex(mon.index, freq="M")
    prodes = pd.Series([p.year + (1 if p.month >= 8 else 0) for p in mi], index=mon.index)
    ann_prodes = mon.groupby(prodes).sum()
    ann_prodes.index.name = "prodes_year_ending_july"
    for name, a in (("calendar", ann_cal), ("prodes", ann_prodes)):
        o = a.copy()
        for c in TERR:
            o[c + " ha"] = a[c] * 100
        o.round(4).to_csv(OUT / f"brazil_deter_annual_{name}.csv")

    # numbers (description): 12 months before vs after Feb 2023 (Feb 2022-Jan 2023 vs Feb 2023-Jan 2024)
    before = mon.loc["2022-02":"2023-01"].sum(); after = mon.loc["2023-02":"2024-01"].sum()
    s = "INPE DETER-Amazonia MINERACAO alerts x FUNAI polygons"
    for key, c in (("yan", "Yanomami"), ("kay", "Kayapó"), ("mun", MUN)):
        reg.add(f"br_deter_{key}_12m_before_feb2023_km2", before[c], "km2",
                f"DETER mining alert area, {c}, Feb 2022-Jan 2023 (12 months before the Feb 2023 Yanomami operation)", "description", s)
        reg.add(f"br_deter_{key}_12m_after_feb2023_km2", after[c], "km2",
                f"DETER mining alert area, {c}, Feb 2023-Jan 2024 (12 months from the Feb 2023 Yanomami operation; the date is not a Munduruku/Kayapo event)", "description", s)
    reg.add("br_deter_yan_peak_month_km2", mon["Yanomami"].loc["2022-01":"2024-12"].max(), "km2",
            "Largest monthly DETER mining alert area in Yanomami, 2022-2024", "description", s)
    reg.add("br_deter_yan_peak_month_is_2023", float(mon["Yanomami"].loc["2022-01":"2024-12"].idxmax().startswith("2023")), "flag",
            "1 if the Yanomami monthly peak 2022-2024 falls in 2023 (alerts are dated by detection, not by clearing)", "description", s)
    for c, key in zip(TERR, ("yan", "mun", "kay")):
        for y in (2019, 2022, 2023, 2024, 2025):
            reg.add(f"br_deter_{key}_cal{y}_km2", ann_cal.loc[y, c], "km2", f"DETER mining alert area, {c}, calendar year {y}", "description", s)
    reg.add("br_deter_2019_total_wfs_km2", wfs19, "km2", "DETER mining alerts 2019, Legal Amazon, all states (WFS)", "description", s)
    reg.add("br_deter_2019_total_dashboard_km2", dash19, "km2", "DETER mining alerts 2019, Amazonia biome (TerraBrasilis dashboard); check value", "description", "TerraBrasilis dashboard")

    # ------------------------------------------------------------------ figure
    m = mon.loc["2019-01":LAST_MONTH].copy()
    m.index = pd.PeriodIndex(m.index, freq="M").to_timestamp()
    roll = mon.rolling(12).sum().loc["2019-01":LAST_MONTH]; roll.index = m.index
    ev = {  # territory -> [(date, label, colour, solid)]
        "Yanomami": [("2023-01-20", "Emergency 20 Jan 2023", "#6C7A7B", False),
                     ("2023-02-01", "Operation Feb 2023", "#B03A2E", True)],
        MUN: [("2023-08-01", "Operation Aug 2023", "#B03A2E", True),
              ("2024-11-01", "Operation Nov 2024", "#2E6F9E", True)],
        "Kayapó": [("2025-05-01", "Operation May 2025", "#7A5C1E", True)],
    }
    fig = plt.figure(figsize=(9, 9.6))
    outer = fig.add_gridspec(3, 1, hspace=0.42)
    axs = []
    for g in range(3):
        sub = outer[g].subgridspec(2, 1, height_ratios=[1.25, 1], hspace=0.1)
        axs += [fig.add_subplot(sub[0]), fig.add_subplot(sub[1])]
    for a in axs[1:]:
        a.sharex(axs[0])
    cols = {"Yanomami": "#9C2F2F", MUN: "#1F6F8B", "Kayapó": "#6B8E23"}
    for k, c in enumerate(TERR):
        a, r = axs[2 * k], axs[2 * k + 1]
        a.bar(m.index, m[c], width=28, align="edge", color=cols[c])
        a.set_ylabel("km2 per month", fontsize=8)
        a.set_title(c if c != MUN else "Munduruku (incl. Sai-Cinza and Taquara territories)", loc="left", fontsize=10, pad=22)
        r.plot(roll.index, roll[c], color="#222222", lw=1.5)
        r.set_ylabel("km2, trailing\n12-month sum", fontsize=8)
        r.set_ylim(bottom=0)
        for aa in (a, r):
            style_axes(aa)
            for dt, lab, col, solid in ev[c]:
                aa.axvline(pd.Timestamp(dt), color=col, ls="-" if solid else "--", lw=1.3 if solid else 0.9, zorder=0)
        for i, (dt, lab, col, solid) in enumerate(ev[c]):
            a.annotate(lab, xy=(pd.Timestamp(dt), 1.0), xycoords=("data", "axes fraction"), xytext=(0, 2 + 8 * i),
                       textcoords="offset points", fontsize=6.8, color=col, ha="center", va="bottom", annotation_clip=False)
        a.tick_params(labelbottom=False)
        if k < 2:
            r.tick_params(labelbottom=False)
        a.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, p: f"{v:g}"))
        r.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, p: f"{v:g}"))
    axs[5].xaxis.set_major_locator(mdates.YearLocator())
    axs[5].xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    axs[5].set_xlim(pd.Timestamp("2019-01-01"), pd.Timestamp("2026-09-01"))
    txt = (SRC + ". DETER is an ALERT system: it flags new or expanded mining (minimum area of a few ha), has gaps under cloud and sees "
           "no river dredging; alerts are dated by detection, not by when the clearing happened. It is not a map of the stock and is a "
           "different measurement from MapBiomas: never subtract or splice the two. Monthly bars, calendar months to Aug 2026; "
           "note the different y-axis scales. Description only.")
    finish_figure(fig, txt, OUT / "fig_brazil_deter_monthly.png", rect_bottom=0.07)
