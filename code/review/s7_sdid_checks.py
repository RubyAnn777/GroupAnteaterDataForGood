"""Review session S7 (docs/methods/07_synthetic_did.md): read-only checks of synthetic DiD (attempt A6).

Run from the repo root:  uv run python code/review/s7_sdid_checks.py   (writes nothing; a few minutes)
Reads data/peru_bufferzone_year.csv, data/prices_annual.csv and output/numbers.csv; imports code/peru_sdid.py only to
compare its weights with an independent re-implementation. Not part of main.py.
T1 reproduce: independent SDID (own solver, Algorithm 1 of Arkhangelsky et al. 2021); zeta; objectives; KKT; DiD = M1
T2 time weights: tau and the argmax of lambda for pre-window starts 2010..2014 (end 2018); uniform-lambda variant
T3 unit weights: who gets weight, and what those zones look like before 2019
T4 leave-one-out over comparison zones
T5 placebo SE and exchangeability: placebo taus vs zone size; pre-period noise of Tambopata vs controls
T6 placebo in time: SDID with fake start years (5 pre years, 3 post years, all before 2019)
T7 other pools: Amazon-department zones only; without Amarakaeri and Bahuaja-Sonene
T8 later years 2022-25 with and without 2023
"""
import sys
import numpy as np, pandas as pd
sys.path.insert(0, "code")
pd.set_option("display.width", 200)

bz = pd.read_csv("data/peru_bufferzone_year.csv")
ad = bz.assign(u=bz.buffer_zone + "|" + bz.pa_category).groupby(["u", "year"]).mining_ha.sum().unstack("u").diff()
T, A, B = "Tambopata|Reserva Nacional", "Amarakaeri|Reserva Comunal", "Bahuaja-Sonene|Parque Nacional"
num = pd.read_csv("output/numbers.csv").set_index("id")["value"]
sh = lambda u: u.split("|")[0]
poolB = sorted(u for u in ad.columns if ad.loc[2014:2018, u].abs().sum() > 0)
pre_mean = ad.loc[2014:2018].mean()
pool_big = sorted(u for u in poolB if pre_mean[u] > 10)
YH, YS = ad[poolB], ad[pool_big] / pre_mean[pool_big]
DUR, LAT = (2019, 2021), (2022, 2025)


def proj_simplex(v):
    u = np.sort(v)[::-1]; css = np.cumsum(u)
    k = np.nonzero(u * np.arange(1, len(v) + 1) > (css - 1))[0][-1]
    return np.maximum(v - (css[k] - 1) / (k + 1), 0)


def solve(A_, b, pen, iters=30000, tol=1e-11):
    """min_{c, w in simplex} ||c + A w - b||^2 + pen ||w||^2 by FISTA with adaptive restart (own code)."""
    A_ = A_ - A_.mean(0); b = b - b.mean()
    f = lambda w: float(np.sum((A_ @ w - b) ** 2) + pen * w @ w)
    fw_ = None
    Lc = 2 * (np.linalg.norm(A_, 2) ** 2 + pen)
    w = z = np.full(A_.shape[1], 1 / A_.shape[1]); t = 1.0
    for _ in range(iters):
        wn = proj_simplex(z - (2 * A_.T @ (A_ @ z - b) + 2 * pen * z) / Lc)
        fn = f(wn)
        if fw_ is not None and fn > fw_:
            z, t = w, 1.0; continue
        fw_ = fn
        tn = (1 + np.sqrt(1 + 4 * t * t)) / 2
        z = wn + (t - 1) / tn * (wn - w)
        if np.abs(wn - w).max() < tol:
            w = wn; break
        w, t = wn, tn
    return w, f


def sdid_own(Y, tr, pre, post, lam_uniform=False, ddof=1, years=None):
    pre_y = years or list(range(pre[0], pre[1] + 1)); post_y = list(range(post[0], post[1] + 1))
    co = [u for u in Y.columns if u != tr]
    Yp, Yq = Y.loc[pre_y, co].to_numpy(), Y.loc[post_y, co].to_numpy()
    yp, yq = Y.loc[pre_y, tr].to_numpy(), Y.loc[post_y, tr].to_numpy()
    N0, T0 = len(co), len(pre_y)
    sigma = np.std(np.diff(Yp, axis=0), ddof=ddof)
    zeta = (1 * len(post_y)) ** 0.25 * sigma
    w, fw = solve(Yp, yp, zeta ** 2 * T0)
    if lam_uniform:
        lam, fl = np.full(T0, 1 / T0), None
    else:
        lam, fl = solve(Yp.T, Yq.mean(0), (1e-6 * sigma) ** 2 * N0)
    tau = (yq.mean() - lam @ yp) - (w @ Yq.mean(0) - w @ (Yp.T @ lam))
    return dict(tau=float(tau), w=pd.Series(w, co), lam=pd.Series(lam, pre_y), zeta=zeta, sigma=sigma, fw=fw, fl=fl)


import peru_sdid as ps


def sdid(Y, tr, pre, post, lam_uniform=False, **kw):
    """Stress tests T2-T8 call the repo's sdid (validated against sdid_own in T1, weights equal to 1e-9; it is much
    faster); the uniform-lambda variant has no repo counterpart and uses sdid_own."""
    if lam_uniform or kw:
        return sdid_own(Y, tr, pre, post, lam_uniform=lam_uniform, **kw)
    return ps.sdid(Y, tr, pre, post, "sdid")


def placebo(Y, pre, post, **kw):
    others = [u for u in Y.columns if u != T]
    return pd.Series({u: sdid(Y[others], u, pre, post, **kw)["tau"] for u in others})


def rank(real, est):
    return 1 + int((est <= real).sum())


print("T1 reproduce (independent solver)")
for lab, Y, key in (("ha", YH, "sdid_sdid_ha_during"), ("scaled", YS, "sdid_sdid_scaled_during")):
    r = sdid_own(Y, T, (2014, 2018), DUR)
    rr = ps.sdid(Y, T, (2014, 2018), DUR, "sdid")
    wr, lr = rr["w"].to_numpy(), rr["lam"].to_numpy()
    print(f"  {lab}: tau ours {r['tau']:.4f}  repo function {rr['tau']:.4f}  numbers.csv {num[key]:.4f}; sigma {r['sigma']:.2f}, zeta {r['zeta']:.2f}"
          f" (with ddof=0 sigma: tau {sdid_own(Y, T, (2014, 2018), DUR, ddof=0)['tau']:.2f})")
    print(f"     unit objective ours {r['fw'](r['w'].to_numpy()):,.4f} vs at repo weights {r['fw'](wr):,.4f}; "
          f"max |w ours - w repo| {np.abs(r['w'].to_numpy() - wr).max():.2e}; max |lambda diff| {np.abs(r['lam'].to_numpy() - lr).max():.2e}")
    # KKT on the simplex: gradient equal (to the minimum) on the support, not smaller off it
    co = [u for u in Y.columns if u != T]
    Ap = Y.loc[2014:2018, co].to_numpy(); Ap = Ap - Ap.mean(0); bp = Y.loc[2014:2018, T].to_numpy(); bp = bp - bp.mean()
    g = 2 * Ap.T @ (Ap @ r["w"].to_numpy() - bp) + 2 * r["zeta"] ** 2 * 5 * r["w"].to_numpy()
    on = r["w"].to_numpy() > 1e-8
    print(f"     KKT: gradient on support spread {g[on].max() - g[on].min():.2e}; min off-support gradient minus support level {(g[~on] - g[on].mean()).min() if (~on).any() else float('nan'):.2f} (>= 0 required; nan = every zone weighted)")
uni = (YH.loc[2019:2021, T].mean() - YH.loc[2014:2018, T].mean()) - (YH.loc[2019:2021].drop(columns=T).mean().mean() - YH.loc[2014:2018].drop(columns=T).mean().mean())
print(f"  DiD special case (uniform weights) {uni:.4f} vs model_m1_during {num['model_m1_during']:.4f} and sdid_did_ha_during {num['sdid_did_ha_during']:.4f}")

print("\nT2 time weights: pre-window start s..2018, post 2019-21 (ha)")
rows = []
for s in range(2010, 2015):
    r = sdid(YH, T, (s, 2018), DUR); ru = sdid(YH, T, (s, 2018), DUR, lam_uniform=True)
    est = placebo(YH, (s, 2018), DUR)
    top = r["lam"].sort_values(ascending=False)
    rows.append(dict(pre=f"{s}-18", tau=r["tau"], rank=rank(r["tau"], est), argmax=top.index[0], lam_max=top.iloc[0],
                     lam_2nd=f"{top.index[1]}:{top.iloc[1]:.2f}", lam_2018=r["lam"].loc[2018],
                     tam_at_lam=float(r["lam"] @ YH.loc[s:2018, T]), tau_uniform_lambda=ru["tau"],
                     top_unit=f"{sh(r['w'].idxmax())} {r['w'].max():.2f}"))
print(pd.DataFrame(rows).round(2).to_string(index=False))
print("  Tambopata additions 2010-2018:", YH.loc[2010:2018, T].round(0).astype(int).tolist())
r14 = sdid(YH, T, (2014, 2018), DUR)
print("  lambda (2014-18):", r14["lam"].round(3).to_dict())
co = [u for u in YH.columns if u != T]
print(f"  controls' mean addition by year 2014-18 vs their 2019-21 mean ({YH.loc[2019:2021, co].mean().mean():.1f}):",
      YH.loc[2014:2018, co].mean(axis=1).round(1).to_dict())
# Tambopata's 2019-21 counterfactual baseline under each lambda choice
for yr in range(2010, 2019):
    print(f"    if all lambda on {yr}: Tambopata baseline {YH.loc[yr, T]:.0f}", end=";")
print()
print("  scaled panel, pre 2014-18: lambda", sdid(YS, T, (2014, 2018), DUR)["lam"].round(3).to_dict())

print("\nT3 unit weights (ha, pre 2014-18) and what those zones look like")
w = r14["w"][r14["w"] > 0.005].sort_values(ascending=False)
depts = bz.groupby(bz.buffer_zone + "|" + bz.pa_category).department.unique()
tab = pd.DataFrame({"weight": w, "mean_add_2014_18": YH.loc[2014:2018, w.index].mean(), "mean_add_2019_21": YH.loc[2019:2021, w.index].mean(),
                    "sd_add_2014_18": YH.loc[2014:2018, w.index].std(), "departments": depts.reindex(w.index).map(lambda d: ", ".join(sorted(d)))})
tab.index = tab.index.map(sh); print(tab.round(2).to_string())
syn = YH.loc[2014:2021, r14["w"].index] @ r14["w"]
print("  weighted comparison 2014-21 (ha):", syn.round(1).to_dict())
print("  Tambopata 2014-21 (ha):          ", YH.loc[2014:2021, T].round(0).to_dict())
print(f"  pre-period trend match: corr(Tambopata, weighted comparison) 2014-18 = {np.corrcoef(YH.loc[2014:2018, T], syn.loc[2014:2018])[0, 1]:.2f}; "
      f"demeaned pre-RMSPE {np.sqrt((((YH.loc[2014:2018, T] - YH.loc[2014:2018, T].mean()) - (syn.loc[2014:2018] - syn.loc[2014:2018].mean())) ** 2).mean()):.0f} ha; "
      f"sd of Tambopata 2014-18 {YH.loc[2014:2018, T].std(ddof=0):.0f}")

print("\nT4 leave-one-out (drop one comparison zone, ha, 2019-21, pre 2014-18)")
loo = {sh(u): sdid(YH.drop(columns=u), T, (2014, 2018), DUR)["tau"] for u in co}
print(pd.Series(loo).round(1).sort_values().to_string())
print(f"  range {min(loo.values()):.0f} to {max(loo.values()):.0f}; full sample {r14['tau']:.1f}")
loo11 = {sh(u): sdid(YH.drop(columns=u), T, (2011, 2018), DUR)["tau"] for u in co}
print(f"  same with pre 2011-18: range {min(loo11.values()):.0f} to {max(loo11.values()):.0f} (drop Amarakaeri {loo11['Amarakaeri']:.0f})")

print("\nT5 placebo SE and exchangeability")
est = placebo(YH, (2014, 2018), DUR)
size = YH.loc[2014:2018, co].abs().mean()
print(pd.DataFrame({"placebo_tau": est, "mean_abs_add_2014_18": size}).rename(index=sh).round(1).sort_values("placebo_tau").to_string())
print(f"  placebo SE {est.std(ddof=1):.1f} (repo {num['sdid_sdid_ha_during_se']:.1f}); corr(|placebo tau|, size) {np.corrcoef(est.abs(), size)[0, 1]:.2f}")
print(f"  Arkhangelsky Alg. 4 style 95% interval tau +/- 1.96 SE: [{r14['tau'] - 1.96 * est.std(ddof=1):.0f}, {r14['tau'] + 1.96 * est.std(ddof=1):.0f}]")
fd = YH.loc[2014:2018].diff().dropna()
print(f"  sd of yearly first differences 2014-18: Tambopata {fd[T].std():.0f} ha; controls median {fd[co].std().median():.1f}, max {fd[co].std().max():.0f} ({sh(fd[co].std().idxmax())})")
print(f"  Tambopata's own 2019-21 tau / its pre-period first-difference sd = {r14['tau'] / fd[T].std():.2f}")
ests = placebo(YS, (2014, 2018), DUR)
rs = sdid(YS, T, (2014, 2018), DUR)
print(f"  scaled: tau {rs['tau']:.3f}, placebos {sorted(np.round(ests.values, 2))}, rank {rank(rs['tau'], ests)} of {len(ests)+1}")

print("\nT6 placebo in time: SDID with a fake start s (pre s-5..s-1, post s..s+2, all before 2019), ha")
fake = {}
for s in range(2011, 2017):
    fake[s] = sdid(YH.loc[:2018], T, (s - 5, s - 1), (s, s + 2))["tau"]
print("  ", {k: round(v) for k, v in fake.items()})
real = r14["tau"]
print(f"  real {real:.0f}; fakes range {min(fake.values()):.0f} to {max(fake.values()):.0f}; rank of real among real + fakes {1 + sum(v <= real for v in fake.values())} of {len(fake)+1}")
fake3 = {s: sdid(YH.loc[:2018], T, (s - 3, s - 1), (s, s + 2))["tau"] for s in range(2009, 2017)}
print("   with 3 pre years:", {k: round(v) for k, v in fake3.items()})

print("\nT7 other pools (ha, pre 2014-18, 2019-21)")
AMZ = {T, A, B, "Allpahuayo Mishana|Reserva Nacional", "Cordillera Azul|Parque Nacional", "Alto Mayo|Bosque de Protección",
       "Pacaya-Samiria|Reserva Nacional", "El Sira|Reserva Comunal"}
for lab, cols in (("Amazon-department zones only", [u for u in poolB if u in AMZ]),
                  ("without Amarakaeri and Bahuaja-Sonene", [u for u in poolB if u not in (A, B)]),
                  ("without Amarakaeri", [u for u in poolB if u != A])):
    for pre in ((2014, 2018), (2011, 2018)):
        r = sdid(YH[cols], T, pre, DUR); e = placebo(YH[cols], pre, DUR)
        print(f"  {lab:40s} pre {pre[0]}-18: n {len(cols):2d}  tau {r['tau']:8.1f}  rank {rank(r['tau'], e)} of {len(e)+1}  "
              f"top unit {sh(r['w'].idxmax())} {r['w'].max():.2f}, argmax lambda {r['lam'].idxmax()} {r['lam'].max():.2f}")

print("\nT8 later years (ha, pre 2014-18)")
for lab, yrs in (("2022-25", None), ("2022, 2024, 2025 (no 2023)", [2022, 2024, 2025])):
    if yrs is None:
        r = sdid(YH, T, (2014, 2018), LAT); e = placebo(YH, (2014, 2018), LAT)
    else:
        Y2 = YH.drop(index=2023).copy(); Y2.index = [y if y < 2023 else y - 1 for y in Y2.index]   # 2022, 2024, 2025 -> 2022-24
        r = sdid(Y2, T, (2014, 2018), (2022, 2024)); e = placebo(Y2, (2014, 2018), (2022, 2024))
    print(f"  {lab:28s} tau {r['tau']:8.1f}  rank {rank(r['tau'], e)} of {len(e)+1}")
