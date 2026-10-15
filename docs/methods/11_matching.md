# S11 · Matching estimators (attempt A11)

*Method card 11 of the causal review (plan: `docs/methods/causal_review_plan.md`). Code under review: `code/control_psm.py` (seven estimators: propensity-score nearest 1 and 5, Mahalanobis nearest 1 and 3, coarsened exact matching, entropy balancing, inverse-probability weighting). Inputs are shared with S10 (`amw_candidates_*.csv`, `operations_coded.csv`). Test script: `code/review/s11_matching_checks.py` (read-only).*

---

## 1. In one sentence

Build the comparison group by an algorithm instead of by hand: find untreated units whose pre-treatment traits match the treated unit's, then compare outcomes.

## 2. Simple version

S10 picked Tambopata's twin with four hand-written rules. Matching asks a computer to do the same: "Here are 20 places with no operation in 2017-21, described by five traits (mining stock, elevation, size, country, indigenous or not). Which ones look most like Tambopata?" There are several ways to define "look like":

- **Propensity score:** first predict each place's chance of getting an operation from its traits, then pick the places with the closest chance.
- **Mahalanobis distance:** measure closeness directly on the traits, accounting for how they vary together.
- **Coarsened exact matching (CEM):** put traits into bins (big / small, lowland / highland) and keep only places in Tambopata's bin.
- **Entropy balancing:** weight all places so that their weighted average traits equal Tambopata's.
- **Inverse-probability weighting (IPW):** weight places by how "treatment-like" they look.

Then compare Tambopata's 2019-21 pace of new mining with the matched places' pace.

The catch: matching shines when there are **many treated units**, because then the matched groups are balanced *on average*. With **one** treated unit, every method just picks a few neighbours. It is S10 again, with a formula instead of a rule.

## 3. When to use it, and when not

**Use it when:**
- many units are treated and many are not;
- treatment depends only on observed pre-treatment traits (unconfoundedness);
- treated and untreated units overlap on those traits (common support);
- you can check balance after matching.

**Be careful or avoid it when:**
- there is one treated unit: no averaging, so no balance "in expectation";
- the treated unit is extreme on the traits (outside the support of the controls);
- treatment was targeted on things you do not observe (here: the scale of illegality, political will, media attention);
- the outcome has no pre-period, so matching cannot be combined with differencing.

## 4. Assumptions

| Assumption | In words | Formally |
|---|---|---|
| **Unconfoundedness** (selection on observables) | Given the traits, whether a place got an operation is unrelated to what its mining would have been without one | Y_i(0) ⊥ D_i \| X_i |
| **Overlap** (common support) | For the treated unit's traits, untreated units with the same traits exist | 0 < P(D = 1 \| X = x_T) < 1, and controls observed near x_T |
| **SUTVA** | No spillover from treated to controls; one version of treatment | Y_j = Y_j(0) for controls |
| **Correct score model** (PS methods) | The logit captures how treatment depends on X | P(D = 1 \| X) = Λ(X'β) |
| **Balance** | After matching, the traits are similar | SMD ≈ 0 for every covariate |
| **Placebo exchangeability** (for inference) | Each control playing "treated" is a draw from the same distribution as the real treated unit | gaps of placebos and Tambopata comparable under the null |

## 5. The maths

### 5.1 Master's level

The target is the effect on the treated (ATT):

  τ_ATT = E[Y(1) − Y(0) | D = 1], estimated as Y_T − Σ_j w_j Y_j

Different estimators give different weights w_j over the control pool:

| Estimator | Weights | Reference |
|---|---|---|
| Propensity score, nearest k | 1/k on the k controls with the closest e(X) = P(D = 1 \| X), here on the logit scale | Rosenbaum and Rubin (1983) |
| Caliper | as above, but only controls within c SD of the logit score (often 0.2-0.25 SD) | Rosenbaum and Rubin (1985); Austin (2011) |
| Mahalanobis, nearest k | 1/k on the k smallest (X_j − X_T)' S⁻¹ (X_j − X_T) | Rubin (1980) |
| CEM | equal weight within Tambopata's coarsened stratum | Iacus, King and Porro (2012) |
| Entropy balancing | weights closest to uniform (in KL divergence) subject to Σ w_j X_j = X_T | Hainmueller (2012) |
| IPW for the ATT | w_j ∝ e(X_j) / (1 − e(X_j)) | Hirano, Imbens and Ridder (2003) |

**Balance diagnostic**: the standardised mean difference, SMD_k = (X_T,k − Σ w_j X_j,k) / sd_k. A common rule of thumb asks for |SMD| < 0.1 or 0.25 (Stuart 2010).

### 5.2 PhD level

**Why the propensity score works, and why it does not here.** Rosenbaum and Rubin (1983) show that if Y(0) ⊥ D | X, then Y(0) ⊥ D | e(X). Balancing *on average* follows because, among units with the same e(X), the distribution of X is the same for treated and controls. This is a property of **groups**. With one treated unit, conditioning on e(X_T) picks controls with the same predicted probability but possibly very different X (a big highland area and a small lowland one can have the same score). King and Nielsen (2019) show PS matching can even *increase* imbalance when matching is close to exhaustive. With n_T = 1, Mahalanobis or exact matching on X is the coherent choice.

**Overlap.** Without controls near x_T, any estimate is an extrapolation across the covariate space (Crump, Hotz, Imbens and Mitnik 2009). A caliper enforces overlap by refusing matches that are too far: if no control is within the caliper, the honest output is "no match". Nearest-neighbour matching without a caliper always returns a match, however bad.

**Estimating the score with the treated unit in the sample.** The logit here is fitted on 43 areas whose status is known, including Tambopata itself and three other Mercurio-landscape units. A unit's own outcome-free label then pulls the fitted score toward 1 for units like it. This in-sample fitting inflates Tambopata's score and widens the overlap gap. Abadie and Imbens (2016) analyse the variance consequences of an estimated score; with 43 points and 5 covariates, the fit itself is very noisy.

**IPW with a near-extreme score.** ATT weights e/(1 − e) explode when control scores approach 1. Here the pool's scores are all below Tambopata's, so weights are bounded. But a single control with a very unusual outcome can dominate the weighted mean (T7).

**Post-only outcomes.** Matching on X and comparing post-period levels identifies the ATT only under unconfoundedness in *levels*. With a pre-period, a matched difference in differences (match on X, then difference out each unit's own pre-period) relaxes this to unconfoundedness in *changes*. AMW starts in 2018, so that option is unavailable, and the pace measure (new / 2018 stock) is the only normalisation.

**Inference with one treated unit.** The code uses placebo in space: each pool area in turn plays "treated", the same estimator picks its matches from the rest, and Tambopata's rank among the gaps gives p = rank / (n + 1) (Abadie, Diamond and Hainmueller 2010). This is a valid randomization test only if the treated label could have fallen on any pool area: the placebo areas must be **exchangeable** with Tambopata. Small areas have volatile paces (a 300-ha area can add 140% in a year), so placebo gaps measured in percentage points are much wider for them. A scale-free statistic (log of the pace ratio) is fairer.

## 6. Our example

### 6.1 Set-up as coded

| Element | As coded | Where |
|---|---|---|
| Universe | 108 Amazon areas with AMW mining and elevation (of 1,174 screened) | `control_psm.py:57-80` |
| Treated | Tambopata buffer zone (PE-BZ-RN09) | `:39` |
| Pool | no operation 2017-21 (R2b) + AMW stock ≥ **100 ha** (the S10 funnel uses 500) + outside Madre de Dios box | `:41`, `:83-88` |
| Covariates | log AMW stock 2018, log median mining elevation, log area, Brazil dummy, indigenous dummy | `:44`, `:72-76` |
| Propensity model | ridge logit (λ = 0.1) of "operation reported 2017-21" on the covariates, fitted on 43 areas with known status (14 "treated", **including Tambopata**) | `:92-116` |
| Caliper | 0.25 SD of the logit score: **computed (`:172`, `:265`) but never passed to `w_nn`** | `:173-174` |
| CEM bins | stock ≥ 0.2 × Tambopata, elevation < 500 m (the R4 cut-offs) | `:136-141` |
| Entropy balancing | balances 4 covariates (not Brazil, which cannot be balanced) | `:47`, `:149-161` |
| Outcome | AMW new area as % of own 2018 stock, mean 2019-21 (and 2022-25) | `:77-79` |
| Inference | placebo in space, rank of the gap (1 = most negative) | `:197-204` |

### 6.2 The pool (20 areas)

15 Brazil, 3 Venezuela, 1 Bolivia, 1 Ecuador, **0 Peru**. By descending propensity score: Yapacana (0.76), Tapajós (0.64), Amanã (0.62), Sawré Muybu (0.46), Urupadi, Apolobamba, Llanganates-Yasuní corridor, Canaima, Jamari, Sararé, ... Yanomami (0.12), Tumucumaque (0.09).

### 6.3 What "treatment" means in the logit (T8)

The 14 areas coded as treated in the logit are: Tambopata BZ, Tambopata National Reserve, Amarakaeri BZ, Bahuaja-Sonene BZ (the 4 Peruvian units, all in the Mercurio landscape), Kayapó, Munduruku, Sai-Cinza, two units of the Parc Amazonien de Guyane (coded "permanent since 2008"), Extended Kaieteur, Jamanxim NP, Crepori, Juruena and Rio Novo. **This is "any reported operation in 2017-21", not "Mercurio-like"**: the score predicts news coverage of enforcement anywhere in the Amazon. Four of the 14 treated are Mercurio itself.

## 7. Tests run and results

### T1 · Reproduce

All seven gaps, ratios, ranks and p-values match `output/numbers.csv` exactly:

| Estimator | Matches (top weights) | Gap 2019-21 (pp) | Ratio | Rank / n | p |
|---|---|---|---|---|---|
| PS nearest 1 | Yapacana | −6.67 | 0.54 | 12 / 21 | 0.57 |
| PS nearest 5 | Yapacana, Tapajós, Amanã, ... | −8.08 | 0.49 | 10 / 21 | 0.48 |
| Mahalanobis 1 | Yapacana | −6.67 | 0.54 | 9 / 21 | 0.43 |
| Mahalanobis 3 | Yapacana, Canaima, Amanã | −8.31 | 0.49 | 11 / 21 | 0.52 |
| CEM | Amanã, Tapajós | −11.74 | 0.40 | 12 / 21 | 0.57 |
| Entropy balancing | Tapajós 50%, Llanganates 23%, Yapacana 16% | −14.38 | 0.35 | 5 / 21 | 0.24 |
| IPW | Yapacana 23%, Tapajós 13%, Amanã 12% | −14.79 | 0.35 | 4 / 21 | 0.19 |

(ids `psm_<method>_gap_during`, `_ratio_during`, `_rank`, `_p`). CEM picks exactly Ruby's two twins, so its ratio equals `top3_ratio` (0.402).

### T2 · Common support (lead 1, reproduced)

| Check | Value |
|---|---|
| Tambopata's propensity score | 0.853 (`psm_ps_tam`) |
| Highest in the pool | 0.758 (Yapacana; `psm_ps_pool_max`) |
| Pool areas with a score ≥ Tambopata's | 0 (`psm_ps_n_above_tam`) |
| Caliper (0.25 SD of the logit) | 0.238 |
| Nearest pool area | 0.613 logit units = 0.64 SD |
| PS nearest 1 / nearest 5 **with the caliper passed** | **no match** |
| ... with a 0.5 SD caliper | no match |
| ... with a 1.0 SD caliper | Yapacana |

**The caliper is computed but never used.** Used as designed, the propensity-score estimators return no match: Tambopata is outside the common support of the pool.

### T9 · Is the lack of support an artefact of fitting the logit on Mercurio?

I refitted the logit without the four Mercurio-landscape units (39 areas, 10 treated). Pseudo-R² falls from 0.215 to 0.113. Tambopata's score falls to 0.664, but the pool maximum falls to 0.580, and still **no pool area reaches Tambopata's score**. PS-nearest results are unchanged (gap −6.67 and −8.08; p 0.52 and 0.48); IPW gives −17.26 (p 0.19). The lack of overlap is not only an in-sample artefact: Tambopata is simply bigger than the non-Brazilian areas and outside Brazil.

### T3 · Balance (lead 2, reproduced)

SMD = Tambopata minus weighted controls, in pool SD:

| | ln stock | ln elevation | ln area | Brazil | indigenous | max \|SMD\| |
|---|---|---|---|---|---|---|
| Unweighted pool | 1.76 | 0.41 | −1.02 | −1.69 | −0.72 | 1.76 |
| PS nearest 1 | 1.18 | 1.33 | −0.15 | 0.00 | 0.00 | 1.33 |
| PS nearest 5 | 0.57 | 1.33 | −0.61 | **−1.80** | −0.41 | 1.80 |
| Mahalanobis 1 | 1.18 | 1.33 | −0.15 | 0.00 | 0.00 | 1.33 |
| Mahalanobis 3 | 0.83 | 0.82 | −0.95 | −0.75 | 0.00 | 0.95 |
| CEM | −0.68 | 1.15 | −1.23 | **−2.25** | 0.00 | 2.25 |
| Entropy balancing | 0.40 | 0.15 | −0.74 | −1.37 | −0.22 | 1.37 |
| IPW | 1.10 | 0.72 | −0.69 | −1.33 | −0.38 | 1.33 |

- **No estimator reaches |SMD| < 0.25 on all covariates; most leave a gap above 1 SD.** The walkthrough's "up to about 1.3 SD" (`explainer_content.md:734`) understates this: CEM leaves 2.25 SD on the Brazil dummy and PS nearest 5 leaves 1.80.
- Entropy balancing does not reach exact balance even on its 4 chosen covariates (residual 0.76 SD; `psm_ebal_max_imbalance`); with Brazil added, 0.83 SD.
- Every estimator that balances "not Brazil" picks Yapacana (Venezuela), at the price of 1.18 SD on stock and 1.33 SD on elevation.

### T4 · Log-ratio placebo (lead 5, reproduced)

Statistic: log(Tambopata pace / matched pace), with each placebo area treated the same way.

| | PS 1 | PS 5 | Maha 1 | Maha 3 | CEM | ebal | IPW |
|---|---|---|---|---|---|---|---|
| log ratio | −0.61 | −0.70 | −0.61 | −0.72 | −0.91 | −1.04 | −1.05 |
| rank / 21 | 8 | 10 | 7 | 11 | 8 | 6 | 4 |
| p | 0.38 | 0.48 | 0.33 | 0.52 | 0.38 | 0.29 | 0.19 |

The scale-free statistic gives the same verdict: **p 0.19-0.52, none below 0.10.**

### T5 · Placebo exchangeability

With PS nearest 1, the absolute placebo gap is larger for smaller areas (Spearman correlation of log stock with |gap| −0.56). The largest placebo gaps (±120-143 pp) belong to Acari (388 ha), Jamanxim Flona, Mapinguari and Tumucumaque (306 ha). Tambopata (21,362 ha) cannot produce such gaps, so in percentage points it is not exchangeable with these areas. For Mahalanobis 1 the correlation is +0.05 and for IPW −0.29. The log-ratio statistic (T4) removes most of this problem and does not change the verdict.

### T6 · Pool variants

| Pool | n | Gaps (pp), range over estimators | p, range |
|---|---|---|---|
| Main | 20 | −14.8 to −6.7 | 0.19-0.57 |
| **Without Brazil** | 5 (3 Venezuela, Bolivia, Ecuador) | −12.1 to −5.3 (CEM: no match) | 0.33-0.83 |
| MIN_STOCK 500 (as the S10 funnel) | 13 | −14.5 to −6.7 | 0.21-0.69 |
| Three territories recoded "unclear" (drops Sawré Muybu) | 19 | −16.3 to −6.7 | 0.15-0.55 |
| Unclear / not searched counted as "none" | 38 | −18.6 to **−0.15** | 0.33-0.62 |

- **Without Brazil** the pool has 5 areas; with 6 ranks the smallest attainable p is 0.17, so the placebo cannot reject anything.
- **The recode (S10 T4) matters for PS nearest 5**: dropping Sawré Muybu (pace 0.22%) moves its gap from −8.1 to −15.9 pp. The smallest p becomes 0.15 (IPW). Still nothing below 0.10.
- **"Keeps every gap negative"** (`explainer_content.md:736`) is literally true but misleading: PS nearest 1 falls to −0.15 pp (match: Lucifer Dékou-Dékou), i.e. no gap (lead 7, reproduced).

### T7 · Influence and the 2022-25 gaps (lead 6, reproduced)

| | Controls' 2022-25 pace | of which Sararé | After-gap | After-gap without Sararé |
|---|---|---|---|---|
| Entropy balancing | 70.6% | 43.6 | −64.1 pp | −25.7 pp |
| IPW | 40.1% | 17.9 | −33.5 pp | −16.7 pp |

Sararé (397 ha in 2018) added 404.6% of its 2018 stock per year in 2022-25. With an 11% (ebal) or 4% (IPW) weight it supplies most of the controls' after-pace. Dropping Tapajós moves the ebal after-gap even more (+50.4 pp), because the weights are re-solved. **The 2022-25 gaps of ebal and IPW are unstable and should not be reported.** The 2019-21 gaps are more stable: the largest single-area move is 8.7 pp (Mahalanobis 3, dropping Canaima).

### Tests not possible here

- **Matched difference in differences**: no pre-period on AMW. A MapBiomas pre-period exists only through name matching to Col 6 geocodes, which was not built for the 108 areas.
- **Re-searching operation status** for the 18 unclear / unsearched pool candidates (new web searches needed).

## 8. Assumption check

| Assumption | Verdict | Evidence |
|---|---|---|
| Unconfoundedness | **Implausible** | Operations target scale, illegality and politics, none of which are in X; the logit's "treatment" is news coverage of any operation (§6.3) |
| Overlap | **Fails** | Tambopata's score above every pool area; no match within a 0.25 or 0.5 SD caliper (T2); still fails without the Mercurio units in the fit (T9) |
| SUTVA | Mostly holds for spillover (nearest pool area Apolobamba, Bolivian highlands, 221 km; the next 621 km); **fails for "untreated"**: Brazil's 2019-22 de-enforcement (S10 T11) | |
| Score model | Weak | pseudo-R² 0.215 on 43 points, 5 covariates |
| Balance | **Fails** | max \|SMD\| 0.95-2.25 (T3) |
| Placebo exchangeability | Fails in pp, roughly OK in log ratio | T4, T5 |

## 9. Weaknesses, ranked

1. **One treated unit outside common support.** Every estimator extrapolates; the caliper, if applied, returns no match.
2. **Country is confounded with treatment.** No Peruvian area is in the pool; 15 of 20 are Brazilian, during Brazil's weaker-enforcement years. Matching cannot fix a confounder that is constant within the treated unit and missing among comparable controls.
3. **Balance fails** on at least one covariate for every estimator (≥ 0.95 SD).
4. **The "treatment" in the score is not Mercurio** (any reported operation 2017-21, coded from news searches, with Mercurio's own landscape inside).
5. **Post-only outcome**: no differencing, so permanent differences between areas load straight into the gap.
6. **Fragile details**: MIN_STOCK 100 vs 500 in the funnel; Sawré Muybu miscoded (S10); Sararé drives the 2022-25 gaps; caliper computed but unused.
7. **Text**: "traits differ by up to about 1.3 SD" (actually up to 2.25); "keeps every gap negative" (−0.15 pp for PS nearest 1).

## 10. Proposed decisions

| # | Decision | Recommendation |
|---|---|---|
| D-S11-1 | Apply the caliper | Pass `caliper=cal` in `weights()` for `ps_nn1`/`ps_nn5`. Report "no match within 0.25 SD of the score" instead of a gap. |
| D-S11-2 | What to keep | Keep **Mahalanobis 1 and 3, CEM and the log-ratio placebo** as an illustration. Drop PS and IPW from the headline: with one treated unit they add nothing and invite misreading. |
| D-S11-3 | 2022-25 gaps | Do not report ebal / IPW after-gaps (Sararé). |
| D-S11-4 | Placebo statistic | Report the log-ratio placebo p (0.19-0.52) next to, or instead of, the pp version. |
| D-S11-5 | Pool definition | Align MIN_STOCK with the funnel (500) or justify 100; apply the S10 recode (Sawré Muybu "unclear"). |
| D-S11-6 | Fix text | "Balance fails by up to 2.25 SD (Brazil)"; drop "keeps every gap negative". |
| D-S11-7 | Claim label | **Description.** Wording: "an algorithm finds the same kind of comparison as Ruby's rules, and it cannot separate Tambopata from chance". |

## 11. Verdict

The seven matching estimators are **coded correctly** and reproduce exactly. They agree on the direction: all find Tambopata slower than its matches in 2019-21, with a pace ratio of 0.35-0.54. But the design they implement cannot identify an effect:
- one treated unit;
- outside common support (the caliper, if applied, finds no match);
- confounded with country;
- imbalanced after matching;
- post-only outcome;
- placebo p 0.19-0.57 (pp) or 0.19-0.52 (log ratio).

With one treated unit, matching is a formal restatement of the S10 case study, and the code's own docstring says so (`control_psm.py:23-26`).

Label: **description**.

**The brief may say:** "Formal matching methods pick comparison areas similar to Ruby's twins. All seven find Tambopata slower in 2019-21, but no area in the Amazon resembles Tambopata closely enough for a fair match, and the gap is within the range seen when each comparison area is treated as a fake 'treated' area [D]."

**The brief must not say:** "propensity-score matching shows Mercurio reduced mining by X%", "matched controls", "balanced comparison", or any 2022-25 matching number.

## References

- Abadie, A., Diamond, A. and Hainmueller, J. (2010). Synthetic control methods for comparative case studies. *Journal of the American Statistical Association* 105(490).
- Abadie, A. and Imbens, G. (2006). Large sample properties of matching estimators for average treatment effects. *Econometrica* 74(1).
- Abadie, A. and Imbens, G. (2016). Matching on the estimated propensity score. *Econometrica* 84(2).
- Austin, P. (2011). Optimal caliper widths for propensity-score matching when estimating differences in means and differences in proportions in observational studies. *Pharmaceutical Statistics* 10(2).
- Crump, R., Hotz, V. J., Imbens, G. and Mitnik, O. (2009). Dealing with limited overlap in estimation of average treatment effects. *Biometrika* 96(1).
- Hainmueller, J. (2012). Entropy balancing for causal effects. *Political Analysis* 20(1).
- Hirano, K., Imbens, G. and Ridder, G. (2003). Efficient estimation of average treatment effects using the estimated propensity score. *Econometrica* 71(4).
- Iacus, S., King, G. and Porro, G. (2012). Causal inference without balance checking: coarsened exact matching. *Political Analysis* 20(1).
- Imbens, G. and Rubin, D. (2015). *Causal Inference for Statistics, Social, and Biomedical Sciences*. Cambridge University Press.
- King, G. and Nielsen, R. (2019). Why propensity scores should not be used for matching. *Political Analysis* 27(4).
- Rosenbaum, P. and Rubin, D. (1983). The central role of the propensity score in observational studies for causal effects. *Biometrika* 70(1).
- Rosenbaum, P. and Rubin, D. (1985). Constructing a control group using multivariate matched sampling methods that incorporate the propensity score. *The American Statistician* 39(1).
- Rubin, D. (1980). Bias reduction using Mahalanobis-metric matching. *Biometrics* 36(2).
- Stuart, E. (2010). Matching methods for causal inference: a review and a look forward. *Statistical Science* 25(1).
