"""Review session S11 (docs/methods/11_matching.md): read-only checks of the seven matching estimators (control_psm.py).

Run from the repo root:  uv run python code/review/s11_matching_checks.py   (writes nothing)
Reads data_intermediate/amw_candidates_*.csv, operations_coded.csv and output/numbers.csv via control_psm's own loaders.
T1  reproduce: pool size and composition, logit sample, every gap / ratio / rank / p in numbers.csv
T2  common support: propensity scores of Tambopata and the pool; the caliper the code computes but never passes
T3  balance: SMD of every covariate, before and after each estimator; entropy-balancing residual imbalance
T4  log-ratio placebo statistic (scale-free) instead of the percentage-point gap
T5  placebo exchangeability: are placebo gaps driven by small stocks?
T6  pool variants: without Brazil; MIN_STOCK 500 (as the funnel); three territories recoded "unclear"; unknown_none
T7  influence: drop each pool area in turn (which area moves ebal / IPW most?); the 2022-25 after-gaps
T8  what the logit "treatment" is: list of the 14 treated areas; coefficients
T9  refit the logit without the Mercurio landscape (4 Peruvian units): does Tambopata enter common support?
"""
import sys
import warnings
import numpy as np
import pandas as pd

sys.path.insert(0, "code")
warnings.filterwarnings("ignore")
import control_psm as cp  # noqa: E402  (functions only; run() is not called, nothing is written)

pd.set_option("display.width", 220); pd.set_option("display.max_columns", 30)
TU = cp.TU
num = pd.read_csv("output/numbers.csv").set_index("id").value
t = cp.load()
score, info = cp.propensity(t)
bins = cp.cem_bins(t)
P = cp.pool(t)
M = list(cp.METHODS)
ps = 1 / (1 + np.exp(-score))

def run_all(t, P, score, bins, stat="gap", methods=M):
    out = {}
    for m in methods:
        r = cp.estimate(m, t, TU, P, score, bins)
        if r is None:
            out[m] = dict(gap=np.nan); continue
        if stat == "gap":
            real = r["gap_during"]; col = "gap_during"
            rank, n, g = cp.placebo(m, t, P, score, bins, real, col)
        else:  # log ratio of paces: log(treated pace / controls' pace)
            real = np.log(t.loc[TU, "pace_during"] / r["ctl_during"])
            g = []
            for j in P:
                rj = cp.estimate(m, t, j, P.drop(j), score, bins)
                if rj is not None and rj["ctl_during"] > 0 and t.loc[j, "pace_during"] > 0:
                    g.append(np.log(t.loc[j, "pace_during"] / rj["ctl_during"]))
            g = np.array(g); rank = cp.placebo_rank(real, g); n = len(g) + 1
        out[m] = dict(gap=real, ctl=r["ctl_during"], gap_after=r["gap_after"], rank=rank, n=n, p=rank / n,
                      top=", ".join(f"{t.loc[i, 'name'][:14]} {v:.0%}" for i, v in r["w"].sort_values(ascending=False).head(3).items()))
    return pd.DataFrame(out).T

# ------------------------------------------------------------------ T1
print("T1 reproduce")
print(f"  universe {len(t)}; pool {len(P)}; by country {t.loc[P, 'country'].value_counts().to_dict()}; Peru in pool {int(t.loc[P,'country'].eq('Peru').sum())}")
print(f"  logit n {info['n']}, treated {info['n_treated']}, pseudo-R2 {info['pseudo_r2']:.3f}; coef {dict((k, round(v, 2)) for k, v in info['coef'].items())}")
R = run_all(t, P, score, bins)
R["ratio"] = t.loc[TU, "pace_during"] / R.ctl.astype(float)
R["num_gap"] = [num.get(f"psm_{m}_gap_during") for m in R.index]
R["num_p"] = [num.get(f"psm_{m}_p") for m in R.index]
print(R[["gap", "num_gap", "ratio", "rank", "n", "p", "num_p", "gap_after", "top"]].to_string())
print("  pool areas:\n" + t.loc[P, ["name", "country", "stock_2018", "elev_median_m", "verdict", "pace_during", "pace_after"]]
      .assign(ps=ps.loc[P]).sort_values("ps", ascending=False).round(2).to_string())

# ------------------------------------------------------------------ T2
print("\nT2 common support")
cal = cp.CALIPER_SD * score.loc[P].std()
d = (score.loc[P] - score.loc[TU]).abs()
print(f"  Tambopata ps {ps.loc[TU]:.3f} (logit {score.loc[TU]:.2f}); pool max ps {ps.loc[P].max():.3f}; pool areas with ps >= Tambopata: {(score.loc[P] >= score.loc[TU]).sum()}")
print(f"  caliper 0.25 SD of logit = {cal:.3f}; nearest pool distance {d.min():.3f} ({d.min()/score.loc[P].std():.2f} SD) -> within caliper: {d.min() <= cal}")
for m in ("ps_nn1", "ps_nn5"):
    k = 1 if m == "ps_nn1" else 5
    print(f"  {m} with the caliper actually passed: {cp.w_nn(score, TU, P, k, caliper=cal)}")
for c in (0.5, 1.0):
    print(f"  caliper {c} SD: nn1 -> {cp.w_nn(score, TU, P, 1, caliper=c*score.loc[P].std())}")
ps_all_treated = ps[t.op_2017_21 & t.status_known]
print(f"  ps of areas with an operation 2017-21: median {ps_all_treated.median():.2f}, max {ps_all_treated.max():.2f}; Tambopata's rank among all {len(t)} areas: "
      f"{int((ps > ps.loc[TU]).sum()) + 1}")

# ------------------------------------------------------------------ T3
print("\nT3 balance (SMD = Tambopata minus weighted controls, in pool SD)")
bal = {"unweighted pool": cp.smd(t, P, pd.Series(1 / len(P), index=P))}
for m in M:
    w_ = cp.weights(m, t, TU, P, score, bins)
    if w_ is not None:
        bal[m] = cp.smd(t, P, w_)
B = pd.DataFrame(bal).T
print(B.round(2).to_string())
print(f"  max |SMD| per estimator: {B.abs().max(axis=1).round(2).to_dict()}")
print(f"  ebal residual imbalance (4 covs) {cp.w_ebal(t, TU, P)[1]:.3f}; with Brazil {cp.w_ebal(t, TU, P, cp.COVS)[1]:.3f}")
print(f"  Tambopata covariates: {t.loc[TU, cp.COVS].round(2).to_dict()}; pool ranges: "
      f"{ {c: (round(t.loc[P, c].min(), 2), round(t.loc[P, c].max(), 2)) for c in cp.COVS} }")

# ------------------------------------------------------------------ T4
print("\nT4 log-ratio placebo statistic: log(Tambopata pace / matched pace)")
L = run_all(t, P, score, bins, stat="logratio")
print(L[["gap", "rank", "n", "p"]].rename(columns={"gap": "log_ratio"}).to_string())

# ------------------------------------------------------------------ T5
print("\nT5 placebo exchangeability (ps_nn1, maha1, ipw): |placebo gap| vs own 2018 stock")
for m in ("ps_nn1", "maha1", "ipw"):
    rows = []
    for j in P:
        r = cp.estimate(m, t, j, P.drop(j), score, bins)
        if r is not None:
            rows.append((t.loc[j, "stock_2018"], r["gap_during"], t.loc[j, "name"][:18]))
    df = pd.DataFrame(rows, columns=["stock", "gap", "name"])
    rho = df[["stock", "gap"]].assign(stock=np.log(df.stock), gap=df.gap.abs()).corr(method="spearman").iloc[0, 1]
    ext = df.reindex(df.gap.abs().sort_values(ascending=False).index).head(4)
    print(f"  {m}: Spearman(log stock, |gap|) {rho:+.2f}; largest |gap|: {list(zip(ext.name, ext.gap.round(1), ext.stock.round(0)))}")

# ------------------------------------------------------------------ T6
print("\nT6 pool variants (gap pp / rank / n / p)")
three = ["BR-TI-56701", "BR-TI-28701", "BR-TI-11201"]
variants = {}
variants["main"] = P
variants["no Brazil"] = P[~t.loc[P, "brazil"].astype(bool)]
old = cp.MIN_STOCK; cp.MIN_STOCK = 500.0; variants["MIN_STOCK 500"] = cp.pool(t); cp.MIN_STOCK = old
variants["3 TIs recoded unclear"] = P.drop([i for i in three if i in P])
variants["unknown_none"] = cp.pool(t, unknown_as_none=True)
for k, VP in variants.items():
    print(f"  -- {k}: n = {len(VP)} {t.loc[VP, 'country'].value_counts().to_dict()}")
    meths = M if len(VP) > 5 else ["ps_nn1", "maha1", "cem", "ipw"]
    try:
        r = run_all(t, VP, score, bins, methods=meths)
        print(r[["gap", "rank", "n", "p", "top"]].to_string())
    except Exception as ex:
        print("    failed:", ex)
print(f"  in main pool? {[i for i in three if i in P]}")

# ------------------------------------------------------------------ T7
print("\nT7 influence: drop one pool area, effect on each estimator's 2019-21 gap and 2022-25 gap")
base = {m: cp.estimate(m, t, TU, P, score, bins) for m in M}
infl = []
for j in P:
    for m in M:
        r = cp.estimate(m, t, TU, P.drop(j), score, bins)
        if r is not None and base[m] is not None:
            infl.append((m, t.loc[j, "name"][:20], r["gap_during"] - base[m]["gap_during"], r["gap_after"] - base[m]["gap_after"]))
I = pd.DataFrame(infl, columns=["method", "dropped", "d_gap_during", "d_gap_after"])
for m in M:
    x = I[I.method == m]
    a = x.loc[x.d_gap_during.abs().idxmax()]; b = x.loc[x.d_gap_after.abs().idxmax()]
    print(f"  {m:7s} during: biggest move {a.d_gap_during:+.1f} pp (drop {a.dropped}) | after: {b.d_gap_after:+.1f} pp (drop {b.dropped}); "
          f"base after-gap {base[m]['gap_after']:+.1f}")
sar = t.index[t.name.str.startswith("Sarar")][0]
print(f"  Sarare: pace during {t.loc[sar, 'pace_during']:.1f}, after {t.loc[sar, 'pace_after']:.1f}; weight ebal "
      f"{cp.w_ebal(t, TU, P)[0].get(sar, 0):.2f}, ipw {cp.w_ipw(score, TU, P).get(sar, 0):.2f}")
for m in ("ebal", "ipw"):
    w_ = cp.weights(m, t, TU, P, score, bins); r = base[m]; r2 = cp.estimate(m, t, TU, P.drop(sar), score, bins)
    print(f"  {m}: controls' 2022-25 pace {r['ctl_after']:.1f}, of which Sarare {w_[sar] * t.loc[sar, 'pace_after']:.1f}; "
          f"after-gap {r['gap_after']:+.1f} -> without Sarare {r2['gap_after']:+.1f}")

# ------------------------------------------------------------------ T8
print("\nT8 the logit's 'treated' areas (operation reported 2017-21)")
s = t[t.status_known]
print(s[s.op_2017_21][["name", "country", "verdict"]].join(pd.read_csv("data_intermediate/operations_coded.csv").set_index("unit_id")["first_op_2017_2025"]).to_string())
print(f"  controls in the logit (status known, no op 2017-21): {int((~s.op_2017_21).sum())}")

# ------------------------------------------------------------------ T9
print("\nT9 refit the propensity logit without the Mercurio landscape (Tambopata BZ + NR, Amarakaeri BZ, Bahuaja-Sonene BZ)")
merc = ["PE-BZ-RN09", "PE-ANP-RN09", "PE-BZ-RC03", "PE-BZ-PN08"]
s9 = t[t.status_known & ~t.index.isin(merc)]
mu, sd = s9[cp.COVS].mean(), s9[cp.COVS].std().replace(0, 1)
b9, r2_9 = cp.logit_fit(((s9[cp.COVS] - mu) / sd).to_numpy(), s9.op_2017_21.astype(float).to_numpy())
z9 = pd.Series(np.column_stack([np.ones(len(t)), ((t[cp.COVS] - mu) / sd).to_numpy()]) @ b9, index=t.index)
p9 = 1 / (1 + np.exp(-z9))
print(f"  n {len(s9)}, treated {int(s9.op_2017_21.sum())}, pseudo-R2 {r2_9:.3f}; Tambopata ps {p9.loc[TU]:.3f}; pool max {p9.loc[P].max():.3f}; "
      f"pool areas >= Tambopata {(z9.loc[P] >= z9.loc[TU]).sum()}")
R9 = run_all(t, P, z9, bins, methods=["ps_nn1", "ps_nn5", "ipw"])
print(R9[["gap", "rank", "n", "p", "top"]].to_string())
