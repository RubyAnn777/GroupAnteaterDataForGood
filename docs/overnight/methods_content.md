<!--
Source of docs/overnight/METHODS.html (how everything is built). Build: `uv run python docs/overnight/build_report.py`.
Same placeholder, claim-tag and block syntax as explainer_content.md. Organised by the question each method answers.
-->

# How the analysis is built: one command, every number traceable

> One chapter per method: the question it answers, how it works, what it controls for, what it can't, and where the code lives. Version: plan v2 after the critical review (12 Oct 2026).

@part Overview

## Pipeline | One command builds every number, figure and page

**`uv run python code/main.py` checks the data against the publishers, builds every measure, fits every model, draws every figure and writes every number to `output/numbers.csv`.**

{{PIPELINE_DIAGRAM}}

- **Data:** satellite maps of mining (MapBiomas, Amazon Mining Watch, INPE and GLAD alerts), boundaries (parks, buffer zones, corridor, communities), and context (gold price, gold output, spending, fines).
- **Measures:** how much *new* mining appears each year, per area.
- **Comparisons:** the targeted area against areas that show what might have happened without the operation.

**Why it matters:** any number in the brief can be traced: brief → `numbers.csv` → the function that made it → the raw file → the publisher.

## Claim labels | Every claim says what kind of claim it is

| Label | Means | Example |
|---|---|---|
| [[D]] | what happened | "net new mining fell from {{mean_add_tambopata_2016_18}} to {{mean_add_tambopata_2019_21}} ha/yr" |
| [[P]] | what we expect next time | "a return within about three years" |
| [[C]] | what caused it | used once, *conditional* on the comparison areas being a fair counterfactual |

**Why it matters:** grading puts 30% on honesty about the claim. A causal claim by accident is the main way to lose points.

@part Data and measures

## Data | One check per dataset, and no mixing of sources

**We never add or subtract numbers from different sources or collections.** Different products measure different things.

| Data | What it measures | Years | Used for | Check against publisher |
|---|---|---|---|---|
| **MapBiomas Peru, Collection 4** (course tables + our raster download) | Land class of every 30 m pixel each year; class 30 = mining (legal and illegal) | 1985–2025 | Main outcome, Peru | Tambopata buffer zone 2025 = 20,730 ha ✔ |
| **MapBiomas Peru rasters** | Same product, as maps, so we can use our own boundaries | 1985–2025 | All Peru zones | Raster gives {{v2_check_tambopatabufferzone_2025}} ha vs 20,730 ✔ |
| **Amazon Mining Watch (AMW)** | Gold-mining scars found by a machine-learning model, in 480 m squares | 2018–2026 | Twin search, Brazil, robustness | No published totals |
| **MapBiomas Amazonía, Collection 6** | Same idea as MapBiomas, all nine Amazon countries | 1985–2023 | Pre-2019 trend of candidate twins | Amazon mining 2023 = 0.78 Mha ✔ |
| **MapBiomas Brazil, Collections 10.1 and 11** | Mining per indigenous territory and per municipality | 1985–2025 | Brazil | Garimpo 2025 = 445,987 ha ✔ |
| **INPE DETER alerts** | Monthly alerts of new mining, Brazil | 2016–2026 | Brazil timing | 2019 total within 0.2% ✔ |
| **GLAD-L alerts** (University of Maryland) | Forest loss, each Landsat pixel dated to the day | 2017–2026 | Timing within the year | — |
| **Boundaries** | SERNANP parks and buffer zones; INGEMMET legal corridor; RAISG roads and protected areas; MapBiomas Amazonía native communities; FUNAI territories | current | Zones | — |
| **Context** | World Bank gold price; MINEM and central-bank gold output; MEF spending (PP 0128); IBAMA fines | various | Context only | Gold Aug 2026 = $4,411/oz ✔ |

**Why it matters:** the instructor will trace one number back to the publisher. Each check is logged in `output/checks.csv` and `DOWNLOAD_LOG.csv`.

## Measures | We count change, not stock, and split it into its parts

**Total mining area only grows, like the gold price, so totals correlate with almost anything. We count change.**

- **Addition** (the course measure) = mining area this year − mining area last year, per area, in hectares.
- **Rule:** add up all rows of an area *first*, then take the difference.

| Part | A pixel that is… | Tells us |
|---|---|---|
| **New land** (first-time mining) | mining now, never mining before | expansion into forest or new ground |
| **Re-mined** (return to old pits) | mining now, not last year, but mining in some earlier year | miners returning to old pits |
| **Stopped** | mining last year, not now | abandoned, regrowing, or reclassified |
| **From forest** | mining now, forest last year | forest lost to mining |

`addition = new land + re-mined − stopped`, checked in code for every area and year.

**Can't see:** river dredges, mercury, who mines, and whether a site is legal. Satellites see bare ground and ponds.

## Zones | One zone map on the raster grid, first match wins

**Each pixel belongs to exactly one zone, in this order:**

1. Tambopata reserve
2. Other reserves and parks
3. Kotsimba (native community)
4. Other native communities
5. **Corridor across the road:** the legal corridor directly north of the Interoceanic Highway, opposite La Pampa, within 10 km
6. Rest of the legal corridor
7. **La Pampa sector:** the Tambopata buffer zone between longitudes 70.15° and 69.80° W
8. Rest of the Tambopata buffer zone
9. Amarakaeri buffer zone
10. Bahuaja-Sonene buffer zone
11. Other buffer zones
12. Rest of Madre de Dios

- **Two zones have no official boundary:** La Pampa and "across the road". We define them by longitude and test a narrower and a wider version.
- **Road bands:** inside the La Pampa longitudes, every pixel gets its distance to the highway (north = positive).

**Why it matters:** "Tambopata buffer zone" mixes La Pampa (shut down) with new fronts. The zone map separates the stories.

**Code:** `code/raster_zones.py`.

@part Did it fall?

## Placebos | How a fake test replaces a standard error

**Question:** is the real result bigger than what "nothing happened" looks like in these data?

- **Fake place (placebo in space):** give the operation to each other unit in turn, re-run the identical analysis, rank the real result. Randomization p = rank / number of units (Abadie, Diamond & Hainmueller, 2010).
- **Fake date (placebo in time):** pretend the operation started earlier (2016) and re-run on pre-2019 data only. A real effect should vanish.
- **Fake border:** move the RD cut-off 2–4 km into one side. A real border effect shouldn't appear there.
- **Floor:** p can't go below 1 / n (with 15 zones, {{model_m1_ri_p:.2f}}).
- **What a pass proves:** the result is unusual. Not that Mercurio caused it: a shock that hit only Tambopata in 2019 also passes.

**Code:** `code/placebo_explainer.py` (figure), and each estimator's own module.

## 2×2 | Before and after, against a neighbour

**Question:** did the targeted zone change more than a comparison zone?

- **How:** gap change = (targeted after − before) − (comparison after − before). Before = 2016–18, during = 2019–21, after = 2022–25.
- **Controls for:** anything that moved both zones equally (gold price, COVID, national policy).
- **Can't control for:** anything that hit only one zone. Spillovers into the comparison zone make the gap look bigger.
- **Result:** {{did_main}} ha/yr against Amarakaeri, which was itself partly treated. [[D]]

**Code:** `code/peru.py` (`describe_and_compare`).

## Event study | Year by year, against 14 zones, with fake places

**Question:** is the fall bigger than normal year-to-year noise?

`y_zt = α_z + γ_t + Σ_k β_k · [z = Tambopata] · [t = k] + ε_zt`, with 2018 left out.

- **Zone effect (α):** each zone's normal level. **Year effect (γ):** each year's shock shared by all zones (gold price, COVID). **β_k:** how far Tambopata sits from the others in year *k*, relative to 2018.
- **Fake places:** each other zone gets the "operation" in turn, with Tambopata removed from its comparison pool. Tambopata ranks 1 of {{model_m1_n}} (p = {{model_m1_ri_p:.2f}}, the smallest possible).
- **Why no error bars:** with one treated zone, standard errors are not trustworthy (Conley and Taber, 2011). The rank is the honest substitute.

**Code:** `code/peru.py` (`run_event_study`), estimated with `pyfixest`.

## Model ladder | Does the fall survive harder controls?

| Model | Adds | What it rules out |
|---|---|---|
| **M1** | zone + year effects | shared shocks (gold price, COVID) |
| **M2** | + each zone's pre-2019 size × log gold price | big zones reacting more to a price rise |
| **M3** | + a straight-line trend per zone | zones that were already drifting apart |
| **M4** | outcome scaled to each zone's own 2014–18 average | Tambopata's size driving the result |

- **Fake 2016 date:** each model also runs on 2011–18 data with a fake start. A trustworthy model shows a big real effect and a small fake one.
- **Result:** the 2019–21 gap is {{model_m1_during}} to {{model_m3_during}} ha/yr (M1–M3, rank 1 of {{model_m1_n}}). Scaled to size (M4) it ranks {{model_m4_rank:.0f}} of {{model_m4_n:.0f}} (p = {{model_m4_ri_p:.2f}}). M3's fake date ({{model_m3_placebo}}) has the same sign as the real effect. A variant of M3 that fits Tambopata's trend on pre-years only gives {{model_m3pre_during}} ha/yr (2022–25: {{model_m3pre_after}}). [[D]]

**Code:** `code/peru_models.py`. The numpy fit is checked against `pyfixest`.

## Cell panel | 1-km cells with clustered errors and a wild bootstrap

**Question:** does the fall hold per square kilometre, against cells that weren't displacement targets?

- **Units:** every 1-km cell in the study window (lon 70.65–69.30 W, lat 13.30–12.40 S); {{st_n_cells}} cells, 2014–2025 for the DiD (baseline 2014–18), 2010–2025 for event studies.
- **Comparison cells:** outside every named zone, the legal corridor and native communities ({{st_n_ref_cells_clean:.0f}} cells). Cells never mined stay in, with zeros (dropping them would select on the outcome).
- **Model:** `y_ct = a_c + g_t + Σ b_zp [zone = z][period = p]`, y = first-time mining (ha); cell and year fixed effects.
- **Errors:** clustered by 10 × 10 km blocks ({{st_n_clusters:.0f}} clusters), so nearby cells can share shocks.
- **Wild cluster bootstrap:** restricted (WCR), 999 Rademacher draws over 10-km blocks, after removing cell and year effects. Needed because only {{st_clusters_lp:.0f}} (La Pampa) and {{st_clusters_across:.0f}} (across the road) blocks contain the treated zones. Cached in `data_intermediate/wcb_cache_v2.csv` (delete to recompute, ~30 s).
- **Event studies:** year-by-year coefficients against the pooled 2014–18 reference, plus a joint test that the 2010–13 leads are zero.
- **Robustness:** gold-bearing land × year effects; returns to old pits as outcome; Poisson (PPML) for zeros.
- **Road gradient:** distance bands north/south of the highway × period, reference = 10–30 km south.

**Result:** La Pampa {{st_main_lapampasector_during:+.2f}} ha per cell-year in 2019–21 (p = {{st_main_lapampasector_during_p:.2f}}; bootstrap p = {{st_wcb_lp_p:.2f}}), pre-trends fail (p = {{st_event_lp_pretrend_p:.3f}}). Corridor across the road {{st_main_corridoracross_during:+.2f}} (p = {{st_main_corridoracross_during_p:.2f}}), pre-trends pass. [[D]]

**Code:** `code/v2_stats.py`.

## Context controls | COVID exposure and enforcement money

**Question:** does the 2019–21 gap survive controls for what year effects can't remove?

- **Base (K0):** model M2 on 2015–25 (spending data start in 2015).
- **K1:** + each zone's 2014–18 mean addition × 1[2020–21] (COVID exposure).
- **K2:** + Madre de Dios × ln(PP 0128 spending booked in Madre de Dios).
- **K3:** both. Inference by fake places.
- **Caveat:** money rose with Mercurio, so it is partly the treatment itself (a bad control): K2 absorbs part of the effect.
- **Result:** COVID exposure alone shrinks the gap to {{ctx_k1_during:,.0f|abs}} of {{ctx_k0_during:,.0f|abs}} ha/yr; both controls give {{ctx_k3_during}} ({{ctx_k3_vs_k0_share:.0%}} of K0); rank {{ctx_k3_rank:.0f}} of {{ctx_n:.0f}} throughout. [[D]]

**Code:** `code/peru_context_models.py`.

## Synthetic DiD | Trend-matched weights plus a free intercept

**Question:** does a method built for few treated units agree with the model ladder?

- **How:** unit weights (≥ 0, sum 1, ridge-regularised) match the comparison zones' 2014–18 *trend* to Tambopata's; time weights pick the pre-years that best predict the post years; a free intercept absorbs the level gap (Arkhangelsky et al., 2021).
- **Check:** with equal weights it reproduces M1 exactly.
- **Result:** {{sdid_sdid_ha_during}} ha/yr in 2019–21 (rank 1 of {{sdid_sdid_ha_during_n:.0f}}); scaled, rank {{sdid_sdid_scaled_during_rank:.0f}} of {{sdid_sdid_scaled_during_n:.0f}}; 2022–25 {{sdid_sdid_ha_after:+,.0f}}. [[D]]

**Code:** `code/peru_sdid.py` (own FISTA solver for the simplex weights).

## Synthetic twin | A weighted mix of zones, fitted before 2019

**Question:** can a weighted mix of other zones copy Tambopata before 2019?

- **How:** weights (≥ 0, summing to 1) on other zones so the mix tracks Tambopata in 2010–18. After 2019, the gap is the estimate.
- **Why it fails:** Tambopata added more mining than any other zone. A weighted average of small numbers can't reach a big one. It only fits after scaling each zone to its own size, and then only {{synth_core_addsc_n_units_ranked}} zones remain.

**Code:** `code/peru_synth.py`.

## Rule-based twins | One real area that looks like La Pampa (Ruby's design)

**Question:** is there an existing area that looks like La Pampa but had no operation?

**Rules, applied to {{ctl_n_areas}} areas across the Amazon:**

1. **R1** mining before 2019 (≥ 500 ha seen by AMW by 2018)
2. **R2** no operation reported 2017–25 (documented web search, every query logged)
3. **R3** outside Madre de Dios
4. **R4** lowland mining (< 500 m) of similar scale (≥ ⅕ of Tambopata); the closest match wins

- **Result:** no area passes. Relaxing R2 to "no operation in 2017–21" leaves two: **Amanã National Forest** and the **Tapajós protection area** (Brazil). Munduruku was dropped (an operation reported in May 2021, search snippets only).
- **Comparison:** new mining per year as a share of each area's own 2018 mining, same product (AMW) for both. Pre-2019 trends come from each area's own MapBiomas collection, side by side, never subtracted.
- **Pre-trend test:** yearly log-growth difference (Tambopata minus twin), 2010–18, on a constant and a trend, Newey-West errors. Tambopata grew faster than both twins before 2019 (p = {{top3_amana_pre_trend_p:.2f}} Amanã, {{top3_tapajos_pre_trend_p:.2f}} Tapajós), so the twins are a weak check. No significance test for the gap (three years per area).

**Code:** `code/control_amw.py`, `control_elevation.py`, `control_mb_amazonia.py`, `control_select.py`, `control_top3.py`.

## Matching | Seven ways to let an algorithm pick the twin

**Question:** do formal matching estimators agree with Ruby's hand-set rules?

- **Pool:** {{psm_n_pool:.0f}} areas with no operation in 2017–21, ≥ 100 ha of mining by 2018, outside Madre de Dios ({{psm_n_units:.0f}} areas with AMW data).
- **Propensity score:** logit of "operation 2017–21" on log 2018 stock, median elevation of the mining, log area, country and type; {{psm_ps_n:.0f}} areas with known status.
- **Estimators:** propensity nearest 1 and 5; Mahalanobis nearest 1 and 3; coarsened exact matching; entropy balancing; inverse-probability weighting.
- **Outcome:** new mining per year as % of the 2018 stock (same as the twin). Inference by placebo in space.
- **Limit:** with one treated unit, matching is a distance rule. Tambopata's score ({{psm_ps_tam:.2f}}) is above every pool area ({{psm_ps_pool_max:.2f}}): no common support.
- **Result:** gaps {{psm_gap_during_min:+.1f}} to {{psm_gap_during_max:+.1f}} pp; placebo p {{psm_p_min:.2f}}–{{psm_p_max:.2f}}. [[D]]

**Code:** `code/control_psm.py`.

@part Where did it go?

## Displacement layers | Stream, Sankey, corridor share and legality

- **Stream chart:** land mined for the first time, per zone and year. First-time mining ignores year-to-year map flicker.
- **Sankey:** per period, new mining split into new land vs old pits, flowing into zones. Flows are pixels, not people.
- **Corridor share:** first-time mined land inside the legal corridor, as a share of Madre de Dios.
- **Legality:** every pixel of first-time mining crossed with MAAP #235's legality layer (Low / Medium / High / Very high). Time-consistent version: a concession counts only if filed by the mining year.
- **Second product:** Amazon Mining Watch on the same zones. It flags a 480 m square only once, so it misses infill.

**Code:** `code/raster_layers.py`, `code/v2_legality.py`, `code/v2_extra.py`, `code/v2_products_check.py`.

## Spatial RD | A difference in discontinuities at two borders

**Question:** did land just across a legal line change differently after 2019?

- **Borders:** the Interoceanic Highway in La Pampa's longitudes (south = La Pampa sector, north = corridor) and the Tambopata reserve edge (where outside is buffer zone). No new polygons: signed distances from the existing road line and the SERNANP reserve polygon.
- **Units:** 250-m distance bins × 2-km segments. Outcome: first-time mined land, % of the unit per year.
- **Estimator:** `rdrobust`, local linear, triangular kernel, MSE-optimal bandwidth, robust bias-corrected CI, clustered by segment. Main estimate on the change (2019–21 mean minus 2014–18 mean), so fixed border effects (the road's access, the river) cancel (Grembi, Nannicini & Troiano, 2016).
- **Checks:** fixed bandwidths 1–5 km; 500-m donut; fake start years; fake borders ±2–4 km.
- **Limit:** displacement across the border breaks the no-spillover assumption, so the road estimate is the swing (deterrence + displacement), an upper bound on either side.
- **Result:** road {{rd_road_did:+.2f}} pts (p = {{rd_road_did_p:.2f}}; across bandwidths and the donut p = {{rd_road_sens_p_min:.2f}}–{{rd_road_sens_p_max:.2f}}; fake start years from {{rd_road_fake_first_year:.0f}}: rank {{rd_road_fake_rank:.0f}} of {{rd_road_fake_n:.0f}}, p = {{rd_road_fake_p:.2f}}). Reserve edge {{rd_reserve_did:+.2f}} (p = {{rd_reserve_did_p:.2f}}; fake start years rank {{rd_reserve_fake_rank:.0f}} of {{rd_reserve_fake_n:.0f}}, p = {{rd_reserve_fake_p:.2f}}). [[D]]

**Code:** `code/v2_rdd.py`.

## Road tests | Fake start dates and depth into the corridor

- **Fake start dates (T1):** the north share's change, 3 years after minus 3 years before, for every start year 2008–2022. Only start years whose windows don't overlap the event count. Randomization p = rank of the real 2019 shift / number of start years: rank {{t1_road_shift_rank_clean:.0f}} of {{t1_road_shift_n_clean:.0f}} (p = {{t1_road_shift_ri_p_clean:.2f}}).
- **Depth (T9):** mean distance north of the highway of first-time mining per year; OLS on a trend and a post-2019 dummy with Newey-West errors (18 years). Break {{t9_depth_post2019:+.1f}} km (p = {{t9_depth_post2019_p:.3f}}).
- **Boundary sensitivity (T4):** narrow and wide La Pampa windows give the same picture.

**Code:** `code/v2_tests.py`.

@part When and why?

## Timing and gold | Quarterly alerts, gold left, money and the earlier wave

- **Quarterly timing:** GLAD-L alerts on land MapBiomas maps as mining. Compare the same quarter across years (clouds); data version break in 2021.
- **Gold left:** gold-bearing land = INGEMMET geology units (river deposits plus Madre de Dios Formation terraces). Validation: {{gold_broad_validation:.0%}} of all land ever mined lies on them. Depletion = share of a zone's gold-bearing land mined by a year.
- **Enforcement money (T8):** executed PP 0128 spending booked in Madre de Dios, 2015–2025. Department level only; a lower bound.
- **Earlier wave (T3):** model M1 with Tambopata × 2012–13 on 2008–16 data. Tambopata did not fall more than other zones (rank {{t3_wave_rank:.0f}} of {{t3_wave_n:.0f}}); La Pampa first-time mining changed by {{tl_dip_2012_13:+.0%}} in 2012–13 vs 2010–11. Asner & Tupayachi (2017) report a dip on their own maps; ours show none.
- **Declared gold:** MINEM yearly files split into producer-declared gold and the artisanal estimate (until 2019); checked against the central bank for 2012 and 2019.

**Code:** `code/glad_alerts.py`, `code/raster_gold.py`, `code/v2_tests.py`, `code/peru_gold_minem.py`.

## Economics | Cited parameters times our hectares, as ranges

**Question:** what is the mining worth, what does it cost, and what is spent against it? *Informed speculation.*

- **Chain:** land mined for the first time (returns to old pits get no gold: CSF has no yield for them, so both ends understate if old pits still pay) × {{eco_param_yield_kg_ha_lo:.1f}}–{{eco_param_yield_kg_ha_hi:.1f}} kg gold per ha (CSF, 2023) × mean gold price → value. Declared share = MINEM producer-declared gold / that gold.
- **Taxes:** 0% royalty for small producers (Ley 28258); income tax 29.5% × 11–37% margin on undeclared value.
- **Costs:** {{eco_param_hg_per_au_lo:.1f}}–{{eco_param_hg_per_au_hi:.1f}} kg mercury per kg gold; social cost per kg from two separate CSF estimates, never merged: US$ {{eco_param_social_calc_usd_kg_lo:,.0f}}–{{eco_param_social_calc_usd_kg_hi:,.0f}} (calculator) and US$ {{eco_param_social_pdf_usd_kg_lo:,.0f}}–{{eco_param_social_pdf_usd_kg_hi:,.0f}} (2023 report, p. 7). Enforcement: PP 0128 Madre de Dios spending, each year converted at its BCRP annual average (e.g. {{eco_param_pen_per_usd_2019:.2f}} soles per US$ in 2019, {{eco_param_pen_per_usd_2025:.2f}} in 2025).
- **Cross-check:** MINEM's 2016–18 estimate implies {{eco_implied_kg_ha_2016_18:.1f}} kg per hectare we mapped.
- **Result (2022–25, per year):** gold {{eco_gold_t_lo_2022_25:.0f}}–{{eco_gold_t_hi_2022_25:.0f}} t, declared {{eco_declared_share_lo:.0%}}–{{eco_declared_share_hi:.0%}}, untaxed income US$ {{eco_tax_musd_lo:,.0f}}–{{eco_tax_musd_hi:,.0f}} M, social cost US$ {{eco_social_busd_calc_lo:,.1f}}–{{eco_social_busd_calc_hi:,.1f}} bn (calculator) or {{eco_social_busd_pdf_lo:,.0f}}–{{eco_social_busd_pdf_hi:,.0f}} bn (report), enforcement US$ {{eco_spend_musd:,.1f}} M. [[P]]

**Code:** `code/v2_economics.py`; sources and quotes in `docs/overnight/notes/economics_sources.md`.

@part Brazil and prediction

## Brazil | Staggered operations, same pixel method

**Question:** do territories fall after *their own* operation?

- **Data:** MapBiomas Brazil Collection 11 rasters read remotely per territory (24 territories + Yanomami rings). Check: Kayapó 2024/2025 vs the platform.
- **Model:** territory + year effects, treated from each territory's first *verified* operation in 2021–25 (Munduruku Aug 2023, Kayapó Sep 2024); Gardner's two-stage estimator (`did2s`, two-sided p); randomization inference (2,000 shuffles of operation dates, one-sided, on the two-way fixed-effects estimate).
- **Pool:** {{brv2_never_n:.0f}} never-treated territories, of which {{brv2_never_n_unsearched:.0f}} were never searched for operations.
- **Logic:** if operations cause falls, each territory should fall after its own date, not before.
- **Result:** did2s {{brv2_did2s_treat:+.2f}} log points (two-sided p = {{brv2_did2s_treat_p:.2f}}); two-way fixed effects {{brv2_twfe_treat:+.2f}} (p = {{brv2_twfe_treat_p:.2f}}; one-sided randomization p = {{brv2_ri_p:.2f}}). Wrong sign, not significant. [[D]]

**Code:** `code/brazil_raster.py`, `brazil_v2.py`, `brazil_stagger.py` (AMW), `brazil_deter_all.py`.

## Risk map | A prediction, tested out of sample

- **Model:** logit on 1-km cells. Features: distance to highway and rivers, north side, gold-bearing share, mined share, mining within ~3 km, zone.
- **Validation:** trained on 2018 → 2019–21, tested on 2021 → 2022–25 in held-out 10-km blocks, against a "mining nearby" benchmark. AUC {{risk_auc_spatial_holdout:.2f}} vs {{risk_auc_benchmark:.2f}}. [[P]]
- **Use:** applied to 2025 → 2026–28. It misses river-borne incursions into the reserve.

**Code:** `code/v2_extra.py` (E4).

@part Review

## Review fixes | What a critical referee found, and what changed

- **Fake places:** Tambopata removed from each placebo's comparison pool (before, its own fall made every placebo positive). Amazon-only pool added.
- **Causal number:** reworded to net mining; first-time mining reported alongside.
- **Cell panel:** clean comparison cells, 2014–18 baseline, pooled reference in event studies, wild cluster bootstrap.
- **Twins:** Munduruku dropped; no p-values on three annual values.
- **Brazil:** first operation inside 2021–25 (Kayapó 2024-09; Munduruku 2023-08, the first verified operation).
- **Legality:** a concession counts only if filed by the mining year.
- **Risk map:** spatial hold-out and benchmark.
- **Gold proxy:** lift reported (share of mining vs share of land).
- **Untraceable numbers** (Sentinel-2, producer-declared gold) now computed in code.

:::more Where to find the rest
- **Full review:** `docs/overnight/notes/critical_review_v2.md`.
- **Plan and decisions:** `docs/PLAN_v2.md`, `docs/overnight/LOG.md`.
- **Qualitative sources:** `docs/overnight/notes/qualitative_background.md` (each with link and quote) and 30 papers in `literature_v2.md`.
- **Code map and every number:** the {{WALK_LINK}}, chapters Files and Appendix.
:::
