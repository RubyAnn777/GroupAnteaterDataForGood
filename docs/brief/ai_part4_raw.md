# Brief part 4: required AI prompt, RAW answer (unedited)

- Tool: Claude (Anthropic), model Sonnet, run as a sub-agent with no tool use, 2026-10-11. Caveat: the sub-agent auto-loads the repo's agent.md, so it knew project facts (e.g. MAAP dredge counts, the 74% corridor share) beyond the prompt.
- The team may prefer to re-run the prompt in its own AI tool. If so, replace this file and keep the tool name and date.

## Prompt (as sent)

Here is my comparison: Units: the buffer zone of the Tambopata National Reserve in Madre de Dios, Peru (targeted by the government enforcement operation "Operación Mercurio" against illegal gold mining from February 2019) versus the buffer zone of the Amarakaeri Communal Reserve (a nearby comparison zone with mining but no targeted operation), plus 13 other Peruvian buffer zones with mining as additional comparisons. Years: 2014–2025. Outcome: new mining area per year (annual change in hectares classified as mining in MapBiomas Peru Collection 4 satellite land-cover maps). Comparison: the change in mean annual new mining area from 2016–18 (before) to 2019–21 (during the operation) in Tambopata minus the same change in Amarakaeri (difference-in-differences: −1,762 ha/yr), and the same with zone and year fixed effects across all 15 zones. List the reasons this comparison could mislead, distinguishing omitted variables, reverse causation, selection of units, and measurement error in the outcome. For each, say what data or design would fix it.

## Raw answer

## Why this comparison could mislead

Treat the −1,762 ha/yr as **description**. It is the gap in before/after changes between two zones, not an effect of Mercurio.

### 1. Omitted variables (time-varying shocks that hit the zones differently)
- **COVID-19 (2020):** it falls inside your "during" window. It cut patrols and mobility, and it may have hit the two zones differently.
- **Gold price:** it rose through 2019-21 and again in 2023. Zones differ in how much accessible gold they hold, so a common price shock can have unequal effects. Year fixed effects absorb only the average shock.
- **Other enforcement and policy:** the pre-period was not enforcement-free (2017-18 operations). Plan Restauración (2021) and the 2023 state of emergency also add treatment waves. Amarakaeri is partly treated too (Camanti fell), so you compare more vs. less enforcement, not treated vs. untreated.
- **Fixes:**
  - Add zone-specific covariates (distance to roads and rivers, gold geology, mining concessions, legal-corridor share).
  - Add price × baseline-suitability interactions.
  - Add enforcement-intensity data (patrol or interdiction records from SERNANP/OEFA) instead of a 0/1 flag.
  - Mark the 2020, 2021 and 2023 events in every figure.

### 2. Reverse causation and anticipation
- **Selection into targeting:** Tambopata was targeted because La Pampa was the worst mining area, so mining caused enforcement. High pre-period values (1,640 ha/yr) invite mean reversion. A drop after a peak looks like an effect even without enforcement.
- **Timing:** miners may have left before February 2019 once the operation was announced or rumoured.
- **Fixes:**
  - Check pre-trends with an event study, omitting 2018. Use all pre-years from 2014 or earlier, not only three.
  - Test whether the treated zone's pre-trend differs from the comparison zones.
  - Use synthetic control or synthetic DiD, with weights fitted on pre-2019 data only.
  - Document the announcement timeline and, if possible, find the policy rule that decided where to target. Without that rule, say plainly that causation cannot be established.

### 3. Selection of units
- **One treated unit:** clustered standard errors are not informative with a single treated zone. Use placebo-in-space ranking (permute which zone is "treated") and show it.
- **Control choice:** Amarakaeri is not an independent control. Displacement from La Pampa may flow into it (its additions rose from 54 ha in 2018 to 1,086 ha in 2022). That biases the DiD away from zero. The 13 other zones are mostly far from mining and have near-zero baselines, so the zone/year FE result is driven by the Madre de Dios zones. Check that dropping the largest unit doesn't change the answer.
- **Window choice:** 2016-18 vs. 2019-21 is a researcher choice. Report the placebo (a 2016 start), alternative windows and the extension to 2025.
- **Fixes:**
  - Restrict controls to pre-2019 mining zones with comparable baselines.
  - Define comparison units by distance from La Pampa, to separate spillover from clean control.
  - Test displacement explicitly by summing Tambopata, neighbouring zones and "rest of Madre de Dios". The department total did not fall.
  - Also test inside the reserve itself, using the ANP series.

### 4. Measurement error in the outcome
- **Legality:** MapBiomas class 4.2 captures all mining (legal and illegal, artisanal and industrial). It cannot tell legal from illegal, so the 74% of 2021-24 mining deforestation inside the legal corridor is mixed in.
- **Invisible mining:** satellites cannot see river dredging (MAAP #193 counted 148 → 598 dredges in La Pampa) or mercury use. A fall in mapped land mining could be a shift to rivers.
- **Classification noise:** additions can be negative from reclassification. Re-mining of old scars counts as an addition. Collection changes can alter the series. Classification accuracy may differ by cloud cover and area.
- **Fixes:**
  - Triangulate with independent sources: MAAP deforestation polygons, Amazon Mining Watch, and declared gold production (which fell 88% from 2018 to 2025 while mapped area grew).
  - Run the analysis on 3-year rolling sums to dampen noise, and run sensitivity checks against a second classification.
  - Collect dredge counts from boat or river surveys, or radar/SAR data.
  - Never mix collections or subtract numbers from different publishers.

### What you can honestly claim
- **Description:** Tambopata's additions fell sharply relative to Amarakaeri's in 2019-21.
- **Prediction (weak):** expect a partial or full rebound once enforcement lapses. The 2022-25 data show one.
- **Causal:** not supported. One treated unit, contaminated controls, concurrent shocks, and an outcome that misses dredging.
