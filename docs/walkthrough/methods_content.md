<!--
Source of docs/walkthrough/METHODS.html (how everything is built). Build: `uv run python docs/walkthrough/build_report.py`.
Same placeholder, claim-tag and block syntax as explainer_content.md. Organised by the question each method answers.
Plan v3 (docs/PLAN_v3.md, code/definitions.py): one outcome (net mining additions = new + re-mined − stopped),
one zone registry, one treatment (Mercurio, Feb 2019; first treated year 2019; reference 2018).
-->

# How the analysis is built: one outcome, one zone map, one treatment

> One chapter per method: the question it answers, how it works, what it controls for, what it can't, and where the code lives. Version: plan v3 (15 Oct 2026). Every number comes from `output/numbers.csv`.

@part Overview

## Pipeline | One command builds every number, figure and page

**`uv run python code/main.py` checks the data against the publishers, builds the zone registry and the pixel accounting, fits every model, draws every figure and writes every number to `output/numbers.csv`.**

{{PIPELINE_DIAGRAM}}

- **Data:** MapBiomas Peru Collection 4 annual maps (the outcome); other products as checks only (Amazon Mining Watch, GLAD alerts, MapBiomas Amazonía and Brazil); boundaries (SERNANP, INGEMMET corridor, RAISG roads, native communities, FUNAI); context (gold price, gold output, spending, fines).
- **One outcome:** net mining additions per zone and year, split into new land, re-mined and stopped.
- **Comparisons:** the targeted zone against zones and areas that might show what would have happened without the operation.

**Why it matters:** any number in the brief can be traced: brief → `numbers.csv` (id, value, unit, measure, zone, period, description) → the function that made it → the raw file → the publisher.

## Claim labels | Every claim says what kind of claim it is

| Label | Means | Example |
|---|---|---|
| [[D]] | what happened | "net additions in the Tambopata buffer zone fell from {{tambopata_bz_pre_net}} to {{tambopata_bz_during_net}} ha/yr (2016–18 vs 2019–21)" |
| [[P]] | what we expect next time | "new pits in a ring around the next operation" |
| [[C]] | what caused it | used once, *conditional* on the other Peruvian buffer zones being a fair counterfactual (the brief's sentence) |

**Why it matters:** grading puts 30% on honesty about the claim. A causal claim by accident is the main way to lose points.

@part Data and definitions

## Data | One check per dataset, and no mixing of sources

**We never add or subtract numbers from different sources or collections.** Different products measure different things.

| Data | What it measures | Years | Used for | Check against publisher |
|---|---|---|---|---|
| **MapBiomas Peru, Collection 4 rasters** | Land class of every 30-m pixel each year; class 4.2 Minería = all mining (legal and illegal) | 1985–2025 | **The outcome**, every Peru zone | Tambopata buffer zone 2025: {{chk_tbz_2025_ours}} vs {{chk_tbz_2025_pub}} ha; reserve {{chk_tnr_2025_ours:,.1f}} vs {{chk_tnr_2025_pub}}; Madre de Dios {{chk_mdd_2025_ours}} vs {{chk_mdd_2025_pub}} |
| **MapBiomas Peru statistics workbook** (course tables) | Mining per buffer zone, department | 1985–2025 | Reproduction and reconciliation checks only | Card numbers reproduce in `checks.py` |
| **Amazon Mining Watch (AMW)** | Gold-mining scars found by a model, 480-m squares; no "stopped" state | 2018–2026 | Twins, matching, a second product for displacement | No published totals |
| **GLAD-L alerts** (University of Maryland) | Forest loss, each Landsat pixel dated to the day | 2017–2026 | Timing within the year | — |
| **MapBiomas Amazonía, Collection 6** | Mining stock, nine Amazon countries | 1985–2023 | Pre-2019 paths of the twins | Amazon mining 2023: {{chk_mb_amazonia_2023_ours}} vs {{chk_mb_amazonia_2023_pub}} ha |
| **MapBiomas Brazil, Collection 11** (rasters and statistics) | Mining per territory | 1985–2025 | Brazil (backup) | Indigenous lands 2025: {{chk_br_ti_2025_ours}} vs {{chk_br_ti_2025_pub}} ha; Kayapó {{chk_kayapo_2025_ours}} vs {{chk_kayapo_2025_pub}} |
| **INPE DETER alerts** | Monthly alerts of new mining, Brazil | 2016–2026 | Brazil timing | 2019: {{br_deter_2019_total_wfs_km2:.2f}} vs {{br_deter_2019_total_dashboard_km2:.2f}} km² |
| **Boundaries** | SERNANP parks and buffer zones; INGEMMET legal corridor (D.L. 1100); RAISG roads and protected areas; native communities; FUNAI territories | current | Zones | — |
| **Context** | World Bank gold price; MINEM and central-bank gold output; MEF spending (PP 0128); IBAMA fines | various | Context only | Gold Aug 2026 {{chk_gold_aug2026_ours}} vs {{chk_gold_aug2026_pub}} $/oz; MINEM vs BCRP 2019 {{chk_bcrp_2019_ours}} vs {{chk_bcrp_2019_pub}} kg; PP 0128 2019 {{chk_pp0128_2019_ours}} vs {{chk_pp0128_2019_pub}} soles |

**Why it matters:** the instructor will trace one number back to the publisher. Each check is logged in `output/checks.csv` and `DOWNLOAD_LOG.csv`.

## Outcome | Net mining additions, split into three parts

**Total mining area only grows, like the gold price, so totals correlate with almost anything. We count the yearly change, and we split it.**

`net additions(t) = mining(t) − mining(t−1) = new land + re-mined − stopped`, per zone, ha/yr, checked in code for every zone and year.

| Part | A pixel that is… | Tells us |
|---|---|---|
| **New land** (first-time mining) | mining now, never mining in any earlier year since 1985 | expansion into forest or new ground |
| **Re-mined** | mining now, not last year, but mining in some year before | old pits worked again |
| **Stopped** | mining last year, not now | the pit left the mining class: flooded, regrowing, bare, or reclassified |

- **Stopped, split further** (no image check; plan v3 V3-5): what the land becomes the next year (water, forest, bare ground, other) and whether it is mining again within two years. The water share collapses in 2023–25 in every zone, an end-of-series effect of the map, so later-years shares are not compared with earlier ones.
- **Linear estimators** (DiD, two-way fixed effects, event studies, RD at a fixed bandwidth) give the four estimates that add up: net = new + re-mined − stopped. **Non-linear ones** (ratios, logs, Poisson, weights fitted on net) say so next to the number.
- **The stopped share of a fall** is counted four ways: the raw change in stopped land; without land mined again within two years; only stopping above the zone's 2016–18 rate; and relative to Amarakaeri. For the Tambopata buffer zone, 2016–18 to 2019–21, it runs {{tambopata_bz_stopped_share_of_fall_min:.0%}}–{{tambopata_bz_stopped_share_of_fall_max:.0%}}. [[D]]
- **Other products cannot give net additions:** AMW and GLAD have no "stopped" state. They appear only as checks of timing and of the twins, labelled with their own measure.

**Can't see:** river dredges, mercury, who mines, and whether a site is legal. Satellites see bare ground and ponds.

**Code:** `code/definitions.py` (OUTCOME), `code/raster_zones.py`.

## Zones | One registry on the raster grid, official boundaries whole

**Each pixel belongs to exactly one zone, first match wins, in this order:**

1. Tambopata National Reserve
2. Other protected areas
3. **La Pampa sector:** the Tambopata buffer zone between longitudes 70.15° and 69.80° W
4. Rest of the Tambopata buffer zone
5. Amarakaeri buffer zone (whole, incl. its Cusco part)
6. Bahuaja-Sonene buffer zone
7. Other buffer zones
8. **Corridor across the road:** the legal corridor (D.L. 1100) within 10 km north of the Interoceanic Highway, at La Pampa's longitudes, outside every buffer zone
9. Rest of the mining corridor
10. Native communities
11. Rest of Madre de Dios

- **Official buffer zones stay whole.** The Tambopata buffer zone (3 + 4) is the publisher's unit, Kotsimba included. Where official zones overlap, the land goes to Tambopata first, then Amarakaeri, as MapBiomas does.
- **Tenure is a tag, not a zone:** corridor, Kotsimba, other community, none. Corridor land inside a buffer zone stays in the buffer zone, tagged "corridor".
- **Two zones have no official boundary:** La Pampa and "across the road". We test a narrower and a wider window.
- **Road bands:** inside La Pampa's longitudes, every pixel gets its north-south distance to the highway (north = positive).
- **National panel** (zone designs): every Peruvian buffer zone with mapped mining, whole.

**What changed versus v2:** communities and the corridor used to take precedence over buffer zones, so the raster "Tambopata buffer zone" lacked Kotsimba (31,568 ha) and 21 km² of corridor, and zone designs used the workbook while pixel designs used the raster.

**Code:** `code/definitions.py` (ZONES, UNITS, TENURE), `code/raster_zones.py`, `code/zonedata.py`.

## Treatment | One start date; everything after it is context

- **The treatment:** the start of Operation Mercurio, February 2019, in the Tambopata buffer zone (La Pampa). Because addition(2019) = map 2019 − map 2018, **2019 is the first treated year and 2018 the reference year**.
- **Context, not separate treatments:** COVID-19 (2020), Plan Restauración (2021), Mercurio II (all of Madre de Dios), the April 2023 state of emergency, the 2025 navy withdrawal. Shown as dashed lines at Y − 0.5; not estimated.
- **Periods:** 2016–18 (before, the course card), 2014–18 (pooled reference for models), 2019–21 ("Mercurio and what followed"), 2022–25 ("later years", always also without 2023, a MapBiomas-only spike year). Never "after enforcement ended".
- **So every estimate measures "Mercurio together with what followed"**, never Mercurio alone.

**Code:** `code/definitions.py` (TREATMENT, PERIODS).

@part Did it fall?

## Placebos | How a fake test replaces a standard error

**Question:** is the real result bigger than what "nothing happened" looks like in these data?

- **Fake place (placebo in space):** give the operation to each other zone in turn (Tambopata removed from the pool), re-run the identical analysis, rank the real result. p = rank / number of zones (Abadie, Diamond & Hainmueller, 2010).
- **Raw vs scaled:** in hectares the biggest zone tends to rank first: the Tambopata buffer zone ranks {{placebo_space_rank_raw_preyear_2014:.0f}} in 2014, {{placebo_space_rank_raw_preyear_2015:.0f}} in 2015 and {{placebo_space_rank_raw_preyear_2016:.0f}} in 2016, before Mercurio. So we always give the scaled rank (coefficient / the zone's own 2014–18 mean, zones above 10 ha/yr) next to the raw rank.
- **Fake date (placebo in time):** pretend the operation started in 2016 and re-run on pre-2019 data only. A real effect should vanish.
- **Fake border:** move the RD cut-off 2–4 km into one side.
- **Floor:** p can't go below 1 / n (with 15 zones, {{model_m1_ri_p:.2f}}).
- **What a pass proves:** the result is unusual. Not that Mercurio caused it: a shock that hit only the target in 2019–21 also passes.

**Code:** `code/placebo_explainer.py` (figure), and each estimator's own module.

## 2×2 | Before and after, against a neighbour

**Question:** did the targeted zone change more than the less-treated neighbour?

- **How:** gap = (Tambopata after − before) − (Amarakaeri after − before), for net additions and each part. Before = 2016–18 (also 2014–18), during = 2019–21, later = 2022–25.
- **Controls for:** anything that moved both zones equally.
- **Can't control for:** anything that hit only one zone. Spillovers into Amarakaeri make the gap look bigger; Mercurio II in Amarakaeri makes it look smaller.
- **Result:** {{did_main_net}} ha/yr (2016–18 base), {{did_base2014_net}} (2014–18 base); fake start 2016 {{did_placebo_net:+,.0f}}. [[D]]

**Code:** `code/peru.py`, `code/peru_robust.py` (other comparison zones).

## Event study | Year by year, against 14 zones

**Question:** how far does the target sit from the comparison zones each year?

`y_zt = α_z + γ_t + Σ_k β_k · [z = Tambopata] · [t = k] + ε_zt`, net additions (and each part), 2018 left out.

- **Zone effect (α):** each zone's normal level. **Year effect (γ):** each year's shock *common to all zones*. It does not remove shocks that hit zones unequally (gold price, COVID). **β_k:** how far Tambopata sits from the others in year *k*, relative to 2018.
- **Pooled reference:** the mean of 2019–21 minus the mean of 2014–18 is {{es_poolB_pooledref_during_net}} ha/yr, equal to M1.
- **Why no error bars:** with one treated zone, standard errors are not informative (Conley and Taber, 2011). Ranks are the honest substitute: raw {{placebo_space_rank_raw:.0f}} of {{placebo_space_n:.0f}}, scaled {{placebo_space_rank_scaled:.0f}} of {{placebo_space_n_scaled:.0f}}.

**Code:** `code/peru.py`, estimated with `pyfixest`.

## Model ladder | Does the fall survive harder controls?

| Model | Adds | What it targets |
|---|---|---|
| **M1** | zone + year effects, pooled 2014–18 reference | shocks common to all zones |
| **M2** | + each zone's 2014–18 mean × log gold price | big zones reacting more to a price rise |
| **M3** | + a straight-line trend per zone | zones that were already drifting apart |
| **M4** | outcome scaled to each zone's own 2014–18 mean | Tambopata's size driving the result |

- **Fake 2016 date:** each model also runs on 2011–18 with a fake start. A trustworthy model shows a big real effect and a small fake one.
- **Result (net additions, 2019–21):** {{model_m1_during_net}} (M1), {{model_m2_during_net}} (M2), {{model_m3_during_net}} (M3) ha/yr, raw rank 1 of {{model_m1_n:.0f}}; scaled ranks {{model_m1_rank_scaled:.0f}}, {{model_m2_rank_scaled:.0f}}, {{model_m3_rank_scaled:.0f}} of 7; M4 rank {{model_m4_rank:.0f}} of {{model_m4_n:.0f}}. M3's fake date ({{model_m3_placebo_net:+,.0f}}) has the same sign as the real effect. M1's parts: new {{model_m1_during_new:+,.0f}}, re-mined {{model_m1_during_remined:+,.0f}}, stopped {{model_m1_during_stopped:+,.0f}}. [[D]]
- **The brief's range** uses M1 and the 2×2 on the 2014–18 baseline ({{model_m1_during_net:,.0f|abs}}–{{did_base2014_net:,.0f|abs}} ha/yr): pooled baseline, no extrapolated slope (review card 14, D-S14-3).

**Code:** `code/peru_models.py`. The numpy fit is checked against `pyfixest`.

## Cell panel | 1-km cells, clustered errors, a wild bootstrap

**Question:** does the fall hold per square kilometre?

- **Units:** every 1-km cell in the study window; {{st_n_cells:,.0f}} cells, 2014–2025 (reference 2014–18); event studies from 2011 (sensitivity from 2010). Majority registry zone per cell.
- **Comparison cells:** other protected areas, other buffer zones and the rest of Madre de Dios with tenure "none" ({{st_n_ref_cells_clean:,.0f}} cells). They hold almost no mining ({{st_n_ref_cells_depleted18:.0f}} had any by 2018), so **each coefficient is close to the zone's own before/after** and its p-value overstates. Keep cell p-values out of headlines.
- **Model:** `y_ct = a_c + g_t + Σ b_zp [zone = z][period = p]`, y = net additions (ha), and each part.
- **Errors:** clustered by 10 × 10 km blocks ({{st_n_clusters:.0f}} clusters); wild cluster bootstrap (restricted, 999 Rademacher draws) because only {{st_clusters_lapampa:.0f}} (La Pampa) and {{st_clusters_corridor_across:.0f}} (across the road) blocks contain the treated zones.
- **Pre-trends, two lead windows:** La Pampa 2011–13 p = {{st_event_lapampa_pretrend_net_p:.2f}}, 2010–13 p = {{st_event_lapampa_pretrend2010_net_p:.3f}}; corridor across the road 2011–13 p = {{st_event_corridor_across_pretrend_net_p:.2f}}, 2010–13 p = {{st_event_corridor_across_pretrend2010_net_p:.3f}}. La Pampa passes only without the 2010 lead.
- **Depletion:** gold-bearing bins × year; 2018-depletion bins × year; a hazard version (new land as % of not-yet-mined land): on that basis La Pampa's cell-level change is {{st_hazard_ols_lapampa_during:+.2f}} points (p = {{st_hazard_ols_lapampa_during_p:.2f}}).
- **Road gradient:** distance bands north/south of the highway × period, reference = 10–30 km south.

**Result:** La Pampa {{st_main_lapampa_during_net:+.2f}} ha of net additions per cell-year in 2019–21 (new {{st_main_lapampa_during_new:+.2f}}, re-mined {{st_main_lapampa_during_remined:+.2f}}, stopped {{st_main_lapampa_during_stopped:+.2f}}); corridor across the road {{st_main_corridor_across_during_net:+.2f}}. Description: a before/after per cell. [[D]]

**Code:** `code/v2_stats.py` (bootstrap cache keyed by an input hash).

## Context controls | COVID exposure and enforcement money

**Question:** does the 2019–21 gap survive controls for shocks that hit zones unequally?

- **Base (K0):** M2 on 2015–25 (spending data start in 2015), post years saturated.
- **K1:** + each zone's 2014–18 mean × 1[2020–21] (COVID exposure).
- **K2:** + Madre de Dios × ln(PP 0128 spending booked in Madre de Dios).
- **K3:** both. Inference by fake places.
- **Caveat:** money rose with Mercurio, so it is partly the treatment itself (a bad control).
- **Result (net additions, 2019–21):** K0 {{ctx_k0_during_net}}, K3 {{ctx_k3_during_net}} ha/yr. The COVID term moves the gap by {{ctx_shift_covid_during_net:+,.0f}} and the money term by {{ctx_shift_money_during_net:+,.0f}}: they offset, so K3 ≈ K0 is not a robustness check. Raw rank {{ctx_k3_rank:.0f}} of {{ctx_n:.0f}}, scaled {{ctx_k3_rank_scaled:.0f}} of {{ctx_n_scaled:.0f}}. [[D]]

**Code:** `code/peru_context_models.py`.

## Synthetic DiD | Weighted zones and pre-years, then a DiD

**Question:** does a method built for few treated units agree with the model ladder?

- **How:** unit weights (≥ 0, sum 1, ridge-regularised) chosen to make the comparison parallel to Tambopata in 2014–18; time weights pick the pre-years; a free intercept absorbs the level gap (Arkhangelsky et al., 2021).
- **Fit:** the weights explain {{sdid_pre_fit_r2:.0%}} of Tambopata's pre-2019 variation; the time weight is {{sdid_lambda_max:.0%}} on 2014.
- **Check:** with equal weights it reproduces M1 exactly.
- **Result (net additions):** {{sdid_sdid_ha_during_net}} ha/yr in 2019–21 (raw rank {{sdid_sdid_ha_during_rank:.0f}} of {{sdid_sdid_ha_during_n:.0f}}; scaled {{sdid_sdid_scaled_during_rank:.0f}} of {{sdid_sdid_scaled_during_n:.0f}}); {{sdid_sdid_ha_during_pre2011_net}} when fitted on 2011–18; later years {{sdid_sdid_ha_later_net:+,.0f}} ({{sdid_sdid_ha_later_ex2023_net:+,.0f}} without 2023). Sensitivity only. [[D]]

**Code:** `code/peru_sdid.py` (own FISTA solver for the simplex weights).

## Synthetic control | A weighted mix of zones, fitted before 2019

**Question:** can a weighted mix of other zones copy Tambopata before 2019?

- **How:** weights (≥ 0, sum 1) on other zones so the mix tracks Tambopata's net additions in 2014–18. After 2019, the gap is the estimate.
- **Why it fails:** Tambopata added more than any other zone. A weighted average of small numbers can't reach a big one: outside every donor's range in {{synth_core_add_hull_years_outside:.0f}} of 5 fit years. With Amarakaeri as a donor, all weight goes to it, and the gap ({{synth_ext_add_gap_during}} ha/yr) is just Tambopata minus Amarakaeri. Description of a misfit.

**Code:** `code/peru_synth.py`.

## Rule-based twins | One real area that looks like La Pampa (Ruby's design)

**Question:** is there an existing area that looks like La Pampa but had no operation?

**Rules, applied to {{ctl_n_areas:,.0f}} areas across the Amazon:**

1. **R1** mining before 2019 (≥ 500 ha seen by AMW by 2018)
2. **R2** no verified operation 2017–25 (documented web search; one dating rule R* for all scripts)
3. **R3** outside the registry region (Madre de Dios and the Tambopata and Amarakaeri buffer zones)
4. **R4** lowland mining (< 500 m) of similar scale (≥ ⅕ of Tambopata)

- **Result:** no area passes. Allowing verified operations after 2021 leaves {{ctl_n_relaxed:.0f}}: Amanã, Tapajós and Munduruku (Brazil); {{ctl_n_relaxed_excl_unverified:.0f}} if an unverified report disqualifies.
- **Measure:** AMW new area per year as a share of each area's own 2018 AMW area (comparable to new land, not to net additions). Pre-2019 paths from each area's own MapBiomas collection, side by side, never subtracted.
- **Result:** Tambopata at {{top3_ratio:.0%}} of the twins' mean pace in 2019–21, {{top3_ratio_excl_unverified:.0%}} without Munduruku. [[D]]
- **Pre-2019 test:** yearly log-growth gap (Tambopata minus twin), 2010–18, on a constant and a trend, Newey-West errors. The constant = mean growth gap; the trend = whether that gap was changing (it was shrinking: Tambopata converging). Not parallel. No significance test for the 2019–21 gap (three years per area).

**Code:** `code/control_amw.py`, `control_elevation.py`, `control_mb_amazonia.py`, `control_select.py`, `control_top3.py`.

## Matching | Letting an algorithm pick the twin

**Question:** do formal matching estimators agree with Ruby's hand-set rules?

- **Pool:** {{psm_n_pool:.0f}} areas with no operation in 2017–21, ≥ 100 ha of AMW mining by 2018, outside Madre de Dios ({{psm_n_units:.0f}} areas with AMW data).
- **Propensity score:** ridge-penalised logit of "operation 2017–21" on log 2018 stock, median elevation of the mining, log area, country and type; {{psm_ps_n:.0f}} areas with known status; caliper 0.25 SD of the logit score.
- **Estimators:** propensity nearest 1 and 5 (no control within the caliper); Mahalanobis nearest 1 and 3; coarsened exact matching; entropy balancing; inverse-probability weighting.
- **Outcome:** AMW new area as % of the 2018 AMW stock (same as the twins). Inference by placebo in space.
- **Limit:** with one treated unit, matching is a distance rule. Tambopata's score ({{psm_ps_tam:.2f}}) is above every pool area ({{psm_ps_pool_max:.2f}}): no common support.
- **Result:** gaps {{psm_gap_during_min:+.1f}} to {{psm_gap_during_max:+.1f}} percentage points; placebo p {{psm_p_min:.2f}}–{{psm_p_max:.2f}}. [[D]]

**Code:** `code/control_psm.py`.

@part Where did it go?

## Displacement layers | Streams, Sankey, corridor share and legality

- **Stream chart:** net additions per zone and year (zones with a net loss drawn below zero); a second stream for re-mined land.
- **Sankey:** per period, the gross inflow (new land and re-mined land) flowing into zones, with stopped land and net additions named. Flows are pixels, not people.
- **Corridor share:** net additions on corridor-tenure land (any zone, native communities excluded), period sum / period sum, and the same for new land.
- **Displacement bound:** the sum of rises in net additions in other Madre de Dios zones, divided by the target's fall ({{mdd_rise_elsewhere_vs_tambopata_fall:.1f}} for 2016–18 to 2019–21).
- **Legality (new land only, a per-pixel grade at first mining):** each pixel crossed with MAAP #235's legality layer (Low / Medium / High / Very high); time-consistent version counts a concession only if filed by the mining year.
- **Second product:** Amazon Mining Watch on the same zones; it flags a 480-m square only once, so it misses infill and has no net version.

**Code:** `code/raster_layers.py`, `code/v2_legality.py`, `code/v2_extra.py`, `code/v2_products_check.py`.

## Spatial RD | A difference in discontinuities at two borders

**Question:** did land just across a legal line change differently after 2019?

- **Borders:** the Interoceanic Highway at La Pampa's longitudes (south = La Pampa sector, north = corridor across the road) and the Tambopata reserve edge (where outside is buffer zone).
- **Units:** 250-m distance bins × 2-km segments. Outcome: net additions, % of the unit's land per year; parts at a fixed bandwidth, where they add up.
- **Estimator:** `rdrobust`, local linear, triangular kernel, MSE-optimal bandwidth, robust bias-corrected CI, clustered by segment. Main estimate on the change (2019–21 mean minus 2014–18 mean), so fixed border effects cancel (Grembi, Nannicini & Troiano, 2016). Also 2019 alone, 2022–25, and perpendicular distance to the road.
- **Checks:** fixed bandwidths 1–5 km; 500-m donut; fake start years; fake borders ±2–4 km.
- **Limit:** displacement across the border breaks the no-spillover assumption, so the road estimate is the swing, an upper bound on either side.
- **Result (net additions):** road {{rd_road_did_net:+.2f}} pts (p = {{rd_road_did_net_p:.2f}}; across bandwidths and the donut p = {{rd_road_sens_p_min:.2f}}–{{rd_road_sens_p_max:.2f}}; fake start years from {{rd_road_fake_first_year:.0f}}: rank {{rd_road_fake_rank:.0f}} of {{rd_road_fake_n:.0f}}). Reserve edge {{rd_reserve_did_net:+.2f}} (p = {{rd_reserve_did_net_p:.2f}}; fake start years rank {{rd_reserve_fake_rank:.0f}} of {{rd_reserve_fake_n:.0f}}). Uninformative on net. [[D]]

**Code:** `code/v2_rdd.py`.

## Road tests | Fake start dates and depth into the corridor

- **Fake start dates (T1):** the north share's change (net additions, and new land), 3 years after minus 3 years before, for every start year 2008–2022. Clean comparison: only start years whose windows don't overlap the event. Net additions: rank {{t1_road_shift_rank_clean_net:.0f}} of {{t1_road_shift_n_clean_net:.0f}} (p = {{t1_road_shift_ri_p_clean_net:.2f}}); new land: rank {{t1_road_shift_rank_clean_new:.0f}} of {{t1_road_shift_n_clean_new:.0f}}.
- **Depth (T9, new land only):** mean distance north of the highway of new land per year (a weighted ratio, not defined for net); OLS on a trend and a post-2019 dummy with Newey-West errors (18 years). Break {{t9_depth_post2019:+.1f}} km (p = {{t9_depth_post2019_p:.3f}}).
- **Boundary sensitivity (T4):** narrow and wide La Pampa windows give the same picture.

**Code:** `code/v2_tests.py`.

@part When and why?

## Timing and gold | Quarterly alerts, gold left, money and the earlier wave

- **Quarterly timing (another measure):** GLAD-L alerts on land MapBiomas maps as mining by the next year (no look-ahead). Compare the same quarter across years (clouds); data version break in 2021.
- **Gold left:** gold-bearing land = INGEMMET geology units (river deposits plus Madre de Dios Formation terraces). Validation: {{gold_broad_validation:.0%}} of all land ever mined lies on them. Depletion = share of a zone's gold-bearing land first mapped as mining by a year; cell terciles show local depletion.
- **Enforcement money (T8):** executed PP 0128 spending booked in Madre de Dios, 2015–2025. Department level only; a lower bound.
- **The 2012–13 check (T3):** M1-type model on 2008–16 with Tambopata × 2012–13 (net additions): {{t3_asner_2012_13_net:+,.0f}} ha/yr, rank {{t3_asner_rank:.0f}} of {{t3_asner_n:.0f}}. Asner & Tupayachi (2017) report a dip on their own maps; ours show none.
- **Declared gold:** MINEM yearly files split into producer-declared gold and the artisanal estimate (until 2019); compared with the central bank every year ({{gold_minem_bcrp_n_match:.0f}} of 25 years within 2%).

**Code:** `code/glad_alerts.py`, `code/raster_gold.py`, `code/v2_tests.py`, `code/peru_gold_minem.py`.

## Economics | Cited parameters times our hectares, as ranges

**Question:** what is the mining worth, what does it cost, and what is spent against it? *Informed speculation.*

- **Chain:** new land (first-time mining; not net additions) × {{eco_param_yield_kg_ha_lo:.1f}}–{{eco_param_yield_kg_ha_hi:.1f}} kg gold per ha (CSF, 2023) × mean gold price → value. Re-mined land gets no gold (CSF has no yield for old pits), so both ends understate if old pits still pay. Declared share = MINEM producer-declared gold, 2022–25 mean / that gold.
- **Taxes:** 0% royalty for small producers (Ley 28258, Art. 5); income tax 29.5% × 11–37% margin on undeclared value.
- **Costs:** {{eco_param_hg_per_au_lo:.1f}}–{{eco_param_hg_per_au_hi:.1f}} kg mercury per kg gold; social cost per kg from two separate CSF estimates, never merged: US$ {{eco_param_social_calc_usd_kg_lo:,.0f}}–{{eco_param_social_calc_usd_kg_hi:,.0f}} (calculator) and US$ {{eco_param_social_pdf_usd_kg_lo:,.0f}}–{{eco_param_social_pdf_usd_kg_hi:,.0f}} (2023 report, p. 7). Enforcement: PP 0128 Madre de Dios spending, each year converted at its BCRP annual average.
- **Cross-check:** MINEM's 2016–18 gold implies {{eco_implied_kg_ha_new_pre:.1f}} kg per hectare of new land we mapped.
- **Result (2022–25, per year):** gold {{eco_gold_t_lo_later:.0f}}–{{eco_gold_t_hi_later:.0f}} t, declared {{eco_declared_share_lo:.0%}}–{{eco_declared_share_hi:.0%}}, untaxed income US$ {{eco_tax_musd_lo:,.0f}}–{{eco_tax_musd_hi:,.0f}} M, social cost US$ {{eco_social_busd_calc_lo:,.1f}}–{{eco_social_busd_calc_hi:,.1f}} bn (calculator) or {{eco_social_busd_pdf_lo:,.0f}}–{{eco_social_busd_pdf_hi:,.0f}} bn (report), enforcement US$ {{eco_spend_musd:,.1f}} M. [[P]]

**Code:** `code/v2_economics.py`; sources and quotes in `docs/walkthrough/notes/economics_sources.md`.

@part Brazil and prediction

## Brazil | Staggered operations, same pixel accounting

**Question:** do territories fall after *their own* operation?

- **Data:** MapBiomas Brazil Collection 11 rasters read per territory, same net = new + re-mined − stopped accounting. Check: Kayapó 2025 {{chk_kayapo_2025_ours}} vs {{chk_kayapo_2025_pub}} ha.
- **Model:** territory + year effects on net additions (and parts), treated from each territory's first *verified* operation in 2021–25 (rule R*); Gardner's two-stage estimator; an event study for the leads.
- **Pool:** {{brv2_n_units:.0f}} territories with Collection 11 mining in 2014–18; {{brv2_n_treated:.0f}} treated, {{brv2_never_n:.0f}} never treated ({{brv2_never_n_unsearched:.0f}} never searched).
- **Why it can't decide:** the treated territories boomed before their operations, so the leads are not flat and parallel trends fail; the estimate changes sign across dating rules and samples. We report no p-value as a test of the operations.
- **Wording (review card 12):** mining boomed for years and fell after 2022; operations arrived at the peak; Munduruku was already falling before its operation; our data cannot separate the operations from the end of the boom. [[D]]

**Code:** `code/brazil_raster.py`, `brazil_v2.py`, `brazil_stagger.py` (AMW), `brazil_deter_all.py`.

## Risk map | A prediction, tested out of sample

- **Model:** logit on 1-km cells for more than 1 ha of new land (first-time mining). Features: distance to the highway and rivers, north side, gold-bearing share, mined share, mining within ~3 km, zone.
- **Validation:** trained on 2018 → 2019–21, tested on 2021 → 2022–25 in held-out 10-km blocks, against a "mining nearby" benchmark. AUC {{risk_auc_spatial_holdout:.2f}} vs {{risk_auc_benchmark:.2f}}. [[P]]
- **Use and limits:** applied to 2025 → 2026–28. Reserves score low by construction (almost no mining in training), and river access by boat is not in the model, so it misses river-borne incursions into the reserve.

**Code:** `code/v2_extra.py` (E4).

@part Review

## Review fixes | What the v3 definitions changed

- **One outcome:** every module now reports net additions, with the three parts where the estimator is linear; first-time mining appears only as a named part or where a measure cannot be net (depth, legality grade, AMW, GLAD).
- **One registry:** official buffer zones whole (Kotsimba inside the Tambopata buffer zone); the statistics workbook only for reconciliation.
- **One treatment:** Mercurio, Feb 2019; reference 2018; later events context; later years with and without 2023.
- **Inference wording:** raw ranks next to scaled ranks and pre-year ranks; cell p-values out of headlines; both pre-trend lead windows; "year effects absorb the gold price and COVID" withdrawn; K-model "keeps 97%" withdrawn.
- **Twins and Brazil:** one dating rule (R*); twins with and without Munduruku; Brazil in card-12 wording.
- **Stopped land:** split by destination and by return within two years; destination shares of 2022–25 not compared with earlier periods.

:::more Where to find the rest
- **Plan:** `docs/PLAN_v3.md`. **Review cards:** `docs/methods/` (00–14; synthesis in 14).
- **Decisions:** `docs/walkthrough/LOG.md` (D29 on for v3).
- **Qualitative sources:** `docs/walkthrough/notes/qualitative_background.md` (each with link and quote) and the papers in `literature_v2.md`.
- **Code map and every number:** the {{WALK_LINK}}, chapters Files and Appendix.
:::
