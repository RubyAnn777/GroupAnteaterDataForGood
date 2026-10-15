"""Brazil case: weaker federal enforcement 2019-22, then the Yanomami operation (Feb 2023).

Three data sources, never mixed in one series (agent.md rule 7):
  * pack mining_area.csv            = MapBiomas Brazil Collection 11 (1985-2025), ALL indigenous lands combined,
                                      artisanal vs industrial, by substance.  -> context series
  * MapBiomas Brazil Collection 10.1, indigenous territories (xlsx in data_raw/)  = per territory, class 30
                                      "4.3 Mining" (all mining), 1985-2024.   -> Yanomami / Munduruku / Kayapo
  * pack brazil_municipality_year.csv = MapBiomas Brazil Collection 10.1 per municipality (to 2024).  -> displacement
Every claim is DESCRIPTION unless labelled otherwise; with one treated territory and 2 post years the DiD is
a descriptive contrast of means, not a causal estimate (no standard errors reported).
"""
from __future__ import annotations
import pandas as pd, numpy as np
import matplotlib.pyplot as plt
from common import ROOT, OUT, additions, period_mean, style_axes, finish_figure
import brazil_ibama
import checks

TI101 = ROOT / "data_raw/mapbiomas_brazil/MAPBIOMAS_BRAZIL-COVERAGE_STATISTICS-COL.10.1-INDIGENOUS_TERRITORIES_STATE_BIOME.xlsx"
TI10 = ROOT / "data_raw/mapbiomas_brazil/MAPBIOMAS_BRAZIL-COL.10-INDIGENOUS_TERRITORIES_STATE_BIOME_DOI.xlsx"
SHEET = "COVERAGE_INDIGENOUS_TERRITORIES"
YAN, MUN, KAY = 50901, 29801, 23001
BIG3 = [YAN, MUN, KAY]
PRE, POST = (2020, 2022), (2023, 2024)
SRC101 = "MapBiomas Brazil, Collection 10.1, Indigenous Territories (class 4.3 Mining, all mining)"
SRC11 = "MapBiomas Brazil, Collection 11, all indigenous lands combined (artisanal mining)"
SRCMUN = "MapBiomas Brazil, Collection 10.1, municipalities (class 4.3 Mining, all mining)"
SRCIB = "IBAMA open data, autos de infracao (non-cancelled), Legal Amazon states"

C_YAN, C_MUN, C_KAY, C_GREY = "#B03A2E", "#2E6F9E", "#7A5C1E", "#555555"

CHECKS: list[dict] = []
def bcheck(label, value, expected, tol=1.0):
    ok = abs(value - expected) < tol
    print(f"{'OK  ' if ok else 'FAIL'} {label:78s} {value:>12,.1f}   (expected: {expected:,.1f})")
    CHECKS.append(dict(label=label, value=value, expected=expected, ok=ok, kind="numeric"))
    if not ok:
        raise AssertionError(label)

# ------------------------------------------------------------------ events (local marker, same style as common)
# Convention: the addition of year t is drawn at x = t; an event in year Y is drawn at x = Y - 0.5.
BR_EVENTS = [
    (2019, "Jan 2019: federal government change;\n2019-22: weaker federal enforcement (see sources)", "#7F8C8D", 0.97),
    (2023, "Jan 2023 Yanomami emergency (20 Jan); Feb 2023 Yanomami operation;\nAug 2023 Munduruku operation", "#B03A2E", 0.97),
    (2024, "Nov 2024:\nMunduruku\ndesintrusao", "#2E6F9E", 0.78),
    (2025, "May 2025:\nKayapo\ndesintrusao", "#7A5C1E", 0.78),
]
def add_br_events(ax, last_year, label=False):
    for Y, text, col, ypos in BR_EVENTS:
        if Y > last_year:
            continue
        ax.axvline(Y - 0.5, color=col, linestyle="--", linewidth=0.9, alpha=0.85, zorder=0)
        if label:
            ax.annotate(text, xy=(Y - 0.5, ypos), xycoords=("data", "axes fraction"), xytext=(3, 0),
                        textcoords="offset points", fontsize=6.3, color=col, va="top", ha="left")

def events_legend(fig, last_year, y=0.085):
    """Event key as a figure-level legend (labels on the axes collided: several 2023 events share one x)."""
    from matplotlib.lines import Line2D
    keys = {2019: "Jan 2019 federal government change; 2019-22: weaker federal enforcement (see sources)",
            2023: "2023: Yanomami emergency (20 Jan), Yanomami operation (Feb), Munduruku operation (Aug)",
            2024: "Nov 2024: Munduruku desintrusao", 2025: "May 2025: Kayapo desintrusao"}
    hs = [Line2D([0], [0], color=c, ls="--", lw=1.1) for Y, _, c, _ in BR_EVENTS if Y <= last_year]
    ls = [keys[Y] for Y, _, _, _ in BR_EVENTS if Y <= last_year]
    fig.legend(hs, ls, loc="lower center", bbox_to_anchor=(0.5, y), ncol=1, frameon=False, fontsize=7.3,
               title="Dashed lines (drawn between the year before and the year of the event)", title_fontsize=7.3)

def year_axis(ax, y0, y1):
    ax.set_xticks(range(y0, y1 + 1)); ax.set_xticklabels([str(y) for y in range(y0, y1 + 1)], fontsize=8)
    ax.set_xlim(y0 - 0.6, y1 + 0.6)

# ------------------------------------------------------------------ data
def load_ti(path=TI101) -> pd.DataFrame:
    d = pd.read_excel(path, sheet_name=SHEET)
    d = d[d["class_id"] == 30].copy()
    if "geocode" not in d.columns:      # the Collection 10 sibling file has no geocode column: take it from "Name (code)"
        d["geocode"] = d["indigenous_territories"].str.extract(r"\((\d+)\)\s*$")[0].astype(int)
    return d

def ti_levels(m: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    """Class-30 rows -> wide (year x geocode), SUMMED across state/biome rows per territory (rule 2)."""
    ycols = [c for c in m.columns if isinstance(c, (int, np.integer))]
    names = {int(g): n.rsplit(" (", 1)[0] for g, n in zip(m["geocode"], m["indigenous_territories"])}
    w = m.groupby("geocode")[ycols].sum().T
    w.index = w.index.astype(int); w.columns = w.columns.astype(int)
    return w, names

def adds_of(level: pd.Series) -> pd.Series:
    """First difference with consecutive-year safety (reuses common.additions)."""
    d = pd.DataFrame({"year": level.index.astype(int), "v": level.values, "unit": "u"})
    return additions(d, "unit", "v").set_index("year")["addition_ha"]

def group_adds(w, codes):
    return adds_of(w[list(codes)].sum(axis=1)), w[list(codes)].sum(axis=1)

def group_adds_mean(w, codes):
    """Per-unit MEAN of the controls (same scale as one treated unit), additions and stock."""
    m = w[list(codes)].mean(axis=1)
    return adds_of(m), m

SUM_SPECS = {"vs_Munduruku+Kayapo_pooled", "vs_other_top5_by_2022_stock", "vs_all_19_other_territories"}

# ------------------------------------------------------------------ DiD (descriptive)
def did_row(spec, tname, cname, t_add, c_add, t_stock, c_stock, pre=PRE, post=POST, note="", claim="description"):
    tp0, tp1 = period_mean(t_add, *pre), period_mean(t_add, *post)
    cp0, cp1 = period_mean(c_add, *pre), period_mean(c_add, *post)
    out = dict(spec=spec, treated=tname, control=cname, pre=f"{pre[0]}-{pre[1]}", post=f"{post[0]}-{post[1]}",
               treated_pre_ha_yr=tp0, treated_post_ha_yr=tp1, control_pre_ha_yr=cp0, control_post_ha_yr=cp1,
               DiD_ha_yr=(tp1 - tp0) - (cp1 - cp0))
    # relative: additions as % of each group's 2022 stock (stock of the year before the post period)
    ts, cs = t_stock.loc[2022], c_stock.loc[2022]
    out["DiD_pct_of_2022_stock"] = 100 * ((tp1 - tp0) / ts - (cp1 - cp0) / cs)
    out["treated_pre_pct"], out["treated_post_pct"] = 100 * tp0 / ts, 100 * tp1 / ts
    out["control_pre_pct"], out["control_post_pct"] = 100 * cp0 / cs, 100 * cp1 / cs
    out["claim_type"] = claim; out["note"] = note
    return out

# ------------------------------------------------------------------ main
def run(pack, reg):
    print("\n== Brazil ==")
    out = {}
    sub, br = pack["substance"], pack["br"]

    # ---- 1. pack, Collection 11: all indigenous lands combined --------------------------------------
    ti = sub[sub["territory"] == "all indigenous lands combined"].set_index("year").sort_index()
    bcheck("Brazil, all indigenous lands, artisanal mining, 2025, ha (pack C11; card 39,915)", ti.loc[2025, "mining_artisanal_ha"], 39915)
    bcheck("Brazil, all indigenous lands, artisanal mining, 2018, ha (pack C11; brief 13,704)", ti.loc[2018, "mining_artisanal_ha"], 13704)
    bcheck("Brazil, all indigenous lands, artisanal mining, 2022, ha (pack C11; brief 30,980)", ti.loc[2022, "mining_artisanal_ha"], 30980)
    pk = {}
    for col, tag, lab in [("mining_artisanal_ha", "art", "artisanal mining"),
                          ("gold_or_nosub_artisanal_ha", "gns", "artisanal gold-or-no-substance (working measure of illegal gold)")]:
        a = additions(ti.reset_index().assign(unit="all"), "unit", col).set_index("year")["addition_ha"]
        pk[tag] = a
        for (y0, y1) in [(2016, 2018), (2019, 2022), (2023, 2025)]:
            reg.add(f"br_pack_{tag}_add_mean_{y0}_{y1}", period_mean(a, y0, y1), "ha/yr",
                    f"Mean annual addition, {lab}, all indigenous lands combined, {y0}-{y1} ({SRC11})",
                    "description", "data/mining_area.csv")
        for y in (2018, 2022, 2025):
            reg.add(f"br_pack_{tag}_level_{y}", ti.loc[y, col], "ha", f"Level, {lab}, all indigenous lands, {y}",
                    "description", "data/mining_area.csv")
    pd.DataFrame({"year": range(2014, 2026),
                  "artisanal_level_ha": [ti.loc[y, "mining_artisanal_ha"] for y in range(2014, 2026)],
                  "artisanal_addition_ha": [pk["art"][y] for y in range(2014, 2026)],
                  "gold_or_nosub_artisanal_level_ha": [ti.loc[y, "gold_or_nosub_artisanal_ha"] for y in range(2014, 2026)],
                  "gold_or_nosub_artisanal_addition_ha": [pk["gns"][y] for y in range(2014, 2026)],
                  "collection": "MapBiomas Brazil Collection 11"}).to_csv(OUT / "brazil_pack_all_ti_additions.csv", index=False)

    # ---- 2. Collection 10.1 per territory -------------------------------------------------------------
    m = load_ti()
    w, names = ti_levels(m)
    assert w.index.min() == 1985 and w.index.max() == 2024 and len(w.columns) == 22
    bcheck("Kayapo, mining class, 2024, ha (Col 10.1 file; rounds to 18,176)", w.loc[2024, KAY], 18176, tol=0.5)
    bcheck("Yanomami (RR rows summed; AM row has no mining row), 2022, ha (Col 10.1)", w.loc[2022, YAN], 3573, tol=0.5)
    # sibling Collection 10 file (consistency check, same publisher; NOT mixed into any series)
    if TI10.exists():
        w10, _ = ti_levels(load_ti(TI10))
        yrs = [y for y in range(1985, 2025) if y in w10.index and y in w.index]
        worst = worst_all = 0.0
        for code in (YAN, MUN, KAY):
            rel = ((w10.loc[yrs, code] - w.loc[yrs, code]).abs() / w.loc[yrs, code].replace(0, np.nan)).dropna()
            worst_all = max(worst_all, float(rel[rel.index >= 2014].max()))
            rel = rel[rel.index >= 2018]
            worst = max(worst, float(rel.max()))
        print(f"{'OK  ' if worst < 0.001 else 'FAIL'} Collection 10 sibling file vs 10.1, Yanomami/Munduruku/Kayapo 2018-{max(yrs)}: max relative diff {100*worst:.4f}%  (2014-17 differ by up to {100*worst_all:.2f}%, small stocks)")
        CHECKS.append(dict(label="Col 10 sibling file vs Col 10.1 per territory (max rel diff, 2018-2024)", value=worst, expected=0.001, ok=worst < 0.001, kind="consistency"))
        reg.add("br_col10_vs_col101_max_rel_diff_2014_17_pct", 100 * worst_all, "%", "Max relative difference Col 10 vs Col 10.1, three territories, 2014-2024 (driven by Yanomami 2014-16)", "description", "data_raw/mapbiomas_brazil (two xlsx)")
        assert worst < 0.001, "Collection 10 and 10.1 disagree by more than 0.1%"
        reg.add("br_col10_vs_col101_max_rel_diff_pct", 100 * worst, "%", "Max relative difference Col 10 vs Col 10.1, three territories, 2018-2024 (2014-17: larger, up to 2% for Yanomami)", "description", "data_raw/mapbiomas_brazil (two xlsx)")
    else:
        print("note: Collection 10 sibling file not found; consistency check skipped")
    # Publisher-side comparison for the per-territory file (platform read 2026-10-10 is Collection 11, the file is Col 10.1)
    CHECKS.append(dict(label="Kayapo 2024: file Col 10.1 = 18,176 ha; platform Col 11 = 17,632 ha (2026-10-10): collection difference",
                       value=float(w.loc[2024, KAY]), expected=17632, ok="MISMATCH-documented", kind="publisher (not asserted)"))
    checks.check_documented("Kayapo 2024 mining, ha: file Col 10.1 vs platform Col 11 (2026-10-10), collection difference, not asserted",
                            float(w.loc[2024, KAY]), 17632, "MISMATCH-documented")
    checks.save()

    A, STK = {}, {}
    for c in w.columns:
        A[int(c)], STK[int(c)] = adds_of(w[c]), w[c]
    others = [c for c in w.columns if c not in BIG3]
    top_other = list(w.loc[2022, others].sort_values(ascending=False).index[:5])
    nm = lambda cs: " + ".join(names[c] for c in cs)

    # per territory table (all 22) ---------------------------------------------------------------------
    tab = pd.DataFrame({names[c]: A[c] for c in w.columns}).loc[2014:2024].T
    tab.insert(0, "stock_2022_ha", [w.loc[2022, c] for c in w.columns]); tab.insert(1, "stock_2024_ha", [w.loc[2024, c] for c in w.columns])
    tab.insert(0, "geocode", list(w.columns))
    tab.sort_values("stock_2022_ha", ascending=False).round(2).to_csv(OUT / "brazil_ti_additions_all22.csv")
    # three focus territories: period means
    rows = []
    for c in BIG3:
        r = dict(territory=names[c], geocode=c)
        for (y0, y1) in [(2016, 2018), (2019, 2022), (2020, 2022), (2023, 2024)]:
            v = period_mean(A[c], y0, y1); r[f"mean_add_{y0}_{y1}"] = v
            reg.add(f"br_ti_{names[c].lower().replace('ó','o')}_add_mean_{y0}_{y1}", v, "ha/yr",
                    f"Mean annual addition in {names[c]} TI, {y0}-{y1} ({SRC101})", "description", TI101.name)
        r["stock_2022"] = w.loc[2022, c]; r["stock_2024"] = w.loc[2024, c]
        rows.append(r)
    pd.DataFrame(rows).round(2).to_csv(OUT / "brazil_ti_period_means.csv", index=False)
    for c in BIG3:
        k = names[c].lower().replace("ó", "o")
        reg.add(f"br_ti_{k}_stock_2022", w.loc[2022, c], "ha", f"Mining stock {names[c]} 2022 ({SRC101})", "description", TI101.name)
        reg.add(f"br_ti_{k}_stock_2024", w.loc[2024, c], "ha", f"Mining stock {names[c]} 2024 ({SRC101})", "description", TI101.name)
        for y in (2022, 2023, 2024):
            reg.add(f"br_ti_{k}_add_{y}", A[c][y], "ha", f"Addition {names[c]} {y} ({SRC101})", "description", TI101.name)

    # DiD specs ------------------------------------------------------------------------------------------
    Yd, Ys = A[YAN], STK[YAN]
    Mc, Kc = A[MUN], A[KAY]
    MK_a, MK_s = group_adds(w, [MUN, KAY])
    O19_a, O19_s = group_adds(w, others)
    T5_a, T5_s = group_adds(w, top_other)
    R = []
    R.append(did_row("main_vs_Munduruku", "Yanomami", "Munduruku", Yd, Mc, Ys, STK[MUN],
                     note="Munduruku had its own operation from Aug 2023 and desintrusao Nov 2024 (partly treated): contrast of more vs less enforcement"))
    R.append(did_row("main_vs_Kayapo", "Yanomami", "Kayapo", Yd, Kc, Ys, STK[KAY],
                     note="Best control 2023-24 (one PF action Jun 2023; desintrusao only May 2025)"))
    R.append(did_row("vs_Munduruku+Kayapo_pooled", "Yanomami", "Munduruku + Kayapo (pooled)", Yd, MK_a, Ys, MK_s,
                     note="Pooled control is dominated by Kayapo (about 2/3 of the stock)"))
    MKm_a, MKm_s = group_adds_mean(w, [MUN, KAY])
    O19m_a, O19m_s = group_adds_mean(w, others)
    R.append(did_row("vs_Munduruku_Kayapo_mean", "Yanomami", "Munduruku and Kayapo (per-unit mean)", Yd, MKm_a, Ys, MKm_s,
                     note="Control = equal-weight MEAN of the two territories (same scale as the treated unit)"))
    R.append(did_row("vs_all_19_other_mean", "Yanomami", "19 other territories (per-unit mean)", Yd, O19m_a, Ys, O19m_s,
                     note="Control = equal-weight MEAN of the 19 other territories with mining rows (Sarare drives most of the 2023-24 rise)"))
    R.append(did_row("drop_Kayapo_from_pool", "Yanomami", "Munduruku only", Yd, Mc, Ys, STK[MUN],
                     note="Same as main_vs_Munduruku: dropping the largest unit (Kayapo) from the pooled control leaves Munduruku"))
    R.append(did_row("drop_Munduruku_from_pool", "Yanomami", "Kayapo only", Yd, Kc, Ys, STK[KAY],
                     note="Same as main_vs_Kayapo: dropping Munduruku (partly treated) from the pooled control leaves Kayapo"))
    R.append(did_row("vs_other_top5_by_2022_stock", "Yanomami", nm(top_other), Yd, T5_a, Ys, T5_s,
                     note="Other high-mining territories, all tiny (stock 2022 < 1,200 ha each); Sarare grows fast in 2023-24 (+800 ha)"))
    R.append(did_row("vs_all_19_other_territories", "Yanomami", "19 other territories with mining rows", Yd, O19_a, Ys, O19_s,
                     note="All other territories with a class-30 row; Tenharim do Igarape Preto is the largest"))
    R.append(did_row("Munduruku_vs_Kayapo", "Munduruku", "Kayapo", Mc, Kc, STK[MUN], STK[KAY],
                     note="Munduruku treated from Aug 2023 (operation) / Nov 2024 (desintrusao): partial treatment, reading is descriptive"))
    R.append(did_row("persistence_2023_only", "Yanomami", "Kayapo", Yd, Kc, Ys, STK[KAY], post=(2023, 2023),
                     note="First post year only"))
    R.append(did_row("persistence_2024_only", "Yanomami", "Kayapo", Yd, Kc, Ys, STK[KAY], post=(2024, 2024),
                     note="Second post year only"))
    R.append(did_row("placebo_time_start_2020", "Yanomami", "Kayapo", Yd, Kc, Ys, STK[KAY], pre=(2017, 2019), post=(2020, 2022),
                     note="Pseudo-operation 3 years earlier; a non-zero value means pre-trends are not parallel (Yanomami boom 2019-22)"))
    R[-1]["claim_type"] = "description"
    # relative stock for placebo uses 2022 stock too (same normaliser) -> keep, flagged in note
    rob = pd.DataFrame(R)
    rob.round(3).to_csv(OUT / "brazil_robustness.csv", index=False)
    rob.round(3).to_csv(OUT / "brazil_did.csv", index=False)
    print(rob[["spec", "treated_pre_ha_yr", "treated_post_ha_yr", "control_pre_ha_yr", "control_post_ha_yr", "DiD_ha_yr", "DiD_pct_of_2022_stock"]].round(1).to_string())
    for r in R:
        pre_txt = "SUM of controls (scale mismatch; do not cite): " if r["spec"] in SUM_SPECS else ""
        reg.add(f"br_did_{r['spec']}_ha_yr", r["DiD_ha_yr"], "ha/yr", f"{pre_txt}Descriptive DiD in mean annual additions: {r['treated']} vs {r['control']}, {r['pre']} -> {r['post']} ({SRC101})", "description", TI101.name)
        reg.add(f"br_did_{r['spec']}_pct", r["DiD_pct_of_2022_stock"], "pp of 2022 stock", f"{pre_txt}Same, additions as % of 2022 stock", "description", TI101.name)
    out["did"] = rob

    # ---- 3. displacement ---------------------------------------------------------------------------------
    b = br[(br["biome"] == "Amazônia")].copy()
    b = b[b.groupby(["state_acronym", "municipality"])["total_ha"].transform("max") >= 100]    # drop tiny border rows
    rr = b[b.state_acronym == "RR"]
    rr_lev = rr.groupby("year")["mining_ha"].sum()
    bcheck("Roraima, mining class, all Amazonia municipalities, 2018, ha (card 446)", rr_lev[2018], 446, tol=1)
    bcheck("Roraima, mining class, all Amazonia municipalities, 2024, ha (card 4,745)", rr_lev[2024], 4745, tol=1)
    rr_add = adds_of(rr_lev.loc[:2024])
    yan_munis = [("RR", "Alto Alegre"), ("RR", "Mucajaí"), ("RR", "Iracema"), ("RR", "Caracaraí"), ("RR", "Amajari"),
                 ("AM", "Barcelos"), ("AM", "Santa Isabel do Rio Negro"), ("AM", "São Gabriel da Cachoeira")]
    mt = []
    for st, mn in yan_munis:
        g = b[(b.state_acronym == st) & (b.municipality == mn)].set_index("year")["mining_ha"].sort_index()
        assert len(g) == 40, (st, mn, len(g))
        mt.append(dict(state=st, municipality=mn, stock_2018=g[2018], stock_2022=g[2022], stock_2024=g[2024],
                       add_mean_2020_22=period_mean(adds_of(g), 2020, 2022), add_mean_2023_24=period_mean(adds_of(g), 2023, 2024)))
    mt = pd.DataFrame(mt); mt.round(1).to_csv(OUT / "brazil_yanomami_municipalities.csv", index=False)
    print(mt.round(1).to_string())
    sel = rr[rr.municipality.isin([x[1] for x in yan_munis if x[0] == "RR"])].groupby("year")["mining_ha"].sum()
    rr_other = rr_lev - sel      # Roraima municipalities not listed
    ratio = (w[YAN].loc[2014:2024] / rr_lev.loc[2014:2024])
    pd.DataFrame({"year": range(2014, 2025), "roraima_level_ha": rr_lev.loc[2014:2024].values,
                  "roraima_addition_ha": rr_add.loc[2014:2024].values, "yanomami_ti_level_ha": w[YAN].loc[2014:2024].values,
                  "yanomami_ti_addition_ha": A[YAN].loc[2014:2024].values,
                  "roraima_minus_yanomami_ti_level_ha": (rr_lev.loc[2014:2024] - w[YAN].loc[2014:2024]).values,
                  "collection": "MapBiomas Brazil Collection 10.1 (both columns)"}).round(2).to_csv(OUT / "brazil_roraima.csv", index=False)
    reg.add("br_rr_level_2018", rr_lev[2018], "ha", f"Roraima mining stock 2018, all Amazonia municipalities ({SRCMUN})", "description", "data/brazil_municipality_year.csv")
    reg.add("br_rr_level_2024", rr_lev[2024], "ha", f"Roraima mining stock 2024 ({SRCMUN})", "description", "data/brazil_municipality_year.csv")
    for (y0, y1) in [(2016, 2018), (2019, 2022), (2020, 2022), (2023, 2024)]:
        reg.add(f"br_rr_add_mean_{y0}_{y1}", period_mean(rr_add, y0, y1), "ha/yr", f"Roraima mean annual mining addition {y0}-{y1} ({SRCMUN})", "description", "data/brazil_municipality_year.csv")
    reg.add("br_rr_minus_yanomami_ti_2024", rr_lev[2024] - w.loc[2024, YAN], "ha",
            "Roraima municipal mining stock 2024 minus Yanomami TI stock 2024 (both Col 10.1): mining in Roraima outside the TI, plus land in the TI that lies in AM", "description", "pack + territory xlsx (Col 10.1)")
    reg.add("br_rr_yanomami_share_2024", 100 * w.loc[2024, YAN] / rr_lev[2024], "%", "Yanomami TI stock as share of Roraima municipal stock 2024", "description", "pack + territory xlsx (Col 10.1)")
    reg.add("br_rr_outside_yanomami_add_2023_24", float((rr_lev[2024] - w.loc[2024, YAN]) - (rr_lev[2022] - w.loc[2022, YAN])), "ha",
            "Change 2022 to 2024 in Roraima mining outside the Yanomami TI (Roraima stock minus TI stock)", "description", "pack + territory xlsx (Col 10.1)")

    # other territories excluding the big three -> did mining rise in 2023-24?
    o_add, o_stk = group_adds(w, others)
    for (y0, y1) in [(2016, 2018), (2019, 2022), (2020, 2022), (2023, 2024)]:
        reg.add(f"br_other19_add_mean_{y0}_{y1}", period_mean(o_add, y0, y1), "ha/yr", f"Mean annual addition, 19 other territories with mining, {y0}-{y1} ({SRC101})", "description", TI101.name)
    reg.add("br_other19_stock_2022", o_stk[2022], "ha", "Stock of 19 other territories 2022", "description", TI101.name)
    reg.add("br_other19_stock_2024", o_stk[2024], "ha", "Stock of 19 other territories 2024", "description", TI101.name)
    for c in [c for c in others if c in (42101, 44701, 12101)]:
        reg.add(f"br_ti_{c}_add_2023_24_sum", float(A[c][2023] + A[c][2024]), "ha", f"Sum of additions 2023+2024, {names[c]} ({SRC101})", "description", TI101.name)
    SAR = 42101
    print("Territory 42101 =", names[SAR])
    oex = [c for c in others if c != SAR]
    oex_a, _ = group_adds_mean(w, oex)
    for (y0, y1) in [(2020, 2022), (2023, 2024)]:
        reg.add(f"br_other18_ex_sarare_add_mean_{y0}_{y1}", period_mean(oex_a, y0, y1), "ha/yr",
                f"Per-unit MEAN annual addition of the {len(oex)} other territories with mining excluding {names[SAR]} (geocode 42101), {y0}-{y1}; "
                f"each territory's addition averaged over the group, then over years ({SRC101})", "description", TI101.name)
    reg.add("br_sarare_add_2023_24_sum", float(A[SAR][2023] + A[SAR][2024]), "ha",
            f"Sum of additions 2023+2024, {names[SAR]} (geocode 42101)", "description", TI101.name)
    big3_a, big3_s = group_adds(w, BIG3)
    all_a, all_s = group_adds(w, list(w.columns))
    reg.add("br_all22_stock_2022", all_s[2022], "ha", f"All 22 territories with mining, stock 2022 ({SRC101})", "description", TI101.name)
    reg.add("br_all22_stock_2024", all_s[2024], "ha", f"All 22 territories with mining, stock 2024 ({SRC101})", "description", TI101.name)
    disp = pd.DataFrame({"yanomami": A[YAN], "munduruku": A[MUN], "kayapo": A[KAY], "other19": o_add, "all22": all_a}).loc[2014:2024]
    disp["roraima_minus_yanomami_ti_addition"] = (rr_add - A[YAN]).loc[2014:2024]
    disp.round(2).to_csv(OUT / "brazil_displacement.csv"); print(disp.round(0).to_string())
    reg.add("br_all22_add_mean_2020_22", period_mean(all_a, 2020, 2022), "ha/yr", "All 22 territories: mean annual addition 2020-22 (Col 10.1)", "description", TI101.name)
    reg.add("br_all22_add_mean_2023_24", period_mean(all_a, 2023, 2024), "ha/yr", "All 22 territories: mean annual addition 2023-24 (Col 10.1); total fell vs 2020-22", "description", TI101.name)

    # ---- 4. IBAMA ---------------------------------------------------------------------------------------
    ib, how = brazil_ibama.load()
    ib = ib.set_index("year")
    for (y0, y1) in [(2015, 2018), (2019, 2022)]:
        reg.add(f"br_ibama_aml_mean_{y0}_{y1}", ib.loc[y0:y1, "n_legal_amazon_states"].mean(), "autos/yr", f"Mean IBAMA autos per year, Legal Amazon states, {y0}-{y1} ({SRCIB})", "description", "data_raw/ibama/auto_infracao_csv.zip")
        reg.add(f"br_ibama_mining_aml_mean_{y0}_{y1}", ib.loc[y0:y1, "n_mining_legal_amazon"].mean(), "autos/yr", f"Mean mining-flagged IBAMA autos (noisy regex), Legal Amazon, {y0}-{y1}", "description", "data_raw/ibama/auto_infracao_csv.zip")
    for y in (2018, 2020, 2022, 2023, 2024):
        reg.add(f"br_ibama_aml_{y}", ib.loc[y, "n_legal_amazon_states"], "autos", f"IBAMA autos, Legal Amazon states, {y}", "description", "data_raw/ibama/auto_infracao_csv.zip")
        reg.add(f"br_ibama_mining_aml_{y}", ib.loc[y, "n_mining_legal_amazon"], "autos", f"Mining-flagged IBAMA autos (noisy regex), Legal Amazon, {y}", "description", "data_raw/ibama/auto_infracao_csv.zip")
    fig_enforcement(ib, pk["art"], how)
    fig_territories(w, A, pk["art"], names)
    fig_roraima(rr_add, A, o_add, A[42101], float(rr_lev[2024] - w.loc[2024, YAN]))
    pd.DataFrame(CHECKS).to_csv(OUT / "brazil_checks.csv", index=False)
    out["checks"] = CHECKS
    return out

# ------------------------------------------------------------------ figures
def _line(ax, x, y, col, label, lw=1.8, marker="o"):
    ax.plot(x, y, color=col, lw=lw, marker=marker, ms=3.5, label=label)

def fig_territories(w, A, pk_art, names):
    yrs = list(range(2014, 2025))
    fig, ax = plt.subplots(3, 1, figsize=(9, 9.2), sharex=True)
    for c, col in [(KAY, C_KAY), (MUN, C_MUN), (YAN, C_YAN)]:
        _line(ax[0], yrs, A[c].loc[yrs], col, names[c])
        _line(ax[1], yrs, 100 * A[c].loc[yrs] / w.loc[2022, c], col, names[c])
    ax[0].set_ylabel("Net addition to mining area (ha/yr)")
    ax[0].set_title("Yanomami (operation from Feb 2023) vs Munduruku and Kayapo: annual additions to mining area", fontsize=10.5, loc="left")
    ax[0].legend(frameon=False, fontsize=8, loc="center left")
    ax[1].set_ylabel("Addition as % of the\nterritory's 2022 mining stock")
    ax[1].set_title("Same, scaled by each territory's own 2022 stock (sizes differ a lot)", fontsize=9, loc="left")
    y2 = list(range(2014, 2026))
    _line(ax[2], y2, pk_art.loc[y2], C_GREY, "all indigenous lands combined, artisanal (Collection 11)", marker="s")
    ax[2].set_ylabel("Net addition (ha/yr)")
    ax[2].set_title("Context (different collection and measure): ALL indigenous lands, artisanal mining", fontsize=9, loc="left")
    for a in ax:
        style_axes(a); a.axhline(0, color="#999999", lw=0.6)
    add_br_events(ax[0], 2025); add_br_events(ax[1], 2025); add_br_events(ax[2], 2025)
    events_legend(fig, 2025)
    year_axis(ax[2], 2014, 2025)
    ax[0].set_ylim(top=ax[0].get_ylim()[1] * 1.12)
    finish_figure(fig, f"Sources: top two panels {SRC101}, 2014-2024;\nbottom panel {SRC11}, 2014-2025. Description only; one treated territory, 2 post years.\n"
                       "MapBiomas class 'mining' cannot separate legal from illegal mining nor see river dredging.",
                  OUT / "fig_brazil_territories.png", rect_bottom=0.20)

def fig_roraima(rr_add, A, o_add, sarare, gap2024):
    yrs = list(range(2014, 2025))
    fig, ax = plt.subplots(2, 1, figsize=(9, 6.8), sharex=True)
    _line(ax[0], yrs, rr_add.loc[yrs], C_GREY, "Roraima, all Amazonia municipalities (municipal table)", marker="s")
    _line(ax[0], yrs, A[YAN].loc[yrs], C_YAN, "Yanomami territory (territory table)")
    ax[0].set_ylabel("Net addition (ha/yr)")
    ax[0].set_title("Displacement check 1: mining additions in Roraima vs the Yanomami territory", fontsize=10.5, loc="left")
    ax[0].legend(frameon=False, fontsize=8, loc="upper left")
    _line(ax[1], yrs, o_add.loc[yrs], C_MUN, "19 other territories with mining (excl. Yanomami, Munduruku, Kayapo)")
    _line(ax[1], yrs, sarare.loc[yrs], C_KAY, "of which Sarare (MT)", marker="^")
    ax[1].set_ylabel("Net addition (ha/yr)")
    ax[1].set_title("Displacement check 2: mining additions in the other territories", fontsize=10.5, loc="left")
    ax[1].legend(frameon=False, fontsize=8, loc="upper left")
    for a in ax:
        style_axes(a); a.axhline(0, color="#999999", lw=0.6)
    add_br_events(ax[0], 2024); add_br_events(ax[1], 2024)
    events_legend(fig, 2024)
    year_axis(ax[1], 2014, 2024)
    ax[0].set_ylim(top=ax[0].get_ylim()[1] * 1.15)
    finish_figure(fig, f"Sources: {SRCMUN};\n{SRC101}. Both Collection 10.1, 2014-2024.\n"
                       f"Description only. Municipal mining includes industrial mines and land outside the territory; Roraima minus Yanomami territory = {gap2024:,.0f} ha in 2024.",
                  OUT / "fig_brazil_roraima.png", rect_bottom=0.19)

def fig_enforcement(ib, pk_art, how):
    yrs = list(range(2014, 2026))
    fig, ax = plt.subplots(3, 1, figsize=(9, 8.8), sharex=True)
    _line(ax[0], yrs, ib.loc[yrs, "n_legal_amazon_states"], C_GREY, "all autos, Legal Amazon states")
    ax[0].set_ylabel("IBAMA autos per year"); ax[0].set_ylim(0, ax[0].get_ylim()[1] * 1.18)
    ax[0].set_title("Enforcement intensity (all IBAMA autos de infracao, Legal Amazon states)", fontsize=10.5, loc="left")
    _line(ax[1], yrs, ib.loc[yrs, "n_mining_legal_amazon"], C_YAN, "mining-flagged autos (noisy text match)")
    ax[1].set_ylabel("Mining-flagged autos per year"); ax[1].set_ylim(0, ax[1].get_ylim()[1] * 1.1)
    ax[1].set_title("Mining-flagged autos only (noisy text match on infraction wording)", fontsize=9, loc="left")
    _line(ax[2], yrs, pk_art.loc[yrs], C_MUN, "all indigenous lands, artisanal mining (Collection 11)", marker="s")
    ax[2].set_ylabel("Net addition (ha/yr)")
    ax[2].set_title("Outcome: annual additions to artisanal mining in ALL indigenous lands", fontsize=9, loc="left")
    for a in ax:
        style_axes(a)
    ax[2].axhline(0, color="#999999", lw=0.6)
    add_br_events(ax[0], 2025); add_br_events(ax[1], 2025); add_br_events(ax[2], 2025)
    events_legend(fig, 2025)
    year_axis(ax[2], 2014, 2025)
    finish_figure(fig, f"Sources: {SRCIB} (non-cancelled, by year of the auto);\n{SRC11}. Description only, no causal claim. IBAMA table: {how}.\n"
                       "Mining-flagged autos did not fall in 2019-22 (see numbers.csv); the general fall in autos is not mining-specific.",
                  OUT / "fig_brazil_enforcement.png", rect_bottom=0.19)
