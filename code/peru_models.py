"""Peru model ladder: can controls (gold price, trends, size) rescue a causal reading of Mercurio?

Panel: every Peruvian buffer zone with non-zero mining additions in 2014-18 (event-study pool B, 15 zones),
outcome = annual addition to mining area (ha), MapBiomas Peru Collection 4. Tambopata = treated from 2019.
Treatment dummies: Tambopata x 2019-21 ("during") and Tambopata x 2022-25 ("after").

  M1  zone + year fixed effects. Year effects absorb anything that hits every zone in the same year:
      the gold price, COVID, national policy. So the gold price IS controlled for, as a common shock.
  M2  M1 + gold-price sensitivity: (zone's mean addition 2014-18) x ln(gold price). Big mining zones may react
      more to a price rise than small ones; this lets them.
  M3  M1 + a separate linear trend per zone (one control zone's trend dropped: collinear with year effects).
  M4  M1 with the outcome scaled by each zone's own mean addition 2014-18 (1 = a normal pre-2019 year),
      zones with mean > 10 ha/yr only, so Tambopata's size cannot drive the result.

Each model is checked two ways, because one treated zone makes standard errors uninformative:
  - placebo in time: same model on 2011-18 with a fake operation in 2016 (should be ~0);
  - placebo in space: give the "operation" to each other zone in turn; rank Tambopata (1 = biggest fall).
All results are DESCRIPTION. A model only supports a causal reading if its placebo-in-time is small AND
Tambopata ranks first. Written to output/peru_models.csv and output/fig_peru_models.png.
"""
from __future__ import annotations
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pyfixest as pf

from common import OUT, style_axes, finish_figure, SRC_MAPBIOMAS, SRC_PRICE, headline, C, INK, INK2, GRID

TU = "Tambopata|Reserva Nacional"
SRC = "peru_bufferzone_year.csv, prices_annual.csv"
TITLE = "In hectares, every model shows a big 2019–21 fall; scaled to size, it ranks {rank} of {n}"
MODELS = {
    "M1": "Zone + year effects (gold price, COVID as common shocks)",
    "M2": "M1 + bigger zones react more to the gold price",
    "M3": "M1 + own linear trend per zone",
    "M4": "M1, scaled to each zone's own size",
}

# Buffer zones whose mining lies in Amazon (lowland/forest) departments: drops coastal and high-Andean zones
# (Lachay, Huascaran, Junin, Cotahuasi, Nor Yauyos, Calipuy, Rio Abiseo) from the Amazon-only placebo pool.
AMAZON = {"Tambopata|Reserva Nacional", "Amarakaeri|Reserva Comunal", "Bahuaja-Sonene|Parque Nacional",
          "Allpahuayo Mishana|Reserva Nacional", "Cordillera Azul|Parque Nacional", "Alto Mayo|Bosque de Protección",
          "Pacaya-Samiria|Reserva Nacional", "El Sira|Reserva Comunal"}


def _zone_adds(pack) -> pd.DataFrame:
    zb = pack["zb"].assign(unit=lambda d: d["buffer_zone"] + "|" + d["pa_category"])
    return zb.groupby(["unit", "year"])["mining_ha"].sum().unstack("unit").diff()   # aggregate first, then diff

def _design(ad, units, treated, model, y0, y1, posts, gold):
    """Long panel + regressor matrix (zone and year dummies spelled out) for numpy OLS."""
    d = ad.loc[y0:y1, units].reset_index().melt(id_vars="year", var_name="unit", value_name="y")
    pre = ad.loc[2014:2018, units].mean() if y1 > 2018 else ad.loc[y0:min(y1, 2015), units].mean()
    if model == "M4":
        d["y"] = d["y"] / d["unit"].map(pre)
    X = {f"post_{k}": ((d["unit"] == treated) & d["year"].between(*v)).astype(float) for k, v in posts.items()}
    if model == "M2":
        X["pre_x_lngold"] = d["unit"].map(pre) * np.log(d["year"].map(gold))
    if model == "M3":
        drop = next(u for u in units if u != treated)          # one trend is collinear with year effects
        for u in units:
            if u != drop:
                X[f"trend_{u}"] = ((d["unit"] == u) * (d["year"] - y0)).astype(float)
    X = pd.DataFrame(X)
    fe = pd.concat([pd.get_dummies(d["unit"], drop_first=False, dtype=float),
                    pd.get_dummies(d["year"], prefix="y", drop_first=True, dtype=float)], axis=1)
    return d, X, fe

def fit(ad, units, treated, model, y0, y1, posts, gold) -> dict:
    d, X, fe = _design(ad, units, treated, model, y0, y1, posts, gold)
    M = pd.concat([X, fe], axis=1).to_numpy()
    b, *_ = np.linalg.lstsq(M, d["y"].to_numpy(), rcond=None)
    return dict(zip(X.columns, b[: X.shape[1]]))

def _check_pyfixest(ad, units, gold):
    """The numpy fit must equal pyfixest's two-way fixed-effects fit (M1 and M2)."""
    d, X, _ = _design(ad, units, TU, "M2", 2014, 2025, {"during": (2019, 2021), "after": (2022, 2025)}, gold)
    dd = pd.concat([d, X], axis=1)
    for m, rhs in [("M1", "post_during + post_after"), ("M2", "post_during + post_after + pre_x_lngold")]:
        f = pf.feols(f"y ~ {rhs} | unit + year", data=dd)
        ours = fit(ad, units, TU, m, 2014, 2025, {"during": (2019, 2021), "after": (2022, 2025)}, gold)
        assert np.isclose(f.coef()["post_during"], ours["post_during"], atol=1e-6), f"{m}: numpy != pyfixest"

def run(pack, reg):
    print("\n== Peru model ladder (gold price, trends, scaling) ==")
    ad = _zone_adds(pack)
    gold = pack["prices"].set_index("year")["gold"]
    pre = ad.loc[2014:2018].mean()
    poolB = sorted(u for u in ad.columns if ad.loc[2014:2018, u].abs().sum() > 0)
    pool_big = sorted(u for u in poolB if pre[u] > 10)
    assert TU in poolB and TU in pool_big and len(poolB) == 15
    _check_pyfixest(ad, poolB, gold)

    REAL = {"during": (2019, 2021), "after": (2022, 2025)}
    FAKE = {"fake": (2016, 2018)}
    rows = []
    for m, label in MODELS.items():
        units = pool_big if m == "M4" else poolB
        real = fit(ad, units, TU, m, 2014, 2025, REAL, gold)
        fake = fit(ad, units, TU, m, 2011, 2018, FAKE, gold)
        # placebo in space (fixed after the critical review, 12 Oct 2026): when a fake zone is "treated",
        # Tambopata is REMOVED from the pool, so its real fall cannot make every placebo look positive.
        others = {u: fit(ad, [v for v in units if v != TU], u, m, 2014, 2025, REAL, gold)["post_during"]
                  for u in units if u != TU}
        others[TU] = real["post_during"]
        rank = int(pd.Series(others).rank().loc[TU])
        amz = [u for u in units if u in AMAZON]
        oth_a = {u: fit(ad, [v for v in amz if v != TU], u, m, 2014, 2025, REAL, gold)["post_during"] for u in amz if u != TU}
        oth_a[TU] = fit(ad, amz, TU, m, 2014, 2025, REAL, gold)["post_during"]
        rank_amz = int(pd.Series(oth_a).rank().loc[TU])
        rows.append(dict(model=m, label=label, n_zones=len(units),
                         unit="share of own pre-2019 mean" if m == "M4" else "ha/yr",
                         during_2019_21=real["post_during"], after_2022_25=real["post_after"],
                         placebo_fake_2016=fake["post_fake"], rank_in_space=rank, rank_amazon=rank_amz, n_amazon=len(amz),
                         placebo_min=min(v for k, v in others.items() if k != TU), placebo_max=max(v for k, v in others.items() if k != TU),
                         gold_slope=real.get("pre_x_lngold", np.nan)))
    res = pd.DataFrame(rows)
    res.round(3).to_csv(OUT / "peru_models.csv", index=False)
    print(res.drop(columns="label").round(2).to_string(index=False))

    for r in rows:
        k, u = r["model"].lower(), r["unit"]
        lab = f"{r['model']} ({r['label']}; {r['n_zones']} zones, 2014-25)"
        reg.add(f"model_{k}_during", r["during_2019_21"], u, f"Tambopata 2019-21 coefficient, {lab}. Description: one treated zone.", "description", SRC)
        reg.add(f"model_{k}_after", r["after_2022_25"], u, f"Tambopata 2022-25 coefficient, {lab}. Description.", "description", SRC)
        reg.add(f"model_{k}_placebo", r["placebo_fake_2016"], u, f"Placebo in time: fake operation 2016-18, same model on 2011-18, {lab}", "description", SRC)
        reg.add(f"model_{k}_rank", r["rank_in_space"], "rank", f"Tambopata's rank among {r['n_zones']} zones when each zone is treated in turn (1 = biggest fall 2019-21), {lab}", "description", SRC)
        reg.add(f"model_{k}_n", r["n_zones"], "count", f"Zones in {lab}", "description", SRC)
        reg.add(f"model_{k}_ri_p", r["rank_in_space"] / r["n_zones"], "p-value", f"Randomization p-value (rank / zones; best possible = 1/{r['n_zones']}), {lab}", "description", SRC)
        reg.add(f"model_{k}_rank_amazon", r["rank_amazon"], "rank", f"Rank among Amazon-department zones only ({r['n_amazon']}), {lab}", "description", SRC)
        reg.add(f"model_{k}_n_amazon", r["n_amazon"], "count", f"Amazon-department zones, {lab}", "description", SRC)
        reg.add(f"model_{k}_placebo_min", r["placebo_min"], u, f"Smallest placebo-in-space effect (Tambopata removed from pool), {lab}", "description", SRC)
        reg.add(f"model_{k}_placebo_max", r["placebo_max"], u, f"Largest placebo-in-space effect, {lab}", "description", SRC)
    reg.add("model_m2_gold_slope", rows[1]["gold_slope"], "ha per (ha of pre mean x 1 log-point)",
            "M2: extra annual addition per hectare of a zone's 2014-18 mean addition, per 1.0 rise in ln(gold price)", "description", SRC)
    t = ad[TU]
    reg.add("tam_add_min_2011_2018", t.loc[2011:2018].min(), "ha", "Lowest annual addition, Tambopata BZ, 2011-2018", "description", SRC)
    reg.add("tam_add_max_2019_2021", t.loc[2019:2021].max(), "ha", "Highest annual addition, Tambopata BZ, 2019-2021", "description", SRC)
    reg.add("tam_add_2016", t.loc[2016], "ha", "Annual addition, Tambopata BZ, 2016 (the low year behind the event-study pre-trend coefficient)", "description", SRC)
    reg.add("tam_add_2017", t.loc[2017], "ha", "Annual addition, Tambopata BZ, 2017", "description", SRC)
    reg.add("tam_add_2018", t.loc[2018], "ha", "Annual addition, Tambopata BZ, 2018", "description", SRC)
    for y in (2019, 2020, 2021):
        reg.add(f"tam_add_{y}", t.loc[y], "ha", f"Annual addition, Tambopata BZ, {y}", "description", SRC)
    _figure(res)
    return res

def _figure(res):
    from matplotlib.ticker import FuncFormatter
    fig, axes = plt.subplots(len(res), 1, figsize=(9, 7.6), gridspec_kw={"hspace": 0.95})
    m4 = res[res["model"] == "M4"].iloc[0]
    headline(fig, TITLE.format(rank=int(m4["rank_in_space"]), n=int(m4["n_zones"])), "Tambopata minus the other zones, after zone and year effects. Orange: real operation 2019–21. "
                         "Grey: fake operation 2016–18 (should be near 0).")
    for ax, (_, r) in zip(axes, res.iterrows()):
        ax.barh([1], [r["during_2019_21"]], 0.62, color=C["lapampa"])
        ax.barh([0], [r["placebo_fake_2016"]], 0.62, color=C["other"])
        for yy, v, lab in [(1, r["during_2019_21"], "real"), (0, r["placebo_fake_2016"], "fake")]:
            txt = (f"{v:,.2f}" if r["model"] == "M4" else f"{v:,.0f}").replace("-", "−")
            ax.annotate(f"{txt}  {lab}", (v, yy), xytext=(5 if v >= 0 else -5, 0), textcoords="offset points",
                        va="center", ha="left" if v >= 0 else "right", fontsize=8.5, color=INK,
                        fontweight="semibold" if lab == "real" else "normal")
        ax.axvline(0, color=INK2, lw=0.8)
        lo = min(r["during_2019_21"], r["placebo_fake_2016"]) * 1.45
        hi = max(0, r["placebo_fake_2016"]) + abs(lo) * 0.3
        ax.set_xlim(lo, hi)
        ax.set_yticks([])
        for sp in ("top", "right", "left"):
            ax.spines[sp].set_visible(False)
        ax.xaxis.grid(True, color=GRID, lw=0.6); ax.set_axisbelow(True)
        ax.xaxis.set_major_formatter(FuncFormatter(lambda v, p: "0" if v == 0 else (f"{v:,.1f}" if abs(v) < 5 else f"{v:,.0f}").replace("-", "−")))
        unit = "1 = one normal pre-2019 year" if r["model"] == "M4" else "ha per year"
        ax.set_title(f"{r['model']}  {r['label']}", fontsize=9.5)
        ax.text(1.0, 1.04, f"{unit}  ·  rank {int(r['rank_in_space'])} of {int(r['n_zones'])}", transform=ax.transAxes,
                ha="right", va="bottom", fontsize=8, color=INK2)
    finish_figure(fig, f"{SRC_MAPBIOMAS}; {SRC_PRICE}. Outcome = new mining area per year. Rank = Tambopata's place when "
                       "each zone gets the operation in turn (1 = biggest fall). One treated zone: no confidence intervals. "
                       "Description.", OUT / "fig_peru_models.png")
