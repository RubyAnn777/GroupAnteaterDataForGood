# When the patrols leave: what Operation Mercurio tells FZS about enforcement against gold mining

Group Giant Anteater · Data for Good · Question 2 · October 2026 · Team: [names]

## 1. The question

**FZS pays for enforcement and needs to know what it buys.** It supports SERNANP's operations against alluvial gold mining around Tambopata and Bahuaja-Sonene (FZS, n.d.). Operations are costly and temporary, so: **what happens in the targeted area, and around it, when an operation ends?** Mining could stop (**deterrence**), move (**displacement**) or return (**delay**); inside the target these look alike, so we need comparisons.

**Case:** Operation Mercurio at La Pampa, Peru's largest illegal mining area, in the buffer zone of Tambopata National Reserve (Madre de Dios). **Treatment:** its start in February 2019 (first treated year 2019); COVID-19 (2020), Plan Restauración (2021) and the April 2023 state of emergency are context, so we measure "Mercurio and what followed". **Target:** the Tambopata buffer zone (official boundary) and its La Pampa sector (70.15–69.80 W). **Comparison:** the Amarakaeri buffer zone, only "less treated" (Mercurio II covered all of Madre de Dios; MINAM, 2021, p. 33), and 14 Peruvian buffer zones with mining. **Around it:** the legal corridor across the highway, the reserve, the department. **Periods:** 2016–18, 2019–21, 2022–25 ("later years").

## 2. Data and provenance

**One outcome everywhere: net mining additions** (ha/yr) = land mined for the first time (**new**) + old mining land mined again (**re-mined**) − mining land that left the mining class (**stopped**), counted pixel by pixel on the 30-m annual maps of **MapBiomas Peru, Collection 4** (class 4.2: all mining, legal and illegal). Checks (ours vs publisher): Tambopata buffer zone 2025 20,716 vs 20,730 ha; reserve 776 vs 777; Madre de Dios 112,537 vs 112,622. **Context:** World Bank gold price (Aug 2026 $4,411/oz vs 4,411); MINEM/BCRP gold (2019 7,103 vs 7,073 kg; an artisanal *estimate* until 2019); MEF spending, PP 0128 (2019 S/ 31,120,611 vs 31,120,611). **Cross-checks only (other measures):** Amazon Mining Watch (no publisher totals; two clips 21,108 vs 21,113 ha), MapBiomas Amazonía Col. 6 (775,746 vs 780,000 ha, 2023), MapBiomas Brazil Col. 11 (39,915 vs 39,915 ha). Files: `DOWNLOAD_LOG.csv`; numbers and figure: `code/main.py`.

## 3. Findings

![Net mining additions and their three parts: La Pampa sector and the corridor across the road (top); Madre de Dios by area (bottom)](../../output/fig_brief_main.png)

**Net mining collapsed in the target during the operation** **[description]**. The Tambopata buffer zone fell from 1,639 to 162 ha/yr (2016–18 vs 2019–21) while the less-treated Amarakaeri rose from 289 to 573: a difference of **−1,761 ha/yr**. A fake start in 2016 gives +208; every 2019–21 year (≤ 417 ha) was below every 2011–18 year (≥ 707).

**About half of that fall is pits going out of use, not fewer new pits** **[description]**. New land fell from 2,015 to 1,061 ha/yr, while stopped land rose from 720 to 1,412 (65% and 47% of the net fall). In Amarakaeri stopped land barely moved (542 → 584), so the stopping was specific to the target. In La Pampa new pits kept opening in 2019 (1,532 ha vs 1,834 in 2018) while 1,494 ha stopped; new land fell only in 2020–21, the COVID years. 50% of stopped land became water; 37% was mined again within two years (before 2019: 28%). Dethier et al. (2023), using mining ponds, independently report 70–90% abandonment in the targeted zones and faster mining just outside them.

**Mining moved across the road, and the department never fell** **[description]**. In the legal corridor across the highway net additions rose from 60 to 395 ha/yr; the corridor's share of the department's net additions rose from 42% to 80%. Madre de Dios went 3,607 → 4,636 → 12,039 ha/yr. Rises elsewhere add up to 1.8 times the target's fall: not all of it can be miners who moved.

**Therefore** **[causal]**, *if the other Peruvian buffer zones show what the Tambopata buffer zone would otherwise have done*, Mercurio and the operations that followed lowered its net mining additions by about 1,452 to 1,662 ha/yr in 2019–21 (all 14 zones, or Amarakaeri alone, 2014–18 baseline). About half is land stopping (759 of 1,452), not less new clearing; the fall is large in hectares but ordinary relative to the zone's size (rank 4 of 7; in hectares it also ranks first in 2014–16, before Mercurio). Read it as an upper bound (4b).

**It came back, on old pits; then mining entered the reserve** **[description]**. In 2022–25 the target averaged 1,828 ha/yr (1,250 without 2023, a spike only MapBiomas shows), 1,139 of it re-mined. Inside the reserve net additions were +241 ha in 2025; MAAP reports ~500 ha from late 2025 to Feb 2026, after the navy left the river posts (Pacsi et al., 2026).

## 4. What FZS can do with this

**(a) What FZS learns** **[prediction]**. From this one case: a sharp local fall while patrols are present, half of it pits being abandoned; new pits nearby and across the nearest legal boundary; a return within about three years, largely on old pits; no fall in the region. So: **fund presence, not one-off sweeps; watch a ring of a few kilometres around each operation with near-real-time forest-loss alerts** (new pits opened in 2019 while patrolled pits stopped); **hold the reserve's first kilometre and the river posts** (91% of first-time mining inside the reserve is within 1 km of its edge); and trace gold origin in the corridor (0% royalty for small producers, Ley 28258, Art. 5; 145 of 9,592 miners in formalization fully formalized, MINAM, 2021, pp. 55–56).

**(b) Why this could mislead, and which way.** *Omitted variables:* COVID-19, the gold price (×2.7 2018–25) and later waves overlap the post-period and need not hit all zones alike (probably overstates). *Reverse causation:* La Pampa was targeted at its peak; part of the fall is a return to normal (overstates). *Selection of units:* one targeted zone, far larger than any comparison: standard errors are not informative (Conley & Taber, 2011) and raw placebo ranks measure size; Amarakaeri received miners (overstates) but had its own operation (understates). *Measurement error:* net additions mix three processes; half the fall is pits leaving the mining class, and part of "stopped" is temporary or classification flicker, so **net additions can fall while activity does not** (overstates); hectares proxy for miners; the class mixes legal and illegal mining; **satellites cannot see river dredges or mercury** (MAAP counted 148 → 598 dredges in La Pampa, 2021–23; Yupanqui et al., 2023), so a shift to rivers adds no hectares (overstates). **Read the fall as an upper bound, the return as a lower bound.**

**(c) What would let us say more.** Dated patrol and interdiction records from SERNANP or FZS (intensity, not a 0/1 flag: were the stopped pits the raided ones?); an image-checked sample of stopped pits; concession and REINFO maps for legality pixel by pixel; dredge counts and mercury sampling; more operations as cases.

## References

Access dates are when the source was opened for this project (see `DOWNLOAD_LOG.csv`).

- Asner, G. P., & Tupayachi, R. (2017). Accelerated losses of protected forests from gold mining in the Peruvian Amazon. *Environmental Research Letters*, 12, 094004. https://doi.org/10.1088/1748-9326/aa7dab (accessed 2026-10-12)
- Conley, T. G., & Taber, C. R. (2011). Inference with "difference in differences" with a small number of policy changes. *Review of Economics and Statistics*, 93(1), 113–125. https://doi.org/10.1162/REST_a_00049 (accessed 2026-10-10)
- Dethier, E. N., Silman, M. R., Fernandez, L. E., Caballero Espejo, J., Alqahtani, S., Pauca, P., & Lutz, D. A. (2023). Operation Mercury: Impacts of national-level armed forces intervention and anticorruption strategy on artisanal gold mining and water quality in the Peruvian Amazon. *Conservation Letters*, 16(5), e12978. https://doi.org/10.1111/conl.12978 (abstract; accessed 2026-10-15)
- Earth Genome (2026). Amazon Mining Watch, mining detections, model 48px_v4.10b (updated 3 Oct 2026). https://source.coop/earthgenome/amazon-mining-watch (accessed 2026-10-10)
- Finer, M., & Mamani, N. (2020, 1 Dec). Illegal gold mining down 78% in Peruvian Amazon, but still threatens key areas. MAAP #130, figures "La Pampa" and "Before and after". https://www.maapprogram.org/gold-mining-peru/ (accessed 2026-10-10)
- Frankfurt Zoological Society (n.d.). Bahuaja-Sonene and Tambopata. https://fzs.org/en/programs/peru/bahuaja-sonene-and-tambopata/ (accessed 2026-10-09)
- MapBiomas Amazonía (2024). Colección 6.0 de mapas anuales de cobertura y uso del suelo en la Amazonía, 1985–2023; factsheet p. 3. https://amazonia.mapbiomas.org (accessed 2026-10-12)
- MapBiomas Brasil (2025). Collection 11 (mining) and Collection 10.1 (indigenous-territory statistics). https://brasil.mapbiomas.org (accessed 2026-10-10)
- MapBiomas Peru (2025). Collection 4 of annual land cover maps of Peru: annual maps and buffer-zone, protected-area and department statistics. https://peru.mapbiomas.org (accessed 2026-10-10)
- MEF (2026). Consulta Amigable, programa presupuestal 0128, Madre de Dios. https://apps5.mineco.gob.pe/transparencia/Navegador/ (accessed 2026-10-12)
- MINAM (2021). Plan Restauración: Plan integral frente a la minería ilegal (Anexo, D.S. N° 017-2021-MINAM), pp. 33, 55–56. https://faolex.fao.org/docs/pdf/per206467anx.pdf (accessed 2026-10-13)
- MINEM (2026). Estadísticas mineras: producción minera; and BCRP (2026), Madre de Dios gold production series. https://www.gob.pe/institucion/minem/informes-publicaciones/5472883-produccion-minera ; https://estadisticas.bcrp.gob.pe (accessed 2026-10-12)
- Pacsi, R., Novoa, S., La Torre, S., Balbuena, H., Finer, M., Santana, A., & Castillo, H. (2026, 10 May). Rapid expansion of illegal gold mining in Tambopata National Reserve. MAAP #241, Image 1. https://www.maapprogram.org/mining-peru-tambopata/ (accessed 2026-10-10)
- Peru (2004). Ley N° 28258, Ley de Regalía Minera, Art. 5 and Art. 10. https://www.leyes.congreso.gob.pe (accessed 2026-10-13)
- University of Maryland GLAD (2026). GLAD-L Landsat forest-loss alerts, 2017–2026. https://storage.googleapis.com/earthenginepartners-hansen/ (accessed 2026-10-12)
- World Bank (2026). Commodity price data (Pink Sheet), monthly, gold. https://www.worldbank.org/en/research/commodity-markets (accessed 2026-09-23)
- Yupanqui, O., Quispe, M., Novoa, S., Castañeda, C., Escalante, E., Finer, M., & Mamani, N. (2023, 28 Sep). El retorno de minería ilegal en La Pampa. MAAP #193, dredge counts. https://www.maapprogram.org/es/retorno-mineria-la-pampa-peru/ (accessed 2026-10-10)

AI is not a source: no fact above is cited to an AI tool.

## Appendix A. Data log and definitions

`DOWNLOAD_LOG.csv` has one row per raw file (or per set of identical-format files): source, URL, collection, theme, years, access date, downloader and check number. Files above 50 MB and files with personal data are not in the zip; the log links them. Definitions used everywhere (`code/definitions.py`): net additions = new + re-mined − stopped; zones = official SERNANP buffer zones kept whole (overlaps go to Tambopata, as MapBiomas does), the La Pampa sector, the D.L. 1100 corridor outside buffer zones (across the road: ≤ 10 km north of the highway at La Pampa's longitudes), native communities, rest of Madre de Dios; periods 2016–18, 2019–21, 2022–25. `output/brief_numbers.csv` lists every number in this brief, in order of appearance, with its measure, zone and period.

## Appendix B. AI output for part 4

**Prompt (the course's required prompt, our comparison filled in):** "Here is my comparison: Units: the buffer zone of the Tambopata National Reserve in Madre de Dios, Peru, where the government enforcement operation "Operación Mercurio" against illegal gold mining started in February 2019, versus the buffer zone of the Amarakaeri Communal Reserve, a nearby zone with mining that was less treated (a follow-up operation in 2019 also covered it), plus 13 other Peruvian buffer zones with mining as additional comparisons. Years: 2014–2025. Outcome: net mining additions per year in hectares, i.e. the annual change in area classified as mining in MapBiomas Peru Collection 4 satellite land-cover maps, which equals land mined for the first time plus old mining land mined again minus mining land that left the mining class. Comparison: the change in mean annual net additions from 2016–18 (before) to 2019–21 (during the operation and its follow-ups) in Tambopata minus the same change in Amarakaeri (difference-in-differences: −1,761 ha/yr), and the same with zone and year fixed effects across all 15 zones. List the reasons this comparison could mislead, distinguishing omitted variables, reverse causation, selection of units, and measurement error in the outcome. For each, say what data or design would fix it."

**Tool:** Claude Code CLI 2.1.300 (Anthropic), non-interactive, no tools, run outside our project folder (no access to our files), 2026-10-15. **Raw answer:** reproduced in full below (Appendix B1). **Edited version:** part 4(b) above.

**What we kept, changed and dropped:**

- *Kept:* mean reversion (targeted at the peak), displacement into the comparison, one treated unit (placebo inference), net additions mixing new, re-mined and exits (the AI's "net additions could fall while mining activity stays the same"), dredges invisible to the maps.
- *Added from our own tests:* the size of each part (half the fall is stopping), the flicker share, the direction of each bias, and the fake-start check.
- *Dropped, could not do with our data or time:* hydrology and cloud-cover controls, per-zone accuracy assessment, a dose built from operation logs, distance-to-base designs (no patrol records available to us).
- *Corrected:* the AI dates follow-up operations under "Plan Restauración extensions" in 2019; Plan Restauración is from 2021 (MINAM, 2021).

### Appendix B1. Raw AI answer (unedited)

#### Why the Tambopata vs. Amarakaeri DiD (−1,761 ha/yr) could mislead

The −1,761 ha/yr estimate rests on one treated unit, a control that was partly treated, and an outcome built by subtracting one classified map from another. Below, each problem is listed with the data or design that would fix it.

---

#### 1. Omitted variables (things that changed differently in the two zones around 2019)

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

#### 2. Reverse causation (the outcome drove the treatment)

- **Operation targeted the surge.** Operación Mercurio was launched *because* La Pampa's expansion peaked in 2016–18. Picking the treated unit at its peak creates mean reversion (an Ashenfelter-type dip in reverse). The 2016–18 baseline is exactly the abnormal period, so part of the post-2019 drop would have happened anyway.
  - **Fix:** Show pre-trends from 2014 in an event study. Use a baseline that excludes the peak years, or model the trend explicitly. Use synthetic control matched on the whole 2014–18 trajectory, not just levels. Find timing variation that is plausibly unrelated to mining, such as the national political decision under the Vizcarra government or the Supreme Decree date. Use that as an instrument or in a timing-based design.
- **Follow-up operations responded to displacement.** Later 2019 operations, such as the Plan Restauración extensions, moved into areas including Amarakaeri because miners showed up there. So the control's treatment status depends on its own outcome.
  - **Fix:** Code treatment as a time-varying dose from operation logs (base locations, patrol and interdiction counts by zone and month). Lag the dose so that this year's mining cannot cause this year's enforcement.
- **Within-zone targeting.** Patrols go where mining is visible, so enforcement intensity tracks the outcome.
  - **Fix:** Use a distance-to-base design, comparing pixels just inside vs. just outside patrol radii. Treat base locations as fixed before 2019.

---

#### 3. Selection of units (who counts as treated and who counts as control)

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

#### 4. Measurement error in the outcome (MapBiomas mining class)

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

#### Bottom line

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


---
*Built 2026-10-15 19:41 from git commit 3c7487d (working tree may contain uncommitted changes). Numbers from output/numbers.csv (2611 rows).*
