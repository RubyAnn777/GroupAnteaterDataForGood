<!--
Source of docs/overnight/REPORT.html. Build: `uv run python docs/overnight/build_report.py`.
Placeholders {{id}} or {{id:fmt}} are filled from output/numbers.csv (default fmt ",.0f"; the build fails if an id is missing).
Claim tags: [[D]] description, [[P]] prediction, [[C]] causal. Figures: ![caption](output/fig_x.png) are embedded as base64.
Sections are split on "## ". Lines starting with "> " become callouts.
-->

# Overnight analysis report: how does mining move with enforcement?

> For the team (Group Giant Anteater, Question 2, Peru + Brazil). Produced overnight on 10/11 Oct 2026 on branch `analysis/overnight-2026-10-10` by Claude, an AI assistant, and its subagents. Every number below is read from `output/numbers.csv`, which `uv run python code/main.py` writes. An adversarial review pass (`docs/overnight/notes/review.md`) was applied, but nothing here is checked by a human yet. Read it critically, re-open every source you cite, and treat every claim tag as a proposal. This report is not a source for the brief. The sources are.

## 1. Summary of findings

**What FZS asked:** what to expect in the targeted area, and around it, when an enforcement operation ends.

**Short answer from our data** [[D]]: Where Mercurio hit (the Tambopata buffer zone), new mining fell sharply in 2019–21 and was back near or above its 2016–18 level in 2022–25. Over the same years the nearby Amarakaeri buffer zone and the rest of Madre de Dios rose. From this data we cannot tell whether that rise is displacement, COVID, the gold price or legal corridor mining. The prediction for FZS is in the box at the end of this section.

**Peru (Operation Mercurio, Feb 2019)**

1. [[D]] New mining in the **Tambopata buffer zone** (where La Pampa lies) fell from {{mean_add_tambopata_2016_18}} ha/yr (2016–18) to {{mean_add_tambopata_2019_21}} ha/yr (2019–21). In the **Amarakaeri buffer zone** it rose from {{mean_add_amarakaeri_2016_18}} to {{mean_add_amarakaeri_2019_21}} ha/yr. These four period means reproduce the question card. Their difference of changes is **{{did_main}} ha/yr**, matching the starter. With a 2014–18 baseline it is {{did_main_base_2014_18}} ha/yr. The 2016–18 "before" period already includes the 2017–18 interdictions (MAAP #241), so it is not enforcement-free.
2. [[D]] No other buffer zone with real mining fell as much. Among the {{placebo_space_n_restricted}} Amazon buffer zones with more than 10 ha/yr of pre-2019 additions, Tambopata has the most negative 2019–21 coefficient (rank {{placebo_space_rank_restricted}}). With so few peers this is "no comparable zone fell", not a significance test. A fake operation in 2016 gives {{did_placebo}} ha/yr. The event study, however, shows a 2016 coefficient ({{eventstudy_pretrend_poolA_2016}} ha) as far outside the placebo band as the post-2019 ones, so the parallel-trends assumption behind any causal reading is **not supported**.
3. [[D]] **The region did not fall.** New mining in all of Madre de Dios was {{mean_add_mdd_total_2016_18}} → {{mean_add_mdd_total_2019_21}} → {{mean_add_mdd_total_2022_25}} ha/yr (2016–18 / 2019–21 / 2022–25). Most of it lies outside the buffer zones ("rest of Madre de Dios": {{mean_add_rest_mdd_2016_18}} → {{mean_add_rest_mdd_2019_21}} → {{mean_add_rest_mdd_2022_25}} ha/yr). This fits displacement, but it fits COVID, the gold price, legal corridor mining and REINFO formalisation just as well. MAAP #208 finds that 74% of 2021–24 mining deforestation in Madre de Dios lay inside the official mining corridor. A second product, Amazon Mining Watch, does **not** show the rise: its new patch area in the corridor falls from {{spz_corridor_ha_2019_21}} ha (2019–21) to {{spz_corridor_ha_2022_24}} ha (2022–24). The regional rise therefore rests on MapBiomas alone.
4. [[D]] **Return:** Tambopata's annual additions after 2021 were {{add_tambopata_2022}} (2022), {{add_tambopata_2023}} (2023), {{add_tambopata_2024}} and {{add_tambopata_2025}} ha (2024–25). The 2022–25 mean ({{mean_add_tambopata_2022_25}} ha/yr) is above 2016–18, but only because of 2023, a year when every unit spiked (Amarakaeri {{add_amarakaeri_2023}}, rest of Madre de Dios {{add_rest_mdd_2023}} ha). Without 2023 the mean is {{mean_add_tambopata_2022_25_ex2023}} ha/yr, below the pre-Mercurio level. The 2023 spike falls inside the state of emergency (from 7 Apr 2023), so "mining came back when enforcement ended" is too simple.
5. [[D]] **Inside the reserve itself** (new file: MapBiomas Peru protected-area statistics), mining in Tambopata National Reserve is small but growing: {{anp_level_tam_nr_2025:,.0f}} ha in 2025, of which {{anp_tam_nr_addition_2025}} ha was added in 2025 alone. Two differently built products point the same way. MAAP #241 reports 500 ha of new mining inside the reserve (H2 2025 to Feb 2026). Amazon Mining Watch first detects {{sp_amw_tambopata_nr_new_ha_2019_2024}} ha inside the reserve over 2019–24 combined, then {{sp_amw_tambopata_nr_new_ha_2025}} ha in 2025 alone (provisional). The three measure different things, so we compare only their direction, never their hectares.
6. [[D]] Declared (formal) gold production in Madre de Dios fell by {{pe_prod_fall_2018_2025_pct:.0f}}% between 2018 and 2025, while mapped mining area more than doubled ({{pe_prod_mapbiomas_level_2018_ha}} → {{pe_prod_mapbiomas_level_2025_ha}} ha). Production was already falling before Mercurio ({{pe_prod_2016_t:.1f}} t in 2016, {{pe_prod_2018_t:.1f}} t in 2018). The steepest drop was 2019 → 2020, the COVID year ({{pe_prod_fall_2019_2020_pct:.0f}}%). Either more gold left undeclared, or reporting and formalisation rules changed. We cannot tell which.
7. [[D]] A synthetic control for Tambopata **does not work**. Tambopata adds far more mining than any donor zone (outside the donor range in {{synth_core_add_hull_years_outside}} of 9 pre-years), so no weighted mix of donors reproduces its history. We report the attempt in §5 and do not use it.

**Brazil (weak enforcement 2019–22, Yanomami operation Feb 2023)**

8. [[D]] Total IBAMA infraction notices in the Legal Amazon averaged {{br_ibama_aml_mean_2015_2018}} per year in 2015–18 and {{br_ibama_aml_mean_2019_2022}} in 2019–22, then {{br_ibama_aml_2023}} in 2023. This matches the documented fall in federal enforcement: embargoes −59% and confiscations −55% in 2019–2020 (Nunes et al. 2024). Notices that our text match flags as mining-related **did not fall** ({{br_ibama_mining_aml_mean_2015_2018}} → {{br_ibama_mining_aml_mean_2019_2022}} per year, a noisy count). Over the same periods, new artisanal mining in all indigenous lands combined went {{br_pack_art_add_mean_2016_2018}} → {{br_pack_art_add_mean_2019_2022}} → {{br_pack_art_add_mean_2023_2025}} ha/yr (2016–18 / 2019–22 / 2023–25). The fit with weaker enforcement is plausible, but this data does not show it.
9. [[D]] New mining in the **Yanomami** territory fell from {{br_ti_yanomami_add_2022}} ha (2022) to {{br_ti_yanomami_add_2023}} (2023) and {{br_ti_yanomami_add_2024}} ha (2024), per MapBiomas Collection 10.1. **Kayapó** and **Munduruku** also fell, so the 2×2 comparison (2020–22 vs 2023–24) is inconclusive. In hectares, Yanomami fell *less* than Kayapó ({{br_did_main_vs_Kayapo_ha_yr:+,.0f}} ha/yr), the opposite of an operation effect. Relative to each territory's 2022 stock it fell more ({{br_did_main_vs_Kayapo_pct:+.1f}} pp). A fake 2020 start already gives {{br_did_placebo_time_start_2020_ha_yr:+,.0f}} ha/yr. The sources also disagree on 2023: DETER mining alerts in Yanomami *rose* in the 12 months after Feb 2023 ({{br_deter_yan_12m_before_feb2023_km2:.1f}} → {{br_deter_yan_12m_after_feb2023_km2:.1f}} km²), while the annual maps fell. Alerts are dated by detection, and the operation itself may have revealed sites.
10. [[D]] We see no growth in mapped mining in the rest of Roraima ({{br_rr_yanomami_share_2024:.0f}}% of Roraima's mining is inside the Yanomami territory; the rest changed by {{br_rr_outside_yanomami_add_2023_24:+,.0f}} ha in 2023–24). That tests only one narrow channel. Miners can also move to Venezuela, Amazonas or Pará. The 19 smaller mining territories together added {{br_other19_add_mean_2020_2022}} → {{br_other19_add_mean_2023_2024}} ha/yr, and one of them, Sararé, accounts for +{{br_sarare_add_2023_24_sum}} ha of the 2023–24 additions. Without Sararé the other 18 fell (per territory, {{br_other18_ex_sarare_add_mean_2020_2022}} → {{br_other18_ex_sarare_add_mean_2023_2024}} ha/yr).

> **What FZS can take from this** [[P]] (prediction from two cases, one treated unit each; not a causal estimate): when an operation targets one hotspot, expect a sharp local fall while the presence lasts. Nearby, less protected land does not fall and may rise. The local fall can reverse within a few years, as Tambopata did from 2022, but how fast depends on one spike year (2023). In Peru the protected core is now being entered (2025). Brazil's 2023 fall happened in every large territory at once, so it says more about national enforcement than about one operation.

## 2. Data obtained

| Source | File (data_raw/ unless noted) | Years | Check number | Status |
|---|---|---|---|---|
| MapBiomas Peru, Collection 4, buffer zones (pack) | data/peru_bufferzone_year.csv | 1985–2025 | Tambopata BZ 2025 = 20,730 ha (card; platform also shows 20,730 ha) | OK |
| MapBiomas Peru, Collection 4, departments (pack) | data/peru_department_year.csv | 1985–2025 | Madre de Dios 2025 = 112,622 ha | OK |
| MapBiomas Peru, Collection 4, **protected areas** (new) | mapbiomas_peru/MAPBIOMAS-PERU-LULC-COL4-AREAS-PROTEGIDAS.xlsx | 1985–2025 | Tambopata NR mining 2025 = {{anp_level_tam_nr_2025:,.1f}} ha; MapBiomas platform shows 777 ha (screenshot) | OK |
| MapBiomas Brazil, Collection 10.1, **indigenous territories** (new) | mapbiomas_brazil/MAPBIOMAS_BRAZIL-COVERAGE_STATISTICS-COL.10.1-INDIGENOUS_TERRITORIES_STATE_BIOME.xlsx | 1985–2024 | Kayapó 2024 = {{br_ti_kayapo_stock_2024}} ha; Col 10 file agrees within {{br_col10_vs_col101_max_rel_diff_pct:.2f}}% (2018+) | {{CHECK_BRAZIL_TI}} |
| MapBiomas Brazil, Collection 11, mining (pack) | data/mining_area.csv | 1985–2025 | All TIs artisanal 2025 = {{br_pack_art_level_2025}} ha (card) | OK (Brazil publisher check) |
| MapBiomas Brazil, Collection 10.1, municipalities (pack) | data/brazil_municipality_year.csv | 1985–2024 | Roraima 2018 = {{br_rr_level_2018}} ha, 2024 = {{br_rr_level_2024}} ha | OK |
| IBAMA open data, autos de infração (new) | ibama/auto_infracao_csv.zip (117 MB, git-ignored; small intermediate in data_intermediate/) | 1977–2026 | IBAMA's site shows no total; file integrity only | data OK / check BLOCKED |
| IBAMA embargoes | – | – | – | BLOCKED (no download URL found) |
| INPE TerraBrasilis DETER, class MINERACAO (new) | inpe_deter/deter_amz_mineracao.geojson | 2016–2026 | 2019 = {{br_deter_2019_total_wfs_km2:.2f}} km² vs dashboard {{br_deter_2019_total_dashboard_km2:.2f}} km² | OK (0.2% domain difference) |
| BCRP series (source MINEM), gold production Madre de Dios (new) | bcrp/*.json | 2001–2025 | Monthly sums = annual (all years) | OK (internal only) |
| Amazon Mining Watch, mining patches (new) | amw/amazon_basin_detections.geojson (112 MB, git-ignored) | 2018–2026 | 232,030 patches | OK (prototype) |
| SERNANP protected areas, buffer zones, illegal-mining layer (new) | sernanp/*.geojson | current | Tambopata = anp_codi RN09 | OK |
| FUNAI indigenous territories (new) | funai/tis_poligonais.geojson (49 MB, git-ignored) | current | Yanomami 9,664,975 ha (FUNAI attribute) | OK |
| INGEMMET mining corridor D.L. 1100 (new) | ingemmet/corredor_minero_madre_de_dios_DL1100.geojson | current | 498,308 ha vs 498,296 ha cited by government | OK |
| MAAP #130, #193, #208, #241 (citations) | maap/*.txt | 2020–2026 | Quotes with locations in notes/maap_citations.md | Quotes verified. Raw HTML must be saved manually |

Every file has a row in `DOWNLOAD_LOG.csv` (URL, access date, collection, sha256, check number). Literature opened overnight: `docs/overnight/notes/literature.md`.

## 3. Steps taken

1. Created branch `analysis/overnight-2026-10-10` from `main`. Read agent.md, basics.html, strategy.html and the course PDFs.
2. Phase 1, in parallel: Peru protected-area download, Brazil territory download, Brazil enforcement (IBAMA + papers), MAAP citations, enforcement timeline (were the controls treated?), spatial layers, extra-data scout (DETER, BCRP).
3. Phase 2: `code/main.py` plus one module per part. `checks.py` re-runs the 6 starter checks plus the card and publisher numbers and fails loudly.
4. Phase 3, Peru: additions per unit, 2×2 DiD, displacement sums, placebo (2016), persistence (2022–25), event study (pyfixest, 2018 = reference) with placebo-in-space, inside-reserve analysis, declared production.
5. Phase 4, Brazil: all-indigenous-land series (Col 11), per-territory series (Col 10.1), 2×2 DiD in ha and in % of stock, placebo, Roraima displacement, IBAMA intensity, DETER monthly alerts.
6. Phase 5: robustness (alternative controls, drop the largest unit, 2014–18 baseline, restricted placebo pool, synthetic control attempt, buffer-zone overlap check).
7. Phase 6: spatial prototype with Amazon Mining Watch patches by zone (reserve / buffer zone / corridor / rest) and distance rings around La Pampa and the Brazilian territories.
8. Publisher-side checks on the MapBiomas platforms in Chrome; MAAP pages captured as text.
9. Adversarial review of claims and code (`notes/review.md`). The high- and medium-severity items are fixed in this version.
10. Built this report from `output/` with `docs/overnight/build_report.py`.

## 4. Decision log

{{DECISIONS_TABLE}}

## 5. Figures

![Proposed brief figure: Tambopata BZ vs Amarakaeri BZ vs inside Tambopata NR; Madre de Dios total and rest](output/fig_brief_main.png)
**Reading:** [[D]] Tambopata's additions drop in 2019–21 and return from 2022. Amarakaeri and the rest of the department rise. Inside the reserve stays near zero until 2025.

![Peru: annual additions by buffer zone, Madre de Dios total and rest, and the gold price](output/fig_peru_additions.png)
**Reading:** [[D]] All series jump in 2023. The gold price rose {{gold_price_ratio_2025_2018:.1f}}× between 2018 and 2025, but only {{gold_price_pct_change_2022_2023:.0f}}% in 2023 itself, so the price alone does not explain that year's spike.

![Event study: Tambopata vs comparison zones, 2018 = 0](output/fig_peru_event_study.png)
**Reading:** [[D]] The 2019–22 coefficients sit far below the placebo band, but so does 2016 ({{eventstudy_pretrend_poolA_2016}} ha against a band of {{eventstudy_band_min_2016}} to {{eventstudy_band_max_2016}}). The reference year 2018 is high for Tambopata and very low for Amarakaeri. 2023 is inside the band, and 2024–25 are below it again. Pool A has only two comparison zones.

![Synthetic control attempt (not used)](output/fig_peru_synth.png)
**Reading:** [[D]] In hectares the synthetic Tambopata is about {{synth_core_add_pre_mean_synth}} ha/yr against a real {{synth_core_add_pre_mean_tam}} ha/yr before 2019, so the method fails here (pre-RMSPE {{synth_core_add_pre_rmspe}} ha). Scaled to each zone's own history the fit improves, with rank {{synth_core_addsc_rank}} of {{synth_core_addsc_n_units_ranked}}, but six units cannot carry inference.

![Displacement: sum of units vs Madre de Dios total](output/fig_peru_displacement.png)
**Reading:** [[D]] The three buffer zones together fall in 2019–21, while the department total does not.

![Amazon Mining Watch: new mining area by zone and onset year](output/fig_spatial_zones.png)
**Reading:** [[D]] By AMW, new area in the corridor falls steadily from 2019, and the Tambopata buffer zone bottoms out in 2022 and rises again. Inside the reserve AMW shows almost nothing until 2025–26 (provisional). The corridor's share of new area is unchanged ({{spz_corridor_share_2019_21:.0%}} in 2019–21, {{spz_corridor_share_2022_24:.0%}} in 2022–24).

![Inside the reserves (protected-area file) vs their buffer zones](output/fig_peru_inside_reserves.png)
**Reading:** [[D]] Mining inside Tambopata NR is small compared with its buffer zone. The one-year step in 2017 ({{anp_tam_nr_addition_2017}} ha) coincides with forest-class swaps in the same year, so it is probably partly reclassification. 2025 is the first clear rise.

![Tambopata buffer zone plus reserve](output/fig_peru_displacement_into_reserve.png)
**Reading:** [[D]] Adding the reserve to its buffer zone barely changes the picture through 2024. This assumes the buffer-zone statistics exclude the reserve, which we have not verified.

![Declared gold production vs mapped mining area, Madre de Dios](output/fig_peru_production_vs_area.png)
**Reading:** [[D]] Declared production falls from 2016 and collapses in 2020 while mapped area keeps rising. These are two sources measuring two different things, so we never divide one by the other.

![Map of Madre de Dios: zones, corridor, Amazon Mining Watch patches by onset period](output/fig_map_madre_de_dios.png)
**Reading:** [[D]] Most patches lie in the D.L. 1100 corridor and around La Pampa. The newest (2025–26, provisional) line the northern edge of Tambopata NR, where MAAP #241 reports the Malinowski incursion. The La Pampa centre is derived from the data (densest pre-2019 patch cluster in the buffer zone), not an official coordinate.

![Amazon Mining Watch: new mining area by distance ring around La Pampa](output/fig_spatial_rings.png)
**Reading:** [[D]] Within 50 km of La Pampa, new AMW area splits across the rings in the same way in 2019–21 ({{sp_lp_ring_0_10km_share_2019_21:.0f}} / {{sp_lp_ring_10_25km_share_2019_21:.0f}} / {{sp_lp_ring_25_50km_share_2019_21:.0f}} %) as in 2022–24. At this resolution we see no outward shift ring by ring.

![Brazil: Yanomami vs Munduruku vs Kayapó additions; all indigenous lands as context](output/fig_brazil_territories.png)
**Reading:** [[D]] All three territories peak in 2019–22 and fall in 2023–24. Yanomami peaks latest (2022), so its fall coincides with a fall everywhere. Only 2 post years: Collection 10.1 ends in 2024.

![Brazil: IBAMA infraction notices vs mining additions in indigenous lands](output/fig_brazil_enforcement.png)
**Reading:** [[D]] Total notices dip in 2019–22 while mining additions surge. Mining-flagged notices (a noisy text match) do not dip.

![Brazil: DETER monthly mining alerts per territory](output/fig_brazil_deter_monthly.png)
**Reading:** [[D]] Yanomami alerts spike in Mar–Apr 2023, during the operation, then fade. Munduruku and Kayapó alerts had already fallen in mid-2022, before any 2023 action. Alerts are dated by detection, not by when the clearing happened.

![Brazil: Roraima municipalities around Yanomami](output/fig_brazil_roraima.png)
**Reading:** [[D]] Roraima's mapped mining is almost all inside the Yanomami territory, so there is no visible spill into the rest of the state.

![Map: Yanomami, Munduruku, Kayapó with Amazon Mining Watch patches](output/fig_map_yanomami.png)
**Reading:** [[D]] The patches lie mostly inside the territories.

## 6. Numbers table

{{NUMBERS_TABLE}}

## 7. Open problems

- **Publisher-side check numbers.** Peru protected areas match the MapBiomas platform (777 ha). The Brazil per-territory file (Col 10.1) has **no** publisher match: the platform shows only Collection 11 (Kayapó 2024 = 17,632 ha against 18,176 ha), and no Collection 11 per-territory file has been published. For the brief, use the pack's Col 11 all-territories number (39,915 ha) as the Brazil check, and state the per-territory mismatch openly. IBAMA shows no totals on its site. MAAP pages could only be saved as rendered text, so a human must use "Save as".
- **Parallel trends are not supported in Peru.** The 2016 event-study coefficient is as large as the post-period ones. The DiD of {{did_main}} ha/yr is a description of different changes, not an effect.
- **One treated unit per country.** Standard errors are not informative (Conley & Taber 2011). Placebo-in-space has only {{placebo_space_n_restricted}} meaningful Peruvian zones, and the synthetic control fails because Tambopata is outside the donor range.
- **Partly treated controls.** Amarakaeri had its own interventions (Camanti decline in MAAP #130; Huepetuhe under the 2023 emergency). Munduruku had operations from Aug 2023 and Nov 2024. Kayapó's formal operation began May 2025, after the data end (from search snippets, so verify).
- **Spillovers bias the Peru DiD away from zero.** If miners moved from Tambopata into Amarakaeri, the control rises because of the treatment.
- **Confounders:** COVID-19 (2020), the gold price ({{gold_price_ratio_2025_2018:.1f}}× from 2018 to 2025) and further enforcement waves (Restauración 2021, emergency 2023) all overlap the post-period.
- **"Rest of Madre de Dios" mixes legal and illegal mining** (the D.L. 1100 corridor holds 74% of 2021–24 mining deforestation per MAAP #208). It is also slightly understated because buffer zones overlap: the largest overlap is {{bz_overlap_max_ha}} ha, Tambopata/Bahuaja-Sonene, where mining is small.
- **Sources disagree.** MapBiomas shows a regional surge after 2022, while AMW shows the corridor falling. For Yanomami in 2023, DETER alerts rise while the annual maps fall. We report both sides and choose neither.
- **Measurement:** MapBiomas "mining" covers legal and illegal mining and any mineral. Additions include re-mining and reclassification (Tambopata NR 2017). Satellites do not see **river dredges** or **mercury**. MAAP #193 counts 148 → 598 dredges in La Pampa (Aug 2021 → Aug 2023) on already-degraded land, which a "new area" measure misses. Cite the counts: the page's "more than 400%" is really +304%.
- **Brazil scale problem:** the DiD sign flips between hectares and % of stock. A placebo ≠ 0 shows the pre-trends differ. Pooled controls are per-unit means; the older SUM versions in numbers.csv are marked "do not cite".
- **IBAMA mining flag** is a free-text regex and has not been checked by hand. The embargo file is BLOCKED.
- **AMW** onset_year 2018 is a stock, not an addition. Its 480 m patches overstate area. 2025–26 values are provisional.

## 8. Next steps

{{NEXT_STEPS_DIAGRAM}}

## 9. Brief skeleton (draft)

**Part 1. The question (~½ page).** FZS supports SERNANP's enforcement against alluvial gold mining in the Tambopata–Bahuaja-Sonene landscape (FZS programme page). Operations are expensive and temporary. FZS needs to know what happens in the targeted area, and around it, when one ends. Our question: *after Operation Mercurio (Feb 2019), did mining in the Tambopata buffer zone fall, move, or wait?* Places: Tambopata buffer zone (targeted) vs Amarakaeri buffer zone (comparison), plus the reserve itself and the rest of Madre de Dios. Years 2014–2025. Brazil (Yanomami, Feb 2023) as a second, shorter case.

**Part 2. Data and provenance (~¼ page).** MapBiomas Peru Collection 4 (buffer zones; protected areas), annual mining area, class 4.2. Checks: Tambopata buffer zone 2025 = 20,730 ha; Tambopata NR 2025 = 777 ha on the MapBiomas platform. MapBiomas Brazil Collection 11 (all indigenous lands) check: 39,915 ha in 2025. Collection 10.1 per territory: {{CHECK_BRAZIL_TI_SHORT}}. World Bank Pink Sheet gold price check: Aug 2026 = $4,411/oz. One check per dataset, logged in DOWNLOAD_LOG.csv.

**Part 3. Findings (one figure).** Use `output/fig_brief_main.png`. Text, every sentence [[D]]: Tambopata {{mean_add_tambopata_2016_18}} → {{mean_add_tambopata_2019_21}} ha/yr vs Amarakaeri {{mean_add_amarakaeri_2016_18}} → {{mean_add_amarakaeri_2019_21}} (difference of changes {{did_main}}); placebo 2016 {{did_placebo}}; department total {{mean_add_mdd_total_2016_18}} → {{mean_add_mdd_total_2019_21}} → {{mean_add_mdd_total_2022_25}}; Tambopata 2022–25 {{mean_add_tambopata_2022_25}} ({{mean_add_tambopata_2022_25_ex2023}} without 2023); reserve core +{{anp_tam_nr_addition_2025}} ha in 2025. Allow at most one causal sentence, stated conditionally and with its failure: "If Amarakaeri had moved in parallel, this would be a fall of ~1,760 ha/yr. But the 2016 pre-period already differs by as much, so we do not claim it."

**Part 4. What FZS can do with this.** (a) [[P]] Expect a local fall that lasts only while the presence lasts, no fall in the region, and pressure on the reserve core. Plan for permanent presence at the edges of the core (cf. the 2025 navy withdrawal on the Malinowski, MAAP #241), and monitor the next-nearest unprotected land. (b) Why it could mislead: one treated unit; parallel trends fail; spillovers into the control; COVID and the gold price; the sources disagree; MapBiomas cannot tell legal from illegal mining; river dredging and mercury are invisible. (c) What would let us say more: dated enforcement records (patrol days, interdictions per zone) from SERNANP/FZS; more treated units (Plan Restauración zones 2021); AMW quarterly patches in distance rings; river-dredge counts (MAAP-style SkySat); mercury sampling. Put the required AI-prompt output in the appendix, raw and edited.
