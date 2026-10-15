# S4 · Two-way fixed effects: the model ladder M1-M4 (attempt A3)

*Method card 4 of the causal review (plan: `docs/methods/causal_review_plan.md`). Code under review: `code/peru_models.py` (with `code/common.py:55-61`, `placebo_rank`). Test script: `code/review/s4_twfe_checks.py` (read-only, about 6 s).*

---

## 1. In one sentence

A two-way fixed effects (TWFE) regression is a difference in differences written as a regression: each place gets its own constant, each year gets its own constant, and the treatment coefficient is what is left of the treated place's post-period outcome after both are removed.

## 2. Simple version

Think of a class of 15 pupils and their test scores over 12 years.

- The **pupil effect** says "Ana always scores higher than Ben". It removes permanent differences.
- The **year effect** says "2020's exam was harder for everyone". It removes shocks that hit every pupil in the same year by the same number of points.
- The **treatment coefficient** asks: after removing both, did the one pupil who got a tutor in 2019 score differently from what we would expect?

Two traps follow from "by the same number of points".

1. If the exam got harder by 10% for everyone, a pupil who usually scores 90 loses 9 points and one who scores 10 loses 1 point. Year effects in points cannot absorb that. You need either a proportional scale or an interaction ("harder exam × usual score").
2. If 14 pupils score around 1 point and one scores 100, the year effects are learnt almost only from the 14 small pupils. "The year effect absorbs the hard exam" then means "we assume the big pupil lost as many points as the small ones", which is usually wrong.

Our case is trap 2 almost exactly: Tambopata's pre-2019 additions are 50 times the average of the 14 comparison zones.

## 3. When to use it, and when not

**Use it when:**
- one or more units are treated at known dates and many comparable units are not;
- the comparison units are similar in size and dynamics, so additive common shocks are plausible;
- you want the 2×2 DiD with more years and more comparison units, plus covariates.

**Be careful or avoid it when:**
- the treated unit is far larger than the comparison units (year effects learnt from small units say little about a big one);
- you add covariates that vary within the post period while the treatment dummy is binned (the covariate then explains part of the treated unit's own post-period path, see §5.2);
- you add unit-specific trends fitted on the whole sample (post-period data then bend the treated unit's trend);
- treatment timing is staggered with heterogeneous effects (negative weights; not our case, one treated unit);
- there is one treated unit: no sampling standard error. Use placebo ranks.

## 4. Assumptions

| Assumption | In words | Formally |
|---|---|---|
| **Additive separability** | Without treatment, each zone's outcome is its own constant plus a common year shock plus noise | Y_it(0) = α_i + γ_t + ε_it |
| **Parallel trends (levels)** | The common year shock is the same number of hectares for every zone, Tambopata included | E[Y_Tt(0) − Y_Ts(0)] = E[Y_Ct(0) − Y_Cs(0)] |
| **Correct covariate model** (M2, M3) | The extra terms describe the untreated path: gold response proportional to pre-2019 size (M2); a straight-line trend per zone that would have continued (M3) | Y_it(0) = α_i + γ_t + θ·pre_i·ln g_t (+ δ_i·t) + ε_it |
| **Covariates not affected by treatment** | The covariates do not respond to Mercurio | pre_i, g_t and t are fixed before 2019 or external |
| **No anticipation** | 2014-18 is untreated | Y_it = Y_it(0) for t ≤ 2018 |
| **No spillover (SUTVA)** | Mercurio did not change the comparison zones | Y_jt = Y_jt(0) for j ≠ Tambopata |
| **Scale** (M4) | The same, after dividing each zone's outcome by its own 2014-18 mean | Y_it / pre_i = α_i + γ_t + ε_it |

## 5. The maths

### 5.1 Master's level

**The model (M1).**

  y_it = α_i + γ_t + β_1·D_i·1[2019-21] + β_2·D_i·1[2022-25] + ε_it

with D_i = 1 for Tambopata only. Because every post year of Tambopata is covered by one of the two dummies:
- the year effects γ_t are estimated from the 14 comparison zones alone;
- Tambopata's own constant α_T is estimated from its pre-years 2014-18 alone.

So β_1 has a closed form:

  β_1 = [ȳ_T(2019-21) − ȳ_T(2014-18)] − [ȳ_C(2019-21) − ȳ_C(2014-18)]

where ȳ_C is the unweighted mean of the 14 comparison zones. It is a 2×2 DiD with a 2014-18 baseline and a 14-zone average as comparison.

**What year effects absorb.** γ_t is the comparison zones' average addition in year t, in hectares. Any shock that changes every zone's addition by the same number of hectares is removed. A shock that changes additions in proportion to size (a high gold price that makes big fronts grow faster) is not.

**Interacted exposure control (M2).** Add θ·pre_i·ln(gold_t), where pre_i is the zone's 2014-18 mean addition. This lets a zone with twice the pre-2019 mining react twice as strongly to a gold-price rise. θ is a single slope shared by all zones.

**Unit-specific trends (M3).** Add δ_i·t for each zone. One trend must be dropped, because the year effects already span one linear trend.

**Scaled outcome (M4).** Replace y_it by y_it / pre_i. A coefficient of −1.45 then means "1.45 normal pre-2019 years of mining fewer per year".

**Inference with one treated unit.** The sampling distribution of β_1 is unknown (Conley and Taber 2011). The ladder uses a **placebo in space**: each comparison zone in turn is "treated", Tambopata is removed from the pool, and Tambopata's β_1 is ranked among the placebo β's. Rank 1 of 15 gives p = 1/15 = 0.067, the smallest attainable.

### 5.2 PhD level

**Frisch-Waugh-Lovell (FWL).** β is the coefficient from regressing the residualised outcome on the residualised treatment dummy, both residualised on all other regressors (fixed effects and covariates). Two consequences matter here.

1. *Binned dummies + a covariate that varies inside the bin.* In M2 the covariate pre_i·ln g_t moves within 2019-21. Its residual is correlated with Tambopata's own within-bin path. The slope θ is then partly fitted to Tambopata's post-treatment outcomes, and β_1 inherits that. Saturating the treated unit's post years (one dummy per year 2019-2025) removes every post observation of Tambopata from the identification of θ: θ is then learnt from the comparison zones and Tambopata's pre-years only. This is the same logic as the referee's C5 point on M3 (Borusyak, Jaravel and Spiess 2024 make the general argument for imputation estimators: fit the untreated model on untreated observations only).
2. *Unit trends.* With δ_T fitted on 2014-25 and binned post dummies, post-period data feed Tambopata's trend. Fitting it on 2014-18 only (saturated dummies) is the imputation version; with five pre-years the extrapolation is very sensitive to single years.

**Leverage and effective comparison.** The 14 comparison zones get equal weight in γ_t, but the covariate slope θ is identified from cross-zone variation in pre_i. When one comparison zone (Amarakaeri) carries most of that variation, θ is effectively Amarakaeri's gold response, extrapolated to a zone 4.7 times larger.

**Scale.** Parallel trends in hectares and in proportional terms cannot both hold unless trends are flat (Roth and Sant'Anna 2023). M4 is the proportional version. The ratio estimator with a signed pre-mean denominator is unstable when a zone's pre-mean is near zero or partly negative.

**Placebo-in-space as randomization inference.** The rank test is exact under a sharp null only if treatment assignment is exchangeable across zones. It is not: Tambopata was chosen because it was the largest front. In hectares, a zone with a pre-mean of 5 ha cannot produce a placebo effect of −1,450 ha, so rank 1 partly measures size (cross-cutting issue X1). Scaling (M4) is the fair version of the test.

## 6. Our example

### 6.1 Variables and code path

| Element | As coded | Where |
|---|---|---|
| Outcome | net annual addition, ha, MapBiomas Peru Col 4 workbook, all department rows summed then differenced | `peru_models.py:46-48` |
| Pool | 15 Peruvian buffer zones with any non-zero addition in 2014-18 (pool B) | `peru_models.py:89` |
| M4 pool | 7 zones with a signed 2014-18 mean > 10 ha | `peru_models.py:90` |
| Treated | Tambopata BZ from 2019 | `peru_models.py:29`, `:94` |
| Post dummies | binned: 2019-21 ("during"), 2022-25 ("after") | `peru_models.py:56`, `:94` |
| M2 covariate | 2014-18 mean addition × ln(annual gold price, nominal USD) | `peru_models.py:57-58`, `:53` |
| M3 trends | one per zone, first non-treated zone dropped | `peru_models.py:59-63` |
| M4 scaling | y / signed 2014-18 mean | `peru_models.py:53-55` |
| Estimator | numpy `lstsq` with explicit dummies; M1, M2 asserted equal to pyfixest | `peru_models.py:69-82` |
| Placebo in time | same model on 2011-18, fake 2016-18; pre-means then from 2011-15 | `peru_models.py:53`, `:100` |
| Placebo in space | each other zone treated, Tambopata removed from its pool | `peru_models.py:103-105` |
| "Amazon" pool | hand-coded list of 8 zones | `peru_models.py:41-43`, `:107-109` |
| m3pre | M3 with saturated post dummies | `peru_models.py:135-141` |

### 6.2 The 15 zones

| Zone | Departments | 2014-18 mean addition (ha) |
|---|---|---|
| Tambopata | Madre de Dios, Puno | 1,594 |
| Amarakaeri | Cusco, Madre de Dios | 342 |
| Allpahuayo Mishana | Loreto | 53 |
| Bahuaja-Sonene | Madre de Dios, Puno | 12 |
| Cotahuasi | Apurímac, Arequipa, Ayacucho, Cusco | 12 |
| Junín | Junín, Pasco | 12 (absolute mean 31) |
| Río Abiseo | La Libertad, San Martín | 11 |
| eight others | various | −4 to +5 |

The 14 comparison zones average 32 ha/yr in 2014-18; Tambopata is 50 times that.

## 7. Tests run and results

### T1 · Reproduce

My independent re-implementation matches `output/numbers.csv` to the decimal.

| Model | 2019-21 | 2022-25 | Fake 2016-18 | Rank in space | Placebo range | ids |
|---|---|---|---|---|---|---|
| M1 | −1,453.6 | +160.7 | +255.0 | 1 of 15 (p 0.067) | −66 to +226 | `model_m1_*` |
| M2 | −1,604.8 | −174.5 | +187.5 | 1 of 15 | −82 to +418 | `model_m2_*`, slope 0.343 `model_m2_gold_slope` |
| M3 | −1,859.0 | −599.3 | −337.4 | 1 of 15 | −68 to +546 | `model_m3_*` |
| M4 | −1.449 | −0.205 | −0.331 | 3 of 7 (p 0.43) | −1.57 to +2.20 | `model_m4_*` |
| m3pre | −2,004.0 | −871.1 | | | | `model_m3pre_*` |

pyfixest gives the same M1 and M2 coefficients.

### T2 · M1 is Tambopata's own before/after, minus a 22 ha drift (lead (a): confirmed)

| | 2014-18 | 2019-21 | Change |
|---|---|---|---|
| Tambopata | 1,594.4 | 162.5 | −1,431.9 |
| Mean of the 14 comparison zones | 32.0 | 53.8 | +21.8 |
| M1 coefficient | | | **−1,453.6** |

The comparison moves by 1.5% of Tambopata's change. Without Amarakaeri the drift is only +5.6 ha; Amarakaeri's own +231.6 ha change makes up 76% of the 14-zone drift. **M1 is, to 98.5%, a before/after comparison of Tambopata.** This is description dressed as a regression; the regression adds the placebo ranking, not a counterfactual.

### T3 · What the year effects absorb (lead (b): confirmed)

M1 year effects (2014 = 0), ha: 2015 −26, 2016 −72, 2017 +50, 2018 −18, 2019 +7, 2020 +22, 2021 −3, 2022 −21, **2023 +230**, 2024 −19, 2025 +53.

- The 2019-21 mean minus the 2014-18 mean is **+21.8 ha**. That is everything the year effects "remove" from Tambopata's 1,432 ha fall.
- The year effects correlate weakly with ln(gold) in levels (r = 0.33, slope 77 ha per log-point) and not at all in first differences (r = −0.04).
- The gold price rose by 0.35 log-points from 2018 to 2021. In a zone with Tambopata's pre-2019 size, a proportional response would be hundreds of hectares, not 22.

**So "year effects absorb the gold price and COVID" is not true for Tambopata in hectares.** They absorb the hectare change of zones that average 32 ha/yr. The sentence appears in `peru_models.py:7-8` (docstring), `:33` (model label written into every `model_m1_*` description), `peru_context_models.py:6-7`, `brief_content.md:27` and `:39`, `explainer_content.md:377`, `:379`, `:389`, `:542`, `methods_content.md:137` (cross-cutting X10). M2 is the model that tries to handle the proportional part, which makes T4 important.

### T4 · Binned vs saturated post dummies (lead (c): confirmed, and the mechanism is worse than reported)

Tambopata's post years binned (as coded) vs one dummy per post year 2019-2025 (gap = mean of the 2019-21 dummies):

| Model | Binned | Saturated | Saturated 2019 / 2020 / 2021 |
|---|---|---|---|
| M1 | −1,453.6 | −1,453.6 | −1,179 / −1,448 / −1,735 |
| M2 | −1,604.8 (slope 0.343) | **−2,508.1 (slope 2.396)** | −1,614 / −2,781 / −3,130 |
| M3 | −1,859.0 | −2,004.0 (= m3pre) | −1,592 / −1,998 / −2,423 |
| M4 | −1.449 | −1.449 | −0.7 / −1.9 / −1.7 |

- M1 and M4 have no covariate, so binning changes nothing.
- In M2 the binned slope (0.34) is pulled down because Tambopata's additions fell inside 2019-21 (417 → 181 → −111) while ln(gold) rose (7.24 → 7.48 → 7.50). The saturated slope (2.40) is almost exactly the slope from the 14 comparison zones alone (2.43).
- **New:** that comparison-only slope comes from Amarakaeri. Without Amarakaeri, the 13 remaining comparison zones give a slope of **−4.89** (the opposite sign). Amarakaeri is the only comparison zone with a pre-mean above 53 ha (342 ha).
- The saturated M2 counterfactual adds 2.40 × (1,594 − 32) × 0.282 = **1,054 ha/yr** of "expected gold-driven growth" to Tambopata in 2019-21 (binned: 151 ha/yr). That is Amarakaeri's 2019-21 growth, scaled up 4.7 times to Tambopata's size.
- **X12 applies directly.** Amarakaeri's mined land is 58% legal corridor and 41% native communities (S2 T6b), and it rose in 2019-21 when displaced miners were most likely to arrive. If part of its rise is spillover from Mercurio, the saturated M2 converts displacement into "gold response" and pushes the gap away from zero.
- Saturated M2 without Amarakaeri: slope 0.75, gap −1,772.5.
- Both saturated M2 and M3 still rank 1 of 15 in space (placebo ranges −82 to +597 and −84 to +560).
- Tambopata's own 2014-18 trend is +133 ha/yr per year; m3pre extrapolates that rising line into 2019-21, which is why it is more negative than binned M3.

### T5 · Leave one comparison zone out (lead (d): confirmed)

| Dropped | M1 | M2 | M3 | M2 saturated | M3 saturated |
|---|---|---|---|---|---|
| Amarakaeri | −1,437 | **−1,401** | −1,820 | **−1,773** | −1,964 |
| any other single zone | −1,452 to −1,458 | −1,602 to −1,615 | −1,859 to −1,864 | −2,499 to −2,551 | −2,004 to −2,010 |

Only Amarakaeri matters. Dropping it moves M2 from −1,605 to −1,401 (binned) and from −2,508 to −1,773 (saturated).

M4 leave-one-out (6 zones each): Tambopata ranks **2 or 3 of 6** in every case (gap −1.08 to −1.71). Never rank 1.

### T6 · Fake-date windows (lead (e): confirmed; M3's placebo is window-dependent)

Each run uses only data up to 2018.

| Sample, fake window | M1 | M2 | M3 | M4 |
|---|---|---|---|---|
| 2011-18, fake 2016-18 (as coded) | +255 | +187 | −337 | −0.33 |
| 2011-18, fake 2014-15 | +51 | −101 | +51 | +0.05 |
| 2008-18, fake 2013-15 | +574 | +528 | +349 | +0.05 |
| 2008-18, fake 2011-13 | +218 | −393 | +473 | +0.49 |
| 2011-18, fake 2017-18 | +836 | +828 | +1,131 | +0.04 |
| 2014-18, fake 2017-18 | +860 | +955 | +2,066 | −0.23 |

- The coded fake window 2016-18 contains the 2017-18 operations (agent.md §10), so it is not a clean placebo.
- Most fakes are **positive**: before 2019 Tambopata was rising faster than the comparison (consistent with S2 T3).
- M3's single "weak fail" (−337) is not robust: across windows M3's fake ranges from −337 to +2,066. Unit trends fitted on few years are unstable.
- In the fake runs, M2 and M4 use 2011-15 means as the size measure (`peru_models.py:53`); Amarakaeri's is 547 ha there against 342 ha in 2014-18, and Río Abiseo's 5 against 11. Real and fake M4 are on different scales.

### T7 · M4 denominators (lead (f): confirmed; M4's verdict is robust)

| Denominator | Tambopata | Rank |
|---|---|---|
| Signed 2014-18 mean (as coded) | −1.45 | 3 of 7 |
| Absolute 2014-18 mean (Junín 31.1 instead of 11.7) | −1.52 | 2 of 7 |
| Signed 2016-18 mean | −1.41 | 2 of 7 |

M4 placebo effects (as coded): Allpahuayo −1.57, Junín −1.49, Río Abiseo −0.58, Amarakaeri +0.15, Cotahuasi +1.29, Bahuaja +2.20. Two small zones (52 and 12 ha/yr) fall as much, relative to their size. **Relative to size, Tambopata's fall is ordinary: rank 2-3 in every variant (T5, T7).**

### T8 · Full rank (lead (g): confirmed)

Every design matrix has full column rank: M1 28/28, M2 29/29, M3 42/42, M4 20/20; saturated versions 33, 34, 47, 25; M3 fake 37/37. numpy `lstsq` returns the unique OLS solution.

### T9 · The hand-coded "Amazon" pool (lead (h): confirmed, no effect on results)

`AMAZON` (`peru_models.py:41-43`) is a typed list with no rule. Río Abiseo (La Libertad, San Martín) is excluded although San Martín is an Amazon-biome department; Junín (Junín, Pasco) too. Adding Río Abiseo: M1 rank 1 of 9 (was 1 of 8), M4 rank 2 of 5 (was 2 of 4). The result does not change, but the pool should come from one shared rule (X7).

### T10 · Honest range of the 2019-21 gap (ha/yr)

| Specification | Gap | Comment |
|---|---|---|
| Tambopata's own before/after (2014-18 → 2019-21) | −1,432 | no comparison at all |
| M1 without Amarakaeri | −1,438 | |
| M2 binned without Amarakaeri | −1,401 | |
| M1 (published) | −1,454 | = before/after − 22 |
| M2 binned (published) | −1,605 | slope fitted partly on Tambopata's post path |
| 2×2 vs Amarakaeri, 2016-18 base (S2) | −1,762 | |
| M2 saturated without Amarakaeri | −1,773 | |
| M3 binned (published, upper end of brief's [C] range) | −1,859 | trend fitted partly on post data |
| M3 saturated (m3pre, published) | −2,004 | extrapolates a pre-trend of +133 ha/yr per year |
| M2 saturated | −2,508 | gold slope = Amarakaeri's response × 4.7 |

**The TWFE family spans about −1,400 to −2,500 ha/yr.** The low end is essentially Tambopata's own before/after. Everything more negative than about −1,450 comes from one of two extrapolations: Tambopata's own 2014-18 trend (M3) or Amarakaeri's 2019-21 growth projected onto Tambopata's size (M2). Relative to size (M4), the fall is not unusual.

### Tests not possible here

None. All inputs (`data/peru_bufferzone_year.csv`, `data/prices_annual.csv`) are in the repo.

## 8. Assumption check

| Assumption | Verdict | Evidence |
|---|---|---|
| Additive separability / parallel trends in ha | **Not credible for Tambopata** | Comparison zones average 32 ha/yr vs 1,594; year effects move by 22 ha (T2, T3); pre-2019 fakes mostly positive (T6) |
| M2 gold-response model | **Identified from one zone** | Slope 2.43 from controls comes from Amarakaeri; −4.89 without it (T4) |
| M3 trends would have continued | **Weak** | Five pre-years; fake placebo −337 to +2,066 by window (T6) |
| Covariates not affected by treatment | Holds for pre_i and gold; **violated in practice** for M2 via Amarakaeri's post-2019 growth (spillover enters the slope) | T4, X12 |
| No anticipation | Unclear | 2017-18 operations inside the pre-period and the fake window |
| No spillover | **Likely violated** | Amarakaeri = corridor + communities, rising 2019-21 (S2, X12) |
| Scale (M4) | Plausible, and the verdict is stable | rank 2-3 of 6-7 in every variant (T5, T7) |
| Full rank / estimator correct | Holds | T1, T8 |

## 9. Weaknesses, ranked

1. **The regression adds almost nothing to the before/after.** M1 = −1,432 − 22. The "comparison" is 14 zones whose average barely moves (T2).
2. **"Year effects absorb the gold price and COVID" is false in hectares** and appears in the brief, the walkthrough, the methods page and the code (T3).
3. **M2's slope is either contaminated by Tambopata's post path (binned) or by Amarakaeri's possibly displaced growth (saturated).** The two give −1,605 and −2,508 (T4). Neither is a clean gold control.
4. **Rank 1 of 15 in hectares mostly measures size** (X1): relative to size Tambopata ranks 2-3 in every variant.
5. **Placebo in time sits on top of the 2017-18 operations** and depends on the window (T6).
6. **The quoted ladder (−1,454 to −1,859) understates the specification range** (−1,401 to −2,508) and stops at a binned M3 that the code itself flags as contaminated (`peru_models.py:133-134`).
7. Minor: hand-coded Amazon list (T9), signed denominators (T7), fake-run denominators from a different window (T6).

## 10. Proposed decisions

| # | Decision | Recommendation |
|---|---|---|
| D-S4-1 | Wording on year effects | Delete "absorbing the gold price and COVID" everywhere it appears (list in T3). Replace with: "year effects remove what changed in the average comparison zone (+22 ha/yr); they cannot remove shocks that scale with a zone's size". Fix the model label in `peru_models.py:33` and the docstring `:7-8`. |
| D-S4-2 | How to present M1 | Say plainly: "M1 is close to Tambopata's own before/after (−1,432 of −1,454 ha/yr), because the comparison zones hold little mining". Label **description**. |
| D-S4-3 | M2 | Report binned and saturated together (−1,605 / −2,508), with the note that the slope is Amarakaeri's response. Do not let M2 set either end of a [C] range. If kept, switch the code to saturated dummies (as already done for M3) and add the no-Amarakaeri version (−1,773). |
| D-S4-4 | M3 | Replace binned M3 by m3pre (−2,004) as the trend variant; report the fake-window range (−337 to +2,066) instead of the single −337. |
| D-S4-5 | M4 | Keep as the decisive fair test: rank 3 of 7 (2 of 7 with absolute denominators; 2-3 of 6 leave-one-out). Use absolute or 2014-18 positive-only denominators with a stated rule. |
| D-S4-6 | Range in the brief | Do not quote "−1,454 to −1,859" as the ladder's range. Quote the TWFE family as "about −1,400 to −2,500 ha/yr in hectares; ordinary relative to size". Leave the [C] range itself to S14. |
| D-S4-7 | Fake dates | Use fake windows that end before 2017 (e.g. 2014-15 on 2011-15 data), and show several (T6), as S2/S3 do. |
| D-S4-8 | Pools | One shared rule for the "Amazon" pool across `peru.py`, `peru_robust.py`, `peru_models.py` (X7). |

## 11. Verdict

The ladder is coded correctly: every number reproduces, every matrix is full rank, and pyfixest agrees. But **the regressions are not more informative than Tambopata's own before/after**. With 14 comparison zones that average 32 ha/yr, the year effects shift Tambopata's counterfactual by 22 ha. Everything beyond that comes from extrapolations: Tambopata's own rising pre-trend (M3) or Amarakaeri's gold response scaled up 4.7 times (M2), and Amarakaeri is a corridor-and-community zone that may have received displaced miners (X12). Relative to size, the fall ranks 2-3 of 6-7.

Label: **description**.

Wording the brief may use: "Tambopata's net additions fell by about 1,430 ha/yr from 2014-18 to 2019-21, while 14 other Peruvian buffer zones together barely changed (+22 ha/yr on average). With zone and year effects and different controls, the gap ranges from about −1,400 to −2,500 ha/yr (the upper end relies on slopes or trends that S14 does not accept as range ends) and is the largest of the 15 zones in hectares, as it was in 2014-16 too; relative to each zone's size it is not unusual (rank 3 of 7) [D]."

Wording the brief must not use: "year effects absorb the gold price and COVID"; "the model ladder (−1,454 to −1,859) bounds the effect"; "controls for the gold price" without saying how the slope is identified.

## References

- Angrist, J. and Pischke, J.-S. (2009). *Mostly Harmless Econometrics*. Princeton University Press, ch. 5.
- Borusyak, K., Jaravel, X. and Spiess, J. (2024). Revisiting event-study designs: robust and efficient estimation. *Review of Economic Studies* 91(6).
- Conley, T. and Taber, C. (2011). Inference with "difference in differences" with a small number of policy changes. *Review of Economics and Statistics* 93(1).
- Frisch, R. and Waugh, F. (1933). Partial time regressions as compared with individual trends. *Econometrica* 1(4). Lovell, M. (1963). Seasonal adjustment of economic time series. *JASA* 58(304).
- Roth, J. and Sant'Anna, P. (2023). When is parallel trends sensitive to functional form? *Econometrica* 91(2).
- Wooldridge, J. (2010). *Econometric Analysis of Cross Section and Panel Data*, 2nd ed. MIT Press, ch. 10.
