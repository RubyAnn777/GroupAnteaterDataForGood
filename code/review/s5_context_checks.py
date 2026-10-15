"""Review session S5 (docs/methods/05_context_controls.md): read-only checks of the context models K0-K3
(peru_context_models.py): COVID exposure and Madre de Dios x ln(PP 0128 enforcement spending) as controls.

Run from the repo root:  uv run python code/review/s5_context_checks.py   (writes nothing; ~5 s)
Needs data_raw/enforcement_peru/mef_pp0128/*.html (committed) through v2_tests.mef_series().
U1 reproduce · U2 where the COVID term comes from · U3 binned vs saturated post dummies · U4 offsetting decomposition
U5 where the spending coefficient comes from · U6 is spending post-treatment? · U7 the dose correlation.
"""
import sys
import numpy as np, pandas as pd
sys.path.insert(0, "code")
from v2_tests import mef_series                     # same parser the pipeline uses (read-only)

bz = pd.read_csv("data/peru_bufferzone_year.csv")
bz["u"] = bz.buffer_zone + "|" + bz.pa_category
ad = bz.groupby(["u", "year"]).mining_ha.sum().unstack("u").diff()
gold = pd.read_csv("data/prices_annual.csv").set_index("year")["gold"]
spend_all = mef_series().sort_index()
spend = spend_all.loc[2015:2025]
T, A, B = "Tambopata|Reserva Nacional", "Amarakaeri|Reserva Comunal", "Bahuaja-Sonene|Parque Nacional"
MDD = {T, A, B}
POOL = sorted(u for u in ad.columns if ad.loc[2014:2018, u].abs().sum() > 0)
C = [u for u in POOL if u != T]
REAL = {"during": (2019, 2021), "after": (2022, 2025)}
SAT = {f"y{y}": (y, y) for y in range(2019, 2026)}


def fit(units, treated=T, model="K0", posts=REAL, y0=2015, y1=2025, sp=spend, mdd=MDD):
    d = ad.loc[y0:y1, units].reset_index().melt(id_vars="year", var_name="unit", value_name="y")
    pre = ad.loc[2014:2018, units].mean()
    X = {f"p_{k}": ((d.unit == treated) & d.year.between(*v)).astype(float) for k, v in posts.items()}
    X["gold"] = d.unit.map(pre) * np.log(d.year.map(gold))
    if model in ("K1", "K3"):
        X["covid"] = d.unit.map(pre) * d.year.between(2020, 2021)
    if model in ("K2", "K3"):
        X["spend"] = d.unit.isin(mdd) * np.log(d.year.map(sp))
    X = pd.DataFrame(X).astype(float)
    M = pd.concat([X, pd.get_dummies(d.unit, dtype=float), pd.get_dummies(d.year, prefix="y", drop_first=True, dtype=float)], axis=1)
    b, *_ = np.linalg.lstsq(M.to_numpy(), d.y.to_numpy(), rcond=None)
    assert np.linalg.matrix_rank(M.to_numpy()) == M.shape[1]
    return dict(zip(M.columns, b))


def gap(r):
    return r["p_during"] if "p_during" in r else np.mean([r[f"p_y{y}"] for y in (2019, 2020, 2021)])


def rank(units, model, posts=REAL):
    real = gap(fit(units, T, model, posts))
    pl = [gap(fit([v for v in units if v != T], u, model, posts)) for u in units if u != T]
    return real, 1 + sum(p <= real for p in pl)


print("U1 reproduce")
res = {}
for m in ["K0", "K1", "K2", "K3"]:
    r = fit(POOL, model=m); real, rk = rank(POOL, m); res[m] = r
    print(f"  {m}: during {r['p_during']:9.1f}  after {r['p_after']:7.1f}  rank {rk} of 15  covid {r.get('covid', np.nan):.3f}  spend {r.get('spend', np.nan):.1f}")
print(f"  K3/K0 = {res['K3']['p_during'] / res['K0']['p_during']:.3f}")
print("  PP 0128 devengado, Madre de Dios, M soles:", (spend_all / 1e6).round(2).to_dict())

print("\nU2 where the COVID term comes from")
print(f"  K1 binned, all 15 zones: covid coef {res['K1']['covid']:.3f}")
print(f"  K1 saturated (Tambopata 2019-25 one dummy per year): {fit(POOL, model='K1', posts=SAT)['covid']:.3f}")
print(f"  K1 on the 14 controls only: {fit(C, treated='_', model='K1', posts={})['covid']:.3f}")
print(f"  K1 on the controls without Amarakaeri: {fit([u for u in C if u != A], treated='_', model='K1', posts={})['covid']:.3f}")
pre = ad.loc[2014:2018].mean()
print(f"  regressor value for Tambopata in 2020-21 = its pre mean {pre[T]:.0f}; for Amarakaeri {pre[A]:.0f}; the other 13 zones' max {pre[[u for u in C if u != A]].max():.0f}")
print("  Tambopata 2019-21 additions:", ad.loc[2019:2021, T].round(0).tolist(), " -> with one 2019-21 bin, the 2020-21 dip below 2019 loads on the COVID term")
print(f"  implied COVID effect on Tambopata (binned): {res['K1']['covid'] * pre[T]:.0f} ha/yr in 2020-21; saturated: {fit(POOL, model='K1', posts=SAT)['covid'] * pre[T]:.0f}")

print("\nU3 binned vs saturated post dummies")
sat = {m: gap(fit(POOL, model=m, posts=SAT)) for m in ["K0", "K1", "K2", "K3"]}
for m in sat:
    print(f"  {m}: binned {res[m]['p_during']:8.1f}  saturated {sat[m]:8.1f}   rank saturated {rank(POOL, m, SAT)[1]} of 15")
print(f"  K1 vs K0: binned {res['K1']['p_during'] / res['K0']['p_during'] - 1:+.1%}, saturated {sat['K1'] / sat['K0'] - 1:+.1%}")
print(f"  K3/K0 saturated: {sat['K3'] / sat['K0']:.3f}")

print("\nU4 offsetting decomposition (binned, as published)")
k0 = res["K0"]["p_during"]
for m in ["K1", "K2", "K3"]:
    print(f"  {m} - K0 = {res[m]['p_during'] - k0:+7.1f} ha/yr")
print(f"  sum of the K1 and K2 shifts {res['K1']['p_during'] + res['K2']['p_during'] - 2 * k0:+.1f} vs K3 shift {res['K3']['p_during'] - k0:+.1f}")

print("\nU5 where the spending coefficient comes from (K2)")
for nm, mdd in [("as coded (Tambopata, Amarakaeri, Bahuaja)", MDD), ("Amarakaeri + Bahuaja only", {A, B}), ("Amarakaeri only", {A}), ("Bahuaja only", {B}), ("Tambopata only", {T})]:
    r = fit(POOL, model="K2", mdd=mdd)
    print(f"  spending on {nm:42s}: coef {r['spend']:7.1f}  gap {r['p_during']:8.1f}")
r = fit(POOL, model="K2", posts=SAT)
print(f"  K2 saturated: coef {r['spend']:.1f}  gap {gap(r):.1f}")
print(f"  K2 dropping Amarakaeri: gap {fit([u for u in POOL if u != A], model='K2', mdd={T, B})['p_during']:.1f} "
      f"(coef {fit([u for u in POOL if u != A], model='K2', mdd={T, B})['spend']:.1f})")
r0 = fit(POOL, model="K0")
d = ad.loc[2015:2025, [A, B]]
print("  Amarakaeri and Bahuaja additions 2015-25:\n", d.round(0).T.to_string())
print("  ln spend:", np.log(spend).round(2).to_dict())

print("\nU6 is spending post-treatment?")
pre_s, d_s, a_s = spend.loc[2015:2018].mean(), spend.loc[2019:2021].mean(), spend.loc[2022:2025].mean()
print(f"  mean M soles 2015-18 {pre_s / 1e6:.2f} | 2019-21 {d_s / 1e6:.2f} | 2022-25 {a_s / 1e6:.2f}; 2019 / 2018 = {spend[2019] / spend[2018]:.0f}x")
ls = np.log(spend)
post = pd.Series((ls.index >= 2019).astype(float), index=ls.index)
print(f"  corr(ln spend, 1[year >= 2019]) = {np.corrcoef(ls, post)[0, 1]:.2f}; corr(ln spend, 1[2019-21]) = "
      f"{np.corrcoef(ls, ((ls.index >= 2019) & (ls.index <= 2021)).astype(float))[0, 1]:.2f}")
r = np.polyfit(post, ls, 1); resid = ls - np.polyval(r, post)
print(f"  R2 of ln spend on 1[year >= 2019] alone: {1 - resid.var() / ls.var():.2f}")

print("\nU7 the dose correlation")
gp = ad.loc[2015:2025, T] - ad.loc[2015:2025, C].mean(axis=1)
gp = gp - gp.loc[2015:2018].mean()
print(f"  corr(gap, ln spend) 2015-25 = {np.corrcoef(ls, gp)[0, 1]:.3f}  (published ctx_dose_corr)")
print(f"  corr(gap, 1[year >= 2019]) = {np.corrcoef(post, gp)[0, 1]:.3f}")
for nm, yrs in [("2015-18 only", range(2015, 2019)), ("2019-25 only", range(2019, 2026)), ("2019-21 only", range(2019, 2022))]:
    yy = list(yrs)
    print(f"  within {nm}: corr = {np.corrcoef(ls.loc[yy], gp.loc[yy])[0, 1]:.2f}  (n = {len(yy)})")
e_ls = ls - ls.groupby(post).transform("mean"); e_gp = gp - gp.groupby(post).transform("mean")
print(f"  partial corr after removing pre/post means: {np.corrcoef(e_ls, e_gp)[0, 1]:.2f}")
print("  gap by year:", gp.round(0).to_dict())
