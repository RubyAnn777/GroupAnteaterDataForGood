# Causal methods review: walkthrough plan

**Owner:** Ruby · **Branch:** `ruby/causal-methods-review-1ogcxj` (branched from `analysis/v2-raster` @ 4c0d255, where all the analysis code lives) · **Started:** 2026-10-14

This is the reference plan for going through every causal attempt in the project with Ruby, one method at a time. Each session **starts with the method card** (what the method is, from simple to PhD level, then this project's example), and only then do we test and check the code.

Everything below was derived from the code (`code/*.py`, `data_intermediate/`, `output/numbers.csv`), not from the READMEs. File references are `file:line` on this branch. The findings in each session are **audit leads to verify together**, not settled conclusions: we reproduce each one before changing code or text.

---

## 0. How each session runs

Each method gets one session. A session produces one card in `docs/methods/NN_<method>.md` and, where needed, code fixes on this branch.

### 0.1 The method card (always written first)

| Section | Content |
|---|---|
| **1. In one sentence** | What question the method answers, in plain words. |
| **2. Simple version** | The intuition with a toy example (no formulas). |
| **3. When to use it / when not** | The data shapes and situations it fits; the ones where it breaks. |
| **4. Assumptions** | Every identifying assumption, stated formally and in words. |
| **5. Maths** | Estimand, estimator, formulas, inference. Master's level first, then the PhD-level details (e.g. weights, asymptotics, recent literature). |
| **6. Our example** | How the project applies it: the exact variables, data lineage and code path. |
| **7. Variables table** | For each variable: name in code → definition → source dataset (publisher, collection, file) → engineering steps → `file:line`. |
| **8. Assumption check** | For each assumption: supported by / threatened by / why, with evidence from our data. |
| **9. Weaknesses found** | Ranked, with `file:line` and how we verified. |
| **10. Tests run** | What we ran, what we expected, what we got. |
| **11. Verdict** | Claim label (description / prediction / causal), what we may say in the brief, and what we must not say. |

### 0.2 The test routine (after the card)

1. **Trace:** follow each variable from raw file → intermediate → model input, and print a few rows at each step.
2. **Reproduce:** recompute the headline numbers independently (small script) and match `output/numbers.csv`.
3. **Stress:** run the session's list of tests (below).
4. **Decide:** fix code, fix wording, or accept and document. Log the decision in the card, in this plan and in `agent.md` §16.

### 0.3 Ground rules

- Claim labels follow the assignment: **description**, **prediction** or **causal**. Nothing becomes causal by accident.
- Every number must come from `code/main.py` → `output/numbers.csv`.
- One treated unit means conventional standard errors are not informative (Conley and Taber 2011). Placebos are the default inference.
- Never subtract numbers across products or collections (MapBiomas Col 4 / Col 6 / Col 10.1 / Col 11, AMW, DETER, MAAP).

---

## 1. Inventory: what exists in the code

### 1.1 Causal / quasi-causal attempts

| # | Attempt | Code | Unit, years | Outcome | Inference | Current claim |
|---|---|---|---|---|---|---|
| A1 | 2×2 difference in differences | `peru.py:61-126`, `peru_robust.py` | Tambopata BZ vs Amarakaeri BZ; 2016-18 vs 2019-21 | net annual addition (ha) | none (description) | D: −1,762 ha/yr |
| A2 | Event study + placebo in space and time | `peru.py:129-266` | 15 Peruvian BZs, 2014-25, ref 2018 | net addition (ha) | placebo-in-space rank | D: rank 1 of 15 |
| A3 | TWFE model ladder M1-M4 | `peru_models.py` | 15 BZs, 2014-25 | net addition (ha; M4 scaled) | placebo rank, fake 2016 | upper end of the [C] range (−1,859) |
| A4 | Context controls K0-K3 (COVID, PP 0128 money) | `peru_context_models.py` | 15 BZs, 2015-25 | net addition | placebo rank | D: "keeps 97%" |
| A5 | Synthetic control | `peru_synth.py`, SC inside `peru_sdid.py` | Peruvian BZ donors | net addition (ha, scaled, cumulative) | RMSPE-ratio rank | lower end of the [C] range (−411) |
| A6 | Synthetic DiD | `peru_sdid.py` | 15 BZs, pre 2014-18 | net addition | placebo rank | D: −1,545, rank 1 |
| A7 | 1-km cell panel DiD + event study + road gradient | `v2_stats.py` | 14,241 cells, 2010/2014-25 | first-time mined ha per cell | CRV1 (10-km blocks), wild cluster bootstrap, PPML | D: La Pampa −1.2, across the road +0.9 |
| A8 | Spatial RD (difference in discontinuities) | `v2_rdd.py` | 250-m bins × 2-km segments at the road and the reserve edge | first-time mined % of land | rdrobust CR1, fake years, fake borders | D: road +2.1 pts (p 0.08) |
| A9 | Road fake-date test | `v2_tests.py:35-60`, `placebo_explainer.py` | road bands | north share of new mining | rank among fake start years | D: rank 1 of 8 |
| A10 | Rule-based twins (Ruby's design) | `control_amw/elevation/mb_amazonia/select/top3.py` | 1,174 Amazon areas → Amanã, Tapajós | AMW new area as % of 2018 stock | pre-trend OLS, Welch (none headline) | D: 40% of the twins' pace |
| A11 | Matching (7 estimators) | `control_psm.py` | 20-area pool | AMW pace | placebo rank | D: p 0.19-0.57, no common support |
| A12 | Brazil 2×2 | `brazil.py` | Yanomami vs Kayapó / Munduruku, Col 10.1 | net addition | none | D: inconclusive |
| A13 | Brazil per-territory before/after vs pool | `brazil_stagger.py` | AMW, 2019-25 | log change in new area | none | D |
| A14 | Brazil staggered DiD (TWFE, did2s) + randomization inference | `brazil_v2.py`, `brazil_raster.py` | 24 TIs, Col 11 rasters, 2014-25 | ln(1 + first-time ha) | CRV1, RI | D: "+0.26, wrong sign" |
| A15 | Risk map | `v2_extra.py` (E4) | 1-km cells | P(new mining) | spatial hold-out AUC | P |

### 1.2 Descriptive building blocks the attempts depend on

| Block | Code | What it gives |
|---|---|---|
| Pack tables and source checks | `how_the_panels_were_built/04_panels.py`, `checks.py`, `DOWNLOAD_LOG.csv` | MapBiomas Peru Col 4 / Brazil Col 10.1 panels; publisher checks |
| Net additions | `common.py:36-53`, `peru.py:33-58` | level(t) − level(t−1), all departments summed |
| Raster zones and pixel accounting | `raster_zones.py` | 12 zones; first-time / re-mined / stopped pixels |
| Displacement layers | `raster_layers.py`, `v2_legality.py`, `v2_products_check.py` | stream, Sankey, corridor share, legality |
| Inside the reserve | `peru_anp.py` | MapBiomas Peru ANP Col 4 |
| AMW zones and rings | `spatial.py`, `spatial_zones.py`, `v2_extra.py` | AMW new area by zone |
| Timing, gold, money | `glad_alerts.py`, `raster_gold.py`, `peru_production.py`, `peru_gold_minem.py`, `v2_tests.py` (T8) | GLAD alerts, gold proxy, declared gold, PP 0128 spending |
| Brazil enforcement context | `brazil_deter*.py`, `brazil_ibama.py` | DETER alerts, IBAMA autos |

### 1.3 The three outcome measures (session 1 topic)

| Measure | Definition | Product | Used by |
|---|---|---|---|
| **Net addition** | mining stock(t) − stock(t−1); negative allowed | MapBiomas Peru Col 4 (statistics workbooks) | A1-A6 |
| **First-time mining** | pixels classified mining in t and never before (since 1985) | MapBiomas Peru Col 4 rasters / Brazil Col 11 rasters | A7-A9, A14, figures |
| **AMW new area** | union of new 480-m patches minus all earlier patches; 2018 = stock | Amazon Mining Watch (2026-10-03) | A10, A11, A13, AMW checks |

These three measure different things. Net additions drop when re-mined land stays mined and when pits turn into water. First-time mining ignores re-mining. AMW misses infill inside earlier patches. Any "Tambopata fell" statement must name its measure.

---

## 2. Session order

| Session | Topic | Why in this order |
|---|---|---|
| **S0** | Potential outcomes and claim labels (card only) | The language for every later card |
| **S1** | Data lineage, outcomes, zones, treatment timing | Every method inherits these; errors here propagate |
| **S2** | 2×2 DiD (A1) | The simplest design; sets the logic |
| **S3** | Event study and placebo inference (A2) | Adds dynamics and the placebo logic used everywhere |
| **S4** | TWFE model ladder (A3) | Regression version of S2-S3 |
| **S5** | Context controls and bad controls (A4) | Builds on S4 |
| **S6** | Synthetic control (A5) | A different counterfactual: weights instead of averages |
| **S7** | Synthetic DiD (A6) | Combines S4 and S6 |
| **S8** | Raster backbone and the 1-km cell panel (A7) | Moves from zones to pixels |
| **S9** | Spatial RD and the road tests (A8, A9) | Uses the raster backbone from S8 |
| **S10** | Rule-based twins (A10) | Ruby's design |
| **S11** | Matching estimators (A11) | Algorithmic version of S10 |
| **S12** | Brazil (A12-A14) | Re-uses DiD, staggered DiD and RI |
| **S13** | Descriptive and predictive blocks (displacement, reserve, AMW, GLAD, gold, risk map) | Context for the story |
| **S14** | Synthesis: the claim, the range, the figure, the limits | Decide what the brief says |

---

## S0. Potential outcomes and claim labels (card only, no code)

**Card:** potential outcomes Y(1), Y(0); ATT; the fundamental problem; what "counterfactual" means for one treated zone; description vs prediction vs causal; selection on observables vs design-based identification; SUTVA (no interference, one version of treatment). Project example: Y(0) = mining in the Tambopata buffer zone in 2019-21 if Mercurio had not happened.

**Decided 2026-10-14 (Ruby):** the treatment is the **start of Operation Mercurio (Feb 2019, first treated year 2019)**. Later events are context, shown in figures but not modelled. Card: `docs/methods/00_potential_outcomes.md`.

**Background to that decision:** what is "the treatment"? The code always treats **2019** as the first treated year (Feb 2019). But enforcement is a sequence: 2017-18 operations (pre-period is not clean), Mercurio 2019, COVID 2020, Plan Restauración 2021, Mercurio II (all of Madre de Dios, incl. Amarakaeri), state of emergency from April 2023, navy withdrawal 2025. Every design below actually estimates "Mercurio + whatever followed, relative to a comparison that was itself partly treated".

---

## S1. Data lineage, outcomes, zones, treatment timing

**Card:** measurement error in the outcome (classical vs non-classical), stock vs flow, absorbing outcomes, classification noise in remote sensing, the modifiable areal unit problem.

**Files:** `how_the_panels_were_built/04_panels.py`, `checks.py`, `common.py`, `peru.py:33-58`, `raster_zones.py`, `peru_anp.py`, `peru_gold_minem.py`, `DOWNLOAD_LOG.csv`.

**Variables to trace**

| Variable | Definition as coded | Source | Where |
|---|---|---|---|
| `mining_ha` | area with `class_level_4 == "4.2. Minería"` | MapBiomas Peru Col 4, ZONA-AMORTIGUAMIENTO workbook | `04_panels.py:56-63` |
| buffer-zone unit | `buffer_zone|pa_category`, summed over departments | pack table | `peru.py:39` |
| net addition | `levels.diff()` | derived | `peru.py:57` |
| first-time mining | `mine & ~ever` per pixel | MapBiomas Peru Col 4 rasters | `raster_zones.py:186-208` |
| zones 1-12 | first match wins; La Pampa = Tambopata BZ × lon −70.15…−69.80; across = D.L. 1100 corridor ≤ 10 km north of the road | SERNANP, INGEMMET, RAISG, native communities | `raster_zones.py:58-165` |
| road distance | latitude offset to the road × 110.574 km | RAISG roads | `raster_zones.py:112-134` |

**Leads to verify**

1. **Net additions are net of outflows and blind to re-mining** (`common.py:36-47`). 106 of 421 nonzero BZ unit-years are negative; Tambopata 2021 = −111. Pits turning into water subtract. This biases toward finding a fall in a mature hotspot like La Pampa.
2. **Shared 2023 spike** in every unit (first-time and re-mined) may be a map artefact. Untested.
3. **Single treatment date, different year-mapping rules:** Peru always 2019; Brazil stagger uses the operation's calendar year, `brazil_v2` shifts Jul-Dec operations to the next year (`brazil_v2.py:59-61`).
4. **"Rest of Madre de Dios" is mislabelled** (`peru.py:43-47, 316, 356`): it also contains the reserve interiors and native communities, not only the legal corridor.
5. **Bahuaja-Sonene is a Puno unit**: it enters pool A through a 145-ha Madre de Dios row (`peru.py:160-162`).
6. **Running variable is a north-south offset, not a perpendicular distance**, while the docstring says ESRI:102033 (`raster_zones.py:113-114`). Ratio to true distance: median 1.08, up to 1.44 near the road.
7. **La Pampa window was chosen by looking at the outcome map** (`raster_zones.py:21-22`); the `ACROSS_KM = 10` parameter is never varied.
8. **Today's boundaries applied to 1985-2025** (corridor, communities).
9. **Checks:** some are reproductions of the instructor's numbers, not publisher checks (`checks.py:55-59`). Real publisher checks: Tambopata BZ 20,730 (platform screenshot), Tambopata NR 777, raster checks (`raster_layers.py:273-275`).
10. **MINEM gold rebuild does not match BCRP** after 2014 (2015 +48%, 2016 +8%, 2020 +47%, 2021-25 +10-16%), but the check tests only 2012 and 2019 (`peru_gold_minem.py:119-120`). `explainer_content.md:352` and log row 65 claim 2016 matches exactly. Confirmed: rebuilt 2020 declared = 2,152 kg vs BCRP 1,460 kg.
11. "2017 = map reclassification" inside the reserve (`peru_anp.py:62-93`) is asserted, but the transition table shows ~390 ha came from forest and farm classes.

**Tests**
- Gross vs net: split Tambopata BZ 2019-21 net additions into first-time, re-mined and outflow (mining → water/beach) using `zone_year_v2.csv`.
- 2023 spike: compare with GLAD and AMW in the same zones; if MapBiomas-only, report 2022-25 without 2023 throughout.
- Grid identity: assert same CRS/transform/shape across all yearly rasters (needs the git-ignored rasters).
- Flicker: count pixels mined in exactly one year; redefine first-time as "mined in t and t+1" and see how much the La Pampa numbers move.
- MINEM vs BCRP for every year 2005-2025; fix the check and the text.
- Decide one treatment-date rule for the whole package.

---

## S2. The 2×2 difference in differences (A1)

**Card:** DiD as a double contrast; ATT under parallel trends; levels vs logs vs scaled outcomes (parallel trends is scale-dependent); spillovers into the control and their sign; no-anticipation.

**Files:** `peru.py:61-126`, `peru_robust.py`.

**Spec:** (mean addition Tambopata 2019-21 − 2016-18) − (same for Amarakaeri) = −1,477 − (+285) = **−1,762 ha/yr**. Placebo window 2013-15 vs 2016-18 = +209. Persistence 2016-18 vs 2022-25 = −737.

**Assumptions and leads**
- *Parallel trends in hectares between units of very different size*: in 2016-18 Tambopata added 20.5% of its stock per year, Amarakaeri 4.4%.
- *Untreated control*: Amarakaeri had Camanti displacement and Mercurio II; under spillover the DiD is biased **away from zero**.
- *Clean pre-period*: 2017-18 operations sit in it; Amarakaeri 2018 = 54 ha is an outlier (301-542 in 2014-17).
- Pre-window sensitivity: 2016-17 only → −1,586; 2014-18 → −1,663.

**Tests**
- Re-run with 2014-18 and 2016-17 bases; report the spread.
- Placebo in time for every fake start 2008-16 (audit: all positive, +167 to +1,034; real ranks 1 of 10, p = 0.10).
- Log and scaled versions of the 2×2.

---

## S3. Event study and placebo inference (A2)

**Card:** dynamic DiD, lead/lag coefficients, the omitted year, pre-trend tests and their low power (Roth 2022), Rambachan-Roth bounds; Fisher randomization inference, placebo-in-space (Abadie, Diamond and Hainmueller 2010), exchangeability, one-sided rank p = rank/n.

**Files:** `peru.py:129-266`, `common.py:55-61` (`placebo_rank`).

**Spec:** `y ~ Σ_k d_k (k ≠ 2018) | unit + year`, CRV1 saved but flagged not informative; pool A = Tambopata, Amarakaeri, Bahuaja; pool B = 15 zones with any 2014-18 change.

**Leads to verify**
1. **Rank 1 also fires in a pre-year**: 2016 coefficient −1,195 (pool A), below every placebo (−67 to +314). Raw-hectare ranks mainly measure that Tambopata swings 5× Amarakaeri and ~100× the others.
2. Scale-free rank is **10 of 15** (`placebo_space_rank_scaled`), registered but not discussed.
3. **Reference year 2018** inflates magnitudes: mean 2019-21 coefficient −1,863 (ref 2018), −1,634 (ref 2016-18), −1,562 (ref 2014-18).
4. **Restricted "Amazon" pool contains Andean zones** (Junín, Río Abiseo) (`peru.py:268-294`); three modules use three "Amazon" definitions.
5. Pool B includes coastal and Andean zones and zones with negative pre-means.
6. The figure mixes pools: pool A line, pool B placebo band (`peru.py:233-236`).
7. Previously fixed: Tambopata excluded from its own placebo pools; one rank convention.

**Tests**
- Rank the 2016 coefficient with the same loop (if rank 1, the test measures scale).
- Pooled reference periods; Rambachan-Roth relative-magnitude bounds.
- One shared list of comparable alluvial-gold zones across `peru.py`, `peru_robust.py`, `peru_models.py`.

---

## S4. Two-way fixed effects model ladder (A3)

**Card:** TWFE as a regression DiD; what unit and year effects absorb (and do not); interacted controls (exposure × common shock); unit-specific trends and how post-period data contaminate them; scaled outcomes; Frisch-Waugh-Lovell.

**Files:** `peru_models.py`.

**Spec:**
- M1: `y_it = α_i + γ_t + β_1 T_i·1[2019-21] + β_2 T_i·1[2022-25] + ε`
- M2: + `pre_i × ln(gold_t)`
- M3: + zone-specific linear trends
- M4: y scaled by the zone's signed 2014-18 mean
- Estimated with `numpy.lstsq` (full rank checked), asserted equal to pyfixest.

**Leads to verify**
1. **M1 is essentially Tambopata's own before/after**: control mean moves only +21.8 ha; −1,432 − 21.8 = −1,453.6.
2. **"Year effects absorb the gold price and COVID"** (docstring, label, brief) is not valid in levels: year effects are ~22 ha against a 1,500 ha gap.
3. **M2's gold slope is identified from Tambopata's own post-period** with binned post dummies (slope 0.34). Saturating Tambopata's post years: slope 2.40, gap **−2,508**. Same mechanism as referee C5 for M3 (fixed via `m3pre` = −2,004), not fixed for M2.
4. Honest model range is roughly −1,450 to −2,500, wider than the quoted ladder.
5. Fake 2016 window overlaps the 2017-18 operations; M2/M4 fakes use 2011-15 denominators (different scale).
6. M4 rank 3 of 7 is robust ("ordinary relative to size").

**Tests:** saturate post years in M2/M4; leave-one-out over controls; regress year effects on Δln gold.

---

## S5. Context controls and bad controls (A4)

**Card:** bad controls (Angrist and Pischke), controls that are themselves outcomes of the treatment, mediators vs confounders, dose-response.

**Files:** `peru_context_models.py`, `v2_tests.py:175-186` (PP 0128 spending).

**Spec:** M2 on 2015-25 + `pre × 1[2020-21]` (COVID) + `MdD × ln(PP 0128 spending)`.

**Leads to verify**
1. **K1's COVID term is identified mostly from Tambopata's own within-bin fall**: −0.348 binned, about −0.145 without Tambopata. Saturated: K0 −2,568 → K1 −2,425 (−6%), not −1,608 → −1,322 (−18%).
2. **"Keeps 97%" is two offsetting biases**: K1 shrinks the gap, K2 enlarges it (spending coefficient +93, from Amarakaeri and Bahuaja rising in 2020-21).
3. Spending spikes **because of** Mercurio (0.65 M soles in 2018 → 31.1 M in 2019): a post-treatment variable, so a bad control by construction; the dose correlation (−0.31) is mechanical.

**Tests:** COVID term estimated on controls only; saturated versions; decide whether K-models stay in the brief.

---

## S6. Synthetic control (A5)

**Card:** Abadie et al. (2003, 2010, 2015); convex-hull condition; pre-period fit (RMSPE); donor pool rules; post/pre RMSPE ratio test; interpolation bias; why it fails for extreme units.

**Files:** `peru_synth.py`, SC branch of `peru_sdid.py:262-263`.

**Leads to verify**
1. **Convex-hull failure is real and documented**: in hectares Tambopata is outside the donor range in 9 of 9 pre-years (pre-RMSPE 1,467).
2. **The scaled "good fit" is an Andean twin** (77% Cotahuasi); its rank-1 statistic pools 2019-25 two-sidedly, so "deepest dip" is a mislabel; unstable across pools (ext pool: rank 5 of 8).
3. **The −411 lower bound of the brief's [C] range** comes from SC in `peru_sdid` with weight 1.0 on Amarakaeri and no pre-fit; the same estimate ranks 13 of 13 in `peru_synth` and 1 of 15 in `peru_sdid` (different statistics). It is not a credible counterfactual.
4. Pool rules, scales, fit windows and rank statistics differ from the ladder and SDID.

**Tests:** align pools and statistic with the ladder; apply a pre-fit criterion before any SC number enters the [C] range.

---

## S7. Synthetic difference in differences (A6)

**Card:** Arkhangelsky et al. (2021): unit weights with intercept and ridge penalty ζ, time weights, the τ formula, nesting of DiD and SC, placebo variance.

**Files:** `peru_sdid.py`.

**Implementation:** matches Algorithm 1 (ζ, intercepts, penalties, τ); FISTA converges (the audit verified a lower objective than the referee's SLSQP, which violated Σw = 1).

**Leads to verify**
1. **Time weights collapse onto one or two pre-years**: 0.86 on 2014, 0.14 on 2017, 0 on 2018. With pre 2011-18: 0.93 on 2012 → τ = −684. τ swings by 2.3× depending on which pre-year the weights select.
2. Unit weights load on tiny or negative zones (Cordillera Azul 0.45, Junín 0.25).
3. Leave-one-out: dropping Amarakaeri gives −2,198.
4. Placebo SE (45 ha) is a size artefact; scaled versions rank 3 of 7 for every method.

**Tests:** τ against pre-window start 2010-2014 and the argmax of λ; leave-one-out.

---

## S8. Raster backbone and the 1-km cell panel (A7)

**Card:** gridded panels, absorbing outcomes, cluster-robust inference with few treated clusters, wild cluster restricted bootstrap (Cameron, Gelbach and Miller 2008; MacKinnon and Webb), spatial correlation (Conley), PPML for count-like outcomes, multiple testing (Holm, Romano-Wolf).

**Files:** `raster_zones.py`, `raster_layers.py`, `v2_stats.py`, `v2_tests.py`.

**Spec:** `new_land_ha_ct ~ Σ_z Σ_p zone_z × period_p | cell + year`, 2014-25, pooled 2014-18 reference, CRV1 by 10 × 10-km blocks; own WCR bootstrap (correct, cached by input hash); PPML; event studies 2010-25; road gradient.

**Leads to verify**
1. **The cell DiD is a before/after**: the clean reference (4,856 cells) is 99.56% zeros; only 68 cells ever mine. −1.208 = La Pampa's own −1.202 minus +0.006.
2. **PPML "robustness" comes from those 68 cells** (−0.67 own change minus +1.29 reference); every focal zone gets a large negative PPML coefficient. Still cited at `explainer_content.md:571`.
3. **"Across the road" gains also occur east of La Pampa**: corridor strip east of the window +0.89 vs across +0.94. Only the relative jump is distinctive. Threat to the displacement reading.
4. **La Pampa pre-trend failure (p 0.0055)** comes from the 2010-13 ramp-up; 2019 coefficient +0.13 (p 0.87); the fall starts in 2020 with COVID.
5. **Clustering vs shock level**: one contiguous treated zone (14 blocks); p = 0.081 (10 km), 0.088 (20 km), 0.051 (30 km). `st_n_clusters` = 161 is counted on the full panel; the regression uses 136.
6. Gradient reference band contains La Pampa and Kotsimba cells; cells beyond ±30 km fall into the omitted category.
7. Gold × year control is nearly empty (82% of cells "high gold").
8. GLAD mask still looks ahead (`glad_alerts.py:67`, `first > 0`).
9. Doc drift (`v2_stats.py:12-19`, `raster_zones.py:113`).
10. 12 × 5 + 12 + 2 tests, no multiple-testing correction.

**Tests:** placebo "across" strips at other longitudes; sliding fake La Pampa windows (spatial RI); depletion control (lagged cumulative mined share or at-risk denominator); 20/30-km blocks and Conley SEs; PPML on ever-positive cells or drop; Holm on the S1 family.

---

## S9. Spatial RD and the road tests (A8, A9)

**Card:** sharp RD, continuity, local linear regression, bandwidth choice (MSE-optimal), robust bias-corrected inference (Calonico, Cattaneo and Titiunik), geographic RD (Keele and Titiunik 2015), difference in discontinuities (Grembi et al. 2016), compound treatment at borders, donut RD, mass points.

**Files:** `v2_rdd.py`, `v2_tests.py:35-60`, `placebo_explainer.py`.

**Spec:** outcome = first-time mined ha / bin area × 100 per year; diff-in-disc of 2019-21 mean minus 2014-18 mean; north (corridor, zone 5) vs south (La Pampa, zone 7); rdrobust triangular kernel, mserd h, area weights, CR1 by 2-km segment (19 clusters).

**Leads to verify**
1. **Constant-gap assumption is weak**: yearly north-south gap swings ±3 points without treatment (2011 −3.52, 2017-18 −1.3); PRE window choice moves the estimate 1.9-2.6 and p 0.04-0.72.
2. **Timing**: 2019 alone +0.82 (p 0.22); 2020-21 +2.75 (p 0.09). "Within a year" overstates.
3. **Fake-year rank 1 of 10** wins by 1.2% over fake 2011 (|2.077|); minimum attainable p = 0.10.
4. Running variable is a vertical offset (see S1).
5. Compound treatment: legality, road access, targeting, COVID all change at the road.
6. **Depletion differs across the line**: 16.4% south vs 9.7% north already mined by 2018; the gold proxy cannot test continuity (gold_share = 1 everywhere within ±6 km).
7. Reserve: fake-year pool still padded with 1998-2006 zeros; the 2017 invasion sits in PRE; "outside" includes treated La Pampa.
8. "0.04-0.98 across bandwidths" in the brief includes the donut run.
9. **Road fake-date test (A9)** uses ±30 km bands, while the docs say 0-15 km; with ±15 km 2019 ranks 2 of 7. Start year 2022 is still in the "clean" set though its pre-window is 2019-21. A two-sided rank gives 2 of 8.

**Tests:** perpendicular distance; PRE-window table; 2019-only vs 2020-21; CR3 and 4/6-km clusters; at-risk denominator (audit: 2.05, p 0.24); LP window variants; reserve pool from 2007.

---

## S10. Rule-based twins (A10, Ruby's design)

**Card:** case-control and comparative case study logic; selection on pre-treatment characteristics vs on outcomes; the n = 1 problem; cross-product comparability.

**Files:** `control_amw.py`, `control_elevation.py`, `control_mb_amazonia.py`, `control_select.py`, `control_top3.py`, `data_intermediate/operations_coded.csv`.

**Rules as coded** (`control_select.py:47-63`): R1 AMW 2018 stock ≥ 500 ha; R2 no operation 2017-25 (R2b: or first operation ≥ 2022); R3 outside the Madre de Dios box; R4 median elevation < 500 m and stock ≥ 0.2 × Tambopata. Strict: 0 pass. Relaxed: Amanã, Tapajós.

**Leads to verify**
1. **The twins are treated in the opposite direction**: Brazil's 2019-22 de-enforcement overstates Tambopata's relative fall.
2. **R2b selects on the outcome**: operations from 2022 plausibly responded to fast growth.
3. **R2 measures media coverage, not enforcement**: Kayapó excluded for a 3-day raid; Amanã's "none" rests on two searches.
4. **Coding bug**: Sawré Muybu, Menkragnoti and Enawenê-Nawê are coded "none" but were searched for 2022-25 only. Sawré Muybu passes R1-R3 and sits in the PSM pool.
5. **Pre-trends predict the gap**: a linear trend in the growth difference predicts a larger 2019-21 gap than observed, so trend-adjusted Tambopata did *better* than predicted.
6. **AMW vs MapBiomas ratio** 1.65× (Tambopata) vs 5-6× (twins): size matching depends on the product; overlap-free AMW accounting penalises dense mining.
7. Pre-trend test subtracts Col 4 and Col 6 growth rates (`control_top3.py:47`).
8. Stale "three twins" text; `methods_content.md:209` cites the slope-test p as a level test.

**Tests:** trend-adjusted gap; recode the three territories; MapBiomas-based twin choice; non-Brazil pool; Col 4 vs Col 6 on the Tambopata reserve.

---

## S11. Matching estimators (A11)

**Card:** propensity score (Rosenbaum and Rubin), unconfoundedness and overlap, nearest neighbour, calipers, Mahalanobis, CEM, entropy balancing (Hainmueller 2012), IPW for the ATT, balance diagnostics, why matching with one treated unit is a case study.

**Files:** `control_psm.py`.

**Leads to verify**
1. **No common support**: Tambopata's score 0.853 > pool maximum 0.758; the caliper is computed but never passed (`control_psm.py:285`).
2. **Country is fully confounded**: pool = 15 Brazil, 3 Venezuela, 1 Bolivia, 1 Ecuador, 0 Peru; Brazil dummy unbalanced (SMD −1.8 to −2.25); entropy balancing max imbalance 0.76 SD.
3. The propensity "treatment" is any reported operation 2017-21, not Mercurio.
4. Post-only outcome (AMW starts 2018): not a DiD.
5. Placebo exchangeability fails (small units give huge gaps); the log-ratio statistic gives the same verdict (p 0.19-0.52).
6. Ebal/IPW after-gaps driven by Sararé.
7. MIN_STOCK 100 vs 500 in the funnel; "unknown_none keeps every gap negative" overstated (−0.15 pp).

**Tests:** pass the caliper; Peru-plus-non-Brazil pool; report the log-ratio placebo.

---

## S12. Brazil (A12-A14)

**Card:** staggered adoption; why TWFE fails with heterogeneous effects (Goodman-Bacon 2021, de Chaisemartin and D'Haultfœuille 2020); Gardner's two-stage did2s; Callaway and Sant'Anna; randomization inference with targeted assignment.

**Files:** `brazil.py`, `brazil_stagger.py`, `brazil_v2.py`, `brazil_raster.py`, `brazil_deter*.py`, `brazil_ibama.py`.

**Leads to verify**
1. **Critical: 13 of 24 territories have zero mapped mining in every year** (confirmed: 14 of 26 units in `brazil_raster_unit_year.csv` incl. a ring). Units were chosen with AMW, measured with MapBiomas. Dropping them flips the sign: TWFE −0.22, did2s −0.37. The brief's "wrong sign" sentence rests on this.
2. **Critical: parallel trends fail**: treated territories rise 1.10 → 3.72 (2015-2020) in ln(1+ha), never-treated stay flat. Operations target booms.
3. **Treatment dates**: Kayapó's verified PF action (Jun 2023) is ignored (coded Sep 2024); Munduruku's May 2021 snippet excludes it as a twin but is rejected as a treatment date. Estimates range −0.37 to +0.62 across defensible choices. Event lines in figures are hard-coded.
4. **Pools never searched**: 10 of 13 never-treated (v2) and 14 of 18 (stagger); 58% of the pool's 2023-25 growth is in Aripuanã, next to Golden Border targets.
5. **Products disagree on timing**: Col 10.1 falls in 2023, Col 11 in 2024, DETER rises in 2023, AMW new area 2.3× the MapBiomas stock. No Col 10.1 vs Col 11 check exists.
6. **The 2019-22 "weaker enforcement" premise is not shown by the IBAMA data in the code**: all autos fell, but mining autos 157 → 147.5/yr and mining-and-indigenous autos rose. Needs an external citation.
7. "Munduruku" means three different units across modules; treated set mixes ranch-clearing desintrusões; 4 treated units have one post year.

**Tests:** units with mining > 0 only; event study with leads; one dating rule package-wide; RI restricted to mining units with did2s; Col 10.1 vs Col 11 comparison; IBAMA regex with word boundary.

---

## S13. Descriptive and predictive blocks

**Card:** accounting identities, displacement measurement, prediction vs causation (AUC, out-of-sample validation, calibration).

**Topics and leads**
- **Displacement sums** (`peru.py:115-125`): MdD total 3,610 → 4,640 → 12,049 ha/yr; no counterfactual trend; "rest" includes reserve interiors.
- **Corridor share** (`raster_layers.py`): 49 → 68 → 72%; the rest-of-corridor rise (+1,588) is larger than La Pampa's fall (−673), so most corridor growth cannot be the same miners.
- **Inside the reserve** (`peru_anp.py`): +241 ha in 2025; the 2017 step needs a source; `anp_..._share_..._2019_21` = −0.257 should not be cited.
- **AMW zones** (`spatial.py`): the "Madre de Dios box" is 58% outside the department; zone precedence differs from `raster_zones`; "two sources agree" with MAAP holds for direction only (AMW ~4× larger).
- **Legality** (`v2_legality.py`): time-consistency correction is one-directional.
- **Gold proxy** (`raster_gold.py`): strict vs broad definitions reverse the depletion ranking.
- **GLAD** (`glad_alerts.py`): look-ahead mask; collection break in 2021.
- **Declared gold** (`peru_gold_minem.py`): see S1 lead 10.
- **Risk map** (`v2_extra.py` E4): AUC 0.923 vs benchmark 0.909; uncalibrated threshold; road distance wrong where the road runs north-south.

---

## S14. Synthesis

1. Decide the measure each claim uses (net / first-time / AMW).
2. Rebuild the conditional causal range from specifications that pass agreed criteria (pre-fit, placebo, leave-one-out). The current "411-1,859 ha/yr" mixes a no-pre-fit SC with M3, so it is neither a bound nor a sensitivity interval.
3. Re-word claims flagged above: "rank 1" (scale), "year effects absorb gold/COVID", "keeps 97%", "within a year", "wrong sign" (Brazil), "two sources agree", "map reclassification", "2016 matches BCRP exactly".
4. Re-check the one brief figure against the agreed measure and wording.
5. Update `agent.md`, the walkthrough and the brief.

---

## 3. Cross-cutting issues register

| # | Issue | Affects | Severity |
|---|---|---|---|
| X1 | Raw-hectare placebo ranks measure scale, not effect (rank 1 also in 2016) | A2, A3, A6 | High |
| X2 | Comparison units partly treated (Amarakaeri; Brazil de-enforcement for twins) | A1-A6, A10-A11 | High |
| X3 | Fall starts 2020, with COVID; 2019 shows nothing | A2, A7, A8 | High |
| X4 | Net additions vs first-time vs AMW measure different things | all | High |
| X5 | Specifications whose controls absorb the treatment's own dynamics (binned post dummies) | A3, A4 | High |
| X6 | Treatment dating rules differ across modules | A9, A10, A12-A14 | High |
| X7 | Pools and "Amazon" lists defined differently per module | A2-A6, A10-A11 | Medium |
| X8 | Absorbing outcome / depletion not controlled | A7, A8 | Medium |
| X9 | Clustering level below the shock level | A7, A8 | Medium |
| X10 | Text and docstrings out of sync with code | many | Low-Medium |
| X11 | Several raw inputs are git-ignored, so some steps verify only from intermediates | S1, S8-S12 | Process |
| X12 | Amarakaeri BZ's mined land is 58% legal corridor and 41% native communities (found in S2): the main comparison is a mostly legal mining area and the likely destination of displaced miners | A1-A6 | High |

## 4. Progress tracker

| Session | Card written | Tests run | Decisions logged | Fixes merged |
|---|---|---|---|---|
| S0 Potential outcomes | ☑ | n/a | ☑ | n/a |
| S1 Data and outcomes | ☑ | ☑ | ☐ | ☐ |
| S2 2×2 DiD | ☑ | ☑ | ☐ | ☐ |
| S3 Event study, placebos | ☐ | ☐ | ☐ | ☐ |
| S4 TWFE ladder | ☐ | ☐ | ☐ | ☐ |
| S5 Context controls | ☐ | ☐ | ☐ | ☐ |
| S6 Synthetic control | ☐ | ☐ | ☐ | ☐ |
| S7 Synthetic DiD | ☐ | ☐ | ☐ | ☐ |
| S8 Cell panel | ☐ | ☐ | ☐ | ☐ |
| S9 Spatial RD, road tests | ☐ | ☐ | ☐ | ☐ |
| S10 Rule-based twins | ☐ | ☐ | ☐ | ☐ |
| S11 Matching | ☐ | ☐ | ☐ | ☐ |
| S12 Brazil | ☐ | ☐ | ☐ | ☐ |
| S13 Descriptive blocks | ☐ | ☐ | ☐ | ☐ |
| S14 Synthesis | n/a | n/a | ☐ | ☐ |
