"""Peru protected areas themselves (MapBiomas Peru Collection 4, "Areas naturales protegidas").

Question: did mining move INTO the reserves (MAAP #241)? The pack only has buffer zones; this file has the
reserves proper. Same publisher + collection as the buffer-zone table (MapBiomas Peru Col 4, class 30 =
"4.2. Minería"), so side-by-side comparison and the combined buffer-zone + reserve view are allowed
(rule 6 only forbids mixing sources, e.g. MAAP).

Parsing: sheet COVERAGE_4; one row = ANP x department x class. ANP = (territory_level_2_1 name,
territory_level_3_1 category); department = territory_level_2_2; years are columns y1985..y2025.
Aggregate first (rule 2): sum over departments per ANP-year, then difference. Missing class-30 rows are
implicit zeros (ANP has other classes but no mining row), so the panel is built from ALL ANP in the file.
ASSUMPTION (not verifiable from the data): the buffer zone excludes the reserve itself, so
buffer-zone + reserve is not double counting.

Rows 2016->2017: see investigate_2017(); the transition sheet shows where the +534 ha came from.
"""
from __future__ import annotations
import pandas as pd
import matplotlib.pyplot as plt

from common import (ROOT, OUT, period_mean, x_of, style_axes, add_event_markers, set_year_ticks,
                    finish_figure, EVENT_TITLE_PAD)
import checks

ANP_FILE = ROOT / "data_raw" / "mapbiomas_peru" / "MAPBIOMAS-PERU-LULC-COL4-AREAS-PROTEGIDAS.xlsx"
MINING = "4.2. Minería"
SRC = "MAPBIOMAS-PERU-LULC-COL4-AREAS-PROTEGIDAS.xlsx (MapBiomas Peru, Collection 4, v1 Aug 2026)"
SRC_FIG = "MapBiomas Peru, Collection 4 (class 4.2 Minería), protected areas and buffer-zone statistics"
Y0 = 2010
YEARS = list(range(1985, 2026))
PERIODS = {"2016-18": (2016, 2018), "2019-21": (2019, 2021), "2022-25": (2022, 2025)}
RES = {  # label -> (ANP name, category, buffer-zone column name in peru.build_series)
    "Tambopata NR": ("Tambopata", "Reserva Nacional", "Tambopata"),
    "Bahuaja-Sonene NP": ("Bahuaja-Sonene", "Parque Nacional", "Bahuaja-Sonene"),
    "Amarakaeri RC": ("Amarakaeri", "Reserva Comunal", "Amarakaeri"),
}
COL = {"Tambopata NR": "#d9a441", "Bahuaja-Sonene NP": "#6aa84f", "Amarakaeri RC": "#7a9cc6"}

def load_anp() -> tuple[pd.DataFrame, pd.DataFrame]:
    """Return (raw COVERAGE_4 rows, panel of mining_ha: one row per ANP-year, zeros filled)."""
    raw = pd.read_excel(ANP_FILE, sheet_name="COVERAGE_4")
    ycols = [f"y{y}" for y in YEARS]
    need = ["territory_level_2_1", "territory_level_3_1", "territory_level_2_2", "class_level_4"] + ycols
    missing = [c for c in need if c not in raw.columns]
    assert not missing, f"ANP file layout changed: {missing}"
    raw = raw.rename(columns={"territory_level_2_1": "anp", "territory_level_3_1": "category",
                              "territory_level_2_2": "department"})
    mine = raw[raw["class_level_4"] == MINING]
    assert len(mine) == 13, f"expected 13 ANP x department rows with mining, got {len(mine)}"
    lv = (mine.groupby(["anp", "category"])[ycols].sum()
          .reindex(raw[["anp", "category"]].drop_duplicates().set_index(["anp", "category"]).index, fill_value=0.0))
    lv.columns = YEARS
    panel = lv.stack().rename("mining_ha").reset_index().rename(columns={"level_2": "year"})
    panel.columns = ["anp", "category", "year", "mining_ha"]
    return raw, panel

def _series(panel, key):
    name, cat, _ = key
    return panel[(panel.anp == name) & (panel.category == cat)].set_index("year")["mining_ha"].sort_index()

def investigate_2017(reg):
    """Where does the +534 ha in Tambopata NR 2016->2017 come from? Uses TRANSITION_4 (class from -> class to,
    annual periods p2016_2017) and the class-area table. Description only; no external confirmation."""
    f = ANP_FILE
    tr = pd.read_excel(f, sheet_name="TRANSITION_4")
    t = tr[tr["territory_level_2"] == "Tambopata"]
    into = t[(t["class_level_2_to"] == MINING) & (t["class_from"] != 30)].set_index("class_level_2_from")["p2016_2017"]
    out = t[(t["class_level_2_from"] == MINING) & (t["class_to"] != 30)]["p2016_2017"].sum()
    stay = t[(t["class_from"] == 30) & (t["class_to"] == 30)]["p2016_2017"].sum()
    tab = into.sort_values(ascending=False).rename("ha_converted_to_mining_2016_17").to_frame()
    tab.loc["(outflow from mining to other classes)"] = -out
    tab.round(1).to_csv(OUT / "peru_anp_tambopata_2017_transitions.csv")
    # class-area changes 2016 -> 2017 in the same reserve (is there a matching loss elsewhere?)
    raw = pd.read_excel(f, sheet_name="COVERAGE_4")
    c = raw[raw["territory_level_2_1"] == "Tambopata"].groupby("class_level_4")[["y2016", "y2017"]].sum()
    c["delta"] = c["y2017"] - c["y2016"]
    c.round(1).sort_values("delta").to_csv(OUT / "peru_anp_tambopata_class_change_2016_17.csv")
    inflow = float(into.sum())
    nat = float(into.get("1.1. Bosque", 0) + into.get("1.4. Bosque inundable", 0))
    anthro = float(into.get("3.1. Mosaico agropecuario", 0) + into.get("4.8. Otra área antrópica sin vegetación", 0))
    # the sheet has 'p2016_2017' summed rounding vs level jump
    assert abs(inflow - out - (c.loc[MINING, "delta"])) < 3, "transitions do not reconcile with level change"
    for id_, v, d in [
        ("anp_tam_2017_gross_inflow_to_mining", inflow, "Gross area converted to mining inside Tambopata NR, 2016->2017 (TRANSITION_4)"),
        ("anp_tam_2017_inflow_from_forest_types", nat, "...of which from 1.1 Bosque + 1.4 Bosque inundable"),
        ("anp_tam_2017_inflow_from_agri_or_bare_anthropic", anthro, "...of which from 3.1 Mosaico agropecuario + 4.8 otra area antropica sin vegetacion"),
        ("anp_tam_2017_outflow_from_mining", out, "Area leaving mining inside Tambopata NR, 2016->2017"),
        ("anp_tam_2017_swap_forest_classes_ha", float(c.loc["1.4. Bosque inundable", "delta"]), "Level change of 1.4 Bosque inundable 2016->2017 (compare: +471 in 1.1 Bosque, i.e. forest-class swapping)")]:
        reg.add(id_, v, "ha", d, "description", SRC)
    print(f"\n2016->17 Tambopata NR: gross inflow into mining {inflow:.0f} ha (forest types {nat:.0f}, agri/bare-anthropic {anthro:.0f}); "
          f"outflow {out:.1f}; flooded-forest class changed {c.loc['1.4. Bosque inundable','delta']:.0f}, forest {c.loc['1.1. Bosque','delta']:+.0f}.")
    return tab

def run(pack, reg):
    print("\n== Peru protected areas (ANP, Collection 4) ==")
    import peru
    raw, panel = load_anp()
    # ---- internal checks of the parser (fail loudly)
    tam = _series(panel, RES["Tambopata NR"])
    checks.check("ANP file: Tambopata NR mining 2025 (class 4.2), ha, rounded to 0.1",
                 round(tam.loc[2025], 1), 776.9, tol=0.05)
    checks.check("ANP file: all ANP mining 2025 (class 4.2), ha, rounded",
                 round(panel[panel.year == 2025]["mining_ha"].sum(), 0), 834, tol=0.5)
    area = raw[(raw["anp"] == "Tambopata")][["y2000", "y2025"]].sum()
    checks.check("ANP file: Tambopata total area constant 2000 vs 2025 (diff, ha)", abs(area["y2025"] - area["y2000"]), 0, tol=1)
    # file-total area vs FZS (Tambopata NR 2,746 km2 per fzs.org, via agent.md §10): external plausibility, +1.2%
    checks.check("ANP file: Tambopata total area, km2 (FZS says 2,746; plausibility only, tol 50)", area["y2025"] / 100, 2746, tol=50)
    checks.check_pending("Publisher check: Tambopata NR class 4.2 Minería 2025 (ha) vs MapBiomas Peru platform", float(tam.loc[2025]))
    checks.save()

    # ---- series
    levels = pd.DataFrame({k: _series(panel, v) for k, v in RES.items()})
    adds = levels.diff()
    assert (levels.index == YEARS).all()
    levels.loc[Y0:].round(1).to_csv(OUT / "peru_anp_mining_levels_2010_2025.csv")
    adds.loc[Y0 + 1:].round(1).to_csv(OUT / "peru_anp_additions_2011_2025.csv")
    # buffer zones of the same three areas, same collection
    _, bz_adds, _ = peru.build_series(pack)
    bz = pd.DataFrame({k: bz_adds[v[2]] for k, v in RES.items()})
    # combined 'displacement into the reserve': buffer zone + reserve (Tambopata)
    comb = pd.DataFrame({"Tambopata buffer zone": bz["Tambopata NR"], "Tambopata NR (inside)": adds["Tambopata NR"]})
    comb["Tambopata BZ + NR"] = comb.sum(axis=1)
    comb.loc[Y0 + 1:].round(1).to_csv(OUT / "peru_anp_tambopata_bz_plus_reserve.csv")

    slug = {"Tambopata NR": "tam_nr", "Bahuaja-Sonene NP": "bah_np", "Amarakaeri RC": "ama_rc"}
    rows = {}
    for k in RES:
        for p, (a, b) in PERIODS.items():
            v = period_mean(adds[k], a, b)
            rows[(k, p)] = v
            reg.add(f"anp_mean_add_{slug[k]}_{p.replace('-', '_')}", v, "ha/yr",
                    f"Mean annual addition to mining area INSIDE {k} (reserve proper), {p}", "description", SRC)
        reg.add(f"anp_level_{slug[k]}_2025", float(levels.loc[2025, k]), "ha", f"Mining area inside {k}, 2025", "description", SRC)
    for p, (a, b) in PERIODS.items():
        for lab in ["Tambopata BZ + NR"]:
            v = period_mean(comb[lab], a, b)
            reg.add(f"anp_mean_add_tam_bz_plus_nr_{p.replace('-', '_')}", v, "ha/yr",
                    f"Mean annual addition, Tambopata buffer zone + Tambopata NR combined, {p}", "description", SRC)
            rows[(lab, p)] = v
        reg.add(f"anp_mean_add_tam_nr_share_of_bz_plus_nr_{p.replace('-', '_')}",
                period_mean(adds['Tambopata NR'], a, b) / rows[("Tambopata BZ + NR", p)], "share",
                f"Share of the combined Tambopata (BZ + NR) mean addition that falls inside the reserve, {p}", "description", SRC)
    reg.add("anp_tam_nr_addition_2025", float(adds.loc[2025, "Tambopata NR"]), "ha",
            "Addition inside Tambopata NR in 2025 (cf. MAAP #241 ~500 ha H2 2025-Feb 2026; different source/period, not subtracted)",
            "description", SRC)
    reg.add("anp_tam_nr_addition_2017", float(adds.loc[2017, "Tambopata NR"]), "ha",
            "Addition inside Tambopata NR in 2017: a one-year step, see anp_tam_2017_* numbers", "description", SRC)
    pm = pd.Series(rows).unstack()[list(PERIODS)]
    pm.round(1).to_csv(OUT / "peru_anp_period_means.csv")
    print("\nMean annual additions INSIDE the reserves / combined (ha/yr):\n", pm.round(1).to_string())
    print("\nTambopata BZ + NR additions:\n", comb.loc[2014:].round(0).to_string())

    investigate_2017(reg)

    # ---- figures
    yrs = list(range(Y0 + 1, 2026))
    fig, (a1, a2) = plt.subplots(2, 1, figsize=(8.5, 7.5), sharex=True)
    for k in RES:
        a1.plot(x_of(yrs), adds.loc[yrs, k], marker="o", markersize=4, color=COL[k], linewidth=2, label=k)
        a2.plot(x_of(yrs), bz.loc[yrs, k], marker="o", markersize=4, color=COL[k], linewidth=2, label=k.split()[0] + " buffer zone")
    a1.set_ylabel("New mining area INSIDE\nthe reserve (ha)")
    a1.set_title("Mining inside the reserves (top) is small next to their buffer zones (bottom)", loc="left", pad=EVENT_TITLE_PAD)
    a1.annotate("2017: +534 ha in one year step\n(gross conversion of forest, flooded forest,\nagri. mosaic, beach; classes also swap that year)",
                xy=(2017, adds.loc[2017, "Tambopata NR"]), xytext=(2012.0, 330), fontsize=7, color="#555555",
                arrowprops=dict(arrowstyle="-", color="#999999"))
    a2.set_ylabel("New mining area in the\nbuffer zone (ha)")
    for a in (a1, a2):
        a.legend(fontsize=8, frameon=True, facecolor="white", edgecolor="none", framealpha=0.95, loc="upper left").set_zorder(10)
    a1.set_ylim(None, 560)
    for i, a in enumerate((a1, a2)):
        style_axes(a); add_event_markers(a, label=(i == 0))
    set_year_ticks(a2, yrs)
    finish_figure(fig, f"Source: {SRC_FIG}. Same collection, so the panels are comparable; note the different y-scales.\n"
                       "Description only. Mining area = all mining (legal and illegal); river dredging and mercury are invisible.",
                  OUT / "fig_peru_inside_reserves.png", event_note=True)

    yrs2 = list(range(2014, 2026))
    fig, ax = plt.subplots(figsize=(8.5, 4.6))
    ax.bar(x_of(yrs2), comb.loc[yrs2, "Tambopata buffer zone"], color="#d9a441", width=0.8, label="Tambopata buffer zone")
    ax.bar(x_of(yrs2), comb.loc[yrs2, "Tambopata NR (inside)"], bottom=comb.loc[yrs2, "Tambopata buffer zone"].clip(lower=0),
           color="#B03A2E", width=0.8, label="Tambopata National Reserve (inside)")
    ax.plot(x_of(yrs2), comb.loc[yrs2, "Tambopata BZ + NR"], color="black", marker="o", markersize=4, linewidth=1.2,
            label="Sum: buffer zone + reserve")
    ax.set_ylabel("New mining area (ha)")
    ax.set_title("Tambopata: did mining move into the reserve? Buffer zone + reserve combined", loc="left", pad=EVENT_TITLE_PAD)
    ax.legend(fontsize=8, frameon=True, facecolor="white", edgecolor="none", framealpha=0.95, loc="upper left").set_zorder(10)
    style_axes(ax); add_event_markers(ax, label=True); set_year_ticks(ax, yrs2)
    finish_figure(fig, f"Source: {SRC_FIG}. Assumes the buffer zone excludes the reserve. Description only.",
                  OUT / "fig_peru_displacement_into_reserve.png", event_note=True)
    return dict(levels=levels, adds=adds, bz=bz, combined=comb, period_means=pm)
