# How the analysis is built: one outcome, one zone map, one treatment

> One chapter per method: the question it answers, how it works, what it controls for, what it can't, and where the code lives. Version: plan v3 (15 Oct 2026). Every number comes from `output/numbers.csv`.

---

**Part: Overview**

## One command builds every number, figure and page

**`uv run python code/main.py` checks the data against the publishers, builds the zone registry and the pixel accounting, fits every model, draws every figure and writes every number to `output/numbers.csv`.**

**Raw files** (data_raw/) → **Checks** (against publisher numbers) → **Measure** (net additions = new + re-mined − stopped) → **Models** (DiD, event study, twins) → **Figures** (and tables in output/) → **numbers.csv** (every cited number) → **Pages** (walk-through, methods, brief)

- **Data:** MapBiomas Peru Collection 4 annual maps (the outcome); other products as checks only (Amazon Mining Watch, GLAD alerts, MapBiomas Amazonía and Brazil); boundaries (SERNANP, INGEMMET corridor, RAISG roads, native communities, FUNAI); context (gold price, gold output, spending, fines).
- **One outcome:** net mining additions per zone and year, split into new land, re-mined and stopped.
- **Comparisons:** the targeted zone against zones and areas that might show what would have happened without the operation.

**Why it matters:** any number in the brief can be traced: brief → `numbers.csv` (id, value, unit, measure, zone, period, description) → the function that made it → the raw file → the publisher.

## Every claim says what kind of claim it is

| Label | Means | Example |
|---|---|---|
| **[description]** | what happened | "net additions in the Tambopata buffer zone fell from 1,640 to 163 ha/yr (2016–18 vs 2019–21)" |
| **[prediction]** | what we expect next time | "new pits in a ring around the next operation" |
| **[causal]** | what caused it | used once, *conditional* on the other Peruvian buffer zones being a fair counterfactual (the brief's sentence) |

**Why it matters:** grading puts 30% on honesty about the claim. A causal claim by accident is the main way to lose points.

---

**Part: Data and definitions**

## One check per dataset, and no mixing of sources

**We never add or subtract numbers from different sources or collections.** Different products measure different things.

| Data | What it measures | Years | Used for | Check against publisher |
|---|---|---|---|---|
| **MapBiomas Peru, Collection 4 rasters** | Land class of every 30-m pixel each year; class 4.2 Minería = all mining (legal and illegal) | 1985–2025 | **The outcome**, every Peru zone | Tambopata buffer zone 2025: 20,730 vs 20,730 ha; reserve 776.7 vs 777; Madre de Dios 112,611 vs 112,622 |
| **MapBiomas Peru statistics workbook** (course tables) | Mining per buffer zone, department | 1985–2025 | Reproduction and reconciliation checks only | Card numbers reproduce in `checks.py` |
| **Amazon Mining Watch (AMW)** | Gold-mining scars found by a model, 480-m squares; no "stopped" state | 2018–2026 | Twins, matching, a second product for displacement | No published totals |
| **GLAD-L alerts** (University of Maryland) | Forest loss, each Landsat pixel dated to the day | 2017–2026 | Timing within the year | — |
| **MapBiomas Amazonía, Collection 6** | Mining stock, nine Amazon countries | 1985–2023 | Pre-2019 paths of the twins | Amazon mining 2023: 775,746 vs 780,000 ha |
| **MapBiomas Brazil, Collection 11** (rasters and statistics) | Mining per territory | 1985–2025 | Brazil (backup) | Indigenous lands 2025: 39,915 vs 39,915 ha; Kayapó 18,569 vs 18,573 |
| **INPE DETER alerts** | Monthly alerts of new mining, Brazil | 2016–2026 | Brazil timing | 2019: 105.64 vs 105.40 km² |
| **Boundaries** | SERNANP parks and buffer zones; INGEMMET legal corridor (D.L. 1100); RAISG roads and protected areas; native communities; FUNAI territories | current | Zones | — |
| **Context** | World Bank gold price; MINEM and central-bank gold output; MEF spending (PP 0128); IBAMA fines | various | Context only | Gold Aug 2026 4,411 vs 4,411 $/oz; MINEM vs BCRP 2019 7,103 vs 7,073 kg; PP 0128 2019 31,120,611 vs 31,120,611 soles |

**Why it matters:** the instructor will trace one number back to the publisher. Each check is logged in `output/checks.csv` and `DOWNLOAD_LOG.csv`.

## Net mining additions, split into three parts

**Total mining area only grows, like the gold price, so totals correlate with almost anything. We count the yearly change, and we split it.**

`net additions(t) = mining(t) − mining(t−1) = new land + re-mined − stopped`, per zone, ha/yr, checked in code for every zone and year.

| Part | A pixel that is… | Tells us |
|---|---|---|
| **New land** (first-time mining) | mining now, never mining in any earlier year since 1985 | expansion into forest or new ground |
| **Re-mined** | mining now, not last year, but mining in some year before | old pits worked again |
| **Stopped** | mining last year, not now | the pit left the mining class: flooded, regrowing, bare, or reclassified |

- **Stopped, split further** (no image check; plan v3 V3-5): what the land becomes the next year (water, forest, bare ground, other) and whether it is mining again within two years. The water share collapses in 2023–25 in every zone, an end-of-series effect of the map, so later-years shares are not compared with earlier ones.
- **Linear estimators** (DiD, two-way fixed effects, event studies, RD at a fixed bandwidth) give the four estimates that add up: net = new + re-mined − stopped. **Non-linear ones** (ratios, logs, Poisson, weights fitted on net) say so next to the number.
- **The stopped share of a fall** is counted four ways: the raw change in stopped land; without land mined again within two years; only stopping above the zone's 2016–18 rate; and relative to Amarakaeri. For the Tambopata buffer zone, 2016–18 to 2019–21, it runs 25%–47%. **[description]**
- **Other products cannot give net additions:** AMW and GLAD have no "stopped" state. They appear only as checks of timing and of the twins, labelled with their own measure.

**Can't see:** river dredges, mercury, who mines, and whether a site is legal. Satellites see bare ground and ponds.

**Code:** `code/definitions.py` (OUTCOME), `code/raster_zones.py`.

## One registry on the raster grid, official boundaries whole

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

## One start date; everything after it is context

- **The treatment:** the start of Operation Mercurio, February 2019, in the Tambopata buffer zone (La Pampa). Because addition(2019) = map 2019 − map 2018, **2019 is the first treated year and 2018 the reference year**.
- **Context, not separate treatments:** COVID-19 (2020), Plan Restauración (2021), Mercurio II (all of Madre de Dios), the April 2023 state of emergency, the 2025 navy withdrawal. Shown as dashed lines at Y − 0.5; not estimated.
- **Periods:** 2016–18 (before, the course card), 2014–18 (pooled reference for models), 2019–21 ("Mercurio and what followed"), 2022–25 ("later years", always also without 2023, a MapBiomas-only spike year). Never "after enforcement ended".
- **So every estimate measures "Mercurio together with what followed"**, never Mercurio alone.

**Code:** `code/definitions.py` (TREATMENT, PERIODS).

---

**Part: Did it fall?**

## How a fake test replaces a standard error

**Question:** is the real result bigger than what "nothing happened" looks like in these data?

- **Fake place (placebo in space):** give the operation to each other zone in turn (Tambopata removed from the pool), re-run the identical analysis, rank the real result. p = rank / number of zones (Abadie, Diamond & Hainmueller, 2010).
- **Raw vs scaled:** in hectares the biggest zone tends to rank first: the Tambopata buffer zone ranks 1 in 2014, 1 in 2015 and 1 in 2016, before Mercurio. So we always give the scaled rank (coefficient / the zone's own 2014–18 mean, zones above 10 ha/yr) next to the raw rank.
- **Fake date (placebo in time):** pretend the operation started in 2016 and re-run on pre-2019 data only. A real effect should vanish.
- **Fake border:** move the RD cut-off 2–4 km into one side.
- **Floor:** p can't go below 1 / n (with 15 zones, 0.07).
- **What a pass proves:** the result is unusual. Not that Mercurio caused it: a shock that hit only the target in 2019–21 also passes.

**Code:** `code/placebo_explainer.py` (figure), and each estimator's own module.

## Before and after, against a neighbour

**Question:** did the targeted zone change more than the less-treated neighbour?

- **How:** gap = (Tambopata after − before) − (Amarakaeri after − before), for net additions and each part. Before = 2016–18 (also 2014–18), during = 2019–21, later = 2022–25.
- **Controls for:** anything that moved both zones equally.
- **Can't control for:** anything that hit only one zone. Spillovers into Amarakaeri make the gap look bigger; Mercurio II in Amarakaeri makes it look smaller.
- **Result:** −1,762 ha/yr (2016–18 base), −1,663 (2014–18 base); fake start 2016 +209. **[description]**

**Code:** `code/peru.py`, `code/peru_robust.py` (other comparison zones).

## Year by year, against 14 zones

**Question:** how far does the target sit from the comparison zones each year?

`y_zt = α_z + γ_t + Σ_k β_k · [z = Tambopata] · [t = k] + ε_zt`, net additions (and each part), 2018 left out.

- **Zone effect (α):** each zone's normal level. **Year effect (γ):** each year's shock *common to all zones*. It does not remove shocks that hit zones unequally (gold price, COVID). **β_k:** how far Tambopata sits from the others in year *k*, relative to 2018.
- **Pooled reference:** the mean of 2019–21 minus the mean of 2014–18 is −1,453 ha/yr, equal to M1.
- **Why no error bars:** with one treated zone, standard errors are not informative (Conley and Taber, 2011). Ranks are the honest substitute: raw 1 of 15, scaled 6 of 7.

**Code:** `code/peru.py`, estimated with `pyfixest`.

## Does the fall survive harder controls?

| Model | Adds | What it targets |
|---|---|---|
| **M1** | zone + year effects, pooled 2014–18 reference | shocks common to all zones |
| **M2** | + each zone's 2014–18 mean × log gold price | big zones reacting more to a price rise |
| **M3** | + a straight-line trend per zone | zones that were already drifting apart |
| **M4** | outcome scaled to each zone's own 2014–18 mean | Tambopata's size driving the result |

- **Fake 2016 date:** each model also runs on 2011–18 with a fake start. A trustworthy model shows a big real effect and a small fake one.
- **Result (net additions, 2019–21):** −1,453 (M1), −1,605 (M2), −1,859 (M3) ha/yr, raw rank 1 of 15; scaled ranks 4, 3, 4 of 7; M4 rank 3 of 7. M3's fake date (−337) has the same sign as the real effect. M1's parts: new −945, re-mined +251, stopped +759. **[description]**
- **The brief's range** uses M1 and the 2×2 on the 2014–18 baseline (1,453–1,663 ha/yr): pooled baseline, no extrapolated slope (review card 14, D-S14-3).

**Code:** `code/peru_models.py`. The numpy fit is checked against `pyfixest`.

## 1-km cells, clustered errors, a wild bootstrap

**Question:** does the fall hold per square kilometre?

- **Units:** every 1-km cell in the study window; 14,249 cells, 2014–2025 (reference 2014–18); event studies from 2011 (sensitivity from 2010). Majority registry zone per cell.
- **Comparison cells:** other protected areas, other buffer zones and the rest of Madre de Dios with tenure "none" (4,854 cells). They hold almost no mining (24 had any by 2018), so **each coefficient is close to the zone's own before/after** and its p-value overstates. Keep cell p-values out of headlines.
- **Model:** `y_ct = a_c + g_t + Σ b_zp [zone = z][period = p]`, y = net additions (ha), and each part.
- **Errors:** clustered by 10 × 10 km blocks (161 clusters); wild cluster bootstrap (restricted, 999 Rademacher draws) because only 16 (La Pampa) and 10 (across the road) blocks contain the treated zones.
- **Pre-trends, two lead windows:** La Pampa 2011–13 p = 0.11, 2010–13 p = 0.009; corridor across the road 2011–13 p = 0.04, 2010–13 p = 0.017. La Pampa passes only without the 2010 lead.
- **Depletion:** gold-bearing bins × year; 2018-depletion bins × year; a hazard version (new land as % of not-yet-mined land): on that basis La Pampa's cell-level change is −0.31 points (p = 0.73).
- **Road gradient:** distance bands north/south of the highway × period, reference = 10–30 km south.

**Result:** La Pampa −1.69 ha of net additions per cell-year in 2019–21 (new −1.06, re-mined +0.32, stopped +0.95); corridor across the road +0.89. Description: a before/after per cell. **[description]**

**Code:** `code/v2_stats.py` (bootstrap cache keyed by an input hash).

## COVID exposure and enforcement money

**Question:** does the 2019–21 gap survive controls for shocks that hit zones unequally?

- **Base (K0):** M2 on 2015–25 (spending data start in 2015), post years saturated.
- **K1:** + each zone's 2014–18 mean × 1[2020–21] (COVID exposure).
- **K2:** + Madre de Dios × ln(PP 0128 spending booked in Madre de Dios).
- **K3:** both. Inference by fake places.
- **Caveat:** money rose with Mercurio, so it is partly the treatment itself (a bad control).
- **Result (net additions, 2019–21):** K0 −2,569, K3 −2,216 ha/yr. The COVID term moves the gap by +142 and the money term by −53: they offset, so K3 ≈ K0 is not a robustness check. Raw rank 1 of 15, scaled 2 of 7. **[description]**

**Code:** `code/peru_context_models.py`.

## Weighted zones and pre-years, then a DiD

**Question:** does a method built for few treated units agree with the model ladder?

- **How:** unit weights (≥ 0, sum 1, ridge-regularised) chosen to make the comparison parallel to Tambopata in 2014–18; time weights pick the pre-years; a free intercept absorbs the level gap (Arkhangelsky et al., 2021).
- **Fit:** the weights explain 2% of Tambopata's pre-2019 variation; the time weight is 86% on 2014.
- **Check:** with equal weights it reproduces M1 exactly.
- **Result (net additions):** −1,544 ha/yr in 2019–21 (raw rank 1 of 15; scaled 3 of 7); −732 when fitted on 2011–18; later years +135 (−393 without 2023). Sensitivity only. **[description]**

**Code:** `code/peru_sdid.py` (own FISTA solver for the simplex weights).

## A weighted mix of zones, fitted before 2019

**Question:** can a weighted mix of other zones copy Tambopata before 2019?

- **How:** weights (≥ 0, sum 1) on other zones so the mix tracks Tambopata's net additions in 2014–18. After 2019, the gap is the estimate.
- **Why it fails:** Tambopata added more than any other zone. A weighted average of small numbers can't reach a big one: outside every donor's range in 5 of 5 fit years. With Amarakaeri as a donor, all weight goes to it, and the gap (−411 ha/yr) is just Tambopata minus Amarakaeri. Description of a misfit.

**Code:** `code/peru_synth.py`.

## One real area that looks like La Pampa (Ruby's design)

**Question:** is there an existing area that looks like La Pampa but had no operation?

**Rules, applied to 1,174 areas across the Amazon:**

1. **R1** mining before 2019 (≥ 500 ha seen by AMW by 2018)
2. **R2** no verified operation 2017–25 (documented web search; one dating rule R* for all scripts)
3. **R3** outside the registry region (Madre de Dios and the Tambopata and Amarakaeri buffer zones)
4. **R4** lowland mining (< 500 m) of similar scale (≥ ⅕ of Tambopata)

- **Result:** no area passes. Allowing verified operations after 2021 leaves 3: Amanã, Tapajós and Munduruku (Brazil); 2 if an unverified report disqualifies.
- **Measure:** AMW new area per year as a share of each area's own 2018 AMW area (comparable to new land, not to net additions). Pre-2019 paths from each area's own MapBiomas collection, side by side, never subtracted.
- **Result:** Tambopata at 16% of the twins' mean pace in 2019–21, 41% without Munduruku. **[description]**
- **Pre-2019 test:** yearly log-growth gap (Tambopata minus twin), 2010–18, on a constant and a trend, Newey-West errors. The constant = mean growth gap; the trend = whether that gap was changing (it was shrinking: Tambopata converging). Not parallel. No significance test for the 2019–21 gap (three years per area).

**Code:** `code/control_amw.py`, `control_elevation.py`, `control_mb_amazonia.py`, `control_select.py`, `control_top3.py`.

## Letting an algorithm pick the twin

**Question:** do formal matching estimators agree with Ruby's hand-set rules?

- **Pool:** 19 areas with no operation in 2017–21, ≥ 100 ha of AMW mining by 2018, outside Madre de Dios (108 areas with AMW data).
- **Propensity score:** ridge-penalised logit of "operation 2017–21" on log 2018 stock, median elevation of the mining, log area, country and type; 36 areas with known status; caliper 0.25 SD of the logit score.
- **Estimators:** propensity nearest 1 and 5 (no control within the caliper); Mahalanobis nearest 1 and 3; coarsened exact matching; entropy balancing; inverse-probability weighting.
- **Outcome:** AMW new area as % of the 2018 AMW stock (same as the twins). Inference by placebo in space.
- **Limit:** with one treated unit, matching is a distance rule. Tambopata's score (0.81) is above every pool area (0.75): no common support.
- **Result:** gaps −41.5 to −6.7 percentage points; placebo p 0.15–0.60. **[description]**

**Code:** `code/control_psm.py`.

---

**Part: Where did it go?**

## Streams, Sankey, corridor share and legality

- **Stream chart:** net additions per zone and year (zones with a net loss drawn below zero); a second stream for re-mined land.
- **Sankey:** per period, the gross inflow (new land and re-mined land) flowing into zones, with stopped land and net additions named. Flows are pixels, not people.
- **Corridor share:** the department's net additions on legal-mining-corridor land (D.L. 1100 tenure, any zone, native communities excluded) divided by all of the department's net additions, period sum / period sum, and the same for new land. Not to be confused with the *corridor across the road* (the ≤ 10-km strip north of the highway at La Pampa's longitudes).
- **Displacement bound:** the sum of the rises in net additions in the other Madre de Dios zones whose net additions rose (inside the department), divided by the Tambopata buffer zone's fall (1.8 for 2016–18 to 2019–21).
- **Legality (new land only, a per-pixel grade at first mining):** each pixel crossed with MAAP #235's legality layer (Low / Medium / High / Very high); time-consistent version counts a concession only if filed by the mining year.
- **Second product:** Amazon Mining Watch on the same zones; it flags a 480-m square only once, so it misses infill and has no net version.

**Code:** `code/raster_layers.py`, `code/v2_legality.py`, `code/v2_extra.py`, `code/v2_products_check.py`.

## A difference in discontinuities at two borders

**Question:** did land just across a legal line change differently after 2019?

- **Borders:** the Interoceanic Highway at La Pampa's longitudes (south = La Pampa sector, north = corridor across the road) and the Tambopata reserve edge (where outside is buffer zone).
- **Units:** 250-m distance bins × 2-km segments. Outcome: net additions, % of the unit's land per year; parts at a fixed bandwidth, where they add up.
- **Estimator:** `rdrobust`, local linear, triangular kernel, MSE-optimal bandwidth, robust bias-corrected CI, clustered by segment. Main estimate on the change (2019–21 mean minus 2014–18 mean), so fixed border effects cancel (Grembi, Nannicini & Troiano, 2016). Also 2019 alone, 2022–25, and perpendicular distance to the road.
- **Checks:** fixed bandwidths 1–5 km; 500-m donut; fake start years; fake borders ±2–4 km.
- **Limit:** displacement across the border breaks the no-spillover assumption, so the road estimate is the swing, an upper bound on either side.
- **Result (net additions):** road +2.17 pts (p = 0.25; across bandwidths and the donut p = 0.18–0.86; fake start years from 2008: rank 2 of 10). Reserve edge −0.23 (p = 0.63; fake start years rank 8 of 20). Uninformative on net. **[description]**

**Code:** `code/v2_rdd.py`.

## Fake start dates and depth into the corridor

- **Fake start dates (T1):** the north share's change (net additions, and new land), 3 years after minus 3 years before, for every start year 2008–2022. Clean comparison: only start years whose windows don't overlap the event. Net additions: rank 1 of 8 (p = 0.12); new land: rank 1 of 8.
- **Depth (T9, new land only):** mean distance north of the highway of new land per year (a weighted ratio, not defined for net); OLS on a trend and a post-2019 dummy with Newey-West errors (18 years). Break −8.8 km (p < 0.001).
- **Boundary sensitivity (T4):** narrow and wide La Pampa windows give the same picture.

**Code:** `code/v2_tests.py`.

---

**Part: When and why?**

## Quarterly alerts, gold left, money and the earlier wave

- **Quarterly timing (another measure):** GLAD-L alerts on land MapBiomas maps as mining by the next year (no look-ahead). Compare the same quarter across years (clouds); data version break in 2021.
- **Gold left:** gold-bearing land = INGEMMET geology units (river deposits plus Madre de Dios Formation terraces). Validation: 90% of all land ever mined lies on them. Depletion = share of a zone's gold-bearing land first mapped as mining by a year; cell terciles show local depletion.
- **Enforcement money (T8):** executed PP 0128 spending booked in Madre de Dios, 2015–2025. Department level only; a lower bound.
- **The 2012–13 check (T3):** M1-type model on 2008–16 with Tambopata × 2012–13 (net additions): +629 ha/yr, rank 14 of 14. Asner & Tupayachi (2017) report a dip on their own maps; ours show none.
- **Declared gold:** MINEM yearly files split into producer-declared gold and the artisanal estimate (until 2019); compared with the central bank every year (13 of 25 years within 2%).

**Code:** `code/glad_alerts.py`, `code/raster_gold.py`, `code/v2_tests.py`, `code/peru_gold_minem.py`.

## Cited parameters times our hectares, as ranges

**Question:** what is the mining worth, what does it cost, and what is spent against it? *Informed speculation.*

- **Chain:** new land (first-time mining; not net additions) × 1.6–1.9 kg gold per ha (CSF, 2023) × mean gold price → value. Re-mined land gets no gold (CSF has no yield for old pits), so both ends understate if old pits still pay. Declared share = MINEM producer-declared gold, 2022–25 mean / that gold.
- **Taxes:** 0% royalty for small producers (Ley 28258, Art. 5); income tax 29.5% × 11–37% margin on undeclared value.
- **Costs:** 2.4–2.8 kg mercury per kg gold; social cost per kg from two separate CSF estimates, never merged: US$ 81,000–364,000 (calculator) and US$ 1,200,000–1,800,000 (2023 report, p. 7). Enforcement: PP 0128 Madre de Dios spending, each year converted at its BCRP annual average.
- **Cross-check:** MINEM's 2016–18 gold implies 2.5 kg per hectare of new land we mapped.
- **Result (2022–25, per year):** gold 18–22 t, declared 6%–8%, untaxed income US$ 42–169 M, social cost US$ 1.5–7.9 bn (calculator) or 22–39 bn (report), enforcement US$ 1.7 M. **[prediction]**

**Code:** `code/v2_economics.py`; sources and quotes in `docs/walkthrough/notes/economics_sources.md`.

---

**Part: Brazil and prediction**

## Staggered operations, same pixel accounting

**Question:** do territories fall after *their own* operation?

- **Data:** MapBiomas Brazil Collection 11 rasters read per territory, same net = new + re-mined − stopped accounting. Check: Kayapó 2025 18,569 vs 18,573 ha.
- **Model:** territory + year effects on net additions (and parts), treated from each territory's first *verified* operation in 2021–25 (rule R*); Gardner's two-stage estimator; an event study for the leads.
- **Pool:** 9 territories with Collection 11 mining in 2014–18; 6 treated, 3 never treated (1 never searched).
- **Why it can't decide:** the treated territories boomed before their operations, so the leads are not flat and parallel trends fail; the estimate changes sign across dating rules and samples. We report no p-value as a test of the operations.
- **Wording (review card 12):** mining boomed for years and fell after 2022; operations arrived at the peak; Munduruku was already falling before its operation; our data cannot separate the operations from the end of the boom. **[description]**

**Code:** `code/brazil_raster.py`, `brazil_v2.py`, `brazil_stagger.py` (AMW), `brazil_deter_all.py`.

## A prediction, tested out of sample

- **Model:** logit on 1-km cells for more than 1 ha of new land (first-time mining). Features: distance to the highway and rivers, north side, gold-bearing share, mined share, mining within ~3 km, zone.
- **Validation:** trained on 2018 → 2019–21, tested on 2021 → 2022–25 in held-out 10-km blocks, against a "mining nearby" benchmark. AUC 0.92 vs 0.91. **[prediction]**
- **Use and limits:** applied to 2025 → 2026–28. Reserves score low by construction (almost no mining in training), and river access by boat is not in the model, so it misses river-borne incursions into the reserve.

**Code:** `code/v2_extra.py` (E4).

---

**Part: Review**

## What the v3 definitions changed

- **One outcome:** every module now reports net additions, with the three parts where the estimator is linear; first-time mining appears only as a named part or where a measure cannot be net (depth, legality grade, AMW, GLAD).
- **One registry:** official buffer zones whole (Kotsimba inside the Tambopata buffer zone); the statistics workbook only for reconciliation.
- **One treatment:** Mercurio, Feb 2019; reference 2018; later events context; later years with and without 2023.
- **Inference wording:** raw ranks next to scaled ranks and pre-year ranks; cell p-values out of headlines; both pre-trend lead windows; "year effects absorb the gold price and COVID" withdrawn; K-model "keeps 97%" withdrawn.
- **Twins and Brazil:** one dating rule (R*); twins with and without Munduruku; Brazil in card-12 wording.
- **Stopped land:** split by destination and by return within two years; destination shares of 2022–25 not compared with earlier periods.

<details><summary>Go deeper: Where to find the rest</summary>

- **Plan:** `docs/PLAN_v3.md`. **Review cards:** `docs/methods/` (00–14; synthesis in 14).
- **Decisions:** `docs/walkthrough/LOG.md` (D29 on for v3).
- **Qualitative sources:** `docs/walkthrough/notes/qualitative_background.md` (each with link and quote) and the papers in `literature_v2.md`.
- **Code map and every number:** the [EXPLAINER.html](EXPLAINER.html), chapters Files and Appendix.

</details>

---
*Built 2026-10-15 22:56 from git commit 79211f8 (working tree may contain uncommitted changes). Numbers from output/numbers.csv (2723 rows).*
