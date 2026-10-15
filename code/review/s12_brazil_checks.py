"""Review session S12 (docs/methods/12_brazil.md): read-only checks of the Brazil designs A12-A14.

Run from the repo root:  uv run python code/review/s12_brazil_checks.py   (writes nothing; ~2 min)
A12 = 2x2 in brazil.py (Col 10.1 workbook), A13 = per-territory before/after vs pool in brazil_stagger.py (AMW),
A14 = staggered DiD (TWFE, did2s) + randomization inference in brazil_v2.py (Col 11 raster panel).
T1 reproduce A14 · T2 all-zero units · T3 event study with leads (TWFE dummies, did2s, Callaway-Sant'Anna by hand)
T4 TWFE weights (de Chaisemartin-D'Haultfoeuille) · T5 treatment dating variants · T6 randomization inference variants
T7 never-treated pools (A13, A14) · T8 products disagree (Col 10.1, Col 11, AMW, DETER) · T9 IBAMA
T10 A12 2x2 reproduce + windows + fake start years · T11 unit definitions.
Inputs: data_intermediate/{brazil_raster_unit_year, operations_coded, amw_candidates_year, amw_candidates_units,
deter_ti_month, ibama_autos_annual}.csv, data_raw/mapbiomas_brazil/*COL.10.1*.xlsx, output/numbers.csv.
"""
import sys, re, warnings
from pathlib import Path
import numpy as np, pandas as pd
import pyfixest as pf

warnings.filterwarnings("ignore")
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "code"))
import brazil_v2 as bv2            # read-only import (first_operations, first_treat_year, did, ri)

I = ROOT / "data_intermediate"
NUM = pd.read_csv(ROOT / "output/numbers.csv").set_index("id").value
pd.set_option("display.width", 200)

# ------------------------------------------------------------------ panel helpers
raw = pd.read_csv(I / "brazil_raster_unit_year.csv")
names = raw.drop_duplicates("unit_id").set_index("unit_id").unit
P0 = raw[raw.year.between(2014, 2025) & ~raw.unit_id.str.startswith("Yanomami_ring")].copy()
P0["ln_new"] = np.log1p(P0.new_land_ha.fillna(0))
ZERO = sorted(P0.groupby("unit_id").mining_ha.max().loc[lambda s: s == 0].index)


def ftyear(ym, rule="halfyear"):
    y, m = int(ym[:4]), int(ym[5:7])
    return y + (1 if (rule == "halfyear" and m >= 7) else 0)


def panel(dates: dict, drop=(), rule="halfyear"):
    p = P0[~P0.unit_id.isin(drop)].copy()
    ft = {u: ftyear(v, rule) for u, v in dates.items() if v}
    p["first_treat"] = p.unit_id.map(ft).fillna(0).astype(int)
    p["treat"] = ((p.first_treat > 0) & (p.year >= p.first_treat)).astype(int)
    return p


def twfe(p, y="ln_new"):
    f = pf.feols(f"{y} ~ treat | unit_id + year", data=p, vcov={"CRV1": "unit_id"})
    return f.coef()["treat"], f.pvalue()["treat"]


def did2s(p, y="ln_new"):
    g = pf.did2s(p, yname=y, first_stage="~ 0 | unit_id + year", second_stage="~ treat", treatment="treat", cluster="unit_id")
    return g.coef()["treat"], g.pvalue()["treat"]


def did2s_point(p, y="ln_new"):
    """Gardner stage 1 on untreated cells (unit + year effects by least squares), stage 2 = mean residual on treated cells."""
    u = pd.get_dummies(p.unit_id).astype(float).values; t = pd.get_dummies(p.year).astype(float).values[:, 1:]
    X = np.hstack([u, t]); m = p.treat.values == 0
    b = np.linalg.lstsq(X[m], p[y].values[m], rcond=None)[0]
    r = p[y].values - X @ b
    return r[p.treat.values == 1].mean()


_fo = bv2.first_operations()
BASE = _fo[_fo.index.isin(P0.unit_id.unique())]                   # unit -> 'YYYY-MM' as coded (panel units only)

print("=" * 100, "\nT1 reproduce A14 (brazil_v2): 24 units, 11 treated, ln(1 + first-time ha), 2014-2025")
p, tw, g = bv2.did(bv2.load())
print("coded first operations:", {names[k]: v for k, v in BASE.items()})
print(f"  TWFE {tw.coef()['treat']:+.3f} (p {tw.pvalue()['treat']:.3f}) vs numbers.csv {NUM['brv2_twfe_treat']:+.3f} ({NUM['brv2_twfe_treat_p']:.3f})")
print(f"  did2s {g[0]:+.3f} (p {g[2]:.3f}) vs numbers.csv {NUM['brv2_did2s_treat']:+.3f} ({NUM['brv2_did2s_treat_p']:.3f})")
pb = panel(BASE)
print(f"  own panel(): TWFE {twfe(pb)[0]:+.3f}; did2s {did2s(pb)[0]:+.3f}; manual did2s point {did2s_point(pb):+.3f}")
real, rip, _ = bv2.ri(p, reps=2000, seed=0)
print(f"  RI p (2000 shuffles, seed 0) {rip:.3f} vs numbers.csv {NUM['brv2_ri_p']:.3f}")
ft = pb.groupby("unit_id").first_treat.first()
print("  treated units and first treated year:", {names[u]: int(v) for u, v in ft[ft > 0].items()})
print("  treated units with only ONE post year (first treated 2025):", [names[u] for u in ft[ft == 2025].index])

print("\n" + "=" * 100, "\nT2 units with zero MapBiomas mining in EVERY year 2014-2025 (Col 11 raster)")
print(f"  {len(ZERO)} of {P0.unit_id.nunique()} territories:", [names[u] for u in ZERO])
amw = pd.read_csv(I / "amw_candidates_year.csv"); amwtot = amw.groupby("unit_id").new_ha.sum()
print("  AMW new area 2019-25 in these zero units (selection used AMW >= 50 ha, brazil_raster.py:36-37):")
print("   ", {names[u]: round(amwtot.get(u, np.nan)) for u in ZERO})
print(f"  treated among them: {[names[u] for u in ZERO if u in BASE.index]}")
pz = panel(BASE, drop=ZERO)
print(f"  baseline  : TWFE {twfe(pb)[0]:+.3f} (p {twfe(pb)[1]:.3f}); did2s {did2s(pb)[0]:+.3f} (p {did2s(pb)[1]:.3f}); N units {pb.unit_id.nunique()}")
print(f"  drop zeros: TWFE {twfe(pz)[0]:+.3f} (p {twfe(pz)[1]:.3f}); did2s {did2s(pz)[0]:+.3f} (p {did2s(pz)[1]:.3f}); N units {pz.unit_id.nunique()}, treated {pz[pz.first_treat>0].unit_id.nunique()}")
# Col 10.1 workbook: do the zero units have any mining row there either?
x = pd.read_excel(ROOT / "data_raw/mapbiomas_brazil/MAPBIOMAS_BRAZIL-COVERAGE_STATISTICS-COL.10.1-INDIGENOUS_TERRITORIES_STATE_BIOME.xlsx",
                  sheet_name="COVERAGE_INDIGENOUS_TERRITORIES")
yc = [c for c in x.columns if isinstance(c, (int, np.integer))]
w101 = x[x.class_id == 30].groupby("geocode")[yc].sum().T
codes = {u: int(u.split("-")[-1]) for u in P0.unit_id.unique()}
print("  Col 10.1 workbook, zero units with a mining row:", [names[u] for u in ZERO if codes[u] in w101.columns and w101[codes[u]].max() > 0],
      "| zero units absent from the workbook entirely:", [names[u] for u in ZERO if codes[u] not in set(x.geocode)])

print("\n" + "=" * 100, "\nT3 event study with leads")
m = pz.copy(); m["grp"] = np.where(m.first_treat > 0, "treated", "never")
gm = m.groupby(["grp", "year"]).ln_new.mean().unstack(0)
print("  T3a raw means of ln(1+first-time ha), mining units only (12 units):\n", gm.round(2).T.to_string())
gmall = pb.assign(grp=np.where(pb.first_treat > 0, "treated", "never")).groupby(["grp", "year"]).ln_new.mean().unstack(0)
print("  same, all 24 units:\n", gmall.round(2).T.to_string())
for lab, q in (("all 24 units", pb), ("mining units only", pz)):
    q = q.copy(); q["rel"] = np.where(q.first_treat > 0, q.year - q.first_treat, -1000)
    tr = q[q.first_treat > 0]
    print(f"  T3b mean ln_new by event time, treated, {lab}:", tr.groupby("rel").ln_new.mean().round(2).to_dict())
    q["relb"] = q.rel.clip(-6, 2).where(q.first_treat > 0, -1000)
    f = pf.feols("ln_new ~ i(relb, ref=-1) | unit_id + year", data=q.assign(relb=q.relb.replace(-1000, -1)), vcov={"CRV1": "unit_id"})
    tb = f.tidy()[["Estimate", "Pr(>|t|)"]].round(3)
    print(f"  T3c TWFE event study (event time binned at -6 and +2, ref -1, never-treated coded -1), {lab}:\n", tb.to_string())
    try:
        q2 = q.assign(rel_year=q.rel.clip(-6, 2).astype(float).where(q.first_treat > 0, np.inf))
        e = pf.did2s(q2, yname="ln_new", first_stage="~ 0 | unit_id + year",
                     second_stage="~ i(rel_year, ref=-1.0)", treatment="treat", cluster="unit_id")
        print(f"  T3d did2s event study, {lab}:\n", e.tidy()[["Estimate", "Pr(>|t|)"]].round(3).to_string())
    except Exception as ex:
        print("  did2s event study failed:", ex)


def cs_att(q):
    """Callaway-Sant'Anna ATT(g,t), never-treated control, base g-1 (long difference), unweighted means."""
    never = q[q.first_treat == 0].pivot(index="year", columns="unit_id", values="ln_new").mean(axis=1)
    out = []
    for gg in sorted(q.first_treat[q.first_treat > 0].unique()):
        tg = q[q.first_treat == gg].pivot(index="year", columns="unit_id", values="ln_new").mean(axis=1)
        n = q[q.first_treat == gg].unit_id.nunique()
        for t in range(2014, 2026):
            if t == gg - 1: continue
            out.append(dict(g=gg, t=t, e=t - gg, n=n, att=(tg[t] - tg[gg - 1]) - (never[t] - never[gg - 1])))
    return pd.DataFrame(out)


for lab, q in (("all 24 units", pb), ("mining units only", pz)):
    a = cs_att(q)
    ev = a.groupby("e").apply(lambda s: np.average(s.att, weights=s.n)).round(2)
    post = a[a.e >= 0]; overall = np.average(post.att, weights=post.n)
    print(f"  T3e Callaway-Sant'Anna (never-treated control, base g-1), {lab}: overall post ATT {overall:+.3f}")
    print("      by event time:", ev.loc[-9:3].to_dict())
    print("      cohorts:", a.groupby("g").n.first().to_dict())

print("\n" + "=" * 100, "\nT4 TWFE implicit weights on treated cells (de Chaisemartin and D'Haultfoeuille 2020)")
for lab, q in (("all 24 units", pb), ("mining units only", pz)):
    r = pf.feols("treat ~ 1 | unit_id + year", data=q.assign(treat=q.treat.astype(float)))
    e = q.treat.values - r.predict()
    wts = e[q.treat.values == 1] / (e[q.treat.values == 1]).sum()
    tr = q[q.treat == 1].assign(w=wts)
    print(f"  {lab}: {len(wts)} treated cells, {int((wts < 0).sum())} negative weights (sum {wts[wts < 0].sum():+.3f})")
    print("    weight by first-treat cohort:", tr.groupby("first_treat").w.sum().round(3).to_dict(),
          "| negative cells:", tr[tr.w < 0][["unit_id", "year"]].assign(unit=lambda s: s.unit_id.map(names)).drop(columns="unit_id").values.tolist())

print("\n" + "=" * 100, "\nT5 treatment dating variants (TWFE / did2s; all units | mining units only)")
MUN, SAI, KAY = "BR-TI-29801", "BR-TI-40901", "BR-TI-23001"
RANCH = ["BR-TI-3002", "BR-TI-46201"]          # Apyterewa, Trincheira Bacaja: desintrusao of mainly cattle invaders
V = {
    "coded (package rule)": (BASE.to_dict(), (), "halfyear"),
    "calendar-year mapping (as brazil_stagger)": (BASE.to_dict(), (), "calendar"),
    "Kayapo 2023-06 (verified PF action, own rule)": ({**BASE.to_dict(), KAY: "2023-06"}, (), "halfyear"),
    "Kayapo 2017-10 (raid)": ({**BASE.to_dict(), KAY: "2017-10"}, (), "halfyear"),
    "Munduruku+Sai-Cinza 2021-05": ({**BASE.to_dict(), MUN: "2021-05", SAI: "2021-05"}, (), "halfyear"),
    "Munduruku 2021-05 + Kayapo 2023-06": ({**BASE.to_dict(), MUN: "2021-05", SAI: "2021-05", KAY: "2023-06"}, (), "halfyear"),
    "drop ranch desintrusoes": (BASE.to_dict(), RANCH, "halfyear"),
    "drop 1-post-year treated": (BASE.to_dict(), [u for u in BASE.index if ftyear(BASE[u]) == 2025], "halfyear"),
    "Yanomami only treated (others dropped)": ({u: v for u, v in BASE.items() if u == "BR-TI-50901"},
                                              [u for u in BASE.index if u != "BR-TI-50901"], "halfyear"),
    "drop Munduruku+Sai-Cinza (doubtful date)": (BASE.to_dict(), [MUN, SAI], "halfyear"),
    "PROPOSED R*: Kayapo 2023-06, ranch dropped": ({**BASE.to_dict(), KAY: "2023-06"}, RANCH, "halfyear"),
}
rows = []
for k, (dts, drop, rule) in V.items():
    a, b = panel(dts, drop, rule), panel(dts, list(drop) + ZERO, rule)
    rows.append(dict(variant=k, n_tr=a[a.first_treat > 0].unit_id.nunique(), twfe_all=twfe(a)[0], p_all=twfe(a)[1],
                     did2s_all=did2s(a)[0], p2_all=did2s(a)[1], n_tr_min=b[b.first_treat > 0].unit_id.nunique(),
                     twfe_min=twfe(b)[0], p_min=twfe(b)[1], did2s_min=did2s(b)[0], p2_min=did2s(b)[1]))
T5 = pd.DataFrame(rows).round(3); print(T5.to_string(index=False))
vals = T5[["twfe_all", "did2s_all", "twfe_min", "did2s_min"]].values.ravel()
print(f"  range across variants and samples: {vals.min():+.2f} to {vals.max():+.2f}; positive in {int((vals > 0).sum())} of {vals.size}")

PRE18 = sorted(P0[P0.year <= 2018].groupby("unit_id").mining_ha.max().loc[lambda s: s == 0].index)
print(f"  sample chosen on PRE-period MapBiomas (mining > 0 in some year 2014-18): drops {len(PRE18)} units:", [names[u] for u in PRE18 if u not in ZERO])
for k in ("coded (package rule)", "PROPOSED R*: Kayapo 2023-06, ranch dropped"):
    dts, drop, rule = V[k]; q = panel(dts, list(drop) + PRE18, rule)
    print(f"   {k}: units {q.unit_id.nunique()}, treated {q[q.first_treat>0].unit_id.nunique()}: TWFE {twfe(q)[0]:+.3f} (p {twfe(q)[1]:.3f}); did2s {did2s(q)[0]:+.3f} (p {did2s(q)[1]:.3f})")
    a = cs_att(q); post = a[a.e >= 0]
    print(f"     Callaway-Sant'Anna overall post ATT {np.average(post.att, weights=post.n):+.3f}; leads e=-5..-2:", a[a.e.between(-5, -2)].groupby('e').apply(lambda s: np.average(s.att, weights=s.n)).round(2).to_dict())

print("\n" + "=" * 100, "\nT6 randomization inference variants (one-sided, share of fakes <= real; 2,000 draws, seed 0)")


def ri(q, stat, pool_units, reps=2000, seed=0):
    rng = np.random.default_rng(seed); fts = q.groupby("unit_id").first_treat.first()
    real = stat(q); dates = fts[fts > 0].values; sims = []
    for _ in range(reps):
        fake = pd.Series(0, index=fts.index)
        fake[rng.choice(pool_units, size=len(dates), replace=False)] = rng.permutation(dates)
        f = q.unit_id.map(fake)
        sims.append(stat(q.assign(first_treat=f, treat=((f > 0) & (q.year >= f)).astype(int))))
    sims = np.array(sims)
    return real, (sims <= real).mean(), np.percentile(sims, [5, 50, 95])


tw_pt = lambda q: pf.feols("ln_new ~ treat | unit_id + year", data=q).coef()["treat"]
for lab, q in (("all 24, TWFE (as coded)", pb), ("all 24, did2s", pb), ("mining 12, TWFE", pz), ("mining 12, did2s", pz)):
    st = tw_pt if "TWFE" in lab else did2s_point
    r, pv, qs = ri(q, st, q.unit_id.unique())
    print(f"  {lab:28s} real {r:+.3f}  p {pv:.3f}  fakes 5/50/95% {np.round(qs, 2)}")
# timing-only RI: keep the treated set, shuffle dates among them (exchangeable timing, Athey-Imbens style)
rng = np.random.default_rng(0); fts = pz.groupby("unit_id").first_treat.first(); tr = fts[fts > 0]
sims = []
for _ in range(2000):
    fake = fts.copy(); fake[tr.index] = rng.permutation(tr.values); f = pz.unit_id.map(fake)
    sims.append(did2s_point(pz.assign(first_treat=f, treat=((f > 0) & (pz.year >= f)).astype(int))))
print(f"  mining 12, did2s, timing-only shuffle (treated set fixed, first treated years {sorted(map(int, tr.values))} permuted): p {(np.array(sims) <= did2s_point(pz)).mean():.3f}")

print("\n" + "=" * 100, "\nT7 never-treated pools")
ops = pd.read_csv(I / "operations_coded.csv").set_index("unit_id")
nev = sorted(set(P0.unit_id) - set(BASE.index))
st = ops.verdict_2017_2025.reindex(nev).fillna("NOT SEARCHED")
print("  A14 never-treated (13):", {names[u]: s for u, s in st.items()})
print("  of which with zero MapBiomas mining in every year:", sum(u in ZERO for u in nev))
units = pd.read_csv(I / "amw_candidates_units.csv").set_index("unit_id")
wamw = amw.pivot(index="year", columns="unit_id", values="new_ha")
grp = {"BR-TI-50901", MUN, SAI, KAY, "BR-TI-42101"}
dated = {c for c in _fo.index if c.startswith("BR-TI-") and _fo[c] >= "2022"}   # as brazil_stagger.load (all coded TIs)
pool = sorted(c for c in wamw if c.startswith("BR-TI-") and c not in grp and c not in dated)
pst = ops.verdict_2017_2025.reindex(pool).fillna("NOT SEARCHED")
print(f"  A13 pool ({len(pool)}): searched none {int((pst=='none').sum())}, unclear {int((pst=='unclear').sum())}, "
      f"op before 2022 {int((pst=='yes').sum())}, not searched {int((pst=='NOT SEARCHED').sum())}")
print("   pool units with an earlier operation:", {units.name[c]: ops.first_op_2017_2025.get(c) for c in pool if pst[c] == 'yes'})
top = wamw[pool].loc[2023:2025].sum().sort_values(ascending=False)
print(f"  pool 2023-25 AMW new area {top.sum():,.0f} ha; largest {units.name[top.index[0]]} {top.iloc[0]:,.0f} ha = {top.iloc[0]/top.sum():.3f} (numbers.csv {NUM['bs_pool_top_share_2023_25']:.3f})")
print("   Aripuana by year:", wamw["BR-TI-4201"].loc[2019:2025].round(0).to_dict(), "| MapBiomas Col 11 max", P0[P0.unit_id == "BR-TI-4201"].mining_ha.max())
hav = lambda a, b: 6371 * 2 * np.arcsin(np.sqrt(np.sin(np.radians(b.lat - a.lat) / 2) ** 2 + np.cos(np.radians(a.lat)) * np.cos(np.radians(b.lat)) * np.sin(np.radians(b.lon - a.lon) / 2) ** 2))
for t in ("BR-TI-33601", "BR-TI-40701"):
    print(f"   centroid distance Aripuana - {units.name[t]} (Golden Border, Mar 2025): {hav(units.loc['BR-TI-4201'], units.loc[t]):.0f} km")
pool_ex = wamw[[c for c in pool if c != "BR-TI-4201"]].sum(axis=1)
print("   pool without Aripuana, AMW new ha by year:", pool_ex.loc[2019:2025].round(0).to_dict())
pool_in = wamw[pool].sum(axis=1)
print("   pool with Aripuana:", pool_in.loc[2019:2025].round(0).to_dict())
for g_, y_ in (("Yanomami", 2023), ("Kayapo/Sarare", 2024)):
    ch = lambda s: 100 * (s.loc[y_:2025].mean() / s.loc[y_ - 3:y_ - 1].mean() - 1)
    print(f"   pool change for the {g_} window ({y_-3}-{y_-1} -> {y_}-2025): with Aripuana {ch(pool_in):+.0f}%, without {ch(pool_ex):+.0f}%, without Aripuana and 2025 (to 2024) "
          f"{100 * (pool_ex.loc[y_:2024].mean() / pool_ex.loc[y_ - 3:y_ - 1].mean() - 1):+.0f}%")
gs = {"Yanomami": ["BR-TI-50901"], "Munduruku + Sai-Cinza": [MUN, SAI], "Kayapo": [KAY], "Sarare": ["BR-TI-42101"]}
for g_, us in gs.items():
    y_ = 2023 if g_ in ("Yanomami", "Munduruku + Sai-Cinza") else 2024
    tser = wamw[us].sum(axis=1); lt = np.log(tser.loc[y_:2025].mean() / tser.loc[y_ - 3:y_ - 1].mean())
    print(f"   A13 gap {g_}: with Aripuana in pool {lt - np.log(pool_in.loc[y_:2025].mean() / pool_in.loc[y_ - 3:y_ - 1].mean()):+.2f}, "
          f"without {lt - np.log(pool_ex.loc[y_:2025].mean() / pool_ex.loc[y_ - 3:y_ - 1].mean()):+.2f} log points")

print("\n" + "=" * 100, "\nT8 products: same territories, six measurements")
deter = pd.read_csv(I / "deter_ti_month.csv"); deter["year"] = deter.ym.str[:4].astype(int)
dy = deter.groupby(["terrai_codigo", "year"]).km2.sum()
c11 = raw.set_index(["unit_id", "year"])
for u in ("BR-TI-50901", MUN, KAY, "BR-TI-42101"):
    c = codes[u]; rws = {}
    for y in (2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025):
        rws[y] = dict(c101_stock=w101[c].get(y, np.nan), c11_stock=c11.loc[(u, y), "mining_ha"],
                      c101_net=w101[c].get(y, np.nan) - w101[c].get(y - 1, np.nan),
                      c11_net=c11.loc[(u, y), "mining_ha"] - c11.loc[(u, y - 1), "mining_ha"],
                      c11_first=c11.loc[(u, y), "new_land_ha"], amw_new=wamw[u].get(y, np.nan),
                      deter_ha=100 * dy.get((c, y), 0.0))
    print(f"  {names[u]} (ha):\n", pd.DataFrame(rws).round(0).to_string())
print("  Col 10.1 vs Col 11 stock, all territories in both (ratio Col 11 / Col 10.1):")
rr = []
for u in P0.unit_id.unique():
    c = codes[u]
    if c in w101.columns and w101[c].loc[2024] > 0:
        rr.append(dict(unit=names[u], **{f"r{y}": c11.loc[(u, y), "mining_ha"] / w101[c].loc[y] if w101[c].loc[y] > 0 else np.nan for y in (2018, 2022, 2024)},
                       c101_2024=w101[c].loc[2024], c11_2024=c11.loc[(u, 2024), "mining_ha"]))
print(pd.DataFrame(rr).round(2).to_string(index=False))

print("\n" + "=" * 100, "\nT9 IBAMA autos (committed intermediate; raw zip absent)")
ib = pd.read_csv(I / "ibama_autos_annual.csv").set_index("year")
for col in ("n_legal_amazon_states", "n_mining_legal_amazon", "n_mining_and_indigenous_text_legal_amazon", "n_mining_RR"):
    print(f"  {col:45s} 2015-18 {ib.loc[2015:2018, col].mean():8.2f}  2019-22 {ib.loc[2019:2022, col].mean():8.2f}  2023-25 {ib.loc[2023:2025, col].mean():8.2f}")
print("  mining share of Legal Amazon autos:", (ib.n_mining_legal_amazon / ib.n_legal_amazon_states).round(3).loc[2015:2025].to_dict())
rx = re.compile(r"lavra"); rxb = re.compile(r"\blavra\b|permissao de lavra|lavra garimpeira")
ex = ["auto de infracao lavrado contra", "lavratura do auto", "executar lavra sem licenca", "permissao de lavra garimpeira"]
print("  regex illustration (no data): 'lavra' matches", [s for s in ex if rx.search(s)], "| with word boundary:", [s for s in ex if rxb.search(s)])

print("\n" + "=" * 100, "\nT10 A12 2x2 (Col 10.1 net additions), Yanomami vs Kayapo")
add = w101.diff()
Y, K = 50901, 23001
def d22(pre, post, c=K, scale=False):
    f = lambda s, a, b: s.loc[a:b].mean()
    dy_, dc = f(add[Y], *post) - f(add[Y], *pre), f(add[c], *post) - f(add[c], *pre)
    if scale: dy_, dc = 100 * dy_ / w101[Y].loc[post[0] - 1], 100 * dc / w101[c].loc[post[0] - 1]
    return dy_ - dc
print(f"  main 2020-22 -> 2023-24: {d22((2020, 2022), (2023, 2024)):+.1f} ha/yr (numbers.csv {NUM['br_did_main_vs_Kayapo_ha_yr']:+.1f}); vs Munduruku {d22((2020, 2022), (2023, 2024), c=29801):+.1f}")
print(f"  code placebo 2017-19 -> 2020-22: {d22((2017, 2019), (2020, 2022)):+.1f} ha/yr (numbers.csv {NUM['br_did_placebo_time_start_2020_ha_yr']:+.1f}); code scales every spec by the 2022 stock")
for pre in [(2020, 2022), (2019, 2022), (2021, 2022), (2016, 2022), (2022, 2022)]:
    print(f"  pre {pre} -> 2023-24: ha {d22(pre, (2023, 2024)):+8.1f}   pp of stock(post-1) {d22(pre, (2023, 2024), scale=True):+6.2f}")
print("  fake start years s (pre s-3..s-1, post s..s+1), ha | pp of stock in s-1:")
fk = {s: (d22((s - 3, s - 1), (s, s + 1)), d22((s - 3, s - 1), (s, s + 1), scale=True)) for s in range(2005, 2022)}
print("   ", {s: (round(a), round(b, 1)) for s, (a, b) in fk.items()})
clean = [v[0] for s, v in fk.items() if s + 1 <= 2022]
real = d22((2020, 2022), (2023, 2024))
print(f"  real {real:+.0f}: share of clean fakes (post ends <= 2022) <= real: {np.mean(np.array(clean) <= real):.2f}; rank by ha (most negative = 1): {1 + sum(c < real for c in clean)} of {len(clean) + 1}")

print("\n" + "=" * 100, "\nT11 what 'Munduruku' means in each module")
print("  brazil.py: geocode 29801 only (Col 10.1) | brazil_stagger.py: 29801 + 40901 Sai-Cinza (AMW) |")
print("  brazil_deter.py: Munduruku + Sai-Cinza + Munduruku-Taquara (DETER) | brazil_v2.py: 29801 and 40901 as two treated units")
print("  control_top3/control_select: RAISG/AMW polygon 'Munduruku territory', dropped for the May 2021 operation")
