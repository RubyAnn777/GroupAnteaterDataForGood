"""Review session S4 (docs/methods/04_twfe_ladder.md): read-only checks of the TWFE model ladder M1-M4 (peru_models.py).

Run from the repo root:  uv run python code/review/s4_twfe_checks.py   (writes nothing; ~10 s)
Independent re-implementation (own design matrix + numpy lstsq, cross-checked with pyfixest), then:
T1 reproduce M1-M4, m3pre, gold slope, ranks · T2 M1 = Tambopata's own before/after minus a tiny control drift
T3 size of the year effects vs the gap, and year effects vs ln(gold) · T4 binned vs saturated post dummies (M2, M3, M4)
T5 leave-one-control-out · T6 fake-date windows and denominators · T7 M4 denominators (signed vs absolute)
T8 rank of every design matrix · T9 the hand-coded AMAZON pool · T10 range table across specifications.
"""
import numpy as np, pandas as pd, pyfixest as pf

bz = pd.read_csv("data/peru_bufferzone_year.csv")
bz["u"] = bz.buffer_zone + "|" + bz.pa_category
ad = bz.groupby(["u", "year"]).mining_ha.sum().unstack("u").diff()          # aggregate first, then difference
gold = pd.read_csv("data/prices_annual.csv").set_index("year")["gold"]
T, A, B = "Tambopata|Reserva Nacional", "Amarakaeri|Reserva Comunal", "Bahuaja-Sonene|Parque Nacional"
POOL = sorted(u for u in ad.columns if ad.loc[2014:2018, u].abs().sum() > 0)
PRE = ad.loc[2014:2018].mean()
BIG = sorted(u for u in POOL if PRE[u] > 10)
REAL = {"during": (2019, 2021), "after": (2022, 2025)}
SAT = {f"y{y}": (y, y) for y in range(2019, 2026)}
assert len(POOL) == 15 and len(BIG) == 7


def fit(units, treated=T, model="M1", y0=2014, y1=2025, posts=REAL, denom=None, ret_fe=False, ret_rank=False):
    """y = unit FE + year FE + treated x post bins [+ pre x ln gold (M2)] [+ unit trends (M3)]; M4 divides y by denom."""
    d = ad.loc[y0:y1, units].reset_index().melt(id_vars="year", var_name="unit", value_name="y")
    pre = ad.loc[2014:2018, units].mean() if y1 > 2018 else ad.loc[y0:min(y1, 2015), units].mean()
    if model == "M4":
        d["y"] = d.y / d.unit.map(pre if denom is None else denom)
    X = {f"p_{k}": ((d.unit == treated) & d.year.between(*v)).astype(float) for k, v in posts.items()}
    if model == "M2":
        X["gold"] = d.unit.map(pre) * np.log(d.year.map(gold))
    if model == "M3":
        drop = next(u for u in units if u != treated)
        for u in units:
            if u != drop:
                X[f"tr_{u}"] = ((d.unit == u) * (d.year - y0)).astype(float)
    X = pd.DataFrame(X)
    U = pd.get_dummies(d.unit, dtype=float); Y = pd.get_dummies(d.year, prefix="y", drop_first=True, dtype=float)
    M = pd.concat([X, U, Y], axis=1)
    b, *_ = np.linalg.lstsq(M.to_numpy(), d.y.to_numpy(), rcond=None)
    out = dict(zip(M.columns, b))
    if ret_rank:
        return np.linalg.matrix_rank(M.to_numpy()), M.shape[1]
    return out


def gap(r, yrs=(2019, 2020, 2021)):
    """2019-21 gap: the 'during' coefficient, or the mean of the saturated yearly dummies."""
    return r["p_during"] if "p_during" in r else np.mean([r[f"p_y{y}"] for y in yrs])


def rank(units, model, posts=REAL, denom=None):
    real = gap(fit(units, T, model, posts=posts, denom=denom))
    pl = [gap(fit([v for v in units if v != T], u, model, posts=posts, denom=denom)) for u in units if u != T]
    return real, 1 + sum(p <= real for p in pl), len(units), min(pl), max(pl)


print("T1 reproduce")
for m in ["M1", "M2", "M3", "M4"]:
    units = BIG if m == "M4" else POOL
    real, rk, n, lo, hi = rank(units, m)
    r = fit(units, model=m); f = fit(units, model=m, y0=2011, y1=2018, posts={"fake": (2016, 2018)})
    print(f"  {m}: during {real:9.3f}  after {r['p_after']:8.3f}  fake2016 {f['p_fake']:8.3f}  rank {rk} of {n} (p {rk/n:.3f})"
          f"  placebo range {lo:.2f}..{hi:.2f}" + (f"  gold slope {r['gold']:.3f}" if m == "M2" else ""))
s3 = fit(POOL, model="M3", posts=SAT)
print(f"  m3pre: {gap(s3):.1f}  after {np.mean([s3[f'p_y{y}'] for y in range(2022, 2026)]):.1f}")
d = ad.loc[2014:2025, POOL].reset_index().melt(id_vars="year", var_name="unit", value_name="y")
d["p_during"] = ((d.unit == T) & d.year.between(2019, 2021)).astype(float); d["p_after"] = ((d.unit == T) & d.year.between(2022, 2025)).astype(float)
d["gold"] = d.unit.map(PRE) * np.log(d.year.map(gold))
print("  pyfixest M1 / M2:", round(pf.feols("y ~ p_during + p_after | unit + year", data=d).coef()["p_during"], 3),
      round(pf.feols("y ~ p_during + p_after + gold | unit + year", data=d).coef()["p_during"], 3))

print("\nT2 M1 = Tambopata's own before/after minus the controls' drift")
C = [u for u in POOL if u != T]
cm = ad.loc[2014:2025, C].mean(axis=1)
dT = ad.loc[2019:2021, T].mean() - ad.loc[2014:2018, T].mean(); dC = cm.loc[2019:2021].mean() - cm.loc[2014:2018].mean()
print(f"  Tambopata 2014-18 {ad.loc[2014:2018, T].mean():.1f} -> 2019-21 {ad.loc[2019:2021, T].mean():.1f}: change {dT:.1f}")
print(f"  14-zone control mean 2014-18 {cm.loc[2014:2018].mean():.1f} -> 2019-21 {cm.loc[2019:2021].mean():.1f}: change {dC:.1f}")
print(f"  dT - dC = {dT - dC:.1f}  (M1 = {fit(POOL)['p_during']:.1f})")
cmA = ad.loc[2014:2025, [u for u in C if u != A]].mean(axis=1)
print(f"  control drift without Amarakaeri: {cmA.loc[2019:2021].mean() - cmA.loc[2014:2018].mean():.1f}; Amarakaeri's own change "
      f"{ad.loc[2019:2021, A].mean() - ad.loc[2014:2018, A].mean():.1f} (share of the 14-zone drift: "
      f"{(ad.loc[2019:2021, A].mean() - ad.loc[2014:2018, A].mean()) / 14 / dC:.0%})")

print("\nT3 size of the year effects (M1) and their link to the gold price")
r1 = fit(POOL)
ye = pd.Series({y: r1.get(f"y_{y}", 0.0) for y in range(2014, 2026)})
print("  year effects (2014 = 0):", ye.round(1).to_dict())
print(f"  range {ye.min():.1f}..{ye.max():.1f}; 2019-21 mean minus 2014-18 mean = {ye.loc[2019:2021].mean() - ye.loc[2014:2018].mean():.1f} ha")
lg = np.log(gold.loc[2014:2025])
sl = np.polyfit(lg.values, ye.values, 1)
print(f"  year effect on ln(gold): slope {sl[0]:.1f} ha per log-point, corr {np.corrcoef(lg, ye)[0, 1]:.2f}; ln gold 2018->2021 +{lg[2021] - lg[2018]:.2f}")
dlg = lg.diff().dropna(); dye = ye.diff().dropna()
print(f"  first differences: corr(d year effect, d ln gold) = {np.corrcoef(dlg, dye)[0, 1]:.2f}")
print(f"  Tambopata's pre mean is {PRE[T] / cm.loc[2014:2018].mean():.0f}x the control mean: a common shock in hectares is a "
      "proportional shock of very different size")

print("\nT4 binned vs saturated post dummies")
for m, units in [("M1", POOL), ("M2", POOL), ("M3", POOL), ("M4", BIG)]:
    rb, rs = fit(units, model=m), fit(units, model=m, posts=SAT)
    extra = f"  slope binned {rb['gold']:.3f} saturated {rs['gold']:.3f}" if m == "M2" else ""
    print(f"  {m}: binned {gap(rb):9.2f}  saturated {gap(rs):9.2f}  saturated 2019 / 2020 / 2021 = "
          f"{rs['p_y2019']:.1f} / {rs['p_y2020']:.1f} / {rs['p_y2021']:.1f}{extra}")
tt = np.polyfit(range(2014, 2019), ad.loc[2014:2018, T].values, 1)[0]
print(f"  Tambopata's own 2014-18 linear trend: {tt:+.0f} ha/yr per year (m3pre extrapolates it into 2019-21)")
noA = [u for u in POOL if u != A]
rs = fit(noA, model="M2", posts=SAT)
print(f"  M2 saturated, Amarakaeri dropped: slope {rs['gold']:.3f}, gap {gap(rs):.1f}")
rc = fit(C, treated="__none__", model="M2", posts={})
print(f"  M2 slope from the 14 controls only (no Tambopata): {rc['gold']:.3f}; without Amarakaeri too: "
      f"{fit([u for u in C if u != A], treated='__none__', model='M2', posts={})['gold']:.3f}")
dlg = np.log(gold.loc[2019:2021]).mean() - np.log(gold.loc[2014:2018]).mean()
for nm, sl_ in [("binned", fit(POOL, model="M2")["gold"]), ("saturated", fit(POOL, model="M2", posts=SAT)["gold"])]:
    print(f"  M2 {nm}: predicted extra 2019-21 rise of Tambopata from gold = slope x (pre_T - mean pre_C) x d ln gold "
          f"= {sl_:.2f} x {PRE[T] - PRE[C].mean():.0f} x {dlg:.3f} = {sl_ * (PRE[T] - PRE[C].mean()) * dlg:.0f} ha/yr")
print(f"  Amarakaeri (the only large control) 2014-18 mean {PRE[A]:.0f} ha; Tambopata {PRE[T]:.0f} ha = {PRE[T] / PRE[A]:.1f}x")
for m in ["M2", "M3"]:
    real, rk, n, lo, hi = rank(POOL, m, posts=SAT)
    print(f"  {m} saturated, placebo-in-space (each placebo saturated too): gap {real:.1f}, rank {rk} of {n}, placebo range {lo:.0f}..{hi:.0f}")
print("  why binned M2 differs: Tambopata's 2019-21 additions (", ad.loc[2019:2021, T].round(0).tolist(),
      ") fall while ln gold rises", lg.loc[2019:2021].round(2).tolist(), "; with one bin, the slope is fitted partly from this within-bin path")

print("\nT5 leave one control zone out (binned and saturated)")
rows = []
for drop in C:
    us = [u for u in POOL if u != drop]
    rows.append([drop.split("|")[0]] + [gap(fit(us, model=m)) for m in ("M1", "M2", "M3")] + [gap(fit(us, model="M2", posts=SAT)), gap(fit(us, model="M3", posts=SAT))])
loo = pd.DataFrame(rows, columns=["dropped", "M1", "M2", "M3", "M2sat", "M3sat"]).set_index("dropped")
print(loo.round(0).to_string()); print("  min/max:", loo.min().round(0).to_dict(), loo.max().round(0).to_dict())
bigC = [u for u in BIG if u != T]
rows = []
for drop in bigC:
    us = [u for u in BIG if u != drop]
    real, rk, n, *_ = rank(us, "M4")
    rows.append((drop.split("|")[0], round(real, 2), f"{rk} of {n}"))
print("  M4 leave-one-out:", rows)

print("\nT6 fake-date windows (sample ends 2018, so no post data)")
for y0, fk in [(2011, (2016, 2018)), (2011, (2014, 2015)), (2008, (2013, 2015)), (2008, (2011, 2013)), (2011, (2017, 2018)), (2014, (2017, 2018))]:
    res = {m: fit(BIG if m == "M4" else POOL, model=m, y0=y0, y1=2018, posts={"fake": fk})["p_fake"] for m in ("M1", "M2", "M3", "M4")}
    print(f"  sample {y0}-2018, fake {fk}: " + "  ".join(f"{k} {v:,.2f}" for k, v in res.items()))
d15 = ad.loc[2011:2015].mean()
print("  M2/M4 fake denominators (2011-15 means) vs real (2014-18):", {u.split("|")[0]: (round(d15[u], 1), round(PRE[u], 1)) for u in BIG})

print("\nT7 M4 denominators")
ABS = ad.loc[2014:2018].abs().mean()
print("  signed vs absolute 2014-18 mean:", {u.split("|")[0]: (round(PRE[u], 1), round(ABS[u], 1)) for u in BIG})
for nm, den in [("signed (as coded)", None), ("absolute", ABS), ("2016-18 signed", ad.loc[2016:2018].mean())]:
    real, rk, n, lo, hi = rank(BIG, "M4", denom=den)
    print(f"  {nm}: Tambopata {real:.2f}, rank {rk} of {n}, placebo range {lo:.2f}..{hi:.2f}")
pl = {u: gap(fit([v for v in BIG if v != T], u, "M4")) for u in bigC}
print("  M4 placebo effects (signed denominators):", {k.split("|")[0]: round(v, 2) for k, v in pl.items()})

print("\nT8 rank of each design matrix")
for m in ["M1", "M2", "M3", "M4"]:
    for posts, nm in [(REAL, "binned"), (SAT, "saturated")]:
        print(f"  {m} {nm}: rank {fit(BIG if m == 'M4' else POOL, model=m, posts=posts, ret_rank=True)}")
print("  M3 fake (2011-18):", fit(POOL, model="M3", y0=2011, y1=2018, posts={"fake": (2016, 2018)}, ret_rank=True))

print("\nT9 the AMAZON list (peru_models.py:41-43)")
for u in POOL:
    print(f"  {u.split('|')[0]:24s} depts {sorted(bz[bz.u == u].department.unique())}  pre {PRE[u]:7.1f}")
AMZ = {T, A, B, "Allpahuayo Mishana|Reserva Nacional", "Cordillera Azul|Parque Nacional", "Alto Mayo|Bosque de Protección",
       "Pacaya-Samiria|Reserva Nacional", "El Sira|Reserva Comunal"}
for extra in [set(), {"del Río Abiseo|Parque Nacional"}]:
    for m in ["M1", "M4"]:
        us = sorted(u for u in (BIG if m == "M4" else POOL) if u in AMZ | extra)
        real, rk, n, *_ = rank(us, m)
        print(f"  Amazon pool {'+ Río Abiseo' if extra else '(as coded)'} {m}: rank {rk} of {n}")

print("\nT10 range of the 2019-21 gap across specifications (ha/yr)")
tab = {"M1 binned": gap(fit(POOL)), "M2 binned": gap(fit(POOL, model="M2")), "M3 binned": gap(fit(POOL, model="M3")),
       "M2 saturated": gap(fit(POOL, model="M2", posts=SAT)), "M3 saturated (m3pre)": gap(fit(POOL, model="M3", posts=SAT)),
       "M2 saturated, no Amarakaeri": gap(fit(noA, model="M2", posts=SAT)), "M3 saturated, no Amarakaeri": gap(fit(noA, model="M3", posts=SAT)),
       "M1 no Amarakaeri": gap(fit(noA)), "2x2 vs Amarakaeri 2016-18 (S2)": (ad.loc[2019:2021, T].mean() - ad.loc[2016:2018, T].mean()) - (ad.loc[2019:2021, A].mean() - ad.loc[2016:2018, A].mean()),
       "Tambopata own before/after 2014-18": dT}
for k, v in tab.items():
    print(f"  {k:36s} {v:9.1f}")
