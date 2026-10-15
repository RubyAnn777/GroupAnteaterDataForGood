"""Rule-based comparison area for Tambopata (Ruby's design): find ONE existing area that is a fair 'what if' for La Pampa.

The four rules, applied in order to every protected area, buffer zone and indigenous territory in the Amazon we have
polygons for (SERNANP Peru, RAISG for the other countries and Brazil's conservation units, FUNAI territories):
  R1  Mining before 2019:  Amazon Mining Watch (AMW) detected at least MIN_STOCK ha of mining scars by 2018.
  R2  No operation:        no VERIFIED operation against mining 2017-2025 (rule R*, brazil_v2.verdict over
                           data_intermediate/operations_coded.csv; 'unclear' and 'not searched' fail; an area searched
                           only for 2022-25 is 'unclear'). Relaxed version (R2b): no verified operation 2017-2021, i.e.
                           in Mercurio's own years. Under R* an UNVERIFIED report (Munduruku, May 2021 snippet) is
                           context, not a reason to exclude; sensitivity: count it (the area becomes 'unclear').
  R3  Far enough away:     outside the v3 registry region (Madre de Dios + the Tambopata and Amarakaeri buffer zones),
                           tested at the area's centre on data_intermediate/zones_mdd.tif (v2: a lon/lat box).
  R4  Geographic twin:     lowland mining like La Pampa (median elevation of the area's mining < MAX_ELEV m) AND a similar
                           scale (2018 mining at least MIN_SCALE x Tambopata's); survivors are ranked by distance to
                           Tambopata on elevation and on size of mining in 2018 (both on a log scale); best = chosen.
Then compare Tambopata with the chosen area on the SAME measure: AMW new area per year as % of the area's own 2018
AMW stock, 2019-21 only (definitions.PERIODS["during"]; the twins had their own operations from 2023, so no later-years
comparison is registered). MEASURE: AMW new area (comparable to first-time mining, NOT to net additions).
Tambopata = the official whole Tambopata buffer zone (PE-BZ-RN09 = registry units lapampa + tambopata_bz_rest); its AMW
series is checked against the registry raster (spatial.py). AMW starts in 2018, so pre-2019 paths come from MapBiomas,
each area from its OWN collection: Tambopata from the MapBiomas Peru Collection 4 rasters (registry, zonedata.py), the
twin from MapBiomas Amazonía Collection 6 statistics; shown side by side as indices, never subtracted (rules 6-7).
Review card 10: pre-2019 growth was converging on the twins', not parallel. All results are DESCRIPTION.
"""
from __future__ import annotations
import warnings
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

from common import (ROOT, OUT, style_axes, finish_figure, headline, label_end, callout, period_band, C, INK, INK2,
                    MUTED, GRID, AXIS, SURFACE)
import definitions as D
import checks

INTER = ROOT / "data_intermediate"
TU = "PE-BZ-RN09"                         # official whole Tambopata buffer zone (treated; registry tambopata_bz)
AMARAKAERI = "PE-BZ-RC03"
MIN_STOCK, MAX_ELEV, MIN_SCALE = 500.0, 500.0, 0.2
MEASURE = "amw_new_area"
SRC = ("Amazon Mining Watch (AMW) new area x SERNANP / RAISG / FUNAI polygons (area-weighted); SRTM 90 m elevation "
       "(OpenTopoData); operations: data_intermediate/operations_coded.csv, rule R* (brazil_v2)")
SRC_MB_TAM = "MapBiomas Peru Collection 4 rasters, v3 registry (zonedata.region_units, Tambopata buffer zone)"
SRC_MB_TWIN = "MapBiomas Amazonía Collection 6 statistics (control_mb_amazonia.py)"
DURING = list(range(D.PERIODS["during"][0], D.PERIODS["during"][1] + 1))
YRS = list(range(D.FIRST_POST, 2026))


def load():
    u = pd.read_csv(INTER / "amw_candidates_units.csv").set_index("unit_id")
    w = pd.read_csv(INTER / "amw_candidates_year.csv").pivot(index="unit_id", columns="year", values="new_ha").fillna(0)
    e = pd.read_csv(INTER / "amw_candidates_elevation.csv").set_index("unit_id")
    ops = pd.read_csv(INTER / "operations_coded.csv").set_index("unit_id")
    assert ops.index.is_unique
    return u, w, e, ops


def in_registry(lon, lat) -> np.ndarray:
    """True where (lon, lat) lies inside the v3 registry region (zones_mdd.tif band 1 > 0)."""
    import rasterio
    f = INTER / "zones_mdd.tif"
    with rasterio.open(f) as r:
        b = r.bounds
        ok = (lon > b.left) & (lon < b.right) & (lat > b.bottom) & (lat < b.top)
        out = np.zeros(len(lon), bool)
        idx = np.where(ok)[0]
        if len(idx):
            out[idx] = np.array([v[0] for v in r.sample(list(zip(lon[idx], lat[idx])), indexes=1)]) > 0
    return out


def op_status(index, count_unverified=False):
    """Rule R* (brazil_v2): verdict over the twin window and the first verified operation (YYYY-MM) per area."""
    from brazil_v2 import verdict, first_verified, BRAZIL
    v = verdict(BRAZIL["twin_window"], count_unverified=count_unverified).reindex(index).fillna("not searched")
    first = first_verified(BRAZIL["twin_window"]).reindex(index).fillna("")
    return v, first


def funnel(u, w, e, ops, count_unverified=False) -> pd.DataFrame:
    t = u.join(w[[2018]].rename(columns={2018: "stock_2018"}), how="inner").join(e[["elev_median_m"]])
    t = t.drop(index=TU)
    t["verdict"], t["first_op"] = op_status(t.index, count_unverified)
    fy = pd.to_numeric(t.first_op.str[:4], errors="coerce")
    t["r1_mining"] = t.stock_2018 >= MIN_STOCK
    t["r2_no_op"] = t.verdict.eq("none")
    t["r2b_no_op_2017_21"] = t.r2_no_op | (t.verdict.eq("yes") & (fy > D.PERIODS["during"][1]))
    t["r3_outside_mdd"] = ~(in_registry(t.lon.to_numpy(), t.lat.to_numpy()) & t.country.eq("Peru").to_numpy())
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
    d = dict(control=label, tam_during=t.loc[DURING].mean(), ctl_during=s.loc[DURING].mean())
    d["during_gap"] = d["tam_during"] - d["ctl_during"]
    return d


def twins(count_unverified=False):
    """The rule-based twins: every area passing all four rules with R2b (relaxed), best fit first. The ONE list used
    by control_top3 / control_psm (rule R*)."""
    u, w, e, ops = load()
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        t = funnel(u, w, e, ops, count_unverified)
    return t[t.pass_strict | t.pass_relaxed].index.tolist(), t


def registry_check(w):
    """Same unit everywhere: the AMW series of the official Tambopata buffer zone polygon (vector clip, this file)
    must equal the registry raster (spatial.py: zones lapampa + tambopata_bz_rest) within 2%."""
    f = INTER / "amw_zone_year.csv"
    if not f.exists():
        return
    z = pd.read_csv(f)
    z = z[z.zone.isin(D.UNITS["tambopata_bz"])].groupby("year").new_ha.sum()
    for lab, ys in (("2018 stock", [2018]), ("2019-21 sum", DURING)):
        a, b = float(w.loc[TU, ys].sum()), float(z.loc[ys].sum())
        checks.check(f"AMW Tambopata BZ {lab}: polygon clip vs registry raster, ha (within 2%)", a, b, tol=0.02 * b)
    checks.save()


def fig_funnel(t, n_all):
    steps = [("All protected areas, buffer zones and\nindigenous territories with polygons", n_all),
             ("R1  had mining before 2019 (≥ 500 ha)", int(t.r1_mining.sum())),
             ("R2  + no verified operation, 2017–25", int((t.r1_mining & t.r2_no_op).sum())),
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
    ax.text(0.99, 0.02, f"If verified operations after 2021 are allowed (R2b), {len(rel)} more pass:\n" + ("\n".join(rel[:6]) if rel else "none"),
            transform=ax.transAxes, ha="right", va="bottom", fontsize=8.5, color=INK2, linespacing=1.4)
    note = "Survivors of all four rules: " + (", ".join(names) if names else "none") + "."
    finish_figure(fig, f"Sources: {SRC}. {note} Description.", OUT / "fig_control_funnel.png")


def fig_map(t, u, w, chosen):
    import geopandas as gpd
    fig, ax = plt.subplots(figsize=(9, 7.6))
    m0 = t[t.r1_mining]
    tw0 = list(dict.fromkeys(list(chosen) + m0.index[m0.pass_strict | m0.pass_relaxed].tolist()))
    km = u.loc[tw0, "dist_la_pampa_km"].min() if tw0 else np.nan
    ctry = sorted(set(u.loc[tw0, "country"])) if tw0 else []
    # no country borders in the local data, so the country is named in the labels, not left to the map
    headline(fig, f"The twin candidates sit far from La Pampa: at least {km // 100 * 100:,.0f} km away"
                  + (f", all in {ctry[0]}" if len(ctry) == 1 else ""),
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
    ax.annotate("Tambopata buffer zone\n(Peru; treated, La Pampa)", (tu.lon, tu.lat), xytext=(-14, -26), textcoords="offset points",
                fontsize=8.5, fontweight="semibold", ha="right", color=INK,
                arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.7))
    twins = list(dict.fromkeys(list(chosen) + m[m.cls.isin(["passes all rules", "passes if post-2021 operations allowed"])].index.tolist()))
    for k, uid in enumerate(twins):
        r = u.loc[uid]
        ax.annotate(r["name"].split(" (")[0] + f"\n({r['country']}; rule-based twin)", (r.lon, r.lat), xytext=(28, 34 - 80 * k),
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
    finish_figure(fig, f"{SRC}. Longitude −80 to −48, latitude −19 to 9; no country borders drawn (none in the local data), "
                       "countries named from the area records. Description.", OUT / "fig_control_map.png")


def fig_compare(w, u, chosen_strict, chosen_relaxed, mbpre):
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(9, 4.4), gridspec_kw={"width_ratios": [1.15, 1], "wspace": 0.55})
    tam_d = shares(w, [TU]).loc[DURING].mean()
    twin_id = chosen_strict or chosen_relaxed
    twin_d = shares(w, [twin_id]).loc[DURING].mean() if twin_id else np.nan
    headline(fig, "Tambopata added new mining more slowly than its twin in 2019–21",
             "Left: AMW new area per year, % of each area’s own 2018 AMW area (comparable to first-time mining, not to net\n"
             "additions). Right: mining area (stock), index 2018 = 100, each area from its own MapBiomas collection.")
    lines = [([TU], "Tambopata BZ\n(treated)", C["lapampa"], "-")]
    if chosen_strict:
        lines.append(([chosen_strict], u.loc[chosen_strict, "name"].split(" (")[0], C["corridor"], "-"))
    if chosen_relaxed:
        lines.append(([chosen_relaxed], u.loc[chosen_relaxed, "name"].split(" (")[0] + "\n(twin; own op. 2023)", C["twin"], "-"))
    lines.append(([AMARAKAERI], "Amarakaeri BZ\n(neighbour)", C["buffer"], "-"))
    period_band(a1, DURING[0] - 0.5, DURING[-1] + 0.5, "Mercurio and what\nfollowed (2019–21)")
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
    a1.set_title("Pace of AMW new area, 2019–2025", pad=8)
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
    a2.set_title("Mining area, 2010–2023 (two collections)", pad=8)
    a2.set_xticks(range(2010, 2024, 3))
    finish_figure(fig, f"{SRC}; right: {SRC_MB_TAM} and {SRC_MB_TWIN} (twin, to 2023). Left: 2025 provisional (hollow "
                       "dot, dashed); the twin had its own operation from Mar 2023. Right: the two collections are shown "
                       "side by side, never subtracted; Tambopata's growth was converging on the twin's before 2019 "
                       "(review card 10). Description.", OUT / "fig_control_compare.png")


def tambopata_index(y0=2009, y1=2023) -> pd.Series:
    """Tambopata buffer zone mining area (stock), index 2018 = 100, from the MapBiomas Peru Col 4 rasters on the v3
    registry (the official whole buffer zone; replaces the statistics workbook). Used by control_top3 / slides."""
    import zonedata as Z
    ru = Z.region_units()
    t = ru[ru.unit == D.TREATED_ZONE].set_index("year").mining_ha
    return (100 * t / t.loc[D.REF_YEAR]).loc[y0:y1]


def mb_pre(chosen_name, col="#6250d6"):
    """MapBiomas mining AREA (stock), index 2018 = 100: Tambopata BZ (Peru Col 4 rasters, registry) and the control
    (Amazonía Col 6). A stock index, not additions: additions of a small area are too noisy relative to their mean."""
    out = [("Tambopata BZ (Peru Col 4)", tambopata_index(2010, 2023), C["lapampa"], "-")]
    f = INTER / "mb_amazonia_col6_mining.csv"
    if chosen_name and f.exists():
        m = pd.read_csv(f)
        key = chosen_name.split(" (")[0]
        sel = m[m.territory_level_2.str.fullmatch(key, case=False)]
        if sel.geocode.nunique() >= 1:
            s = sel.groupby("year").mining_ha.sum()
            out.append((f"{key} (Amazonía Col 6)", (100 * s / s.loc[D.REF_YEAR]).loc[2010:2023], col, "-"))
    return out


def _add_ha(reg, id, v, desc, zone, period, unit="ha"):
    reg.add(id, v, unit, desc + ". Measure: AMW new area (comparable to first-time mining, not to net additions)",
            "description", SRC, measure=MEASURE, zone=zone, period=period)


def run(reg):
    print("\n== Rule-based control (Ruby's design, rule R*) ==")
    if not (INTER / "amw_candidates_units.csv").exists():
        warnings.warn("control_select: intermediates missing; skipping"); return
    u, w, e, ops = load()
    registry_check(w)
    t = funnel(u, w, e, ops)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        t_s = funnel(u, w, e, ops, count_unverified=True)
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
    reg.add("ctl_n_r1", t.r1_mining.sum(), "count", f"Areas with >= {MIN_STOCK:.0f} ha AMW area by 2018 (excl. Tambopata BZ)", "description", SRC)
    reg.add("ctl_n_r2", (t.r1_mining & t.r2_no_op).sum(), "count", "... and no verified operation 2017-2025, searched over the whole window (rule R*)", "description", SRC)
    reg.add("ctl_n_r3", (t.r1_mining & t.r2_no_op & t.r3_outside_mdd).sum(), "count", "... and outside the registry region (Madre de Dios + Tambopata/Amarakaeri buffer zones)", "description", SRC)
    reg.add("ctl_n_r4", t.pass_strict.sum(), "count", "... and lowland mining (< 500 m) of similar scale (>= 1/5 of Tambopata): passes all rules", "description", SRC)
    reg.add("ctl_n_relaxed", t.pass_relaxed.sum(), "count", "Pass all rules if verified operations after 2021 are allowed (R2b, rule R*)", "description", SRC)
    reg.add("ctl_n_relaxed_excl_unverified", t_s.pass_relaxed.sum(), "count", "Sensitivity: same, but an UNVERIFIED report in 2017-25 makes an area 'unclear' (fails R2b)", "description", SRC)
    reg.add("ctl_n_r1_unclear_or_unsearched", (t.r1_mining & t.verdict.isin(["unclear", "not searched"])).sum(), "count",
            "Areas with mining whose operation status is unclear (incl. searched 2022-25 only) or not searched", "description", SRC)
    per = D.period_label("during").replace("–", "-20")
    _add_ha(reg, "ctl_tam_stock_2018", w.loc[TU, 2018], "AMW area detected by 2018 (stock), Tambopata buffer zone (official polygon, whole)", "tambopata_bz", "2018")
    reg.add("ctl_tam_elev_m", e.loc[TU, "elev_median_m"], "m", "Median elevation of AMW mining, Tambopata BZ", "description", SRC)
    tags = (["strict"] if cs else []) + (["relaxed"] if cr else []) + ["amarakaeri"]
    for r, tag in zip(rows, tags):
        for k in ("tam_during", "ctl_during", "during_gap"):
            reg.add(f"ctl_{tag}_{k}", r[k], "pp" if k == "during_gap" else "% of 2018 AMW stock per yr",
                    f"{k}, Tambopata BZ vs {r['control']}: AMW new area per year as % of own 2018 AMW area, {per} "
                    "(comparable to first-time mining, not to net additions)", "description", SRC,
                    measure="amw_pace", zone="tambopata_bz", period=per)
    for r, tag in zip(rows, tags[:-1]):
        reg.add(f"ctl_{tag}_during_ratio", r["tam_during"] / r["ctl_during"], "ratio",
                f"Tambopata's {per} pace of AMW new area as a share of {r['control']}'s (both as % of own 2018 AMW area)",
                "description", SRC, measure="amw_pace", zone="tambopata_bz", period=per)
        _add_ha(reg, f"ctl_{tag}_during_gap_ha", r["during_gap"] / 100 * w.loc[TU, 2018],
                f"Gap vs {r['control']} converted to hectares at Tambopata's 2018 AMW area (AMW hectares run large; never "
                "compare with MapBiomas hectares)", "tambopata_bz", per, unit="ha/yr")
    for tag, c in (("strict", cs), ("relaxed", cr)):
        if c:
            _add_ha(reg, f"ctl_{tag}_stock_2018", w.loc[c, 2018], f"AMW area detected by 2018 (stock), {u.loc[c, 'name']}", c, "2018")
            reg.add(f"ctl_{tag}_elev_m", e.loc[c, "elev_median_m"], "m", f"Median mining elevation, {u.loc[c, 'name']}", "description", SRC)
            reg.add(f"ctl_{tag}_dist_km", u.loc[c, "dist_la_pampa_km"], "km", f"Distance to the La Pampa sector (registry), {u.loc[c, 'name']}", "description", SRC)
    fig_funnel(t, n_all)
    fig_map(t, u, w, [c for c in (cs, cr) if c])
    pre = mb_pre(u.loc[cs, "name"] if cs else (u.loc[cr, "name"] if cr else None), C["corridor"] if cs else C["twin"])
    for (lab, sr, _, _), tag in zip(pre, ["tam", "twin"]):
        src = SRC_MB_TAM if tag == "tam" else SRC_MB_TWIN
        for y in (2014, 2021, 2023):
            reg.add(f"ctl_mb_{tag}_index_{y}", sr.loc[y], "index 2018=100", f"Mining area (stock) {y}, index 2018 = 100: {lab}",
                    "description", src, measure="stock", zone="tambopata_bz" if tag == "tam" else "twin", period=str(y))
    fig_compare(w, u, cs, cr, pre)
    return t, res
