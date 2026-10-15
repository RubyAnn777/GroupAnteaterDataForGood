# S13 · Descriptive and predictive building blocks

*Method card 13 of the causal review (plan: `docs/methods/causal_review_plan.md`, session S13). Code under review: `code/peru.py:115-125`, `code/peru_robust.py:197-208`, `code/raster_layers.py`, `code/peru_anp.py`, `code/spatial.py`, `code/spatial_zones.py`, `code/v2_extra.py` (E1, E3, E4), `code/v2_legality.py`, `code/v2_products_check.py`, `code/raster_gold.py`, `code/glad_alerts.py`, `code/peru_production.py`, `code/peru_gold_minem.py`, `code/v2_economics.py`. Test script: `code/review/s13_descriptive_checks.py` (read-only, about 20 seconds). Test numbers below are "T1" to "T10" of that script.*

This card is different from S1-S12. It covers no single estimator but the blocks that the story around the causal claim is built from. They make three different kinds of claim, so the card has three parts:

| Part | Blocks | Claim type |
|---|---|---|
| **A. Displacement accounting** (shared method, then 8 blocks) | workbook sums, raster layers, inside the reserve, AMW zones, legality, gold proxy, GLAD timing, declared gold | description |
| **B. Prediction** (full method, then the risk map E4) | risk map | prediction |
| **C. Informed speculation** (short method, then the economics block) | gold, tax, enforcement money | description of a calculation on cited parameters |

Each block keeps the 1-11 structure in compressed form: what the code does (6), what we tested (7), which assumptions hold (8), weaknesses (9), decisions (10) and the verdict (11). Sections 9-11 at the end rank everything together.

---

# Part A. Displacement accounting (shared method)

## A.1 In one sentence

Displacement accounting asks whether what disappeared from the targeted place reappeared somewhere else, by adding up the outcome over the target and its possible destinations; it can show where the outcome went up, but never, on its own, why.

## A.2 Simple version

A town closes one street market. Stalls on that street fall from 100 to 10. Three questions:

1. **Did the town's total fall?** Count all stalls in town before and after. If the total fell by 90, the closure deterred trade. If the total stayed the same, the stalls may have moved.
2. **But compared with what?** If a new supermarket opened, or the season changed, the town's total would have moved anyway. "The total did not fall" only means "no deterrence" if the total would otherwise have stayed flat.
3. **Are they the same sellers?** If stalls in the next street rose by 300 while 90 left our street, at least 210 are new sellers. The count cannot tell who is who.

Displacement accounting answers question 1 exactly. Question 2 needs a counterfactual (a comparison or a trend), which turns it into a DiD. Question 3 needs data on people, which satellites do not have.

## A.3 When to use it, and when not

**Use it when:**
- the outcome is additive across places (hectares, counts), so a sum means something;
- the destinations can be listed in advance (neighbours, the legal side of a boundary, the reserve);
- you report it as description: "where the outcome rose while it fell in the target".

**Be careful or avoid it when:**
- the "rest" is much larger than the target, because its own trend will swamp any leakage;
- the destinations are defined after looking at where the outcome rose (choosing the comparison on the outcome);
- the destination units overlap or are not a partition, so the parts do not add up to the whole;
- different products or collections are added together (rule 6 of agent.md).

## A.4 Assumptions

| Assumption | In words | Formally |
|---|---|---|
| **AD1 Partition** | Target and destinations cover the region exactly once | Σ_j Y_jt = Y_region,t for every t |
| **AD2 Same measure** | Every part is measured with the same product, collection and outcome definition | one Y for all j |
| **AD3 Counterfactual for the rest** | We know how the destinations would have moved without the operation | E[Y_rest,post(0)] is known or estimable |
| **AD4 Attribution** | A rise next door comes from the people who left the target | not testable with land-cover maps |
| **AD5 Destination set fixed ex ante** | The list of destinations does not depend on where mining rose | |

## A.5 The maths

### A.5.1 Master's level

Let target T and destinations D_1..D_k partition the region R. With outcome Y (new mining, ha/yr) and periods pre and post:

  ΔY_R = ΔY_T + Σ_j ΔY_Dj.

Decompose each destination's change into its own trend and leakage from the target: ΔY_Dj = ΔY_Dj(0) + L_j. Then

  ΔY_R = [ΔY_T(0) + Σ_j ΔY_Dj(0)] + [τ_T + Σ_j L_j],

where τ_T is the effect on the target. The **leakage rate** is λ = −Σ L_j / τ_T (λ = 0 pure deterrence, λ = 1 complete displacement, λ > 1 the operation increased mining overall).

"The total did not fall" means ΔY_R ≥ 0. That is consistent with λ ≥ 1 only if the counterfactual regional trend ΔY_R(0) is zero. If the region was growing anyway (gold price, roads), the total can rise while λ is anything from 0 to above 1. **The sum identifies λ only under AD3.**

A useful bound: if every destination's whole change were leakage, λ_max = −Σ ΔY_Dj / τ_T. If λ_max > 1, then **at least** (λ_max − 1) of the destinations' rise must come from something other than the target's miners.

### A.5.2 PhD level

**Leakage in conservation.** Protected-area and payment programmes face the same problem (Ewers and Rodrigues 2008; Pfaff and Robalino 2017; Fuller et al. 2019). The literature separates:
- *activity leakage* (the same agents move, our AD4), which needs agent-level data;
- *market leakage* (lower local supply raises the price and draws in new agents), which shows up as a regional rise without anyone moving.

With a world gold price, the market channel is weak for one department, but a local channel exists: dredges, fuel and mercury suppliers relocate with the miners. Murray et al. (2004) show leakage estimates are highly sensitive to the assumed counterfactual, which is our AD3.

**Spillovers as an SUTVA violation.** In potential-outcome terms, displacement means Y_Dj depends on the target's treatment. The DiD comparing T with D_j is then biased away from zero by L_j (S2 §5.1). A spatial design can estimate L_j only if some destinations are far enough to be unaffected, and if distance to the target does not also proxy for distance to the deposit.

**Triangulating products.** When several remote-sensing products measure related but different things (MapBiomas first-time mining, AMW onset patches, GLAD forest-loss alerts), agreement in *direction* across products with *different* error structures is evidence that a pattern is not an artefact of one classifier (Munafò and Davey Smith 2018; Lawlor et al. 2016). Agreement in *level* is not expected, so products are compared as ranks, signs or timing, never subtracted (agent.md rule 6). Each product also has a known blind spot: AMW cannot see infill inside flagged patches, GLAD cannot see re-mining of bare land, MapBiomas has annual timing and classification steps. A claim is robust when it survives the product whose blind spot would most threaten it.

---

## A1 · Workbook displacement sums (`peru.py:115-125`, `peru_robust.py:197-208`)

**6 Code and data.** MapBiomas Peru Col 4 statistics. "Madre de Dios total" = department, Amazonía biome (`peru.py:42-43`). "Rest of Madre de Dios" = department minus every buffer-zone row in Madre de Dios (`peru.py:45-46`). "Three buffer zones (sum)" = Tambopata + Amarakaeri + Bahuaja-Sonene, **all department rows** (`peru.py:55`). Outcome = net additions, period means.

**7 Tests (T1).**

| Mean net additions, ha/yr | 2016-18 | 2019-21 | 2022-25 |
|---|---|---|---|
| Madre de Dios total (`displacement_mdd_total_*`) | 3,610 | 4,640 | 12,049 |
| Three BZ, as coded (all departments) | 1,941 | 778 | 3,127 |
| Three BZ, Madre de Dios rows only | 1,922 | 703 | 3,028 |
| Rest of Madre de Dios | 1,688 | 3,937 | 9,020 |

- Reproduces `displacement_*` exactly (+1,030 / −1,163 / +2,249 ha/yr for 2019-21).
- **Partition (AD1) fails slightly.** Three BZ as coded + rest − MdD total = 58 ha (2016), 106 (2018), 330 (2021), 724 (2025). The gap is Amarakaeri BZ in Cusco and Bahuaja-Sonene BZ in Puno, which are in the "three BZ" sum but not in Madre de Dios. Small, but the parts do not add to the whole.
- **Counterfactual (AD3).** The 2010-18 trend of MdD additions is flat (slope −23 ha/yr per year); extrapolated 2019-21 mean 3,480 vs observed 4,640. Among 27 earlier pairs of 3-year windows (1990-2016 starts), 22% rose by at least +1,030. So the 2019-21 rise is **within the historical range**. The 2022-25 rise (+8,439) is far above every earlier change (maximum +1,637).
- **Leakage bound.** Rest-of-MdD rose by 2,249 ha/yr while Tambopata fell by 1,477: λ_max = 1.52. At least a third of the rest's rise cannot be Tambopata's displaced mining.

**8 Assumptions.** AD1 nearly holds (gap ≤ 724 ha). AD2 holds (one collection). AD3 **fails**: no counterfactual; 2019-21 change is ordinary by history. AD4 untestable. AD5 holds (list fixed by the course card).

**9 Weaknesses.** (1) No counterfactual for the total, so "did not fall" cannot separate displacement from a growing region. (2) The rest is 1.5 to 7 times larger than the target's change, so its own trend dominates. (3) The 2022-25 rise mixes the gold price (×2.7, `gold_price_ratio_2025_2018`), the 2023 MapBiomas spike (S1 T2) and any return. (4) Three-BZ sum includes 1-724 ha outside the department.

**10 Decisions.** See D-S13-1 and D-S13-2.

**11 Verdict [D].** "Madre de Dios as a whole did not mine less: net additions went 3,610 → 4,640 → 12,049 ha/yr. Without knowing how the region would have moved, this does not show how much mining was displaced." Must not say: "the total did not fall, so mining was displaced" or "enforcement only moved mining".

---

## A2 · Raster displacement layers (`raster_layers.py`)

**6 Code and data.** MapBiomas Peru Col 4 rasters, 12 exclusive zones (`raster_zones.py:65-68`), first-time mining (`new_land_ha`). Stream (`:107-136`), Sankey (`:139-203`), road bands (`:206-234`), corridor share = (zones 5 + 6) / all zones, **mean of yearly shares** (`:237-262`, ids `v2_corridor_share_*`).

**7 Tests (T2).**

| First-time mining, ha/yr | 2016-18 | 2019-21 | 2022-25 | Change to 2019-21 |
|---|---|---|---|---|
| La Pampa sector (`v2_new_lapampasector_*`) | 1,395 | 722 | 987 | −673 |
| Corridor across the road | 69 | 463 | 538 | +394 |
| Rest of mining corridor | 2,450 | 4,038 | 7,638 | **+1,588** |
| Native communities | 1,028 | 1,121 | 1,747 | +93 |
| Reserves and parks | 202 | 42 | 100 | −160 |
| Total (`v2_new_total_*`) | 5,317 | 6,571 | 11,373 | +1,253 |

- Corridor share reproduces: 48.8 → 68.2 → 72.0% (mean of yearly shares); share of period sums 47.4 → 68.5 → 71.9%.
- **The baseline is the low point.** Mean share 2005-09 = 69.4%, 2010-13 = 54.2%, 2014-18 = 48.7%. The 2019-25 shares return to the 2005-09 level. The figure title already says this (`raster_layers.py:245`); the brief does not.
- Rest-of-corridor first-time mining was flat in 2010-18 (slope +4 ha/yr per year; extrapolated 2,540 vs observed 4,038 in 2019-21). The rise is real growth above trend, not a continuing trend.
- Rest of the corridor rose by 1,588 while La Pampa fell by 673: **at least 915 ha/yr of the corridor's rise is not La Pampa's miners** (the lead reproduces).

**8 Assumptions.** AD1 holds (exclusive raster zones). AD2 holds. AD3 partly: the corridor's flat 2010-18 trend makes the 2019-21 rise stand out, but the share's long history shows 49% was unusual. AD4 untestable; the module says so (`raster_layers.py:11-12`, "the mix shifted, never miners moved").

**9 Weaknesses.** (1) The share's 2016-18 baseline is its lowest period since 2005. (2) The corridor polygon is today's referential D.L. 1100 layer applied to all years. (3) Share rises mechanically when La Pampa falls, even if the corridor stays flat; the hectares table, not the share, carries the displacement evidence.

**11 Verdict [D].** "First-time mining in the rest of the legal corridor rose by about 1,600 ha/yr in 2019-21, more than twice La Pampa's fall of about 670, so most of it cannot be the same miners." For the share: "the corridor's share went from 49% (2014-18, its lowest) back to about 70%, its 2005-09 level". Must not say "the corridor's share rose to a record".

---

## A3 · Inside the reserve (`peru_anp.py`)

**6 Code and data.** MapBiomas Peru Col 4 protected-area workbook (`data_raw/mapbiomas_peru/...AREAS-PROTEGIDAS.xlsx`), sheet COVERAGE_4, class 4.2. Net additions per reserve. `investigate_2017` (`:62-93`) reads TRANSITION_4. Figure callout labels the 2017 step "map reclassification" (`:184`).

**7 Tests (T3).**

Net additions inside Tambopata National Reserve, ha: 2016 −5, **2017 +534**, 2018 −27, 2019 −27, 2020 −26, 2021 −47, 2022 +2, 2023 +60, 2024 +13, **2025 +241** (`anp_tam_nr_addition_2025`). Level 2025 = 776.9 ha (`anp_level_tam_nr_2025`, publisher check 777).

Where the 2017 step came from (TRANSITION_4, 2016→2017, ha converted to mining):

| From | ha | Kind |
|---|---|---|
| 1.4 Flooded forest | 148 | natural |
| 3.1 Farm mosaic | 139 | anthropic |
| 4.3 Beach | 103 | natural (river edge) |
| 4.8 Other bare anthropic | 59 | anthropic |
| 1.1 Forest | 44 | natural |
| 5.1 River | 31 | natural |
| 2.1.1 Flooded grassland | 17 | natural |
| **Total** | **541** | 343 natural, 198 anthropic |

- Raster zone 1 confirms: **525 ha of first-time mining in 2017**, then the land stays mined (stock 588 ha in 2017, 461 in 2021). A classification flicker would revert.
- Asner and Tupayachi (2017) report that "as of October 2016, a total of 521 ha of forest have been lost to gold mining within the Reserve", accumulating at 37-51 ha/yr since 2000. MapBiomas had only 54 ha mapped in 2016.
- **So the 2017 step is real mining land that MapBiomas books in one year.** The artefact is its *timing* (several years of gradual loss mapped at once), not its existence. "Map reclassification" overstates the artefact. The 198 ha from anthropic classes are consistent with earlier-cleared land being relabelled as mining.
- `investigate_2017` filters by name only (`:67`, `:76`); the file has one "Tambopata" territory, so this is harmless but fragile.
- `anp_mean_add_tam_nr_share_of_bz_plus_nr_2019_21` = −0.257 = (−33.2) / 129.3: a negative numerator over a near-zero denominator. Meaningless.
- The 2016-18 reserve mean (167 ha/yr, `anp_mean_add_tam_nr_2016_18`) is entirely the 2017 step.
- 2025 (+241) is the second-largest year in the series, smaller than 2017 (+534).

**8 Assumptions.** AD2 holds within MapBiomas. MapBiomas timing is not reliable for this step (A2 of S1 "stable classification over time" doubtful in 2017 inside the reserve).

**9 Weaknesses.** (1) "Map reclassification" is the wrong label. (2) Period means inside the reserve are driven by one year. (3) The share metric is undefined in 2019-21.

**10 Decisions.** D-S13-3.

**11 Verdict [D].** "Mining inside Tambopata reserve rose by 241 ha in 2025, the largest rise since 2017. In 2017 MapBiomas maps about 530 ha at once; an independent study puts about 521 ha of mining loss inside the reserve by October 2016, built up over several years." Must not say "2017 was a map reclassification" or "mining inside the reserve reached a record in 2025".

---

## A4 · AMW zones and rings (`spatial.py`, `spatial_zones.py`, `v2_extra.py` E1)

**6 Code and data.** Amazon Mining Watch onset patches (480 m, git-ignored; intermediates `amw_zone_year.csv`, `amw_rings_year.csv`). Zones: reserves > buffer zones > D.L. 1100 corridor > other ANP/BZ > "Other Madre de Dios box" (`spatial.py:58-63`), assigned by **patch centroid** (`:128-135`). Box `MDD_BOX = (-72.6, -14.6, -68.6, -10.5)` with the comment "no department polygon available" (`:42`). Rings 0-10 / 10-25 / 25-50 km from a data-derived La Pampa centre (`:149-166`). E1 (`v2_extra.py:57-128`) uses the raster zones instead.

**7 Tests (T4).**

*Geometry*
- Box = 197,106 km². Madre de Dios (geoBoundaries, present in `data_raw/geoboundaries/` and already used by `raster_zones.layers()`) = 84,996 km².
- **113,653 km² of the box (58%) lie outside Madre de Dios**: Cusco 41,766, Puno 29,583, Ucayali 9,850, Apurímac 4,847, and **27,607 km² outside Peru**. "Other Madre de Dios box" therefore includes mining in Puno, Cusco and Bolivia. The comment is outdated.

*Precedence*
- Amarakaeri BZ ∩ corridor = 173 km²; Tambopata BZ ∩ corridor = 21 km². `spatial.py` gives these to the buffer zone; `raster_zones.py` gives them to the corridor, and gives native communities (including Kotsimba) their own zones. `spatial.py` has no community zone.
- So AMW "Amarakaeri BZ" and "Tambopata BZ" are not the same land as the raster zones (S1 T6, X12).

*Rings*
- Ring areas 314 : 1,649 : 5,890 km² (1 : 5.25 : 18.75); area shares 4 / 21 / 75%.
- AMW new-area shares 8.1 / 22.2 / 69.8% (2019-21, `sp_lp_ring_*_share_2019_21`) and 8.5 / 21.5 / 70.0% (2022-24). Shares follow area.
- Density relative to the 50-km disc: **2.0 / 1.06 / 0.93 in 2019-21, 2.1 / 1.03 / 0.93 in 2022-24.** Mining is twice as dense near La Pampa, and this did not change between periods. With 2018 as AMW's stock, there is no pre-period to show a shift outward.

*Inside Tambopata reserve, four sources*

| Source | Measure | Value |
|---|---|---|
| MapBiomas ANP workbook | net addition 2025 | 241 ha |
| MapBiomas raster zone 1 | first-time 2025 | 238 ha |
| AMW (`sp_amw_tambopata_nr_new_ha_2025`) | onset 2025, provisional | 640 ha |
| AMW (`..._2026`) | onset 2026, provisional, part-year | 1,459 ha |
| MAAP #241 | H2 2025 to Feb 2026 | ~500 ha |

AMW 2019-24 sum = 209 ha vs MapBiomas net −26 and first-time 285. **The products agree that 2025 was a jump; they disagree on its size by a factor of 2.7 (AMW vs MapBiomas, 2025) and cover different periods.** "Two other sources agree" (walkthrough) holds for direction only.

**8 Assumptions.** AD1 holds within each module but the two modules partition differently (AD5 by design, not by outcome). AD2: AMW 480-m patches overstate area; never added to MapBiomas (respected).

**9 Weaknesses.** (1) The "Madre de Dios box" is mostly not Madre de Dios. (2) Zone precedence differs from the raster zones. (3) Ring shares are area shares; only densities are informative. (4) Centroid assignment of 480-m patches is fine for 10-km rings and large zones, but splits patches at narrow boundaries (the 173 km² overlap strip).

**10 Decisions.** D-S13-4.

**11 Verdict [D].** "Amazon Mining Watch, a different satellite product, also shows a jump inside the reserve in 2025 (640 ha, provisional), larger than MapBiomas (241 ha); MAAP reports about 500 ha from late 2025 to February 2026." Must not say "two sources agree" without "on the direction", and must not quote "70% of new mining lies 25-50 km away" as evidence of dispersal.

---

## A5 · Legality (`v2_legality.py`, `v2_tests.py:164-171`)

**6 Code and data.** MAAP #235 / AMW legality layer (today's INGEMMET cadastre) rasterised on the MapBiomas grid, crossed with first-mined year (`:32-46`). Time-consistent version (`:47-59`): a Low or Medium pixel becomes High if no covering concession was filed (FEC_DENU) by the mining year. T7 (`v2_tests.py:164-171`) instead counts as "presumed illegal" all first-time mining outside the corridor and outside native communities.

**7 Tests (T5).**

| Presumed illegal share of first-time mining | 2016-18 | 2019-21 | 2022-25 |
|---|---|---|---|
| High + Very high, today's concessions (`leg_illegal_share_*`) | 41.4% | 25.4% | 21.3% |
| Time-consistent (`leg_tc_illegal_share_*`) | 41.8% | 26.1% | 21.7% |
| T7, outside corridor and communities (`t7_presumed_illegal_share_*`) | 31.2% | 14.7% | 12.7% |

- **The correction is one-directional by construction** (`:56-57`): pixels can only move from Low/Medium to High. It moved 76, 130 and 209 ha in the three periods. Pixels that were inside a concession at the time but are outside every right today (expired) stay High; the current cadastre cannot find them. Direction of the remaining error: overstates "illegal" in early years more than late ones, so the true fall may be smaller.
- **Within vs mix decomposition** (today's concessions): illegal share inside the corridor 1.4 / 3.9 / 3.0%, outside 77.3 / 72.3 / 67.9%; corridor share of hectares 47 / 69 / 72%. The fall of −0.201 (2016-18 to 2022-25) = **−0.186 from the mix** (more mining in the corridor) and only −0.042 within the two parts.
- So the legality fall is **93% a restatement of the corridor-share rise (A2)**, not independent evidence that mining became more legal.

**8 Assumptions.** Legality is assigned from today's map (the module says so, `:10-11`); the fix is partial and one-way. T7 and the MAAP layer use different definitions and must not be mixed.

**9 Weaknesses.** (1) One-directional correction. (2) Not independent of the corridor share. (3) "Presumed illegal" depends on the definition: 41% vs 31% in the same years.

**11 Verdict [D].** "Measured against today's concessions, the share of first-time mining outside any concession fell from about 41% to 21%, mostly because more of it happened in the corridor." Always name the definition. Must not say "mining became more legal".

---

## A6 · Gold-left proxy (`raster_gold.py`)

**6 Code and data.** INGEMMET 1:100k geology: strict = alluvial and fluvial units; broad = strict + Madre de Dios Formation upper member (`:26-27`). Depletion = gold-bearing land mined by year Y / gold-bearing land in the zone (`:66-69`). D31 (`docs/PLAN_v2.md:64`) chose broad because 90% of all mining lies on it.

**7 Tests (T6).**

| Zone | Strict: gold land, ha | Strict: share of mined land on it | Strict: depleted 2018 | Broad: gold land, ha | Broad: share on it | Broad: depleted 2018 |
|---|---|---|---|---|---|---|
| La Pampa sector | 10,076 | **17%** | **20.9%** | 52,724 | 98% | **21.1%** |
| Corridor across the road | 3,657 | 40% | **51.5%** | 37,105 | 100% | **8.3%** |
| Rest of mining corridor | 209,218 | 75% | 14.6% | 384,947 | 89% | 9.3% |
| Kotsimba | 8,720 | 67% | 20.3% | 8,777 | 67% | 20.2% |
| All Madre de Dios | 1,329,595 | 64% | 3.5% | 3,960,538 | 90% | 1.6% |

Lift (mining share on the units / their share of the department): strict 4.09, broad 1.93 (`gold_*_lift`).

- **The ranking reverses**: on strict units the land across the road was more depleted than La Pampa in 2018 (52% vs 21%); on broad units much less (8% vs 21%). Reproduces the lead.
- **But La Pampa's own number is robust**: 21% under either definition.
- Strict fails as a proxy *in La Pampa*: only 17% of La Pampa's mined land lies on strict units (La Pampa mines terraces). So choosing broad is not only selection on the outcome; it is what La Pampa's geology requires. The cost is weak discrimination: broad covers 47% of the department (`gold_broad_land_share_mdd`), lift 1.9.
- Hectares are not grade. "Gold left" is unmined land on a unit, not ounces.

**9 Weaknesses.** (1) Cross-zone comparisons depend on the definition. (2) Broad barely discriminates. (3) Area, not grade.

**10 Decisions.** D-S13-5.

**11 Verdict [D].** "La Pampa had not run out of gold-bearing land: about 21% of it was mined by 2018, under either geology definition." Must not say "across the road had the same gold and no risk" or compare depletion across zones without both definitions.

---

## A7 · GLAD timing (`glad_alerts.py`)

**6 Code and data.** UMD GLAD-L alerts 2017-2026 (Collection 1 to 2020, Collection 2 from 2021, `:5-7`), each alert pixel tagged "mining" if the MapBiomas pixel is mining in **any year 1985-2025** (`:71`, `mined = first > 0`).

**7 Tests (T7).**
- La Pampa mining-land alerts reproduce: 936 (2017), 987 (2018), **1,385 (2019)**, 275 (2020), 35 (2021), 130, 306, 800, 747 (2025) ha (`glad_mining_lapampasector_*`).
- **Look-ahead mask.** An alert in 2017 is tagged "mining" if the pixel becomes mining by 2025 (8 years of look-ahead); an alert in 2025 only if it is already mapped in 2025. Land cleared in 2024-25 and mapped as mining later is missing. Direction: understates mining-land alerts in the last years, so it biases against finding a return.
- **2021 version break.** Ratio 2021 / mean(2020, 2022) on mining land: La Pampa 0.17, across the road 0.93, rest of corridor 0.54, native communities 0.39. On non-mining land it also falls in most zones (0.40 to 0.89). All Madre de Dios non-mining alerts: 13,669 (2020) → 9,147 (2021) → 9,130 (2022). So part of the 2021 low is product-wide, and 2021 cannot be read alone.
- The key timing fact (La Pampa high in 2019, falling in 2020) lies **within Collection 1**, so the break does not affect it. It agrees with S1 T1 (MapBiomas first-time mining near peak in 2019) and X3 in the plan's register (new clearing falls from 2020).

**9 Weaknesses.** (1) Look-ahead mask. (2) 2021 collection break. (3) Alerts need forest, so re-mining is invisible. (4) X10: id `glad_lapampa_q1_2017_2019_mean` is the 2017-18 mean.

**11 Verdict [D].** "Forest-loss alerts on mining land in La Pampa were higher in 2019 than in 2018 and fell sharply in 2020, in the same alert collection." Must not use 2021 alone, or the 2021-22 level against 2017-20, as evidence of a fall.

---

## A8 · Declared gold (`peru_production.py`, `peru_gold_minem.py`)

Covered in S1 T3. Re-run here (T8) because the economics block uses it: MINEM files run above the BCRP series by +47.6% (2015), +8.3% (2016), +47.4% (2020) and +10.4% to +16.2% (2021-25). The check tests only 2012 and 2019 (`peru_gold_minem.py:119-120`); the docstring's "2016 exactly" (`:10`) is false. The official MdD series −88% 2018→2025 (`pe_prod_change_2018_2025_pct`) is a definition change, already labelled so in agent.md. **Verdict [D]**: cite BCRP kg for declared output after 2020, and never as a production fall.

---

# Part B. Prediction (the risk map)

## B.1 In one sentence

A prediction model answers "where will the outcome happen next?", and is judged only by how well it does on data it has not seen; it says nothing about what would happen if we intervened.

## B.2 Simple version

A weather forecaster says "70% chance of rain" on 100 days. If it rained on about 70 of them, the forecast is **calibrated**. If it rained more often on the days she said 70% than on the days she said 20%, the forecast **discriminates** (that is what AUC measures). Neither tells you whether carrying an umbrella *causes* dry clothes.

Two traps:
1. **Grading your own homework.** Testing on the same days you trained on flatters the forecast. Use days (or places) the model never saw.
2. **The climate changed.** A forecaster trained before a new dam was built may be wrong after. A mining-risk model trained while the army sat in La Pampa learns "La Pampa is quiet", which stops being true when the army leaves.

And always ask: does the fancy model beat the simple rule "it will rain where it rained yesterday"?

## B.3 When to use it, and when not

**Use it when:**
- the decision is about *where* or *when* to look (targeting patrols, monitoring), not about *what works* (Kleinberg et al. 2015);
- there is a hold-out that mimics real use (later years, unseen places);
- a simple benchmark exists to beat.

**Avoid or be careful when:**
- the policy you want to target is itself what changed the outcome in the training data (regime shift, Lucas 1976);
- outcomes are rare or spatially clustered (AUC looks good by sorting empty forest from mining belts);
- the threshold matters but was not chosen from costs.

## B.4 Assumptions

| Assumption | In words |
|---|---|
| **P1 Stationarity** | The relation between features and outcome in the test period equals the training period |
| **P2 Independence of train and test** | Hold-out cells and years carry no information from the training set (no spatial or temporal leakage) |
| **P3 Same outcome definition** | Train and test outcomes measure the same thing over the same length of time |
| **P4 Benchmark fairness** | The benchmark has the same information and the same hold-out |
| **P5 Threshold from a loss** | A cut-off like 0.5 reflects the costs of false alarms vs misses |

## B.5 The maths

### B.5.1 Master's level

A logit P(y_i = 1 | x_i) = Λ(x_i'β) is fitted on (x, y) from the training set. On the hold-out:
- **AUC** = P(p̂_i > p̂_j | y_i = 1, y_j = 0): the chance a random positive is ranked above a random negative. 0.5 = random. It ignores calibration and base rates.
- **Average precision (AP)**: area under the precision-recall curve; more informative when positives are a minority (Saito and Rehmsmeier 2015).
- **Calibration**: within groups of similar p̂, mean p̂ ≈ observed rate (Steyerberg et al. 2010).
- **Threshold c**: precision = P(y = 1 | p̂ > c), recall = P(p̂ > c | y = 1).

### B.5.2 PhD level

**Spatial cross-validation.** With spatially autocorrelated outcomes and features, random splits leak information and overstate skill. Block CV (Roberts et al. 2017) holds out whole blocks; even then, features computed from neighbourhoods that cross block edges leak (Ploton et al. 2020). Block size should exceed the range of residual autocorrelation.

**AUC is a weak yardstick.** Hand (2009) shows AUC implicitly uses different misclassification costs for different models. Small AUC gains between models (here 0.01-0.02) are usually within split-to-split variation, so report the distribution over many splits, not one seed.

**Prediction vs causation.** Shmueli (2010): a model can predict well with no causal content. A coefficient on "La Pampa" in a model trained in 2019-21 absorbs the enforcement regime. Using it to target enforcement in 2026-28 assumes enforcement continues as in 2019-21 (Lucas critique).

**Outcome window.** With per-year hazard h, P(any event in k years) = 1 − (1 − h)^k. A model trained on a 3-year window and tested on a 4-year window is miscalibrated by construction, even if discrimination is unaffected.

## B.6 Our example: E4 (`v2_extra.py:204-301`)

| Element | As coded | Where |
|---|---|---|
| Unit | 1-km cell, study window, 14,241 cells | `cell_attr_v2.csv` |
| Train outcome | first-time mining > 1 ha in **2019-21** (3 years) | `:235` |
| Test outcome | first-time mining > 1 ha in **2022-25** (4 years) | `:236` |
| Features | \|road distance\|, north of road, river distance, gold share, own mined share, mining within ~3 km, 5 zone dummies, corridor | `:223-234` |
| Hold-out | random half of 10-km blocks (seed 0) train, the rest test | `:245-248` |
| Benchmark | logit on "mining within ~3 km" only, same split | `:252-254` |
| Map | model fitted on all cells, applied to 2025 features; flag p̂ > 0.5 outside the corridor | `:257-262` |

## B.7 Tests run and results (T9)

**T9a Reproduce.** Full-sample AUC 0.935 (`risk_auc_2022_25`), hold-out 0.923 (`risk_auc_spatial_holdout`), benchmark 0.909 (`risk_auc_benchmark`). Positives: 15.0% of cells in training, 22.6% in test (3 vs 4 years).

**T9b The AUC gain across 50 block splits.**

| | Range | Median |
|---|---|---|
| Full model AUC | 0.899 to 0.950 | 0.934 |
| Benchmark AUC | 0.909 to 0.951 | |
| Gain | −0.018 to +0.022 | +0.006 (positive in 70% of splits) |

The published gain (+0.014) is one draw. **The model's advantage over "mining nearby" is small and not robust.**

**T9c Benchmarks without any fitted model** (seed-0 hold-out, 7,262 cells, base rate 26.4%):

| Score | AUC | AP |
|---|---|---|
| Full logit | 0.923 | 0.724 |
| Logit, mining nearby only | 0.909 | 0.687 |
| Raw mining nearby (2021) | 0.909 | 0.687 |
| **Persistence: > 1 ha first-time in 2019-21 (ties broken by mining nearby)** | **0.938** | **0.840** |

A rule with no model ("look where new mining happened last period") beats the logit on both measures.

**T9d Hard cells.** Among hold-out cells with some mining within ~3 km in 2021 (n = 3,835, 49% positive), AUC 0.831 vs 0.787 for the benchmark. The model helps most where it matters, but this is where persistence is strongest too.

**T9e Calibration** (deciles of p̂ on the hold-out): middle deciles under-predict (decile 8: p̂ 0.34 vs observed 0.60); top decile 0.84 vs 0.81. Mean p̂ 0.195 vs observed 0.264, consistent with the 3-year vs 4-year windows.

**T9f Threshold 0.5.** On the hold-out it flags 1,355 cells: precision 0.81, recall 0.57. The cut-off is not derived from any cost.

**T9g Regime shift.** A model trained before Mercurio (2014 features → 2015-17) ranks 2019-21 cells with AUC 0.933, so ranking survives the regime change. Levels do not: it predicts 0.43 for La Pampa cells vs 0.34 observed. Coefficients move: La Pampa dummy +2.87 (pre) vs +1.50 (2019-21); reserves dummy −0.54 vs **−1.56**.

**T9h Reserves.** The map model gives every reserve cell (n = 3,556) a 2026-28 risk of at most 0.091, so `risk_hi_cells_reservesandparks` = 0. Yet 45 reserve cells had > 1 ha of first-time mining in 2022-25, and the 2025 incursion followed. The zero comes from the reserves dummy learned under enforcement plus the 0.5 threshold. The map footnote says the model misses the incursion because of "river access, not in the model" (`:299`), but river distance **is** a feature (`:227`).

**T9i Road distance.** `road_km` is the latitude difference to the road at the same longitude (`raster_zones.py:112-134`), not the distance to the road. Against the true distance (ESRI:102033) for all cells: median error +1.3 km; **42% of cells off by more than 2 km, 28% by more than 5 km**, mostly west of −70.3 (where the road turns north-south towards Mazuko) and east of −69.7. Inside the "wide" La Pampa window used by `v2_stats` road bands: 7.7% off by > 2 km. Refitting with the true distance changes the hold-out AUC from 0.9226 to 0.9227. Zone profile distances (E3, `zp_*_km_to_highway`) are overstated: other buffer zones 66 vs 49 km, native communities 30 vs 23, rest of corridor 25 vs 20, reserves 36 vs 32.

## B.8 Assumption check

| Assumption | Verdict | Evidence |
|---|---|---|
| P1 Stationarity | **Fails for levels, holds for ranks** | T9g |
| P2 Independence | Partly | Neighbourhood feature crosses block edges; test years are later |
| P3 Same outcome | **Fails** | 3-year train vs 4-year test (T9e) |
| P4 Benchmark fair | Holds, but weak benchmark | Persistence beats both (T9c) |
| P5 Threshold from a loss | **Fails** | 0.5 by convention (T9f) |

## B.9 Weaknesses, ranked

1. A no-model persistence rule beats the logit (AUC 0.938 vs 0.923, AP 0.840 vs 0.724).
2. The AUC gain over the benchmark is within split noise (−0.018 to +0.022).
3. Trained under the enforcement regime: the reserves dummy (−1.56) makes the reserve look safe; "0 high-risk cells in reserves" is an artefact.
4. Uncalibrated, with an arbitrary 0.5 threshold and mismatched outcome windows.
5. Road distance is a north-south distance, wrong for 42% of cells (no effect on AUC; wrong E3 numbers).
6. Footnote misstates why the reserve incursion is missed.

## B.10 Proposed decisions

See D-S13-6 to D-S13-8.

## B.11 Verdict

Label: **prediction**. Wording the walkthrough may use: "A simple rule, 'look where new mining appeared in the last three years', ranks next period's new mining as well as our model (AUC about 0.93 on held-out areas). Both are trained while enforcement was in place, so they under-rate places that enforcement protected, such as the reserve." Must not say: "the model shows where enforcement would protect most", "no reserve cell is at high risk", or quote the AUC gain over "mining nearby" as a real improvement.

---

# Part C. Informed speculation (economics)

## C.1 Method in brief

**One sentence.** Informed speculation multiplies our own measured quantities by cited outside parameters to get an order of magnitude, and reports a low-high range that shows which assumption drives it.

**Rules** (general, usable for any project):
1. Every parameter has a source a reader can open (page, table).
2. Report a range, not a point, and say which parameter drives the range (Manski 2015 on communicating uncertainty).
3. Show what is *not* in the range (excluded channels), with the direction of the bias.
4. Never mix two sources' estimates of the same parameter into one range.
5. Label it as speculation: it is a description of a calculation, not a measurement.

## C.2 Our example (`v2_economics.py`)

Gold = first-time hectares × 1.6-1.9 kg/ha (CSF 2023, Cuadro 3, 2.5-m pit) × gold price; declared share = MINEM declared / that gold; tax wedge = 29.5% × 11-36.8% margin; enforcement = PP 0128 money booked in Madre de Dios.

## C.3 Tests (T10)

| Item | Coded | Test |
|---|---|---|
| Gold 2022-25 (`eco_gold_t_lo/hi_2022_25`) | 18.2 to 21.6 t/yr | reproduced |
| Without 2023 | | 16.6 to 19.7 t/yr |
| 5-m pits (CSF: kg/ha scales with depth) | | 36.4 to 43.2 t/yr |
| Declared share, MINEM (`eco_declared_share_lo/hi`) | **6.4% to 7.6%** | reproduced; agent.md §14 says "4-7%" (stale) |
| Declared share, BCRP declared kg | | 5.7% to 6.7% |
| Tax wedge (`eco_tax_share_value_*`) | 3.2% to 10.9% of value | reproduced |
| Enforcement / gold value (`eco_spend_share_of_value`) | 0.12% | reproduced |
| Parameter sources in `economics_sources.md` | yield (Cuadro 3), margins, tax, Hg 2.4-2.8, both social-cost ranges | **all present**; CSF PDF in `data_raw/literature/` |

The range only varies the yield (1.6 vs 1.9). Pit depth, re-mined pits and river dredges are excluded, and each would push gold **up**. Gold declared in other departments would push the true formal share up.

## C.4 Verdict

Label: **description of a calculation (informed speculation)**. Wording: "On cited yields, mapped first-time mining in 2022-25 corresponds to roughly 17-22 tonnes of gold a year, probably more; only about 6-7% of that appears as declared Madre de Dios output (BCRP declared kg), and enforcement spending booked in the department is about 0.1% of its value." Must not present any of these as measured, or the declared share as "the illegal share".

---

# 9. Weaknesses, ranked (all blocks)

1. **Displacement sums have no counterfactual** (A1). The 2019-21 regional rise is within its historical range; "the total did not fall" cannot measure displacement.
2. **Risk map: persistence beats the model; the gain over the benchmark is noise; the reserve's zero risk is a regime artefact** (B).
3. **Legality fall is 93% the corridor-share rise** (A5), so it is not a second piece of evidence.
4. **Corridor-share baseline is its 2014-18 low** (A2); the 2019-25 level equals 2005-09.
5. **"Map reclassification" in 2017 is mislabelled** (A3): real mining land, mapped late.
6. **AMW "Madre de Dios box" is 58% outside Madre de Dios**, and AMW zones differ from raster zones (A4).
7. **Gold-proxy comparisons across zones flip with the definition** (A6); La Pampa's own 21% is robust.
8. GLAD look-ahead mask and 2021 break (A7); road distance wrong for 42% of cells (B); stale "4-7%" (C); id name `glad_lapampa_q1_2017_2019_mean` (X10).

# 10. Proposed decisions

| # | Decision | Recommendation |
|---|---|---|
| D-S13-1 | Wording of the regional total | Keep the numbers, drop the inference: "the region as a whole did not mine less" [D], plus the leakage bound "the rest of the department rose by 1.5 times the target's fall, so not all of it can be displaced miners". Never "displacement was complete". |
| D-S13-2 | Partition | In `peru.py`, build "three BZ" from Madre de Dios rows only (or label it "incl. 1-724 ha in Cusco and Puno"). Low priority. |
| D-S13-3 | The 2017 step in the reserve | Replace "map reclassification" (`peru_anp.py:184`, `slides_figures.py:360,368`, walkthrough) with "real mining land mapped in one year (see Asner and Tupayachi 2017)". Drop `anp_..._share_of_bz_plus_nr_*` from numbers or stop citing it. |
| D-S13-4 | AMW zones | Clip the box to the geoBoundaries department (`spatial.py:42`, update the comment), or rename the zone "rest of the box (incl. Puno, Cusco, Bolivia)". Report ring densities, not shares. "Two sources agree" → "agree on the direction; sizes differ". |
| D-S13-5 | Gold proxy | Keep the brief's La Pampa sentence and add "under either geology definition". Report both definitions wherever zones are compared. |
| D-S13-6 | Risk-map benchmark | Add the persistence rule as a second benchmark and report AUC over many block splits. If persistence wins, say so in the walkthrough. |
| D-S13-7 | Risk-map claims | Remove "0 high-risk cells in reserves" as a finding; fix the footnote (`v2_extra.py:299`: river distance *is* in the model); state the 3- vs 4-year window and that 0.5 is arbitrary. |
| D-S13-8 | Road distance | Replace the north-south distance with true distance to the line for the risk model and E3 (`zp_*_km_to_highway`); keep the signed version for the La Pampa bands, where it is accurate. Flag for S8 (wide-window bands: 7.7% of cells off by > 2 km). |
| D-S13-9 | Legality | Present the legality fall as the same fact as the corridor share, not as separate evidence; note the one-directional correction. |
| D-S13-10 | Corridor share | In the brief: "back to about 70%, its 2005-09 level, from a low of 49% in 2014-18". |
| D-S13-11 | Economics | Fix agent.md §14 "declared 4-7%" → "about 6-7%" (5.7-6.7% on BCRP declared kg, the source D-S1-3 says to cite; 6.4-7.6% on MINEM). Done 2026-10-15. Show the without-2023 range and say every excluded channel raises gold. |

# 11. Verdict

All blocks are correctly computed: every headline number in the leads reproduced. Their problem is interpretation, not arithmetic.

- **Displacement blocks are description.** They show where mining rose while La Pampa fell. They cannot show that miners moved, and the regional totals cannot show how much was displaced. The strongest displacement fact is the hectares one: the rest of the corridor rose by more than twice La Pampa's fall, so most of it is not La Pampa's miners [D].
- **Several blocks repeat one fact.** Corridor share, legality share and the regional total all restate "more new mining in the corridor". They should be presented as one finding, not three.
- **The risk map is prediction**, and a weak one: it does not beat "look where mining happened last period", and it under-rates the reserve because it learned the enforcement regime [P].
- **Economics is informed speculation**, correctly sourced, with a range that understates uncertainty in one direction (gold is probably higher).

What the brief may say (current sentences, with fixes): "Across the highway, in the legal corridor, first-time mining rose from 69 to 463 ha/yr [D]. The corridor's share of the department's new mining went from 49% (2014-18, its lowest) back to about 70% while the total grew; the corridor's rise exceeds La Pampa's fall, so it is not all miners moving [D]. La Pampa had not run out of gold-bearing land (21% mined by 2018 under either geology definition) [D]. Mining inside the reserve rose by 241 ha in 2025, the largest rise since 2017 [D]."

What it must not say: "the total did not fall, so mining was displaced"; "mining became more legal"; "the 2017 jump was a map reclassification"; "two sources agree" (without "on the direction"); "the risk model shows where enforcement would protect most"; "no reserve cell is at risk".

## Tests not possible here

- **GLAD look-ahead size**: needs the raw alert tiles and the first-mined raster at alert level, to retag alerts using only maps up to the alert year + 1.
- **AMW zones re-clipped to the department**: needs `amw/amazon_basin_detections.geojson` (git-ignored).
- **Legality, opposite-direction correction**: needs a historical cadastre with expired rights.
- **Pixel-level reserve check of 2017**: needs the annual rasters to see whether the 2017 pixels were bare in 2014-16 (supporting late mapping).

## References

- Ewers, R. M. and Rodrigues, A. S. L. (2008). Estimates of reserve effectiveness are confounded by leakage. *Trends in Ecology and Evolution* 23(3), 113-116.
- Pfaff, A. and Robalino, J. (2017). Spillovers from conservation programs. *Annual Review of Resource Economics* 9, 299-315.
- Fuller, C., Ondei, S., Brook, B. W. and Buettel, J. C. (2019). First, do no harm: a systematic review of deforestation spillovers from protected areas. *Global Ecology and Conservation* 18, e00591.
- Murray, B. C., McCarl, B. A. and Lee, H.-C. (2004). Estimating leakage from forest carbon sequestration programs. *Land Economics* 80(1), 109-124.
- Munafò, M. R. and Davey Smith, G. (2018). Robust research needs many lines of evidence. *Nature* 553, 399-401.
- Lawlor, D. A., Tilling, K. and Davey Smith, G. (2016). Triangulation in aetiological epidemiology. *International Journal of Epidemiology* 45(6), 1866-1886.
- Shmueli, G. (2010). To explain or to predict? *Statistical Science* 25(3), 289-310.
- Kleinberg, J., Ludwig, J., Mullainathan, S. and Obermeyer, Z. (2015). Prediction policy problems. *American Economic Review* 105(5), 491-495.
- Roberts, D. R. et al. (2017). Cross-validation strategies for data with temporal, spatial, hierarchical, or phylogenetic structure. *Ecography* 40(8), 913-929.
- Ploton, P. et al. (2020). Spatial validation reveals poor predictive performance of large-scale ecological mapping models. *Nature Communications* 11, 4540.
- Hand, D. J. (2009). Measuring classifier performance: a coherent alternative to the area under the ROC curve. *Machine Learning* 77, 103-123.
- Saito, T. and Rehmsmeier, M. (2015). The precision-recall plot is more informative than the ROC plot when evaluating binary classifiers on imbalanced datasets. *PLoS ONE* 10(3), e0118432.
- Steyerberg, E. W. et al. (2010). Assessing the performance of prediction models: a framework for traditional and novel measures. *Epidemiology* 21(1), 128-138.
- Lucas, R. E. (1976). Econometric policy evaluation: a critique. *Carnegie-Rochester Conference Series on Public Policy* 1, 19-46.
- Manski, C. F. (2015). Communicating uncertainty in official economic statistics. *Journal of Economic Literature* 53(3), 631-653.
- Asner, G. P. and Tupayachi, R. (2017). Accelerated losses of protected forests from gold mining in the Peruvian Amazon. *Environmental Research Letters* 12, 094004 (PDF in `data_raw/literature/`; quote on the 521 ha).
- Pacsi, R. et al. (2026). MAAP #241, Rapid expansion of illegal gold mining in Tambopata National Reserve.
- CSF (Conservation Strategy Fund) (2023). Metodología de valorización de la minería ilegal de oro en Perú (PDF in `data_raw/literature/`; parameters in `docs/walkthrough/notes/economics_sources.md`).
