# S10 · Rule-based twins (attempt A10, Ruby's design)

*Method card 10 of the causal review (plan: `docs/causal_review_plan.md`). Code under review: `code/control_amw.py`, `control_elevation.py`, `control_mb_amazonia.py`, `control_select.py`, `control_top3.py`, and the AMW accounting in `code/spatial.py:72-82`. Data: `data_intermediate/operations_coded.csv`, `amw_candidates_*.csv`, `mb_amazonia_col6_mining.csv`; search log `docs/overnight/notes/control_interventions.*`. Test script: `code/review/s10_twin_checks.py` (read-only).*

---

## 1. In one sentence

Pick, by rules written down before looking at the result, one real place that looked like the treated place before the treatment but was not treated, and read its path afterwards as "what would have happened".

## 2. Simple version

A doctor wants to know whether a new diet helped one patient. She cannot run a trial with one patient. So she looks through her files for a **twin**: someone of the same age, weight and blood pressure *before* the diet, who did not take it. She writes the matching rules first ("same age ± 5 years, same weight class, no diet"), then opens the files. If the twin's weight kept rising while her patient's stopped, that is suggestive.

Three things can spoil it:
- **Wrong rules.** If one rule quietly uses what happened *after* the diet (say "patients who later went to hospital"), the twin is chosen on the outcome.
- **The twin was treated too, or the opposite way.** If the twin went on a high-sugar binge at the same time, the gap overstates the diet.
- **One twin is one story.** A single comparison cannot tell a real effect from the normal difference between two people.

Ruby's design is exactly this, for La Pampa: four rules, applied to 1,174 protected areas, buffer zones and indigenous territories across the Amazon, to find an area that mined like Tambopata before 2019 but saw no operation.

## 3. When to use it, and when not

**Use it when:**
- there is one treated unit and no natural comparison group nearby;
- you can state, before seeing outcomes, which pre-treatment traits matter;
- the outcome is measured the same way for both units;
- you want a transparent comparison a non-specialist can audit (each rule is one line).

**Be careful or avoid it when:**
- the candidates sit in another country, with its own policy shocks in the same years;
- "untreated" is coded from news searches, so absence of evidence stands in for evidence of absence;
- the pre-treatment traits are measured in a different product or collection from the treated unit;
- the treated unit is at an extreme (largest, densest, fastest-growing), so no twin can be close. Then the twin is a case study, not a counterfactual.

## 4. Assumptions

| Assumption | In words | Formally |
|---|---|---|
| **Selection on pre-treatment traits only** | The rules use only what was known before 2019 | Rule set R is a function of X_i,t<2019 and not of Y_i,t≥2019 |
| **Twin untreated** | The twin had no enforcement change in 2019-21 (no operation, and no general enforcement shift) | D_twin,t = 0 for t in 2019-21 |
| **Twin's path = treated's counterfactual** | Without Mercurio, Tambopata would have grown at the twin's pace (here: in % of own 2018 stock) | E[Y_T,t(0) / S_T,2018] = E[Y_twin,t / S_twin,2018] |
| **Comparable measurement** | The outcome and the scale rule mean the same thing in both places | same product, same accounting, same detection bias |
| **No spillover** | Mercurio did not change the twin | Y_twin,t = Y_twin,t(0) |
| **No interference from the search** | Being "in the news" is unrelated to the twin's mining path | coding error independent of Y |

## 5. The maths

### 5.1 Master's level

The design is the **method of difference** (Mill 1843) used in comparative politics as the **most-similar-systems design** (Przeworski and Teune 1970; Lijphart 1971): two cases alike on everything that matters except the treatment. Seawright and Gerring (2008) call the case-selection version "most-similar case selection".

With one treated unit T and one twin C, the estimator in `control_select.py:71-77` is a post-period difference in paces:

  gap = p̄_T,2019-21 − p̄_C,2019-21,  where p_i,t = 100 × new_i,t / stock_i,2018

and the ratio p̄_T / p̄_C. Because the pace divides by each area's own 2018 stock, it is a **proportional** comparison: it assumes equal growth *rates*, not equal hectares (Roth and Sant'Anna 2023 on scale dependence; see S2 §5.2).

With several twins pooled, `control_top3.py:58` uses the **unweighted mean of paces**; a stock-weighted pool would weight Tapajós (167,341 ha) seven times more than Amanã.

Note that the gap is **post-only**: there is no "before" term, because Amazon Mining Watch (AMW) starts in 2018 (the 2018 value is the stock already present). Pre-period similarity is checked separately, on MapBiomas.

### 5.2 PhD level

**Selection on pre-treatment traits vs on outcomes.** A rule that uses post-treatment information is a form of conditioning on a post-treatment variable (Rosenbaum 2002, ch. 3; Imbens and Rubin 2015, ch. 12). Rule R2b ("no operation 2017-21, or first operation from 2022") is pre-treatment by date for 2019-21, but if operations from 2022 were *triggered* by fast mining in 2019-21, then R2b selects twins with high Y_2019-21(0). The gap is then biased away from zero. This is the logic of the "Ashenfelter dip" in reverse (Ashenfelter 1978): units enter or avoid treatment because of their outcome path.

**Regression to the mean and convergence.** Tambopata was a young boom: its MapBiomas stock grew 1,009 → 12,926 ha in 2010-18. Young booms decelerate (log growth falls as the base grows, and S1/S8/S13 show La Pampa was already 18-21% mined by 2018, on three definitions). A twin that is at a different stage of its boom has a different counterfactual growth path even with the same 2018 stock. A linear trend in the growth difference is one crude correction; it is very sensitive to the fitting window (T6).

**The n = 1 problem.** With one treated unit and one or two twins there is no sampling distribution for the gap. A Welch test on three annual values per area (`control_top3.py:53`) treats years as independent draws, which they are not, and says nothing about the design. Valid inference needs many comparison units and a placebo (each candidate in turn plays "treated"; Abadie, Diamond and Hainmueller 2010; Conley and Taber 2011). Ruby's rules deliberately produce one or two units, so no placebo is possible: the design is a **comparative case study**, labelled description.

**Cross-product comparability.** The twin rules use AMW (480-m patches, overlap-free union; `spatial.py:72-82`) for scale and outcome, and MapBiomas (30-m pixels) for pre-trends. Patch-based products overstate scattered mining more than dense mining, so "same AMW stock" does not mean "same mined land". And because AMW new area excludes infill inside earlier patches (S1), a dense area's new mining is under-counted relative to a scattered one's.

**Synthetic control as the formal version.** A weighted twin chosen to fit the pre-period path (Abadie, Diamond and Hainmueller 2010) is the formal descendant of this design. It needs a pre-period on the *same* outcome measure, which AMW does not have.

## 6. Our example

### 6.1 The rules as coded

| Rule | Intent (Ruby) | As coded | Where |
|---|---|---|---|
| Universe | All protected areas, buffer zones and indigenous territories with polygons | 1,174 areas (SERNANP Peru, RAISG other countries and Brazilian conservation units, FUNAI territories); 108 have any AMW mining | `control_amw.py:142-167` |
| R1 mining before 2019 | Real mining existed | AMW 2018 stock ≥ 500 ha | `control_select.py:53` |
| R2 no operation | Untreated | verdict "none" in `operations_coded.csv` for 2017-25 | `control_select.py:54` |
| R2b relaxed | Untreated during Mercurio's years | "none", or "yes" with first operation ≥ "2022" (string compare) | `control_select.py:55` |
| R3 far away | No displacement from La Pampa | outside a lon/lat box around Madre de Dios (Peru only) | `control_select.py:56-57` |
| R4 geographic twin | Lowland alluvial mining of similar scale | median elevation of AMW patch centroids < 500 m, and AMW stock ≥ 0.2 × Tambopata's 21,362 = 4,272 ha | `control_select.py:58` |
| Ranking | Closest twin first | \|log elevation ratio\| + \|log stock ratio\| | `control_select.py:60` |

### 6.2 Variables

| Variable | Definition | Source | Engineering | Where |
|---|---|---|---|---|
| `stock_2018` | AMW mining present when the series starts | Amazon Mining Watch (2026-10-03 release, git-ignored) | patch centroids within polygon; union of patches per onset year minus earlier years; 2018 = stock | `control_amw.py:174-197`, `spatial.py:72-82` |
| `new_ha` (2019-25) | AMW new area per onset year | same | same; 2025 provisional | same |
| `elev_median_m` | median SRTM 90 m elevation of up to 15 sampled patch centroids (onset ≤ 2019) | OpenTopoData API (raw JSON in `data_raw/opentopodata/`) | seed 0 sample | `control_elevation.py:27-66` |
| `verdict`, `first_op` | operation reported 2017-25, first date (YYYY-MM) | our logged web searches | hand-coded | `operations_coded.csv`, log `control_interventions.csv` |
| MapBiomas index | mining area, 2018 = 100 | MapBiomas Peru Col 4 (Tambopata BZ, pack table) / MapBiomas Amazonía Col 6 (twins, class 30) | sum rows per unit | `control_select.py:218-233`, `control_top3.py:36-43`, `control_mb_amazonia.py` |

### 6.3 Results as published

| Number | Value | Id |
|---|---|---|
| Areas screened / pass R1 / R1+R2 / +R3 / all four | 1,174 / 31 / 2 / 2 / **0** | `ctl_n_areas`, `ctl_n_r1`..`ctl_n_r4` |
| Pass with R2b | 2: Amanã National Forest, Tapajós Environmental Protection Area (both Brazil) | `ctl_n_relaxed` |
| Tambopata BZ pace 2019-21 | 7.90% of 2018 stock per year | `top3_tam_during` |
| Amanã / Tapajós pace | 20.91 / 18.37 | `top3_amana_twin_during`, `top3_tapajos_twin_during` |
| Ratio (Amanã only) | 0.378 | `ctl_relaxed_during_ratio` |
| Ratio (mean of the two twins' paces) | 0.402 | `top3_ratio` |
| Pre-trend, mean growth gap 2010-18 (p) | Amanã +0.195 (0.081); Tapajós +0.236 (0.017) | `top3_*_pre_growth_diff`, `_p` |
| Pre-trend, slope test p | Amanã 1.1e-5; Tapajós 4.3e-4 | `top3_*_pre_trend_p` |

## 7. Tests run and results

### T1 · Reproduce

Every number in §6.3 reproduces exactly. The stock-weighted pooled pace would be 18.69%, giving a ratio of 0.423. **Two different "twin" headline numbers circulate**: 38% (Amanã alone; agent.md §14) and 40% (two-twin mean; walkthrough). The range across the two twins and the two pooling choices is 0.38-0.43.

### T2 · Who fails which rule (the 31 areas with ≥ 500 ha)

| Status among R1 areas | Count |
|---|---|
| operation reported ("yes") | 22 |
| "unclear" | 7 |
| "none" | 2 (Apolobamba, Bolivia; Sawré Muybu, Brazil) |

- **Strict result = 0** because the only two "none" areas fail R4. Apolobamba is highland (586 m) and small (717 ha). Sawré Muybu is small (871 ha vs the 4,272 ha cut-off).
- **The closest area of all is Kayapó** (AMW stock 17,876 ha, elevation 258 m). It fails only R2, because of a three-day Ibama operation in October 2017 ("12 diving rafts and 12 excavators destroyed", Ibama news 2017-10-24, `operations_coded.csv`). Its 2019-21 pace was 28.8%; as a twin it would give a ratio of 0.27.
- Munduruku (8,832 ha, 137 m) fails R2b because of Operation Mundurukânia in May 2021 (search snippets, unverified). Its pace was 105.4%.

### T3 · R2b's string comparison

All 36 non-empty `first_op_2017_2025` values have the form YYYY-MM, and no "yes" row lacks a date. So `first_op >= "2022"` (`control_select.py:55`, also `control_psm.py:67-68`) is **a correct year test on the current data**. It is fragile: a value like "2021/12" or a year-only entry would sort differently. Not a bug today.

### T4 · Coding check: three territories searched for 2022-25 only (lead 4, reproduced)

| Territory | Coded | ops_text | AMW 2018 stock | Effect |
|---|---|---|---|---|
| Sawré Muybu (BR-TI-56701) | none | "No operation found 2022-2025 (searched 2022-2025 only)" | 871 ha | passes R1, R2 (as coded), R3; fails R4 size. **Sits in the S11 matching pool** |
| Menkragnoti (BR-TI-28701) | none | same | 41 ha | fails R1 |
| Enawenê-Nawê (BR-TI-11201) | none | same | 47 ha | fails R1 |

None of the three appears in `control_interventions.csv`. They were never searched for 2017-21, so "none 2017-25" is a coding error. Recoded as "unclear": **R1+R2 drops from 2 to 1** (`ctl_n_r2`); strict (0) and relaxed (Amanã, Tapajós) are unchanged. The S11 consequences are in card 11.

### T5 · Does R2b select on outcomes? (lead 2)

AMW 2019-21 pace (% of own 2018 stock) of the 31 R1 areas, by operation timing:

| Group | n | Median pace | Mean pace |
|---|---|---|---|
| operation 2017-21 | 11 | 22.2 | 27.4 |
| first operation 2022 or later | 11 | 18.4 | 39.2 |
| none found | 2 | 19.8 | 19.8 |
| unclear / not searched | 7 | 15.9 | 26.8 |

At the median, areas targeted from 2022 were **not** faster in 2019-21 than the others. The high mean comes from two areas (Yanomami 140%, Jamanxim National Forest 146%), both of which fail R4. The twins themselves (20.9 and 18.4) sit at the median of all mining areas. **The selection-on-outcome risk is real in principle but does not show in this sample** [D].

### T13 · Tambopata against every mining area, whatever its status

Tambopata's 7.9% is slower than 26 of the other 31 areas with ≥ 500 ha (median 18.4%). The five slower ones are the Tambopata National Reserve (also treated), Brownsberg, Tenharim do Igarapé Preto, Mapinguari and Sawré Muybu. Pace is not related to size in this group (log pace on log stock: slope +0.13, p = 0.49), and the fitted pace at Tambopata's stock is 23.0%, a ratio of 0.34.

So **the "Tambopata was slow in 2019-21" finding does not depend on which twin is picked**. This is description, and it includes treated areas in the comparison.

### T6 · Pre-trends and the trend-adjusted gap (lead 5, reproduced, with a caveat)

MapBiomas mining area, each from its own collection (ha):

| | 2010 | 2012 | 2014 | 2016 | 2018 | 2019 | 2020 | 2021 |
|---|---|---|---|---|---|---|---|---|
| Tambopata BZ (Peru Col 4) | 1,009 | 3,315 | 6,544 | 8,714 | 12,926 | 13,343 | 13,524 | 13,413 |
| Amanã (Amazonía Col 6) | 1,163 | 1,390 | 1,965 | 2,819 | 4,127 | 4,695 | 5,248 | 6,807 |
| Tapajós (Amazonía Col 6) | 12,409 | 16,006 | 21,138 | 26,794 | 32,342 | 34,813 | 37,801 | 45,567 |

Yearly log-growth gap (Tambopata minus twin), 2010-18: Amanã 0.48, 0.85, 0.16, 0.24, 0.10, 0.04, −0.11, 0.04, −0.02; Tapajós 0.54, 0.83, 0.10, 0.25, 0.15, 0.09, −0.04, 0.14, 0.06.

- **The "Tambopata grew faster" result is driven by 2010-11**, when Tambopata BZ held 1,009-2,572 ha (small-base growth). On 2014-18 the mean gap is +0.007 (p = 0.80) against Amanã and +0.082 (p < 0.01) against Tapajós.
- **The gap was closing**: slopes −0.086 (Amanã) and −0.073 (Tapajós) log points per year.

Lead 5 reproduces exactly with the 2010-18 trend: predicted 2019-21 gaps Amanã −0.24 / −0.32 / −0.41 vs actual −0.10 / −0.10 / −0.27; Tapajós −0.13 / −0.20 / −0.28 vs −0.04 / −0.07 / −0.20. **But the answer depends on the fitting window:**

| Trend window | Amanã: actual − predicted, mean 2019-21 | Tapajós: actual − predicted |
|---|---|---|
| 2010-18 | +0.17 (Tambopata better than its trend) | +0.10 |
| 2012-18 | −0.01 | −0.11 |
| 2013-18 | +0.02 | −0.07 |
| 2014-18 | −0.06 | −0.13 |

Against Amanã, the 2019-21 gap is about what the converging trend predicts, for any window. Against Tapajós, a gap of −0.07 to −0.13 log points per year remains once the early small-base years are dropped. **Trend-adjusted, the twin evidence ranges from "no effect" to "a modest fall"**; the 2010-18 version ("Tambopata did better than predicted") rests on two small-base years.

### T11 · Did the twins speed up in 2019-21? (lead 1)

Own log growth per year, MapBiomas (each unit in its own collection):

| | 2013-15 | 2016-18 | 2019-21 | 2021-23 |
|---|---|---|---|---|
| Tambopata BZ | +0.294 | +0.160 | **+0.012** | +0.135 |
| Amanã | +0.170 | +0.193 | +0.167 | +0.077 |
| Tapajós | +0.130 | +0.104 | +0.114 | +0.066 |

The twins kept roughly their 2016-18 pace in 2019-21; Tambopata's growth stopped. In growth terms the before/after difference is −0.12 log points per year against Amanã and −0.16 against Tapajós [D]. So the gap comes from Tambopata falling, not from the twins accelerating.

This does not clear lead 1. Brazil's federal enforcement weakened in 2019-22. Our own Ibama data show all Legal Amazon infraction notices falling from 6,920 to 4,359 per year (`br_ibama_aml_mean_2015_2018`, `_2019_2022`), while mining-flagged notices barely moved (157 → 147.5; `br_ibama_mining_aml_mean_*`). The twins might otherwise have slowed, as their 2021-23 growth did after their own March 2023 operation. **The twins are plausibly treated in the opposite direction; the size of that bias is unknown; its sign makes the gap too large.**

### T7 · Cross-product scale (lead 6, reproduced)

| Area | AMW 2018 stock | MapBiomas 2018 stock | AMW / MapBiomas |
|---|---|---|---|
| Tambopata BZ | 21,362 | 12,926 (Peru Col 4) | **1.65** |
| Amanã | 23,916 | 4,127 (Amazonía Col 6) | **5.80** |
| Tapajós | 167,341 | 32,342 (Amazonía Col 6) | **5.17** |

- On AMW, Amanã is Tambopata's size (1.12×). On MapBiomas it is a third (0.32×). Both twins still pass R4 on MapBiomas (0.32 and 2.50 against the 0.2 cut-off). So the twin choice survives, but **"similar scale" depends on the product.**
- AMW patches inflate scattered mining (as in the Tapajós garimpos) far more than dense mining (La Pampa). Because AMW's overlap-free accounting does not count infill inside earlier patches (S1), dense areas also show less "new" mining. Plausibly this lowers Tambopata's pace relative to the twins. The direction is not proven here.

### T8 · Same land, two collections (lead 7)

`control_top3.py:47` subtracts a Peru Col 4 growth rate from an Amazonía Col 6 growth rate. That breaks agent.md rule 7. To see how much it matters, I compared the two collections on the **same land**: Tambopata National Reserve (geocode 47011 in Col 6; `output/peru_anp_mining_levels_2010_2025.csv` for Col 4).

| | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 |
|---|---|---|---|---|---|---|---|---|
| Col 4 (ha) | 54.4 | 588.1 | 561.3 | 534.7 | 508.4 | 461.7 | 463.3 | 523.1 |
| Col 6 (ha) | 51.5 | 570.3 | 536.7 | 508.5 | 487.9 | 436.5 | 439.0 | 445.9 |

The mean log-growth difference 2011-18 is +0.001 per year (sd 0.027); the only large gap is 2023 (+0.11). **On this land, mixing collections in a growth comparison costs little before 2023.** It is still a rule break and should be stated as such. One small reserve is weak evidence for the much larger buffer zone.

### T9 · Sensitivity of the twin set to the cut-offs

| Change | Relaxed twins | Ratio (mean of paces) |
|---|---|---|
| Main (500 ha, 500 m, 0.2×) | Amanã, Tapajós | 0.40 |
| R1 at 250 or 1,000 ha | same | 0.40 |
| R4 elevation < 300, 700 or 1,000 m | same | 0.40 |
| R4 scale ≥ 0.33× or 0.5× | same | 0.40 |
| R4 scale ≥ 0.1× | + Urupadi, Canaima, Yapacana (5) | 0.43 |
| R4 scale ≥ 0.05× | 9 areas incl. Yanomami, Jamanxim Flona | 0.18 |

The twin choice is robust to every cut-off except a much looser size rule. That rule lets in young booms with paces above 140%.

### T10 · Twins outside Brazil

No area outside Brazil passes. Every non-Brazilian area with ≥ 500 ha AMW stock is below the 4,272 ha size cut-off (largest: Lucifer Dékou-Dékou 3,974 ha, status unclear). Peru has no area outside Madre de Dios with ≥ 100 ha of AMW mining. **A same-country twin does not exist**; any twin carries Brazil's (or Venezuela's) national shocks.

### T12 · Year by year (AMW pace, % of own 2018 stock)

| | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 |
|---|---|---|---|---|---|---|---|
| Tambopata BZ | 11.1 | 8.0 | 4.6 | 3.2 | 5.4 | 8.0 | 9.6 |
| Amanã | 19.0 | 17.9 | 25.8 | 25.7 | 17.5 | 7.4 | 6.6 |
| Tapajós | 19.6 | 16.0 | 19.6 | 21.4 | 15.0 | 8.7 | 6.2 |
| Amarakaeri BZ | 18.1 | 14.0 | 14.7 | 10.0 | 12.0 | 11.1 | 7.0 |

On AMW, Tambopata's 2019 pace is its highest after 2018, and its fall deepens through 2022 (consistent with X3: the decline is a 2020-22 story). After their own 2023 operations both twins fall below Tambopata (2024-25), so the twins cannot be used after 2022, as the code already says.

### T14 · Text checks (lead 8, reproduced; by grep, not in the script)

- `docs/overnight/methods_content.md:209` and `explainer_content.md:626` say "Tambopata grew faster than both twins before 2019 (p = `top3_*_pre_trend_p`)". That is the **slope** test (p 1.1e-5, 4.3e-4). It tests whether the gap was *changing*, not whether Tambopata grew *faster*. The level test gives p 0.081 and 0.017, and on 2014-18 p 0.80 and < 0.01 (T6).
- `control_top3.py` still calls the twins "three" (docstring, print header, `top3_pooled_during` description "Mean of the three twins", `top3_median_during` "Munduruku's pace is extreme, so the median is the headline"). With two twins the median equals the mean (both 19.64), so `top3_median_*` is redundant.
- `control_psm.py:18` says "the twin: 38%" while the walkthrough uses 40%.

### Tests not possible here

- **A MapBiomas-based twin choice for all 1,174 areas.** There is no crosswalk from AMW unit ids to MapBiomas Col 6 geocodes except by name. Only the two twins were checked (T7).
- **Recomputing AMW accounting** (patch density, infill): the AMW geojson is git-ignored and absent.
- **Searching the 2017-21 operation status** of Sawré Muybu and the 7 "unclear" areas needs new web searches.

## 8. Assumption check

| Assumption | Verdict | Evidence |
|---|---|---|
| Selection on pre-treatment traits | **Mostly holds** | R1, R3, R4 are 2018 or fixed traits. R2b uses post-2021 operations, but the selected twins sit at the median pace of all mining areas (T5) |
| Twin untreated | **Doubtful** | Brazil's 2019-22 de-enforcement (Ibama notices −37%); "no operation 2017-21" for Amanã rests on two log rows about March 2023 (one search, one fetch of the same page) |
| Twin's path = counterfactual | **Weak** | Growth paths converge before 2019; trend-adjusted gap ranges from ≈ 0 (Amanã) to −0.13 (Tapajós) (T6) |
| Comparable measurement | **Partly** | AMW/MapBiomas ratio 1.65 vs 5.2-5.8 (T7); Col 4 vs Col 6 harmless on the reserve before 2023 (T8) |
| No spillover | Holds | Twins are ≥ 1,500 km away (`ctl_relaxed_dist_km` 1,511) |
| R2 coding | **Errors found** | 3 territories coded "none" were searched for 2022-25 only (T4); Kayapó excluded for a 3-day raid in 2017 (T2) |

## 9. Weaknesses, ranked

1. **One or two twins, no inference.** The design cannot separate a real effect from the normal spread between areas. T13 is the closest thing to a reference distribution, and it puts Tambopata at the 6th-slowest pace of 32 areas, which also includes treated areas.
2. **Pre-trends converge, so the counterfactual is not pinned down.** Tambopata's boom was slowing before 2019. Whether the 2019-21 gap exceeds that slowdown depends on the trend window (T6).
3. **Opposite treatment in Brazil.** The twins' 2019-21 pace may be inflated by weaker federal enforcement. Direction: the gap is too large; size unknown.
4. **R2 measures news coverage.** "None found" for Amanã rests on two log rows; the best-fitting area (Kayapó) is excluded for a three-day raid; three territories were coded "none" without a 2017-21 search.
5. **Cross-product scale.** "Similar size" on AMW is not similar size on MapBiomas (T7). The pace denominator means different things in dense and scattered mining.
6. **Text out of sync.** Slope-test p cited as a level test; "three twins" leftovers; 38% vs 40%.

### 9.1 What Ruby's design does well, and how to improve it

**What it does well:**
- **Rules before results.** Every rule is pre-treatment by intent and written down in code; anyone can re-run the funnel.
- **Transparency.** The funnel figure shows why the strict design fails ("no area passes"). That is itself an informative, honest result: La Pampa has no untreated twin in the Amazon.
- **Same outcome product for both sides after 2019**, and an explicit refusal to subtract collections in levels.
- **Robust to its own cut-offs** (T9): the twins are not the product of one tuned threshold.
- **Its main message survives every check here**: Tambopata's 2019-21 pace was low against almost any mining area (T13), and the twins did not speed up (T11).

**How to improve it:**
1. **Make the search depth a coded variable.** Record the years searched and the number of queries per area. Treat "searched 2022-25 only" as "unclear".
2. **Show the comparison as a distribution, not a pair.** Plot Tambopata's pace against all 31 R1 areas, coloured by operation status (T13). This turns one twin into a reference set and makes the n = 1 problem visible.
3. **Use MapBiomas growth before and after for the twins** (T11 table) as the main twin evidence. It has a pre-period, so it is a real (two-collection) difference in differences. Report the trend-window range from T6.
4. **Add Kayapó as a sensitivity twin** (ratio 0.27), stating its 2017 raid.
5. **State the opposite-treatment bias** next to every twin number.

## 10. Proposed decisions

| # | Decision | Recommendation |
|---|---|---|
| D-S10-1 | Recode Sawré Muybu, Menkragnoti, Enawenê-Nawê | Set to "unclear (searched 2022-25 only)" in `operations_coded.csv`; `ctl_n_r2` becomes 1. Twins unchanged. |
| D-S10-2 | One twin headline number | Use the two-twin mean, **0.40**, with the range 0.38-0.43 (twin and pooling choice). Fix "38%" in agent.md and the `control_psm.py` docstring. |
| D-S10-3 | Pre-trend wording | Replace "grew faster (p = slope p)" with: "Tambopata's growth was converging on both twins' before 2019; the trend-adjusted 2019-21 gap ranges from about zero (Amanã) to −0.13 log points per year (Tapajós)". |
| D-S10-4 | Add the before/after growth table (T11) | Keep it as the main twin evidence, labelled description and "two MapBiomas collections". |
| D-S10-5 | Add the all-areas pace plot (T13) | Recommended; it carries Ruby's message better than one twin. |
| D-S10-6 | Clean `control_top3.py` | Rename to two twins; drop `top3_median_*`; make the R2b test numeric (`int(first_op[:4]) >= 2022`). |
| D-S10-7 | Claim label | **Description** only. Never "Tambopata mined at 40% of its counterfactual". |

## 11. Verdict

Ruby's design is **sound in intent and honestly executed**. It selects on pre-treatment traits, it uses one product for the outcome, and its main negative result ("no untreated twin exists") is informative. Its two twins are robust to the cut-offs.

It cannot carry a causal claim:
- there are only two twins and no placebo;
- the pre-trends converge, and trend adjustment moves the gap from about zero to modestly negative depending on the window;
- the twins are in Brazil during its weaker-enforcement years;
- "no operation" is coded from news searches with known errors.

Label: **description**.

**The brief may say:** "In 2019-21 the Tambopata buffer zone added new mining at about 40% of the pace of two Brazilian areas that had mined like it and saw no reported operation until 2023 (Amazon Mining Watch). Its pace was also lower than in 26 of 31 Amazon areas with comparable mining. Tambopata's growth was already slowing before 2019, and Brazil weakened enforcement in those years, so this is a comparison, not an estimate of Mercurio's effect [D]."

**The brief must not say:** "the twin shows what would have happened", "Mercurio cut mining to 40% of its counterfactual", or "Tambopata grew faster than its twins before 2019 (p < 0.001)".

## References

- Abadie, A., Diamond, A. and Hainmueller, J. (2010). Synthetic control methods for comparative case studies. *Journal of the American Statistical Association* 105(490).
- Ashenfelter, O. (1978). Estimating the effect of training programs on earnings. *Review of Economics and Statistics* 60(1).
- Conley, T. and Taber, C. (2011). Inference with "difference in differences" with a small number of policy changes. *Review of Economics and Statistics* 93(1).
- Imbens, G. and Rubin, D. (2015). *Causal Inference for Statistics, Social, and Biomedical Sciences*. Cambridge University Press.
- Lijphart, A. (1971). Comparative politics and the comparative method. *American Political Science Review* 65(3).
- Mill, J. S. (1843). *A System of Logic*, book III, ch. 8 (method of difference).
- Przeworski, A. and Teune, H. (1970). *The Logic of Comparative Social Inquiry*. Wiley.
- Rosenbaum, P. (2002). *Observational Studies*, 2nd ed. Springer.
- Roth, J. and Sant'Anna, P. (2023). When is parallel trends sensitive to functional form? *Econometrica* 91(2).
- Seawright, J. and Gerring, J. (2008). Case selection techniques in case study research. *Political Research Quarterly* 61(2).
