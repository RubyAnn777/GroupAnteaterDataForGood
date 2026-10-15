# S3 · Event study and placebo inference (attempt A2)

*Method card 3 of the causal review (plan: `docs/causal_review_plan.md`). Code under review: `code/peru.py:129-297` (event study, placebo in space, restricted placebo, figure), `code/common.py:55-61` (`placebo_rank`), `code/peru_robust.py:124-149` (Amazon pool). Test script: `code/review/s3_event_study_checks.py` (read-only).*

---

## 1. In one sentence

An event study runs a difference in differences separately for every year around the treatment date, so you can see whether the treated unit was already drifting before the treatment (leads) and how the gap evolves after it (lags); placebo inference then asks whether a gap that large would also appear if an untreated unit, or an untreated year, were labelled "treated".

## 2. Simple version

Take the ice-cream shops from the S2 card. Instead of one before/after number, plot for every year how far shop T's sales sit from the other shops' average, minus that same distance in the reference year (the year before the new competitor arrived). Before the competitor, the line should hover around zero. After it, the line shows the effect, year by year.

With one treated shop there is no textbook standard error. So you play a game instead: pretend each of the other shops got the competitor, compute the same line for each, and see where the real shop ranks. If the real shop's drop is bigger than every pretend drop, you say "rank 1 of 15".

The catch: the game is only fair if the shops are alike. If shop T is ten times bigger than every other shop, its line will swing ten times more in every year, before the competitor too. Then "rank 1" tells you shop T is big, not that the competitor did anything. The way to see this is to play the same game in a year *before* the competitor. If shop T also ranks 1 there, the game is measuring size.

## 3. When to use it, and when not

**Use it when:**
- treatment starts at a known date and you have several years before and after;
- you want to show dynamics (does the effect build up, fade, reverse?);
- you want a visual pre-trend check;
- there are many treated units (sampling inference), or one treated unit and many similar untreated ones (placebo inference).

**Be careful or avoid it when:**
- the single treated unit is much larger or more volatile than every placebo unit: placebo ranks then measure scale (the exchangeability problem);
- the reference year is unusual: every coefficient inherits its noise;
- pre-period coefficients are themselves large: "no pre-trend" cannot be claimed, and a test that fails to reject has little power (Roth 2022);
- treatment timing is staggered and effects vary over time: two-way fixed effects event studies then mix cohorts (Sun and Abraham 2021). Not our case: one treated unit, one date.

## 4. Assumptions

| Assumption | In words | Formally |
|---|---|---|
| **Parallel trends (all years)** | Without treatment, the treated unit's gap to the controls would have stayed at its reference-year level | E[Y_T,t(0) − Ȳ_C,t(0)] − E[Y_T,ref(0) − Ȳ_C,ref(0)] = 0 for all t |
| **No anticipation** | Leads are zero because nothing happened yet | β_k = 0 for k < first treated year, if parallel trends holds |
| **No spillover (SUTVA)** | Controls are untouched by the treatment | Ȳ_C,t = Ȳ_C,t(0) |
| **Reference period is typical** | The omitted year is not itself a shock | gap_ref ≈ long-run pre-period gap |
| **Exchangeability (placebo inference)** | Under the null of no effect, the treated unit's statistic has the same distribution as each placebo unit's | (S_T, S_1, ..., S_J) exchangeable under H0 |
| **Comparable pool** | Placebo units could plausibly have been treated: same kind of mining, same kind of place | design choice, not testable |

## 5. The maths

### 5.1 Master's level

**Estimator.** With units i, years t, a treated indicator T_i and reference year r:

  y_it = α_i + γ_t + Σ_{k ≠ r} β_k · (T_i × 1[t = k]) + ε_it

β_k is the year-k gap between treated and controls minus the same gap in year r. With **one** treated unit and an equal-weight control mean, the regression has a closed form:

  β_k = (y_T,k − ȳ_C,k) − (y_T,r − ȳ_C,r)

Each β_k is a 2×2 DiD with the single years k and r as "after" and "before". The coefficients for k < r are **leads** (pre-trend check). The coefficients for k ≥ first treated year are **lags** (dynamic effects).

**Summary statistic.** A post-period mean such as θ = mean(β_2019, β_2020, β_2021).

**Placebo in space (Fisher randomization inference).** Treat each control j in turn, using the other controls as its comparison, and compute S_j the same way. Under the sharp null (no effect anywhere) and exchangeability, the real unit's rank is uniform. The one-sided p-value is

  p = rank / n,   rank = 1 + #{j : S_j ≤ S_T}

With n units the smallest attainable p is **1/n**: 0.067 with 15 units, 0.167 with 6, 0.33 with 3.

**Placebo in time.** Keep the real unit but move the treatment date to fake years before the real one. This tests "is 2019 special for this unit" and avoids cross-unit comparability, but the fake windows must end before the real date.

### 5.2 PhD level

**Why the reference year matters.** Every β_k subtracts the same gap_r. A noisy reference year shifts all coefficients by the same amount. Pooling the reference over several years (r ∈ R, subtracting mean gap_R) reduces this noise at the cost of assuming a flat pre-trend inside R. Freyaldenhoven, Hansen and Shapiro (2019) discuss normalisation choices.

**Pre-trend tests have low power and distort inference.** Roth (2022) shows that conditioning on "passing" a pre-trend test can make the post-period bias *worse*, and that typical tests have low power against linear violations. A non-significant pre-test is not evidence of parallel trends.

**Honest bounds (Rambachan and Roth 2023).** Instead of assuming the post-period violation of parallel trends δ_post is zero, bound it by the pre-period violations. Under **relative magnitudes** Δ^RM(M̄):

  |δ_{t+1} − δ_t| ≤ M̄ · max_{s < r} |δ_{s+1} − δ_s|   for post-period t

So the post-period trend violation may move each year by up to M̄ times the largest year-to-year swing seen before treatment. The worst-case bias in post year k (k = 1, 2, 3) is k · M̄ · max_pre_step, and the identified set for a three-year mean is θ̂ ± 2 · M̄ · max_pre_step. The **breakdown value** M̄* is the smallest M̄ at which the set includes zero. The full method adds sampling uncertainty; with one treated unit we can only compute the identified set at the point estimates.

**Exchangeability and heteroskedasticity.** Placebo-in-space inference (Abadie, Diamond and Hainmueller 2010) is exact only if the units are exchangeable under the null. If the treated unit's outcome variance is larger than the placebos', the raw-statistic test over-rejects. Ferman and Pinto (2019) and MacKinnon and Webb (2020) show this for DiD with few treated groups. Remedies:
- normalise the statistic by unit scale: divide by the unit's own pre-period level, or by its pre-period standard deviation (a studentised statistic);
- use the ratio of post-period to pre-period mean squared prediction error (MSPE), as ADH (2010) do for synthetic control (Firpo and Possebom 2018 discuss its properties);
- restrict the pool to units with similar scale and variance.

**A consistency check that any placebo test must pass.** Apply the same statistic to **pre-period** years. If the treated unit already ranks first before treatment, then either the test is not valid for this unit (non-exchangeable) or parallel trends already fails. In both cases a post-period rank 1 is not evidence of an effect on its own.

## 6. Our example

### 6.1 Specification as coded

| Element | As coded | Where |
|---|---|---|
| Outcome | net annual addition (ha), MapBiomas Peru Col 4 workbook, buffer zone summed over all department rows | `peru.py:153-156` |
| Years | 2014-2025, reference 2018 omitted | `peru.py:28, 133` |
| Treated | Tambopata buffer zone; first treated year 2019 (decision S0) | `peru.py:166` |
| Pool A (main line) | zones with any row in Madre de Dios and nonzero 2014-18 additions: Tambopata, Amarakaeri, Bahuaja-Sonene | `peru.py:160-162` |
| Pool B (placebo pool) | all 15 Peruvian buffer zones with any 2014-18 change, any department | `peru.py:165` |
| Estimator | `pf.feols(y ~ d2014..d2025 | unit + year)`, CRV1 by unit; asserted equal to the closed form | `peru.py:137-150, 175-176` |
| Placebo in space | each non-Tambopata pool-B zone treated in turn against the other 13; statistic = mean β 2019-21 | `peru.py:180-199` |
| Scaled placebo | same statistic divided by the zone's own 2014-18 mean addition | `peru.py:187-197` |
| Restricted placebo | department-row filter (16 Amazon-biome departments) + pre mean > 10 ha/yr: 6 zones | `peru.py:268-294` |
| Rank rule | 1 + number of placebos at least as negative | `common.py:55-61` |
| Figure | pool A line (orange), pool B line (grey), pool B placebo band | `peru.py:229-265` |

### 6.2 Data lineage

Same as S1/S2: `data/peru_bufferzone_year.csv` (MapBiomas Peru Col 4, class 4.2 Minería) → sum rows by `buffer_zone|pa_category` and year → `diff()` → wide table, one column per zone. No other inputs. The restricted pool first drops rows in departments without an Amazonía row in `peru_department_year.csv`, then sums and differences.

## 7. Tests run and results

### T1 · Reproduce

- Pools reproduce: pool A = Amarakaeri, Bahuaja-Sonene, Tambopata; pool B = 15 zones.
- pyfixest equals the closed form; every registered `eventstudy_beta_poolA_*`, `eventstudy_beta_poolB_*` and `eventstudy_pretrend_poolA_2016` matches.
- **Bahuaja-Sonene enters pool A through a 145-ha Madre de Dios row that has 0 ha of mining.** All its mining (80 ha in 2018) is in the Puno row. Audit lead 1 confirmed.
- The CRV1 standard errors in `peru_event_study.csv` come from 3 clusters. They are correctly labelled "not informative" and are not used anywhere.

### T2 · Coefficients by year (reference 2018, ha/yr)

| Year | Tambopata addition | Pool A control mean | β pool A | β pool B | Placebo band (pool B) |
|---|---|---|---|---|---|
| 2014 | 1,590 | 276 | −404 | −198 | −61 to +493 |
| 2015 | 1,463 | 158 | −412 | −306 | −114 to +254 |
| **2016** | 707 | 185 | **−1,195** | **−1,066** | −67 to +314 |
| 2017 | 2,455 | 228 | +509 | +675 | −72 to +403 |
| 2018 | 1,757 | 39 | 0 | 0 | 0 |
| 2019 | 417 | 151 | −1,451 | −1,358 | −67 to +236 |
| 2020 | 181 | 410 | −1,946 | −1,626 | −96 to +718 |
| 2021 | −111 | 362 | −2,191 | −1,914 | −158 to +602 |
| 2022 | 580 | 585 | −1,722 | −1,269 | −184 to +1,012 |
| 2023 | 3,565 | 1,072 | +775 | +1,660 | −209 to +2,043 |
| 2024 | 1,276 | 391 | −833 | −525 | −330 to +691 |
| 2025 | 1,896 | 547 | −369 | +61 | −269 to +869 |

Registered ids: `eventstudy_beta_poolA_2019..2025`, `eventstudy_beta_poolB_2019..2025`, `eventstudy_pretrend_poolA_2014..2017`, `eventstudy_band_min/max_{2016,2019,2023,2024,2025}`. The 2014, 2015, 2017 and 2020-22 band edges come from the test script (they are in `output/peru_event_study.csv` but not registered).

The pre-period coefficients are not small. The 2016 lead (−1,195) is 64% of the post-period mean (−1,863), and 2017 swings the other way (+509).

### T3 · Rank 1 also fires before 2019 (audit lead 3, confirmed)

Same placebo loop as `peru.py:180-199`, but applied to each single year and to pre-period statistics. Pool B, n = 15.

| Statistic | Tambopata | Placebo range | Rank one-sided (most negative) | Rank two-sided (largest size) |
|---|---|---|---|---|
| β 2014 | −198 | −61 to +493 | **1** | 2 |
| β 2015 | −306 | −114 to +254 | **1** | **1** |
| β 2016 | −1,066 | −67 to +314 | **1** | **1** |
| β 2017 | +675 | −72 to +403 | 15 | **1** |
| β 2019 | −1,358 | −67 to +236 | 1 | 1 |
| β 2020 | −1,626 | −96 to +718 | 1 | 1 |
| β 2021 | −1,914 | −158 to +602 | 1 | 1 |
| β 2022 | −1,269 | −184 to +1,012 | 1 | 1 |
| β 2024 | −525 | −330 to +691 | 1 | 2 |
| β 2025 | +61 | −269 to +869 | 13 | 13 |
| **mean 2019-21 (headline)** | −1,633 | −91 to +519 | **1** | 1 |
| mean 2015-17 (fake post) | −232 | −84 to +324 | **1** | 2 |
| mean absolute pre β 2014-17 | 561 | 12 to 366 | **1 (most volatile)** | |

**In every pre-period year Tambopata is the most extreme zone, in one direction or the other.** The raw-hectare placebo test "rejects" in years when nothing had happened yet. This is what the test does when one unit is far larger than the rest:

| Zone | Mean addition 2014-18 (ha/yr) | SD 2014-18 |
|---|---|---|
| Tambopata | 1,594 | 627 |
| Amarakaeri | 342 | 185 |
| Allpahuayo Mishana | 52 | 24 |
| all other 12 zones | ≤ 12 | ≤ 42 |

**Conclusion (description):** `placebo_space_rank_raw` = 1 of 15 measures that Tambopata is the biggest and most volatile zone. It is not, on its own, evidence that 2019-21 is unusual. Cross-cutting issue X1 is confirmed.

### T4 · Reference period (audit lead 4, confirmed)

Mean 2019-21 coefficient by reference period:

| Reference | Pool A | Pool B | Rank in pool B | Pool A, 2022-25 |
|---|---|---|---|---|
| **2018 (as coded)** | **−1,863** | **−1,633** | 1/15 | −537 |
| 2017-18 | −2,117 | −1,970 | 1/15 | −792 |
| 2016-18 | −1,634 | −1,502 | 1/15 | −308 |
| 2014-18 | −1,562 | −1,454 | 1/15 | −237 |
| 2015-17 | −1,497 | −1,400 | 1/15 | −171 |
| 2017 only | −2,372 | −2,307 | 1/15 | −1,046 |

- 2018 is an unusual reference: Tambopata's gap to the controls is wide (Tambopata 1,757, Amarakaeri 54, its lowest year by far; 301-542 in 2014-17). So ref 2018 inflates the effect by about 300 ha/yr compared with a 2014-18 reference.
- The single-year reference choice alone moves the mean 2019-21 coefficient from −1,497 to −2,372.
- The 2022-25 coefficient moves from −1,046 to −171. "Tambopata stayed below the comparison in 2022-25" depends on the reference year.

### T5 · Scale-free statistics (audit lead 2)

| Statistic | Pool B (15) | Restricted, as coded (6) | `peru_models` AMAZON (8) | Lowland with ≥ 50 ha stock (5) |
|---|---|---|---|---|
| raw mean β 2019-21 (ha) | **1**/15 | 1/6 | 1/8 | 1/5 |
| ÷ own 2014-18 mean (as registered) | **10/11** | 5/6 | 5/6 | 3/4 |
| ÷ SD of own pre β (studentised) | 9/15 | 5/6 | 7/8 | 4/5 |
| post/pre MSPE ratio (ADH 2010) | **1/15** | 1/6 | 1/8 | 1/5 |

Notes:
- `placebo_space_rank_scaled` = 10 is registered with n = 15, but 4 zones have a pre mean ≤ 0 and drop out (NaN never counts in `placebo_rank`), so the real denominator is **11**. The registered description says "among 15". Under the scaled statistic Tambopata's fall (−1.02 times its own pre mean) is ordinary: tiny zones fall by 2 to 56 times their pre mean because their pre mean is near zero. This statistic is unstable for the opposite reason to the raw one.
- The studentised statistic puts Tambopata at 9 of 15 in pool B: its post fall is 2.3 SDs of its own pre-period coefficients, while several tiny zones move 4-5 SDs.
- The MSPE ratio is the one scale-free statistic that keeps Tambopata at rank 1 in every pool (p = 1/n). But it is fragile: dropping Amarakaeri from the AMAZON pool moves it to 3 of 7.
- **Scale-free inference does not give one answer.** Rank 1 under the MSPE ratio, middle of the pack under the two normalised-mean statistics. Combined with T3, the placebo-in-space evidence for an unusual 2019-21 fall is weak.

### T6 · One list of comparable zones (audit lead 5, confirmed)

Three modules use three "Amazon" definitions:

| Module | Rule | Zones (besides Tambopata) |
|---|---|---|
| `peru.py:268-294` (restricted placebo) | rows in the 16 Amazon-biome departments, pre mean > 10 ha/yr | Allpahuayo Mishana, Amarakaeri, Bahuaja-Sonene, **de Junín, del Río Abiseo** |
| `peru_robust.py:124-130` | rows in the 16 Amazon-biome departments, any nonzero 2014-18 change | 12 zones |
| `peru_models.py:39-43` (`AMAZON`) | named list, drops coastal and high-Andean zones including Junín and Río Abiseo | Amarakaeri, Bahuaja-Sonene, Allpahuayo Mishana, Cordillera Azul, Alto Mayo, Pacaya-Samiria, El Sira |

The department-row filter does not remove Andean mining. Junín's mining sits entirely in its Pasco row (148 ha in 2018) and Río Abiseo's entirely in its La Libertad row (223 ha); both departments count as "Amazon" only because they also contain some Amazon-biome land. `peru_models.py` itself labels both zones high-Andean.

**Proposal:** one shared list, `peru_models.AMAZON` (8 lowland zones), moved to `common.py` and used by all three modules. For a robustness pool, the subset with at least 50 ha mined by 2018: Tambopata, Amarakaeri, Allpahuayo Mishana, Bahuaja-Sonene, Cordillera Azul (5 zones; smallest attainable p = 0.20). Results under both lists are in T5: rank 1 in raw hectares and in MSPE ratio, rank 5 of 6 or 3 of 4 when scaled. The 2016 coefficient is again rank 1 in both (AMAZON 8: −1,089 vs placebos −66 to +313; lowland 5: −1,120 vs −117 to +317), so T3's warning applies unchanged.

Not verified here: whether every zone on the list has *alluvial gold* mining. The data only say "mining class 4.2"; Allpahuayo Mishana (Loreto, 421 ha) and Cordillera Azul (San Martín, 78 ha) would need a source before calling them "comparable alluvial-gold zones".

### T7 · Relative-magnitude bounds (approximation of Rambachan and Roth 2023)

Computed at the point estimates; there is no sampling uncertainty to add with one treated unit, so this is the identified set under Δ^RM(M̄), not a confidence set.

| Pool | Pre-period year-to-year steps in β (ha) | Largest step | θ = mean β 2019-21 | Breakdown M̄* (θ) | M̄* (2019 alone) | Set at M̄ = 1 |
|---|---|---|---|---|---|---|
| A | 9, 783, 1,704, 509 | 1,704 | −1,863 | **0.55** | 0.85 | −5,270 to +1,545 |
| B | 108, 760, 1,741, 675 | 1,741 | −1,633 | **0.47** | 0.78 | −5,114 to +1,849 |
| AMAZON 8 | 101, 756, 1,734, 646 | 1,734 | −1,674 | **0.48** | 0.80 | −5,143 to +1,795 |

Reading: if the post-2018 drift of Tambopata relative to the controls could move each year by half of the largest swing seen in 2014-18, the 2019-21 fall is no longer distinguishable from zero. The largest swing is the 2016 dip and 2017 rebound. Excluding steps that touch 2016, the largest step is 509-675 ha and M̄* rises to 1.2-1.8. So the honest-bounds verdict depends on whether the 2016 dip is treated as a one-off. The S1 card shows the dip in both products (workbook 707 ha, raster zones 356 ha), so it is not a workbook artefact; the conservative reading is M̄* ≈ 0.5.

Simpler version of the same point: the largest absolute pre-period coefficient (1,195 in pool A) is 64% of the post-period mean.

### T8 · What pool A's control mean is made of (audit lead 8)

| Year | 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Amarakaeri | 542 | 301 | 362 | 452 | 54 | 291 | 772 | 658 | 1,086 | 2,099 | 740 | 938 |
| Bahuaja-Sonene | 10 | 14 | 8 | 5 | 25 | 10 | 48 | 66 | 83 | 45 | 43 | 157 |
| Amarakaeri share of the control mean | 98% | 96% | 98% | 99% | 68% | 97% | 94% | 91% | 93% | 98% | 95% | 86% |

| Control used | Mean β 2019-21 | β 2016 | Mean β 2022-25 |
|---|---|---|---|
| none (Tambopata vs its own 2018) | −1,594 | −1,050 | +72 |
| Bahuaja-Sonene only | −1,611 | −1,032 | +15 |
| Amarakaeri only | −2,114 | −1,358 | −1,089 |
| **pool A (equal weight)** | **−1,863** | −1,195 | −537 |

- Bahuaja-Sonene is a zero control: using it alone gives Tambopata's own before/after.
- Pool A's estimate is therefore **Tambopata's own change minus half of Amarakaeri's change**. The equal weight halves the main comparison and adds a near-zero series.
- With the S2 fact (X12): Amarakaeri BZ's mined land is 58% legal corridor and 41% native communities. So pool A's comparison is half of a mostly legal-corridor series, which is also a likely destination of displaced miners (spillover, bias away from zero).
- All the "persistence" in pool A (−537 in 2022-25) comes from Amarakaeri's growth: Tambopata's own 2022-25 change against 2018 is +72.

### T9 · The figure (audit lead 6, confirmed)

- The orange line is pool A (3 zones); the grey band is pool B's placebos (`peru.py:233-236`). A pool-A band would have only 2 placebo lines (Amarakaeri +503, Bahuaja −503 for mean 2019-21), so the code borrows pool B's band. The line and the band therefore come from different comparisons.
- The headline is "Tambopata dropped below every placebo zone in 2019–22, then came back" (`peru.py:230`), and the walkthrough caption says "Tambopata drops below the whole band in 2019–22" (`docs/overnight/explainer_content.md:502`). In fact the pool-A line is below the band minimum in **2014, 2015, 2016, 2019, 2020, 2021, 2022, 2024 and 2025**: 9 of 11 non-reference years, including three of the four pre-years. The figure itself shows that being below the band is normal for Tambopata.
- "Then came back" invites the reading "enforcement ended and mining returned". Under decision S0, 2022-25 are "later years", not "after enforcement".

### T10 · Placebo in time on the event-study statistic

Tambopata's own pool-B gap; statistic at a fake start s = mean gap s..s+2 minus gap s−1 (the same statistic as the headline, at a fake date; all fake windows end by 2018).

| Fake start | 2003 | 2004 | 2005 | 2006 | 2007 | 2008 | 2009 | 2010 | 2011 | 2012 | 2013 | 2014 | 2015 | 2016 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Statistic (ha) | −15 | −83 | +33 | +43 | +74 | +173 | +501 | +842 | +858 | −222 | +828 | −381 | −34 | +175 |

- Real −1,633: **rank 1 of 15** (p = 0.067). With a pooled 2014-18 reference (fakes use the five preceding years): fakes −34 to +1,149, real −1,454, rank 1 of 15.
- This test compares Tambopata with itself, so it does not suffer from the scale problem in T3. It is the stronger of the two placebo tests, and it agrees with the S2 placebo-in-time result.
- Its limits: fake dates are exchangeable with 2019 only if nothing else made 2019-21 special. COVID-19 (2020) breaks this (X3), and 2017-18 operations sit inside the last fake windows.

### Tests not possible here

- Full Rambachan-Roth with sampling uncertainty (HonestDiD): needs a covariance matrix for β, which one treated unit cannot provide.
- Event study on first-time mining at zone level with the same placebo pool: the raster zone table covers the 12 Madre de Dios zones only, not the 15 Peruvian buffer zones.

## 8. Assumption check

| Assumption | Verdict | Evidence |
|---|---|---|
| Parallel trends (pre-period) | **Not supported** | β 2016 = −1,195 and β 2017 = +509 (T2); pre-period coefficients are outside the placebo band in 3 of 4 years (T3, T9) |
| No anticipation | Unclear | 2017-18 operations sit in the leads (S0, S1) |
| No spillover | Likely violated | Pool A's control is ~95% Amarakaeri, mostly legal corridor (T8, X12) |
| Reference year typical | **Violated** | 2018 is Amarakaeri's lowest year by far; ref choice moves θ from −1,497 to −2,372 (T4) |
| Exchangeability in space | **Violated** | Tambopata ranks 1 in pre-years; mean 1,594 vs ≤ 52 ha/yr for 13 of 14 controls (T3) |
| Exchangeability in time | Plausible before 2019, threatened after | Fakes span −381 to +858; COVID in 2020 (T10) |
| Comparable pool | Partly | Pool B holds coastal and Andean zones; the "restricted" pool keeps two Andean zones (T6) |

## 9. Weaknesses, ranked

1. **The raw placebo-in-space rank measures scale, not effect.** Tambopata ranks first in 2014, 2015 and 2016 too (T3). The headline p = 0.067 cannot be read as evidence of an unusual 2019-21 on its own.
2. **Pre-period coefficients are large.** The 2016 lead is 64% of the post mean, and the relative-magnitude breakdown value is about 0.5 (T7).
3. **Reference year 2018 is unusual** and inflates the effect by about 300 ha/yr against a 2014-18 reference; it also manufactures the 2022-25 "persistence" (T4).
4. **Pool A is Tambopata minus half of Amarakaeri.** Bahuaja-Sonene adds nothing and enters through a 145-ha sliver with no mining (T1, T8).
5. **The figure mixes pools and its headline is contradicted by its own pre-years** (T9).
6. **Three "Amazon" definitions**; the restricted placebo keeps two Andean zones (T6).
7. **`placebo_space_rank_scaled` is reported "of 15" but has 11 valid units** and is not discussed in the text (T5).
8. Wording: "then came back" (figure) suggests enforcement ended.

## 10. Proposed decisions

| # | Decision | Recommendation |
|---|---|---|
| D-S3-1 | Placebo-in-space statistic | Stop citing raw-hectare rank 1 as a test. Report it next to the same rank for the pre-years (2016: also rank 1) and next to the scale-free ranks (MSPE ratio 1/15, scaled 10/11, studentised 9/15). Lead with placebo in time (T10), which compares Tambopata with itself. |
| D-S3-2 | Reference period | Use the pooled 2014-18 reference as the main specification (θ = −1,562 pool A, −1,454 pool B); report ref 2018 (−1,863 / −1,633) as a sensitivity. |
| D-S3-3 | Main pool | Drop pool A as the main line (it is Tambopata minus half of Amarakaeri). Use one shared list, `peru_models.AMAZON` (8 lowland zones), in `peru.py`, `peru_robust.py` and `peru_models.py`, defined once in `common.py`; report pool B as robustness. Before calling the list "alluvial gold", find a source for Allpahuayo Mishana and Cordillera Azul. |
| D-S3-4 | Figure | Line and band from the same pool. Pooled reference. Headline that describes, e.g. "Tambopata's gap to other zones was widest in 2019-22; it already swung widely in 2014-17". Drop "then came back". Mark 2016 so readers see the pre-period swing. |
| D-S3-5 | Honest bounds | Add the T7 table (breakdown M̄* ≈ 0.5; 1.2-1.8 only if the 2016 dip, which both products show, is set aside) to the methods page as a sensitivity statement. |
| D-S3-6 | Registry | Fix the denominator of `placebo_space_rank_scaled` (n = 11, not 15); register the pre-year ranks and the pooled-reference coefficients. |

## 11. Verdict

The event study is computed correctly: pyfixest equals the closed form, and every registered number reproduces. What it shows is **description**: Tambopata's net additions sat far below the comparison zones in 2019-22, by about 1,450-1,860 ha/yr in 2019-21 depending on the reference year and pool.

What it does **not** show:
- **That the fall is unusual for Tambopata relative to other zones.** The raw placebo rank is 1 in pre-years as well, and scale-free ranks range from 1 to 10.
- **Parallel pre-trends.** The 2016 and 2017 leads are large, and a post-period drift half the size of the largest pre-period swing would explain the whole 2019-21 gap.

The strongest piece of placebo evidence is placebo in time on Tambopata's own gap: rank 1 of 15, robust to the reference choice. But 2020 coincides with COVID.

Label: **description**.

**The brief may say:** "Relative to other Peruvian buffer zones, Tambopata's net mining additions were about 1,450-1,560 ha/yr lower in 2019-21 than in 2014-18 (pooled reference), the largest such gap for any three-year window since 2003 [D]. Tambopata already swung by up to 1,200 ha/yr against the same zones before 2019 [D]."

**The brief must not say:**
- "Tambopata dropped below every placebo zone" or "rank 1 of 15" as if it were a significance test;
- "the effect came back after enforcement ended";
- any p-value from the clustered standard errors.

## References

- Abadie, A., Diamond, A. and Hainmueller, J. (2010). Synthetic control methods for comparative case studies. *JASA* 105(490).
- Conley, T. and Taber, C. (2011). Inference with "difference in differences" with a small number of policy changes. *REStat* 93(1).
- Ferman, B. and Pinto, C. (2019). Inference in differences-in-differences with few treated groups and heteroskedasticity. *REStat* 101(3).
- Firpo, S. and Possebom, V. (2018). Synthetic control method: inference, sensitivity analysis and confidence sets. *Journal of Causal Inference* 6(2).
- Fisher, R. A. (1935). *The Design of Experiments*.
- Freyaldenhoven, S., Hansen, C. and Shapiro, J. (2019). Pre-event trends in the panel event-study design. *AER* 109(9).
- MacKinnon, J. and Webb, M. (2020). Randomization inference for difference-in-differences with few treated clusters. *Journal of Econometrics* 218(2).
- Rambachan, A. and Roth, J. (2023). A more credible approach to parallel trends. *REStud* 90(5).
- Roth, J. (2022). Pretest with caution: event-study estimates after testing for parallel trends. *AER: Insights* 4(3).
- Sun, L. and Abraham, S. (2021). Estimating dynamic treatment effects in event studies with heterogeneous treatment effects. *Journal of Econometrics* 225(2).
