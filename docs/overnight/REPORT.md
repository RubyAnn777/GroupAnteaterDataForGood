# Overnight analysis report: how does mining move with enforcement?

> For the team (Group Giant Anteater, Question 2, Peru + Brazil). Produced overnight on 10/11 Oct 2026 on branch `analysis/overnight-2026-10-10` by Claude, an AI assistant, and its subagents. Every number below is read from `output/numbers.csv`, which `uv run python code/main.py` writes. An adversarial review pass (`docs/overnight/notes/review.md`) was applied, but nothing here is checked by a human yet. Read it critically, re-open every source you cite, and treat every claim tag as a proposal. This report is not a source for the brief. The sources are.

## 1. Summary of findings

**What FZS asked:** what to expect in the targeted area, and around it, when an enforcement operation ends.

**Short answer from our data** **[description]**: Where Mercurio hit (the Tambopata buffer zone), new mining fell sharply in 2019–21 and was back near or above its 2016–18 level in 2022–25. Over the same years the nearby Amarakaeri buffer zone and the rest of Madre de Dios rose. From this data we cannot tell whether that rise is displacement, COVID, the gold price or legal corridor mining. The prediction for FZS is in the box at the end of this section.

**Peru (Operation Mercurio, Feb 2019)**

1. **[description]** New mining in the **Tambopata buffer zone** (where La Pampa lies) fell from 1,640 ha/yr (2016–18) to 163 ha/yr (2019–21). In the **Amarakaeri buffer zone** it rose from 289 to 574 ha/yr. These four period means reproduce the question card. Their difference of changes is **−1,762 ha/yr**, matching the starter. With a 2014–18 baseline it is −1,663 ha/yr. The 2016–18 "before" period already includes the 2017–18 interdictions (MAAP #241), so it is not enforcement-free.
2. **[description]** No other buffer zone with real mining fell as much. Among the 6 Amazon buffer zones with more than 10 ha/yr of pre-2019 additions, Tambopata has the most negative 2019–21 coefficient (rank 1). With so few peers this is "no comparable zone fell", not a significance test. A fake operation in 2016 gives 209 ha/yr. The event study, however, shows a 2016 coefficient (−1,195 ha) as far outside the placebo band as the post-2019 ones, so the parallel-trends assumption behind any causal reading is **not supported**.
3. **[description]** **The region did not fall.** New mining in all of Madre de Dios was 3,610 → 4,640 → 12,049 ha/yr (2016–18 / 2019–21 / 2022–25). Most of it lies outside the buffer zones ("rest of Madre de Dios": 1,688 → 3,937 → 9,020 ha/yr). This fits displacement, but it fits COVID, the gold price, legal corridor mining and REINFO formalisation just as well. MAAP #208 finds that 74% of 2021–24 mining deforestation in Madre de Dios lay inside the official mining corridor. A second product, Amazon Mining Watch, does **not** show the rise: its new patch area in the corridor falls from 44,716 ha (2019–21) to 32,339 ha (2022–24). The regional rise therefore rests on MapBiomas alone.
4. **[description]** **Return:** Tambopata's annual additions after 2021 were 580 (2022), 3,565 (2023), 1,276 and 1,896 ha (2024–25). The 2022–25 mean (1,829 ha/yr) is above 2016–18, but only because of 2023, a year when every unit spiked (Amarakaeri 2,099, rest of Madre de Dios 13,676 ha). Without 2023 the mean is 1,251 ha/yr, below the pre-Mercurio level. The 2023 spike falls inside the state of emergency (from 7 Apr 2023), so "mining came back when enforcement ended" is too simple.
5. **[description]** **Inside the reserve itself** (new file: MapBiomas Peru protected-area statistics), mining in Tambopata National Reserve is small but growing: 777 ha in 2025, of which 241 ha was added in 2025 alone. Two differently built products point the same way. MAAP #241 reports 500 ha of new mining inside the reserve (H2 2025 to Feb 2026). Amazon Mining Watch first detects 209 ha inside the reserve over 2019–24 combined, then 640 ha in 2025 alone (provisional). The three measure different things, so we compare only their direction, never their hectares.
6. **[description]** Declared (formal) gold production in Madre de Dios fell by 88% between 2018 and 2025, while mapped mining area more than doubled (50,506 → 112,622 ha). Production was already falling before Mercurio (16.2 t in 2016, 10.1 t in 2018). The steepest drop was 2019 → 2020, the COVID year (79%). Either more gold left undeclared, or reporting and formalisation rules changed. We cannot tell which.
7. **[description]** A synthetic control for Tambopata **does not work**. Tambopata adds far more mining than any donor zone (outside the donor range in 9 of 9 pre-years), so no weighted mix of donors reproduces its history. We report the attempt in §5 and do not use it.

**Brazil (weak enforcement 2019–22, Yanomami operation Feb 2023)**

8. **[description]** Total IBAMA infraction notices in the Legal Amazon averaged 6,920 per year in 2015–18 and 4,359 in 2019–22, then 7,907 in 2023. This matches the documented fall in federal enforcement: embargoes −59% and confiscations −55% in 2019–2020 (Nunes et al. 2024). Notices that our text match flags as mining-related **did not fall** (157 → 148 per year, a noisy count). Over the same periods, new artisanal mining in all indigenous lands combined went 1,332 → 4,319 → 2,978 ha/yr (2016–18 / 2019–22 / 2023–25). The fit with weaker enforcement is plausible, but this data does not show it.
9. **[description]** New mining in the **Yanomami** territory fell from 1,617 ha (2022) to 824 (2023) and 179 ha (2024), per MapBiomas Collection 10.1. **Kayapó** and **Munduruku** also fell, so the 2×2 comparison (2020–22 vs 2023–24) is inconclusive. In hectares, Yanomami fell *less* than Kayapó (+905 ha/yr), the opposite of an operation effect. Relative to each territory's 2022 stock it fell more (−4.4 pp). A fake 2020 start already gives −355 ha/yr. The sources also disagree on 2023: DETER mining alerts in Yanomami *rose* in the 12 months after Feb 2023 (1.9 → 4.7 km²), while the annual maps fell. Alerts are dated by detection, and the operation itself may have revealed sites.
10. **[description]** We see no growth in mapped mining in the rest of Roraima (96% of Roraima's mining is inside the Yanomami territory; the rest changed by +19 ha in 2023–24). That tests only one narrow channel. Miners can also move to Venezuela, Amazonas or Pará. The 19 smaller mining territories together added 523 → 560 ha/yr, and one of them, Sararé, accounts for +831 ha of the 2023–24 additions. Without Sararé the other 18 fell (per territory, 29 → 8 ha/yr).

> **What FZS can take from this** **[prediction]** (prediction from two cases, one treated unit each; not a causal estimate): when an operation targets one hotspot, expect a sharp local fall while the presence lasts. Nearby, less protected land does not fall and may rise. The local fall can reverse within a few years, as Tambopata did from 2022, but how fast depends on one spike year (2023). In Peru the protected core is now being entered (2025). Brazil's 2023 fall happened in every large territory at once, so it says more about national enforcement than about one operation.

## 2. Data obtained

| Source | File (data_raw/ unless noted) | Years | Check number | Status |
|---|---|---|---|---|
| MapBiomas Peru, Collection 4, buffer zones (pack) | data/peru_bufferzone_year.csv | 1985–2025 | Tambopata BZ 2025 = 20,730 ha (card; platform also shows 20,730 ha) | OK |
| MapBiomas Peru, Collection 4, departments (pack) | data/peru_department_year.csv | 1985–2025 | Madre de Dios 2025 = 112,622 ha | OK |
| MapBiomas Peru, Collection 4, **protected areas** (new) | mapbiomas_peru/MAPBIOMAS-PERU-LULC-COL4-AREAS-PROTEGIDAS.xlsx | 1985–2025 | Tambopata NR mining 2025 = 776.9 ha; MapBiomas platform shows 777 ha (screenshot) | OK |
| MapBiomas Brazil, Collection 10.1, **indigenous territories** (new) | mapbiomas_brazil/MAPBIOMAS_BRAZIL-COVERAGE_STATISTICS-COL.10.1-INDIGENOUS_TERRITORIES_STATE_BIOME.xlsx | 1985–2024 | Kayapó 2024 = 18,176 ha; Col 10 file agrees within 0.07% (2018+) | MISMATCH by collection: platform shows only Collection 11 (Kayapó 2024 = 17,632 ha) vs 18,176 ha in our Col 10.1 file; no Col 11 per-territory file published (checked 2026-10-11) |
| MapBiomas Brazil, Collection 11, mining (pack) | data/mining_area.csv | 1985–2025 | All TIs artisanal 2025 = 39,915 ha (card) | OK (Brazil publisher check) |
| MapBiomas Brazil, Collection 10.1, municipalities (pack) | data/brazil_municipality_year.csv | 1985–2024 | Roraima 2018 = 446 ha, 2024 = 4,745 ha | OK |
| IBAMA open data, autos de infração (new) | ibama/auto_infracao_csv.zip (117 MB, git-ignored; small intermediate in data_intermediate/) | 1977–2026 | IBAMA's site shows no total; file integrity only | data OK / check BLOCKED |
| IBAMA embargoes | – | – | – | BLOCKED (no download URL found) |
| INPE TerraBrasilis DETER, class MINERACAO (new) | inpe_deter/deter_amz_mineracao.geojson | 2016–2026 | 2019 = 105.64 km² vs dashboard 105.40 km² | OK (0.2% domain difference) |
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

| # | Decision | Alternatives | Why |
|---|---|---|---|
| D1 | Subagents never edit DOWNLOAD_LOG.csv or commit; they write draft rows to `docs/overnight/notes/*_rows.csv`, the orchestrator merges and commits. | Each agent edits the log | Avoid merge conflicts between parallel agents |
| D2 | Pack-based Peru analysis (phase 2/3) starts in parallel with the downloads; new datasets plug in later as separate modules. | Wait for downloads | The core Peru design only needs `data/` |
| D3 | User (23:50) allows any additional public data source that adds value, esp. for figures; same provenance rules (log row, check number, cite publisher). Launched a data-scout agent. | Pack + listed sources only | User instruction |
| D4 | Peru buffer-zone units = sum over ALL department rows (Amarakaeri has a Cusco row, Tambopata a Puno row). Reproduces the card (1,640→163, 289→574, DiD −1,762); agent.md §10's 1,638/284 were MdD rows only. | MdD rows only | The card's check numbers are the reference |
| D5 | Event-study pool A = Tambopata + Amarakaeri + Bahuaja-Sonene BZ (MdD zones with non-zero 2014–18 additions); pool B = all 15 Peruvian BZ with pre-2019 additions (robustness/placebo donors). Inference by placebo-in-space rank, not clustered SEs (one treated unit). | Clustered SEs | Conley–Taber: with one treated cluster SEs are uninformative |
| D6 | Event markers: event in year Y drawn at x = Y − 0.5 (before the first annual addition that can reflect it). | Calendar position | addition(Y) = map(Y) − map(Y−1) |
| D7 | IBAMA zip (123 MB) git-ignored; code/brazil_ibama.py rebuilds a small committed intermediate `data_intermediate/ibama_autos_annual.csv` when the zip is present, else reads it. | Commit zip / skip | Keeps replication possible without a >50 MB file in git |
| D8 | Brazil per-territory = MapBiomas Col 10.1 class 4.3 (all mining; no garimpo/substance split per territory exists). Pack all-TIs series (Col 11, artisanal) kept as a separate panel, never in one series. | Mix collections | Rule 7 |
| D9 | Brazil best control 2023–24 = Kayapó (only light action, formal desintrusão May 2025, after data end); Munduruku partly treated (operation Aug 2023, desintrusão Nov 2024). | Pool both | Enforcement timeline evidence |
| D10 | Extra datasets added: INPE DETER mining alerts (monthly, per TI via FUNAI polygons) and BCRP/MINEM declared gold production Madre de Dios. GFW skipped (API key). | More sources | Monthly resolution around Feb 2023; formal vs mapped mining contrast |
| D11 | Brazil 2×2 DiD reported in ha/yr AND relative to 2022 stock; sign flips → reported as inconclusive. | One metric | Units differ ~4× in size; honest reporting |

## 5. Figures

![The brief's one figure: new mining area per year, Tambopata and Amarakaeri buffer zones, Tambopata National Reserve, Madre de Dios total and rest](../../output/fig_brief_main.png)
**Reading:** **[description]** Tambopata's additions fall after Mercurio (Feb 2019) and return from 2022; Amarakaeri and the rest of Madre de Dios rise. Description only.

![Proposed brief figure: Tambopata BZ vs Amarakaeri BZ vs inside Tambopata NR; Madre de Dios total and rest](../../output/fig_brief_main.png)
**Reading:** **[description]** Tambopata's additions drop in 2019–21 and return from 2022. Amarakaeri and the rest of the department rise. Inside the reserve stays near zero until 2025.

![Peru: annual additions by buffer zone, Madre de Dios total and rest, and the gold price](../../output/fig_peru_additions.png)
**Reading:** **[description]** All series jump in 2023. The gold price rose 2.7× between 2018 and 2025, but only 8% in 2023 itself, so the price alone does not explain that year's spike.

![Event study: Tambopata vs comparison zones, 2018 = 0](../../output/fig_peru_event_study.png)
**Reading:** **[description]** The 2019–22 coefficients sit far below the placebo band, but so does 2016 (−1,195 ha against a band of 10 to 389). The reference year 2018 is high for Tambopata and very low for Amarakaeri. 2023 is inside the band, and 2024–25 are below it again. Pool A has only two comparison zones.

![Synthetic control attempt (not used)](../../output/fig_peru_synth.png)
**Reading:** **[description]** In hectares the synthetic Tambopata is about 32 ha/yr against a real 1,375 ha/yr before 2019, so the method fails here (pre-RMSPE 1,467 ha). Scaled to each zone's own history the fit improves, with rank 1 of 6, but six units cannot carry inference.

![Displacement: sum of units vs Madre de Dios total](../../output/fig_peru_displacement.png)
**Reading:** **[description]** The three buffer zones together fall in 2019–21, while the department total does not.

![Amazon Mining Watch: new mining area by zone and onset year](../../output/fig_spatial_zones.png)
**Reading:** **[description]** By AMW, new area in the corridor falls steadily from 2019, and the Tambopata buffer zone bottoms out in 2022 and rises again. Inside the reserve AMW shows almost nothing until 2025–26 (provisional). The corridor's share of new area is unchanged (66% in 2019–21, 67% in 2022–24).

![Inside the reserves (protected-area file) vs their buffer zones](../../output/fig_peru_inside_reserves.png)
**Reading:** **[description]** Mining inside Tambopata NR is small compared with its buffer zone. The one-year step in 2017 (534 ha) coincides with forest-class swaps in the same year, so it is probably partly reclassification. 2025 is the first clear rise.

![Tambopata buffer zone plus reserve](../../output/fig_peru_displacement_into_reserve.png)
**Reading:** **[description]** Adding the reserve to its buffer zone barely changes the picture through 2024. This assumes the buffer-zone statistics exclude the reserve, which we have not verified.

![Declared gold production vs mapped mining area, Madre de Dios](../../output/fig_peru_production_vs_area.png)
**Reading:** **[description]** Declared production falls from 2016 and collapses in 2020 while mapped area keeps rising. These are two sources measuring two different things, so we never divide one by the other.

![Map of Madre de Dios: zones, corridor, Amazon Mining Watch patches by onset period](../../output/fig_map_madre_de_dios.png)
**Reading:** **[description]** Most patches lie in the D.L. 1100 corridor and around La Pampa. The newest (2025–26, provisional) line the northern edge of Tambopata NR, where MAAP #241 reports the Malinowski incursion. The La Pampa centre is derived from the data (densest pre-2019 patch cluster in the buffer zone), not an official coordinate.

![Amazon Mining Watch: new mining area by distance ring around La Pampa](../../output/fig_spatial_rings.png)
**Reading:** **[description]** Within 50 km of La Pampa, new AMW area splits across the rings in the same way in 2019–21 (8 / 22 / 70 %) as in 2022–24. At this resolution we see no outward shift ring by ring.

![Brazil: Yanomami vs Munduruku vs Kayapó additions; all indigenous lands as context](../../output/fig_brazil_territories.png)
**Reading:** **[description]** All three territories peak in 2019–22 and fall in 2023–24. Yanomami peaks latest (2022), so its fall coincides with a fall everywhere. Only 2 post years: Collection 10.1 ends in 2024.

![Brazil: IBAMA infraction notices vs mining additions in indigenous lands](../../output/fig_brazil_enforcement.png)
**Reading:** **[description]** Total notices dip in 2019–22 while mining additions surge. Mining-flagged notices (a noisy text match) do not dip.

![Brazil: DETER monthly mining alerts per territory](../../output/fig_brazil_deter_monthly.png)
**Reading:** **[description]** Yanomami alerts spike in Mar–Apr 2023, during the operation, then fade. Munduruku and Kayapó alerts had already fallen in mid-2022, before any 2023 action. Alerts are dated by detection, not by when the clearing happened.

![Brazil: Roraima municipalities around Yanomami](../../output/fig_brazil_roraima.png)
**Reading:** **[description]** Roraima's mapped mining is almost all inside the Yanomami territory, so there is no visible spill into the rest of the state.

![Map: Yanomami, Munduruku, Kayapó with Amazon Mining Watch patches](../../output/fig_map_yanomami.png)
**Reading:** **[description]** The patches lie mostly inside the territories.

## 6. Numbers table

All 418 numbers, with unit, description, claim type and producing function: [`output/numbers.csv`](../../output/numbers.csv). Headline numbers used in section 1:

| id | value | unit | description |
|---|---:|---|---|
| `mean_add_tambopata_2016_18` | 1,640 | ha/yr | Mean annual addition to mining area, Tambopata, 2016-18 |
| `mean_add_tambopata_2019_21` | 162.5 | ha/yr | Mean annual addition to mining area, Tambopata, 2019-21 |
| `mean_add_amarakaeri_2016_18` | 289.2 | ha/yr | Mean annual addition to mining area, Amarakaeri, 2016-18 |
| `mean_add_amarakaeri_2019_21` | 573.8 | ha/yr | Mean annual addition to mining area, Amarakaeri, 2019-21 |
| `did_main` | −1,762 | ha/yr | DiD of mean annual additions, Tambopata minus Amarakaeri, Main: Tambopata vs Amarakaeri. Descriptive contrast of changes; not causal (spillovers, COVID, gold price, further enforcement waves). |
| `did_main_base_2014_18` | −1,663 | ha/yr | DiD of mean annual additions, Tambopata minus Amarakaeri, baseline 2014-18 vs 2019-21 (longer baseline than the main 2016-18; shows sensitivity to Amarakaeri's low 2016-18 level). Descriptive; not causal. |
| `placebo_space_n_restricted` | 6 | count | Number of units (Tambopata + donors) in the restricted placebo-in-space pool; minimum possible rank share is 1/6 |
| `placebo_space_rank_restricted` | 1 | rank | Rank of Tambopata among 6 buffer zones (itself + 5 donors with mean 2014-18 additions > 10 ha/yr in Amazon-biome departments; 1 = most negative) in mean event-study beta 2019-21. Donors: Allpahuayo Mishana; Amarakaeri; Bahuaja-Sonene; de Junín; del Río Abiseo. See output/peru_placebo_in_space_restricted.csv |
| `did_placebo` | 208.7 | ha/yr | DiD of mean annual additions, Tambopata minus Amarakaeri, Placebo: fake operation in 2016 (no real-treatment years in window). Descriptive contrast of changes; not causal (spillovers, COVID, gold price, further enforcement waves). |
| `eventstudy_pretrend_poolA_2016` | −1,195 | ha | Event-study pre-period coefficient 2016 (ref 2018), pool A |
| `mean_add_mdd_total_2016_18` | 3,610 | ha/yr | Mean annual addition to mining area, Madre de Dios total, 2016-18 |
| `mean_add_mdd_total_2019_21` | 4,640 | ha/yr | Mean annual addition to mining area, Madre de Dios total, 2019-21 |
| `mean_add_mdd_total_2022_25` | 12,049 | ha/yr | Mean annual addition to mining area, Madre de Dios total, 2022-25 |
| `mean_add_rest_mdd_2016_18` | 1,688 | ha/yr | Mean annual addition to mining area, Rest of Madre de Dios, 2016-18 |
| `mean_add_rest_mdd_2019_21` | 3,937 | ha/yr | Mean annual addition to mining area, Rest of Madre de Dios, 2019-21 |
| `mean_add_rest_mdd_2022_25` | 9,020 | ha/yr | Mean annual addition to mining area, Rest of Madre de Dios, 2022-25 |
| `spz_corridor_ha_2019_21` | 44,716 | ha | AMW new mining area in the DL 1100 corridor 2019-2021 (sum) |
| `spz_corridor_ha_2022_24` | 32,339 | ha | AMW new mining area in the DL 1100 corridor 2022-2024 (sum) |
| `add_tambopata_2022` | 580.2 | ha | Annual addition to mining area, Tambopata BZ, 2022 |
| `add_tambopata_2023` | 3,565 | ha | Annual addition to mining area, Tambopata BZ, 2023 |
| `add_tambopata_2024` | 1,276 | ha | Annual addition to mining area, Tambopata BZ, 2024 |
| `add_tambopata_2025` | 1,896 | ha | Annual addition to mining area, Tambopata BZ, 2025 |
| `mean_add_tambopata_2022_25` | 1,829 | ha/yr | Mean annual addition to mining area, Tambopata, 2022-25 |
| `add_amarakaeri_2023` | 2,099 | ha | Annual addition to mining area, Amarakaeri BZ, 2023 |
| `add_rest_mdd_2023` | 13,676 | ha | Annual addition to mining area, rest of Madre de Dios (dept. minus MdD buffer-zone rows), 2023 |
| `mean_add_tambopata_2022_25_ex2023` | 1,251 | ha/yr | Mean annual addition, Tambopata BZ, 2022, 2024 and 2025 (2023 excluded: a year in which every unit spiked) |
| `anp_level_tam_nr_2025` | 776.9 | ha | Mining area inside Tambopata NR, 2025 |
| `anp_tam_nr_addition_2025` | 241.1 | ha | Addition inside Tambopata NR in 2025 (cf. MAAP #241 ~500 ha H2 2025-Feb 2026; different source/period, not subtracted) |
| `sp_amw_tambopata_nr_new_ha_2019_2024` | 208.9 | ha | AMW new area inside Tambopata NR, sum of onset years 2019-2024 (confirmed) |
| `sp_amw_tambopata_nr_new_ha_2025` | 640.1 | ha | AMW area with first detection in 2025 inside Tambopata National Reserve (AMW model hectares, not MapBiomas) PROVISIONAL |
| `pe_prod_fall_2018_2025_pct` | 87.8 | % | Fall in declared production 2018 to 2025, as a positive percentage |
| `pe_prod_mapbiomas_level_2018_ha` | 50,506 | ha | MapBiomas mining area level, Madre de Dios (Amazonía), 2018 |
| `pe_prod_mapbiomas_level_2025_ha` | 112,622 | ha | MapBiomas mining area level, Madre de Dios (Amazonía), 2025 (matches 112,622 ha check) |
| `pe_prod_2016_t` | 16.2 | t fine gold | Declared gold production, Madre de Dios, 2016 |
| `pe_prod_2018_t` | 10.1 | t fine gold | Declared gold production, Madre de Dios, 2018 (year before Mercurio) |
| `pe_prod_fall_2019_2020_pct` | 79.4 | % | Fall in declared production 2019 to 2020 (COVID year), as a positive percentage |
| `synth_core_add_hull_years_outside` | 9 | years of 9 | Synthetic control [core_add]: fit-window years where Tambopata lies outside the donors' min-max range (convex-hull problem) |
| `br_ibama_aml_mean_2015_2018` | 6,920 | autos/yr | Mean IBAMA autos per year, Legal Amazon states, 2015-2018 (IBAMA open data, autos de infracao (non-cancelled), Legal Amazon states) |
| `br_ibama_aml_mean_2019_2022` | 4,359 | autos/yr | Mean IBAMA autos per year, Legal Amazon states, 2019-2022 (IBAMA open data, autos de infracao (non-cancelled), Legal Amazon states) |
| `br_ibama_aml_2023` | 7,907 | autos | IBAMA autos, Legal Amazon states, 2023 |
| `br_ibama_mining_aml_mean_2015_2018` | 157 | autos/yr | Mean mining-flagged IBAMA autos (noisy regex), Legal Amazon, 2015-2018 |
| `br_ibama_mining_aml_mean_2019_2022` | 147.5 | autos/yr | Mean mining-flagged IBAMA autos (noisy regex), Legal Amazon, 2019-2022 |
| `br_pack_art_add_mean_2016_2018` | 1,332 | ha/yr | Mean annual addition, artisanal mining, all indigenous lands combined, 2016-2018 (MapBiomas Brazil, Collection 11, all indigenous lands combined (artisanal mining)) |
| `br_pack_art_add_mean_2019_2022` | 4,319 | ha/yr | Mean annual addition, artisanal mining, all indigenous lands combined, 2019-2022 (MapBiomas Brazil, Collection 11, all indigenous lands combined (artisanal mining)) |
| `br_pack_art_add_mean_2023_2025` | 2,978 | ha/yr | Mean annual addition, artisanal mining, all indigenous lands combined, 2023-2025 (MapBiomas Brazil, Collection 11, all indigenous lands combined (artisanal mining)) |
| `br_ti_yanomami_add_2022` | 1,617 | ha | Addition Yanomami 2022 (MapBiomas Brazil, Collection 10.1, Indigenous Territories (class 4.3 Mining, all mining)) |
| `br_ti_yanomami_add_2023` | 824.2 | ha | Addition Yanomami 2023 (MapBiomas Brazil, Collection 10.1, Indigenous Territories (class 4.3 Mining, all mining)) |
| `br_ti_yanomami_add_2024` | 178.6 | ha | Addition Yanomami 2024 (MapBiomas Brazil, Collection 10.1, Indigenous Territories (class 4.3 Mining, all mining)) |
| `br_did_main_vs_Kayapo_ha_yr` | 904.8 | ha/yr | Descriptive DiD in mean annual additions: Yanomami vs Kayapo, 2020-2022 -> 2023-2024 (MapBiomas Brazil, Collection 10.1, Indigenous Territories (class 4.3 Mining, all mining)) |
| `br_did_main_vs_Kayapo_pct` | −4.37 | pp of 2022 stock | Same, additions as % of 2022 stock |
| `br_did_placebo_time_start_2020_ha_yr` | −354.9 | ha/yr | Descriptive DiD in mean annual additions: Yanomami vs Kayapo, 2017-2019 -> 2020-2022 (MapBiomas Brazil, Collection 10.1, Indigenous Territories (class 4.3 Mining, all mining)) |
| `br_deter_yan_12m_before_feb2023_km2` | 1.9 | km2 | DETER mining alert area, Yanomami, Feb 2022-Jan 2023 (12 months before the Feb 2023 Yanomami operation) |
| `br_deter_yan_12m_after_feb2023_km2` | 4.71 | km2 | DETER mining alert area, Yanomami, Feb 2023-Jan 2024 (12 months from the Feb 2023 Yanomami operation; the date is not a Munduruku/Kayapo event) |
| `br_rr_yanomami_share_2024` | 96.4 | % | Yanomami TI stock as share of Roraima municipal stock 2024 |
| `br_rr_outside_yanomami_add_2023_24` | 19.3 | ha | Change 2022 to 2024 in Roraima mining outside the Yanomami TI (Roraima stock minus TI stock) |
| `br_other19_add_mean_2020_2022` | 523.5 | ha/yr | Mean annual addition, 19 other territories with mining, 2020-2022 (MapBiomas Brazil, Collection 10.1, Indigenous Territories (class 4.3 Mining, all mining)) |
| `br_other19_add_mean_2023_2024` | 560.5 | ha/yr | Mean annual addition, 19 other territories with mining, 2023-2024 (MapBiomas Brazil, Collection 10.1, Indigenous Territories (class 4.3 Mining, all mining)) |
| `br_sarare_add_2023_24_sum` | 831.4 | ha | Sum of additions 2023+2024, Sararé (geocode 42101) |
| `br_other18_ex_sarare_add_mean_2020_2022` | 29.0 | ha/yr | Per-unit MEAN annual addition of the 18 other territories with mining excluding Sararé (geocode 42101), 2020-2022; each territory's addition averaged over the group, then over years (MapBiomas Brazil, Collection 10.1, Indigenous Territories (class 4.3 Mining, all mining)) |
| `br_other18_ex_sarare_add_mean_2023_2024` | 8.04 | ha/yr | Per-unit MEAN annual addition of the 18 other territories with mining excluding Sararé (geocode 42101), 2023-2024; each territory's addition averaged over the group, then over years (MapBiomas Brazil, Collection 10.1, Indigenous Territories (class 4.3 Mining, all mining)) |

## 7. Open problems

- **Publisher-side check numbers.** Peru protected areas match the MapBiomas platform (777 ha). The Brazil per-territory file (Col 10.1) has **no** publisher match: the platform shows only Collection 11 (Kayapó 2024 = 17,632 ha against 18,176 ha), and no Collection 11 per-territory file has been published. For the brief, use the pack's Col 11 all-territories number (39,915 ha) as the Brazil check, and state the per-territory mismatch openly. IBAMA shows no totals on its site. MAAP pages could only be saved as rendered text, so a human must use "Save as".
- **Parallel trends are not supported in Peru.** The 2016 event-study coefficient is as large as the post-period ones. The DiD of −1,762 ha/yr is a description of different changes, not an effect.
- **One treated unit per country.** Standard errors are not informative (Conley & Taber 2011). Placebo-in-space has only 6 meaningful Peruvian zones, and the synthetic control fails because Tambopata is outside the donor range.
- **Partly treated controls.** Amarakaeri had its own interventions (Camanti decline in MAAP #130; Huepetuhe under the 2023 emergency). Munduruku had operations from Aug 2023 and Nov 2024. Kayapó's formal operation began May 2025, after the data end (from search snippets, so verify).
- **Spillovers bias the Peru DiD away from zero.** If miners moved from Tambopata into Amarakaeri, the control rises because of the treatment.
- **Confounders:** COVID-19 (2020), the gold price (2.7× from 2018 to 2025) and further enforcement waves (Restauración 2021, emergency 2023) all overlap the post-period.
- **"Rest of Madre de Dios" mixes legal and illegal mining** (the D.L. 1100 corridor holds 74% of 2021–24 mining deforestation per MAAP #208). It is also slightly understated because buffer zones overlap: the largest overlap is 42,310 ha, Tambopata/Bahuaja-Sonene, where mining is small.
- **Sources disagree.** MapBiomas shows a regional surge after 2022, while AMW shows the corridor falling. For Yanomami in 2023, DETER alerts rise while the annual maps fall. We report both sides and choose neither.
- **Measurement:** MapBiomas "mining" covers legal and illegal mining and any mineral. Additions include re-mining and reclassification (Tambopata NR 2017). Satellites do not see **river dredges** or **mercury**. MAAP #193 counts 148 → 598 dredges in La Pampa (Aug 2021 → Aug 2023) on already-degraded land, which a "new area" measure misses. Cite the counts: the page's "more than 400%" is really +304%.
- **Brazil scale problem:** the DiD sign flips between hectares and % of stock. A placebo ≠ 0 shows the pre-trends differ. Pooled controls are per-unit means; the older SUM versions in numbers.csv are marked "do not cite".
- **IBAMA mining flag** is a free-text regex and has not been checked by hand. The embargo file is BLOCKED.
- **AMW** onset_year 2018 is a stock, not an addition. Its 480 m patches overstate area. 2025–26 values are provisional.

## 8. Next steps

| Step | Lane | Owner (role) | Missing data |
|---|---|---|---|
| 1. Re-open every cited source and save MAAP pages with "Save as" | Now (before Lesson 4) | each citer | raw MAAP HTML |
| 2. Agree the brief figure (fig_brief_main) and the claim wording | Now (before Lesson 4) | whole team | none |
| 3. Brazil: switch per-territory series to MapBiomas Collection 11 if available (3 post years, publisher match) | Now (before Lesson 4) | Brazil analyst | Col 11 TI file |
| 4. Run the required AI prompt for brief part 4; keep raw + edited | Before Lesson 5 | writer | none |
| 5. Write brief parts 1–4, 2 pages | Before Lesson 5 | writer + editor | none |
| 6. Build the replication zip from code/main.py + output/ | Before Lesson 5 | data lead | none |
| 7. Ask FZS/SERNANP for dated patrol / interdiction records per zone | Optional / extension | team lead | enforcement intensity, Peru |
| 8. Validate AMW vs MapBiomas inside Tambopata BZ; get an official La Pampa polygon | Optional / extension | spatial analyst | official La Pampa polygon |
| 9. River dredges / mercury: cite MAAP #193 dredge counts; no satellite fix | Optional / extension | writer | none (cite MAAP #193) |

## 9. Brief skeleton (draft)

![The brief's one figure: new mining area per year, Tambopata and Amarakaeri buffer zones, Tambopata National Reserve, Madre de Dios total and rest](../../output/fig_brief_main.png)
**Reading:** **[description]** Tambopata's additions fall after Mercurio (Feb 2019) and return from 2022; Amarakaeri and the rest of Madre de Dios rise. Description only.

**Part 1. The question (~½ page).** FZS supports SERNANP's enforcement against alluvial gold mining in the Tambopata–Bahuaja-Sonene landscape (FZS programme page). Operations are expensive and temporary. FZS needs to know what happens in the targeted area, and around it, when one ends. Our question: *after Operation Mercurio (Feb 2019), did mining in the Tambopata buffer zone fall, move, or wait?* Places: Tambopata buffer zone (targeted) vs Amarakaeri buffer zone (comparison), plus the reserve itself and the rest of Madre de Dios. Years 2014–2025. Brazil (Yanomami, Feb 2023) as a second, shorter case.

**Part 2. Data and provenance (~¼ page).** MapBiomas Peru Collection 4 (buffer zones; protected areas), annual mining area, class 4.2. Checks: Tambopata buffer zone 2025 = 20,730 ha; Tambopata NR 2025 = 777 ha on the MapBiomas platform. MapBiomas Brazil Collection 11 (all indigenous lands) check: 39,915 ha in 2025. Collection 10.1 per territory: Kayapó mining 2024 = 18,176 ha (Collection 10.1); platform (Collection 11) shows 17,632 ha (collection difference, no publisher match). World Bank Pink Sheet gold price check: Aug 2026 = $4,411/oz. One check per dataset, logged in DOWNLOAD_LOG.csv.

**Part 3. Findings (one figure).** Use `output/fig_brief_main.png`. Text, every sentence **[description]**: Tambopata 1,640 → 163 ha/yr vs Amarakaeri 289 → 574 (difference of changes −1,762); placebo 2016 209; department total 3,610 → 4,640 → 12,049; Tambopata 2022–25 1,829 (1,251 without 2023); reserve core +241 ha in 2025. Allow at most one causal sentence, stated conditionally and with its failure: "If Amarakaeri had moved in parallel, this would be a fall of ~1,760 ha/yr. But the 2016 pre-period already differs by as much, so we do not claim it."

**Part 4. What FZS can do with this.** (a) **[prediction]** Expect a local fall that lasts only while the presence lasts, no fall in the region, and pressure on the reserve core. Plan for permanent presence at the edges of the core (cf. the 2025 navy withdrawal on the Malinowski, MAAP #241), and monitor the next-nearest unprotected land. (b) Why it could mislead: one treated unit; parallel trends fail; spillovers into the control; COVID and the gold price; the sources disagree; MapBiomas cannot tell legal from illegal mining; river dredging and mercury are invisible. (c) What would let us say more: dated enforcement records (patrol days, interdictions per zone) from SERNANP/FZS; more treated units (Plan Restauración zones 2021); AMW quarterly patches in distance rings; river-dredge counts (MAAP-style SkySat); mercury sampling. Put the required AI-prompt output in the appendix, raw and edited.

---
*Built 2026-10-11 00:13 from git commit 11aa502 (working tree may contain uncommitted changes). Numbers from output/numbers.csv (418 rows).*
