"""Rule-based comparison area for Tambopata (Ruby's design): find ONE existing area that is a fair 'what if' for La Pampa.

The four rules, applied in order to every protected area, buffer zone and indigenous territory in the Amazon we have
polygons for (SERNANP Peru, RAISG for the other countries and Brazil's conservation units, FUNAI territories):
  R1  Mining before 2019:  Amazon Mining Watch (AMW) detected at least MIN_STOCK ha of mining scars by 2018.
  R2  No operation:        no enforcement operation against mining reported 2017-2025 in our documented searches
                           (data_intermediate/operations_coded.csv; 'unclear' and 'not searched' fail).
                           Relaxed version (R2b): no operation reported 2017-2021, i.e. during Mercurio's own years.
  R3  Far enough away:     outside Madre de Dios (rules out the nearby areas MAAP shows received miners).
  R4  Geographic twin:     lowland mining like La Pampa (median elevation of the area's mining < MAX_ELEV m) AND a similar
                           scale (2018 mining at least MIN_SCALE x Tambopata's); survivors are ranked by distance to
                           Tambopata on elevation and on size of mining in 2018 (both on a log scale); best = chosen.
Then compare Tambopata with the chosen area on the SAME measure (AMW new mining per year as % of the 2018 stock).
AMW starts in 2018, so there is no pre-2019 trend in this comparison; pre-2019 trends are shown from MapBiomas, each area
from its own collection (Peru Col 4 / Amazonía Col 6), side by side, never subtracted (agent.md rules 6-7).
All results are DESCRIPTION.
"""
from __future__ import annotations
import warnings
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

from common import (ROOT, OUT, style_axes, finish_figure, headline, label_end, callout, period_band, C, INK, INK2,
                    MUTED, GRID, AXIS, SURFACE)

INTER = ROOT / "data_intermediate"
TU = "PE-BZ-RN09"                         # Tambopata buffer zone (treated)
AMARAKAERI = "PE-BZ-RC03"
MDD_BOX = (-72.6, -14.6, -68.6, -10.5)    # lon/lat box around Madre de Dios (same as spatial.py)
MIN_STOCK, MAX_ELEV, MIN_SCALE = 500.0, 500.0, 0.2
SRC = ("Amazon Mining Watch (AMW) x SERNANP / RAISG / FUNAI polygons; SRTM 90 m elevation (OpenTopoData); "
       "operations: data_intermediate/operations_coded.csv")
YRS = list(range(2019, 2026))


def load():
    u = pd.read_csv(INTER / "amw_candidates_units.csv").set_index("unit_id")
    w = pd.read_csv(INTER / "amw_candidates_year.csv").pivot(index="unit_id", columns="year", values="new_ha")
    e = pd.read_csv(INTER / "amw_candidates_elevation.csv").set_index("unit_id")
    ops = pd.read_csv(INTER / "operations_coded.csv").set_index("unit_id")
    assert ops.index.is_unique
    return u, w, e, ops


def funnel(u, w, e, ops) -> pd.DataFrame:
    t = u.join(w[[2018]].rename(columns={2018: "stock_2018"}), how="inner").join(e[["elev_median_m"]])
    t = t.drop(index=TU)
    v = ops["verdict_2017_2025"].reindex(t.index).fillna("not searched")
    first = ops["first_op_2017_2025"].reindex(t.index).fillna("")
    t["verdict"] = v; t["first_op"] = first
    t["r1_mining"] = t.stock_2018 >= MIN_STOCK
    t["r2_no_op"] = t.verdict.eq("none")
    t["r2b_no_op_2017_21"] = t.r2_no_op | (t.verdict.eq("yes") & (t.first_op >= "2022"))
    in_mdd = t.lon.between(MDD_BOX[0], MDD_BOX[2]) & t.lat.between(MDD_BOX[1], MDD_BOX[3]) & t.country.eq("Peru")
    t["r3_outside_mdd"] = ~in_mdd
    t["r4_lowland"] = (t.elev_median_m < MAX_ELEV) & (t.stock_2018 >= MIN_SCALE * w.loc[TU, 2018])
    tam = (u.loc[TU], w.loc[TU, 2018], e.loc[TU, "elev_median_m"])
    t["fit_distance"] = (np.abs(np.log(t.elev_median_m.clip(lower=20) / tam[2])) + np.abs(np.log(t.stock_2018 / tam[1])))
    t["pass_strict"] = t.r1_mining & t.r2_no_op & t.r3_outside_mdd & t.r4_lowland
    t["pass_relaxed"] = t.r1_mining & t.r2b_no_op_2017_21 & t.r3_outside_mdd & t.r4_lowland
    return t.sort_values("fit_distance")


def shares(w, ids):
    s = w.loc[ids, YRS].sum() / w.loc[ids, 2018].sum() * 100
    return s


def compare(w, ids, label):
    s, t = shares(w, ids), shares(w, [TU])
    d = dict(control=label, tam_during=t.loc[2019:2021].mean(), tam_after=t.loc[2022:2025].mean(),
             ctl_during=s.loc[2019:2021].mean(), ctl_after=s.loc[2022:2025].mean())
    d["rebound_gap"] = (d["tam_after"] - d["tam_during"]) - (d["ctl_after"] - d["ctl_during"])
    d["during_gap"] = d["tam_during"] - d["ctl_during"]
    return d


def fig_funnel(t, n_all):
    steps = [("All protected areas, buffer zones and\nindigenous territories with polygons", n_all),
             ("R1  had mining before 2019 (≥ 500 ha)", int(t.r1_mining.sum())),
             ("R2  + no operation found, 2017–25", int((t.r1_mining & t.r2_no_op).sum())),
             ("R3  + outside Madre de Dios", int((t.r1_mining & t.r2_no_op & t.r3_outside_mdd).sum())),
             ("R4  + lowland and similar scale", int(t.pass_strict.sum()))]
    names = t[t.pass_strict].name.tolist()
    rel = t[t.pass_relaxed & ~t.pass_strict].name.tolist()
    fig, ax = plt.subplots(figsize=(9, 4.0))
    headline(fig, "No area in the Amazon passes all four rules" if not names else
             f"Only {len(names)} area(s) in the Amazon pass all four rules",
             "Areas left after each rule (log scale). Rules applied in order to find a fair ‘what if’ for La Pampa.")
    for i, (lab, n) in enumerate(steps):
        last = i == len(steps) - 1
        ax.barh(-i, max(n, 0.0), color=C["twin"] if last else C["other"], height=0.6)
        ax.annotate(f"{n:,}", xy=(max(n, 1) if n else 0.02, -i), xytext=(6, 0), textcoords="offset points",
                    va="center", ha="left", fontsize=10, fontweight="bold", color=INK)
    ax.set_yticks([-i for i in range(len(steps))]); ax.set_yticklabels([s_[0] for s_ in steps], fontsize=9, color=INK)
    ax.set_xscale("symlog", linthresh=1); ax.set_xlim(0, n_all * 4)
    ax.set_xticks([]); ax.tick_params(axis="both", length=0); ax.xaxis.set_minor_locator(plt.NullLocator())
    for sp in ("top", "right", "bottom", "left"): ax.spines[sp].set_visible(False)
    ax.text(0.99, 0.02, f"If operations after 2021 are allowed (R2b), {len(rel)} pass:\n" + ("\n".join(rel[:6]) if rel else "none"),
            transform=ax.transAxes, ha="right", va="bottom", fontsize=8.5, color=INK2, linespacing=1.4)
    note = "Survivors of all four rules: " + (", ".join(names) if names else "none") + "."
    finish_figure(fig, f"Sources: {SRC}. {note} Description.", OUT / "fig_control_funnel.png")


def fig_map(t, u, w, chosen):
    import geopandas as gpd
    fig, ax = plt.subplots(figsize=(9, 7.6))
    headline(fig, "The twin candidates sit far from La Pampa, in Brazil",
             "Areas with ≥ 500 ha of mining by 2018 (dot area = hectares, Amazon Mining Watch), by operation status")
    base = ROOT / "data_raw" / "raisg"
    parts = sorted(base.glob("anp_nacionales_part*.geojson"))
    if parts:
        g = pd.concat([gpd.read_file(p)[["geometry"]] for p in parts])
        gpd.GeoDataFrame(g, crs=4326).plot(ax=ax, color="#dfeadb", edgecolor="#c9d6c4", lw=0.2, zorder=0)
    pal = {"passes all rules": C["corridor"], "passes if post-2021 operations allowed": C["twin"],
           "operation reported": C["lapampa_tint"], "unclear / not searched": C["other"]}
    def cls(r):
        if r.pass_strict: return "passes all rules"
        if r.pass_relaxed: return "passes if post-2021 operations allowed"
        if r.verdict == "yes": return "operation reported"
        return "unclear / not searched"
    m = t[t.r1_mining].copy(); m["cls"] = m.apply(cls, axis=1)
    order = ["unclear / not searched", "operation reported", "passes all rules", "passes if post-2021 operations allowed"]
    for c in order:
        d = m[m.cls == c]
        ax.scatter(d.lon, d.lat, s=np.sqrt(d.stock_2018) * 2.2, color=pal[c], edgecolor=SURFACE, lw=0.8,
                   zorder=3 + order.index(c), alpha=0.95)
    tu = u.loc[TU]
    ax.scatter(tu.lon, tu.lat, s=np.sqrt(w.loc[TU, 2018]) * 2.2, color=C["lapampa"], edgecolor=INK, lw=1.0, zorder=8)
    ax.annotate("Tambopata buffer zone\n(treated, La Pampa)", (tu.lon, tu.lat), xytext=(-14, -26), textcoords="offset points",
                fontsize=8.5, fontweight="semibold", ha="right", color=INK,
                arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.7))
    twins = list(dict.fromkeys(list(chosen) + m[m.cls.isin(["passes all rules", "passes if post-2021 operations allowed"])].index.tolist()))
    for k, uid in enumerate(twins):
        r = u.loc[uid]
        ax.annotate(r["name"].split(" (")[0] + "\n(rule-based twin)", (r.lon, r.lat), xytext=(28, 34 - 80 * k),
                    textcoords="offset points", fontsize=8.5, fontweight="semibold", color=INK,
                    arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.7))
    ax.set_xlim(-80, -48); ax.set_ylim(-19, 9); ax.set_aspect(1)
    ax.set_xticks([]); ax.set_yticks([]); ax.set_xlabel(""); ax.set_ylabel("")
    for sp in ax.spines.values(): sp.set_visible(False)
    hs = [Line2D([], [], marker="o", ls="", color=pal[l], ms=7, label=l) for l in
          ["passes all rules", "passes if post-2021 operations allowed", "operation reported", "unclear / not searched"]
          if (m.cls == l).any()]
    hs.append(Line2D([], [], marker="o", ls="", color=C["lapampa"], mec=INK, ms=8, label="Tambopata buffer zone"))
    hs.append(Line2D([], [], marker="s", ls="", color="#dfeadb", ms=9, label="National protected areas (RAISG)"))
    ax.legend(handles=hs, fontsize=8, frameon=False, loc="upper center", bbox_to_anchor=(0.5, -0.01), ncol=3,
              handletextpad=0.3, columnspacing=1.2)
    finish_figure(fig, f"{SRC}. Longitude −80 to −48, latitude −19 to 9. Description.", OUT / "fig_control_map.png")


def fig_compare(w, u, chosen_strict, chosen_relaxed, mbpre):
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(9, 4.4), gridspec_kw={"width_ratios": [1.15, 1], "wspace": 0.55})
    tam_d = shares(w, [TU]).loc[2019:2021].mean()
    twin_id = chosen_strict or chosen_relaxed
    twin_d = shares(w, [twin_id]).loc[2019:2021].mean() if twin_id else np.nan
    headline(fig, "Tambopata added new mining far more slowly than its twin in 2019–21",
             "Left: new mining per year, % of each area’s own 2018 mining (Amazon Mining Watch). "
             "Right: mining area, index 2018 = 100 (MapBiomas).")
    lines = [([TU], "Tambopata BZ\n(treated)", C["lapampa"], "-")]
    if chosen_strict:
        lines.append(([chosen_strict], u.loc[chosen_strict, "name"].split(" (")[0], C["corridor"], "-"))
    if chosen_relaxed:
        lines.append(([chosen_relaxed], u.loc[chosen_relaxed, "name"].split(" (")[0] + "\n(twin; own op. 2023)", C["twin"], "-"))
    lines.append(([AMARAKAERI], "Amarakaeri BZ\n(neighbour)", C["buffer"], "-"))
    period_band(a1, 2018.5, 2021.5, "Mercurio years")
    ends, ymax = [], 0.0
    for ids, lab, col, ls in lines:
        s = shares(w, ids)
        a1.plot(YRS[:-1], s[YRS[:-1]], color=col, ls=ls, lw=2, zorder=3)
        a1.plot(YRS[:-1], s[YRS[:-1]], "o", color=col, ms=4, mec="white", mew=0.8, zorder=4)
        a1.plot(YRS[-2:], s[YRS[-2:]], color=col, ls=(0, (2, 2)), lw=1.2, zorder=3)
        a1.plot([2025], [s[2025]], marker="o", mfc="white", color=col, ms=5, zorder=4)
        ends.append([s[2025], lab]); ymax = max(ymax, float(s[YRS].max()))
    # spread end labels so they do not collide (two-line labels: keep ~3.6 points of y per label)
    style_axes(a1); a1.set_ylim(0, ymax * 1.07)
    gap = 0.135 * a1.get_ylim()[1]
    lab_of = {}
    order = sorted(range(len(ends)), key=lambda i: ends[i][0])
    ys = [ends[i][0] for i in order]
    for j in range(1, len(ys)):
        ys[j] = max(ys[j], ys[j - 1] + gap)
    shift = max(0, ys[-1] - a1.get_ylim()[1] * 0.97)
    for j, i in enumerate(order):
        a1.annotate(ends[i][1], xy=(2025, ends[i][0]), xytext=(2025.35, ys[j] - shift), textcoords="data", va="center",
                    fontsize=7.5, color=INK, fontweight="semibold", annotation_clip=False, linespacing=1.1,
                    arrowprops=dict(arrowstyle="-", color=AXIS, lw=0.6, shrinkA=0, shrinkB=3))
    a1.set_ylabel("% of own 2018 mining")
    a1.set_title("Pace of new mining, 2019–2025", pad=8)
    a1.set_xticks(YRS); a1.set_xticklabels([f"'{str(y)[2:]}" for y in YRS])
    a1.set_xlim(2018.6, 2025.3)
    if twin_id:
        callout(a1, 2020, tam_d, f"2019–21 mean: {tam_d:.0f}%\n(twin {twin_d:.0f}%)", dy=-30, arrow=False, fontsize=7.5)
    for (lab, s_, col, ls) in mbpre:
        a2.plot(s_.index, s_.values, color=col if "Tambopata" in lab else C["twin"], ls="-", lw=2)
        nm = lab.split(" (")[0].replace("Tambopata BZ", "Tambopata BZ")
        label_end(a2, s_.index[-1], s_.values[-1], nm + "\n(" + lab.split("(")[-1], col, dx=6, fontsize=7.5)
    a2.axvline(2018.5, color=INK, lw=1.0)
    a2.axhline(100, color=AXIS, lw=0.8)
    style_axes(a2)
    a2.set_ylabel("Index, 2018 = 100")
    a2.set_title("Before 2019: similar growth paths", pad=8)
    a2.set_xticks(range(2010, 2024, 3))
    finish_figure(fig, f"{SRC}; MapBiomas Peru Collection 4 (Tambopata) and MapBiomas Amazonía Collection 6 "
                       "(twin, to 2023). Left: 2025 provisional (hollow dot, dashed). Right: the two collections are shown "
                       "side by side, never subtracted. Description.", OUT / "fig_control_compare.png")


def mb_pre(chosen_name, col="#6250d6"):
    """MapBiomas mining AREA (stock), index 2018 = 100: Tambopata BZ (Peru Col 4), control (Amazonía Col 6). A stock index is
    used, not additions, because additions of a small area are too noisy to read relative to their own mean."""
    out = []
    zb = pd.read_csv(ROOT / "data" / "peru_bufferzone_year.csv")
    t = zb[(zb.buffer_zone == "Tambopata") & (zb.pa_category == "Reserva Nacional")].groupby("year").mining_ha.sum()
    out.append(("Tambopata BZ (Peru Col 4)", (100 * t / t.loc[2018]).loc[2010:2023], "#eb6834", "-"))
    f = INTER / "mb_amazonia_col6_mining.csv"
    if chosen_name and f.exists():
        m = pd.read_csv(f)
        key = chosen_name.split(" (")[0]
        sel = m[m.territory_level_2.str.fullmatch(key, case=False)]
        if sel.geocode.nunique() >= 1:
            s = sel.groupby("year").mining_ha.sum()
            out.append((f"{key} (Amazonía Col 6)", (100 * s / s.loc[2018]).loc[2010:2023], col, "-"))
    return out


def run(reg):
    print("\n== Rule-based control (Ruby's design) ==")
    if not (INTER / "amw_candidates_units.csv").exists():
        warnings.warn("control_select: intermediates missing; skipping"); return
    u, w, e, ops = load()
    t = funnel(u, w, e, ops)
    keep = ["country", "kind", "name", "stock_2018", "elev_median_m", "dist_la_pampa_km", "verdict", "first_op",
            "r1_mining", "r2_no_op", "r2b_no_op_2017_21", "r3_outside_mdd", "r4_lowland", "fit_distance", "pass_strict", "pass_relaxed"]
    t[t.r1_mining][keep].round(2).to_csv(OUT / "control_funnel.csv")
    strict = t[t.pass_strict].index.tolist()
    relaxed = t[t.pass_relaxed & ~t.pass_strict].index.tolist()
    cs = strict[0] if strict else None
    cr = relaxed[0] if relaxed else None
    print(t[t.r1_mining][["name", "stock_2018", "elev_median_m", "verdict", "first_op", "fit_distance", "pass_strict", "pass_relaxed"]]
          .round(2).to_string())
    rows = [compare(w, [c], u.loc[c, "name"]) for c in [cs, cr] if c] + [compare(w, [AMARAKAERI], "Amarakaeri buffer zone")]
    res = pd.DataFrame(rows); res.round(2).to_csv(OUT / "control_compare.csv", index=False)
    print(res.round(1).to_string(index=False))
    n_all = len(u)
    reg.add("ctl_n_areas", n_all, "count", "Areas with polygons screened (SERNANP ANP+BZ, RAISG national PAs outside Peru, FUNAI TIs)", "description", SRC)
    reg.add("ctl_n_r1", t.r1_mining.sum(), "count", f"Areas with >= {MIN_STOCK:.0f} ha AMW mining by 2018 (excl. Tambopata BZ)", "description", SRC)
    reg.add("ctl_n_r2", (t.r1_mining & t.r2_no_op).sum(), "count", "... and no operation found 2017-2025", "description", SRC)
    reg.add("ctl_n_r3", (t.r1_mining & t.r2_no_op & t.r3_outside_mdd).sum(), "count", "... and outside Madre de Dios", "description", SRC)
    reg.add("ctl_n_r4", t.pass_strict.sum(), "count", "... and lowland mining (< 500 m) of similar scale (>= 1/5 of Tambopata): passes all rules", "description", SRC)
    reg.add("ctl_n_relaxed", t.pass_relaxed.sum(), "count", "Pass all rules if operations after 2021 are allowed", "description", SRC)
    reg.add("ctl_n_r1_unclear_or_unsearched", (t.r1_mining & t.verdict.isin(["unclear", "not searched"])).sum(), "count",
            "Areas with mining whose operation status is unclear or not searched", "description", SRC)
    reg.add("ctl_tam_stock_2018", w.loc[TU, 2018], "ha", "AMW mining stock 2018, Tambopata BZ", "description", SRC)
    reg.add("ctl_tam_elev_m", e.loc[TU, "elev_median_m"], "m", "Median elevation of AMW mining, Tambopata BZ", "description", SRC)
    for r, tag in zip(rows, ["strict", "relaxed", "amarakaeri"] if cs and cr else (["strict" if cs else "relaxed", "amarakaeri"])):
        for k in ("tam_during", "tam_after", "ctl_during", "ctl_after", "during_gap", "rebound_gap"):
            reg.add(f"ctl_{tag}_{k}", r[k], "percent of 2018 stock / pp",
                    f"{k}, Tambopata BZ vs {r['control']} (AMW new mining per year as % of own 2018 stock; during = 2019-21, "
                    "after = 2022-25, 2025 provisional)", "description", SRC)
    for r, tag in zip(rows, ["strict", "relaxed"] if cs and cr else ["strict" if cs else "relaxed"]):
        reg.add(f"ctl_{tag}_during_ratio", r["tam_during"] / r["ctl_during"], "ratio",
                f"Tambopata's 2019-21 pace of new mining as a share of {r['control']}'s (both as % of own 2018 AMW stock)",
                "description", SRC)
        reg.add(f"ctl_{tag}_during_gap_ha", r["during_gap"] / 100 * w.loc[TU, 2018], "ha/yr (AMW scale)",
                f"During gap vs {r['control']} converted to hectares at Tambopata's 2018 AMW stock (AMW hectares run large; "
                "never compare with MapBiomas hectares)", "description", SRC)
    for tag, c in (("strict", cs), ("relaxed", cr)):
        if c:
            reg.add(f"ctl_{tag}_stock_2018", w.loc[c, 2018], "ha", f"AMW stock 2018, {u.loc[c, 'name']}", "description", SRC)
            reg.add(f"ctl_{tag}_elev_m", e.loc[c, "elev_median_m"], "m", f"Median mining elevation, {u.loc[c, 'name']}", "description", SRC)
            reg.add(f"ctl_{tag}_dist_km", u.loc[c, "dist_la_pampa_km"], "km", f"Distance to La Pampa, {u.loc[c, 'name']}", "description", SRC)
    fig_funnel(t, n_all)
    fig_map(t, u, w, [c for c in (cs, cr) if c])
    pre = mb_pre(u.loc[cs, "name"] if cs else (u.loc[cr, "name"] if cr else None), "#2a78d6" if cs else "#6250d6")
    for (lab, sr, _, _), tag in zip(pre, ["tam", "twin"]):
        reg.add(f"ctl_mb_{tag}_index_2014", sr.loc[2014], "index 2018=100", f"MapBiomas mining area 2014, index 2018 = 100: {lab}", "description", SRC)
        reg.add(f"ctl_mb_{tag}_index_2021", sr.loc[2021], "index 2018=100", f"MapBiomas mining area 2021, index 2018 = 100: {lab}", "description", SRC)
        reg.add(f"ctl_mb_{tag}_index_2023", sr.loc[2023], "index 2018=100", f"MapBiomas mining area 2023, index 2018 = 100: {lab}", "description", SRC)
    fig_compare(w, u, cs, cr, pre)
    return t, res
