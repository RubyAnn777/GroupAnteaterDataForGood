"""Inside the Tambopata National Reserve (plan v3): did mining move INTO the reserve (MAAP #241)?

Findings come from the raster registry: unit 'tambopata_nr' (zone 1, first in precedence, so it is disjoint from the
Tambopata buffer zone and "buffer zone + reserve" is an exact sum, no assumption needed). Outcome = NET mining
additions (ha/yr) = new land + re-mined - stopped, MapBiomas Peru Collection 4 rasters, our pixel accounting; every
mean and sum is registered for net and its three parts (net = new + re-mined - stopped, asserted).

The publisher's protected-area statistics (MAPBIOMAS-PERU-LULC-COL4-AREAS-PROTEGIDAS.xlsx, sheet COVERAGE_4, class
"4.2. Minería") are kept ONLY as a publisher check: Tambopata NR mining 2025 = 776.9 ha in the file, 777 ha on the
MapBiomas platform, and our raster stock must agree within 1%. Bahuaja-Sonene NP and Amarakaeri RC have no unit in
the raster registry (they are inside "other protected areas", and Bahuaja-Sonene NP lies mostly in Puno, outside the
study region), so they are no longer reported.

2017: the one-year step inside the reserve (+533 ha net) is first-time mining (new land) in the raster accounting,
matching Asner & Tupayachi (2017) on mining inside the reserve to October 2016. It is not called a reclassification.
"""
from __future__ import annotations
import pandas as pd
import matplotlib.pyplot as plt

from common import (ROOT, OUT, x_of, style_axes, add_event_markers, set_year_ticks, finish_figure, EVENT_TITLE_PAD,
                    headline, label_end, callout, C, INK, INK2)
import checks
import definitions as D
import zonedata as Z

ANP_FILE = ROOT / "data_raw" / "mapbiomas_peru" / "MAPBIOMAS-PERU-LULC-COL4-AREAS-PROTEGIDAS.xlsx"
MINING = "4.2. Minería"
SRC_PUB = "MAPBIOMAS-PERU-LULC-COL4-AREAS-PROTEGIDAS.xlsx (MapBiomas Peru, Collection 4, v1 Aug 2026)"
SRC = D.SOURCE
NR, BZ = "tambopata_nr", D.TREATED_ZONE
MEAS = ["net"] + D.PARTS
Y0 = D.PANEL_YEARS[0] - 1                    # level table from 2010, additions from 2011
YEARS = list(range(1985, D.YEARS[1] + 1))


def publisher_tambopata_nr() -> pd.Series:
    """Tambopata NR mining area (stock, ha) by year from the publisher's protected-area statistics (check only)."""
    raw = pd.read_excel(ANP_FILE, sheet_name="COVERAGE_4")
    need = ["territory_level_2_1", "territory_level_3_1", "class_level_4"] + [f"y{y}" for y in YEARS]
    assert not [c for c in need if c not in raw.columns], "ANP file layout changed"
    t = raw[(raw.territory_level_2_1 == "Tambopata") & (raw.territory_level_3_1 == "Reserva Nacional")]
    s = t[t.class_level_4 == MINING][[f"y{y}" for y in YEARS]].sum()
    s.index = YEARS
    return s, raw


def publisher_checks(reg, ras_stock: pd.Series):
    pub, raw = publisher_tambopata_nr()
    checks.check("ANP file: Tambopata NR mining 2025 (class 4.2), ha, rounded to 0.1", round(pub.loc[2025], 1), 776.9,
                 tol=0.05)
    area = raw[(raw.territory_level_2_1 == "Tambopata")][["y2000", "y2025"]].sum()
    checks.check("ANP file: Tambopata total area constant 2000 vs 2025 (diff, ha)", abs(area["y2025"] - area["y2000"]),
                 0, tol=1)
    PUBLISHER_PERU_ANP_TAMBOPATA_2025 = 777   # MapBiomas Peru platform, Col 4, read 2026-10-10 (tooltip rounds to integer)
    checks.check("Publisher check (MapBiomas Peru platform, Col 4, read 2026-10-10; "
                 "data_raw/mapbiomas_peru/platform_check_tambopata_reserve_2026-10-10.jpg): Tambopata NR mining 2025, ha",
                 round(float(pub.loc[2025])), PUBLISHER_PERU_ANP_TAMBOPATA_2025, tol=0.5)
    checks.check("Raster registry vs publisher file: Tambopata NR mining 2025, ha (tolerance 1%)",
                 float(ras_stock.loc[2025]), float(pub.loc[2025]), tol=0.01 * float(pub.loc[2025]))
    checks.save()
    reg.add("anp_publisher_tam_nr_stock_2025", pub.loc[2025], "ha", "Mining area (stock), Tambopata National Reserve, "
            "2025, publisher's protected-area statistics (check only; platform shows 777 ha)", "description", SRC_PUB,
            measure="stock", zone=NR, period="2025")
    reg.add("anp_raster_minus_publisher_tam_nr_stock_2025", float(ras_stock.loc[2025] - pub.loc[2025]), "ha",
            "Mining area (stock), Tambopata National Reserve, 2025: raster registry minus publisher file (reconciliation)",
            "description", f"{SRC}; {SRC_PUB}", measure="stock", zone=NR, period="2025")


def run(pack, reg):
    print("\n== Inside the Tambopata National Reserve (v3: raster registry, net additions) ==")
    ru = Z.region_units()
    W = {m: Z.wide(ru, D.COLS[m]) for m in MEAS + ["stock"]}
    publisher_checks(reg, W["stock"][NR])

    # ---- tables (file names kept: slides_figures.py reads the levels file's "Tambopata NR" column)
    W["stock"].loc[Y0:, [NR]].rename(columns={NR: "Tambopata NR"}).round(1).to_csv(OUT / "peru_anp_mining_levels_2010_2025.csv")
    adds = pd.DataFrame({m: W[m][NR] for m in MEAS}).loc[Y0 + 1:]
    adds.round(1).to_csv(OUT / "peru_anp_additions_2011_2025.csv")
    comb = {m: W[m][BZ] + W[m][NR] for m in MEAS}
    pd.DataFrame({"tambopata_bz_net": W["net"][BZ], "tambopata_nr_net": W["net"][NR], "bz_plus_nr_net": comb["net"]}) \
        .loc[Y0 + 1:].round(1).to_csv(OUT / "peru_anp_tambopata_bz_plus_reserve.csv")

    rows = {}
    ex = [y for y in range(*D.PERIODS["later"]) if y != D.LATER_EX] + [D.PERIODS["later"][1]]
    for p in ("pre", "during", "later"):
        vals = {m: Z.period_mean(comb[m], p) for m in MEAS}
        assert abs(vals["net"] - (vals["new"] + vals["remined"] - vals["stopped"])) < 0.01
        Z.register_parts(reg, f"tambopata_bz_plus_nr_{p}", vals, "tambopata_bz + tambopata_nr", D.period_label(p),
                         "mean per year, Tambopata buffer zone and the reserve inside it combined (disjoint zones)")
        nr_mean = Z.period_mean(W["net"][NR], p)
        rows[D.period_label(p)] = dict(reserve_net=nr_mean, bz_plus_nr_net=vals["net"])
        if nr_mean <= 0 or vals["net"] <= 0:          # a share of a negative mean is not defined
            continue
        reg.add(f"tambopata_nr_share_of_bz_plus_nr_{p}_net", nr_mean / vals["net"], "share",
                f"Share of the combined (Tambopata buffer zone + reserve) mean net additions, {D.period_label(p)}, that "
                "falls inside the reserve", "description", SRC, measure="net", zone=NR, period=D.period_label(p))
    Z.register_parts(reg, "tambopata_bz_plus_nr_later_ex2023", {m: comb[m].loc[ex].mean() for m in MEAS},
                     "tambopata_bz + tambopata_nr", "2022, 2024, 2025", "mean per year without 2023, combined")
    for y in (2017, 2022, 2024):                           # peru.py registers 2018-21, 2023, 2025 for the reserve
        Z.register_parts(reg, f"tambopata_nr_{y}", {m: W[m].loc[y, NR] for m in MEAS}, NR, str(y), "that year")
    # stable aliases used by the brief, deck and slides_map_export.py (same values as peru.py's tambopata_nr_* ids)
    reg.add("anp_level_tam_nr_2025", W["stock"].loc[2025, NR], "ha", "Mining area (stock), Tambopata National Reserve, "
            "2025, raster registry (= tambopata_nr_stock_2025)", "description", SRC, measure="stock", zone=NR,
            period="2025")
    for y in (2025, 2017):
        reg.add(f"anp_tam_nr_addition_{y}", W["net"].loc[y, NR], "ha/yr", f"Net mining additions, Tambopata National "
                f"Reserve, {y}, raster registry (= tambopata_nr_{y}_net)"
                + ("; cf. MAAP #241 ~500 ha H2 2025-Feb 2026, different source and period, not subtracted" if y == 2025
                   else "; almost all first-time mining (tambopata_nr_2017_new)"),
                "description", SRC, measure="net", zone=NR, period=str(y))
    pm = pd.DataFrame(rows).T
    pm.round(2).to_csv(OUT / "peru_anp_period_means.csv")
    print("\nReserve and combined mean net additions (ha/yr):\n", pm.round(1).to_string())
    print("\nTambopata NR net and parts:\n", adds.loc[2014:].round(0).to_string())
    _fig_reserve(W)
    _fig_combined(W)
    return dict(adds=adds, combined=comb, period_means=pm)


def _parts_panel(ax, W, unit, yrs):
    xs = x_of(yrs)
    net, new, rem, stp = (W[m].loc[yrs, unit] for m in MEAS)
    ax.bar(xs, new, 0.72, color=C["new"], label=D.MEASURE_NAME["new"])
    ax.bar(xs, rem, 0.72, bottom=new.clip(lower=0), color=C["remined"], label=D.MEASURE_NAME["remined"],
           edgecolor="white", linewidth=0.6)
    ax.bar(xs, -stp, 0.72, color=C["stopped"], label="− " + D.MEASURE_NAME["stopped"])
    ax.plot(xs, net, color=INK, lw=2, marker="o", ms=4, mec="white", mew=0.8, label="Net additions", zorder=5)
    ax.axhline(0, color=INK2, lw=0.8)
    ax.set_ylabel("ha/yr")
    style_axes(ax)


def _fig_reserve(W):
    yrs = list(range(Y0 + 1, D.YEARS[1] + 1))
    fig, (a1, a2) = plt.subplots(2, 1, figsize=(9, 8), sharex=True, gridspec_kw={"hspace": 0.42})
    n17, n25 = W["net"].loc[2017, NR], W["net"].loc[2025, NR]
    headline(fig, f"Inside the reserve, net additions were near zero except 2017 ({n17:+,.0f} ha) and 2025 ({n25:+,.0f})"
             .replace("-", "−"),
             f"Net mining additions = new land + re-mined − stopped (ha/yr), {yrs[0]}–{yrs[-1]}, MapBiomas rasters. "
             "Top: the reserve. Bottom: its buffer zone. Different y-scales.")
    _parts_panel(a1, W, NR, yrs)
    a1.set_title("Tambopata National Reserve", pad=EVENT_TITLE_PAD)
    a1.legend(loc="center left", bbox_to_anchor=(0.0, 0.6), ncol=1, fontsize=8, frameon=False)
    callout(a1, 2017, n17, f"2017: {n17:+,.0f} ha,\nalmost all new land".replace("-", "−"), dx=-50, dy=-4, ha="right")
    callout(a1, 2025, n25, f"2025: {n25:+,.0f} ha".replace("-", "−"), dx=-40, dy=10, ha="right")
    _parts_panel(a2, W, BZ, yrs)
    a2.set_title("Tambopata buffer zone")
    add_event_markers(a1, label=True); add_event_markers(a2)
    a2.set_xlim(yrs[0] - 0.6, yrs[-1] + 0.6)
    set_year_ticks(a2, yrs)
    finish_figure(fig, f"{SRC}. Raster stock 2025 inside the reserve agrees with the publisher's protected-area "
                       "statistics (777 ha). Mining area = all mining (legal and illegal); river dredging and mercury are "
                       "invisible. Description.", OUT / "fig_peru_inside_reserves.png", event_note=True)


def _fig_combined(W):
    yrs = list(range(D.YEARS[0], D.YEARS[1] + 1)); xs = x_of(yrs)
    bz, nr = W["net"].loc[yrs, BZ], W["net"].loc[yrs, NR]
    tot = bz + nr
    sh25 = nr.loc[2025] / tot.loc[2025]
    fig, ax = plt.subplots(figsize=(9, 5.2))
    headline(fig, f"Little of Tambopata's net mining additions fell inside the reserve until 2025 ({sh25:.0%} that year)",
             f"Net mining additions (new land + re-mined − stopped), ha/yr, {yrs[0]}–{yrs[-1]}: Tambopata buffer zone and "
             "the reserve inside it (disjoint zones), stacked")
    ax.bar(xs, bz, color=C["lapampa"], width=0.72)
    ax.bar(xs, nr, bottom=bz.clip(lower=0), color=C["reserve"], width=0.72, edgecolor="white", linewidth=0.8)
    ax.plot(xs, tot, color=INK, marker="o", markersize=4, mec="white", mew=0.8, linewidth=1.2)
    from matplotlib.patches import Patch
    from matplotlib.lines import Line2D
    ax.legend(handles=[Patch(color=C["lapampa"], label="Tambopata buffer zone"),
                       Patch(color=C["reserve"], label="Tambopata National Reserve"),
                       Line2D([], [], color=INK, marker="o", ms=4, lw=1.2, label="Sum")],
              loc="upper left", ncol=3, fontsize=8.5, handlelength=1.2, frameon=False)
    ax.axhline(0, color=INK2, lw=0.8)
    ax.set_ylim(None, ax.get_ylim()[1] * 1.12)
    ax.set_ylabel("Net additions, ha/yr")
    ax.set_title("Did mining move into the reserve?", pad=EVENT_TITLE_PAD)
    style_axes(ax); add_event_markers(ax, label=True)
    ax.set_xlim(yrs[0] - 0.6, yrs[-1] + 0.6); set_year_ticks(ax, yrs)
    finish_figure(fig, f"{SRC}. The reserve and its buffer zone are disjoint in the zone registry, so the sum is exact. "
                       "Description.", OUT / "fig_peru_displacement_into_reserve.png", event_note=True)


if __name__ == "__main__":
    from common import Numbers, load_pack
    reg = Numbers(); run(load_pack(), reg)
    for k, v in reg.rows.items():
        print(k, round(v["value"], 3))
