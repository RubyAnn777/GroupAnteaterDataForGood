# When the patrols leave: what Operation Mercurio tells FZS about enforcement against gold mining

Group Giant Anteater · Data for Good · Question 2 · October 2026 · Ruby Ann Grambauer, Sebastian Schmid, Laurens van der Lely, Omkar Mate, Dhruv Chaudhari

## 1. The question

**FZS pays for enforcement and needs to know what it buys.** It supports SERNANP's operations against alluvial gold mining around Tambopata and Bahuaja-Sonene (FZS, n.d.). Operations are costly and temporary, so the question is: **what happens in the targeted area, and around it, when an operation ends?** Mining could stop (**deterrence**), move elsewhere (**displacement**) or return later (**delay**). Inside the target these three look alike, so we need comparison areas.

**Case:** Operation Mercurio at La Pampa, Peru's largest illegal mining area, in the buffer zone of Tambopata National Reserve (Madre de Dios). **Treatment:** the start of the operation in February 2019 (first treated year: 2019). COVID-19 (2020), Plan Restauración (2021) and the April 2023 state of emergency are context, so we measure "Mercurio and what followed". **Target:** the Tambopata buffer zone (official boundary) and its La Pampa sector (70.15–69.80° W). **Comparison:** the 14 other Peruvian buffer zones with mining, above all the Amarakaeri buffer zone, which was only "less treated" (Mercurio II covered all of Madre de Dios in 2019; MINAM, 2021, p. 33). **Around the target:** the legal mining corridor across the highway, the reserve and the department. **Periods:** 2016–18, 2019–21 and 2022–25 ("later years").

## 2. Data and provenance

**One outcome throughout: net mining additions** (ha/yr) = land mined for the first time (**new land**) + old mining land mined again (**re-mined**) − mining land that left the mining class (**stopped**). We count it pixel by pixel on the 30-m annual maps of **MapBiomas Peru, Collection 4** (class 4.2: all mining, legal and illegal); exact definitions are in Appendix A. One check per dataset, our number against the publisher's:

| Dataset (publisher, version; used for) | Check | Ours | Publisher |
|---|---|---|---|
| MapBiomas Peru, Col. 4 annual maps (outcome) | mining area 2025, Tambopata buffer zone | 20,730 ha | 20,730 ha |
| | mining area 2025, Tambopata reserve | 777 ha | 777 ha |
| | mining area 2025, Madre de Dios | 112,611 ha | 112,622 ha |
| World Bank Pink Sheet (gold price) | August 2026 | $4,411/oz | $4,411/oz |
| MINEM files vs central bank, BCRP (gold output, Madre de Dios) | 2019 (an artisanal *estimate* until 2019) | 7,103 kg | 7,073 kg |
| MEF programme PP 0128 (enforcement spending, Madre de Dios) | 2019 | S/ 31,120,611 | S/ 31,120,611 |
| Amazon Mining Watch, AMW (cross-check, twins) | no published totals: Tambopata buffer zone 2018, our zone cut vs a polygon cut | 21,108 ha | 21,127 ha |
| MapBiomas Amazonía, Col. 6 (twins) | mining area, whole Amazon, 2023 | 775,746 ha | 780,000 ha |

Small gaps reflect boundary versions (Madre de Dios) and later revisions (BCRP). Files: `DOWNLOAD_LOG.csv`; every number and the figure: `code/main.py`; online walkthrough: Appendix D.

## 3. Findings

**It fell: net mining in the target dropped 90%** **[description]**. In the Tambopata buffer zone, net additions fell from 1,640 ha/yr (2016–18) to 163 (2019–21), while in the less-treated Amarakaeri buffer zone they rose from 289 to 574: a difference-in-differences of **−1,762 ha/yr** (2016–18 base). A fake start in 2016 (2013–15 vs 2016–18) gives +209. Every year in 2019–21 (at most 417 ha) was below every year in 2011–18 (at least 707 ha).

**In 2019, new pits kept opening while old ones went quiet** **[description]**. In 2019 the Tambopata buffer zone still gained 1,926 ha of new land (2018: 2,369 ha), but 1,807 ha stopped, so net additions were only 417 ha. Over 2019–21, stopping explains a quarter to a half of the fall (25%–47%, depending on whether land mined again within two years is counted), and 68% of the extra stopping came in 2019. The rest of the fall is fewer new pits, mainly in 2020–21 (COVID). In Amarakaeri, stopped land stayed flat (542 → 584 ha/yr). In the Tambopata buffer zone, half of the stopped land became water (50%), and 37% was mined again within two years (2016–18: 28%). Using other indicators (mining ponds), Dethier et al. (2023) report that 70–90% of activity was abandoned in the targeted zones and that mining sped up just outside them.

**Where it went: mining rose next door, and the region never fell** **[description]**. In the corridor strip just across the highway (up to 10 km north, opposite La Pampa), net additions rose from 60 to 395 ha/yr (2016–18 vs 2019–21). Across all legal mining-corridor land (D.L. 1100), the corridor's share of the department's net additions rose from 42% to 80% (period sums). Madre de Dios as a whole went from 3,610 to 4,639 to 12,047 ha/yr (2016–18, 2019–21, 2022–25).

![Net mining additions and their three parts, Tambopata buffer zone 2014–2025 (top); net additions by area, Madre de Dios, period means (bottom)](../../output/fig_brief_main.png)

**Why and how it came back: money faded, gold soared, old pits reopened** **[description]**. Enforcement spending in Madre de Dios (PP 0128) peaked at S/ 31.1 million in 2019 and fell to S/ 5.0 million in 2025, while the gold price rose 2.7-fold (2018–25). In 2022–25 the Tambopata buffer zone averaged 1,829 ha/yr (1,251 without 2023, a spike that only MapBiomas shows), and a third to a half of the land added was re-mined (33%–46%, without/with 2023). Inside Tambopata National Reserve, net additions were +241 ha in 2025, the year the navy left the river posts; MAAP reports about 500 ha from late 2025 to February 2026 (Pacsi et al., 2026).

**What we can say about cause** **[causal]**. *If the other Peruvian buffer zones show what the Tambopata buffer zone would otherwise have done*, then Mercurio and the operations that followed lowered its net mining additions by about 1,453 to 1,663 ha/yr in 2019–21 (compared with all 14 other zones, or with Amarakaeri alone, using a 2014–18 base). A quarter to a half of this is pits going quiet; the rest is fewer new pits. All six methods we tried point down and two hold up in hectares, but none passes all of its own checks (Appendix C): the fall is the largest of the 15 zones in hectares, as it already was in 2014–16 because Tambopata is the largest mining zone, yet it ranks only 3rd to 6th of 7 relative to each zone's size. Read it as an upper bound (see 4b).

## 4. What FZS can do with this

**(a) What FZS learns** **[prediction]**. From this one case, expect a sharp local fall while the operation runs, of which a quarter to a half is pits going quiet; mining rising next door and across the nearest legal boundary; a return within about three years, partly on old pits; and no fall in the region. FZS could therefore **fund a lasting presence rather than one-off sweeps; watch a ring of a few kilometres around each operation with near-real-time forest-loss alerts** (new pits kept opening in 2019); **guard the reserve's first kilometre and the river posts** (91% of first-time mining inside the reserve along its buffer-zone border, 2000–25, lies within 1 km of the edge); and push for gold-origin tracing in the corridor (small producers pay a 0% royalty, Ley 28258, Art. 5; nationally, only 145 of the 9,592 miners in the formalization register were fully formalized; MINAM, 2021, pp. 55–56).

**(b) Why this could mislead, and in which direction.** *Omitted variables:* COVID-19, the gold price (×2.7, 2018–25) and later operations overlap 2019–21 and need not affect all zones alike (probably overstates the fall). *Reverse causation:* La Pampa was targeted at its peak, so part of the fall is a return to normal (overstates). *Selection of units:* there is one targeted zone, far larger than any comparison, so standard errors are not informative (Conley & Taber, 2011) and rankings in hectares mostly reflect size; Amarakaeri received miners (overstates) but had its own operation (understates). *Measurement error:* net additions mix three processes, and part of "stopped" is temporary or map noise, so **net additions can fall while activity does not** (overstates); hectares are a proxy for miners; the mining class mixes legal and illegal mining; and **satellites cannot see river dredges or mercury** (MAAP counted 148 → 598 dredges in La Pampa, 2021–23; Yupanqui et al., 2023), so a shift to rivers adds no hectares (overstates). **Read the fall as an upper bound and the return as a lower bound.**

**(c) What would let us say more.** Dated patrol and interdiction records from SERNANP or FZS (were the stopped pits the raided ones?); an image-checked sample of stopped pits; concession and formalization-register (REINFO) maps to grade legality pixel by pixel; dredge counts and mercury sampling; and more operations as cases.

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

## Appendix A. Definitions and data log

**Outcome.** For every 30-m pixel and year *t* on the MapBiomas Peru Collection 4 maps (class 30, "4.2 Minería"):

| Part | The pixel is mining… | Meaning |
|---|---|---|
| **New land** | in *t*, and in no earlier year since 1985 | first-time mining, usually cleared forest |
| **Re-mined** | in *t*, not in *t* − 1, but in some year before *t* − 1 | an old pit that was out of use for at least one year and is worked again (a pit mined in both *t* − 1 and *t* is in none of the three flows: it stays in the stock) |
| **Stopped** | in *t* − 1, not in *t* | a pit that left the mining class: flooded, regrowing, bare or reclassified |

**Net additions** = new land + re-mined − stopped = mining area in *t* − mining area in *t* − 1 (checked for every zone and year). Hectares measure mining activity on land, not the number of miners.

**Zones** (`code/definitions.py`, one registry for every number): official SERNANP buffer zones kept whole (where they overlap, the land goes to Tambopata, as MapBiomas does; the Kotsimba native community lies inside the Tambopata buffer zone); the **La Pampa sector** = the Tambopata buffer zone between 70.15° and 69.80° W; the **corridor across the road** = D.L. 1100 mining-corridor land up to 10 km north of the Interoceanic Highway at La Pampa's longitudes; the **legal mining corridor** = all D.L. 1100 land outside buffer zones; native communities; the rest of Madre de Dios. **Treatment:** start of Operation Mercurio, February 2019; first treated year 2019; reference year 2018. **Periods:** 2016–18 (before), 2019–21, 2022–25 (later years, also reported without 2023).

**Data log.** `DOWNLOAD_LOG.csv` has one row per raw file (or per set of files with the same format): source, URL, collection, theme, years, access date, downloader and check number. Files above 50 MB and files with personal data are not in the zip; the log links them. `output/brief_numbers.csv` lists every number in this brief in order of appearance, with its measure, zone and period.

## Appendix B. AI output for part 4

**Prompt (the course's required prompt, our comparison filled in):** "Here is my comparison: Units: the buffer zone of the Tambopata National Reserve in Madre de Dios, Peru, where the government enforcement operation "Operación Mercurio" against illegal gold mining started in February 2019, versus the buffer zone of the Amarakaeri Communal Reserve, a nearby zone with mining that was less treated (a follow-up operation in 2019 also covered it), plus 13 other Peruvian buffer zones with mining as additional comparisons. Years: 2014–2025. Outcome: net mining additions per year in hectares, i.e. the annual change in area classified as mining in MapBiomas Peru Collection 4 satellite land-cover maps, which equals land mined for the first time plus old mining land mined again minus mining land that left the mining class. Comparison: the change in mean annual net additions from 2016–18 (before) to 2019–21 (during the operation and its follow-ups) in Tambopata minus the same change in Amarakaeri (difference-in-differences: −1,761 ha/yr), and the same with zone and year fixed effects across all 15 zones. List the reasons this comparison could mislead, distinguishing omitted variables, reverse causation, selection of units, and measurement error in the outcome. For each, say what data or design would fix it."

**Tool:** Claude Code CLI 2.1.300 (Anthropic), non-interactive, no tools, run outside our project folder (no access to our files), 2026-10-15. The prompt quotes −1,761 ha/yr, our value before a later 0.07% pixel-area correction; the brief uses the corrected −1,762. **Raw answer:** reproduced in full at the end (Appendix B1). **Edited version:** part 4(b) above.

**What we kept, changed and dropped:**

- *Kept:* mean reversion (targeted at the peak), displacement into the comparison, one treated unit (placebo inference), net additions mixing new, re-mined and exits (the AI's "net additions could fall while mining activity stays the same"), dredges invisible to the maps.
- *Added from our own tests:* the size of each part (stopping explains a quarter to a half of the fall), the flicker share, the direction of each bias, and the fake-start check.
- *Dropped, could not do with our data or time:* hydrology and cloud-cover controls, per-zone accuracy assessment, a dose built from operation logs, distance-to-base designs (no patrol records available to us).
- *Corrected:* the AI dates follow-up operations under "Plan Restauración extensions" in 2019; Plan Restauración is from 2021 (MINAM, 2021).

## Appendix C. Six methods for cause, in one table

All on net additions, Tambopata buffer zone, 2019–21. None passes all of its own checks, so every result is a description of how far the target differs from a stand-in.

| Method | Compares Tambopata with | Result | Verdict |
|---|---|---|---|
| Zone and year effects (difference-in-differences) | 14 other Peruvian buffer zones | −1,453 ha/yr; largest of 15 in hectares, 4th of 7 relative to size | holds up, in hectares only |
| Simple before/after vs Amarakaeri | Amarakaeri buffer zone (2014–18 base) | −1,663 ha/yr | other end of the range |
| Synthetic difference-in-differences | weighted zones and years | −1,544 ha/yr | holds up, in hectares only |
| Synthetic control | a weighted copy built before 2019 | −411 ha/yr | no good copy before 2019 |
| Rule-based twins (AMW, another product) | look-alike mining areas in Brazil | Tambopata at 16%–41% of the twins' pace | different trends before 2019 |
| Matching, 5 estimators | areas picked by algorithm | placebo p 0.15–0.60 | cannot beat chance |
| Either side of the road (spatial discontinuity) | land just north vs just south of the highway | +2.2 points of land a year (p = 0.25) | too noisy to tell |

## Appendix D. Online material and files

- **Walkthrough** (every analysis and figure, in the order of this brief): https://claude.ai/artifact/VT9wkZqxhH8WAHU4v36mg6
- **Methods page** (each method: question, how it works, limits, code): https://claude.ai/artifact/83ZeCu4frkocBDJ46RV1pA
- **This brief online:** https://claude.ai/artifact/NRjV7R75F8Wvogn6Bs3ycJ
- Offline copies of all three pages are in `deliverables/pages/` and in the replication zip (`docs/walkthrough/EXPLAINER.html`, `METHODS.html`, `docs/brief/BRIEF.html`).

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
*Built 2026-10-15 22:37 from git commit 34c2c5f (working tree may contain uncommitted changes). Numbers from output/numbers.csv (2723 rows).*
