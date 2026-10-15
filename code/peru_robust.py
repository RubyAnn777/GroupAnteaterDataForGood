"""Robustness of the Peru 2x2 DiD (plan v3): alternative controls, drop the largest unit. Description only.

Outcome = NET mining additions (ha/yr) = new land + re-mined - stopped, MapBiomas Peru Collection 4 rasters, our pixel
accounting. Buffer zones come whole from the national raster panel (zonedata.bz_panel); Madre de Dios land outside
buffer zones from the region registry (zonedata.region_units: corridor outside buffer zones, native communities,
rest of Madre de Dios). Every quantity here is a mean, a difference or an equal-weight event-study coefficient, so all
are linear: each is registered for net AND new land, re-mined and stopped, and net = new + re-mined - stopped holds
(asserted). One treated unit: no standard errors anywhere, by design.

Windows from definitions: main = pre (2016-18) vs during (2019-21); placebo = fake start 2016 (2013-15 vs 2016-18);
persistence = pre vs later years (2022-25). Multi-unit controls are EQUAL-WEIGHT MEANS of the units' net additions
(as in the event study) unless the spec says "summed". "Amazon" pool = definitions.AMAZON_BZ (one filter for all
modules). The v2 checks of the workbook's "rest of Madre de Dios" definition and of buffer-zone overlaps are gone:
the raster registry is an exclusive partition (raster_zones.py), and the workbook is only a reconciliation check.
"""
from __future__ import annotations
import pandas as pd

from common import OUT
import definitions as D
import zonedata as Z
import peru

T, AM, BA = D.TREATED_ZONE, "amarakaeri_bz", "bahuaja_bz"
MEAS = ["net"] + D.PARTS
WINDOWS = {  # name -> (pre, post)
    "main": (D.PERIODS["pre"], D.PERIODS["during"]),
    "placebo": (D.PLACEBO_PERIODS["pre"], D.PLACEBO_PERIODS["during"]),
    "persistence": (D.PERIODS["pre"], D.PERIODS["later"]),
}
SRC = D.SOURCE


def _lab(w):
    (a, b), (c, d) = w
    return f"{a}–{str(b)[2:]} vs {c}–{str(d)[2:]}"


def _did(t: pd.Series, c: pd.Series, pre, post) -> float:
    return (Z.period_mean(t, post) - Z.period_mean(t, pre)) - (Z.period_mean(c, post) - Z.period_mean(c, pre))


def run(pack, reg):
    print("\n== Peru robustness (v3: net additions, raster registry) ==")
    bz, _, poolB_all = peru.pools()
    W = {m: Z.wide(bz, D.COLS[m]) for m in MEAS}
    R = {m: Z.wide(Z.region_units(), D.COLS[m]) for m in MEAS}
    code = bz.groupby("unit").bz_code.first()
    poolB = [u for u in poolB_all if u != T]
    amz = [u for u in poolB if code[u] in D.AMAZON_BZ]
    controls = {   # sid: (name, function measure -> series, note)
        "amarakaeri": ("Amarakaeri buffer zone (main)", lambda m: W[m][AM],
                       "Main control; partly treated too (Mercurio II covered all of Madre de Dios)"),
        "bahuaja": ("Bahuaja-Sonene buffer zone", lambda m: W[m][BA], "Tiny pre-period mining: a weak counterfactual"),
        "ama_bah_mean": ("Amarakaeri + Bahuaja-Sonene, equal-weight mean", lambda m: (W[m][AM] + W[m][BA]) / 2, ""),
        "ama_bah_sum": ("Amarakaeri + Bahuaja-Sonene, summed", lambda m: W[m][AM] + W[m][BA], "Scale mismatch; do not cite"),
        "corridor_outside_bz": ("Mining corridor outside buffer zones (Madre de Dios)",
                                lambda m: R[m]["corridor_outside_bz"], "Legal corridor: a likely destination of "
                                "displaced miners, so spillovers bias the DiD away from zero"),
        "communities": ("Native communities (Madre de Dios, outside buffer zones)", lambda m: R[m]["communities"], ""),
        "rest_mdd": ("Rest of Madre de Dios (outside every other zone)", lambda m: R[m]["rest_mdd"], "Little mining"),
        "amazon_pool": (f"Other Amazon buffer zones with 2014-18 mining (n={len(amz)}), mean",
                        lambda m: W[m][amz].mean(axis=1), "definitions.AMAZON_BZ"),
        "all_peru_poolB": (f"All other Peruvian buffer zones with 2014-18 mining (n={len(poolB)}), mean",
                           lambda m: W[m][poolB].mean(axis=1), "Event-study pool B; includes non-Amazon zones"),
    }
    rows = []
    for sid, (name, f, note) in controls.items():
        for w, (pre, post) in WINDOWS.items():
            vals = {m: _did(W[m][T], f(m), pre, post) for m in MEAS}
            assert abs(vals["net"] - (vals["new"] + vals["remined"] - vals["stopped"])) < 0.01
            per = _lab((pre, post))
            Z.register_parts(reg, f"robust_did_{w}_{sid}", vals, T, per,
                             f"DiD of period means, Tambopata buffer zone minus [{name}], {w} windows"
                             + ("; SUM of controls, scale mismatch, do not cite" if sid == "ama_bah_sum" else "")
                             + ("; PLACEBO: no real treatment" if w == "placebo" else ""), source=SRC)
            rows.append(dict(spec=f"(a) {w}: control = {name}", window=per, note=note,
                             **{f"did_{m}": round(vals[m], 1) for m in MEAS}))

    # ---- (b) drop the largest control unit (by mean net addition 2014-18)
    a, b = D.PERIODS["pre_long"]
    pre = W["net"].loc[a:b].mean()
    big_B = pre[poolB].idxmax()
    poolA = [AM, BA]
    big_A = pre[poolA].idxmax()
    print(f"Largest pre-2019 control: pool B = {big_B} ({pre[big_B]:,.0f} ha/yr); pool A = {big_A} ({pre[big_A]:,.0f})")
    specs = [(f"pool B without {Z.bz_name(big_B)}", [u for u in poolB if u != big_B], "poolB_drop_largest"),
             (f"pool A without {Z.bz_name(big_A)}", [u for u in poolA if u != big_A], "poolA_drop_largest"),
             ("pool B full", poolB, "poolB_full")]
    for lab, units, sid in specs:
        bm = {m: peru.beta(W[m][[T] + units], T) for m in MEAS}
        for key in ("during", "later"):
            lo, hi = D.PERIODS[key]
            vals = {m: float(bm[m].loc[lo:hi].mean()) for m in MEAS}
            assert abs(vals["net"] - (vals["new"] + vals["remined"] - vals["stopped"])) < 0.01
            Z.register_parts(reg, f"robust_es_{sid}_{key}", vals, T, D.period_label(key),
                             f"mean event-study coefficient (reference {D.REF_YEAR}), Tambopata buffer zone vs {lab} "
                             f"({len(units)} zones, equal weights)", source=SRC)
            rows.append(dict(spec=f"(b) event study (ref {D.REF_YEAR}), {lab}", window=D.period_label(key),
                             note=f"{len(units)} zones", **{f"did_{m}": round(vals[m], 1) for m in MEAS}))
    # displacement into the two other Madre de Dios-linked buffer zones (Tambopata dropped)
    for key in ("during", "later"):
        vals = {m: Z.period_mean(W[m][AM] + W[m][BA], key) - Z.period_mean(W[m][AM] + W[m][BA], "pre") for m in MEAS}
        Z.register_parts(reg, f"robust_displ_two_zones_chg_{key}", vals, "amarakaeri_bz + bahuaja_bz",
                         f"{D.period_label('pre')} vs {D.period_label(key)}", "change in the period mean, Amarakaeri + "
                         "Bahuaja-Sonene buffer zones summed (positive = the neighbours gained); not a DiD", source=SRC)
        rows.append(dict(spec="(b) displacement: Amarakaeri + Bahuaja-Sonene summed, change in mean",
                         window=f"{D.period_label('pre')} vs {D.period_label(key)}", note="not a DiD",
                         **{f"did_{m}": round(vals[m], 1) for m in MEAS}))
    tab = pd.DataFrame(rows)
    tab.to_csv(OUT / "peru_robustness.csv", index=False)
    print(tab[["spec", "window", "did_net", "did_new", "did_remined", "did_stopped"]].to_string(index=False, max_colwidth=90))
    return tab


if __name__ == "__main__":
    from common import Numbers, load_pack
    reg = Numbers(); run(load_pack(), reg)
