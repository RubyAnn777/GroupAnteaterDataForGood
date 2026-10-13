# How the analysis is built: one command, every number traceable

> One chapter per method: the question it answers, how it works, what it controls for, what it can't, and where the code lives. Version: plan v2 after the critical review (12 Oct 2026).

---

**Part: Overview**

## One command builds every number, figure and page

**`uv run python code/main.py` checks the data against the publishers, builds every measure, fits every model, draws every figure and writes every number to `output/numbers.csv`.**

<pre class="mermaid">
flowchart LR
  A[Raw files<br/>data_raw/] --> B[Checks against<br/>publisher numbers]
  B --> C[Measures<br/>new mining per area-year]
  C --> D[Comparisons<br/>DiD, event study,<br/>models, twins]
  D --> E[Figures + tables<br/>output/]
  D --> F[numbers.csv<br/>every cited number]
  F --> G[Walkthrough, methods<br/>and brief pages]
</pre>

- **Data:** satellite maps of mining (MapBiomas, Amazon Mining Watch, INPE and GLAD alerts), boundaries (parks, buffer zones, corridor, communities), and context (gold price, gold output, spending, fines).
- **Measures:** how much *new* mining appears each year, per area.
- **Comparisons:** the targeted area against areas that show what might have happened without the operation.

**Why it matters:** any number in the brief can be traced: brief → `numbers.csv` → the function that made it → the raw file → the publisher.

## Every claim says what kind of claim it is

| Label | Means | Example |
|---|---|---|
| **[description]** | what happened | "net new mining fell from 1,640 to 163 ha/yr" |
| **[prediction]** | what we expect next time | "a return within about three years" |
| **[causal]** | what caused it | used once, *conditional* on the comparison areas being a fair counterfactual |

**Why it matters:** grading puts 30% on honesty about the claim. A causal claim by accident is the main way to lose points.

---

**Part: Data and measures**

## One check per dataset, and no mixing of sources

**We never add or subtract numbers from different sources or collections.** Different products measure different things.

| Data | What it measures | Years | Used for | Check against publisher |
|---|---|---|---|---|
| **MapBiomas Peru, Collection 4** (course tables + our raster download) | Land class of every 30 m pixel each year; class 30 = mining (legal and illegal) | 1985–2025 | Main outcome, Peru | Tambopata buffer zone 2025 = 20,730 ha ✔ |
| **MapBiomas Peru rasters** | Same product, as maps, so we can use our own boundaries | 1985–2025 | All Peru zones | Raster gives 20,716 ha vs 20,730 ✔ |
| **Amazon Mining Watch (AMW)** | Gold-mining scars found by a machine-learning model, in 480 m squares | 2018–2026 | Twin search, Brazil, robustness | No published totals |
| **MapBiomas Amazonía, Collection 6** | Same idea as MapBiomas, all nine Amazon countries | 1985–2023 | Pre-2019 trend of candidate twins | Amazon mining 2023 = 0.78 Mha ✔ |
| **MapBiomas Brazil, Collections 10.1 and 11** | Mining per indigenous territory and per municipality | 1985–2025 | Brazil | Garimpo 2025 = 445,987 ha ✔ |
| **INPE DETER alerts** | Monthly alerts of new mining, Brazil | 2016–2026 | Brazil timing | 2019 total within 0.2% ✔ |
| **GLAD-L alerts** (University of Maryland) | Forest loss, each Landsat pixel dated to the day | 2017–2026 | Timing within the year | — |
| **Boundaries** | SERNANP parks and buffer zones; INGEMMET legal corridor; RAISG roads and protected areas; MapBiomas Amazonía native communities; FUNAI territories | current | Zones | — |
| **Context** | World Bank gold price; MINEM and central-bank gold output; MEF spending (PP 0128); IBAMA fines | various | Context only | Gold Aug 2026 = $4,411/oz ✔ |

**Why it matters:** the instructor will trace one number back to the publisher. Each check is logged in `output/checks.csv` and `DOWNLOAD_LOG.csv`.

## We count change, not stock, and split it into its parts

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

## One zone map on the raster grid, first match wins

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

---

**Part: Did it fall?**

## How a fake test replaces a standard error

**Question:** is the real result bigger than what "nothing happened" looks like in these data?

- **Fake place (placebo in space):** give the operation to each other unit in turn, re-run the identical analysis, rank the real result. Randomization p = rank / number of units (Abadie, Diamond & Hainmueller, 2010).
- **Fake date (placebo in time):** pretend the operation started earlier (2016) and re-run on pre-2019 data only. A real effect should vanish.
- **Fake border:** move the RD cut-off 2–4 km into one side. A real border effect shouldn't appear there.
- **Floor:** p can't go below 1 / n (with 15 zones, 0.07).
- **What a pass proves:** the result is unusual. Not that Mercurio caused it: a shock that hit only Tambopata in 2019 also passes.

**Code:** `code/placebo_explainer.py` (figure), and each estimator's own module.

## Before and after, against a neighbour

**Question:** did the targeted zone change more than a comparison zone?

- **How:** gap change = (targeted after − before) − (comparison after − before). Before = 2016–18, during = 2019–21, after = 2022–25.
- **Controls for:** anything that moved both zones equally (gold price, COVID, national policy).
- **Can't control for:** anything that hit only one zone. Spillovers into the comparison zone make the gap look bigger.
- **Result:** −1,762 ha/yr against Amarakaeri, which was itself partly treated. **[description]**

**Code:** `code/peru.py` (`describe_and_compare`).

## Year by year, against 14 zones, with fake places

**Question:** is the fall bigger than normal year-to-year noise?

`y_zt = α_z + γ_t + Σ_k β_k · [z = Tambopata] · [t = k] + ε_zt`, with 2018 left out.

- **Zone effect (α):** each zone's normal level. **Year effect (γ):** each year's shock shared by all zones (gold price, COVID). **β_k:** how far Tambopata sits from the others in year *k*, relative to 2018.
- **Fake places:** each other zone gets the "operation" in turn, with Tambopata removed from its comparison pool. Tambopata ranks 1 of 15 (p = 0.07, the smallest possible).
- **Why no error bars:** with one treated zone, standard errors are not trustworthy (Conley and Taber, 2011). The rank is the honest substitute.

**Code:** `code/peru.py` (`run_event_study`), estimated with `pyfixest`.

## Does the fall survive harder controls?

| Model | Adds | What it rules out |
|---|---|---|
| **M1** | zone + year effects | shared shocks (gold price, COVID) |
| **M2** | + each zone's pre-2019 size × log gold price | big zones reacting more to a price rise |
| **M3** | + a straight-line trend per zone | zones that were already drifting apart |
| **M4** | outcome scaled to each zone's own 2014–18 average | Tambopata's size driving the result |

- **Fake 2016 date:** each model also runs on 2011–18 data with a fake start. A trustworthy model shows a big real effect and a small fake one.
- **Result:** the 2019–21 gap is −1,454 to −1,859 ha/yr (M1–M3, rank 1 of 15). Scaled to size (M4) it ranks 3 of 7 (p = 0.43). M3's fake date (−337) has the same sign as the real effect. **[description]**

**Code:** `code/peru_models.py`. The numpy fit is checked against `pyfixest`.

## 1-km cells with clustered errors and a wild bootstrap

**Question:** does the fall hold per square kilometre, against cells that weren't displacement targets?

- **Units:** every 1-km cell in the study window (lon 70.65–69.30 W, lat 13.30–12.40 S); 14,241 cells, 2014–2025 for the DiD (baseline 2014–18), 2010–2025 for event studies.
- **Comparison cells:** outside every named zone, the legal corridor and native communities (4856 cells). Cells never mined stay in, with zeros (dropping them would select on the outcome).
- **Model:** `y_ct = a_c + g_t + Σ b_zp [zone = z][period = p]`, y = first-time mining (ha); cell and year fixed effects.
- **Errors:** clustered by 10 × 10 km blocks (161 clusters), so nearby cells can share shocks.
- **Wild cluster bootstrap:** restricted (WCR), 999 Rademacher draws over 10-km blocks, after removing cell and year effects. Needed because only 14 (La Pampa) and 10 (across the road) blocks contain the treated zones. Cached in `data_intermediate/wcb_cache_v2.csv` (delete to recompute, ~30 s).
- **Event studies:** year-by-year coefficients against the pooled 2014–18 reference, plus a joint test that the 2010–13 leads are zero.
- **Robustness:** gold-bearing land × year effects; returns to old pits as outcome; Poisson (PPML) for zeros.
- **Road gradient:** distance bands north/south of the highway × period, reference = 10–30 km south.

**Result:** La Pampa −1.21 ha per cell-year in 2019–21 (p = 0.08; bootstrap p = 0.06), pre-trends fail (p = 0.005). Corridor across the road +0.94 (p = 0.01), pre-trends pass. **[description]**

**Code:** `code/v2_stats.py`.

## COVID exposure and enforcement money

**Question:** does the 2019–21 gap survive controls for what year effects can't remove?

- **Base (K0):** model M2 on 2015–25 (spending data start in 2015).
- **K1:** + each zone's 2014–18 mean addition × 1[2020–21] (COVID exposure).
- **K2:** + Madre de Dios × ln(PP 0128 spending booked in Madre de Dios).
- **K3:** both. Inference by fake places.
- **Caveat:** money rose because of Mercurio, so K2 absorbs part of the effect itself.
- **Result:** −1,608 → −1,567 ha/yr, rank 1 of 15 throughout. **[description]**

**Code:** `code/peru_context_models.py`.

## Trend-matched weights plus a free intercept

**Question:** does a method built for few treated units agree with the model ladder?

- **How:** unit weights (≥ 0, sum 1, ridge-regularised) match the comparison zones' 2014–18 *trend* to Tambopata's; time weights pick the pre-years that best predict the post years; a free intercept absorbs the level gap (Arkhangelsky et al., 2021).
- **Check:** with equal weights it reproduces M1 exactly.
- **Result:** −1,545 ha/yr in 2019–21 (rank 1 of 15); scaled, rank 3 of 7; 2022–25 +136. **[description]**

**Code:** `code/peru_sdid.py` (own FISTA solver for the simplex weights).

## A weighted mix of zones, fitted before 2019

**Question:** can a weighted mix of other zones copy Tambopata before 2019?

- **How:** weights (≥ 0, summing to 1) on other zones so the mix tracks Tambopata in 2010–18. After 2019, the gap is the estimate.
- **Why it fails:** Tambopata added more mining than any other zone. A weighted average of small numbers can't reach a big one. It only fits after scaling each zone to its own size, and then only 6 zones remain.

**Code:** `code/peru_synth.py`.

## One real area that looks like La Pampa (Ruby's design)

**Question:** is there an existing area that looks like La Pampa but had no operation?

**Rules, applied to 1,174 areas across the Amazon:**

1. **R1** mining before 2019 (≥ 500 ha seen by AMW by 2018)
2. **R2** no operation reported 2017–25 (documented web search, every query logged)
3. **R3** outside Madre de Dios
4. **R4** lowland mining (< 500 m) of similar scale (≥ ⅕ of Tambopata); the closest match wins

- **Result:** no area passes. Relaxing R2 to "no operation in 2017–21" leaves two: **Amanã National Forest** and the **Tapajós protection area** (Brazil). Munduruku was dropped (operation in May 2021).
- **Comparison:** new mining per year as a share of each area's own 2018 mining, same product (AMW) for both. Pre-2019 trends come from each area's own MapBiomas collection, side by side, never subtracted.
- **Pre-trend test:** yearly log-growth difference (Tambopata minus twin), 2010–18, on a constant and a trend, Newey-West errors. No significance test for the gap (three years per area).

**Code:** `code/control_amw.py`, `control_elevation.py`, `control_mb_amazonia.py`, `control_select.py`, `control_top3.py`.

## Seven ways to let an algorithm pick the twin

**Question:** do formal matching estimators agree with Ruby's hand-set rules?

- **Pool:** 20 areas with no operation in 2017–21, ≥ 100 ha of mining by 2018, outside Madre de Dios (108 areas with AMW data).
- **Propensity score:** logit of "operation 2017–21" on log 2018 stock, median elevation of the mining, log area, country and type; 43 areas with known status.
- **Estimators:** propensity nearest 1 and 5; Mahalanobis nearest 1 and 3; coarsened exact matching; entropy balancing; inverse-probability weighting.
- **Outcome:** new mining per year as % of the 2018 stock (same as the twin). Inference by placebo in space.
- **Limit:** with one treated unit, matching is a distance rule. Tambopata's score (0.85) is above every pool area (0.76): no common support.
- **Result:** gaps −14.8 to −6.7 pp; placebo p 0.19–0.57. **[description]**

**Code:** `code/control_psm.py`.

---

**Part: Where did it go?**

## Stream, Sankey, corridor share and legality

- **Stream chart:** land mined for the first time, per zone and year. First-time mining ignores year-to-year map flicker.
- **Sankey:** per period, new mining split into new land vs old pits, flowing into zones. Flows are pixels, not people.
- **Corridor share:** first-time mined land inside the legal corridor, as a share of Madre de Dios.
- **Legality:** every pixel of first-time mining crossed with MAAP #235's legality layer (Low / Medium / High / Very high). Time-consistent version: a concession counts only if filed by the mining year.
- **Second product:** Amazon Mining Watch on the same zones. It flags a 480 m square only once, so it misses infill.

**Code:** `code/raster_layers.py`, `code/v2_legality.py`, `code/v2_extra.py`, `code/v2_products_check.py`.

## A difference in discontinuities at two borders

**Question:** did land just across a legal line change differently after 2019?

- **Borders:** the Interoceanic Highway in La Pampa's longitudes (south = La Pampa sector, north = corridor) and the Tambopata reserve edge (where outside is buffer zone). No new polygons: signed distances from the existing road line and the SERNANP reserve polygon.
- **Units:** 250-m distance bins × 2-km segments. Outcome: first-time mined land, % of the unit per year.
- **Estimator:** `rdrobust`, local linear, triangular kernel, MSE-optimal bandwidth, robust bias-corrected CI, clustered by segment. Main estimate on the change (2019–21 mean minus 2014–18 mean), so fixed border effects (the road's access, the river) cancel (Grembi, Nannicini & Troiano, 2016).
- **Checks:** fixed bandwidths 1–5 km; 500-m donut; fake start years; fake borders ±2–4 km.
- **Limit:** displacement across the border breaks the no-spillover assumption, so the road estimate is the swing (deterrence + displacement), an upper bound on either side.
- **Result:** road +2.10 pts (p = 0.08; donut +3.29, p = 0.04); reserve edge +0.15 (p = 0.77). **[description]**

**Code:** `code/v2_rdd.py`.

## Fake start dates and depth into the corridor

- **Fake start dates (T1):** the north share's change, 3 years after minus 3 years before, for every start year 2008–2022. Only start years whose windows don't overlap the event count. Randomization p = rank of the real 2019 shift / number of start years: rank 1 of 8 (p = 0.12).
- **Depth (T9):** mean distance north of the highway of first-time mining per year; OLS on a trend and a post-2019 dummy with Newey-West errors (18 years). Break −8.8 km (p = 0.000).
- **Boundary sensitivity (T4):** narrow and wide La Pampa windows give the same picture.

**Code:** `code/v2_tests.py`.

---

**Part: When and why?**

## Quarterly alerts, gold left, money and the earlier wave

- **Quarterly timing:** GLAD-L alerts on land MapBiomas maps as mining. Compare the same quarter across years (clouds); data version break in 2021.
- **Gold left:** gold-bearing land = INGEMMET geology units (river deposits plus Madre de Dios Formation terraces). Validation: 90% of all land ever mined lies on them. Depletion = share of a zone's gold-bearing land mined by a year.
- **Enforcement money (T8):** executed PP 0128 spending booked in Madre de Dios, 2015–2025. Department level only; a lower bound.
- **Earlier wave (T3):** model M1 with Tambopata × 2012–13 on 2008–16 data. Tambopata did not fall more than other zones.
- **Declared gold:** MINEM yearly files split into producer-declared gold and the artisanal estimate (until 2019); checked against the central bank for 2012 and 2019.

**Code:** `code/glad_alerts.py`, `code/raster_gold.py`, `code/v2_tests.py`, `code/peru_gold_minem.py`.

## Cited parameters times our hectares, as ranges

**Question:** what is the mining worth, what does it cost, and what is spent against it? *Informed speculation.*

- **Chain:** hectares worked (first-time mining, low; + returns to old pits, high) × 1.7–1.9 kg gold per ha (CSF, 2023) × mean gold price → value. Declared share = MINEM producer-declared gold / that gold.
- **Taxes:** 0% royalty for small producers (Ley 28258); income tax 29.5% × 11–37% margin on undeclared value.
- **Costs:** 2.4–2.8 kg mercury per kg gold; social cost US$ 81,000–1.8 M per kg (CSF). Enforcement: PP 0128 Madre de Dios spending at 3.3–3.9 soles per US$.
- **Cross-check:** MINEM's 2016–18 estimate implies 1.9 kg per hectare we mapped.
- **Result (2022–25, per year):** gold 19–32 t, declared 4%–7%, untaxed income US$ 45–252 M, enforcement US$ 1.7–2.0 M. **[prediction]**

**Code:** `code/v2_economics.py`; sources and quotes in `docs/overnight/notes/economics_sources.md`.

---

**Part: Brazil and prediction**

## Staggered operations, same pixel method

**Question:** do territories fall after *their own* operation?

- **Data:** MapBiomas Brazil Collection 11 rasters read remotely per territory (24 territories + Yanomami rings). Check: Kayapó 2024/2025 vs the platform.
- **Model:** territory + year effects, treated from each territory's own first operation; Gardner's two-stage estimator (`did2s`); randomization inference (2,000 shuffles of operation dates across territories).
- **Logic:** if operations cause falls, each territory should fall after its own date, not before.
- **Result:** +0.54 log points (p = 0.17; randomization p = 0.92). Wrong sign, not significant. **[description]**

**Code:** `code/brazil_raster.py`, `brazil_v2.py`, `brazil_stagger.py` (AMW), `brazil_deter_all.py`.

## A prediction, tested out of sample

- **Model:** logit on 1-km cells. Features: distance to highway and rivers, north side, gold-bearing share, mined share, mining within ~3 km, zone.
- **Validation:** trained on 2018 → 2019–21, tested on 2021 → 2022–25 in held-out 10-km blocks, against a "mining nearby" benchmark. AUC 0.92 vs 0.91. **[prediction]**
- **Use:** applied to 2025 → 2026–28. It misses river-borne incursions into the reserve.

**Code:** `code/v2_extra.py` (E4).

---

**Part: Review**

## What a critical referee found, and what changed

- **Fake places:** Tambopata removed from each placebo's comparison pool (before, its own fall made every placebo positive). Amazon-only pool added.
- **Causal number:** reworded to net mining; first-time mining reported alongside.
- **Cell panel:** clean comparison cells, 2014–18 baseline, pooled reference in event studies, wild cluster bootstrap.
- **Twins:** Munduruku dropped; no p-values on three annual values.
- **Brazil:** first operation inside 2021–25 (Kayapó 2024-09; Munduruku 2021-05).
- **Legality:** a concession counts only if filed by the mining year.
- **Risk map:** spatial hold-out and benchmark.
- **Gold proxy:** lift reported (share of mining vs share of land).
- **Untraceable numbers** (Sentinel-2, producer-declared gold) now computed in code.

<details><summary>Go deeper: Where to find the rest</summary>

- **Full review:** `docs/overnight/notes/critical_review_v2.md`.
- **Plan and decisions:** `docs/PLAN_v2.md`, `docs/overnight/LOG.md`.
- **Qualitative sources:** `docs/overnight/notes/qualitative_background.md` (each with link and quote) and 30 papers in `literature_v2.md`.
- **Code map and every number:** the [EXPLAINER.html](EXPLAINER.html), chapters Files and Appendix.

</details>

---
*Built 2026-10-13 11:39 from git commit f67219d (working tree may contain uncommitted changes). Numbers from output/numbers.csv (1399 rows).*
