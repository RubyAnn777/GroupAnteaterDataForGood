# S12 · Brazil: 2×2, before/after vs pool, staggered DiD and randomization inference (attempts A12, A13, A14)

*Method card 12 of the causal review (plan: `docs/causal_review_plan.md`). Code under review: `code/brazil.py` (A12, 2×2 on MapBiomas Col 10.1), `code/brazil_stagger.py` (A13, AMW before/after vs pool), `code/brazil_v2.py` + `code/brazil_raster.py` (A14, staggered DiD on MapBiomas Col 11 rasters), `code/brazil_deter.py`, `code/brazil_deter_all.py`, `code/brazil_ibama.py` (context). Test script: `code/review/s12_brazil_checks.py` (read-only, about 2.5 minutes).*

---

## 1. In one sentence

When several places are treated at different dates, a staggered difference in differences compares each treated place, after its own start date, with places not yet treated or never treated; it estimates an average effect only if all those places would otherwise have moved in parallel.

## 2. Simple version

Four schools introduce a tutoring programme: one in 2023, two in 2024, one in 2025. Twenty other schools never do. You want to know whether tutoring raises test scores.

The obvious method is "before vs after, treated vs untreated", pooled over all schools. Two things can go wrong.

1. **Bad comparisons.** A plain regression with school and year effects (TWFE) also compares the 2025 school with the 2023 school *after* the 2023 school was already treated. If tutoring's effect grows over time, the "control" is moving because of tutoring, and the estimate can even get the wrong sign. Newer estimators (Callaway and Sant'Anna; Gardner's two-stage DiD; Borusyak, Jaravel and Spiess) only ever use not-yet-treated or never-treated schools as the comparison.
2. **Targeting.** Suppose the ministry gave tutoring to the schools whose scores were *already collapsing*. Then the treated schools were on a different path before the programme. No estimator fixes that. You see it by plotting the years *before* each school's start date (the "leads"): they should be flat.

Brazil has both problems in mild and severe form: the first is small here, the second is severe. Federal operations went to the territories where gold mining had just boomed.

## 3. When to use it, and when not

**Use it when:**
- many units start treatment at different, known dates;
- there are enough never-treated or late-treated units that look like the treated ones before treatment;
- treatment timing is not chosen in response to the outcome's recent path.

**Be careful or avoid it when:**
- treatment is assigned *because* the outcome spiked (operations sent to booming mining fronts). The leads will trend and every estimator inherits the bias;
- the comparison units do not have the outcome at all (a territory with zero mining in every year cannot show what mining would have done);
- the treatment date is uncertain or coded differently across scripts;
- the outcome is measured with products that disagree with each other on timing;
- units have only one post-treatment year;
- the outcome is log(1 + y) with many zeros: the estimate then depends on the units of y (Chen and Roth 2024).

## 4. Assumptions

| Assumption | In words | Formally |
|---|---|---|
| **Parallel trends (staggered)** | Without treatment, every cohort would have moved like the never-treated (or not-yet-treated) units | E[Y_t(0) − Y_s(0) \| G = g] = E[Y_t(0) − Y_s(0) \| G = ∞] for all t, s, g |
| **No anticipation** | Nothing changed before each unit's own date because of the coming operation | Y_it = Y_it(0) for t < G_i |
| **No spillover (SUTVA)** | An operation in one territory does not move mining in another sample territory | Y_jt does not depend on G_i for j ≠ i |
| **Correct dates** | G_i is the true first treated year | G_i observed without error |
| **Common support** | Never-treated units have mining comparable to the treated before treatment | overlap in pre-period outcomes |
| **Same measurement** | The outcome is one product and collection for all units and years | one source per series |
| **For randomization inference** | Under the null, the assignment of dates to units is exchangeable (as if random) | P(G = g) invariant to permutations |

## 5. The maths

### 5.1 Master's level

**TWFE.** The usual regression is

  y_it = α_i + γ_t + β · D_it + ε_it,  D_it = 1[t ≥ G_i].

With one treatment date, β is the 2×2 DiD. With staggered dates, β is a weighted average of many 2×2 comparisons (Goodman-Bacon 2021):
- early treated vs never treated;
- late treated vs never treated;
- early treated vs late treated, *before* the late ones start (fine);
- late treated vs early treated, *after* the early ones started (the "forbidden" comparison: the already treated act as controls).

If effects change over time, the forbidden comparisons subtract part of the early units' effect and can flip the sign.

**Imputation / two-stage DiD (Gardner 2022; Borusyak, Jaravel and Spiess 2024).**
1. Fit y_it = α_i + γ_t on *untreated* observations only (never treated, and treated units before their date).
2. Predict y_it(0) for treated observations and take τ̂_it = y_it − ŷ_it(0).
3. Average τ̂_it over the treated cells you care about (all, or by event time).

Only untreated cells inform the counterfactual, so there are no forbidden comparisons.

**Callaway and Sant'Anna (2021).** For each cohort g and year t:

  ATT(g, t) = (Ȳ_g,t − Ȳ_g,g−1) − (Ȳ_C,t − Ȳ_C,g−1),

with C = never treated (or not yet treated), then average the ATT(g, t) by event time e = t − g or overall. The "pre-period" ATT(g, t) for t < g are the leads.

**Event study with leads.** Replace D_it with dummies for each event time e = t − G_i, leaving out e = −1. Leads (e < −1) near zero support parallel trends; leads that trend say the treated units were on another path.

### 5.2 PhD level

**Negative weights.** de Chaisemartin and D'Haultfœuille (2020) show β_TWFE = Σ_{(i,t): D=1} w_it · τ_it, with w_it proportional to the residual of D_it after projecting on unit and year effects. Weights can be negative for early-treated cells late in the panel. Whether they are is a property of the design, not the outcome, so it can be checked directly (T4).

**Baseline choice under a pre-trend.** If parallel trends fail with a linear pre-trend δ·(t − G_i) in the treated group, the imputation estimator uses all pre-period cells to estimate α_i, so its bias grows with how far the average pre-period sits from the post-period. Callaway and Sant'Anna with a g − 1 base use only the last pre-year. When the treated units peak just before treatment (selection on a boom, the mining analogue of Ashenfelter's dip), the g − 1 base is the peak, and post-period values look low; the all-years base is low, and post-period values look high. **The two estimators then bracket the truth from opposite sides, and disagreement between them is a symptom of failed parallel trends, not a choice of method.** Borusyak, Jaravel and Spiess recommend testing pre-trends separately from estimating effects, for exactly this reason. Rambachan and Roth (2023) bound the effect under restricted violations; with only 2-3 post years and leads moving by 2-3 log points, any informative restriction would be strong.

**Logs with zeros.** For y ≥ 0 with many zeros, log(1 + y) is not scale invariant: changing units (ha vs m²) changes the estimate, and the "effect" mixes the extensive margin (0 → positive) with the intensive margin (Chen and Roth 2024). Units with y = 0 in every year contribute nothing to α_i except a constant and pin the year effects toward zero.

**Randomization inference with targeted assignment.** Fisher's exact test of the sharp null τ_it = 0 is valid if, under the null, the observed assignment is one draw from a known, exchangeable assignment mechanism. Permuting dates across *all* units assumes any territory could have been chosen. Operations were sent to the largest, fastest-growing fronts, so this exchangeability fails by design. A weaker design-based version (Athey and Imbens 2022) keeps the treated set fixed and permutes only the timing; that still requires the order of operations to be as if random. With 7-8 treated units, the permutation distribution is coarse (MacKinnon and Webb 2020).

**Product and collection consistency.** A remote-sensing series is a model output. A new collection reclassifies the whole history, so differences between collections are not changes on the ground. Mixing collections across units, or using one product to select units and another to measure them, induces measurement error that is correlated with selection.

## 6. Our example

### 6.1 Three designs as coded

| | A12 · 2×2 | A13 · before/after vs pool | A14 · staggered DiD |
|---|---|---|---|
| Code | `brazil.py:104-253` | `brazil_stagger.py:44-68` | `brazil_v2.py:64-99`, units `brazil_raster.py:32-46` |
| Units | Yanomami vs Kayapó / Munduruku / others (22 territories with a mining row) | Yanomami; Munduruku + Sai-Cinza; Kayapó; Sararé; pool of 18 | 24 territories (AMW new area ≥ 50 ha, `brazil_raster.py:36-37`) |
| Outcome | net annual addition (ha), MapBiomas Brazil Col 10.1 workbook | AMW new mining area (ha) by detection year | ln(1 + first-time mined ha), MapBiomas Brazil Col 11 rasters |
| Years | pre 2020-22, post 2023-24 (`brazil.py:24`) | 3 years before op year vs op year to 2025 (2025 provisional) | 2014-2025 |
| Treatment | Yanomami Feb 2023 | each group's coded date, calendar year (`brazil_stagger.py:37-38`) | first verified op 2021-25, Jul-Dec → next year (`brazil_v2.py:59-61`) |
| Inference | none | none | CRV1 by territory; RI 2,000 shuffles on TWFE (`brazil_v2.py:86-98`) |
| Registered result | `br_did_main_vs_Kayapo_ha_yr` +904.8; `_pct` −4.37 | `bs_yan_gap_logpts` −1.86, `bs_mun_gap_logpts` −3.62, `bs_kay_gap_logpts` −2.02 | `brv2_twfe_treat` +0.293 (p 0.389), `brv2_did2s_treat` +0.256 (p 0.439), `brv2_ri_p` 0.728 |

### 6.2 Treatment dates as coded (A14)

The package rule (`brazil_v2.py:31-53`): first *verified* operation inside the systematic search window 2021-2025, from `data_intermediate/operations_coded.csv`; unverified snippets replaced by the next verified operation (`UNVERIFIED`, `brazil_v2.py:35-38`); earlier operations shown but not coded (`OTHER_OPS`, line 39).

| Territory | Coded date | First treated year (v2) | Notes |
|---|---|---|---|
| Yanomami | 2023-02 | 2023 | verified |
| Baú | 2022-07 | 2023 | police "Operação Mercúrio", 3 days |
| Munduruku, Sai-Cinza | 2023-08 (2021-05 overridden) | 2024 | May 2021 Op. Mundurukânia: snippets only |
| Apyterewa, Trincheira Bacajá | 2023-10 | 2024 | desintrusão of mainly cattle invaders |
| Kuruáya | 2023-12 | 2024 | Ibama + PF, 3 days |
| Kayapó | 2024-09 | 2025 | Oct 2017 raid not coded; **Jun 2023 PF action (verified, `enforcement_timeline.md:28`) not coded** |
| Sararé | 2024-09 | 2025 | |
| Parque do Aripuanã, Roosevelt | 2025-03 | 2025 | Operation Golden Border |

### 6.3 Data lineage

- **Col 11 rasters → `data_intermediate/brazil_raster_unit_year.csv`** (`brazil_raster.py:49-100`): class 30 pixels inside FUNAI polygons; first-time = mined in t and never in the history read (1985, 1990, 1995, 2000, 2001-2025). The FUNAI polygons and rasters are git-ignored; only the intermediate is present.
- **Col 10.1 workbook** `data_raw/mapbiomas_brazil/MAPBIOMAS_BRAZIL-COVERAGE_STATISTICS-COL.10.1-INDIGENOUS_TERRITORIES_STATE_BIOME.xlsx`, class 30 rows summed by geocode (`brazil.py:73-86`).
- **AMW** `data_intermediate/amw_candidates_year.csv` (raw geojson git-ignored).
- **DETER** `data_intermediate/deter_ti_month.csv`; **IBAMA** `data_intermediate/ibama_autos_annual.csv` (raw zip absent).

## 7. Tests run and results

All numbers below come from `code/review/s12_brazil_checks.py` or the registered ids named.

### T1 · Reproduce A14

TWFE +0.293 (p 0.389), did2s +0.256 (p 0.439), RI p 0.728: all equal `brv2_*` in `output/numbers.csv`. My own two-stage implementation (stage 1 least squares on untreated cells) gives +0.256 as well. 11 treated, 13 never treated. Four treated units have one post year only (first treated 2025): Kayapó, Parque do Aripuanã, Roosevelt, Sararé.

### T2 · 13 of 24 territories have zero mapped mining in every year (audit lead 1, confirmed)

| Fact | Value |
|---|---|
| Territories with MapBiomas Col 11 mining = 0 in every year 2014-2025 | **13 of 24** |
| Of which treated | 3 (Kuruáya, Roosevelt, Trincheira Bacajá) |
| Of which never treated | 10 of the 13 never-treated |
| AMW new area 2019-25 in those 13 | 69 to 3,370 ha each (Aripuanã 3,370; Trincheira Bacajá 2,340) |
| Col 10.1 workbook mining rows for those 13 | none (12 have rows for other classes; Aracá-Padauiri is absent) |

So both MapBiomas collections agree that these territories hold no mining. The zeros are not a pipeline bug. **Units were selected with one product (AMW) and measured with another (MapBiomas), and the two disagree about whether there is any mining at all.** The same 13 units drop if the sample is chosen on pre-period MapBiomas mining (any mining 2014-18), so "mining units" is a pre-treatment definition.

| Sample | TWFE | did2s |
|---|---|---|
| All 24 (as coded) | +0.293 (p 0.389) | +0.256 (p 0.439) |
| 11 units with mining (8 treated) | **−0.217 (p 0.704)** | **−0.369 (p 0.575)** |

The sign flips. Neither is distinguishable from zero.

### T3 · Event study with leads (audit lead 2, confirmed)

**T3a · Raw means of ln(1 + first-time ha).**

| Year | 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Treated (all 24) | 1.11 | 1.10 | 1.30 | 1.85 | 2.02 | 2.26 | 3.72 | 3.53 | 3.15 | 3.39 | 2.88 | 3.01 |
| Never treated (all 24) | 0.37 | 0.26 | 0.51 | 0.47 | 0.33 | 0.28 | 0.42 | 0.35 | 0.29 | 0.27 | 0.40 | 0.65 |
| Treated (mining units) | 1.52 | 1.52 | 1.79 | 2.54 | 2.78 | 3.11 | 5.12 | 4.85 | 4.33 | 4.66 | 3.96 | 4.14 |
| Never treated (mining units) | 1.60 | 1.15 | 2.23 | 2.03 | 1.44 | 1.21 | 1.82 | 1.52 | 1.24 | 1.18 | 1.75 | 2.80 |

By event time (treated, mining units): 2.13 at e = −11, rising to **5.15 at e = −2**, then 4.46 (−1), 4.43 (0), 3.24 (+1), 3.47 (+2). The treated territories boomed for a decade and were operated on at or after the peak. The never-treated stayed flat.

**T3b · Event-study coefficients (reference e = −1; e binned at −6 and +2).**

| e | ≤ −6 | −5 | −4 | −3 | −2 | 0 | +1 | +2 |
|---|---|---|---|---|---|---|---|---|
| did2s, all 24 | −0.51 (p 0.001) | +0.10 | +0.34 | +0.63 (p 0.002) | +1.01 (p 0.005) | +0.55 | −0.23 | +0.35 |
| did2s, mining units | −0.40 (p 0.04) | −0.01 | +0.19 | +0.47 (p 0.06) | +1.03 (p 0.02) | +0.15 | −1.06 | −0.72 |
| TWFE dummies, all 24 | −1.88 (p 0.004) | −0.91 | −0.40 | +0.10 | +0.52 (p 0.08) | −0.20 | −1.05 (p 0.05) | −0.66 |

Leads are large and move steadily. **Parallel trends fail.** (did2s leads are relative to the imputed counterfactual; TWFE leads relative to e = −1; both say the same thing.)

**T3c · Callaway and Sant'Anna by hand (never-treated control, base g − 1).**

| Sample | Overall post ATT | Leads e = −9 … −2 |
|---|---|---|
| All 24 | **−0.59** | −2.02, −2.06, −1.65, −1.35, −0.63, −0.11, +0.22, +0.53 |
| Mining units | **−1.41** | −2.96, −3.13, −2.58, −1.92, −0.92, −0.23, +0.24, +0.81 |

Same data, same never-treated comparison, opposite sign to did2s. This is §5.2's baseline problem in practice: Callaway and Sant'Anna use the peak year g − 1 as the base, the imputation estimator uses the average of a decade of rising pre-years. With a boom before treatment, the first looks like a fall and the second like a rise. Neither is credible.

### T4 · TWFE weights (de Chaisemartin and D'Haultfœuille)

| Sample | Treated cells | Negative weights | Weight by cohort 2023 / 2024 / 2025 |
|---|---|---|---|
| All 24 | 20 | **0** | 0.31 / 0.50 / 0.20 |
| Mining units | 15 | **0** | 0.45 / 0.39 / 0.17 |

No negative weights: all cohorts start late (2023-25) and 13 of 24 units are never treated, so the forbidden comparisons carry little weight. TWFE and did2s agree (+0.29 vs +0.26). **The "TWFE fails with staggered timing" problem is real in general but is not what drives the Brazil result. The pre-trend is.**

### T5 · Treatment dating (audit lead 3, reproduced)

| Variant | Treated | TWFE (all 24) | did2s (all 24) | TWFE (mining) | did2s (mining) |
|---|---|---|---|---|---|
| Coded (package rule) | 11 | +0.29 | +0.26 | −0.22 | −0.37 |
| Calendar-year mapping (as `brazil_stagger`) | 11 | +0.49 | +0.44 | +0.13 | −0.02 |
| Kayapó 2023-06 (verified PF action: the code's own rule) | 11 | +0.27 | +0.22 | −0.33 | −0.49 |
| Kayapó 2017-10 (raid) | 11 | +0.43 | +0.41 | −0.12 | −0.35 |
| Munduruku + Sai-Cinza 2021-05 | 11 | **+0.62** | +0.55 | +0.16 | −0.10 |
| Munduruku 2021-05 and Kayapó 2023-06 | 11 | +0.58 | +0.50 | +0.06 | −0.23 |
| Drop ranch desintrusões (Apyterewa, Trincheira Bacajá) | 9 | +0.46 | +0.43 | −0.11 | −0.23 |
| Drop treated with one post year | 7 | +0.21 | +0.17 | +0.02 | −0.20 |
| Drop Munduruku + Sai-Cinza (doubtful date) | 9 | +0.44 | +0.42 | −0.02 | −0.09 |
| **Proposed R\*** (Kayapó 2023-06, ranch dropped) | 9 / 7 | +0.41 | +0.37 | −0.26 | −0.37 |
| Yanomami the only treated unit | 1 | +1.59 | +1.59 | +1.33 | +1.33 |

Across the ten multi-unit variants and both samples: **−0.49 to +0.62**, with every p-value above 0.12. The sign depends on the sample more than on the dates: positive with the 13 zero units, mostly negative without them. Yanomami alone is strongly positive because its 2023-25 first-time mining (922, 279, 173 ha) stays above its 2014-18 level, which is the boom problem again.

Two inconsistencies confirmed:
- **Kayapó.** The package rule is "first verified operation 2021-25". The Jun 2023 PF action is verified (page opened, `docs/overnight/notes/enforcement_timeline.md:28`) and inside the window, so the rule itself gives 2023-06, not 2024-09. `operations_coded.csv` does not list it.
- **Munduruku.** The May 2021 snippet is enough to *exclude* Munduruku as a Peru twin (`control_top3.py:23-25`, S10) but not enough to *date* it here (`brazil_v2.py:35-38`). Each use, on its own, errs on the cautious side; together they treat the same evidence two ways.

Year mapping also differs: `brazil_v2.py:59-61` maps Jul-Dec to the next year, `brazil_stagger.py:30-38` uses the calendar year, and `brazil.py:42-47` and `brazil_deter.py:107-113` hard-code their own event lines.

### T6 · Randomization inference

| Statistic, sample | Real | One-sided p | Fakes 5 / 50 / 95% |
|---|---|---|---|
| TWFE, all 24 (as coded) | +0.29 | 0.728 | −0.64 / −0.10 / +0.81 |
| did2s, all 24 | +0.26 | 0.696 | −0.67 / −0.10 / +0.84 |
| TWFE, mining units | −0.22 | 0.401 | −1.42 / +0.05 / +1.35 |
| did2s, mining units | −0.37 | 0.348 | −1.68 / +0.18 / +1.42 |
| did2s, mining units, timing-only shuffle | −0.37 | 0.227 | |

The coded RI permutes dates over all 24 units, half of which have no mining, so most fakes compare zeros with zeros. Restricting to mining units roughly doubles the spread of the fakes. More fundamentally, assignment was targeted at booms, so no permutation scheme over these units is "as if random". RI here only says the estimate is not unusual among arbitrary relabelings; it cannot support a causal reading either way.

### T7 · Never-treated pools (audit lead 4, confirmed)

**A14.** Of the 13 never-treated: 2 searched with nothing found (Menkragnoti, Sawré Muybu; S10 proposes recoding both "unclear, searched 2022-25 only"), 1 unclear (Tenharim do Igarapé Preto), **10 never searched**. Ten of the 13 also have zero mapped mining.

**A13.** The AMW pool has 18 territories: 3 searched (none), 1 unclear, **14 never searched**. Aripuanã holds **57.9%** of the pool's 2023-25 new area (`bs_pool_top_share_2023_25`), 547 ha in 2024 and 1,602 ha in 2025 (provisional), while MapBiomas Col 11 maps **zero** mining there in every year. Its centroid is 90 km from Roosevelt and 111 km from Parque do Aripuanã, both hit by Operation Golden Border in Mar 2025 (centroid distance; a displacement destination is plausible, not shown).

| A13 gap (treated minus pool, log points) | With Aripuanã (as coded) | Without Aripuanã |
|---|---|---|
| Yanomami | −1.86 | −1.30 |
| Munduruku + Sai-Cinza | −3.62 | −3.06 |
| Kayapó | −2.02 | −0.95 |
| Sararé | +0.31 | +1.38 |

Pool change for the 2024 window: +179% with Aripuanã, **−4%** without. "Where no operation came, mining grew" (`brazil_stagger.py:95`) rests on one unsearched territory that MapBiomas says has no mining. The treated groups still fell relative to the remaining pool, but Munduruku's fall started in 2022, before its operation (`bs_mun_first_below_half` = 2022).

### T8 · Products disagree on level and timing (audit lead 5, confirmed)

**Yanomami (ha).**

| | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 |
|---|---|---|---|---|---|---|---|---|
| Col 10.1 stock | 364 | 667 | 1,341 | 1,956 | 3,573 | 4,397 | 4,576 | |
| Col 11 stock (raster) | 1,682 | 1,885 | 2,363 | 2,751 | 3,682 | 4,627 | 4,936 | 5,127 |
| Col 10.1 net addition | 257 | 303 | 674 | 615 | **1,617** | **824** | **179** | |
| Col 11 first-time | 190 | 208 | 490 | 423 | **953** | **922** | **279** | 173 |
| AMW new area | 1,517 | 2,295 | 1,078 | 3,011 | **8,570** | **3,961** | **496** | 190 |
| DETER alerts (ha) | 0 | 198 | 113 | 126 | **190** | **389** | **103** | 49 |

The fall comes in 2023 (Col 10.1, AMW), in 2024 (Col 11), or after a 2023 *rise* (DETER, dated by detection). AMW's 2022 new area is 9 times Col 11's first-time area.

**Col 11 / Col 10.1 stock ratio.**

| Territory | 2018 | 2022 | 2024 |
|---|---|---|---|
| Yanomami | **4.62** | 1.03 | 1.08 |
| Munduruku | 1.08 | 0.69 | **0.59** (4,685 vs 7,909 ha) |
| Kayapó | 1.22 | 0.98 | 0.97 |
| Sawré Muybu | 0.90 | 0.51 | 0.46 |
| Baú | | 0.81 | 0.68 |
| Sararé | 0.98 | 1.03 | 0.99 |

Col 11 rewrites Yanomami's 2018 stock upward 4.6-fold, which turns a 10-fold Col 10.1 boom (364 → 3,573 ha) into a 2-fold one. Col 11 shows Munduruku's stock *falling* 2022-24 (net −448 ha in 2023) where Col 10.1 shows it rising. No check in the code compares the two collections per territory; the only Brazil raster check (`brazil_v2.py:107-108`) is Kayapó, where they happen to agree in 2022-24.

### T9 · IBAMA and the "weaker enforcement 2019-22" premise (audit lead 6)

| Mean autos per year, Legal Amazon | 2015-18 | 2019-22 | 2023-25 |
|---|---|---|---|
| All autos | 6,919.5 | 4,358.75 | 6,659 |
| Mining-flagged | 157.0 | 147.5 | 349 |
| Mining and indigenous text | 11.25 | **18.75** | 69 |
| Mining-flagged, Roraima | 5.0 | 10.25 | 47.7 |

All autos fell by 37%; mining autos by 6%; mining-in-indigenous-land autos *rose*. The mining share of autos rose from 1.4-3.8% (2015-18) to 2.2-4.6% (2019-22). Our own IBAMA data therefore do not show weaker *mining* enforcement in 2019-22. The premise needs an external citation (agent.md lists Nunes et al. 2024 on embargoes and confiscations in 2019-20; open it before citing).

The mining regex contains bare `lavra` (`brazil_ibama.py:23`). It matches "lavra" (mining) but also "lavrado" and "lavratura", the standard verbs for *issuing* an auto. A word boundary (`\blavra\b`) excludes them. The size of the error cannot be measured without the raw zip.

### T10 · A12, the 2×2 (audit lead 7, reproduced)

Pre 2020-22, post 2023-24 means (ha/yr, Col 10.1): Yanomami 969 → 501, Kayapó 2,586 → 1,214, Munduruku 1,641 → 238 (`br_ti_*_add_mean_*`).

| Comparison | ha/yr | pp of 2022 stock |
|---|---|---|
| vs Kayapó (main) | **+904.8** | **−4.37** |
| vs Munduruku | +936.0 | +5.80 |
| vs mean of 19 others | −469.3 | −14.19 |
| Placebo 2017-19 → 2020-22 vs Kayapó | −354.9 | +14.09 |

| Pre-window (post 2023-24, vs Kayapó) | ha/yr | pp |
|---|---|---|
| 2020-22 | +905 | −4.37 |
| 2019-22 | +883 | −0.91 |
| 2021-22 | +440 | −10.51 |
| 2016-22 | +616 | +3.75 |
| 2022 only | −585 | −27.85 |

Fake start years 2005-2021 (pre s−3…s−1, post s…s+1): in hectares the fakes run from −1,100 to +558; the real +905 is the most positive of 18. Yanomami's additions fell less than Kayapó's in hectares and more as a share of stock. The registered placebo divides a 2017-19 vs 2020-22 change by the 2022 stock (`brazil.py:111`), which is a post-period normaliser for a pre-period test. **The 2×2 is inconclusive on sign, as the code says.**

### T11 · What "Munduruku" means (audit lead 8, confirmed)

| Module | Units |
|---|---|
| `brazil.py` | geocode 29801 only (Col 10.1) |
| `brazil_stagger.py` | 29801 + 40901 Sai-Cinza (AMW) |
| `brazil_deter.py` | Munduruku + Sai-Cinza + Munduruku-Taquara (DETER) |
| `brazil_v2.py` | 29801 and 40901 as two separate treated units |
| `control_top3.py`, `control_select.py` | RAISG/AMW polygon "Munduruku territory" |

### Tests not possible here

- IBAMA regex with word boundary on the raw autos (zip not in the repo).
- Re-reading the Col 11 rasters with the polygons (FUNAI file and rasters git-ignored); in particular, checking AMW patches in Aripuanã and Trincheira Bacajá against the MapBiomas classes there.
- Searching operations for the 10 never-searched territories.

## 8. Assumption check

| Assumption | Verdict | Evidence |
|---|---|---|
| Parallel trends | **Fails** | Leads rise steadily to +1.0 log points at e = −2 (T3b); treated means triple 2014-20, never-treated flat (T3a) |
| No anticipation | Doubtful | Munduruku falls from 2022, before its Aug 2023 operation; emergency announced Jan 2023 before the Yanomami operation |
| No spillover | Unknown | Aripuanã surge next to Golden Border targets (T7); Yanomami rings show 0 → 0.39 ha/yr (`brv2_r0_10_*`), too small to judge |
| Correct dates | **Violated by own rule** | Kayapó Jun 2023 omitted; Munduruku 2021 handled two ways; three year-mapping rules (T5) |
| Common support | **Fails** | 13 of 24 units have no mapped mining (T2) |
| Same measurement | **Fails across modules** | A12 Col 10.1, A13 AMW, A14 Col 11; selection by AMW, outcome by MapBiomas; collections disagree up to 4.6-fold (T8) |
| RI exchangeability | **Fails by design** | Operations targeted booms; permutations include zero units (T6) |
| Staggered-timing bias (negative weights) | Holds | 0 negative weights (T4) |

## 9. Weaknesses, ranked

1. **Operations followed booms.** The treated territories rose for a decade and were operated on at the peak. Any decline afterwards is confounded with the end of the boom (and with Brazil's 2023 change in gold-trading rules, which hit all territories at once). No estimator in the code can separate the two.
2. **Half the panel has no outcome.** 13 of 24 territories have zero MapBiomas mining in every year. Including them makes the estimate positive; excluding them makes it negative.
3. **The registered sign is fragile.** −0.49 to +0.62 across defensible dates and samples; imputation and Callaway-Sant'Anna give opposite signs on the same data. "Wrong sign" over-reads a number with p = 0.44.
4. **Dates break the code's own rule** (Kayapó), treat one snippet two ways (Munduruku), and use three year-mapping conventions.
5. **Products disagree** on level (4.6-fold for Yanomami 2018) and timing (2023 vs 2024 vs a 2023 rise in DETER). The three Brazil designs each use a different product, so their results cannot be compared.
6. **The comparison pools were mostly never searched** (10 of 13; 14 of 18). A13's "the pool grew" is one unsearched territory with no MapBiomas mining.
7. **The enforcement premise is not shown by our data.** Mining autos did not fall in 2019-22.
8. **Mixed treatments.** Ranch desintrusões (Apyterewa, Trincheira Bacajá) and 3-day raids are pooled with the Yanomami operation; four treated units have one post year.

## 10. Proposed decisions

| # | Decision | Recommendation |
|---|---|---|
| D-S12-1 | **One dating rule for the package** | **R\*: treatment starts in the month of the unit's first verified operation against mining (source opened, listed in `operations_coded.csv`) inside the systematic search window (2017-25 for twin selection in S10 and S11, 2021-25 for A14 dating); for Peru the treatment is Mercurio (S0). Unverified snippets and operations found outside the search window are context (dashed lines), never treatment and never grounds for excluding a twin on their own (an unverified report makes a twin "unclear", shown as a sensitivity). Annual mapping: an operation starting Jan-Jun treats that year, Jul-Dec treats the next year; Peru (Feb 2019 → 2019) is unchanged. Federal removals of non-mining invaders (Apyterewa, Trincheira Bacajá) are dropped from both groups.** Read all event lines (`brazil.py:42-47`, `brazil_deter.py:107-113`, `brazil_stagger.py:37`) from `operations_coded.csv`. Under R\*: Kayapó = 2023-06 (first treated 2023); A14 = +0.41 / +0.37 (all units), −0.26 / −0.37 (mining units), all p > 0.25. |
| D-S12-2 | Sample | Keep only territories with MapBiomas mining before 2019 (the same 11 as "ever mining"); select and measure with one product. Report the 24-unit result only as a sensitivity. |
| D-S12-3 | Estimator and pre-trends | Never show a Brazil estimate without the event-study leads (T3b). Report did2s and Callaway-Sant'Anna side by side and say that they disagree because of the pre-trend. |
| D-S12-4 | RI | Drop the RI p-value from the walkthrough and brief, or restrict it to mining units with the did2s statistic and label it "relabeling check, not a test of the operations". |
| D-S12-5 | Products | Pick one product per question. A14 (Col 11 rasters) is the only Brazil design measured like Peru's pixel work; label A12 (Col 10.1) superseded. Add a registered Col 10.1 vs Col 11 per-territory comparison (T8 table). |
| D-S12-6 | A13 pool | Flag Aripuanã (AMW-only mining, unsearched, next to Golden Border targets); report the pool with and without it, and fix the figure title "where no operation came, mining grew". |
| D-S12-7 | IBAMA | Add `\b` around `lavra` and rebuild when the zip is available; stop using all-autos counts as evidence of weaker mining enforcement; cite an external source for the 2019-22 premise. |
| D-S12-8 | Unit definitions | One "Munduruku" definition (29801 + 40901 as a complex) across all modules. |
| D-S12-9 | Searches | Search the 10 never-searched A14 controls, or label them "not searched" in every table. |
| D-S12-10 | Brief | Remove the "wrong sign" clause (see §11). Brazil stays in backup slides (agent.md §15). |

## 11. Verdict

The code computes what it says: TWFE, did2s, RI and the 2×2 all reproduce. Staggered-timing bias is not the problem (no negative weights). The problem is design:
- operations were sent to territories at the peak of a decade-long boom, so parallel trends fail visibly;
- half the comparison territories have no mining on the outcome map;
- the dates, the products and the unit definitions differ across the three Brazil scripts.

Under any defensible choice the staggered estimate lies between −0.49 and +0.62 log points, never distinguishable from zero, and its sign depends mostly on whether the 13 no-mining territories are kept. **The Brazil designs cannot tell whether the operations reduced mining.** They can describe what happened.

Label: **description**.

**The brief may say:** "In Brazil, mining in the Yanomami, Munduruku and Kayapó territories had boomed for years and fell after 2022 [D]. Federal operations arrived at the peak, and Munduruku was already falling before its operation, so our data cannot separate the operations from the end of the boom [D]."

**The brief must not say:**
- "the staggered DiD gives the wrong sign" or any Brazil p-value as a test of the operations;
- "where no operation came, mining grew" (one unsearched territory, no MapBiomas mining);
- "enforcement weakened in 2019-22" on the strength of our IBAMA counts;
- any number that splices Col 10.1, Col 11, AMW or DETER.

## References

- Ashenfelter, O. (1978). Estimating the effect of training programs on earnings. *Review of Economics and Statistics* 60(1).
- Athey, S. and Imbens, G. (2022). Design-based analysis in difference-in-differences settings with staggered adoption. *Journal of Econometrics* 226(1).
- Borusyak, K., Jaravel, X. and Spiess, J. (2024). Revisiting event-study designs: robust and efficient estimation. *Review of Economic Studies* 91(6).
- Callaway, B. and Sant'Anna, P. (2021). Difference-in-differences with multiple time periods. *Journal of Econometrics* 225(2).
- Chen, J. and Roth, J. (2024). Logs with zeros? Some problems and solutions. *Quarterly Journal of Economics* 139(2).
- Conley, T. and Taber, C. (2011). Inference with "difference in differences" with a small number of policy changes. *REStat* 93(1).
- de Chaisemartin, C. and D'Haultfœuille, X. (2020). Two-way fixed effects estimators with heterogeneous treatment effects. *American Economic Review* 110(9).
- Gardner, J. (2022). Two-stage differences in differences. Working paper, arXiv:2207.05943.
- Goodman-Bacon, A. (2021). Difference-in-differences with variation in treatment timing. *Journal of Econometrics* 225(2).
- MacKinnon, J. and Webb, M. (2020). Randomization inference for difference-in-differences with few treated clusters. *Journal of Econometrics* 218(2).
- Rambachan, A. and Roth, J. (2023). A more credible approach to parallel trends. *Review of Economic Studies* 90(5).
- Roth, J., Sant'Anna, P., Bilinski, A. and Poe, J. (2023). What's trending in difference-in-differences? A synthesis of the recent econometrics literature. *Journal of Econometrics* 235(2).
- Sun, L. and Abraham, S. (2021). Estimating dynamic treatment effects in event studies with heterogeneous treatment effects. *Journal of Econometrics* 225(2).
