# Critical review of analysis v2 (branch analysis/v2-raster), referee view

Reviewer stance: an applied econometrician grading the brief (Analysis and honesty 30%, Provenance 25%, Framing 20%, FZS usefulness 15%, Figure 10%). Read on 2026-10-12: agent.md, PLAN_v2, review.md, readings.md, explainer_content.md, brief_content.md, methods_content.md, the 13 scripts listed in the task, and `output/numbers.csv` (the committed HEAD version; the working tree was being regenerated while I read it, but the key ids match HEAD). All numbers below come from `output/*.csv` or `data_intermediate/*.csv`, or I recomputed them read-only from those files.

**Overall verdict.** The descriptive work is strong and unusually transparent. But the inference that holds up the one [C] sentence is weaker than the text says. Three of the four "tests" behind it have mechanical or coding problems: the placebo-in-space, the twin set and the Brazil timing. The headline magnitude (1,450–1,860 ha/yr of "new mining") also measures a different outcome from the one the other attempts use. All of it can be fixed in hours.

---

## 1. Top 10 problems, ranked by severity

### P1. The placebo-in-space rank ("1 of 15", p ≈ 0.07) is mechanical, and the pool is not comparable
- **What's wrong.** `peru.py` and `peru_models.py:94` (`others = {u: fit(ad, units, u, ...)}`) give the fake operation to each other zone *while Tambopata stays in the control pool, untreated*. Tambopata's real −1,500 ha/yr fall then goes into the year effects. Every placebo zone therefore gets a positive coefficient. `peru_placebo_in_space.csv`: all 14 placebo betas are positive (+26 to +633 ha/yr). Tambopata's rank of 1 is guaranteed by construction.
- **The pool is not a comparison group either.** Of the 14 comparison zones, 12 average under 13 ha/yr of additions in 2014–18 (Tambopata 1,594; Amarakaeri 342; Allpahuayo Mishana 53). Several are not Amazonian: Lachay is coastal Lima, and Huascarán, Nor Yauyos-Cochas, Cotahuasi, Calipuy and Junín are Andean. In ha, no zone except Amarakaeri could ever produce a fall of more than 100 ha, so a rank in ha is a size ranking. The scaled version ranks 1 of 7, so the smallest attainable p is 0.14.
- **Why it matters.** This is the main inference behind the [C] claim ("rank 1 of 15", "chance about 1 in 15", in the brief §3 and explainer §14 and §17). A referee will spot the contamination at once.
- **Fix (≈1 h).** In the placebo loop, drop the real treated unit: `units_j = [u for u in units if u != TU]` when treating `u ≠ TU`. Restrict the pool to Amazon-biome buffer zones with pre-2019 additions above about 10 ha/yr. Report the scaled rank (M4) as the headline and write "p = 1/7 ≈ 0.14 at best". Brief wording: "Tambopata's fall is the largest of the N comparable zones (the smallest p-value this test can give is 1/N)".

### P2. The causal number is for *net* additions; half of the net fall is pixels *leaving* the mining class, not less new mining
- **What's wrong.** Decomposition of the Tambopata BZ net addition from `official_unit_year_v2.csv`, 2016–18 → 2019–21:
  - net 1,639 → 162 (−1,477);
  - first-time 2,015 → 1,061 (−954);
  - remined 344 → 514 (+170);
  - **stopped 720 → 1,412 (+692)**.

  So 47% of the net fall is extra "stopped" pixels: abandonment, regrowth, or ponds reclassified as water. In **2019** first-time mining was **1,925 ha**, close to 2018 (2,367). Net was low (417) only because 1,805 ha "stopped". La Pampa sector, 2019: new 1,494, stopped 1,453. GLAD agrees that clearing continued (La Pampa 2019 = 1,385 ha vs 987 in 2018; Q3 2019 742 vs Q3 2018 341).
- **Where.** The brief §3 [C] sentence: "Mercurio cut **new mining** … by roughly 1,450–1,860 ha/yr". The range is M1–M3 on *net* additions (`model_m1_during` −1,454, `model_m3_during` −1,859). On first-time mining the fall is ~950 ha/yr, which is outside the claimed range.
- **Why it matters.** It is a causal number tied to a mislabelled outcome (Analysis 30%). The stopped-pixel channel may be a real effect of evictions (sites shut), but it is "activity stopped", not "new mining avoided".
- **Fix (≈1 h).** Report the decomposition table in the brief (one line). Reword the claim: "net additions to the mapped mining area fell by about 1,450–1,860 ha/yr relative to other zones; about half of this is mined land going out of use, and first-time mining fell by about 950 ha/yr". Run M1 with `new_land_ha` from the raster for the official buffer-zone polygons so the claim has a first-time-mining version too.

### P3. Cell-panel DiD: the pre-trends fail, the reference group is the displacement destination, and few treated clusters
- **Pre-trends.** `st_event_lp_pretrend_p` = 0.00014. With 2018 as the reference, the **2016 coefficient is −2.07** (p = 0.03), against −0.57 (2019), −2.66 (2020) and −2.75 (2021). The 2020–21 "fall" is only ~30% bigger than a pre-period dip. The brief reports "−1.02 ha per cell-year (p = 0.06)" and **does not mention the failed pre-trend test**. The explainer (§13–14) does.
- **2018 reference.** 2018 is a high year: La Pampa first-time mining was 1,782 (2018) vs 582 (2016). Normalising on one high year inflates every post coefficient. The course-table event study has the same issue (`eventstudy_beta_poolA_2019` −1,451, with ref 2018 = 1,757 ha vs 707 in 2016).
- **The reference group is contaminated by displacement.** Reference = 10,353 cells. 4,229 of them are "rest of the mining corridor" (zone 6), whose first-time mining rose ~2,400 → ~3,900 → ~7,400 ha/yr (2016–18 → 2019–21 → 2022–25). The other ~4,800 reference cells (rest of Madre de Dios, parks) are almost all zeros. A rising reference makes La Pampa's *relative* fall larger, so the bias goes **away from zero** for La Pampa. Explainer §14 calls the reference "conservative"; that is true only for the positive corridor coefficient.
- **Period coding mismatch.** `zone_did` creates only `during` and `after` dummies, so the omitted period is **2010–18**, not "2014–18" as in the docstring (l.12), the figure legend (`fig_zone`: "2019-21 vs 2014-18") and methods §13.
- **Clustering.** La Pampa covers 14 of 161 blocks (corridor across the road: 10). CRV1 with ~14 treated clusters, all treated at once in one contiguous zone, over-rejects (MacKinnon & Webb 2017). The shock is really zone-level, so Conley–Taber still applies.
- **Absorbing outcome.** First-time mining cannot recur in a cell. Heavily mined La Pampa cells fall mechanically as unmined land runs out.
- **Fix (2–3 h).**
  1. Reference = gold-bearing cells outside the corridor, or corridor cells more than 30 km from La Pampa; show both.
  2. Use the 2014–18 mean as the reference (`i(year, treat, ref=...)` with the pre years binned, or define `pre` dummies explicitly) and fix the labels.
  3. Run a wild cluster bootstrap: `pyfixest` `f.wildboottest(param="lapampasector_during", reps=9999)`.
  4. Add the lagged cumulative mined share of the cell as a control, or use the share of *remaining* unmined land as the outcome.
  5. Put the pre-trend p into the brief sentence.

### P4. The three twins: Munduruku fails the team's own rule, and the twin test mixes products
- **Coding error.** `operations_coded.csv` gives Munduruku a first operation of 2023-08. The team's own logs record **Op. Mundurukânia (PF, PRF, Ibama, Força Nacional) in May 2021 in Munduruku + Sai-Cinza** (`brazil_ti_interventions.csv` l.7, marked "outside window", but the relaxed R2 window is 2017–21). They also record Ibama fines against garimpos *inside TI Munduruku* published 2018-05-15 (`control_interventions.csv` l.94). Munduruku fails R2b. Only two twins remain.
- **The Munduruku normalisation is degenerate.** AMW new area 2019–21 is 105% of its 2018 "stock" per year (2018 stock 8,832 ha; new 9,008 / 11,196 / 7,730). AMW's 2018 layer is a detection baseline, not a true stock.
- **Product mixing.**
  - Pre-trend: Tambopata comes from MapBiomas Peru Col 4, the twins from Amazonía Col 6, as a log-growth *difference* (`control_top3.py:46`). That is a subtraction across collections, against rule 7.
  - Post: the AMW pace has no AMW pre-period, so it is a post-only comparison of growth rates, not a DiD.
  - Within AMW, Tambopata BZ shows no Mercurio fall: new area 2,371 (2019, its highest post year), 1,709, 985, then 675 (2022).
- **The tests are weak.** A Welch t-test on 3 vs 3 serially correlated annual values reuses the *same* Tambopata vector in all three tests. HAC with 8 observations gives `pre_trend_p` = 1.7e-38 for Munduruku, which is meaningless. The pre-growth gaps are +0.20, +0.09 and +0.24 log/yr (Tapajós p = 0.017): Tambopata was growing ~20%/yr faster.
- **Headline chosen after seeing the data.** The code comment at l.70 says the median was picked because Munduruku is extreme. The pooled ratio is 0.16, the median ratio 0.38.
- **Fix (1–2 h).**
  - Recode Munduruku's first operation as 2021-05, which drops it.
  - Report Amanã and Tapajós only, with a note on the AMW 2018 baseline.
  - Delete "p ≈ 0.01–0.02" from the brief and write "below both twins in each of 2019, 2020 and 2021".
  - Show the pre-trends as an index plot only, without p-values, and say "not parallel".
  - Downgrade attempt 3 from "half-works" to "consistent, not a test".

### P5. Brazil staggered DiD: Kayapó miscoded as never-treated, the pool definition and the sign
- **Coding bug.** `brazil_v2.py:37` keeps only first operations with year ≥ 2021. Kayapó's coded first operation is **2017-10** (`operations_coded.csv` l.20), so it is silently set to `first_treat = 0` (never treated). The same row lists the Ibama Xapiri-Tuire operation of Sep 2024 and the desintrusão from 2025-05-02. Kayapó is the largest territory (17,628 ha in 2024) and becomes a control while it is being treated. Any other unit whose first operation is before 2021 is dropped the same way. The figure, meanwhile, draws Kayapó's operation line at Sep 2024 (l.99), so the code contradicts its own figure.
- **Pool.** "Never treated" means "no operation found in 2021–25 searches" (docstring l.13). Earlier operations are ignored, so the controls include treated units.
- **Sign.** did2s = **+0.29 log points** (TWFE +0.34): the point estimate says operations go with *more* first-time mining. The brief and explainer say only "no significant effect".
- **Data disagreement left out.** MapBiomas Col 11 raster, Yanomami first-time mining: 953 (2022), 922 (2023), 279 (2024). MAAP #242 (ISA): ~1,800 (2022), 330 (2023), 84 (2024). The raster shows no 2023 fall, while the team's own sources show −80%. Neither the brief nor the explainer says this.
- **Fix (1 h).**
  - Parse the first operation *on or after 2021* from `ops_text`, or add a column `first_op_2021_25`. For Kayapó: 2024-09 → treated from 2025 under the H2 rule.
  - Treat units with pre-2021 operations as "already treated", or drop them.
  - Re-run and report the sign.
  - Add one sentence: "MapBiomas annual maps show the Yanomami fall a year later than MAAP/ISA's Planet-based counts".

### P6. Displacement and "the region kept growing" depend on the product and on a 2023 map-year spike
- **Magnitudes.** La Pampa first-time mining fell 1,395 → 722 (−673 ha/yr). The corridor across the road rose 69 → 463 (+394, about 58% of the La Pampa fall). But the *rest* of the corridor rose +1,588 ha/yr (2,450 → 4,038). That is more than La Pampa's whole fall, so most of the regional increase cannot be miners moved from La Pampa. Gold price (2.x-fold from 2018 to 2025), new entrants, REINFO extensions and the post-COVID collapse of enforcement all fit as well.
- **AMW disagrees on the region.** AMW corridor new area *fell* 14,848 → 9,967 ha/yr (2019–21 → 2022–25; yearly 16,520 in 2020 → 8,740 in 2025). MapBiomas says it rose 4,038 → 7,638. The explainer cites AMW only for the north-of-road share.
- **2023 artefact risk.** MapBiomas MdD total net additions spike to ~19,000 ha in 2023, then ~7,600 in 2024 (brief figure, bottom panel). Tambopata BZ remined pixels hit 2,705 in 2023 vs 455 in 2024. A one-year jump shared by all zones is the usual signature of a classification or imagery change. "Most new mining in La Pampa in 2023 was on old pits", the 2022–25 means (Tambopata 1,829; ex-2023 1,251, `mean_add_tambopata_2022_25_ex2023`) and "the effect faded" all lean on this year.
- **Road placebo.** `t1_road_shift_rank` = 2 of 15, p = 0.13, not significant. The start-year windows overlap the real event: starts 2017–2021 all contain 2019–21, and 2020 ranks 1st. The real effect contaminates the placebo distribution.
- **Text errors.**
  - Explainer §6 says "the two above it start in 2020 and 2008". The rank is 2, so only one shift (2020) is above it, and 2008's shift is +0.15 < 0.41.
  - Methods §12 and PLAN_v2 still say "ranks 3 of 15; 2008 moved more".
  - T1 claims "±15 km" (docstring, figure caption, `numbers.csv` description) but uses all bands −30..+29 km. At ±15 km the north share is 0.09 (2018) → 0.20 (2019) → 0.60 (2020).
- **Fix (2 h).**
  - Use only non-overlapping placebo starts (2008–2016) and compute p = (1 + #placebos ≥ real)/(1 + 9).
  - Fix the band window (`w = w[[c for c in w if -15 <= c < 15]]`) or relabel to ±30 km.
  - Report all MdD numbers with and without 2023.
  - Add the AMW regional series as a disagreement line.
  - Brief wording: "Some of La Pampa's new mining moved across the road (+394 ha/yr against −673 ha/yr); most of the corridor's growth (+1,588 ha/yr) is too large to be the same miners."

### P7. Legality levels: today's cadastre is applied to the past, and the bias has a direction
- **What's wrong.** The `v2_legality.py` docstring admits the problem. The direction is predictable: claims filed in Madre de Dios jumped to **428 (2025) and 501 (2026 to 9 Oct)**, against 50–150 a year in 2015–21 (`legality_data.md` §1). New TRAMITE claims on recently mined land turn recent pixels "Medium". Titles granted after mining turn old pixels "Low". So "the grey zone grew" (Medium 18% → 30% → 37%) and "presumed illegal fell" (41% → 25% → 21%) may partly be cadastre timing.
- **Two "illegal" shares.** T7 (outside corridor and communities): 31% → 15% → 13%. MAAP levels: 41% → 25% → 21%. The explainer reports both without reconciling them.
- **Fix (2 h).** The cadastre has `FEC_DENU`, `FECHA_RESOL_TIT` and `FECHA_RESOL_EXTI`. Rebuild status as of year *t* for each pixel (titled if `FECHA_RESOL_TIT < t`; filed if `FEC_DENU < t`; extinguished after `FECHA_RESOL_EXTI`). At minimum, report the shares using only rights filed before 2019 as a sensitivity check.

### P8. The risk-map logit (AUC 0.935) is not a fair out-of-sample test and misses FZS's hotspot
- **No real hold-out.** The same 14,241 cells are in training and test. There is no spatial hold-out, and the static features (river distance, corridor, zone dummies, gold share) are fitted on the same cells. Test features at 2021 include the training-label years (2019–21 stock). The windows differ (3 vs 4 years), so the 0.5 threshold is not calibrated across them.
- **No benchmark.** The AUC has no baseline. The strongest terms are `corridor` (+2.87), `z_Native communities` (+2.41), `river_km` (−1.43) and `z_La Pampa` (+1.50). A one-variable model (distance to river, or "mining within 3 km") probably reaches AUC 0.85–0.9.
- **Trained on the enforcement regime.** The model learns zone effects *under* Mercurio (2019–21) and projects them onto 2026–28.
- **Misses the reserve.** `risk_hi_cells_reservesandparks` = **0**, while the reserve is the place being invaded: +241 ha (MapBiomas 2025), 640 ha (AMW 2025), ~500 ha (MAAP #241). The recommendation in explainer §19.3 is weakest exactly where FZS acts.
- **Fix (1 h).**
  - Report the baseline AUC (river distance only; lagged neighbourhood mining only).
  - Do 10-km block cross-validation (hold out blocks, not years).
  - State that the model gives 0 high-risk cells in the reserve and why: there was no training-period mining there.
  - Or drop the risk map from FZS recommendations and keep it as an appendix [P].

### P9. Provenance: numbers outside `numbers.csv`, datasets with no check, and reference gaps
- **Hard-coded in the brief:**
  - "1,450–1,860 ha/yr";
  - "4–9 times smaller" (the actual ratios are 4.4–8.6, and M3's placebo, −337, has the *same sign* as the effect);
  - "p ≈ 0.01–0.02";
  - "about 1 in 15";
  - "~500 ha" (MAAP);
  - "145 of 9,592";
  - "0% royalty";
  - "148 → 598 dredges";
  - "74%";
  - "24 territories".

  The external ones need a citation with a page. Ley 28258 and the source of the Brazil 2023 gold rules are not in the references. The internal ones should be placeholders (`{{model_m1_during}}` etc.).
- **Untraceable in the walkthrough:** "Sentinel-2 alerts confirm clearing Mar–Sep 2019" (§8; no code or number). "Declared producer output <1 t → ~1.4 t" (§11, flagged "not yet citable" but stated anyway).
- **No check (rule: one per dataset):** GLAD-L, INGEMMET geology, RAISG roads, the MAAP #235/AMW legality layer, and AMW (marked "not checkable"). Cheap checks:
  - GLAD: a GFW dashboard total for Madre de Dios in one year (read from the page, no key).
  - INGEMMET: `returnCountOnly` feature count vs the downloaded count, as done for the cadastre.
  - Legality layer: total area per class vs the MAAP #235 figure (14,004 ha of 2025 events in PAs and ITs).
  - AMW: the number of 2025 patches vs the AMW site counter.
- **Run state.** `output/checks.csv` in the working tree currently has 2 rows: modules call `checks.save()` separately, so a partial run overwrites it. Run `code/main.py` end to end before zipping.
- **Reference list.** Conley & Taber (2011) and Nunes et al. (2024) are listed but not cited in the brief text. Asner & Tupayachi (2017), MAAP #242 and Forbidden Stories are used in the explainer but are not in the list.

### P10. Inconsistencies between the brief, walkthrough and code, and the figure
- **Brief vs walkthrough.**
  - Brief §1 says "**one** twin abroad"; §3 uses three.
  - The figure legend calls Amarakaeri "(comparison)", while the explainer calls it "extra buffer zone… treated, not a control".
  - The brief says Brazil's "big territories fell after 2022–24", but the team's own Yanomami raster numbers are 518 → 458 ha/yr (−12%).
- **Figure (10%).**
  - The y-axis says "New mining area in the year" but plots net additions (2021 = −111).
  - The title is clipped at the right margin ("…buffer zone and" / "Amarakaeri and the rest… rose").
  - The figure shows neither the displacement across the road nor the first-time vs net split, which are the two things the brief argues.
  - Suggested one-figure design: top panel = first-time mining in La Pampa vs the corridor across the road vs the reserve (raster); bottom panel = Tambopata minus comparison zones (event study, 2014–18 reference) with the placebo band.
- **Methods drift.**
  - Methods §10 describes the old AMW Brazil stagger, not v2.
  - The v2_stats docstring promises "S4 Amarakaeri 2020–21 vs pre", which is not implemented.
  - Explainer §23 has two items numbered "4".
- **Gold proxy.** The "broad" gold-bearing land covers **3.96 Mha, ~47% of Madre de Dios**. So "90% of mining lies on it" is a lift of only ~1.9. The definition was chosen *because* it validated better (D31), which is selection on the outcome. On the strict definition the corridor across the road was 52% depleted by 2018 vs La Pampa 21%, which weakens "same gold, no risk". Report both definitions.

---

## 2. Specific checks

**(a) Cell-panel DiD.** Covered in P3. In brief:
- *Contamination:* yes. 41% of reference cells are the rest of the corridor, which is the main destination. That makes the La Pampa coefficient anti-conservative.
- *Clustering:* 10-km blocks, 161 clusters, but only 14 treated blocks. Use a wild bootstrap and also 30-km blocks.
- *Study window:* the box (70.65–69.30 W, 13.30–12.40 S) is drawn around the treatment and holds only 95 Amarakaeri cells. Add a sensitivity check with a larger box.
- *Zeros:* keeping never-mined cells is right. But the OLS p of 0.06 and the PPML p of 0.006 are different estimands (ha vs %). Don't present PPML as "confirming" the OLS p.
- *2018 reference:* 2018 is a high year; the 2016 coefficient is −2.07. Use the 2014–18 mean.
- *Omitted period:* 2010–18, mislabelled as 2014–18.

**(b) Randomization and permutation tests.**
- Zone placebo-in-space: contaminated (P1).
- Road fake dates: p = rank/n is computed correctly (2/15), but the windows overlap the real event (P6).
- Brazil RI: the one-sided p (share ≤ real) is correctly coded. With a positive real estimate, p = 0.73 is expected. Coding errors upstream (P5) feed into it.
- Twin "p ≈ 0.01" values are Welch t-tests, not permutation tests, and are not credible with n = 3 (P4).
- No permutation test exists for the cell panel. Cheap version: slide a 0.35°-wide fake "La Pampa" window along other Tambopata/Amarakaeri buffer-zone longitudes and recompute the coefficient.

**(c) Rule-based twins.** Pre-trends are not parallel (+0.09 to +0.24 log/yr). The pre-period mixes collections (Col 4 vs Col 6). The post pace is normalised by AMW's 2018 detection baseline (Munduruku 105%/yr). Munduruku violates R2b on the team's own evidence (May 2021, 2018). Brazil's 2019–22 enforcement weakening flatters every twin (the explainer says so, the brief does not). Fixes in P4.

**(d) Conditional causal claim.** The current wording ("Mercurio cut new mining in its target by roughly 1,450–1,860 ha/yr") mislabels the outcome, uses a magnitude range from models whose placebo ranks are mechanical, and leaves out the failed cell-level pre-trend. Proposed wording:

> [C, conditional] If the other Peruvian buffer zones show what Tambopata's buffer zone would otherwise have done, Mercurio reduced *net* additions to the mapped mining area there by about 1,450–1,860 ha/yr in 2019–21. About half of that is mined land going out of use; first-time mining fell by about 950 ha/yr and only from 2020. With one targeted zone, the best test (fake places, scaled) cannot reject chance below p ≈ 0.14; the per-cell test leans the same way but fails its pre-trend check.

**(e) Displacement vs alternatives.** Covered in P6. The across-the-road jump (+394 ha/yr) is plausibly displacement, but its fake-date p is 0.13. The corridor-wide rise (+1,588 ha/yr) is larger than La Pampa's fall. It matches the gold price (also a level shift, which year effects remove only for shared response), COVID withdrawal, REINFO extensions (and the 2025–26 claim-filing surge), and new entrants just as well. The team already says "can't show the same people moved". Move that line into the brief.

**(f) Data-source disagreements.**
- MapBiomas net (163) vs MapBiomas first-time (1,061) vs AMW (1,688) for Tambopata BZ 2019–21. Only the net series "collapses".
- AMW corridor falls while MapBiomas corridor rises.
- MapBiomas Yanomami vs MAAP/ISA (2023).
- GLAD 2019 > 2018 for La Pampa.

The team handles the GLAD one honestly (D33). The others are in the explainer at best and absent from the brief. Add a three-row "products disagree" box to brief part 4(b). Also, GLAD's mining mask is "ever mined 1985–2025" (`glad_alerts.py:67`), so it uses future outcomes. Restrict it to pixels first mined by t+1 as a sensitivity check.

**(g) Brazil staggered DiD.**
- Timing rule: H2 → next year. Fine.
- Coding bug: any first operation before 2021 is dropped (Kayapó).
- Munduruku's Nov 2024 desintrusão and May 2021 operation are ignored.
- Sai-Cinza is copied from Munduruku. That is defensible, but it makes 2 of 10 treated units one event.
- `did2s` usage (first stage `~0 | unit_id + year`, second stage `~ treat`, clustered by territory) is syntactically right. With 10 treated units and 0–2 post years for most, power is very low.
- log1p(ha) mixes territories with 1 ha and 2,000 ha.

**(h) Risk-map logit.** No leakage of the test *label* into training (labels are 2019–21 vs 2022–25). But there is cell-level overlap and no spatial hold-out, outcome-derived features are lagged correctly, there is no benchmark, and the reserve gets zero high-risk cells (P8).

**(i) Legality.** Today's cadastre applied to all years (P7). There is a directional bias from the 2025–26 claim surge. The fields needed to fix it are already downloaded.

**(j) Brief numbers not traceable to `numbers.csv`.** See the P9 list. Also:
- "First-time clearing only halved" uses `t5_m2` (first-time *mining*), not clearing.
- "the total kept growing (3,610 → 12,049)" uses course-table *net* additions in the same sentence as raster *first-time* shares. Use `v2_new_total` (5,317 → 11,373) for consistency.

---

## 3. What a grader would expect and won't find

1. **The card's displacement check in its own words:** targeted plus neighbours summed. It is already computed (`mean_add_three_bz_sum`: 1,941 → 778 → 3,127 ha/yr) but is not in the brief.
2. **Sensitivity to the pre-period:** 2014–18 base gives −1,663 vs −1,762 (`did_main_base_2014_18`). One clause in the brief.
3. **Robustness to dropping the largest unit** (agent.md §7). `peru_robust.py` exists; cite its result.
4. **An honest small-N inference statement.** Conley & Taber is cited but not applied. A simple version: the distribution of residual "effects" of untreated zones, with Tambopata removed.
5. **Measurement-error discussion of map flicker:** ~300 ha/yr of remined pixels before 2019, the 2023 spike, and ponds reclassified as water in "stopped".
6. **A cost or scale number FZS can act on**, e.g. PP 0128 spending of 31.1 M soles (2019) against the ha of net additions avoided, clearly labelled as a rough description.
7. **A one-line power statement for Brazil:** 10 treated units, 0–2 post years.
8. **Consistent unit naming:** "La Pampa sector" (raster window) vs "Tambopata buffer zone" (course table). The [C] claim is about the buffer zone, not La Pampa.

---

## 4. Done well (brief)

- Exceptional provenance machinery: one script, `numbers.csv` with claim types, publisher checks that pass (raster 20,716 vs 20,730; reserve 776 vs 777; Kayapó Col 11 17,628 vs 17,632).
- The net / first-time / remined / stopped decomposition with an asserted identity. It is the key to fixing P2.
- Honest corrections already made: the "−88% declared gold" claim withdrawn (definition change); "immediate" changed to "from 2020" (D33); Amarakaeri reclassified as less treated; synthetic control reported as a failure.
- Fake dates, fake places, a model ladder and an earlier-wave test (2012–13 rank 14 of 14) are the right toolkit. They need the fixes above, not replacement.
- The FZS framing is sharp: river posts, the reserve incursion, the legal-boundary response, the corridor as a filter. The "cannot see" paragraph names dredges (148 → 598) and mercury.
