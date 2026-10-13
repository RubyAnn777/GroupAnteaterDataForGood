"""The economics of mining in Madre de Dios: gold, taxes, social cost and enforcement money. INFORMED SPECULATION.

Every outside parameter below is cited (full quotes, pages and URLs: docs/overnight/notes/economics_sources.md, accessed
2026-10-13); every result is our arithmetic on those parameters and on our own mapped hectares, given as a LOW-HIGH range.
None of it is a measured quantity: the brief must not present it as one. Numbers carry claim_type "prediction" only where
they are forward-looking; the rest are "description" of a calculation, and every description says "informed speculation".

Chain (per year, Madre de Dios, 2022-25 unless stated):
  hectares worked   = land mined for the first time (low) ... first-time + returns to old pits (high)  [MapBiomas, ours]
  gold (kg)         = hectares x 1.7 (low) ... 1.9 (high) kg Au/ha                                     [CSF-PE 2023, Cuadro 3]
  value (US$)       = gold x mean gold price 2022-25                                                    [prices_annual.csv]
  declared share    = gold declared by producers (MINEM, after the 2020 definition change) / gold      [MINEM, ours]
  tax not paid      = undeclared value x 29.5% income tax x 11-37% profit margin; regalia 0% for small producers
                                                                                  [D.L. 1269; Torres 2015 via MINAM 2016]
  mercury           = gold x 2.4 ... 2.8 kg Hg per kg Au                                                [CSF-PE p.47]
  social cost       = gold x US$ 81,000 (CSF calculator) ... 1.8 M (CSF-PE, mostly mercury health) per kg
  enforcement money = PP 0128 spending booked in Madre de Dios, soles -> US$ at 3.3-3.9 soles per US$
                      (rough range of BCRP annual averages 2019-25; verify before citing)
Cost per hectare kept from mining in the target, 2019-21 = PP 0128 Madre de Dios spending 2019-21 / (|M1 gap| x 3).
It is an upper-bound effect on the target only: the region mined MORE, so these hectares moved, they weren't saved.
"""
from __future__ import annotations
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from common import ROOT, OUT, finish_figure, headline, C, INK, INK2, MUTED, GRID, AXIS
import raster_zones as rz

SRC = "docs/overnight/notes/economics_sources.md (cited parameters) x MapBiomas Peru Col 4 rasters, MINEM, MEF PP 0128, prices_annual.csv"
OZ_G = 31.1034768
P = dict(   # parameter: (low, high, source)
    yield_kg_ha=(1.7, 1.9, "CSF-PE (Gasparinetti et al., CSF 2023) p.22-23, Cuadro 3: 1.7-1.9 kg Au/ha, 2.5 m pit"),
    margin=(0.11, 0.368, "Torres (2015, CooperAcción) via MINAM (2016) p.74-75: profit margin 11.0 / 23.9 / 36.8%"),
    income_tax=(0.295, 0.295, "D.L. 1269 / general regime: 29.5% income tax (RMT 10% on the first 15 UIT ignored)"),
    hg_per_au=(2.4, 2.8, "CSF-PE p.47: Hg:Au 2.6:1, Peru range 2.4-2.8"),
    social_usd_kg=(81_000, 1_800_000, "CSF calculator (US$ 81,000-364,000/kg) to CSF-PE p.7 (US$ 1.2-1.8 M/kg)"),
    pen_per_usd=(3.3, 3.9, "rough range of BCRP annual average exchange rates 2019-25 (verify)"),
)


def mdd_year():
    z = pd.read_csv(rz.OUT_ZONE)
    return z.groupby("year")[["new_land_ha", "remined_ha"]].sum()


def run(pack, reg):
    def add(id_, v, unit, desc, claim="description"):
        reg.add(f"eco_{id_}", v, unit, desc + " Informed speculation (cited parameters, our arithmetic).", claim, SRC)
    for k, (lo, hi, src) in P.items():
        add(f"param_{k}_lo", lo, k, f"Parameter {k}, low: {src}.")
        add(f"param_{k}_hi", hi, k, f"Parameter {k}, high: {src}.")
    y = mdd_year()
    gold = pack["prices"].set_index("year")["gold"]
    minem = pd.read_csv(ROOT / "data_intermediate" / "minem_mdd_gold.csv").set_index("year")
    spend = pd.Series({yy: reg.get(f"t8_pp0128_mdd_{yy}") for yy in range(2015, 2026)})
    out = {}
    for per, (a, b) in {"2016_18": (2016, 2018), "2022_25": (2022, 2025)}.items():
        new, rem = y.loc[a:b, "new_land_ha"].mean(), y.loc[a:b, "remined_ha"].mean()
        usd_g = gold.loc[a:b].mean() / OZ_G
        kg = (new * P["yield_kg_ha"][0], (new + rem) * P["yield_kg_ha"][1])
        val = tuple(k * 1000 * usd_g for k in kg)
        out[per] = dict(new=new, rem=rem, kg=kg, val=val, usd_g=usd_g)
        add(f"ha_low_{per}", new, "ha/yr", f"Hectares worked per year, low = first-time mining, Madre de Dios, {per}.")
        add(f"ha_high_{per}", new + rem, "ha/yr", f"Hectares worked per year, high = first-time + returns to old pits, {per}.")
        add(f"gold_t_lo_{per}", kg[0] / 1000, "t/yr", f"Gold from mapped mining, low, Madre de Dios, {per}.")
        add(f"gold_t_hi_{per}", kg[1] / 1000, "t/yr", f"Gold from mapped mining, high, {per}.")
        add(f"value_musd_lo_{per}", val[0] / 1e6, "million US$/yr", f"Gross value of that gold at the {per} mean price, low.")
        add(f"value_musd_hi_{per}", val[1] / 1e6, "million US$/yr", f"Same, high.")
    # cross-check: gold per hectare implied by MINEM's own estimate (declared + artisanal estimate), 2016-18
    k1618 = minem.loc[2016:2018, "total_kg"].mean()
    ha1618 = (y.loc[2016:2018, "new_land_ha"] + y.loc[2016:2018, "remined_ha"]).mean()
    add("implied_kg_ha_2016_18", k1618 / ha1618, "kg/ha", "MINEM gold for Madre de Dios (declared + artisanal estimate), 2016-18 mean, per hectare worked (first-time + old pits). Cross-check of the CSF yield.")
    o = out["2022_25"]
    decl = minem.loc[2022:2025, "declared_kg"].mean()
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
    soc = (o["kg"][0] * P["social_usd_kg"][0], o["kg"][1] * P["social_usd_kg"][1])
    add("social_busd_lo", soc[0] / 1e9, "billion US$/yr", "Social cost of the gold mined (health, forest, rivers), 2022-25, low.")
    add("social_busd_hi", soc[1] / 1e9, "billion US$/yr", "Same, high.")
    sp = spend.loc[2022:2025].mean()
    spu = (sp / P["pen_per_usd"][1], sp / P["pen_per_usd"][0])
    add("spend_musd_lo", spu[0] / 1e6, "million US$/yr", "PP 0128 spending booked in Madre de Dios, 2022-25 mean, in US$, low (a lower bound: national units book under Lima).")
    add("spend_musd_hi", spu[1] / 1e6, "million US$/yr", "Same, high.")
    add("spend_share_of_value", spu[1] / o["val"][0], "share", "Enforcement money (high) as a share of the gold value mined (low), 2022-25: the most generous ratio.")
    # cost per hectare kept from mining in the target, 2019-21
    gap = abs(reg.get("model_m1_during")) * 3
    s1921 = spend.loc[2019:2021].sum()
    add("soles_per_ha_kept", s1921 / gap, "soles/ha", "PP 0128 Madre de Dios spending 2019-21 divided by hectares of net mining kept out of the Tambopata buffer zone (M1 gap x 3 years; upper-bound effect, local only).")
    usd_g1921 = gold.loc[2019:2021].mean() / OZ_G
    add("gold_usd_per_ha_1921_lo", P["yield_kg_ha"][0] * 1000 * usd_g1921, "US$/ha", "Gold value of one hectare at the 2019-21 price, low.")
    add("gold_usd_per_ha_1921_hi", P["yield_kg_ha"][1] * 1000 * usd_g1921, "US$/ha", "Same, high.")
    add("gold_usd_per_ha_2025_lo", P["yield_kg_ha"][0] * 1000 * gold.loc[2025] / OZ_G, "US$/ha", "Gold value of one hectare at the 2025 price, low: why old pits are worth re-mining.")
    add("gold_usd_per_ha_2025_hi", P["yield_kg_ha"][1] * 1000 * gold.loc[2025] / OZ_G, "US$/ha", "Same, high.")
    figure(o, decl, tax, soc, spu)


def figure(o, decl, tax, soc, spu):
    rows = [("Gold mined (gross value)", o["val"], C["gold"]),
            ("Gold declared by producers", (decl * 1000 * o["usd_g"],) * 2, C["corridor"]),
            ("Social cost (health, forest, rivers)", soc, C["native"]),
            ("Income tax not paid", tax, C["other"]),
            ("Enforcement money (PP 0128, Madre de Dios)", spu, C["reserve"])]
    fig, ax = plt.subplots(figsize=(9, 4.4))
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
    finish_figure(fig, "Sources: our mapped hectares (MapBiomas Peru Col 4) x CSF (2023) 1.7–1.9 kg gold/ha; World Bank gold price; "
                       "MINEM declared gold; income tax 29.5% x 11–37% margin (D.L. 1269; Torres 2015); social cost US\\$ 81 k–1.8 M "
                       "per kg (CSF); MEF PP 0128 at 3.3–3.9 soles per US dollar. Full citations: docs/overnight/notes/economics_sources.md.",
                  OUT / "fig_v2_economics.png")


if __name__ == "__main__":
    from common import Numbers, load_pack
    import csv
    reg = Numbers()
    for r in csv.DictReader(open(OUT / "numbers.csv")):
        if r["id"].startswith(("t8_", "model_m1_during")):
            reg.rows[r["id"]] = dict(value=float(r["value"]))
    run(load_pack(), reg)
    for k, v in reg.rows.items():
        if k.startswith("eco_") and not k.startswith("eco_param"):
            print(k, round(v["value"], 3))
