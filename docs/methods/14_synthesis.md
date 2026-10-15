# S14 · Synthesis: what the causal attempts add up to

**Session:** S14 · **Inputs:** cards 00-13 and their test scripts in `code/review/` · **Date:** 2026-10-15

This card is different from the others. It does not review one estimator. It asks what fifteen attempts (A1-A15) say **together**, which claim the brief can carry, with which measure and range, and what must change in the code and the text. The method behind it is **triangulation**: combining several imperfect designs. Sections 1-5 explain that method in general; sections 6-11 apply it to our attempts.

Decisions already made and applied here: the treatment is the start of Operation Mercurio, Feb 2019, first treated year 2019; later events are context; 2022-25 is "later years" (S0). Every number below either comes from `output/numbers.csv` (id given) or from a test in the card named in brackets.

---

## 1. In one sentence

Several weak designs only add up to a stronger claim when their biases are **different**; if they share the same bias, agreement among them is one piece of evidence counted many times.

## 2. Simple version

Six witnesses say a car was red. If they stood at six different corners, that is strong evidence. If they all looked through the same tinted window, it is one observation repeated six times, and the tint could explain all of it.

Our six "Peru zone" methods (2×2, event study, TWFE ladder, context controls, synthetic control, synthetic DiD) all look through the same window: one treated zone (the Tambopata buffer zone), the same outcome (net additions), the same post years (2019-21, with COVID) and a comparison group that is either Amarakaeri (mostly legal corridor) or 13 zones with almost no mining. Their agreement on the sign is real, but it is mostly Tambopata's own before/after, counted six times.

## 3. When triangulation helps, and when not

**It helps** when each design rests on a different identifying assumption and the likely biases of each point in known, ideally different, directions. Then a result that survives all of them is hard to explain by any single bias.

**It does not help** when:
- the designs share the treated unit, the outcome and the period, so any bias in those is common to all;
- the designs differ only in how they weight the same comparison units;
- one design's "robustness" comes from a control that is itself driven by the treated unit or by one donor;
- the designs agree only after one of them is chosen from many specifications.

## 4. Assumptions

| Assumption | In words | Formal |
|---|---|---|
| **Bias decomposition** | Each estimate is the true effect plus that design's bias | τ̂_k = τ + b_k + e_k |
| **Diversity of bias** | The biases are not all driven by the same source | Cov(b_j, b_k) small for j ≠ k |
| **Known direction** | For each bias we can say whether it inflates or deflates | sign(b_k) known |
| **No specification search** | Designs were not picked because they agreed | Pre-registration or full reporting |

## 5. The maths

### 5.1 Master's level

Write each estimate as τ̂_k = τ + b_k. If the b_k are independent with mean zero, averaging K designs shrinks the bias like any average. If they share a component, b_k = c + u_k, then the average converges to τ + c: no number of designs removes c. Agreement in sign then says only that τ + c < 0.

When the direction of c is known, the designs give a **bound**, not a point. If every shared bias makes the fall look larger, then τ ≥ τ̂ (in our sign convention, the true fall is at most the estimated fall): the estimate is an upper bound on the size of the fall.

### 5.2 PhD level

- **Triangulation** in epidemiology (Lawlor, Tilling and Davey Smith 2016) asks for designs with different, explicitly stated sources of bias, and treats agreement as informative only to that extent.
- **Evidence factors** (Rosenbaum 2010, 2021) formalise this: two analyses are separate evidence only if their test statistics are nearly independent under the null. Our Peru zone designs fail this by construction (same treated unit, same outcome).
- **Partial identification** (Manski 2003) replaces a point estimate by the set of values consistent with stated assumptions. A bound with a stated sign of bias is the honest output when point identification fails.
- **Sensitivity** (Rambachan and Roth 2023): how large a violation of parallel trends would overturn the result. S3 gives a breakdown value of about 0.5 of the largest pre-2019 swing (card 03, T7).
- **Specification curve** (Simonsohn, Simmons and Nelson 2020): report all defensible specifications, not a chosen pair. The current "411-1,859" range is two chosen ends from different designs.

---

## 6. Our example: the scoreboard

All fifteen attempts, with what they actually measure after review.

| # | Attempt | Measure | Headline after review | Passes its own pre-check? | What it really is | Label | Card |
|---|---|---|---|---|---|---|---|
| A1 | 2×2 DiD vs Amarakaeri | net additions | −1,762 (`did_main`); −1,663 with a 2014-18 base (`did_main_base_2014_18`); window range −1,263 to −2,264 | No: fake starts 2008-16 all positive; but the real window is the largest since 2003 | Tambopata vs a zone that is 58% legal corridor | D | 02 |
| A2 | Event study, placebo in space and time | net additions | −1,450 to −1,860 by reference and pool | No: raw rank 1 also in 2014, 2015, 2016; scaled rank 10 of 11; RR breakdown about 0.5 | Size of Tambopata, plus its own before/after | D | 03 |
| A3 | TWFE ladder M1-M4 | net additions | M1 −1,454; variants −1,400 to −2,500; M4 rank 3 of 7 | M1 has no trend term; M2's slope and M3's trend are identified from Amarakaeri or Tambopata itself | M1 = own before/after (−1,432) minus +22 | D | 04 |
| A4 | Context controls K0-K3 | net additions | "keeps 97%" = +286 and −245 cancelling | No: money is a bad control | Not evidence either way | D | 05 |
| A5 | Synthetic control | net additions | −411 = 163 − 574, weight 1.0 on Amarakaeri | No: hull fails, pre-RMSPE 1,377 = 3.4 × gap | Misfit | D (of the failure) | 06 |
| A6 | Synthetic DiD | net additions | −684 to −1,545 by window; −628 to −2,287 overall | Partly: code correct, but weights explain about 2% of pre-2019 variation | Own before/after with a data-chosen baseline year | D | 07 |
| A7 | 1-km cell panel | first-time mining | La Pampa 2.47 → 1.27 ha per cell-year | No: pre-trend p 0.0055; cell-level hazard removes the fall (zone-level hazard still −42%) | Before/after; comparison cells almost never mine | D | 08 |
| A8 | Spatial RD at road and reserve | first-time, % of land | road +2.10 (p 0.079); true distance +2.51 (p 0.108); reserve uninformative | No: pre-2019 gap swings ±3 points | A north-south swing in 2020-22 | D | 09 |
| A9 | Road fake-date test | north share of new mining | rank 1 of 8 at ±30 km; 2 of 8 at ±15 km | Band choice decides | Description | D | 09 |
| A10 | Rule-based twins | AMW new area / 2018 stock | 40% of the twins' pace (0.38-0.43) | Window-dependent: trend-adjusted gap about 0 to −0.13 log points | Comparison with two Brazilian areas in weak-enforcement years | D | 10 |
| A11 | Matching (7 estimators) | AMW pace | ratio 0.35-0.54; placebo p 0.19-0.57 | No common support; caliper never applied | Restatement of A10 | D | 11 |
| A12-14 | Brazil 2×2, per-territory, staggered | net additions; AMW; ln(1 + first-time) | −0.49 to +0.62 log points across dating and sample | No: operations arrived at the peak of a boom | Cannot separate operations from the end of the boom | D | 12 |
| A15 | Risk map | P(first-time mining) | AUC 0.923 vs 0.909; persistence rule 0.938 | Gain over benchmark is noise across splits | Weak prediction | P | 13 |

**Read across the table.** No attempt passes its own identifying check cleanly. All agree on the sign for the Peru target in 2019-21. The question for this card is whether that agreement is worth more than any one of them.

## 7. Cross-checks run across the cards

### 7.1 How much of the agreement is one comparison?

| Design | 2019-21 estimate | Tambopata's own before/after inside it | Share |
|---|---|---|---|
| A3 M1 | −1,454 (`model_m1_during`) | −1,432 (card 04, T2) | 98% |
| A1 2×2, 2014-18 base | −1,663 (`did_main_base_2014_18`) | −1,432 | 86% |
| A2, pool B, pooled 2014-18 reference | −1,454 (card 03, T4) | −1,432 | 98% |
| A6 SDID, 2014-18 window | −1,545 (`sdid_sdid_ha_during`) | own 2019-21 minus its λ-weighted baseline (card 07, T2) | about 100% |

The comparison zones contribute +22 ha/yr (all 14) or +231 ha/yr (Amarakaeri alone, 2014-18 base). So **the Peru zone designs are one piece of evidence**: Tambopata's net additions fell from about 1,594 to 163 ha/yr (card 04, T2), and almost nothing comparable happened elsewhere, because almost nothing else of that size exists.

### 7.2 Which evidence is actually independent?

| Piece of evidence | Source of bias it does **not** share with the zone designs | Bias it does have | Direction |
|---|---|---|---|
| Placebo in time on Tambopata's own series: every 2019-21 year (≤ 417 ha, `tam_add_max_2019_2021`) below every 2011-18 year (≥ 707 ha, `tam_add_min_2011_2018`) | Needs no comparison zone | COVID, depletion, land stopping | Overstates the effect |
| MAAP #130: La Pampa mining deforestation down about 90% (Finer and Mamani 2020) | Different product (MAAP's own mapping), different measure (deforestation) | Same place, same years | Overstates if COVID mattered |
| Twins (A10): Tambopata's pace 40% of two Brazilian areas, and below 26 of 31 Amazon areas | Different country, different product (AMW) | Brazil's weaker enforcement; Tambopata was a maturing boom | Overstates |
| Road swing (A8) and the corridor rise (A7, card 13) | Pixel data, different comparison (the land across the road) | Displacement is part of what is measured; legality and access change at the road | Overstates (the swing counts the fall twice) |

Four partly independent views agree that **the target's mining fell in 2019-21**. Every one of them has a bias that makes the fall attributable to Mercurio look **larger**, Three known biases point the other way: the 2017-18 operations in the pre-period, Amarakaeri's own Mercurio II, and (in hectares only) Tambopata's faster pre-2019 growth if it would have continued. None of them is shown to be large enough to offset the others.

### 7.3 Timing, reconciled across cards

| Measure | 2019 | 2020-21 | Card |
|---|---|---|---|
| Net additions, Tambopata BZ (workbook) | 417 ha, already far below the 2014-18 mean of 1,594 | 181, −111 | 01 T6, 04 |
| First-time mining, La Pampa sector (raster) | 1,494 ha, near its 2018 level of 1,782 | 315, 358 | `zone_year_v2.csv` |
| Land stopping, La Pampa sector (raster) | 1,453 ha, up from 628 in 2018 | 749, 864 | `zone_year_v2.csv` |
| Cell event study, La Pampa | +0.13 (p 0.87) | the fall | 08 |
| Road RD, 2019 alone | +0.82 (p 0.22-0.58) | +2.74 (p 0.078) | 09 |

So "nothing falls in 2019" is true for **new clearing**, not for net additions. In 2019 the net fall is land leaving the mining class (stopped pits), while new clearing continued. New clearing fell in 2020-21, the COVID years. This is the precise version of X3.

### 7.4 Numbers that look alike but are different quantities

| Number | What it is | Card |
|---|---|---|
| 18% | Share of the La Pampa sector's land mapped as mined by 2018 (zone pixels) | 01 |
| 20.7% | Mean of the per-cell mined shares of La Pampa's 1-km cells, 2018 | 08 |
| 21% | Share of La Pampa's **gold-bearing** land mined by 2018 (gold proxy, both definitions) | 13 |
| 525 ha | First-time mining inside the reserve in 2017, raster zone 1 | 13 |
| 521 ha | Same year, RD units clipped to the reserve | 09 |
| 521 ha | Asner and Tupayachi (2017): cumulative loss inside the reserve to October 2016 | 13 |
| 38% / 40% | Twin pace ratio: Amanã alone / mean of Amanã and Tapajós | 10 |
| rank 1 of 15 (A1) | Placebo **in time**: fake start years 2003-16 for the 2×2 | 02 |
| rank 1 of 15 (A2-A6) | Placebo **in space**: each zone treated in turn; measures size | 03 |

Each card now uses these with their definition. The brief must too.

## 8. Shared biases and their direction

| Bias | Designs affected | Direction for "Mercurio reduced mining" | Card |
|---|---|---|---|
| Net additions count stopped land (about half the La Pampa fall) | A1-A6 | Overstates (less net ≠ less clearing) | 01 |
| Depletion: La Pampa's core was 85% mined (top tercile) | A7-A9 | Overstates | 08 |
| COVID from 2020; the fall in new clearing starts in 2020 | all Peru | Ambiguous, most likely overstates | 03, 08, 09 |
| Targeted at its peak (mean reversion) | all Peru, all Brazil | Overstates | 03, 12 |
| Pre-2019 divergence: Tambopata outgrew the comparison in hectares (fakes 2008-16 positive) | A1-A6 | Understates if it would have continued; in log terms Tambopata's growth was already slowing, so the sign depends on the scale | 02, 04, 10 |
| Displacement into the comparison (Amarakaeri, the corridor) | A1-A6, A8 | Overstates (away from zero) | 02, 09 |
| Comparison partly treated (Mercurio II in all of Madre de Dios) | A1-A6 | Understates | 02 |
| 2017-18 operations in the pre-period | A1-A6 | Understates | 00 |
| Raw-hectare placebo ranks measure size | A2, A3, A5, A6 | Overstates the evidence (not the estimate) | 03 |
| Twins in Brazil's weaker-enforcement years | A10, A11 | Overstates | 10 |
| Re-mining and river dredges are invisible to first-time mining | A7-A9 | Overstates the fall in activity | 01, 13 |

**Net direction:** most named biases point towards a larger apparent effect; three point the other way (see the table). Read any 2019-21 number as **likely an upper bound** on Mercurio's effect on mining activity. This matches what the brief already says in part 4(b); the brief's range should now match it too.

## 9. Weaknesses no design solves

1. **One treated zone, much larger than any comparison.** Size-free ranks run from 1 (post/pre MSPE ratio, fragile: 3 of 7 without Amarakaeri) to 10 of 11 (scaled mean); the scaled TWFE rank is 3 of 7. No placebo test in space can be informative here.
2. **COVID and Mercurio cannot be separated** with these data. New clearing fell in 2020, not 2019.
3. **No clean comparison exists.** The only comparable mining zone (Amarakaeri) is mostly legal corridor, partly treated and a likely destination of displaced miners; the twins abroad are in a country that weakened enforcement.
4. **Hectares are a proxy for miners.** Activity moved to old pits and rivers, which add few or no new hectares.
5. **Several key inputs are git-ignored** (rasters, AMW, IBAMA), so some tests could not be rerun here (X11).

## 10. Proposed decisions

| # | Decision | Recommendation |
|---|---|---|
| D-S14-1 | Measure for each claim | Zone designs: **net additions, always with the split** (new / re-mined / stopped). Pixel designs and the brief figure: **first-time mining**. Never compare the two in one sentence without naming both. (This answers the open question on the measure.) |
| D-S14-2 | Does a causal sentence stay in the brief? | **Keep one conditional sentence, narrowed** (wording in §11). The alternative is description only; see the decision put to Ruby. |
| D-S14-3 | The range | **About 1,450 to 1,660 ha/yr of net additions**, from the two registered specifications that use a pooled 2014-18 baseline and no extrapolated slope or trend: M1 against all 14 zones (−1,454, `model_m1_during`) and the 2×2 against Amarakaeri (−1,663, `did_main_base_2014_18`). Drop −411 (SC misfit), −1,859 (binned M3), −2,508 (Amarakaeri's slope) and all SDID values as range ends. No design passes its own pre-check (02, 04), so the criterion is this one, not "passes a pre-check"; the conditional "if" carries the parallel-trends assumption openly. |
| D-S14-4 | What sits next to the range | (a) about half is land stopping; (b) new clearing fell from 2020, with COVID; (c) relative to its size the fall ranks 3 of 7 (`model_m4_rank`); (d) a pre-2019 drift half as large as Tambopata's largest pre-2019 swing would explain it; (e) read it as an upper bound. |
| D-S14-5 | Inference language | Lead with placebo **in time** ("every 2019-21 year below every 2011-18 year"). Report placebo in space only next to its pre-year ranks and the size-relative rank, never as "p = 0.07". |
| D-S14-6 | Later years | "In 2022-25 Tambopata's net additions were back near their earlier level ({{mean_add_tambopata_2022_25}}, {{mean_add_tambopata_2022_25_ex2023}} without 2023)." Never "after enforcement ended", "it came back" as an effect, or a 2022-25 gap without the ex-2023 version. |
| D-S14-7 | Displacement | One finding, not three (corridor share, legality share and the regional total restate one fact). Give the corridor share with its 2005-09 baseline, and the bound "the rest of Madre de Dios rose 1.5 times the target's fall, so not all of it can be miners who left". |
| D-S14-8 | Brazil | Replace "wrong sign" with S12's wording: boom, then fall after 2022; operations arrived at the peak; our data cannot separate them. Backup slides only (as decided in §15 of agent.md). |
| D-S14-9 | The figure | Keep it (first-time mining, description). Three small changes: label the shaded band "Mercurio and what followed (2019-21)" instead of "Operation years"; add "2023 spike seen only in MapBiomas" to the subtitle; give the bottom panel's corridor share its pre-2010 baseline in the text, not the panel. |
| D-S14-10 | Part 4(a) prediction | Keep it [P], but say "from one case" and drop any claim built on the risk model; the persistence rule ("watch where new mining appeared last") predicts as well. |

### 10.1 Fix list, by priority

**Priority 1: text that is wrong now** (brief, walkthrough, methods page; `file:line` from the cards)

| Sentence | Where | Card |
|---|---|---|
| "year effects ... absorbing the gold price and COVID" | `brief_content.md:27, 39`; `explainer_content.md:377, 379, 389, 542`; `methods_content.md:137`; label of `model_m1_*` | 04 |
| [C] range "411 to 1,859" | `brief_content.md:29`; `explainer_content.md:43, 953` | 06, 07, this card |
| "synthetic control −411 ... (both rank 1)" | `brief_content.md:27` | 06, 07 |
| "keeps 97%", COVID-control shrinkage numbers | `brief_content.md:39` (part 4(b)) | 05 |
| "more money, bigger fall" | `explainer_content.md:383`; `peru_context_models.py:131-132` | 05 |
| "below every placebo zone ... then came back" | `peru.py:230`; `explainer_content.md:502` | 03 |
| "within a year" (road) | `explainer_content.md:670, 809, 883, 899`; `v2_rdd.py:234` | 09 |
| "0.04-0.98 across bandwidths" | `brief_content.md:31`; `explainer_content.md:432` | 09 |
| "nothing changed at the reserve edge" | `explainer_content.md:808, 958`; `v2_rdd.py:258` | 09 |
| "robust to Poisson / gold"; "against clean cells" | `explainer_content.md:522, 571, 572, 975`; `methods_content.md:160` | 08 |
| SDID "weights match Tambopata's trend" | `explainer_content.md:752, 758` | 07 |
| Matching "about 1.3 SD", "every gap negative" | `explainer_content.md:734, 736` | 11 |
| Twin slope p cited as a level test | `methods_content.md:209`; `explainer_content.md:626` | 10 |
| Brazil "wrong sign (+0.26, p = 0.44)" | `brief_content.md:33`; STORYLINE row 5c | 12 |
| "where no operation came, mining grew" | `brazil_stagger.py:95` | 12 |
| "map reclassification" (reserve, 2017) | `peru_anp.py:184`; `slides_figures.py:360, 368`; walkthrough | 13 |
| "2016 matches BCRP exactly" | `peru_gold_minem.py:10`; `DOWNLOAD_LOG.csv`; `explainer_content.md:352` | 01 |
| "declared 4-7%" | agent.md §14 (fixed in this session) | 13 |
| "0 high-risk cells in reserves"; river not in model | walkthrough; `v2_extra.py:299` | 13 |

**Priority 2: code changes needed so the new wording has registered numbers**

1. Register the pooled-reference event-study coefficients, the pre-year placebo ranks and the size-relative rank with the right denominator (10 of 11) (`peru.py`; D-S3-2, D-S3-6).
2. Draw the event-study figure's line and band from one pool (`peru.py:233-236`; D-S3-4).
3. One shared zone list for `peru.py`, `peru_robust.py`, `peru_models.py` (D-S3-3, D-S4-8).
4. Register 2022-25 numbers without 2023 for every design that reports later years (D-S1-2, D-S7-6).
5. Register the zone-level hazard and the La Pampa tercile table (`v2_stats.py`; D-S8-3).
6. Register RD for 2019 alone and with perpendicular distance; fix the running-variable docstring (`raster_zones.py:113-114, 133`; D-S9-2, D-S9-3).
7. Pass the caliper in `control_psm.py`; recode Sawré Muybu, Menkragnoti and Enawenê-Nawê to "unclear" (D-S10-1, D-S11-1).
8. One treatment-dating rule (R\*) read from `operations_coded.csv` in all Brazil scripts; add the June 2023 Kayapó action (D-S12-1).
9. MINEM check over all years (`peru_gold_minem.py:119-120`; D-S1-3).

**Priority 3: clean-up** (docstrings `v2_stats.py:12-19`, `raster_zones.py:113-114`; `control_top3.py` "three twins"; `glad_lapampa_q1_2017_2019_mean` id; SLSQP → FISTA in `peru_synth.py`; GLAD look-ahead mask `glad_alerts.py:71`; true road distance for the risk model; AMW box clipped to the department; IBAMA regex word boundary).

None of these code changes has been made. `code/*.py` is unchanged on this branch; only `code/review/` was added.

## 11. Verdict

**What the evidence supports [D]:** net mining additions in the Tambopata buffer zone fell from about 1,600 to 160 ha/yr in 2019-21, every one of those years below every year of 2011-18, while nothing of that size happened in other Peruvian buffer zones. About half of that fall is mined land going out of use. New clearing in La Pampa continued through 2019 and halved in 2020-21. At the same time new mining rose across the road in the legal corridor and along the whole corridor, so the department as a whole did not mine less. In 2022-25 the target's net additions were back near their earlier level.

**What it supports only conditionally [C]:** that Mercurio and the operations that followed caused part of the 2019-21 fall. The identifying assumption (the other zones show Tambopata's path without Mercurio) cannot be checked well: Tambopata is unlike every comparison zone, its pre-2019 path was not parallel, and COVID arrived in the second treated year.

**Wording the brief may use** (if D-S14-2 is accepted):

> *If* the other Peruvian buffer zones show what the Tambopata buffer zone would otherwise have done, Mercurio and the operations that followed lowered its net mining additions by about 1,450 to 1,660 ha/yr in 2019-21 [C]. About half of that is mined land going out of use rather than less new clearing, new clearing fell only from 2020 (the COVID years), and relative to its size the fall is not unusual among buffer zones. Most biases we can name make this number too large, so read it as an upper bound.

**Wording the brief must not use:** "411 to 1,859"; "rank 1 of 15" as a significance test; "year effects absorb the gold price and COVID"; "keeps 97%"; "within a year"; "Brazil gives the wrong sign"; "after enforcement ended"; "two sources agree" without "on the direction"; "map reclassification"; "statistically significant" for any single-zone or cell result.

## References

- Lawlor, D. A., Tilling, K. and Davey Smith, G. (2016). Triangulation in aetiological epidemiology. *International Journal of Epidemiology* 45(6).
- Rosenbaum, P. R. (2010). *Design of Observational Studies*. Springer. Ch. on evidence factors.
- Manski, C. F. (2003). *Partial Identification of Probability Distributions*. Springer.
- Rambachan, A. and Roth, J. (2023). A more credible approach to parallel trends. *Review of Economic Studies* 90(5).
- Simonsohn, U., Simmons, J. P. and Nelson, L. D. (2020). Specification curve analysis. *Nature Human Behaviour* 4.
- Conley, T. and Taber, C. (2011). Inference with "difference in differences" with a small number of policy changes. *REStat* 93(1).
- Finer, M. and Mamani, N. (2020). MAAP #130: Gold mining deforestation in the Peruvian Amazon. maapprogram.org.
