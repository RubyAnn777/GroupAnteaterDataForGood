"""Review session S6 (docs/methods/06_synthetic_control.md): read-only checks of the synthetic control (attempt A5).

Run from the repo root:  uv run python code/review/s6_synth_checks.py   (writes nothing; about 5 min, mostly the placebo loops)
Reads data/peru_bufferzone_year.csv and output/numbers.csv only. Not part of main.py.
Re-implements the solver (projected gradient on the simplex, not SLSQP) so the reproduction is independent of
code/peru_synth.py, then:
T1 reproduce the six specs (core/ext x add/addsc/cum): weights, pre-RMSPE, gaps, ratio ranks
T2 convex hull: Tambopata vs the donor maximum in every fit year
T3 the scaled spec: year-by-year gaps, which statistic gives "rank 1", one-sided 2019-21 statistics
T4 the -411: the SC inside peru_sdid (pool B, fit 2014-18, no intercept) vs peru_synth ext_add, one estimate, two ranks
T5 an aligned spec (pool B as in the ladder/SDID, fit 2014-18, 2019-21) under four rank statistics + ADH pre-fit filter
T6 the cumulative spec: why the weights are 1/3, 1/3, 1/3
T7 pre-fit quality relative to the gap (how big must the pre-fit error be before a gap means nothing)
"""
import numpy as np, pandas as pd
pd.set_option("display.width", 200)

bz = pd.read_csv("data/peru_bufferzone_year.csv")
lw = bz.assign(u=bz.buffer_zone + "|" + bz.pa_category).groupby(["u", "year"]).mining_ha.sum().unstack("u")
ad = lw.diff()
T, A, B = "Tambopata|Reserva Nacional", "Amarakaeri|Reserva Comunal", "Bahuaja-Sonene|Parque Nacional"
POST = list(range(2019, 2026)); D = list(range(2019, 2022)); L = list(range(2022, 2026))
num = pd.read_csv("output/numbers.csv").set_index("id")["value"]
sh = lambda u: u.split("|")[0]


def proj_simplex(v):
    u = np.sort(v)[::-1]; css = np.cumsum(u)
    k = np.nonzero(u * np.arange(1, len(v) + 1) > (css - 1))[0][-1]
    return np.maximum(v - (css[k] - 1) / (k + 1), 0)


def simplex_ls(A_, b, intercept=False, iters=100000, tol=1e-12):
    """min ||c + A w - b||^2 over the simplex (c free only if intercept). FISTA with adaptive restart from the
    uniform start (the problem is convex, so one start reaches the global minimum; peru_synth uses SLSQP)."""
    if intercept:
        A_ = A_ - A_.mean(0); b = b - b.mean()
    Lc = 2 * np.linalg.norm(A_, 2) ** 2
    f = lambda w: float(np.sum((A_ @ w - b) ** 2))
    w = z = np.full(A_.shape[1], 1 / A_.shape[1]); t = 1.0
    for _ in range(iters):
        wn = proj_simplex(z - 2 * A_.T @ (A_ @ z - b) / Lc)
        if f(wn) > f(w):                       # adaptive restart
            z, t = w, 1.0; continue
        tn = (1 + np.sqrt(1 + 4 * t * t)) / 2
        z = wn + (t - 1) / tn * (wn - w)
        if np.abs(wn - w).max() < tol:
            w = wn; break
        w, t = wn, tn
    return w


def synth(P, fit, tr, donors, post=POST, intercept=False):
    w = simplex_ls(P.loc[fit, donors].to_numpy(), P.loc[fit, tr].to_numpy(), intercept)
    s = P[donors] @ w
    if intercept:
        s = s + (P.loc[fit, tr] - s.loc[fit]).mean()
    gap = P[tr] - s
    pre = float(np.sqrt((gap.loc[fit] ** 2).mean()))
    return dict(w=pd.Series(w, donors), synth=s, gap=gap, pre=pre,
                post=float(np.sqrt((gap.loc[post] ** 2).mean())))


def pool(kind, which):
    elig = ad.loc[2010:2018].abs().mean() >= 1.0
    names = [u for u in lw.columns if elig[u] and u != T]
    if which == "core":
        names = [u for u in names if u not in (A, B)]
    if kind == "addsc":
        s = ad.loc[2014:2018].abs().mean(); names = [u for u in names if s[u] >= 5.0]
    return names


def panel(kind):
    if kind == "add":
        return ad.loc[2010:2025], list(range(2010, 2019)), None
    if kind == "addsc":
        s = ad.loc[2014:2018].abs().mean(); return ad.loc[2010:2025] / s, list(range(2010, 2019)), s
    return lw.loc[2013:2025] - lw.loc[2013], list(range(2014, 2019)), None


def placebos(P, fit, donors, post=POST, intercept=False):
    out = {}
    for d in donors:
        o = [x for x in donors if x != d]
        if len(o) >= 2:
            out[d] = synth(P, fit, d, o, post, intercept)
    return out


print("T1 reproduce the six specs (own projected-gradient solver)")
store = {}
for which in ("core", "ext"):
    for kind in ("add", "addsc", "cum"):
        P, fit, s = panel(kind); donors = pool(kind, which)
        m = synth(P, fit, T, donors); pl = placebos(P, fit, donors)
        ratios = pd.Series({T: m["post"] / m["pre"], **{d: r["post"] / r["pre"] for d, r in pl.items()}})
        rank = int((ratios > ratios[T]).sum() + 1)
        sc = s[T] if s is not None else 1.0
        key = f"{which}_{kind}"; store[key] = (P, fit, s, donors, m, pl)
        top = ", ".join(f"{sh(u)} {v:.3f}" for u, v in m["w"].sort_values(ascending=False).head(3).items())
        print(f"  {key:10s} donors {len(donors):2d} preRMSPE {m['pre']*sc:8.1f} (repo {num[f'synth_{key}_pre_rmspe']:8.1f})"
              f"  gap19-21 {m['gap'].loc[2019:2021].mean()*sc:8.1f} (repo {num[f'synth_{key}_gap_2019_21']:8.1f})"
              f"  gap22-25 {m['gap'].loc[2022:2025].mean()*sc:8.1f}  ratio rank {rank}/{len(ratios)} (repo {num[f'synth_{key}_rank']:.0f})  w: {top}")

print("\nT2 convex hull (fit years): Tambopata vs donor min/max, ha")
for key in ("core_add", "ext_add"):
    P, fit, _, donors, m, _ = store[key]
    t = pd.DataFrame({"Tambopata": P.loc[fit, T], "donor max": P.loc[fit, donors].max(axis=1),
                      "argmax": P.loc[fit, donors].idxmax(axis=1).map(sh), "donor min": P.loc[fit, donors].min(axis=1)})
    print(f"  {key}:\n" + t.round(0).to_string().replace("\n", "\n    "))
    print(f"  {key}: Tambopata above every donor in {(t['Tambopata'] > t['donor max']).sum()} of {len(fit)} fit years; "
          f"synthetic pre-mean {m['synth'].loc[fit].mean():.1f} vs Tambopata {P.loc[fit, T].mean():.1f}")

print("\nT3 scaled spec (core_addsc): gaps by year in units of Tambopata's own 2014-18 mean |addition|")
P, fit, s, donors, m, pl = store["core_addsc"]
print(f"  Tambopata scale = {s[T]:.1f} ha; donors and scales:", {sh(d): round(s[d], 1) for d in donors})
g = pd.DataFrame({"Tambopata": m["gap"], **{sh(d): r["gap"] for d, r in pl.items()}}).loc[2010:2025]
print(g.round(2).T.to_string())
stats = pd.DataFrame({
    "pre_rmspe": {T: m["pre"], **{d: r["pre"] for d, r in pl.items()}},
    "ratio_2019_25": {T: m["post"] / m["pre"], **{d: r["post"] / r["pre"] for d, r in pl.items()}},
    "ratio_2019_21": {T: np.sqrt((m["gap"].loc[D] ** 2).mean()) / m["pre"], **{d: np.sqrt((r["gap"].loc[D] ** 2).mean()) / r["pre"] for d, r in pl.items()}},
    "mean_gap_2019_21": {T: m["gap"].loc[D].mean(), **{d: r["gap"].loc[D].mean() for d, r in pl.items()}},
    "mean_gap_2019_21_over_pre": {T: m["gap"].loc[D].mean() / m["pre"], **{d: r["gap"].loc[D].mean() / r["pre"] for d, r in pl.items()}},
    "mean_gap_2022_25": {T: m["gap"].loc[L].mean(), **{d: r["gap"].loc[L].mean() for d, r in pl.items()}},
})
stats.index = [sh(u) for u in stats.index]
print(stats.round(2).to_string())
rk = lambda col, asc: int(stats[col].rank(ascending=asc, method="min")["Tambopata"])
print(f"  ranks (1 = most extreme in the stated direction, of {len(stats)}): ratio 2019-25 (two-sided) {rk('ratio_2019_25', False)}, "
      f"ratio 2019-21 {rk('ratio_2019_21', False)}, most negative mean gap 2019-21 {rk('mean_gap_2019_21', True)}, "
      f"most negative gap/pre 2019-21 {rk('mean_gap_2019_21_over_pre', True)}, most positive mean gap 2022-25 {rk('mean_gap_2022_25', False)}")
print(f"  in ha: 2019-21 gap {m['gap'].loc[D].mean()*s[T]:.0f}, 2022-25 gap {m['gap'].loc[L].mean()*s[T]:.0f}; "
      f"share of Tambopata's post RMSPE^2 from 2022-25: {(m['gap'].loc[L]**2).sum()/(m['gap'].loc[POST]**2).sum():.0%}")
dec = pd.DataFrame({"Tambopata (scaled)": P[T], "synthetic": m["synth"], "gap": m["gap"]}).loc[2014:2025]
print("  Tambopata, its synthetic and the gap, scaled units:\n   ", dec.round(2).T.to_string().replace("\n", "\n    "))
own = P.loc[D, T].mean() - P.loc[2014:2018, T].mean(); syn_ch = m["synth"].loc[D].mean() - m["synth"].loc[2014:2018].mean()
print(f"  2019-21 vs 2014-18: Tambopata's own change {own:.2f} ({own*s[T]:.0f} ha), synthetic's change {syn_ch:+.2f} ({syn_ch*s[T]:+.0f} ha)")
print("  Cotahuasi raw additions 2014-25 (ha):", ad.loc[2014:2025, "Subcuenca del Cotahuasi|Reserva Paisajistica"].round(0).astype(int).tolist())
# what the donors are
for d in donors:
    rows = bz[(bz.buffer_zone + "|" + bz.pa_category == d) & (bz.year == 2018)]
    print(f"    {sh(d):26s} weight {m['w'][d]:.3f}  departments {sorted(rows.department.unique())}  mining 2018 {rows.mining_ha.sum():.0f} ha")
P2, fit2, s2, donors2, m2, pl2 = store["ext_addsc"]
r2 = {T: m2["gap"].loc[D].mean(), **{d: r["gap"].loc[D].mean() for d, r in pl2.items()}}
print(f"  ext_addsc: 2019-21 mean gap {m2['gap'].loc[D].mean():.2f}, 2022-25 {m2['gap'].loc[L].mean():.2f}; one-sided rank on 2019-21 gap "
      f"{1 + sum(v <= r2[T] for k, v in r2.items() if k != T)} of {len(r2)}")

print("\nT4 the -411: SC inside peru_sdid (pool B, fit 2014-18, 2019-21) vs peru_synth ext_add (fit 2010-18)")
poolB = sorted(u for u in ad.columns if ad.loc[2014:2018, u].abs().sum() > 0)
Pb = ad.loc[2010:2025, poolB]; fitB = list(range(2014, 2019))
mb = synth(Pb, fitB, T, [u for u in poolB if u != T], post=D)
print(f"  pool B {len(poolB)} zones; weights > 0.01:", {sh(u): round(v, 3) for u, v in mb['w'].items() if v > 0.01})
print(f"  2019-21 gap {mb['gap'].loc[D].mean():.1f} (repo sdid_sc_ha_during {num['sdid_sc_ha_during']:.1f}); pre-RMSPE 2014-18 {mb['pre']:.1f}; "
      f"Tambopata pre-mean {Pb.loc[fitB, T].mean():.0f} vs synthetic {mb['synth'].loc[fitB].mean():.0f}")
print("  Tambopata vs Amarakaeri 2014-21:\n   ", Pb.loc[2014:2021, [T, A]].round(0).T.rename(index=sh).to_string().replace("\n", "\n    "))
others = [u for u in poolB if u != T]
plb = {u: synth(Pb[others], fitB, u, [v for v in others if v != u], post=D) for u in others}
tau = {u: r["gap"].loc[D].mean() for u, r in plb.items()}
rat = {u: r["post"] / r["pre"] for u, r in plb.items()}
print(f"  rank by signed 2019-21 gap (peru_sdid's statistic): {1 + sum(v <= mb['gap'].loc[D].mean() for v in tau.values())} of {len(tau)+1}")
print(f"  rank by post/pre RMSPE ratio (peru_synth's statistic): {1 + sum(v > mb['post']/mb['pre'] for v in rat.values())} of {len(rat)+1}; "
      f"Tambopata ratio {mb['post']/mb['pre']:.2f}")
print(f"  placebo pre-RMSPEs: median {np.median([r['pre'] for r in plb.values()]):.1f}, max {max(r['pre'] for r in plb.values()):.1f}  vs Tambopata {mb['pre']:.1f}")
print(f"  pre-fit error / |gap| = {mb['pre']/abs(mb['gap'].loc[D].mean()):.2f}")

print("\nT5 aligned spec (pool B, fit 2014-18, post 2019-21), four rank statistics, and ADH pre-fit filters")
for lab, intercept in (("SC, no intercept", False), ("SC with intercept (demeaned SC)", True)):
    mt = synth(Pb, fitB, T, others, post=D, intercept=intercept)
    pp = {u: synth(Pb[others], fitB, u, [v for v in others if v != u], post=D, intercept=intercept) for u in others}
    gt = mt["gap"].loc[D].mean()
    gp = {u: r["gap"].loc[D].mean() for u, r in pp.items()}
    n = len(pp) + 1
    r_signed = 1 + sum(v <= gt for v in gp.values())
    r_abs = 1 + sum(abs(v) >= abs(gt) for v in gp.values())
    r_ratio = 1 + sum(r["post"] / r["pre"] > mt["post"] / mt["pre"] for r in pp.values())
    r_std = 1 + sum(gp[u] / pp[u]["pre"] <= gt / mt["pre"] for u in pp)
    print(f"  {lab}: gap {gt:.0f}, pre-RMSPE {mt['pre']:.0f}; ranks of {n}: signed {r_signed}, |gap| {r_abs}, RMSPE ratio {r_ratio}, gap/pre-RMSPE {r_std}")
    print("     weights > 0.01:", {sh(u): round(v, 3) for u, v in mt['w'].items() if v > 0.01})
    for k in (2, 5, 20):
        keep = [u for u in pp if pp[u]["pre"] <= k * mt["pre"]]
        print(f"     ADH filter: keep placebos with pre-RMSPE <= {k}x Tambopata's: {len(keep)} kept; signed rank "
              f"{1 + sum(gp[u] <= gt for u in keep)} of {len(keep)+1}")

print("\nT6 cumulative spec (core_cum): why 1/3, 1/3, 1/3")
P, fit, _, donors, m, _ = store["core_cum"]
print("  donors' cumulative additions 2014-18 (ha):\n   ", P.loc[fit, donors].rename(columns=sh).round(1).to_string().replace("\n", "\n    "))
print("  Tambopata:", P.loc[fit, T].round(0).tolist())
print("  weights:", {sh(u): round(v, 3) for u, v in m['w'].items() if v > 0.001})
rw = pd.read_csv("output/peru_synth_weights.csv")
for key in ("core_add", "core_cum", "ext_add", "ext_cum"):
    P, fit, _, donors, m, _ = store[key]
    wr = rw[rw.spec == key].set_index("donor")["weight"].reindex(donors).fillna(0)
    obj = lambda w: float(((P.loc[fit, T] - P.loc[fit, donors] @ w) ** 2).sum())
    print(f"  {key}: pre-period SSR at repo (SLSQP) weights {obj(wr):,.0f} vs at our optimum {obj(m['w']):,.0f}"
          f"  (repo top weights {', '.join(f'{sh(u)} {v:.2f}' for u, v in wr.sort_values(ascending=False).head(3).items())})")

print("\nT7 pre-fit quality vs gap, all specs (ha; scaled specs unscaled by Tambopata's own mean)")
for key, (P, fit, s, donors, m, _) in store.items():
    sc = s[T] if s is not None else 1.0
    gD = m["gap"].loc[D].mean() * sc
    print(f"  {key:10s} pre-RMSPE {m['pre']*sc:8.0f}  gap 2019-21 {gD:8.0f}  |gap|/preRMSPE {abs(gD)/(m['pre']*sc):5.2f}  "
          f"pre-RMSPE as % of Tambopata pre-mean |y| {m['pre']*sc/(P.loc[fit, T].abs().mean()*sc):5.0%}")
