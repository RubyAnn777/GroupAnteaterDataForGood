"""The economics of mining in Madre de Dios: gold, taxes, social cost and enforcement money. INFORMED SPECULATION.

Every outside parameter below is cited (full quotes, pages and URLs: docs/overnight/notes/economics_sources.md, accessed
2026-10-13); every result is our arithmetic on those parameters and on our own mapped hectares, given as a LOW-HIGH range.
None of it is a measured quantity: the brief must not present it as one. Numbers carry claim_type "prediction" only where
they are forward-looking; the rest are "description" of a calculation, and every description says "informed speculation".

MEASURE (plan v3, decision 5): gold comes out of land being WORKED, so the physically relevant flow is land newly mined
or re-mined (gross, ha/yr), NOT net additions (net subtracts land that stopped, which yields no gold). Registered with
measure "new" (first-time land, the base of the gold range) and "new+remined" (all land worked).
Chain (per year, Madre de Dios part of the zone registry, in_mdd = 1, 2022-25 unless stated):
  hectares worked   = land mined for the first time (new land); re-mined old pits reported as hectares only
                                                                                           [MapBiomas, ours]
  gold (kg)         = first-time hectares x 1.6 (low) ... 1.9 (high) kg Au/ha                          [CSF-PE 2023, Cuadro 3]
                      Old pits get NO gold: CSF's yields are for fresh 2.5 m pits, and CSF found no grades at all for
                      suction-pump mining (p.22), La Pampa's method. So both ends understate gold if old pits still pay.
  value (US$)       = gold x mean gold price 2022-25                                                    [prices_annual.csv]
  declared share    = gold declared by producers (MINEM, after the 2020 definition change) / gold      [MINEM, ours]
  tax not paid      = undeclared value x 29.5% income tax x 11-37% profit margin; regalia 0% for small producers
                                                                                  [D.L. 1269; Torres 2015 via MINAM 2016]
  mercury           = gold x 2.4 ... 2.8 kg Hg per kg Au                                                [CSF-PE p.43]
  social cost       = two CSF estimates, kept SEPARATE (different models / vintages):
                      calculator web page US$ 81,000-364,000 per kg; CSF-PE report p.7 US$ 1.2-1.8 M per kg
  enforcement money = PP 0128 spending booked in Madre de Dios, soles -> US$ at each year's BCRP annual average
                      exchange rate (PEN_PER_USD below)
Cost per hectare kept from mining in the target, 2019-21 = PP 0128 Madre de Dios spending 2019-21 / (|gap| x 3), gap =
peru.py's pooled-reference event-study gap in NET additions, Tambopata buffer zone vs every Peruvian buffer zone with
pre-2019 mining (es_poolB_pooledref_during_net, raster net additions, 2019-21 vs 2014-18).
It is an upper-bound effect on the target only: the region mined MORE, so these hectares moved, they weren't saved.
"""
from __future__ import annotations
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from common import ROOT, OUT, finish_figure, headline, C, INK, INK2, MUTED, GRID, AXIS
import raster_zones as rz
import definitions as D

SRC = "docs/overnight/notes/economics_sources.md (cited parameters) x MapBiomas Peru Col 4 rasters, MINEM, MEF PP 0128, prices_annual.csv"
OZ_G = 31.1034768
P = dict(   # parameter: (low, high, source)
    yield_kg_ha=(1.6, 1.9, "CSF-PE (Gasparinetti et al., CSF 2023) PDF p.22, Cuadro 3: Puquiri 1.6, Malinowski 1.7, Huepetuhe 1.9 kg Au/ha, 2.5 m pit; no grades found for suction-pump mining (p.22)"),
    margin=(0.11, 0.368, "Torres (2015, CooperAcción) via MINAM (2016) p.74-75: profit margin 11.0 / 23.9 / 36.8%"),
    income_tax=(0.295, 0.295, "D.L. 1269 / general regime: 29.5% income tax (RMT 10% on the first 15 UIT ignored)"),
    hg_per_au=(2.4, 2.8, "CSF-PE PDF p.43: Hg:Au 2.6:1, Peru range 2.4-2.8"),
    social_calc_usd_kg=(81_000, 364_000, "CSF Mining Impacts Calculator, Work Methodology page (miningcalculator.conservation-strategy.org/methodology/resume, opened 2026-10-13): 'In the case of Peru, 1 kg of gold generates socio-environmental impacts worth between US$81,000 and US$364,000.'"),
    social_pdf_usd_kg=(1_200_000, 1_800_000, "CSF-PE PDF p.7: 1 kg of gold causes US$ 1.2-1.8 M of impacts, mostly mercury and health"),
)
# BCRP, tipo de cambio promedio del periodo, S/ per US$, series PN01234PM (monthly; raw API file in data_raw/bcrp/,
# logged in DOWNLOAD_LOG.csv); annual value = mean of the 12 monthly averages.
def _pen_per_usd() -> dict[int, float]:
    import json
    d = json.loads((ROOT / "data_raw/bcrp/bcrp_monthly_pen_per_usd_PN01234PM_2015_2025.json").read_text(encoding="utf-8"))
    s = pd.Series({p["name"]: float(p["values"][0]) for p in d["periods"]})
    by_year = s.groupby(s.index.str[-4:].astype(int))
    assert (by_year.size() == 12).all(), "BCRP exchange rate: every year needs 12 months"
    return by_year.mean().to_dict()
PEN_PER_USD = _pen_per_usd()


def mdd_year():
    """Land newly mined and re-mined per year, Madre de Dios part (zone_year.csv, in_mdd = 1)."""
    z = pd.read_csv(rz.OUT_ZONE)
    return z[z.in_mdd == 1].groupby("year")[["new_ha", "remined_ha"]].sum()


def run(pack, reg):
    def add(id_, v, unit, desc, claim="description", measure="", period=""):
        kw = dict(measure=measure, zone="mdd", period=period) if measure else {}
        reg.add(f"eco_{id_}", v, unit, desc + " Informed speculation (cited parameters, our arithmetic).", claim, SRC, **kw)
    for k, (lo, hi, src) in P.items():
        add(f"param_{k}_lo", lo, k, f"Parameter {k}, low: {src}.")
        add(f"param_{k}_hi", hi, k, f"Parameter {k}, high: {src}.")
    for yy, r in PEN_PER_USD.items():
        add(f"param_pen_per_usd_{yy}", r, "soles per US$", f"BCRP annual average exchange rate {yy} (series PN01234PM, mean of 12 monthly averages).")
    y = mdd_year()
    gold = pack["prices"].set_index("year")["gold"]
    minem = pd.read_csv(ROOT / "data_intermediate" / "minem_mdd_gold.csv").set_index("year")
    spend = pd.Series({yy: reg.get(f"t8_pp0128_mdd_{yy}") for yy in range(2015, 2026)})
    out = {}
    for key in ("pre", "later"):
        (a, b), per, pl = D.PERIODS[key], key, D.period_label(key)
        new, rem = y.loc[a:b, "new_ha"].mean(), y.loc[a:b, "remined_ha"].mean()
        usd_g = gold.loc[a:b].mean() / OZ_G
        kg = (new * P["yield_kg_ha"][0], new * P["yield_kg_ha"][1])     # first-time land only (old pits: no yield known)
        val = tuple(k * 1000 * usd_g for k in kg)
        out[per] = dict(new=new, rem=rem, kg=kg, val=val, usd_g=usd_g)
        add(f"ha_low_{per}", new, "ha/yr", f"Hectares worked per year, low = land mined for the first time (new land; "
            f"not net additions), Madre de Dios, {pl}.", measure="new", period=pl)
        add(f"ha_high_{per}", new + rem, "ha/yr", f"Hectares worked per year, high = land newly mined or re-mined (ha/yr; "
            f"not net additions), Madre de Dios, {pl} (hectares only; old pits are given no gold below).",
            measure="new+remined", period=pl)
        add(f"gold_t_lo_{per}", kg[0] / 1000, "t/yr", f"Gold from mapped mining, low = new land (first-time mined) x 1.6 kg/ha, Madre de Dios, {pl}. Old pits excluded (no yield known), so this understates gold if they still pay.")
        add(f"gold_t_hi_{per}", kg[1] / 1000, "t/yr", f"Gold from mapped mining, high = new land x 1.9 kg/ha, {pl}. Old pits excluded, as in the low case.")
        add(f"value_musd_lo_{per}", val[0] / 1e6, "million US$/yr", f"Gross value of that gold at the {pl} mean price, low.")
        add(f"value_musd_hi_{per}", val[1] / 1e6, "million US$/yr", f"Same, high.")
    # cross-check: gold per hectare implied by MINEM's own estimate (declared + artisanal estimate), 2016-18
    a0, a1 = D.PERIODS["pre"]
    k1618 = minem.loc[a0:a1, "total_kg"].mean()
    ha1618 = (y.loc[a0:a1, "new_ha"] + y.loc[a0:a1, "remined_ha"]).mean()
    add("implied_kg_ha_pre", k1618 / ha1618, "kg/ha", "MINEM gold for Madre de Dios (declared + artisanal estimate), 2016-18 mean, per hectare worked (land newly mined or re-mined, our raster accounting; not net additions). Cross-check of the CSF yield of 1.6-1.9 kg/ha (same order; river dredges add gold but no mapped land).", measure="new+remined", period="2016–18")
    add("implied_kg_ha_new_pre", k1618 / y.loc[a0:a1, "new_ha"].mean(), "kg/ha", "Same, per hectare of new land (first-time mined) only (the base of our gold range): above the CSF yield, so a range built on new land x 1.6-1.9 kg/ha is if anything low.", measure="new", period="2016–18")
    o = out["later"]
    decl = minem.loc[D.PERIODS["later"][0]:D.PERIODS["later"][1], "declared_kg"].mean()
    add("declared_t_2022_25", decl / 1000, "t/yr", "Gold declared by producers in Madre de Dios, 2022-25 mean (MINEM; no artisanal estimate after 2019).")
    sh = (decl / o["kg"][1], decl / o["kg"][0])
    add("declared_share_lo", sh[0], "share", "Declared gold as a share of gold from mapped mining, 2022-25, low.")
    add("declared_share_hi", sh[1], "share", "Same, high.")
    und = tuple(max(o["kg"][i] - decl, 0) * 1000 * o["usd_g"] for i in (0, 1))
    tax = (und[0] * P["income_tax"][0] * P["margin"][0], und[1] * P["income_tax"][1] * P["margin"][1])
    add("tax_musd_lo", tax[0] / 1e6, "million US$/yr", "Income tax not paid on undeclared Madre de Dios gold, 2022-25, low (29.5% x 11% margin). Royalty for small producers is 0%, so nothing is lost there.")
    add("tax_musd_hi", tax[1] / 1e6, "million US$/yr", "Same, high (29.5% x 36.8% margin).")
    add("tax_share_value_lo", P["income_tax"][0] * P["margin"][0], "share", "Tax wedge: income tax as a share of gold value, low.")
    add("tax_share_value_hi", P["income_tax"][1] * P["margin"][1], "share", "Tax wedge, high.")
    hg = (o["kg"][0] * P["hg_per_au"][0], o["kg"][1] * P["hg_per_au"][1])
    add("hg_t_lo", hg[0] / 1000, "t/yr", "Mercury used, Madre de Dios, 2022-25, low.")
    add("hg_t_hi", hg[1] / 1000, "t/yr", "Mercury used, high.")
    soc = {}
    for k, nm in (("calc", "CSF calculator web page, US$ 81,000-364,000 per kg"), ("pdf", "CSF 2023 report p.7, US$ 1.2-1.8 M per kg")):
        pr = P[f"social_{k}_usd_kg"]
        soc[k] = (o["kg"][0] * pr[0], o["kg"][1] * pr[1])
        add(f"social_busd_{k}_lo", soc[k][0] / 1e9, "billion US$/yr", f"Social cost of the gold mined (health, forest, rivers), Madre de Dios 2022-25, low gold x low cost, {nm}.")
        add(f"social_busd_{k}_hi", soc[k][1] / 1e9, "billion US$/yr", f"Same, high gold x high cost, {nm}.")
    spu = float(np.mean([spend[yy] / PEN_PER_USD[yy] for yy in range(D.PERIODS["later"][0], D.PERIODS["later"][1] + 1)]))
    add("spend_musd", spu / 1e6, "million US$/yr", "PP 0128 spending booked in Madre de Dios, 2022-25 mean, each year converted at its BCRP annual average exchange rate (a lower bound: national units book under Lima).")
    add("spend_share_of_value", spu / o["val"][0], "share", "Enforcement money as a share of the gold value mined (low), 2022-25: the most generous ratio.")
    # cost per hectare kept from mining in the target, 2019-21
    d0, d1 = D.PERIODS["during"]
    gap = abs(reg.get("es_poolB_pooledref_during_net")) * (d1 - d0 + 1)
    s1921 = spend.loc[d0:d1].sum()
    add("soles_per_ha_kept", s1921 / gap, "soles/ha", "PP 0128 Madre de Dios spending 2019-21 divided by hectares of net mining additions kept out of the Tambopata buffer zone (peru.py es_poolB_pooledref_during_net: raster net additions, Tambopata buffer zone vs every Peruvian buffer zone with pre-2019 mining, 2019-21 vs 2014-18, x 3 years; an upper-bound effect, local only, and conditional on that comparison). Numerator and denominator differ in scope: the money is ALL PP 0128 spending booked in Madre de Dios (not only Tambopata, and missing national units booked under Lima), the hectares are the Tambopata buffer zone only; the direction of the bias is unclear.", measure="net", period="2019–21 vs 2014–18")
    usd_g1921 = gold.loc[d0:d1].mean() / OZ_G
    add("gold_usd_per_ha_1921_lo", P["yield_kg_ha"][0] * 1000 * usd_g1921, "US$/ha", "Gold value of one hectare at the 2019-21 price, low.")
    add("gold_usd_per_ha_1921_hi", P["yield_kg_ha"][1] * 1000 * usd_g1921, "US$/ha", "Same, high.")
    add("gold_usd_per_ha_2025_lo", P["yield_kg_ha"][0] * 1000 * gold.loc[2025] / OZ_G, "US$/ha", "Gold value of one hectare at the 2025 price, low: why old pits are worth re-mining.")
    add("gold_usd_per_ha_2025_hi", P["yield_kg_ha"][1] * 1000 * gold.loc[2025] / OZ_G, "US$/ha", "Same, high.")
    figure(o, decl, tax, soc, spu)


def figure(o, decl, tax, soc, spu):
    rows = [("Gold mined (gross value)", o["val"], C["gold"]),
            ("Gold declared by producers", (decl * 1000 * o["usd_g"],) * 2, C["gold_tint"]),
            ("Social cost, CSF calculator (US\\$ 81–364 k per kg)", soc["calc"], C["native"]),
            ("Social cost, CSF 2023 report (US\\$ 1.2–1.8 M per kg)", soc["pdf"], C["native"]),
            ("Income tax not paid", tax, C["other"]),
            ("Enforcement money (PP 0128, Madre de Dios)", (spu, spu), INK2)]
    fig, ax = plt.subplots(figsize=(9, 4.9))
    headline(fig, "Each year, mining's damage and gold dwarf the money spent stopping it",
             "Madre de Dios, per year, 2022–25, US$ (log scale). Bars = low–high range from cited parameters. "
             "Informed speculation, not measurement")
    ys = np.arange(len(rows))[::-1]
    def f(v):
        if v >= 1e9: return f"\\${v/1e9:,.1f} bn"
        if v >= 1e7: return f"\\${v/1e6:,.0f} M"
        return f"\\${v/1e6:,.1f} M"
    for y_, (lab, (lo, hi), col) in zip(ys, rows):
        if hi / lo < 1.15:
            ax.scatter([lo], [y_], s=70, color=col, zorder=3)
        else:
            ax.plot([lo, hi], [y_, y_], color=col, lw=9, solid_capstyle="round", zorder=3)
        ax.text(hi * 1.35, y_, f(lo) if hi / lo < 1.15 else f"{f(lo)} – {f(hi)}", va="center", fontsize=8.5, color=INK, fontweight="semibold")
        ax.text(1.2e6, y_ + 0.3, lab, va="bottom", fontsize=8.5, color=INK2)
    ax.set_xscale("log"); ax.set_xlim(1e6, 3e11)
    ax.set_xticks([1e6, 1e7, 1e8, 1e9, 1e10, 1e11])
    ax.set_xticklabels(["\\$1 M", "\\$10 M", "\\$100 M", "\\$1 bn", "\\$10 bn", "\\$100 bn"])
    ax.set_yticks([]); ax.set_ylim(-0.6, len(rows) - 0.2)
    for sp in ("top", "right", "left"): ax.spines[sp].set_visible(False)
    ax.xaxis.grid(True, color=GRID, lw=0.6); ax.set_axisbelow(True)
    finish_figure(fig, "Sources: our new land, first-time mined hectares (MapBiomas Peru Col 4; old pits given no gold; not net additions) x CSF (2023) 1.6–1.9 kg gold/ha; "
                       "World Bank gold price; MINEM declared gold; income tax 29.5% x 11–37% margin (D.L. 1269; Torres 2015); social "
                       "cost: two CSF estimates shown separately; MEF PP 0128 at BCRP annual exchange rates. Full citations: "
                       "docs/overnight/notes/economics_sources.md.",
                  OUT / "fig_v2_economics.png")


if __name__ == "__main__":
    from common import Numbers, load_pack
    import csv
    reg = Numbers()
    for r in csv.DictReader(open(OUT / "numbers.csv")):
        if r["id"].startswith(("t8_", "es_poolB_pooledref_during_net")):
            reg.rows[r["id"]] = dict(value=float(r["value"]))
    run(load_pack(), reg)
    for k, v in reg.rows.items():
        if k.startswith("eco_") and not k.startswith("eco_param"):
            print(k, round(v["value"], 3))
