"""Peru: declared (formal) gold production in Madre de Dios (BCRP, original source MINEM) next to the MapBiomas
mining-area level and its annual additions. Description only. The two sources are never combined (rule 6)."""
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from common import (ROOT, OUT, add_event_markers, style_axes, set_year_ticks, finish_figure,
                    SRC_MAPBIOMAS, EVENT_TITLE_PAD)

RAW = ROOT / "data_raw" / "bcrp"
ANNUAL_JSON = RAW / "bcrp_annual_gold_series_2001_2025.json"
MONTHLY_JSON = RAW / "bcrp_monthly_madre_de_dios_gold_2001_2025.json"
MDD_NAME = "Madre de Dios (grs.f)"                 # series: 'Oro - Madre de Dios (grs.f)', grams of fine gold
Y0, Y1 = 2010, 2025

def _series_index(cfg, needle):
    idx = [i for i, s in enumerate(cfg["config"]["series"]) if needle in s["name"]]
    assert len(idx) == 1, (needle, idx)
    return idx[0]

def load_bcrp():
    """Annual and monthly Madre de Dios gold production in tonnes of fine gold (published in grams)."""
    a = json.load(open(ANNUAL_JSON, encoding="utf-8"))
    i = _series_index(a, "Oro - Madre de Dios (grs.f)")
    ann = pd.DataFrame({"year": [int(p["name"]) for p in a["periods"]],
                        "grams": [float(p["values"][i]) for p in a["periods"]]})
    m = json.load(open(MONTHLY_JSON, encoding="utf-8"))
    j = _series_index(m, "Oro - Madre de Dios (grs.f)")
    mon = pd.DataFrame({"month": pd.to_datetime([p["name"] for p in m["periods"]], format="%b.%Y"),
                        "grams": [float(p["values"][j]) for p in m["periods"]]})
    mon["year"] = mon.month.dt.year
    for d in (ann, mon):
        d["tonnes"] = d.grams / 1e6
    return ann, mon

def run(pack, reg):
    ann, mon = load_bcrp()
    # check: the twelve monthly values sum to the published annual value (relative tolerance 1e-6)
    ms = mon.groupby("year").grams.sum()
    cmp = ann.set_index("year").grams.to_frame("annual").join(ms.rename("monthly_sum"))
    cmp["rel_diff"] = (cmp.monthly_sum - cmp.annual) / cmp.annual.replace(0, np.nan)
    bad = cmp[(cmp.monthly_sum - cmp.annual).abs() > 1e-6 * cmp.annual.abs().clip(lower=1) + 1.0]
    assert bad.empty, f"BCRP monthly sums differ from annual:\n{bad}"
    print(f"BCRP check OK: monthly sum = annual for {len(cmp)} years (2001-2025)")

    ann = ann[ann.year.between(Y0, Y1)].reset_index(drop=True)
    mon[mon.year.between(Y0, Y1)].to_csv(OUT / "peru_production_mdd_monthly.csv", index=False)

    # MapBiomas level and additions, Madre de Dios, Amazonía biome (rules 2 and 4: one row per year first)
    pe = pack["pe"]
    lev = (pe[(pe.department == "Madre de Dios") & (pe.biome == "Amazonía")]
           .groupby("year").mining_ha.sum().sort_index())
    add = lev.diff()
    t = ann.set_index("year")[["tonnes"]].join(lev.rename("mapbiomas_mining_ha")).join(add.rename("mapbiomas_addition_ha"))
    t.loc[:, "tonnes"] = t.tonnes.round(4)
    t.to_csv(OUT / "peru_production_vs_area.csv")      # side by side, never a ratio or difference

    src = "BCRP series RD15556DA (original source MINEM)"
    tn = t.tonnes
    reg.add("pe_prod_2011_t", tn[2011], "t fine gold", "Declared gold production, Madre de Dios, 2011 (peak year of the series 2010-2025)", "description", src)
    reg.add("pe_prod_2016_t", tn[2016], "t fine gold", "Declared gold production, Madre de Dios, 2016", "description", src)
    reg.add("pe_prod_2018_t", tn[2018], "t fine gold", "Declared gold production, Madre de Dios, 2018 (year before Mercurio)", "description", src)
    reg.add("pe_prod_2019_t", tn[2019], "t fine gold", "Declared gold production, Madre de Dios, 2019", "description", src)
    reg.add("pe_prod_2020_t", tn[2020], "t fine gold", "Declared gold production, Madre de Dios, 2020", "description", src)
    reg.add("pe_prod_2025_t", tn[2025], "t fine gold", "Declared gold production, Madre de Dios, 2025", "description", src)
    reg.add("pe_prod_mean_2016_18_t", tn.loc[2016:2018].mean(), "t fine gold/yr", "Mean declared gold production 2016-18", "description", src)
    reg.add("pe_prod_mean_2022_25_t", tn.loc[2022:2025].mean(), "t fine gold/yr", "Mean declared gold production 2022-25", "description", src)
    reg.add("pe_prod_change_2018_2025_pct", 100 * (tn[2025] / tn[2018] - 1), "%",
            "Change in declared production 2018 to 2025 (within one source; not compared with area)", "description", src)
    reg.add("pe_prod_fall_2018_2025_pct", -100 * (tn[2025] / tn[2018] - 1), "%", "Fall in declared production 2018 to 2025, as a positive percentage", "description", src)
    reg.add("pe_prod_fall_2019_2020_pct", -100 * (tn[2020] / tn[2019] - 1), "%", "Fall in declared production 2019 to 2020 (COVID year), as a positive percentage", "description", src)
    reg.add("pe_prod_2017_t", tn[2017], "t fine gold", "Declared gold production, Madre de Dios, 2017", "description", src)
    reg.add("pe_prod_mapbiomas_level_2018_ha", t.mapbiomas_mining_ha[2018], "ha", "MapBiomas mining area level, Madre de Dios (Amazonía), 2018", "description", SRC_MAPBIOMAS)
    reg.add("pe_prod_mapbiomas_level_2025_ha", t.mapbiomas_mining_ha[2025], "ha", "MapBiomas mining area level, Madre de Dios (Amazonía), 2025 (matches 112,622 ha check)", "description", SRC_MAPBIOMAS)

    # ------------------------------------------------------------------ figure: 3 stacked panels, shared x, no dual axis
    yrs = t.index.to_numpy(float)
    fig, axs = plt.subplots(3, 1, figsize=(8, 8.6), sharex=True)
    c1, c2, c3 = "#B8860B", "#1F6F8B", "#1F6F8B"
    axs[0].plot(yrs, t.tonnes, marker="o", color=c1, lw=1.8)
    axs[0].set_ylabel("t of fine gold")
    axs[0].set_title("Declared (formal) gold production, Madre de Dios", loc="left", fontsize=10, pad=EVENT_TITLE_PAD)
    axs[1].plot(yrs, t.mapbiomas_mining_ha, marker="o", color=c2, lw=1.8)
    axs[1].set_ylabel("hectares")
    axs[1].set_title("Mapped mining area (level), Madre de Dios", loc="left", fontsize=10)
    axs[2].bar(yrs, t.mapbiomas_addition_ha, color=c3, width=0.7)
    axs[2].axhline(0, color="#888888", lw=0.6)
    axs[2].set_ylabel("ha per year")
    axs[2].set_title("Mapped mining area, annual additions", loc="left", fontsize=10)
    for k, ax in enumerate(axs):
        style_axes(ax)
        ax.set_xlim(Y0 - 0.6, Y1 + 0.6)
        add_event_markers(ax, label=(k == 0))
    set_year_ticks(axs[2], t.index)
    src_txt = ("Sources: BCRP series RD15556DA, 'Producción de productos mineros según departamentos: Oro - Madre de Dios (grs.f)', "
               "original source MINEM (grams of fine gold shown as tonnes); " + SRC_MAPBIOMAS + ", Amazonía biome. "
               "Description only. Production is FORMAL (declared) output; a fall in it while mapped area rises is consistent with more "
               "undeclared output, but also with changes in reporting or formalisation rules (e.g. the REINFO register). Two different "
               "publishers measuring different things: no ratio or difference is computed across them.")
    finish_figure(fig, src_txt, OUT / "fig_peru_production_vs_area.png", event_note=True)
