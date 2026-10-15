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
                    finish_figure, EVENT_TITLE_PAD, headline, label_end, callout, C, INK, INK2)
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
COL = {"Tambopata NR": C["reserve"], "Bahuaja-Sonene NP": C["other"], "Amarakaeri RC": C["buffer"]}
BZCOL = {"Tambopata NR": C["lapampa"], "Bahuaja-Sonene NP": C["other"], "Amarakaeri RC": C["buffer"]}   # buffer zones: treated orange

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
    PUBLISHER_PERU_ANP_TAMBOPATA_2025 = 777   # MapBiomas Peru platform, Col 4, read 2026-10-10 (tooltip rounds to integer)
    checks.check("Publisher check (MapBiomas Peru platform, Col 4, read 2026-10-10; "
                 "data_raw/mapbiomas_peru/platform_check_tambopata_reserve_2026-10-10.jpg): Tambopata NR mining 2025, ha",
                 round(float(tam.loc[2025])), PUBLISHER_PERU_ANP_TAMBOPATA_2025, tol=0.5)
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
    yrs = list(range(Y0 + 1, 2026)); xs = x_of(yrs)
    fig, (a1, a2) = plt.subplots(2, 1, figsize=(9, 7.8), sharex=True, gridspec_kw={"hspace": 0.38})
    headline(fig, "Mining inside the reserves stays small next to their buffer zones",
             "New mining area each year (annual addition, ha), 2011–2025. Note the different y-scales.")
    for k in RES:
        a1.plot(xs, adds.loc[yrs, k], marker="o", markersize=4, mec="white", mew=0.8, color=COL[k], linewidth=2)
        a2.plot(xs, bz.loc[yrs, k], marker="o", markersize=4, mec="white", mew=0.8, color=BZCOL[k], linewidth=2)
    # direct labels at the right end, nudged apart so they never collide
    def _labels(ax, vals, names, cols, gap):
        order = sorted(range(len(vals)), key=lambda i: vals[i])
        ys, last = {}, -1e18
        for i in order:
            ys[i] = max(vals[i], last + gap); last = ys[i]
        for i in range(len(vals)):
            moved = abs(ys[i] - vals[i]) > 0.15 * gap      # nudged away from its line end: draw a leader line to it
            ax.annotate(names[i], xy=(2025.1, vals[i]), xytext=(2025.45, ys[i]), textcoords="data", va="center", ha="left",
                        fontsize=8.5, color=INK, fontweight="semibold", annotation_clip=False,
                        arrowprops=dict(arrowstyle="-", color=cols[i], lw=0.9, shrinkA=0, shrinkB=1) if moved else None)
    _labels(a1, [adds.loc[2025, k] for k in RES], ["Tambopata", "Bahuaja-Sonene", "Amarakaeri"],
            [COL[k] for k in RES], 62)
    _labels(a2, [bz.loc[2025, k] for k in RES], ["Tambopata", "Bahuaja-Sonene", "Amarakaeri"],
            [BZCOL[k] for k in RES], 330)
    a1.set_ylabel("ha per year")
    a1.set_title("Inside the reserves and park", pad=EVENT_TITLE_PAD)
    callout(a1, 2017, adds.loc[2017, "Tambopata NR"], "2017: one-year step of +534 ha\n(map reclassification, see text)",
            dx=-60, dy=-2, ha="right")
    callout(a1, 2025, adds.loc[2025, "Tambopata NR"], f"2025: +{adds.loc[2025, 'Tambopata NR']:,.0f} ha\ninside Tambopata",
            dx=-56, dy=8, ha="right")
    a2.set_ylabel("ha per year")
    a2.set_title("Their buffer zones")
    a1.set_ylim(None, 600)
    for i, a in enumerate((a1, a2)):
        style_axes(a); add_event_markers(a, label=(i == 0))
    a2.set_xlim(Y0 + 0.4, 2027.4)                       # room on the right for the direct labels
    for a in (a1, a2):
        a.spines["bottom"].set_bounds(Y0 + 0.6, 2025.4)
    set_year_ticks(a2, yrs)
    finish_figure(fig, f"{SRC_FIG}. Same collection, so the panels are comparable. Description only. Mining area = all "
                       "mining (legal and illegal); river dredging and mercury are invisible.",
                  OUT / "fig_peru_inside_reserves.png", event_note=True)

    yrs2 = list(range(2014, 2026)); x2 = x_of(yrs2)
    fig, ax = plt.subplots(figsize=(9, 5.2))
    headline(fig, "Little of Tambopata's mining moved into the reserve, until 2025",
             "New mining area each year (annual addition, ha): Tambopata buffer zone and the reserve inside it, stacked")
    ax.bar(x2, comb.loc[yrs2, "Tambopata buffer zone"], color=C["lapampa"], width=0.72)
    ax.bar(x2, comb.loc[yrs2, "Tambopata NR (inside)"], bottom=comb.loc[yrs2, "Tambopata buffer zone"].clip(lower=0),
           color=C["reserve"], width=0.72, edgecolor="white", linewidth=0.8)
    ax.plot(x2, comb.loc[yrs2, "Tambopata BZ + NR"], color=INK, marker="o", markersize=4, mec="white", mew=0.8, linewidth=1.2)
    from matplotlib.patches import Patch
    from matplotlib.lines import Line2D
    ax.legend(handles=[Patch(color=C["lapampa"], label="Buffer zone"), Patch(color=C["reserve"], label="Inside the reserve"),
                       Line2D([], [], color=INK, marker="o", ms=4, lw=1.2, label="Sum")],
              loc="upper left", ncol=3, fontsize=8.5, handlelength=1.2)
    ax.set_ylim(None, ax.get_ylim()[1] * 1.12)
    ax.set_ylabel("ha per year")
    ax.set_title("Did mining move into the reserve?", pad=EVENT_TITLE_PAD)
    style_axes(ax); add_event_markers(ax, label=True)
    ax.set_xlim(2013.4, 2025.6); set_year_ticks(ax, yrs2)
    finish_figure(fig, f"{SRC_FIG}. Assumes the buffer zone excludes the reserve. Description only.",
                  OUT / "fig_peru_displacement_into_reserve.png", event_note=True)
    return dict(levels=levels, adds=adds, bz=bz, combined=comb, period_means=pm)
