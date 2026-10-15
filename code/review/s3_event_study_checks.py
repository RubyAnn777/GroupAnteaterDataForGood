"""Review session S3 (docs/methods/03_event_study_placebo.md): read-only checks of the event study and placebo inference.

Run from the repo root:  uv run python code/review/s3_event_study_checks.py   (writes nothing; ~10 s)
T1 reproduce pools A/B, pyfixest = closed form, registered numbers; T2 coefficient table by year;
T3 placebo-in-space rank for EVERY year and for pre-period statistics (does rank 1 fire before 2019?);
T4 reference period (2018 vs 2016-18 vs 2014-18 vs 2017-18); T5 scale-free statistics (own-pre scaling,
post/pre MSPE ratio, studentized gap); T6 one list of comparable lowland zones, ranks rerun;
T7 relative-magnitude bounds (Rambachan-Roth Delta^RM, point-identified worst case, no sampling error);
T8 what pool A's control mean is made of; T9 the figure's pools; T10 event-study placebo in time.
"""
import numpy as np, pandas as pd, pyfixest as pf

bz = pd.read_csv("data/peru_bufferzone_year.csv")
pe = pd.read_csv("data/peru_department_year.csv")
nums = pd.read_csv("output/numbers.csv").set_index("id")["value"]
bz["u"] = bz.buffer_zone + "|" + bz.pa_category
lv = bz.groupby(["u", "year"]).mining_ha.sum().unstack("u")
ad = lv.diff()
TU, AM, BA = "Tambopata|Reserva Nacional", "Amarakaeri|Reserva Comunal", "Bahuaja-Sonene|Parque Nacional"
Y0, Y1 = 2014, 2025
short = lambda u: u.split("|")[0]

def beta(w, t, ref=(2018,)):
    """Closed-form event-study coefficients, equal-weight control mean, reference = mean gap over `ref` years."""
    w = w.loc[Y0:Y1]
    gap = w[t] - w.drop(columns=t).mean(axis=1)
    return gap - gap.loc[list(ref)].mean()

def rank(real, others):              # common.placebo_rank: 1 + placebos at least as negative
    return 1 + int((np.asarray(list(others), float) <= real).sum())

# ---------------------------------------------------------------- T1 reproduce
in_mdd = set(bz.loc[bz.department == "Madre de Dios", "u"])
nz = ad.loc[2014:2018].abs().sum() > 0
poolA = sorted(u for u in in_mdd if nz[u]); poolB = sorted(nz[nz].index)
print("T1 pool A:", [short(u) for u in poolA])
print("   pool B (n=%d):" % len(poolB), [short(u) for u in poolB])
print("   Bahuaja-Sonene rows 2018 (dept, mining, total_ha):",
      bz[(bz.u == BA) & (bz.year == 2018)][["department", "mining_ha", "total_ha"]].round(1).values.tolist())
d = ad.loc[Y0:Y1, poolA].reset_index().melt(id_vars="year", var_name="unit", value_name="y")
ks = [k for k in range(Y0, Y1 + 1) if k != 2018]
for k in ks:
    d[f"d{k}"] = ((d.year == k) & (d.unit == TU)).astype(int)
fit = pf.feols("y ~ " + " + ".join(f"d{k}" for k in ks) + " | unit + year", data=d, vcov={"CRV1": "unit"})
bA, bB = beta(ad[poolA], TU), beta(ad[poolB], TU)
print("   pyfixest == closed form (pool A):", np.allclose([fit.coef()[f"d{k}"] for k in ks], bA.drop(2018).values, atol=1e-4))
print("   match numbers.csv:", all(abs(nums[f"eventstudy_beta_poolA_{k}"] - bA[k]) < 1e-6 for k in range(2019, 2026)),
      all(abs(nums[f"eventstudy_beta_poolB_{k}"] - bB[k]) < 1e-6 for k in range(2019, 2026)),
      abs(nums["eventstudy_pretrend_poolA_2016"] - bA[2016]) < 1e-6)
print("   CRV1 clusters:", d.unit.nunique(), "| dof note: with 3 clusters CRV1 SEs are meaningless")

# ---------------------------------------------------------------- T2 coefficient table
noTU = [u for u in poolB if u != TU]
ph = pd.DataFrame({u: beta(ad[noTU], u) for u in noTU})
tab = pd.DataFrame({"Tambopata add": ad.loc[Y0:Y1, TU], "ctrl mean A": ad.loc[Y0:Y1, [AM, BA]].mean(axis=1),
                    "beta A": bA, "beta B": bB, "band min": ph.min(axis=1), "band max": ph.max(axis=1)})
print("\nT2 event-study coefficients (ref 2018), ha/yr:\n", tab.round(0).to_string())

# ---------------------------------------------------------------- T3 rank in every year, incl. pre-years
def ranks_by_stat(w, pool, stat):
    others = [u for u in pool if u != TU]
    s = {u: stat(beta(w[others], u)) for u in others}
    real = stat(beta(w[pool], TU))
    return real, s, rank(real, s.values()), rank(-abs(real), [-abs(v) for v in s.values()])
print("\nT3 placebo-in-space rank (pool B, n=15; one-sided = most negative, two-sided = largest |.|):")
rows = []
for k in [y for y in range(Y0, Y1 + 1) if y != 2018]:
    real, s, r1, r2 = ranks_by_stat(ad, poolB, lambda b, k=k: b.loc[k])
    rows.append((k, round(real), round(min(s.values())), round(max(s.values())), r1, r2))
for lab, f in [("mean 2019-21 (headline)", lambda b: b.loc[2019:2021].mean()), ("2016 only", lambda b: b.loc[2016]),
               ("mean 2015-17", lambda b: b.loc[2015:2017].mean()), ("mean 2014-17", lambda b: b.loc[2014:2017].mean()),
               ("mean |pre beta| 2014-17", lambda b: -b.loc[2014:2017].abs().mean())]:
    real, s, r1, r2 = ranks_by_stat(ad, poolB, f)
    rows.append((lab, round(real), round(min(s.values())), round(max(s.values())), r1, r2))
print(pd.DataFrame(rows, columns=["stat", "Tambopata", "placebo min", "placebo max", "rank 1-sided", "rank |.|"]).to_string(index=False))
print("   (mean |pre beta| is negated so that 'rank 1' = the most volatile pre-period)")
print("   pre-period mean additions 2014-18:", ad.loc[2014:2018, poolB].mean().round(0).sort_values(ascending=False).to_dict())
print("   pre-period SD of additions 2014-18:", ad.loc[2014:2018, poolB].std().round(0).sort_values(ascending=False).head(4).to_dict())

# ---------------------------------------------------------------- T4 reference period
print("\nT4 mean 2019-21 coefficient by reference period:")
for ref in [(2018,), (2016, 2017, 2018), (2014, 2015, 2016, 2017, 2018), (2017, 2018), (2015, 2016, 2017), (2017,)]:
    a = beta(ad[poolA], TU, ref).loc[2019:2021].mean(); b = beta(ad[poolB], TU, ref).loc[2019:2021].mean()
    later = beta(ad[poolA], TU, ref).loc[2022:2025].mean()
    s = {u: beta(ad[noTU], u, ref).loc[2019:2021].mean() for u in noTU}
    print(f"  ref {str(ref):32s} pool A {a:7.0f}  pool B {b:7.0f}  rank B {rank(b, s.values())}/15   pool A 2022-25 {later:6.0f}")
print("  Amarakaeri additions 2014-18:", ad.loc[2014:2018, AM].round(0).tolist(), "| Tambopata:", ad.loc[2014:2018, TU].round(0).tolist())

# ---------------------------------------------------------------- T5 scale-free statistics
def scale_free(w, pool, label):
    others = [u for u in pool if u != TU]
    out = {}
    for u in pool:
        b = beta(w[pool], u) if u == TU else beta(w[others], u)
        pre_mean = w.loc[2014:2018, u].mean()
        pre = b.loc[2014:2017]; post = b.loc[2019:2021]
        out[u] = dict(raw=post.mean(),
                      scaled=post.mean() / pre_mean if pre_mean > 0 else np.nan,
                      mspe_ratio=-(post ** 2).mean() / max((pd.concat([pre, pd.Series([0.0])]) ** 2).mean(), 1e-9),
                      studentized=post.mean() / pre.std(ddof=1) if pre.std(ddof=1) > 0 else np.nan)
    o = pd.DataFrame(out).T
    res = {}
    for c in o.columns:
        others_v = o.loc[others, c].dropna()
        res[c] = f"{rank(o.loc[TU, c], others_v)}/{len(others_v) + 1}"
    print(f"  {label:42s}", res)
    return o
print("\nT5 Tambopata's rank under scale-free statistics (1 = most negative; mspe_ratio negated: 1 = largest post/pre MSPE):")
o = scale_free(ad, poolB, "pool B (15)")
print("   pool B detail:\n", o.round(2).sort_values("scaled").to_string())

# ---------------------------------------------------------------- T6 one comparable list
amz_dept = set(pe.loc[pe.biome == "Amazonía", "department"])
zr = bz[bz.department.isin(amz_dept)]
ad_rows = zr.groupby(["u", "year"]).mining_ha.sum().unstack("u").diff()
pre_r = ad_rows.loc[2014:2018].mean()
restricted = sorted(u for u in pre_r.index if pre_r[u] > 10)
MODELS_AMAZON = sorted({TU, AM, BA, "Allpahuayo Mishana|Reserva Nacional", "Cordillera Azul|Parque Nacional",
                        "Alto Mayo|Bosque de Protección", "Pacaya-Samiria|Reserva Nacional", "El Sira|Reserva Comunal"})
stock18 = lv.loc[2018]
LOWLAND_MINING = sorted(u for u in MODELS_AMAZON if stock18[u] >= 50)
print("\nT6 three 'Amazon' definitions + proposal:")
print("   peru.py placebo_restricted (rows in Amazon-biome depts, pre mean >10):", [short(u) for u in restricted])
print("   where their 2018 mining lies:", {short(u): bz[(bz.u == u) & (bz.year == 2018) & (bz.mining_ha > 0)].department.tolist() for u in restricted})
print("   peru_models.AMAZON (8):", [short(u) for u in MODELS_AMAZON])
print("   proposal subset: AMAZON with 2018 stock >= 50 ha:", [short(u) for u in LOWLAND_MINING], {short(u): round(stock18[u]) for u in LOWLAND_MINING})
scale_free(ad_rows, restricted, "peru.py restricted (6, rows-based)")
scale_free(ad, MODELS_AMAZON, "peru_models AMAZON (8)")
scale_free(ad, LOWLAND_MINING, "lowland, stock>=50 ha (5)")
scale_free(ad, [u for u in MODELS_AMAZON if u != AM], "AMAZON without Amarakaeri (7)")
for pool, lab in [(MODELS_AMAZON, "AMAZON 8"), (LOWLAND_MINING, "lowland 5")]:
    real, s, r1, _ = ranks_by_stat(ad, pool, lambda b: b.loc[2016])
    print(f"   2016 coefficient, {lab}: Tambopata {real:.0f}, placebos {min(s.values()):.0f}..{max(s.values()):.0f}, rank {r1}/{len(pool)}")
    print(f"   {lab} coefficients 2014-25:", beta(ad[pool], TU).round(0).astype(int).to_dict())

# ---------------------------------------------------------------- T7 relative magnitudes
print("\nT7 Rambachan-Roth relative magnitudes (Delta^RM), point estimates only (no sampling error available):")
for lab, b in [("pool A", bA), ("pool B", bB), ("AMAZON 8", beta(ad[MODELS_AMAZON], TU))]:
    pre = b.loc[2014:2018]                       # includes the 0 at 2018
    steps = pre.diff().dropna().abs(); mx = steps.max()
    theta = b.loc[2019:2021].mean()
    # worst-case bias in post year k (k = 1,2,3) under Delta^RM(Mbar) is k*Mbar*mx; mean over 2019-21 -> 2*Mbar*mx
    print(f"  {lab}: pre steps {steps.round(0).astype(int).tolist()}, max {mx:.0f}; theta(2019-21) {theta:.0f}; "
          f"breakdown Mbar (mean 2019-21) = {abs(theta)/(2*mx):.2f}; 2019 alone = {abs(b[2019])/mx:.2f}; "
          f"set at Mbar=1: [{theta-2*mx:.0f}, {theta+2*mx:.0f}]; max|pre beta| {pre.abs().max():.0f} vs |theta| {abs(theta):.0f}")
    # alternative without the 2016 dip: max step among the steps not touching 2016
    st2 = [abs(pre[2015] - pre[2014]), abs(pre[2018] - pre[2017])]
    print(f"     steps not touching 2016: {np.round(st2).astype(int).tolist()} -> breakdown Mbar {abs(theta)/(2*max(st2)):.2f}")

# ---------------------------------------------------------------- T8 pool A's control
print("\nT8 pool A control = equal-weight mean of Amarakaeri and Bahuaja-Sonene (all rows):")
c = pd.DataFrame({"Amarakaeri": ad.loc[2014:2025, AM], "Bahuaja": ad.loc[2014:2025, BA]})
c["control mean"] = c.mean(axis=1); c["Amarakaeri share of |ctrl|"] = (c.Amarakaeri / 2).abs() / ((c.Amarakaeri / 2).abs() + (c.Bahuaja / 2).abs())
print(c.round(2).to_string())
for lab, ctrl in [("no control (Tambopata vs its own 2018)", None), ("Amarakaeri only", [AM]), ("Bahuaja only", [BA]), ("pool A (both, equal weight)", [AM, BA])]:
    t = ad.loc[Y0:Y1, TU]; g = t - (ad.loc[Y0:Y1, ctrl].mean(axis=1) if ctrl else 0)
    b = g - g.loc[2018]
    print(f"  {lab:42s} mean 2019-21 {b.loc[2019:2021].mean():7.0f}   2016 {b.loc[2016]:7.0f}   2022-25 {b.loc[2022:2025].mean():6.0f}")

# ---------------------------------------------------------------- T9 the figure's band
print("\nT9 figure: line = pool A, band = pool B placebos (each zone treated vs the other 13).")
phA = {u: beta(ad[[v for v in poolA if v != TU]], u) for u in poolA if u != TU}
print("   a pool-A band would have only", len(phA), "placebo lines:", {short(u): b.loc[2019:2021].mean().round(0) for u, b in phA.items()})
print("   years where pool-A line is below the pool-B band min:", [k for k in tab.index if k != 2018 and tab.loc[k, "beta A"] < tab.loc[k, "band min"]])

# ---------------------------------------------------------------- T10 placebo in time on the event-study statistic
print("\nT10 placebo in time, pool B gap: stat(s) = mean gap s..s+2 minus gap s-1 (the event-study statistic at a fake date):")
w = ad[poolB]; gap = w[TU] - w.drop(columns=TU).mean(axis=1)
fk = {s: gap.loc[s:s + 2].mean() - gap.loc[s - 1] for s in range(2003, 2017)}
real = gap.loc[2019:2021].mean() - gap.loc[2018]
print("   fakes:", {s: round(v) for s, v in fk.items()})
print(f"   real {real:.0f}: rank {rank(real, fk.values())} of {len(fk)+1}; with pooled ref 2014-18 the real is {gap.loc[2019:2021].mean()-gap.loc[2014:2018].mean():.0f}")
fk2 = {s: gap.loc[s:s + 2].mean() - gap.loc[s - 5:s - 1].mean() for s in range(2003, 2017)}
r2 = gap.loc[2019:2021].mean() - gap.loc[2014:2018].mean()
print(f"   5-yr pooled ref: fakes {min(fk2.values()):.0f}..{max(fk2.values()):.0f}; real {r2:.0f} rank {rank(r2, fk2.values())} of {len(fk2)+1}")
