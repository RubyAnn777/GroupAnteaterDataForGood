"""Phase 5 robustness for the Peru 2x2 DiD (Tambopata buffer zone = more-treated unit). Description only.

(a) alternative controls, (b) drop the largest unit, (c) output/peru_robustness.csv, (d) the "rest of Madre de
Dios" definition issue. One treated unit: no standard errors anywhere, by design.

Definitions
- Additions: one row per unit-year first (sum over departments), then diff (rule 2).
- Multi-unit controls are the EQUAL-WEIGHT MEAN of the units' additions (same weighting as the event study),
  except where the spec says "summed".
- "Peruvian Amazon" controls: the buffer-zone table has no biome column, so we keep only the ROWS whose
  department has an Amazonía-biome row in peru_department_year.csv (16 departments), drop the rest (e.g.
  Ancash, Lambayeque, Ica, Tumbes, Arequipa, Apurimac, Moquegua), sum to zone-year, and keep zones with non-zero
  additions in 2014-18 (pre-2019 mining; selecting on pre-period only, not on the outcome). Department is a
  coarse proxy: Cusco, Junin, Puno etc. also hold Andean land, so some retained rows may be non-Amazonian.
"""
from __future__ import annotations
import numpy as np
import pandas as pd

from common import OUT, period_mean
import peru

TU = "Tambopata|Reserva Nacional"
AM = "Amarakaeri|Reserva Comunal"
BA = "Bahuaja-Sonene|Parque Nacional"
WINDOWS = {  # name -> (pre, post)
    "main": ((2016, 2018), (2019, 2021)),
    "placebo": ((2013, 2015), (2016, 2018)),
    "persistence": ((2016, 2018), (2022, 2025)),
}
SRC = "peru_bufferzone_year.csv, peru_department_year.csv"

def _unit_adds(zb: pd.DataFrame) -> pd.DataFrame:
    zb = zb.assign(unit=zb["buffer_zone"] + "|" + zb["pa_category"])
    lv = zb.groupby(["unit", "year"])["mining_ha"].sum().unstack("unit")
    assert lv.index.is_monotonic_increasing and (np.diff(lv.index) == 1).all()
    return lv.diff()

def _did(t: pd.Series, c: pd.Series, pre, post) -> float:
    return (period_mean(t, *post) - period_mean(t, *pre)) - (period_mean(c, *post) - period_mean(c, *pre))

def run(pack, reg, series=None):
    print("\n== Peru robustness (Phase 5) ==")
    zb, pe = pack["zb"], pack["pe"]
    ad_all = _unit_adds(zb)

    # ---- Amazon-department-restricted pool
    amz_depts = set(pe.loc[pe["biome"] == "Amazonía", "department"])
    zr = zb[zb["department"].isin(amz_depts)]
    dropped = sorted(set(zb["department"]) - amz_depts)
    ad_amz = _unit_adds(zr)
    nz = ad_amz.loc[2014:2018].abs().sum() > 0
    amz_pool = sorted(u for u in nz[nz].index if u != TU)
    print(f"Amazon-department rows kept; departments dropped: {dropped}; pool = {len(amz_pool)} zones")
    # all-Peru pool B (as in the event study, any department)
    nzB = ad_all.loc[2014:2018].abs().sum() > 0
    poolB = sorted(u for u in nzB[nzB].index if u != TU)

    levels, adds, _ = series if series is not None else peru.build_series(pack)
    rest = adds["Rest of Madre de Dios"]
    controls = {
        "Amarakaeri BZ (main)": (AM, ad_all[AM], "Main control; partly treated too (Camanti)"),
        "Bahuaja-Sonene BZ": (BA, ad_all[BA], "Tiny pre-period mining (mean ~13 ha/yr), so a weak counterfactual"),
        "Amarakaeri + Bahuaja-Sonene, equal-weight mean": (f"{AM}; {BA}", (ad_all[AM] + ad_all[BA]) / 2,
                                                          "Mean of the two zones"),
        "Amarakaeri + Bahuaja-Sonene, summed": (f"{AM}; {BA}", ad_all[AM] + ad_all[BA], "Sum of the two zones"),
        "Rest of Madre de Dios": ("dept. minus MdD buffer zones", rest,
                                  "Includes the legal mining corridor; ~5-10x the scale of the treated unit; see (d)"),
        f"Other Peruvian-Amazon-department buffer zones with 2014-18 mining (n={len(amz_pool)}), mean":
            ("; ".join(amz_pool), ad_amz[amz_pool].mean(axis=1), "Equal-weight mean; department-based Amazon filter"),
        f"All Peru buffer zones with 2014-18 mining (n={len(poolB)}), mean (event-study pool B)":
            ("; ".join(poolB), ad_all[poolB].mean(axis=1), "Any department; includes non-Amazon zones"),
    }
    rows = []
    def add_row(spec, treated, control, win, did, note, kind="did"):
        pre, post = WINDOWS[win] if win in WINDOWS else win
        rows.append(dict(spec=spec, treated=treated, control=control, pre=f"{pre[0]}-{pre[1]}",
                         post=f"{post[0]}-{post[1]}", DiD_ha_per_yr=round(float(did), 1),
                         claim_type="description", note=note))
    for name, (cid, cs, note) in controls.items():
        for w, (pre, post) in WINDOWS.items():
            d = _did(ad_all[TU], cs, pre, post)
            add_row(f"(a) {w}: control = {name}", "Tambopata BZ", cid if len(cid) < 90 else f"{len(cid.split('; '))} zones", w, d,
                    note + ("; PLACEBO window: no real treatment, a large value = pre-trend/noise" if w == "placebo" else ""))
    # register the main-window numbers under stable ids
    ids = ["amarakaeri", "bahuaja", "ama_bah_mean", "ama_bah_sum", "rest_mdd", "amazon_pool", "all_peru_poolB"]
    for (name, (cid, cs, note)), sid in zip(controls.items(), ids):
        for w, (pre, post) in WINDOWS.items():
            reg.add(f"robust_did_{w}_{sid}", _did(ad_all[TU], cs, pre, post), "ha/yr",
                    f"DiD of mean annual additions, Tambopata BZ minus control [{name}], {w} windows "
                    f"{pre[0]}-{pre[1]} -> {post[0]}-{post[1]}. Descriptive contrast; not causal.", "description", SRC)

    # ---- (b) drop the largest unit
    def largest(units):   # largest by mean annual addition 2014-18 (pre-2019 mining)
        m = ad_all.loc[2014:2018, units].mean()
        return m.idxmax(), float(m.max())
    big_B, mB = largest(poolB)
    poolB2 = [u for u in poolB if u != big_B]
    poolA = [AM, BA]
    big_A, mA = largest(poolA)
    print(f"Largest pre-2019 control: pool B = {big_B} ({mB:,.0f} ha/yr); pool A = {big_A} ({mA:,.0f} ha/yr)")
    for lab, units, sid in [("pool B without " + big_B.split("|")[0], poolB2, "poolB_drop_largest"),
                            ("pool A without " + big_A.split("|")[0], [u for u in poolA if u != big_A], "poolA_drop_largest")]:
        b = peru.beta_by_formula(ad_all[[TU] + units], TU)
        for lo, hi in [(2019, 2021), (2022, 2025)]:
            v = float(b.loc[lo:hi].mean())
            rows.append(dict(spec=f"(b) event study (ref 2018), {lab}", treated="Tambopata BZ", control=f"{len(units)} zones",
                             pre="2018 (reference)", post=f"{lo}-{hi}", DiD_ha_per_yr=round(v, 1), claim_type="description",
                             note="Mean event-study coefficient over the post window (reference year 2018 only; not the same "
                                  "baseline as the 2016-18 DiD)"))
            reg.add(f"robust_es_{sid}_{lo}_{hi}", v, "ha/yr", f"Mean event-study coefficient {lo}-{hi}, {lab}", "description", SRC)
    b_full = peru.beta_by_formula(ad_all[[TU] + poolB], TU)
    for lo, hi in [(2019, 2021), (2022, 2025)]:
        v = float(b_full.loc[lo:hi].mean())
        rows.append(dict(spec="(b) event study (ref 2018), pool B full (reference for the two rows above)", treated="Tambopata BZ",
                         control=f"{len(poolB)} zones", pre="2018 (reference)", post=f"{lo}-{hi}", DiD_ha_per_yr=round(v, 1),
                         claim_type="description", note="Same estimator, nothing dropped"))
        reg.add(f"robust_es_poolB_full_{lo}_{hi}", v, "ha/yr", f"Mean event-study coefficient {lo}-{hi}, pool B full", "description", SRC)
    # displacement sum without Tambopata: Amarakaeri + Bahuaja-Sonene
    s2 = ad_all[AM] + ad_all[BA]
    base = period_mean(s2, 2016, 2018)
    for lo, hi in [(2019, 2021), (2022, 2025)]:
        v = period_mean(s2, lo, hi) - base
        rows.append(dict(spec="(b) displacement: sum of the 2 other zones (Tambopata dropped), before/after change",
                         treated="Amarakaeri + Bahuaja-Sonene (summed)", control="(none)", pre="2016-18", post=f"{lo}-{hi}",
                         DiD_ha_per_yr=round(v, 1), claim_type="description",
                         note="Not a DiD: change in mean annual addition. Positive = the neighbours gained"))
        reg.add(f"robust_displ_two_zones_chg_{lo}_{hi}", v, "ha/yr",
                f"Change in mean annual addition, Amarakaeri + Bahuaja-Sonene summed (Tambopata dropped), {lo}-{hi} vs 2016-18",
                "description", SRC)

    # ---- (d) rest-of-MdD definition issue
    mdd_all = pe[pe["department"] == "Madre de Dios"].groupby("year")["mining_ha"].sum()
    mdd_amz = pe[(pe["department"] == "Madre de Dios") & (pe["biome"] == "Amazonía")].groupby("year")["mining_ha"].sum()
    non_amz = (mdd_all - mdd_amz)
    mdd_bz = zb[zb["department"] == "Madre de Dios"].groupby("year")["mining_ha"].sum()
    rest_all = mdd_all - mdd_bz
    area = pe[pe["department"] == "Madre de Dios"].groupby("biome")["total_ha"].first()
    adds_alt = rest_all.diff()
    out_d = pd.DataFrame({"MdD mining, Amazonia biome": mdd_amz, "MdD mining, all biomes": mdd_all,
                          "non-Amazon-biome mining (diff)": non_amz, "buffer-zone rows in MdD": mdd_bz,
                          "rest of MdD (Amazonia - BZ)": mdd_amz - mdd_bz, "rest of MdD (all biomes - BZ)": rest_all})
    out_d.round(2).to_csv(OUT / "peru_rest_mdd_definition_check.csv")
    mx = float(non_amz.abs().max())
    print(f"(d) MdD non-Amazon-biome mining: max over years {mx:.3f} ha (2025: {non_amz.loc[2025]:.3f} ha); "
          f"non-Amazon biome area {area.get('Andes', np.nan):,.0f} ha of {area.sum():,.0f} ha ({area.get('Andes', np.nan)/area.sum():.2%})")
    diff_adds = float((adds_alt - adds["Rest of Madre de Dios"]).abs().loc[2014:2025].max())
    reg.add("restmdd_nonamazon_mining_max_ha", mx, "ha", "Max over 1985-2025 of MdD mining outside the Amazonia biome (department table, all biomes minus Amazonia)", "description", SRC)
    reg.add("restmdd_nonamazon_area_share", float(area.get("Andes", 0) / area.sum()), "share", "Share of Madre de Dios department area in the non-Amazon (Andes) biome", "description", SRC)
    reg.add("restmdd_definition_max_abs_diff_additions", diff_adds, "ha", "Max abs difference in annual additions 2014-25 between 'rest of MdD' defined with all biomes vs Amazonia only", "description", SRC)
    rows.append(dict(spec="(d) rest-of-MdD definition: all biomes vs Amazonia only", treated="Rest of Madre de Dios", control="(n/a)",
                     pre="2014-25", post="", DiD_ha_per_yr=round(diff_adds, 3), claim_type="description",
                     note=f"Value = max abs difference in annual additions (ha). MdD non-Amazon-biome mining max {mx:.2f} ha; "
                          f"that biome is {area.get('Andes', np.nan)/area.sum():.2%} of the department area. Mismatch negligible; the real "
                          f"issue is the legal mining corridor inside 'rest'."))
    tab = pd.DataFrame(rows)
    tab.to_csv(OUT / "peru_robustness.csv", index=False)
    show = tab[tab.spec.str.startswith("(a)")][["spec", "DiD_ha_per_yr"]]
    print(show.to_string(index=False, max_colwidth=110))
    print(tab[~tab.spec.str.startswith("(a)")][["spec", "post", "DiD_ha_per_yr"]].to_string(index=False, max_colwidth=100))
    return tab
