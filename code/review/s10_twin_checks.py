"""Review session S10 (docs/methods/10_rule_based_twins.md): read-only checks of Ruby's rule-based twin design.

Run from the repo root:  uv run python code/review/s10_twin_checks.py   (writes nothing)
Reads data_intermediate/amw_candidates_*.csv, operations_coded.csv, mb_amazonia_col6_mining.csv, data/, output/.
T1  reproduce the funnel (1,174 / 31 / 2 / 0; relaxed 2) and the pace numbers (7.90 vs 20.91 / 18.37; ratio 0.40)
T2  the R1 table: every area with >= 500 ha, its verdict, first operation, and which rule it fails
T3  R2b string comparison: formats of first_op; does ">= '2022'" do what it should?
T4  coding check: Sawre Muybu, Menkragnoti, Enawene-Nawe recoded "unclear" -> funnel unchanged?
T5  selection on outcomes (R2b): 2019-21 pace of R1 areas by operation timing
T6  pre-trends: reproduce the P1 tests; linear-trend extrapolation of the growth gap to 2019-21
T7  cross-product scale: AMW 2018 stock / MapBiomas 2018 stock for Tambopata and the twins
T8  Col 4 vs Col 6 on the same land: Tambopata National Reserve in both collections
T9  sensitivity of the twin choice to the cut-offs (MIN_STOCK, MAX_ELEV, MIN_SCALE)
T10 non-Brazil and same-country pools under the relaxed rules
T11 Brazil context: did the twins speed up in 2019-21 (own MapBiomas growth); IBAMA autos
T13 Tambopata's rank among all 31 areas with >= 500 ha; pace vs size
T12 AMW year-by-year pace and the "2019 shows nothing" check
"""
import sys
import warnings
import numpy as np
import pandas as pd
import statsmodels.api as sm

sys.path.insert(0, "code")
warnings.filterwarnings("ignore")
import control_select as cs  # noqa: E402  (functions only; run() is not called, nothing is written)

pd.set_option("display.width", 220); pd.set_option("display.max_columns", 30); pd.set_option("display.max_colwidth", 60)
TU = cs.TU
u, w, e, ops = cs.load()
t = cs.funnel(u, w, e, ops)
num = pd.read_csv("output/numbers.csv").set_index("id").value
TWINS = {"RAISG-434": 4443, "RAISG-512": 4442}          # Amana, Tapajos: AMW unit id -> Col 6 geocode

def pace(ids, yrs):
    return w.loc[ids, yrs].sum() / w.loc[ids, 2018].sum() * 100

# ------------------------------------------------------------------ T1
print("T1 reproduce the funnel")
r1 = t.r1_mining; r2 = r1 & t.r2_no_op; r3 = r2 & t.r3_outside_mdd
print(f"  areas {len(u)}; R1 {r1.sum()}; R1+R2 {r2.sum()}; +R3 {r3.sum()}; strict {t.pass_strict.sum()}; relaxed {t.pass_relaxed.sum()}")
print("  relaxed survivors:", t[t.pass_relaxed].name.tolist())
tam = pace([TU], range(2019, 2022)).mean()
tw = {k: pace([k], range(2019, 2022)).mean() for k in TWINS}
pooled = np.mean(list(tw.values()))
print(f"  Tambopata 2019-21 pace {tam:.2f}% | twins {[round(v, 2) for v in tw.values()]} | pooled mean {pooled:.2f} | ratio {tam/pooled:.3f}"
      f" (numbers.csv top3_ratio {num['top3_ratio']:.3f}; ctl_relaxed_during_ratio {num['ctl_relaxed_during_ratio']:.3f})")
pooled_stock = pace(list(TWINS), range(2019, 2022)).mean()
print(f"  stock-weighted pooled twin pace {pooled_stock:.2f} -> ratio {tam/pooled_stock:.3f}")

# ------------------------------------------------------------------ T2
print("\nT2 the R1 table (stock >= 500 ha), sorted by fit distance")
def fails(r):
    f = []
    if not r.r2_no_op: f.append("R2" + ("(b ok)" if r.r2b_no_op_2017_21 else ""))
    if not r.r3_outside_mdd: f.append("R3")
    if not r.r4_lowland: f.append("R4:" + ("elev" if r.elev_median_m >= cs.MAX_ELEV else "") + ("size" if r.stock_2018 < cs.MIN_SCALE * w.loc[TU, 2018] else ""))
    return " ".join(f) or "-"
R1 = t[r1].copy(); R1["fails"] = R1.apply(fails, axis=1)
print(R1[["name", "country", "stock_2018", "elev_median_m", "verdict", "first_op", "fails"]].round(0).to_string())
print("  verdicts among R1:", R1.verdict.value_counts().to_dict())
print(f"  R4 size cut-off = {cs.MIN_SCALE} x {w.loc[TU, 2018]:.0f} = {cs.MIN_SCALE * w.loc[TU, 2018]:.0f} ha")

# ------------------------------------------------------------------ T3
print("\nT3 R2b string compare: first_op formats")
fo = ops.first_op_2017_2025.dropna().astype(str)
print("  lengths:", fo.str.len().value_counts().to_dict(), "| all match YYYY-MM:", bool(fo.str.fullmatch(r"\d{4}-\d{2}").all()))
print("  verdict 'yes' with empty first_op:", int((ops.verdict_2017_2025.eq("yes") & ops.first_op_2017_2025.isna()).sum()))
print("  -> with YYYY-MM strings, '>= \"2022\"' is a correct year test; it would break on '2021/12' or '' (empty < '2022').")

# ------------------------------------------------------------------ T4
print("\nT4 recode the three 'searched 2022-25 only' territories as unclear")
three = ["BR-TI-56701", "BR-TI-28701", "BR-TI-11201"]
print(ops.loc[three, ["area", "verdict_2017_2025", "ops_text"]].to_string())
print(t.reindex(three)[["name", "stock_2018", "elev_median_m", "r1_mining", "r3_outside_mdd", "r4_lowland"]].to_string())
ops2 = ops.copy(); ops2.loc[three, "verdict_2017_2025"] = "unclear"
t2 = cs.funnel(u, w, e, ops2)
print(f"  recoded funnel: R1 {t2.r1_mining.sum()}; R1+R2 {(t2.r1_mining & t2.r2_no_op).sum()}; strict {t2.pass_strict.sum()}; relaxed {t2.pass_relaxed.sum()}")
print("  R1+R2 areas before recode:", t[r2].name.tolist())
amw_s = w.loc[[k for k in three if k in w.index], 2018]
print("  AMW 2018 stock of the three:", amw_s.round(1).to_dict())

# ------------------------------------------------------------------ T5
print("\nT5 selection on outcomes: AMW 2019-21 pace of areas with >= 500 ha (R1) and >= 100 ha, by operation timing")
for floor in (500, 100):
    a = t[(t.stock_2018 >= floor)].copy()
    a["pace_1921"] = (w.loc[a.index, [2019, 2020, 2021]].mean(axis=1) / a.stock_2018 * 100)
    a["pace_2223"] = (w.loc[a.index, [2022, 2023]].mean(axis=1) / a.stock_2018 * 100)
    grp = np.select([a.verdict.eq("yes") & (a.first_op < "2022"), a.verdict.eq("yes") & (a.first_op >= "2022"),
                     a.verdict.eq("none"), a.verdict.isin(["unclear", "not searched"])],
                    ["op 2017-21", "first op 2022+", "none found", "unclear/not searched"], "other")
    g = a.groupby(grp).agg(n=("name", "size"), median_pace_1921=("pace_1921", "median"), mean_pace_1921=("pace_1921", "mean"),
                           median_pace_2223=("pace_2223", "median"))
    print(f"  stock >= {floor} ha:\n" + g.round(1).to_string())
    late = a[a.verdict.eq("yes") & (a.first_op >= "2022")]
    print(f"  first-op-2022+ areas: {late.name.str[:28].tolist()} paces {late.pace_1921.round(1).tolist()}")

# ------------------------------------------------------------------ T6
print("\nT6 pre-trends (MapBiomas Col 4 Tambopata BZ vs Col 6 twins), 2010-18, and extrapolation to 2019-21")
m6 = pd.read_csv("data_intermediate/mb_amazonia_col6_mining.csv")
bz = pd.read_csv("data/peru_bufferzone_year.csv")
tamb = bz[(bz.buffer_zone == "Tambopata") & (bz.pa_category == "Reserva Nacional")].groupby("year").mining_ha.sum()
series = {"Tambopata BZ (Col 4)": tamb}
for k, gc in TWINS.items():
    series[u.loc[k, "name"][:24]] = m6[m6.geocode == gc].groupby("year").mining_ha.sum()
S = pd.DataFrame(series).loc[2008:2023]
print("  mining area (ha), MapBiomas, own collection:\n" + S.loc[2009:2023].round(0).T.to_string())
G = np.log(S).diff()
for nm in list(series)[1:]:
    dg = (G.iloc[:, 0] - G[nm])
    pre = dg.loc[2010:2018]
    r1_ = sm.OLS(pre, np.ones(len(pre))).fit(cov_type="HAC", cov_kwds={"maxlags": 1})
    x = np.arange(len(pre)); r2_ = sm.OLS(pre.values, sm.add_constant(x)).fit(cov_type="HAC", cov_kwds={"maxlags": 1})
    xf = np.arange(len(pre), len(pre) + 3)
    pred = r2_.params[0] + r2_.params[1] * xf
    act = dg.loc[2019:2021].values
    print(f"  {nm}: mean gap {r1_.params.iloc[0]:+.3f} (p {r1_.pvalues.iloc[0]:.3f}); slope {r2_.params[1]:+.3f}/yr (p {r2_.pvalues[1]:.1e})")
    print(f"     yearly gap 2010-18: {pre.round(2).tolist()}")
    print(f"     trend-predicted gap 2019-21 {np.round(pred, 2).tolist()} vs actual {np.round(act, 2).tolist()} -> actual minus predicted {np.round(act - pred, 2).tolist()}")
    for lo in (2012, 2013, 2014):
        pw = dg.loc[lo:2018]
        a_ = sm.OLS(pw, np.ones(len(pw))).fit(cov_type="HAC", cov_kwds={"maxlags": 1})
        b_ = sm.OLS(pw.values, sm.add_constant(np.arange(len(pw)))).fit(cov_type="HAC", cov_kwds={"maxlags": 1})
        pr = b_.params[0] + b_.params[1] * np.arange(len(pw), len(pw) + 3)
        print(f"     window {lo}-18: mean gap {a_.params.iloc[0]:+.3f} (p {a_.pvalues.iloc[0]:.2f}); slope {b_.params[1]:+.3f} (p {b_.pvalues[1]:.2f}); "
              f"trend-predicted 2019-21 mean {pr.mean():+.2f} vs actual {act.mean():+.2f}")
    pre14 = dg.loc[2014:2018]
    print(f"     mean gap 2014-18 only {pre14.mean():+.3f}; mean gap 2016-18 {dg.loc[2016:2018].mean():+.3f}; 2019-21 mean {act.mean():+.3f}")
    # same test on levels (index) instead of growth: drop the early years when the twin stock was tiny
    print(f"     twin stock 2010 {S.loc[2010, nm]:.0f} ha vs 2018 {S.loc[2018, nm]:.0f} ha (early log growth from a small base)")

# ------------------------------------------------------------------ T7
print("\nT7 cross-product scale: AMW 2018 stock / MapBiomas 2018 stock")
rows = [("Tambopata BZ", w.loc[TU, 2018], tamb.loc[2018], "Peru Col 4")]
for k, gc in TWINS.items():
    rows.append((u.loc[k, "name"][:24], w.loc[k, 2018], S.loc[2018, u.loc[k, "name"][:24]], "Amazonia Col 6"))
# Tambopata BZ is not a Col 6 unit; the reserve interior is (geocode 47011): see T8
for nm, a_, m_, c in rows:
    print(f"  {nm:26s} AMW {a_:8.0f} | MapBiomas ({c}) {m_:8.0f} | ratio {a_/m_:.2f}")
print(f"  R4 on MapBiomas instead of AMW: twin/Tambopata stock = "
      + ", ".join(f"{nm} {m_/tamb.loc[2018]:.2f}" for nm, _, m_, _c in rows[1:]) + f" (cut-off {cs.MIN_SCALE})")
print(f"  R4 on AMW: " + ", ".join(f"{nm} {a_/w.loc[TU, 2018]:.2f}" for nm, a_, _, _c in rows[1:]))

# ------------------------------------------------------------------ T8
print("\nT8 same land, two collections: Tambopata National Reserve, Peru Col 4 vs Amazonia Col 6")
c4 = pd.read_csv("output/peru_anp_mining_levels_2010_2025.csv").set_index("year")["Tambopata NR"]
c6 = m6[m6.geocode == 47011].groupby("year").mining_ha.sum()
both = pd.DataFrame({"Col 4": c4, "Col 6": c6}).loc[2010:2023]
both["log growth diff (4 - 6)"] = np.log(both["Col 4"]).diff() - np.log(both["Col 6"]).diff()
print(both.round(2).T.to_string())
d = both["log growth diff (4 - 6)"].loc[2011:2018]
print(f"  mean 'growth gap' between two collections on the SAME land, 2011-18: {d.mean():+.3f} log points/yr (sd {d.std():.3f})")

# ------------------------------------------------------------------ T9
print("\nT9 sensitivity of the relaxed twin set to the cut-offs")
orig = (cs.MIN_STOCK, cs.MAX_ELEV, cs.MIN_SCALE)
for ms, me, sc in [(500, 500, 0.2), (250, 500, 0.2), (1000, 500, 0.2), (500, 300, 0.2), (500, 700, 0.2), (500, 1000, 0.2),
                   (500, 500, 0.1), (500, 500, 0.05), (500, 500, 0.33), (500, 500, 0.5)]:
    cs.MIN_STOCK, cs.MAX_ELEV, cs.MIN_SCALE = ms, me, sc
    tt = cs.funnel(u, w, e, ops)
    rel = tt[tt.pass_relaxed]
    ratio = tam / pace(rel.index.tolist(), range(2019, 2022)).mean() if len(rel) else np.nan
    mean_ratio = tam / np.mean([pace([i], range(2019, 2022)).mean() for i in rel.index]) if len(rel) else np.nan
    print(f"  stock>={ms:4d} elev<{me:4d} scale>={sc:.2f}: strict {int(tt.pass_strict.sum())} relaxed {len(rel)} "
          f"{[n[:18] for n in rel.name]} ratio (mean of paces) {mean_ratio:.2f}")
cs.MIN_STOCK, cs.MAX_ELEV, cs.MIN_SCALE = orig

# ------------------------------------------------------------------ T10
print("\nT10 pools outside Brazil")
nb = t[~t.country.eq("Brazil") & t.r3_outside_mdd & (t.stock_2018 >= 100)]
print(nb[["name", "country", "stock_2018", "elev_median_m", "verdict", "first_op"]].round(0).to_string())
peru = t[t.country.eq("Peru") & (t.stock_2018 >= 100)]
print("  Peru areas with >= 100 ha AMW 2018 (any status):")
print(peru[["name", "stock_2018", "elev_median_m", "verdict", "first_op", "r3_outside_mdd"]].round(0).to_string())

# ------------------------------------------------------------------ T11
print("\nT11 Brazil context: did the twins speed up in 2019-21? Own log growth per year, MapBiomas (own collection)")
for nm in S.columns:
    g = lambda a, b: np.log(S.loc[b, nm] / S.loc[a, nm]) / (b - a)
    print(f"  {nm:26s} 2013-15 {g(2012, 2015):+.3f} | 2016-18 {g(2015, 2018):+.3f} | 2019-21 {g(2018, 2021):+.3f} | 2021-23 {g(2021, 2023):+.3f}")
print("  IBAMA autos, Legal Amazon (numbers.csv):",
      {k: round(num[k], 1) for k in ["br_ibama_aml_mean_2015_2018", "br_ibama_aml_mean_2019_2022", "br_ibama_mining_aml_mean_2015_2018",
                                    "br_ibama_mining_aml_mean_2019_2022"]})

# ------------------------------------------------------------------ T13
print("\nT13 where does Tambopata sit among ALL areas with >= 500 ha (any operation status)? AMW pace 2019-21")
a = t[t.r1_mining].copy()
a["pace"] = w.loc[a.index, [2019, 2020, 2021]].mean(axis=1) / a.stock_2018 * 100
tp = w.loc[TU, [2019, 2020, 2021]].mean() / w.loc[TU, 2018] * 100
print(f"  Tambopata {tp:.1f}%; others: min {a.pace.min():.1f}, q25 {a.pace.quantile(.25):.1f}, median {a.pace.median():.1f}, "
      f"max {a.pace.max():.1f}; areas slower than Tambopata: {a[a.pace < tp].name.str[:30].tolist()}")
X = sm.add_constant(np.log(a.stock_2018)); fit = sm.OLS(np.log(a.pace), X).fit()
pred = np.exp(fit.params.iloc[0] + fit.params.iloc[1] * np.log(w.loc[TU, 2018]))
print(f"  log pace on log stock (31 areas): slope {fit.params.iloc[1]:+.2f} (p {fit.pvalues.iloc[1]:.2f}); predicted pace at Tambopata's stock {pred:.1f}% "
      f"-> Tambopata / predicted = {tp/pred:.2f}")
big = a[a.stock_2018 >= 4272]
print(f"  areas >= 4,272 ha (R4 size): paces {dict(zip(big.name.str[:20], big.pace.round(1)))}")

# ------------------------------------------------------------------ T12
print("\nT12 AMW yearly pace, % of own 2018 stock")
yrs = list(range(2019, 2026))
P = pd.DataFrame({u.loc[k, "name"][:22]: pace([k], yrs) for k in [TU, *TWINS, cs.AMARAKAERI]})
print(P.round(1).T.to_string())
