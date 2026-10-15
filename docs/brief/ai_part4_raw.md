# Brief part 4: required AI prompt and RAW answer (unedited)

- Tool: Claude Code CLI 2.1.300 (Anthropic, account default model), non-interactive `claude -p`, all tools disabled, run in an empty folder outside the repository, so it had no project files; run 2026-10-15T16:58Z. Replaces the 2026-10-11 run (archived in docs/archive/), whose prompt called Amarakaeri untreated and used the old outcome wording.
- The prompt is the course's required prompt with our units, years, outcome and comparison filled in.

## Prompt (as sent)

Here is my comparison: Units: the buffer zone of the Tambopata National Reserve in Madre de Dios, Peru, where the government enforcement operation "Operación Mercurio" against illegal gold mining started in February 2019, versus the buffer zone of the Amarakaeri Communal Reserve, a nearby zone with mining that was less treated (a follow-up operation in 2019 also covered it), plus 13 other Peruvian buffer zones with mining as additional comparisons. Years: 2014–2025. Outcome: net mining additions per year in hectares, i.e. the annual change in area classified as mining in MapBiomas Peru Collection 4 satellite land-cover maps, which equals land mined for the first time plus old mining land mined again minus mining land that left the mining class. Comparison: the change in mean annual net additions from 2016–18 (before) to 2019–21 (during the operation and its follow-ups) in Tambopata minus the same change in Amarakaeri (difference-in-differences: −1,761 ha/yr), and the same with zone and year fixed effects across all 15 zones. List the reasons this comparison could mislead, distinguishing omitted variables, reverse causation, selection of units, and measurement error in the outcome. For each, say what data or design would fix it.

## Raw answer

# Why the Tambopata vs. Amarakaeri DiD (−1,761 ha/yr) could mislead

The −1,761 ha/yr estimate rests on one treated unit, a control that was partly treated, and an outcome built by subtracting one classified map from another. Below, each problem is listed with the data or design that would fix it.

---

## 1. Omitted variables (things that changed differently in the two zones around 2019)

| Problem | Why it biases the estimate | Fix |
|---|---|---|
| **Running out of minable land in La Pampa.** By 2018 much of the accessible gravel along the Interoceanic Highway (km 98–115) was already mined. | Net additions would have fallen anyway as land ran out. The DiD would then credit the operation with a decline caused by exhaustion. | Use "remaining minable area" as the outcome's denominator, built from alluvial-terrace and soil maps or the pre-2014 forest edge. Model additions as a hazard rate on unmined but minable pixels, not raw hectares. |
| **Different legal regimes.** Parts of the Amarakaeri buffer overlap the mining corridor and formalization areas (e.g. Huepetuhe), while La Pampa is outside the corridor and illegal. REINFO and formalization deadlines (2016–2019 decrees) affected the two zones differently. | The control's trend reflects formalization policy, not only the absence of enforcement. | Add pixel or area shares inside the corridor, mining concessions (INGEMMET cadastre) and REINFO registrations as covariates or strata. Compare like with like, e.g. only non-concession land in both zones. |
| **Gold price × exposure.** The gold price rose sharply in 2019–2020. Year fixed effects absorb the common shock but not differences in how strongly each zone responds. | Alluvial zones with cheap access respond more to price. That differential response gets loaded onto the treatment. | Interact the gold price with pre-period mining intensity, deposit type and road distance. Check for any differential price response in the 2014–18 data. |
| **COVID-19 (2020–21), which falls inside the "during" window.** Patrols were cut back, migrant labour moved, and supply chains broke. | These shocks hit Madre de Dios zones unevenly, and the "during" window is half pandemic years. | Report 2019 alone as the cleanest single post-period year, and 2020–21 separately. Use an event study rather than a pooled 3-year mean. Add data on enforcement presence, such as checkpoint or base locations and interdiction counts from Ministerio del Interior/FEMA. |
| **Hydrology and climate.** River levels, floods and El Niño years change both mining feasibility and how rivers look in satellite images. | Shocks specific to each zone and year are not absorbed by year fixed effects. | Add basin-level precipitation and river-gauge controls (CHIRPS, SENAMHI). |
| **Earlier interventions** (2014–2015 interdictions and the state of emergency in Madre de Dios). | Effects of these may still be playing out in the 2016–18 baseline. | Show the full 2014–2025 event study, and run a placebo "treatment" in 2015–16. |
| **Road and infrastructure changes**, such as Interoceanic access roads and new trails. | These change accessibility in one zone only. | Use time-varying distance-to-road from OSM history or MapBiomas urban/infrastructure classes. |

---

## 2. Reverse causation (the outcome drove the treatment)

- **Operation targeted the surge.** Operación Mercurio was launched *because* La Pampa's expansion peaked in 2016–18. Picking the treated unit at its peak creates mean reversion (an Ashenfelter-type dip in reverse). The 2016–18 baseline is exactly the abnormal period, so part of the post-2019 drop would have happened anyway.
  - **Fix:** Show pre-trends from 2014 in an event study. Use a baseline that excludes the peak years, or model the trend explicitly. Use synthetic control matched on the whole 2014–18 trajectory, not just levels. Find timing variation that is plausibly unrelated to mining, such as the national political decision under the Vizcarra government or the Supreme Decree date. Use that as an instrument or in a timing-based design.
- **Follow-up operations responded to displacement.** Later 2019 operations, such as the Plan Restauración extensions, moved into areas including Amarakaeri because miners showed up there. So the control's treatment status depends on its own outcome.
  - **Fix:** Code treatment as a time-varying dose from operation logs (base locations, patrol and interdiction counts by zone and month). Lag the dose so that this year's mining cannot cause this year's enforcement.
- **Within-zone targeting.** Patrols go where mining is visible, so enforcement intensity tracks the outcome.
  - **Fix:** Use a distance-to-base design, comparing pixels just inside vs. just outside patrol radii. Treat base locations as fixed before 2019.

---

## 3. Selection of units (who counts as treated and who counts as control)

- **The control is contaminated in two opposite ways.**
  - Amarakaeri was partly treated, which pushes the DiD toward zero.
  - Miners displaced from La Pampa may have moved into Amarakaeri and other zones, which inflates control additions and pushes the DiD away from zero (a SUTVA violation).

  The sign of the net bias is unknown, and the "effect" may be partly relocation rather than reduction.
  - **Fix:**
    - Estimate spillovers directly with rings at increasing distance from La Pampa, or with distance-decay terms.
    - Use far-away buffer zones (outside Madre de Dios) as clean controls.
    - Report a regional total (treated plus neighbours) to get the net effect on mining overall.
    - Track where miners went using worker-movement or REINFO address data where available.
- **Only one treated unit.** Clustered standard errors with a single treated cluster are not valid, so the −1,761 ha/yr has no credible standard error as it stands.
  - **Fix:** Use randomization or permutation inference, assigning placebo treatment to each of the 14 other zones. Use synthetic control placebo tests, Conley–Taber style inference, or wild cluster bootstrap with few treated units.
- **Zones are not comparable in hectares.** The 13 other zones differ hugely in size, deposit type (alluvial in Madre de Dios vs. hard-rock or Andean elsewhere) and baseline mining. Parallel trends in *hectares* is implausible across zones whose levels differ by orders of magnitude, and the large treated zone mechanically produces large absolute changes.
  - **Fix:** Normalize the outcome, e.g. additions as a share of minable area or of the existing mining stock, or use logs. Restrict to alluvial-gold zones, or weight controls via synthetic control.
- **Choosing zones "with mining".** If the inclusion threshold is based on outcomes, including post-2019 outcomes, it is selection on the dependent variable.
  - **Fix:** Define the sample using pre-2016 data only.
- **TWFE with staggered or partial treatment.** If other zones got follow-up operations at different times, two-way fixed effects uses already-treated zones as controls, which biases the estimate (Goodman-Bacon).
  - **Fix:** Use Callaway–Sant'Anna, Sun–Abraham or de Chaisemartin–D'Haultfœuille estimators with "never treated" or "not yet treated" controls.
- **Arbitrary units and windows.** Mining at La Pampa straddles the buffer-zone boundary, and 2016–18 vs. 2019–21 is one of many possible window choices.
  - **Fix:** Use pixel or grid-cell analysis with alternative boundaries (e.g. 5/10/20 km from the operation). Show a specification curve across window choices.

---

## 4. Measurement error in the outcome (MapBiomas mining class)

- **The difference of two noisy maps is noisier than either.** Net additions is the difference between two annual classifications, so the errors of both years add up. The errors are also not random:
  - They scale with mining extent, so the treated zone has the largest absolute errors.
  - They depend on how accurate the classifier is in each region.
  - **Fix:** Get per-zone, per-year accuracy assessments from MapBiomas validation points, or hand-label a stratified sample. Use estimators that correct for misclassification (Olofsson-style area adjustment).
- **Temporal filtering smears the timing.** MapBiomas applies temporal filters that use the neighbouring years. The 2018 and 2019 maps borrow information from each other, which blurs a February 2019 break. The first and last years (2014, 2024–25) are less reliable because the filter has fewer neighbouring years at the ends of the series.
  - **Fix:** Use the unfiltered or raw classifications if available. Validate the break with an independent sensor time series.
- **Net additions mixes three different processes:** new mining, remining and exits. Enforcement could:
  - push miners onto already-degraded land (remining), which does not add area;
  - change how fast abandoned pits revegetate or get reclassified as water or bare soil.

  Net additions could therefore fall while mining activity stays the same, or exits could rise without any real change.
  - **Fix:** Use the MapBiomas transition matrices to analyse gross forest→mining conversion separately from mining→other exits. Add intensity measures, such as NDVI or turbidity in active pits, or nighttime-light and pond-water dynamics.
- **Activity the maps cannot see.** At 30 m Landsat resolution, small or scattered pits are missed, and river dredges (*balsas*) are classified as water. If enforcement moved miners onto rivers or into smaller operations, measured mining falls without real mining falling.
  - **Fix:** Use higher-resolution data: Sentinel-2 (10 m, from 2016), Planet NICFI monthly mosaics (from late 2020), and dredge-detection datasets (e.g. Amazon Mining Watch, CINCIA, MAAP/ACCA). Add non-satellite outcomes: river turbidity, mercury imports or seizures, SUNAT gold exports, and mercury levels in fish or people.
- **Cloud cover and composite quality vary by year and zone.** Madre de Dios is very cloudy, so the number of usable observations per year differs.
  - **Fix:** Use the count of valid observations per pixel and year as a control, or drop low-quality pixel-years.
- **Training samples may be concentrated in famous hotspots.** If so, the classifier is more accurate in Tambopata than in controls, so the measurement errors differ between treated and controls.
  - **Fix:** Validate accuracy separately in each zone, and compare with other mining maps (RAISG, Amazon Mining Watch).

---

## Bottom line

The most serious problems are:
1. The treated unit was selected *because* of its 2016–18 peak (mean reversion).
2. The exhaustion of minable land in La Pampa.
3. Displacement into the control zones.
4. A single treated unit with no valid inference.

A pixel- or grid-level event study would address most of this. It should use:
- an outcome normalized by remaining minable area;
- a dose built from enforcement logs;
- distance-based spillover rings;
- synthetic control or permutation inference;
- validation against higher-resolution imagery and dredge data.
