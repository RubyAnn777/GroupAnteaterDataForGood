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

from common import ROOT, OUT, style_axes, finish_figure

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
    steps = [("All areas with polygons", n_all),
             ("R1  mining before 2019 (>= 500 ha)", int(t.r1_mining.sum())),
             ("R2  + no operation found, 2017-25", int((t.r1_mining & t.r2_no_op).sum())),
             ("R3  + outside Madre de Dios", int((t.r1_mining & t.r2_no_op & t.r3_outside_mdd).sum())),
             ("R4  + lowland and similar scale", int(t.pass_strict.sum()))]
    fig, ax = plt.subplots(figsize=(8.5, 3.6))
    for i, (lab, n) in enumerate(steps):
        ax.barh(-i, n, color="#2a78d6" if i == len(steps) - 1 else "#9aa5a8", height=0.62)
        ax.text(n * 1.08 if n else 0.3, -i, f"{n:,}", va="center", fontsize=9, fontweight="bold")
    ax.set_yticks([-i for i in range(len(steps))]); ax.set_yticklabels([s[0] for s in steps], fontsize=9)
    ax.set_xscale("symlog", linthresh=1); ax.set_xlim(0, n_all * 3)
    ax.set_xticks([]); ax.tick_params(axis="x", length=0); ax.xaxis.set_minor_locator(plt.NullLocator())
    for sp in ("top", "right", "bottom"): ax.spines[sp].set_visible(False)
    names = t[t.pass_strict].name.tolist()
    rel = t[t.pass_relaxed & ~t.pass_strict].name.tolist()
    ax.set_title("Ruby's four rules leave " + (f"{len(names)} area(s)" if names else "no area") +
                 " in the whole Amazon that fits", loc="left", fontsize=11, fontweight="bold")
    note = ("Survivors: " + (", ".join(names) if names else "none") + ". If operations after 2021 are allowed (R2b): " +
            (", ".join(rel[:6]) if rel else "none") + ".")
    finish_figure(fig, note + f" Sources: {SRC}. Bars on a log scale. Description.", OUT / "fig_control_funnel.png",
                  rect_bottom=0.2, event_note=False)


def fig_map(t, u, w, chosen):
    import geopandas as gpd
    fig, ax = plt.subplots(figsize=(9, 6.6))
    base = ROOT / "data_raw" / "raisg"
    parts = sorted(base.glob("anp_nacionales_part*.geojson"))
    if parts:
        g = pd.concat([gpd.read_file(p)[["geometry"]] for p in parts])
        gpd.GeoDataFrame(g, crs=4326).plot(ax=ax, color="#E3EDE0", edgecolor="#cfd8cc", lw=0.2, zorder=0)
    pal = {"passes all rules": "#2a78d6", "passes if post-2021 operations allowed": "#6250d6",
           "operation reported": "#eb6834", "unclear / not searched": "#9aa5a8"}
    def cls(r):
        if r.pass_strict: return "passes all rules"
        if r.pass_relaxed: return "passes if post-2021 operations allowed"
        if r.verdict == "yes": return "operation reported"
        return "unclear / not searched"
    m = t[t.r1_mining].copy(); m["cls"] = m.apply(cls, axis=1)
    for c, col in pal.items():
        d = m[m.cls == c]
        ax.scatter(d.lon, d.lat, s=np.sqrt(d.stock_2018) * 2.2, color=col, edgecolor="white", lw=0.6, zorder=3, label=c)
    tu = u.loc[TU]
    ax.scatter(tu.lon, tu.lat, s=np.sqrt(w.loc[TU, 2018]) * 2.2, marker="*", color="black", zorder=4, label="Tambopata (treated)")
    for uid in [TU] + chosen:
        r = u.loc[uid]
        ax.annotate(r["name"].split(" (")[0], (r.lon, r.lat), xytext=(6, 4), textcoords="offset points", fontsize=8,
                    fontweight="bold" if uid in chosen else "normal")
    ax.set_xlim(-80, -48); ax.set_ylim(-19, 9); ax.set_aspect(1)
    ax.set_xlabel("Longitude"); ax.set_ylabel("Latitude")
    for sp in ("top", "right"): ax.spines[sp].set_visible(False)
    hs = [Line2D([], [], marker="o", ls="", color=c, ms=7, label=l) for l, c in pal.items()]
    hs.append(Line2D([], [], marker="*", ls="", color="black", ms=10, label="Tambopata buffer zone (treated)"))
    ax.legend(handles=hs, fontsize=7.5, frameon=True, framealpha=0.9, loc="lower left",
              title="Areas with >= 500 ha mining by 2018 (dot size = ha)", title_fontsize=7.5)
    ax.set_title("Candidate comparison areas across the Amazon", loc="left", fontsize=11, fontweight="bold")
    finish_figure(fig, f"Sources: {SRC}; green shapes = RAISG national protected areas. Description.",
                  OUT / "fig_control_map.png", rect_bottom=0.06, event_note=False)


def fig_compare(w, u, chosen_strict, chosen_relaxed, mbpre):
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(12, 4.4), gridspec_kw={"width_ratios": [1.25, 1]})
    lines = [([TU], "Tambopata buffer zone (treated)", "#eb6834", "-")]
    if chosen_strict:
        lines.append(([chosen_strict], u.loc[chosen_strict, "name"].split(" (")[0] + " (passes all rules)", "#2a78d6", "-"))
    if chosen_relaxed:
        lines.append(([chosen_relaxed], u.loc[chosen_relaxed, "name"].split(" (")[0] + " (rule-based twin; first operation 2023)", "#6250d6", "--"))
    lines.append(([AMARAKAERI], "Amarakaeri buffer zone (neighbour)", "#1baf7a", ":"))
    for ids, lab, col, ls in lines:
        s = shares(w, ids)
        a1.plot(YRS[:-1], s[YRS[:-1]], color=col, ls=ls, lw=2, marker="o", ms=4, label=lab)
        a1.plot(YRS[-2:], s[YRS[-2:]], color=col, ls=":", lw=1.2)
        a1.plot([2025], [s[2025]], marker="o", mfc="white", color=col, ms=5)
    a1.axvspan(2018.5, 2021.5, color="#f3e3c2", alpha=0.5, zorder=0)
    a1.text(2020, 0.5, "Mercurio years", ha="center", fontsize=8, va="bottom", color="#8a6d2b")
    style_axes(a1); a1.set_ylim(0, None)
    a1.set_ylabel("New mining per year,\n% of the area's 2018 mining (AMW)")
    a1.set_title("Same satellite measure for both areas, 2019-2025", loc="left", fontsize=9.5)
    a1.legend(fontsize=7.5, frameon=True, framealpha=0.9, loc="upper right")
    a1.set_xticks(YRS)
    for (lab, s, col, ls) in mbpre:
        a2.plot(s.index, s.values, color=col, ls=ls, lw=1.8, label=lab)
    a2.axvline(2018.5, color="#52514e", lw=1, ls="--")
    a2.axhline(100, color="#888", lw=0.6)
    style_axes(a2)
    a2.set_ylabel("Total mining area,\nindex 2018 = 100 (MapBiomas)")
    a2.set_title("Before 2019: MapBiomas, each area from its own collection", loc="left", fontsize=9.5)
    a2.legend(fontsize=7.5, frameon=False, loc="upper left")
    fig.suptitle("The twin grew like Tambopata until 2018; in 2019-21 Tambopata added mining at well under half the twin's pace",
                 x=0.01, ha="left", fontsize=11, fontweight="bold")
    finish_figure(fig, f"Sources: {SRC}; MapBiomas Peru Collection 4 (Tambopata) and MapBiomas Amazonía Collection 6 "
                       "(control, to 2023). Left: 2025 provisional (hollow). Right: the two collections are only shown side "
                       "by side, never subtracted. Description.", OUT / "fig_control_compare.png", rect_bottom=0.12)


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
