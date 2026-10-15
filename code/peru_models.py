"""Peru model ladder (plan v3): how much do controls for size, trends and the gold price move the 2019-21 gap?

Panel: the national panel of Peruvian buffer zones, whole official SERNANP polygons (zonedata.bz_panel()), every zone
with non-zero net additions in 2014-18 (pool B, 15 zones). Outcome = NET mining additions (ha/yr) = new land +
re-mined - stopped, MapBiomas Peru Collection 4 rasters, our pixel accounting. Treated unit = definitions.TREATED_ZONE
(Tambopata buffer zone) from definitions.FIRST_POST (2019). Dummies: treated x 2019-21 ("during") and treated x 2022-25
("later": later years, which contain the 2023 emergency; not "after enforcement ended"). Baseline = all 2014-18 years
(pooled reference, definitions.PERIODS["pre_long"]).

  M1  zone + year effects. The year effects remove what changed in the AVERAGE comparison zone in each year (about
      +20 ha/yr here, because the comparison zones hold little mining). They do NOT remove shocks that scale with a
      zone's size, such as a gold-price rise or COVID hitting big mining zones harder (M2 and peru_context_models try).
      So M1 is close to Tambopata's own before/after.
  M2  M1 + (zone's mean net addition 2014-18) x ln(gold price): big mining zones may react more to the price.
  M3  M1 + a linear trend per zone (one control zone's trend dropped: collinear with year effects).
      M3pre: Tambopata's post years saturated, so its trend is fitted on 2014-18 only.
  M4  M1 with the outcome divided by each zone's own mean net addition 2014-18 (1 = a normal pre-2019 year), zones
      above definitions.MIN_PRE_HA only, so Tambopata's size cannot drive the result.

Linear and additive: M1, M2 (its regressor is built from the NET pre mean and held fixed), M3, M3pre. For these the
coefficients are also estimated on new land, re-mined and stopped, and net = new + re-mined - stopped holds (asserted).
NOT additive: M4 (a ratio to the net pre mean), all ranks and randomization p-values: net only.

Each model is checked two ways, because one treated zone makes standard errors uninformative:
  - placebo in time: same model on 2011-18 with a fake start in 2016 (definitions.PLACEBO_PERIODS);
  - placebo in space: each other zone gets the "operation" in turn, Tambopata removed from the pool. The raw rank in
    hectares measures size as much as effect (peru.py: pre-year ranks), so a scaled rank (coefficient divided by the
    zone's own pre mean, zones above MIN_PRE_HA) is reported next to every raw rank.
All results are DESCRIPTION. Written to output/peru_models.csv and output/fig_peru_models.png.
"""
from __future__ import annotations
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pyfixest as pf

from common import OUT, style_axes, finish_figure, SRC_PRICE, headline, C, INK, INK2, GRID, placebo_rank
import definitions as D
import zonedata as Z

TU = D.TREATED_ZONE
SRC = f"{D.SOURCE}; prices_annual.csv"
MEAS = ["net"] + D.PARTS
MODELS = {
    "M1": "Zone + year effects",
    "M2": "M1 + bigger zones react more to the gold price",
    "M3": "M1 + own linear trend per zone",
    "M4": "M1, scaled to each zone's own size",
}
LINEAR = ("M1", "M2", "M3")                    # additive in the outcome (M2 regressor held at the net pre mean)
PRE = D.PERIODS["pre_long"]                    # pooled reference 2014-18
EST = (PRE[0], D.YEARS[1])                     # estimation sample 2014-25
REAL = {"during": D.PERIODS["during"], "later": D.PERIODS["later"]}
FAKE = {"fake": D.PLACEBO_PERIODS["during"]}   # fake start 2016: 2016-18
FAKE_EST = (D.PANEL_YEARS[0], D.PLACEBO_PERIODS["during"][1])   # 2011-18
FAKE_PRE = (D.PANEL_YEARS[0], D.PLACEBO_START - 1)              # 2011-15: pre mean inside the placebo sample


def _zone_adds(pack=None, measure: str = "net") -> pd.DataFrame:
    """year x buffer zone table of one measure (default net additions), national raster panel (zonedata.bz_panel).
    `pack` is accepted for backwards compatibility and ignored: zones never come from the statistics workbook."""
    return Z.wide(Z.bz_panel(), D.COLS[measure])


def pools(ad: pd.DataFrame | None = None):
    """Pool B (non-zero net additions 2014-18), the scaled pool (pre mean > MIN_PRE_HA), the Amazon pool, pre means."""
    ad = _zone_adds() if ad is None else ad
    pre = ad.loc[PRE[0]:PRE[1]].mean()
    poolB = sorted(u for u in ad.columns if ad.loc[PRE[0]:PRE[1], u].abs().sum() > 0)
    big = sorted(u for u in poolB if pre[u] > D.MIN_PRE_HA)
    code = Z.bz_panel().groupby("unit").bz_code.first()
    amz = sorted(u for u in poolB if code[u] in D.AMAZON_BZ)
    return poolB, big, amz, pre


def _design(ad, units, treated, model, y0, y1, posts, gold, pre=None):
    """Long panel + regressor matrix (zone and year dummies spelled out) for numpy OLS. `pre` = the zone pre means used
    for M2's regressor and M4's scale; pass the NET pre means when fitting a part so the regressors stay fixed."""
    d = ad.loc[y0:y1, units].reset_index().melt(id_vars="year", var_name="unit", value_name="y")
    if pre is None:
        a, b = PRE if y1 >= D.FIRST_POST else (y0, min(y1, FAKE_PRE[1]))
        pre = ad.loc[a:b, units].mean()
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


def fit(ad, units, treated, model, y0, y1, posts, gold, pre=None) -> dict:
    d, X, fe = _design(ad, units, treated, model, y0, y1, posts, gold, pre)
    M = pd.concat([X, fe], axis=1).to_numpy()
    b, *_ = np.linalg.lstsq(M, d["y"].to_numpy(), rcond=None)
    return dict(zip(X.columns, b[: X.shape[1]]))


def _check_pyfixest(ad, units, gold):
    """The numpy fit must equal pyfixest's two-way fixed-effects fit (M1 and M2)."""
    d, X, _ = _design(ad, units, TU, "M2", *EST, REAL, gold)
    dd = pd.concat([d, X], axis=1)
    for m, rhs in [("M1", "post_during + post_later"), ("M2", "post_during + post_later + pre_x_lngold")]:
        f = pf.feols(f"y ~ {rhs} | unit + year", data=dd)
        ours = fit(ad, units, TU, m, *EST, REAL, gold)
        assert np.isclose(f.coef()["post_during"], ours["post_during"], atol=1e-6), f"{m}: numpy != pyfixest"


def _parts(model, units, gold, posts, est, net_pre):
    """Coefficients of one linear model on net and each part (regressors held at the net pre means)."""
    out = {m: fit(_zone_adds(measure=m), units, TU, model, *est, posts, gold, pre=net_pre) for m in MEAS}
    for k in out["net"]:
        if k.startswith("post_"):
            s = out["new"][k] + out["remined"][k] - out["stopped"][k]
            assert abs(out["net"][k] - s) < 0.01, f"{model} {k}: net != new + remined - stopped"
    return out


def run(pack, reg):
    print("\n== Peru model ladder (v3: net additions, national raster buffer-zone panel) ==")
    ad = _zone_adds()
    gold = pack["prices"].set_index("year")["gold"]
    poolB, big, amz, pre = pools(ad)
    assert TU in poolB and TU in big and TU in amz
    _check_pyfixest(ad, poolB, gold)
    fpre_all = ad.loc[FAKE_PRE[0]:FAKE_PRE[1]].mean()

    rows, parts = [], {}
    for m, label in MODELS.items():
        units = big if m == "M4" else poolB
        real = fit(ad, units, TU, m, *EST, REAL, gold)
        fake = fit(ad, units, TU, m, *FAKE_EST, FAKE, gold)
        noT = [v for v in units if v != TU]
        others = {u: fit(ad, noT, u, m, *EST, REAL, gold)["post_during"] for u in noT}
        rank = placebo_rank(real["post_during"], others.values())
        if m == "M4":
            rank_sc, n_sc = rank, len(units)
        else:                                       # scaled rank: each zone's coefficient / its own net pre mean
            rank_sc = placebo_rank(real["post_during"] / pre[TU], [others[u] / pre[u] for u in big if u != TU])
            n_sc = len(big)
        amz_u = [u for u in units if u in amz]
        oth_a = {u: fit(ad, [v for v in amz_u if v != TU], u, m, *EST, REAL, gold)["post_during"]
                 for u in amz_u if u != TU}
        rank_amz = placebo_rank(fit(ad, amz_u, TU, m, *EST, REAL, gold)["post_during"], oth_a.values())
        rows.append(dict(model=m, label=label, n_zones=len(units),
                         unit="share of own pre-2019 mean" if m == "M4" else "ha/yr",
                         during=real["post_during"], later=real["post_later"], placebo_fake_2016=fake["post_fake"],
                         rank_in_space=rank, rank_scaled=rank_sc, n_scaled=n_sc, rank_amazon=rank_amz,
                         n_amazon=len(amz_u), placebo_min=min(others.values()), placebo_max=max(others.values()),
                         gold_slope=real.get("pre_x_lngold", np.nan)))
        if m in LINEAR:
            parts[m] = dict(real=_parts(m, units, gold, REAL, EST, pre[units]),
                            fake=_parts(m, units, gold, FAKE, FAKE_EST, fpre_all[units]))
    res = pd.DataFrame(rows)
    res.round(3).to_csv(OUT / "peru_models.csv", index=False)
    print(res.drop(columns="label").round(2).to_string(index=False))

    pl = {"during": D.period_label("during"), "later": D.period_label("later")}
    for r in rows:
        k, u, m = r["model"].lower(), r["unit"], r["model"]
        lab = (f"{m} ({r['label']}; Tambopata buffer zone vs {r['n_zones'] - 1} Peruvian buffer zones, "
               f"{EST[0]}-{str(EST[1])[2:]}, reference {PRE[0]}-{str(PRE[1])[2:]})")
        if m in LINEAR:
            P = parts[m]
            Z.register_parts(reg, f"model_{k}_during", {q: P["real"][q]["post_during"] for q in MEAS}, TU, pl["during"],
                             f"coefficient, {lab}; description, one treated zone", source=SRC)
            Z.register_parts(reg, f"model_{k}_later", {q: P["real"][q]["post_later"] for q in MEAS}, TU, pl["later"],
                             f"coefficient (later years), {lab}; description", source=SRC)
            Z.register_parts(reg, f"model_{k}_placebo", {q: P["fake"][q]["post_fake"] for q in MEAS}, TU,
                             "fake start 2016 (2016–18, sample 2011–18)", f"placebo in time, {lab}", source=SRC)
        else:
            per = {"during": pl["during"], "later": pl["later"]}
            for key, col in (("during", "during"), ("later", "later")):
                reg.add(f"model_{k}_{key}_net", r[col], u, f"Net mining additions scaled to each zone's own mean "
                        f"net addition 2014-18 (1 = one normal year), Tambopata buffer zone, {per[key]}: coefficient, "
                        f"{lab}. Ratio to the net pre mean: net only, no split. Description.", "description", SRC,
                        measure="net", zone=TU, period=per[key])
            reg.add(f"model_{k}_placebo_net", r["placebo_fake_2016"], u, f"Placebo in time (fake start 2016, sample "
                    f"2011-18), scaled net additions, {lab}. Net only.", "description", SRC, measure="net", zone=TU,
                    period="fake start 2016")
        rk = f"net additions, {pl['during']}, {lab}; net only"
        reg.add(f"model_{k}_rank", r["rank_in_space"], "rank", f"Raw placebo-in-space rank of the Tambopata buffer "
                f"zone among {r['n_zones']} zones (1 = most negative), {rk}. "
                + ("This IS the size-relative rank." if m == "M4" else f"Raw hectares measure size: read next to "
                   f"model_{k}_rank_scaled."), "description", SRC, measure="net", zone=TU, period=pl["during"])
        reg.add(f"model_{k}_rank_scaled", r["rank_scaled"], "rank", f"Size-relative placebo-in-space rank (coefficient "
                f"/ own mean net addition 2014-18, zones above {D.MIN_PRE_HA:g} ha/yr), {rk}", "description", SRC,
                measure="net", zone=TU, period=pl["during"])
        reg.add(f"model_{k}_n_scaled", r["n_scaled"], "count", f"Zones in the size-relative ranking, {lab}",
                "description", SRC)
        reg.add(f"model_{k}_n", r["n_zones"], "count", f"Zones in {lab}", "description", SRC)
        reg.add(f"model_{k}_ri_p", r["rank_in_space"] / r["n_zones"], "p-value", f"Raw rank / zones (best possible "
                f"1/{r['n_zones']}); measures size as much as effect, never cite alone; {rk}", "description", SRC,
                measure="net", zone=TU, period=pl["during"])
        reg.add(f"model_{k}_rank_amazon", r["rank_amazon"], "rank", f"Raw rank among Amazon buffer zones only "
                f"(definitions.AMAZON_BZ, {r['n_amazon']} zones), {rk}", "description", SRC, measure="net", zone=TU,
                period=pl["during"])
        reg.add(f"model_{k}_n_amazon", r["n_amazon"], "count", f"Amazon buffer zones, {lab}", "description", SRC)
        for e in ("min", "max"):
            reg.add(f"model_{k}_placebo_{e}_net", r[f"placebo_{e}"], u, f"{'Smallest' if e == 'min' else 'Largest'} "
                    f"placebo-in-space coefficient (Tambopata removed from the pool), {rk}", "description", SRC,
                    measure="net", zone="placebo zones", period=pl["during"])
    # M3pre: Tambopata's post years saturated (one dummy per year 2019-25), so its own trend is fitted on 2014-18 only
    post_years = range(D.FIRST_POST, EST[1] + 1)
    sat = {q: fit(_zone_adds(measure=q), poolB, TU, "M3", *EST, {f"y{y}": (y, y) for y in post_years}, gold,
                  pre=pre[poolB]) for q in MEAS}
    for key in ("during", "later"):
        a, b = D.PERIODS[key]
        vals = {q: np.mean([sat[q][f"post_y{y}"] for y in range(a, b + 1)]) for q in MEAS}
        assert abs(vals["net"] - (vals["new"] + vals["remined"] - vals["stopped"])) < 0.01
        Z.register_parts(reg, f"model_m3pre_{key}", vals, TU, pl[key], "gap, M3 with Tambopata's trend fitted on "
                         "2014-18 only (one dummy per post year 2019-25, gap = mean of the period's dummies; "
                         f"{len(poolB)} zones); description", source=SRC)
        if key == "during":
            print(f"M3pre 2019-21 gap (net): {vals['net']:,.0f} ha/yr")
    reg.add("model_m2_gold_slope", rows[1]["gold_slope"], "ha per (ha of pre mean x 1 log-point)",
            "M2: extra net addition per hectare of a zone's 2014-18 mean net addition, per 1.0 rise in ln(gold price); "
            "identified mainly by the two big zones", "description", SRC, measure="net", zone="pool B",
            period="2014-25")
    # Tambopata's own yearly net additions in two pre-years not registered by peru.py (2016 = the low year)
    t = Z.bz_panel().query("unit == @TU").set_index("year")
    for y in (2016, 2017):
        Z.register_parts(reg, f"tambopata_bz_{y}", {q: t.loc[y, D.COLS[q]] for q in MEAS}, TU, str(y), "that year",
                         source=D.SOURCE)
    _figure(res)
    return res


def _figure(res):
    from matplotlib.ticker import FuncFormatter
    fig, axes = plt.subplots(len(res), 1, figsize=(9, 7.8), gridspec_kw={"hspace": 1.0})
    m1, m4 = res.iloc[0], res[res["model"] == "M4"].iloc[0]
    headline(fig, f"In hectares every model shows a 2019–21 fall of {abs(res.during.iloc[:3]).min():,.0f}–"
                  f"{abs(res.during.iloc[:3]).max():,.0f} ha/yr; relative to size it ranks {int(m4.rank_in_space)} of "
                  f"{int(m4.n_zones)}",
             f"Net mining additions (new + re-mined − stopped), Tambopata buffer zone minus {int(m1.n_zones) - 1} Peruvian "
             f"buffer zones, zone + year effects, reference {PRE[0]}–{str(PRE[1])[2:]}.\nOrange: real start 2019 "
             "(2019–21). Grey: fake start 2016 (2016–18 on 2011–18 data; should be near 0).")
    ha_rows = res[res["model"] != "M4"]                      # M1-M3 share one hectare axis, so bars compare
    ha_lo = min(ha_rows["during"].min(), ha_rows["placebo_fake_2016"].min()) * 1.45
    ha_hi = max(0, ha_rows["placebo_fake_2016"].max()) + abs(ha_lo) * 0.3
    for ax, (_, r) in zip(axes, res.iterrows()):
        ax.barh([1], [r["during"]], 0.62, color=C["lapampa"])
        ax.barh([0], [r["placebo_fake_2016"]], 0.62, color=C["other"])
        for yy, v, lab in [(1, r["during"], "real"), (0, r["placebo_fake_2016"], "fake")]:
            txt = (f"{v:,.2f}" if r["model"] == "M4" else f"{v:,.0f}").replace("-", "−")
            ax.annotate(f"{txt}  {lab}", (v, yy), xytext=(5 if v >= 0 else -5, 0), textcoords="offset points",
                        va="center", ha="left" if v >= 0 else "right", fontsize=8.5, color=INK,
                        fontweight="semibold" if lab == "real" else "normal")
        ax.axvline(0, color=INK2, lw=0.8)
        if r["model"] == "M4":
            lo = min(r["during"], r["placebo_fake_2016"]) * 1.45
            hi = max(0, r["placebo_fake_2016"]) + abs(lo) * 0.3
        else:
            lo, hi = ha_lo, ha_hi
        ax.set_xlim(lo, hi)
        ax.set_yticks([])
        for sp in ("top", "right", "left"):
            ax.spines[sp].set_visible(False)
        ax.xaxis.grid(True, color=GRID, lw=0.6); ax.set_axisbelow(True)
        ax.xaxis.set_major_formatter(FuncFormatter(lambda v, p: "0" if v == 0 else (f"{v:,.1f}" if abs(v) < 5 else f"{v:,.0f}").replace("-", "−")))
        if r["model"] == "M4":
            info = f"1 = one normal pre-2019 year  ·  size-relative rank {int(r['rank_in_space'])} of {int(r['n_zones'])}"
        else:
            info = (f"ha per year  ·  raw rank {int(r['rank_in_space'])} of {int(r['n_zones'])}, "
                    f"size-relative {int(r['rank_scaled'])} of {int(r['n_scaled'])}")
        ax.set_title(f"{r['model']}  {r['label']}", fontsize=9.5)
        ax.text(1.0, 1.04, info, transform=ax.transAxes, ha="right", va="bottom", fontsize=8, color=INK2)
    finish_figure(fig, f"{D.SOURCE}; {SRC_PRICE}. Raw rank = Tambopata's place when each zone gets the operation in "
                       "turn (1 = biggest fall); in hectares it measures size. Size-relative rank divides by each zone's "
                       "own 2014–18 mean. One treated zone: no confidence intervals. Description.",
                  OUT / "fig_peru_models.png")


if __name__ == "__main__":
    from common import Numbers, load_pack
    reg = Numbers(); run(load_pack(), reg)
