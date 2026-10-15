# S6 · Synthetic control (attempt A5)

*Method card 6 of the causal review (plan: `docs/causal_review_plan.md`). Code under review: `code/peru_synth.py` (six specifications) and the `"sc"` branch of `code/peru_sdid.py:72-73` (the source of the −411 in the brief). Test script: `code/review/s6_synth_checks.py` (read-only, own solver, about 5 minutes).*

---

## 1. In one sentence

Build a "synthetic" copy of the treated unit as a weighted average of untreated units, with weights chosen so that the copy tracks the treated unit closely before the treatment; after the treatment, the gap between the unit and its copy is the estimated effect.

## 2. Simple version

Suppose one region gets a new policy and you want to know what would have happened without it. No single other region looks like it. But maybe 60% of region X plus 40% of region Y, averaged year by year, reproduces the treated region's past almost exactly. If that mix tracked it for ten years before the policy, it is a believable stand-in for the years after. The gap after the policy is the effect.

Two things make the idea work:
- **The copy must fit the past.** If the mix does not reproduce the treated region before the policy, its path after the policy says nothing.
- **The copy can only interpolate.** Weights are non-negative and sum to one, so the mix always lies *between* the donors. If the treated region is bigger than every donor in every year, no mix can reach it.

The second point is our problem. Tambopata's buffer zone added about 1,400 ha of mining a year before 2019. The largest non-Madre de Dios donor added at most 89 ha in any year. You cannot average numbers below 89 and get 1,400.

## 3. When to use it, and when not

**Use it when:**
- one or a few units are treated (a country, a state, a reserve);
- there is a pool of untreated "donors" with the same kind of outcome;
- there is a long pre-period (Abadie 2021 suggests many pre-treatment periods), so the fit is informative;
- the treated unit sits inside the range of the donors (the convex hull), at least approximately.

**Avoid it, or change the method, when:**
- the treated unit is extreme (the largest, the fastest-growing): the copy cannot fit, and the gap mostly measures the level difference;
- the outcome is very noisy relative to the effect, so a good pre-fit can be luck (overfitting);
- donors may be affected by the treatment (spillovers), because then the copy moves with the treatment;
- the donors are very small, so a few hectares of noise in a donor become hundreds of hectares once scaled.

## 4. Assumptions

| Assumption | In words | Formally |
|---|---|---|
| **Factor (or autoregressive) model** | Untreated outcomes are driven by a few common shocks that hit units with different loadings | Y_it(0) = δ_t + θ_t Z_i + λ_t μ_i + ε_it |
| **Convex hull / good pre-fit** | Some mix of donors reproduces the treated unit's pre-period path, and through it its loadings μ_1 | ∃ w ∈ Δ: Σ_j w_j Y_jt ≈ Y_1t for all t ≤ T_0 |
| **No interference** | Donors are not affected by the treatment | Y_jt = Y_jt(0) for donors j, all t |
| **No anticipation** | The treated unit did not react before T_0 | Y_1t = Y_1t(0), t ≤ T_0 |
| **No other unit-specific shock** | Nothing else hit the treated unit (and not the donors) after T_0 | ε_1t is not systematically shifted after T_0 |
| **Exchangeability (for placebo inference)** | Under the null, the treated unit's statistic is just one draw from the same distribution as the donors' | permutation-based p-values are valid |

## 5. The maths

### 5.1 Master's level

Unit 1 is treated from period T_0 + 1. Donors j = 2..J+1. Choose weights

  ŵ = argmin over w of Σ_{t ≤ T_0} (Y_1t − Σ_j w_j Y_jt)², subject to w_j ≥ 0 and Σ_j w_j = 1.

(With covariates, Abadie et al. 2010 match a vector of pre-period characteristics X_1 ≈ X_0 w with a variable-importance matrix V; ours uses only the outcome in each pre-year.)

The synthetic outcome is Ŷ_1t(0) = Σ_j ŵ_j Y_jt and the estimated effect in year t > T_0 is

  τ̂_t = Y_1t − Ŷ_1t(0).

**Pre-fit.** RMSPE_pre = √(mean over t ≤ T_0 of (Y_1t − Ŷ_1t)²). If RMSPE_pre is of the same size as the post-period gap, the gap is not distinguishable from misfit.

**Inference (placebo in space).** Re-run the method pretending each donor is treated (using the other donors). Compute for each unit the ratio R = RMSPE_post / RMSPE_pre. The rank of the treated unit's R among all units gives a permutation p-value, p = rank / (J + 1) (Abadie et al. 2010, 2015). The ratio is a **two-sided** statistic: a large post-period gap in *either* direction, in *any* post year, raises it.

### 5.2 PhD level

**Why the fit justifies the estimate.** Under the factor model with J donors and T_0 pre-periods, Abadie et al. (2010) bound the bias of τ̂_t when the synthetic unit fits the pre-period outcomes *exactly*. The bound shrinks with T_0 relative to the noise scale and grows with the number of donors. With imperfect fit, the bound does not apply. Ferman and Pinto (2021) show that with imperfect pre-fit the SC estimator is generally biased even as T_0 grows, unless the outcome is demeaned (an intercept), which links SC to DiD.

**Interpolation vs extrapolation.** The simplex constraint (w ≥ 0, Σw = 1) is what keeps SC honest: the counterfactual is an interpolation among real units, and weights are sparse and interpretable (Abadie 2021). The price is that the method has no answer when the treated unit lies outside the convex hull of the donors. Then the optimum sits on a corner (all weight on the donor nearest the treated unit), the pre-fit is poor, and the "gap" equals the level difference between the treated unit and that one donor. Relaxing the constraint (Doudchenko and Imbens 2016: intercept, negative weights, penalties) or adding an outcome model (Ben-Michael, Feller and Rothstein 2021, augmented SC) allows extrapolation, at the cost of the interpretability that made SC attractive.

**Interpolation bias.** Even inside the hull, a mix of very different units (say an Andean reserve and a lowland one) only reproduces the treated unit's path if the relationship between characteristics and outcomes is roughly linear. Abadie et al. (2015) recommend restricting the donor pool to units similar to the treated one for this reason.

**Donor pool rules.** Donors must (a) be plausibly untreated and unaffected by spillovers, (b) be driven by the same structural process, (c) be chosen *before* looking at post-period results (Abadie 2021). Changing the pool after seeing the results is a specification search.

**The RMSPE ratio test.** Firpo and Possebom (2018) show the ratio test is a Fisher randomization test under the sharp null with equal assignment probabilities; it is invalid if units differ systematically in how likely they were to be treated, and it tests "any post-period deviation", not "a fall in 2019-21". If the hypothesis is one-sided and about a sub-period, the test statistic should be too (for example, the mean gap in 2019-21 divided by RMSPE_pre). Abadie et al. (2010) also drop placebos whose pre-fit is much worse than the treated unit's (for example, more than 5 times its MSPE). The logic of that filter assumes the treated unit fits *well*; it gives no guidance when the treated unit fits worst of all.

**Extreme units.** When the treated unit is the largest in the pool, three things happen together: the pre-fit is poor (hull failure), the RMSPE_pre is large, so the ratio is deflated and the treated unit ranks *low*; and the raw gap is large in absolute terms, so a signed-gap statistic ranks it *high*. The two statistics then disagree for a reason unrelated to the treatment: scale.

## 6. Our example

### 6.1 Units, outcome and specifications

| Element | As coded | Where |
|---|---|---|
| Treated | Tambopata buffer zone, all department rows summed | `peru_synth.py:30`, levels from `peru.build_series` |
| Outcome | net annual addition (ha), MapBiomas Peru Col 4 workbook | `peru_synth.py:50-60` |
| Eligible donors | mean \|addition\| 2010-18 ≥ 1 ha, Tambopata excluded (12 zones) | `peru_synth.py:62-65` |
| Pools | **core** = without Amarakaeri and Bahuaja-Sonene (10 donors); **ext** = with them (12) | `peru_synth.py:66-67` |
| Outcomes | **add** (ha, fit 2010-18); **addsc** (÷ own 2014-18 mean \|addition\|, donors with scale ≥ 5 ha, fit 2010-18); **cum** (cumulative since 2013, fit 2014-18) | `peru_synth.py:50-71` |
| Weights | simplex least squares, SLSQP from the uniform start and every vertex | `peru_synth.py:34-48` |
| Statistic | RMSPE ratio over all post years 2019-25; rank 1 = largest ratio | `peru_synth.py:73-96` |
| Hull check | fit years where Tambopata is outside the donors' min-max | `peru_synth.py:97-98` |
| Registered | 14 ids per spec, `synth_<pool>_<kind>_*` | `peru_synth.py:104-125` |
| **Second SC** | `sdid(..., method="sc")`: pool B (15 zones, as the ladder), fit 2014-18, no intercept, no penalty, no time weights; statistic = signed τ, rank 1 = most negative | `peru_sdid.py:72-73, 79, 83-87` |
| Used in text | `sdid_sc_ha_during` (−411) is the lower end of the brief's [C] range | `brief_content.md:27, 29`; `explainer_content.md:43, 430, 953` |

The SC branch is at `peru_sdid.py:72-73` (the plan pointer has been corrected).

### 6.2 The three pool and statistic regimes side by side

| | `peru_synth` (A5) | `peru_sdid` SC branch | Ladder M1-M4 (A3) and SDID (A6) |
|---|---|---|---|
| Pool rule | mean \|add\| 2010-18 ≥ 1 ha; core drops Amarakaeri, Bahuaja | Σ\|add\| 2014-18 > 0 (pool B, 15 zones) | pool B (15); M4 / scaled: pre-mean > 10 ha (7 zones) |
| Zones in B but not in A5 | de Calipuy, Pacaya-Samiria (both near 0 ha) | | |
| Scale for "scaled" | own 2014-18 mean **\|addition\|**, donors ≥ 5 ha | | own 2014-18 **signed** mean, > 10 ha |
| Fit window | 2010-18 (cum: 2014-18) | 2014-18 | 2014-18 (SDID sensitivity 2011-18) |
| Statistic | RMSPE ratio, 2019-25, two-sided | signed τ 2019-21, one-sided | signed coefficient 2019-21, one-sided |

Three different pools, two scales, two fit windows and two statistics. A rank from one regime cannot be compared with a rank from another (X7).

## 7. Tests run and results

All numbers below come from `code/review/s6_synth_checks.py` unless an id from `output/numbers.csv` is given.

### T1 · Reproduce the six specifications with an independent solver

I re-solved every weight problem with my own accelerated projected-gradient solver (convex problem, so one start reaches the global minimum).

| Spec | Donors | Top weight (repo) | Pre-RMSPE repo / ours (ha) | Gap 2019-21 repo (ha) | Gap 2022-25 repo (ha) | Ratio rank (repo) |
|---|---|---|---|---|---|---|
| core_add | 10 | Allpahuayo Mishana 0.987 (ours 1.000) | 1,466.7 / 1,466.3 | +149.5 | +1,907 | 10 of 11 (p 0.91) |
| core_addsc | 5 | Subcuenca del Cotahuasi 0.771 | 646.6 / 646.6 | −3,383.7 | +3,650 | **1 of 6 (p 0.17)** |
| core_cum | 10 | 1/3 each on three donors (ours: Allpahuayo 1.000) | **4,980.7 / 4,887.6** | +8,299 | +12,689 | 8 of 11 |
| ext_add | 12 | Amarakaeri 0.998 (ours 1.000) | 1,130.1 / 1,129.6 | −410.3 | +616 | **13 of 13** (p 1.00) |
| ext_addsc | 7 | Río Abiseo 0.336, Amarakaeri 0.284, Bahuaja 0.267 | 536.1 / 536.1 | −2,670.6 | −2,702 | 5 of 8 (p 0.63) |
| ext_cum | 12 | 0.5 / 0.5 (ours: Amarakaeri 1.000) | **4,346.1 / 3,807.2** | +6,946 | +9,395 | 12 of 13 |

Repo ids: `synth_<spec>_pre_rmspe`, `_gap_2019_21`, `_gap_2022_25`, `_rank`, `_w1`.

- The add and addsc specs reproduce to the first decimal.
- **New finding: SLSQP does not reach the optimum in the two cum specs.** The pre-period sum of squared residuals at the repo weights is 124.0 M (core_cum) and 94.4 M (ext_cum); at the true optimum it is 119.4 M and 72.5 M. The repo's "1/3, 1/3, 1/3" and "0.5, 0.5" are solver artefacts. The true optimum is a corner (all weight on the largest donor), as the hull failure predicts.
- **Audit lead (1) partly does not reproduce:** the core_add top weight is 0.987 on Allpahuayo Mishana (`synth_core_add_w1`), not 0.79. Everything else in lead (1) reproduces: synthetic pre-mean 32.4 vs Tambopata 1,375.3 (`synth_core_add_pre_mean_synth`, `_pre_mean_tam`), outside the donor range in 9 of 9 fit years, pre-RMSPE 1,466.7, rank 10 of 11.

### T2 · Convex hull

| Fit year | 2010 | 2011 | 2012 | 2013 | 2014 | 2015 | 2016 | 2017 | 2018 |
|---|---|---|---|---|---|---|---|---|---|
| Tambopata (ha) | 461 | 1,563 | 743 | 1,639 | 1,590 | 1,463 | 707 | 2,455 | 1,757 |
| Largest core donor (ha) | 31 | 9 | 14 | 56 | 58 | 89 | 53 | 28 | 59 |
| Largest ext donor (ha) | 653 | 882 | 587 | 423 | 542 | 301 | 362 | 452 | 59 |

- Core pool: Tambopata is above every donor in **9 of 9** years, by a factor of 13 to 174.
- Ext pool: above every donor in 8 of 9 (only Amarakaeri in 2010 is higher).
- The convex-hull condition fails completely in hectares. No reweighting of these donors can fix it.

### T3 · The scaled specification (core_addsc): what the "good fit" is made of

**The donors.** After the 5-ha scale filter, five donors remain. The fit puts 77% on Subcuenca del Cotahuasi, a landscape reserve in Apurímac, Arequipa, Ayacucho and Cusco (high Andes, 144 ha of mining in 2018, scale 12.2 ha). Cordillera Azul gets 16% and Río Abiseo 7%.

**The gaps, year by year (units of one normal 2014-18 year):**

| | 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Tambopata | 1.00 | 0.92 | 0.44 | 1.54 | 1.10 | 0.26 | 0.11 | −0.07 | 0.36 | 2.24 | 0.80 | 1.19 |
| Synthetic | 0.48 | 0.64 | 0.99 | 0.86 | 0.89 | 0.92 | **3.44** | **2.31** | 1.14 | 0.07 | 0.51 | **−6.29** |
| Gap | 0.51 | 0.28 | −0.54 | 0.68 | 0.21 | −0.66 | −3.33 | −2.38 | −0.78 | 2.16 | 0.29 | 7.48 |

(Verified for the scaled values: Tambopata 2019-21 mean = 0.10, i.e. 163 ha over a scale of 1,594 ha.)

**New finding: more than half of the scaled 2019-21 gap is the synthetic rising, not Tambopata falling.**
- Tambopata's own change, 2014-18 to 2019-21: **−0.90** normal years (−1,432 ha).
- The synthetic's change: **+1.45** normal years.
- The synthetic jumps because Cotahuasi added 53 ha in 2020 and 34 ha in 2021 (against a 12.2 ha scale). Unscaled with Tambopata's 1,594 ha, these few dozen Andean hectares become about 2,300 "Tambopata hectares" of counterfactual.
- The same mechanism makes 2025: Cotahuasi's −96 ha in 2025 sends the synthetic to −6.29 and the gap to +7.48, which drives the 2022-25 gap of +3,650 ha.

**Ranks under different statistics (6 units):**

| Statistic | Tambopata rank |
|---|---|
| RMSPE ratio 2019-25, two-sided (repo) | 1 |
| RMSPE ratio 2019-21 | 1 |
| Most negative mean gap 2019-21 | 1 |
| Most negative mean gap 2019-21 ÷ pre-RMSPE | 1 |
| Most positive mean gap 2022-25 | 1 |

- **Audit lead (2) only partly reproduces.** The registered statistic pools 2019-25 two-sided, and 78% of Tambopata's post-period squared gap comes from 2022-25 (mostly the 2025 Cotahuasi artefact). So the explainer's "Tambopata's 2019-21 dip is the deepest" (`explainer_content.md:583, 587`) is **not what the registered rank measures**. But a one-sided 2019-21 statistic also gives rank 1 of 6. The sentence is true in this specification; it is cited with the wrong statistic.
- The mirror image: Cotahuasi's own placebo gap in 2019-21 is +1.80, the third-largest in absolute value (after Tambopata −2.12 and Junín −1.92). On the 2019-21 RMSPE ratio, Tambopata and its main donor rank 1 and 2 (5.90 and 5.44) because they are the two sides of the same Andean spike.
- **Ext pool (ext_addsc):** adding Amarakaeri and Bahuaja-Sonene changes the weights (Río Abiseo 0.34, Amarakaeri 0.28, Bahuaja 0.27), the ratio rank falls to 5 of 8, the one-sided 2019-21 rank is 2 of 8, and the 2022-25 gap flips sign (+3,650 core vs −2,702 ext, in ha). Audit lead (2) reproduces on this point.

### T4 · The −411: one estimate, two ranks

| | `peru_sdid` SC branch | `peru_synth` ext_add |
|---|---|---|
| Pool, fit window | pool B (15), 2014-18 | ext (13), 2010-18 |
| Weights | Amarakaeri **1.000** | Amarakaeri 0.998 |
| Gap 2019-21 | **−411.3** (`sdid_sc_ha_during`) | −410.3 (`synth_ext_add_gap_2019_21`) |
| Pre-RMSPE | 1,376.9 (ours) | 1,130.1 |
| Synthetic pre-mean vs Tambopata | 342 vs 1,594 (2014-18) | 472 vs 1,375 (2010-18) |
| Rank | **1 of 15** (signed τ) | **13 of 13** (RMSPE ratio) |

**What the −411 is.** With all weight on Amarakaeri and no intercept, the SC gap is simply Tambopata's 2019-21 mean minus Amarakaeri's 2019-21 mean: 163 − 574 = −411. It ignores that Tambopata mined 1,252 ha/yr *more* than Amarakaeri in 2014-18. By the same logic the "effect" in 2014-18, before the operation, would be +1,252 ha/yr.

**Why the ranks disagree.** On the same pool B and the same estimate, I computed four statistics:

| Statistic | Tambopata rank of 15 |
|---|---|
| Signed 2019-21 gap (peru_sdid) | 1 |
| \|gap\| | 2 |
| RMSPE ratio (peru_synth) | **15** |
| Gap ÷ pre-RMSPE | 6 |

- Placebo pre-RMSPEs: median 2.0 ha, largest 340 ha. Tambopata's: 1,377 ha.
- The signed rank is 1 because Tambopata's gap is measured in hundreds of hectares and the placebos' in single hectares: a scale effect (X1).
- The ratio rank is 15 because Tambopata's pre-fit error (1,377) is 3.4 times its post-period gap: by the method's own logic the gap is pure misfit.
- Once the gap is put on the pre-fit scale, Tambopata ranks 6 of 15: unremarkable.
- The ADH pre-fit filter (drop placebos with pre-RMSPE more than 2, 5 or 20 times the treated unit's) removes no placebo at all here, because the treated unit is the one with the worst fit.

**Audit lead (4) reproduces in full.** And per X12, the single donor carrying 100% of the weight is a buffer zone whose land mined by 2018 is 58% legal corridor and 41% native communities, partly treated (Mercurio II, the 2023 emergency) and the likely destination of displaced miners (S2 T6b). The −411 is "Tambopata vs the legal corridor near Huepetuhe in 2019-21", without any pre-period adjustment.

### T5 · An aligned specification

Same pool, fit window and post window as the ladder and SDID (pool B, fit 2014-18, post 2019-21).

| Variant | Gap 2019-21 (ha) | Pre-RMSPE (ha) | Weights | Signed rank | Ratio rank | Gap/pre rank |
|---|---|---|---|---|---|---|
| SC, no intercept | −411 | 1,377 | Amarakaeri 1.00 | 1 | 15 | 6 |
| SC with intercept (demeaned) | −1,457 | 553 | Cordillera Azul 0.93, Amarakaeri 0.07 | 1 | 12 | 6 |

- Adding an intercept (Ferman and Pinto 2021; Doudchenko and Imbens 2016) moves the estimate from −411 to −1,457, close to M1 (−1,454, `model_m1_during`). With an intercept, SC becomes a reweighted DiD.
- But the demeaned weights fall 93% on Cordillera Azul, a zone whose cumulative additions 2014-18 were negative (−18 ha by 2018, T6). Its role is to be flat; the estimate is then essentially Tambopata's own before/after change (−1,432 ha from 2014-18 to 2019-21, S2 T2).
- Under no statistic that accounts for pre-fit does Tambopata stand out (ratio rank 12-15, gap/pre rank 6).

### T6 · The cumulative specification is degenerate

- Donors' cumulative additions since 2013 reach at most 262 ha by 2018 (Allpahuayo Mishana); Tambopata reaches 7,972 ha.
- The true optimum is a corner (all weight on the largest donor). The repo's equal weights come from SLSQP stopping early (T1).
- Pre-RMSPE is 108% of Tambopata's own pre-mean in the core pool (84% ext). The cum gaps (+8,299 and +6,946 ha in 2019-21) are positive simply because the cumulative level gap keeps growing. Audit lead (5) reproduces.

### T7 · Pre-fit quality against the gap, all specifications

| Spec | Pre-RMSPE (ha) | Gap 2019-21 (ha) | \|gap\| ÷ pre-RMSPE | Pre-RMSPE as % of Tambopata's mean |
|---|---|---|---|---|
| core_add | 1,466 | +150 | 0.10 | 107% |
| ext_add | 1,130 | −411 | 0.36 | 82% |
| core_cum | 4,888 | +8,156 | 1.67 | 108% |
| ext_cum | 3,807 | +5,737 | 1.51 | 84% |
| core_addsc | 647 | −3,384 | 5.23 | 47% |
| ext_addsc | 536 | −2,671 | 4.98 | 39% |

(Gaps for cum and add here use our optimal weights; they differ slightly from the repo values in T1.)

- In every hectare and cumulative specification, the pre-fit error is 82-108% of Tambopata's own pre-period mean: the copy explains essentially nothing.
- Only the scaled specifications have a gap that exceeds the pre-fit error, and T3 shows their gap is driven by an Andean donor's few dozen hectares.

### Tests not possible here

- Covariate-based SC (gold geology, distance to road, river access per buffer zone): no covariate table at buffer-zone level exists in the repo.
- SC on first-time mining by buffer zone: raster zone-year accounting (`data_intermediate/zone_year_v2.csv`) covers 12 custom zones in Madre de Dios, not the 15 Peruvian buffer zones (and the rasters are git-ignored).

## 8. Assumption check

| Assumption | Verdict | Evidence |
|---|---|---|
| Convex hull / good pre-fit (ha) | **Fails completely** | Outside the donor range in 9 of 9 (core) and 8 of 9 (ext) fit years; pre-RMSPE 82-108% of Tambopata's mean (T2, T7) |
| Convex hull / good pre-fit (scaled) | Fits, for the wrong reason | Pre-RMSPE 0.41 normal years, but 77% weight on an Andean reserve with a 12-ha scale (T3) |
| Factor model shared by donors and treated | **Implausible** | Donors are Andean, coastal and Loreto zones with near-zero mining; Tambopata is the centre of the Madre de Dios gold rush |
| No interference (ext pool, SC in peru_sdid) | **Violated** | Weight 1.0 on Amarakaeri: 58% legal corridor, partly treated, likely recipient of displaced miners (X12, S2 T6b) |
| No interference (core pool) | Plausible | Core donors are far from Madre de Dios |
| Exchangeability for placebo ranks | **Fails** | Tambopata's pre-RMSPE (1,377) is 4 times the worst placebo's (340) and 700 times the median (2.0) (T4) |
| Valid test statistic for the claim | **No** | Ratio is two-sided over 2019-25; signed τ is a scale statistic (T3, T4) |

## 9. Weaknesses, ranked

1. **The −411 in the brief's [C] range is not a synthetic-control estimate in any meaningful sense.** It is Tambopata minus Amarakaeri in 2019-21 (163 − 574), with a pre-fit error 3.4 times its size, from a single donor that is mostly legal corridor and partly treated. The same number ranks 15 of 15 (ratio) or 1 of 15 (signed), depending only on the statistic (T4).
2. **Convex-hull failure in hectares is total.** No specification in hectares or cumulative hectares has a usable pre-fit (T2, T7). The module's own docstring (`peru_synth.py:16-18`) and figure title already say so; the brief does not.
3. **The scaled "good fit" is an Andean artefact.** More than half the 2019-21 scaled gap is Cotahuasi's 2020-21 spike of a few dozen hectares, multiplied by 1,594/12.2 ≈ 130 when unscaled (T3). The 2022-25 gap is likewise driven by Cotahuasi's 2025 drop (−96 ha).
4. **Specification instability.** Adding two donors flips the scaled 2022-25 gap from +3,650 to −2,702 ha and moves the ratio rank from 1 of 6 to 5 of 8 (T3).
5. **Mislabelled statistic.** "Deepest dip" (explainer) is supported by a one-sided statistic I computed, not by the registered two-sided 2019-25 ratio.
6. **Solver does not converge in the cum specs** (T1); the equal weights in `peru_synth_weights.csv` are wrong. Low impact because the spec is degenerate anyway.
7. **Three pool rules, two scales, two fit windows, two statistics** across A3, A5, A6 (X7).

## 10. Proposed decisions

| # | Decision | Recommendation |
|---|---|---|
| D-S6-1 | The −411 lower end of the [C] range (`brief_content.md:29`, `explainer_content.md:43, 953`) | **Remove.** No SC number enters the [C] range. Replace the lower end with a specification meeting S14's criterion (pooled 2014-18 baseline, no extrapolated slope or trend); see D-S14-3. |
| D-S6-2 | `brief_content.md:27` "synthetic control −411 ... (both rank 1)" | Replace with: "A synthetic control cannot be built: Tambopata mined more than every other zone in every year before 2019, so no weighted mix of them fits [D]." |
| D-S6-3 | Explainer "Scaled, a good fit: the deepest dip" (`explainer_content.md:583, 587`) | Rewrite: the scaled fit puts 77% weight on an Andean reserve, more than half the 2019-21 gap is that reserve's spike, six zones, p = 0.17. Label [D]; "weak check" stays. |
| D-S6-4 | Statistic | If SC is kept anywhere, report a one-sided 2019-21 statistic divided by pre-RMSPE, together with the ratio, and say which one the text uses. |
| D-S6-5 | Pool and window alignment | If SC is kept, use pool B and fit 2014-18 (as A3 and A6) so ranks are comparable; drop the cum spec. |
| D-S6-6 | Solver | Replace SLSQP in `peru_synth.fit_weights` by the FISTA solver already in `peru_sdid._simplex_ls` (no intercept, no penalty), or stop registering cum weights. Low priority. |
| D-S6-7 | Figure `fig_peru_synth.png` | Keep only as the illustration of why SC fails (its title already says so). |

## 11. Verdict

Synthetic control is the wrong tool for this treated unit. Tambopata's buffer zone is the most extreme unit in the pool: before 2019 it added 13 to 174 times more mining a year than any donor outside Madre de Dios. The hull condition fails in every year. The pre-fit error is as large as Tambopata's own mean, so every hectare gap, including the −411 in the brief, is misfit, not counterfactual. The scaled version fits, but only by leaning on an Andean landscape reserve whose few dozen hectares of noise become thousands of "Tambopata hectares".

Label: **description**, and only of the failure.

**The brief may say:** "A synthetic control cannot reproduce Tambopata's buffer zone before 2019: it added more mining than any other Peruvian buffer zone in every year, so no weighted mix of them fits [D]."

**The brief must not say:** "synthetic control −411 ha/yr (rank 1)"; any [C] range whose end comes from SC; "the deepest dip" as evidence of an effect; that SC "agrees" with the other methods.

## References

- Abadie, A. (2021). Using synthetic controls: feasibility, data requirements, and methodological aspects. *Journal of Economic Literature* 59(2).
- Abadie, A. and Gardeazabal, J. (2003). The economic costs of conflict: a case study of the Basque Country. *American Economic Review* 93(1).
- Abadie, A., Diamond, A. and Hainmueller, J. (2010). Synthetic control methods for comparative case studies: estimating the effect of California's tobacco control program. *Journal of the American Statistical Association* 105(490).
- Abadie, A., Diamond, A. and Hainmueller, J. (2015). Comparative politics and the synthetic control method. *American Journal of Political Science* 59(2).
- Ben-Michael, E., Feller, A. and Rothstein, J. (2021). The augmented synthetic control method. *Journal of the American Statistical Association* 116(536).
- Doudchenko, N. and Imbens, G. (2016). Balancing, regression, difference-in-differences and synthetic control methods: a synthesis. NBER Working Paper 22791.
- Ferman, B. and Pinto, C. (2021). Synthetic controls with imperfect pretreatment fit. *Quantitative Economics* 12(4).
- Firpo, S. and Possebom, V. (2018). Synthetic control method: inference, sensitivity analysis and confidence sets. *Journal of Causal Inference* 6(2).
