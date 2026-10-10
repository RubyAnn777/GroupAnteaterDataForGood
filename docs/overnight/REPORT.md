# Overnight analysis report: how does mining move with enforcement?

> DRAFT for the team (Group Giant Anteater, Question 2, Peru + Brazil). Produced overnight on 10/11 Oct 2026 on branch `analysis/overnight-2026-10-10` by Claude, an AI assistant, and its subagents. Every number below is read from `output/numbers.csv`, which `uv run python code/main.py` writes. Nothing here is checked by a human yet. Read it critically, re-open the sources you cite, and treat every claim tag as a proposal.

## 1. Summary of findings

**What FZS asked:** what to expect in the targeted area, and around it, when an enforcement operation ends.

**Short answer from our data:** Enforcement moved mining more than it stopped it. Mining also came back when enforcement eased.

**Peru (Operation Mercurio, Feb 2019)**

1. **[description]** New mining in the **Tambopata buffer zone** (where La Pampa lies) fell from 1,640 ha/yr (2016–18) to 163 ha/yr (2019–21). In the **Amarakaeri buffer zone** it rose from 289 to 574 ha/yr. The difference of the changes is **−1,762 ha/yr**, which reproduces the course check number.
2. **[description]** The fall in Tambopata is unusual. Among 15 Peruvian buffer zones with pre-2019 mining, Tambopata has the most negative 2019–21 coefficient (rank 1). A fake operation in 2016 gives only 209 ha/yr.
3. **[description]** **The region did not gain.** New mining in all of Madre de Dios rose from 3,610 to 4,640 ha/yr and then to 12,049 ha/yr (2022–25). Most of this is outside the buffer zones ("rest of Madre de Dios": 1,688 → 3,937 → 9,020 ha/yr), and that area includes the legal mining corridor. This pattern is what displacement would look like. It is not proof that the same miners moved. MAAP #208 finds that 74% of 2021–24 mining deforestation in Madre de Dios lay inside the official mining corridor, where small-scale mining can be legal, so part of this rise may be legal or formalising mining that MapBiomas cannot tell apart.
4. **[description]** **Delay:** after 2021, Tambopata returned to 1,829 ha/yr in 2022–25, above its pre-Mercurio level. The persistence DiD shrinks to −737 ha/yr against Amarakaeri. Against the wider pool of buffer zones it is about zero (112 ha/yr).
5. **[description]** **Inside the reserve itself** (new file: MapBiomas Peru ANP statistics), mining in Tambopata National Reserve is small but growing: 777 ha in 2025, and 241 ha were added in 2025 alone. This is consistent in direction with MAAP #241's report of new mining inside the reserve in late 2025, though MAAP's figures come from a different method. A third, independent source agrees on timing: Amazon Mining Watch first detects 209 ha inside the reserve over 2019–24 combined, then 640 ha in 2025 alone (provisional). The three sources measure different things, so we compare only their direction, never their hectares.
6. **[description]** Declared (formal) gold production in Madre de Dios fell −88% between 2018 and 2025, while mapped mining area more than doubled (50,506 → 112,622 ha). Either more gold left the region undeclared, or reporting rules changed. We cannot tell which.

**Brazil (weak enforcement 2019–22, Yanomami operation Feb 2023)**

7. **[description]** IBAMA issued 6,920 infraction notices per year in the Legal Amazon in 2015–18 and 4,359 in 2019–22, then 7,907 in 2023. In the same years, new artisanal mining in all indigenous lands combined rose from 1,332 ha/yr (2016–18) to 4,319 ha/yr (2019–22) and fell to 2,978 ha/yr (2023–25). The two series move as mirror images, which is what weaker enforcement would predict. It does not prove it.
8. **[description]** New mining in the **Yanomami** territory fell from 1,617 ha (2022) to 824 ha (2023) and 179 ha (2024). It also fell in **Kayapó** and **Munduruku**, so the 2×2 comparison is inconclusive: +905 ha/yr vs Kayapó in hectares, but −4.4 percentage points of the 2022 stock. The sign depends on the scale, and a fake 2020 start already gives −355 ha/yr.
9. **[description]** No sign of displacement into the rest of Roraima: 96% of Roraima's mapped mining lies in the Yanomami territory, and the rest changed by only +19 ha in 2023–24. Elsewhere, the 19 smaller mining territories kept adding mining (523 → 560 ha/yr).

**What FZS can take from this** **[prediction]**: when an operation targets one hotspot, expect a sharp local fall, a rise in nearby less-protected land, and a return within 3–4 years if the presence is not kept up. The protected core is the last line, and in 2025 it is being crossed. This is a prediction from two cases and one treated unit each, not a causal estimate.

## 2. Data obtained

| Source | File (data_raw/ unless noted) | Years | Check number | Status |
|---|---|---|---|---|
| MapBiomas Peru, Collection 4, buffer zones (pack) | data/peru_bufferzone_year.csv | 1985–2025 | Tambopata BZ 2025 = 20,730 ha | OK (starter checks) |
| MapBiomas Peru, Collection 4, departments (pack) | data/peru_department_year.csv | 1985–2025 | Madre de Dios 2025 = 112,622 ha | OK |
| MapBiomas Peru, Collection 4, **Áreas protegidas** (new) | mapbiomas_peru/MAPBIOMAS-PERU-LULC-COL4-AREAS-PROTEGIDAS.xlsx | 1985–2025 | Tambopata NR 2025 = 776.9 ha (internal); platform check see §7 | OK; publisher check OK: platform shows 777 ha (Tambopata NR, Minería 2025) and 20,730 ha (buffer zone); screenshots in data_raw/mapbiomas_peru/ |
| MapBiomas Brazil, Collection 10.1, **Indigenous territories** (new) | mapbiomas_brazil/MAPBIOMAS_BRAZIL-COVERAGE_STATISTICS-COL.10.1-INDIGENOUS_TERRITORIES_STATE_BIOME.xlsx | 1985–2024 | Kayapó 2024 = 18,176 ha; Col 10 vs 10.1 within 0.07% (2018+) | OK; publisher check MISMATCH by collection: platform shows only Collection 11 (Kayapó 2024 = 17,632 ha) vs 18,176 ha in our Col 10.1 file; Col 11 per-territory file being sought |
| MapBiomas Brazil, Collection 11, mining (pack) | data/mining_area.csv | 1985–2025 | All TIs artisanal 2025 = 39,915 ha | OK |
| MapBiomas Brazil, Collection 10.1, municipalities (pack) | data/brazil_municipality_year.csv | 1985–2024 | Roraima 2018 = 446 ha, 2024 = 4,745 ha | OK |
| IBAMA open data, autos de infração (new) | ibama/auto_infracao_csv.zip (117 MB, git-ignored; small intermediate in data_intermediate/) | 1977–2026 | No total shown on IBAMA site; file integrity only | OK (data) / check BLOCKED |
| IBAMA embargoes | – | – | – | BLOCKED (no download URL found) |
| INPE TerraBrasilis DETER, class MINERACAO (new) | inpe_deter/deter_amz_mineracao.geojson | 2016–2026 | 2019 = 105.64 km² vs dashboard 105.40 km² | OK (0.2% domain difference) |
| BCRP series (source MINEM), gold production Madre de Dios (new) | bcrp/*.json | 2001–2025 | Monthly sums = annual (all years) | OK (internal) |
| Amazon Mining Watch, mining patches (new) | amw/amazon_basin_detections.geojson (112 MB, git-ignored) | 2018–2026 | 232,030 patches | OK (prototype only) |
| SERNANP protected areas, buffer zones, illegal-mining layer (new) | sernanp/*.geojson | current | Tambopata = anp_codi RN09 | OK |
| FUNAI indigenous territories (new) | funai/tis_poligonais.geojson (49 MB, git-ignored) | current | Yanomami 9,664,975 ha (FUNAI attribute) | OK |
| INGEMMET mining corridor D.L. 1100 (new) | ingemmet/corredor_minero_madre_de_dios_DL1100.geojson | current | 498,308 ha vs 498,296 ha cited by govt | OK |
| MAAP #130, #193, #208, #241 (citations) | maap/ | 2020–2026 | quotes with locations in notes/maap_citations.md | Quotes verified; only rendered text saved (site blocks downloads), raw HTML: manual |

Every file has a row in `DOWNLOAD_LOG.csv` (URL, access date, collection, sha256, check number).

## 3. Steps taken

1. Created branch `analysis/overnight-2026-10-10` from `main` and read agent.md, basics.html, strategy.html and the course PDFs.
2. Ran seven parallel agents: Peru ANP download, Brazil territory download, Brazil enforcement (IBAMA + papers), MAAP citations, enforcement timeline (were controls treated?), spatial layers, and code skeleton.
3. Wrote `code/main.py` with modules `common.py` (paths, registry, style, event markers), `checks.py` (6 starter checks + card numbers, fails loudly), `peru.py`, `peru_anp.py`, `peru_robust.py`, `peru_production.py`, `brazil.py`, `brazil_ibama.py`, `brazil_deter.py`, `spatial.py`.
4. Peru: additions per unit, 2×2 DiD, displacement sums, placebo (2016), persistence (2022–25), event study (pyfixest, 2018 = reference) and placebo-in-space, inside-reserve analysis, robustness controls.
5. Brazil: all-TI series (Col 11), per-territory series (Col 10.1), 2×2 DiD in ha and in % of stock, placebo, Roraima displacement, IBAMA intensity, DETER monthly alerts.
6. Extra data: DETER (monthly alerts) and declared gold production; spatial prototype with Amazon Mining Watch patches, zones and distance rings.
7. Publisher-side checks on the MapBiomas platforms and MAAP page captures in Chrome.
8. Built this report from `output/` with `docs/overnight/build_report.py`.

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

![Peru: annual additions by buffer zone, Madre de Dios total and rest, and the gold price](../../output/fig_peru_additions.png)
**Reading:** **[description]** Tambopata collapses after Mercurio, while Amarakaeri and the rest of Madre de Dios rise. All series jump in 2023. The gold price rises over the same years, and this data cannot separate the two.

![Event study: Tambopata vs comparison zones, 2018 = 0](../../output/fig_peru_event_study.png)
**Reading:** **[description]** 2019–22 coefficients sit far below the placebo band, then return to it from 2023. The pre-period is noisy (2016, 2017), so parallel trends are only roughly plausible.

![Displacement: sum of units vs Madre de Dios total](../../output/fig_peru_displacement.png)
**Reading:** **[description]** The targeted zones fall, the department total does not.

![Inside the reserves (ANP file) vs their buffer zones](../../output/fig_peru_inside_reserves.png)
**Reading:** **[description]** Mining inside Tambopata NR is small compared with its buffer zone, but it jumps in 2017 and again in 2025.

![Tambopata buffer zone plus reserve](../../output/fig_peru_displacement_into_reserve.png)
**Reading:** **[description]** Adding the reserve to its buffer zone barely changes the picture through 2024. 2025 is the first year where the reserve's share is visible.

![Declared gold production vs mapped mining area, Madre de Dios](../../output/fig_peru_production_vs_area.png)
**Reading:** **[description]** Declared production collapses after 2019 while mapped area keeps rising. These are two sources and two concepts, so we never divide one by the other.

![Map of Madre de Dios: zones, corridor, Amazon Mining Watch patches by onset period](../../output/fig_map_madre_de_dios.png)
**Reading:** **[description]** Most patches lie in the D.L. 1100 corridor and around La Pampa. The newest ones (2025–26, provisional) sit along the northern edge of Tambopata NR, where MAAP #241 reports the Malinowski incursion.

![Amazon Mining Watch: new mining area by distance ring around La Pampa](../../output/fig_spatial_rings.png)
**Reading:** **[description]** Within 50 km of La Pampa, the split of new AMW area across rings is the same in 2019–21 (8 / 22 / 70 %) and 2022–24. We see no ring-by-ring outward shift at this resolution.

![Brazil: Yanomami vs Munduruku vs Kayapó additions; all indigenous lands as context](../../output/fig_brazil_territories.png)
**Reading:** **[description]** All three territories peak during 2019–22 and fall in 2023–24. Yanomami peaks latest (2022), so the operation coincides with a nationwide fall.

![Brazil: IBAMA infraction notices vs mining additions in indigenous lands](../../output/fig_brazil_enforcement.png)
**Reading:** **[description]** Infraction notices dip in 2019–22 while mining additions surge, and they reverse in 2023.

![Brazil: DETER monthly mining alerts per territory](../../output/fig_brazil_deter_monthly.png)
**Reading:** **[description]** Yanomami alerts spike in Mar–Apr 2023, during the operation, then fade. Munduruku and Kayapó alerts had already fallen in mid-2022, before any 2023 action. Alerts are dated by detection, so they show when mining was seen, not when it began.

![Brazil: Roraima municipalities around Yanomami](../../output/fig_brazil_roraima.png)
**Reading:** **[description]** Roraima's mapped mining is almost all inside the Yanomami territory, so there is no visible spill into the rest of the state.

![Map: Yanomami, Munduruku, Kayapó with Amazon Mining Watch patches](../../output/fig_map_yanomami.png)
**Reading:** **[description]** Mining patches are concentrated inside the territories, not on their edges.

## 6. Numbers table

All 269 numbers, with unit, description, claim type and producing function: [`output/numbers.csv`](../../output/numbers.csv). Headline numbers used in section 1:

| id | value | unit | description |
|---|---:|---|---|
| `mean_add_tambopata_2016_18` | 1,640 | ha/yr | Mean annual addition to mining area, Tambopata, 2016-18 |
| `mean_add_tambopata_2019_21` | 162.5 | ha/yr | Mean annual addition to mining area, Tambopata, 2019-21 |
| `mean_add_amarakaeri_2016_18` | 289.2 | ha/yr | Mean annual addition to mining area, Amarakaeri, 2016-18 |
| `mean_add_amarakaeri_2019_21` | 573.8 | ha/yr | Mean annual addition to mining area, Amarakaeri, 2019-21 |
| `did_main` | −1,762 | ha/yr | DiD of mean annual additions, Tambopata minus Amarakaeri, Main: Tambopata vs Amarakaeri. Descriptive contrast of changes; not causal (spillovers, COVID, gold price, further enforcement waves). |
| `placebo_space_n_units` | 15 | count | Number of units in the placebo-in-space donor pool B |
| `placebo_space_rank_raw` | 1 | rank | Rank of Tambopata among 15 buffer zones (1 = most negative) in mean event-study beta 2019-21, each unit treated in turn |
| `did_placebo` | 208.7 | ha/yr | DiD of mean annual additions, Tambopata minus Amarakaeri, Placebo: fake operation in 2016 (no real-treatment years in window). Descriptive contrast of changes; not causal (spillovers, COVID, gold price, further enforcement waves). |
| `mean_add_mdd_total_2016_18` | 3,610 | ha/yr | Mean annual addition to mining area, Madre de Dios total, 2016-18 |
| `mean_add_mdd_total_2019_21` | 4,640 | ha/yr | Mean annual addition to mining area, Madre de Dios total, 2019-21 |
| `mean_add_mdd_total_2022_25` | 12,049 | ha/yr | Mean annual addition to mining area, Madre de Dios total, 2022-25 |
| `mean_add_rest_mdd_2016_18` | 1,688 | ha/yr | Mean annual addition to mining area, Rest of Madre de Dios, 2016-18 |
| `mean_add_rest_mdd_2019_21` | 3,937 | ha/yr | Mean annual addition to mining area, Rest of Madre de Dios, 2019-21 |
| `mean_add_rest_mdd_2022_25` | 9,020 | ha/yr | Mean annual addition to mining area, Rest of Madre de Dios, 2022-25 |
| `mean_add_tambopata_2022_25` | 1,829 | ha/yr | Mean annual addition to mining area, Tambopata, 2022-25 |
| `did_persistence` | −737.0 | ha/yr | DiD of mean annual additions, Tambopata minus Amarakaeri, Persistence: 2016-18 vs 2022-25. Descriptive contrast of changes; not causal (spillovers, COVID, gold price, further enforcement waves). |
| `robust_did_persistence_all_peru_poolB` | 112.2 | ha/yr | DiD of mean annual additions, Tambopata BZ minus control [All Peru buffer zones with 2014-18 mining (n=14), mean (event-study pool B)], persistence windows 2016-2018 -> 2022-2025. Descriptive contrast; not causal. |
| `anp_level_tam_nr_2025` | 776.9 | ha | Mining area inside Tambopata NR, 2025 |
| `anp_tam_nr_addition_2025` | 241.1 | ha | Addition inside Tambopata NR in 2025 (cf. MAAP #241 ~500 ha H2 2025-Feb 2026; different source/period, not subtracted) |
| `sp_amw_tambopata_nr_new_ha_2019_2024` | 208.9 | ha | AMW new area inside Tambopata NR, sum of onset years 2019-2024 (confirmed) |
| `sp_amw_tambopata_nr_new_ha_2025` | 640.1 | ha | AMW area with first detection in 2025 inside Tambopata National Reserve (AMW model hectares, not MapBiomas) PROVISIONAL |
| `pe_prod_change_2018_2025_pct` | −87.8 | % | Change in declared production 2018 to 2025 (within one source; not compared with area) |
| `pe_prod_mapbiomas_level_2018_ha` | 50,506 | ha | MapBiomas mining area level, Madre de Dios (Amazonía), 2018 |
| `pe_prod_mapbiomas_level_2025_ha` | 112,622 | ha | MapBiomas mining area level, Madre de Dios (Amazonía), 2025 (matches 112,622 ha check) |
| `br_ibama_aml_mean_2015_2018` | 6,920 | autos/yr | Mean IBAMA autos per year, Legal Amazon states, 2015-2018 (IBAMA open data, autos de infracao (non-cancelled), Legal Amazon states) |
| `br_ibama_aml_mean_2019_2022` | 4,359 | autos/yr | Mean IBAMA autos per year, Legal Amazon states, 2019-2022 (IBAMA open data, autos de infracao (non-cancelled), Legal Amazon states) |
| `br_ibama_aml_2023` | 7,907 | autos | IBAMA autos, Legal Amazon states, 2023 |
| `br_pack_art_add_mean_2016_2018` | 1,332 | ha/yr | Mean annual addition, artisanal mining, all indigenous lands combined, 2016-2018 (MapBiomas Brazil, Collection 11, all indigenous lands combined (artisanal mining)) |
| `br_pack_art_add_mean_2019_2022` | 4,319 | ha/yr | Mean annual addition, artisanal mining, all indigenous lands combined, 2019-2022 (MapBiomas Brazil, Collection 11, all indigenous lands combined (artisanal mining)) |
| `br_pack_art_add_mean_2023_2025` | 2,978 | ha/yr | Mean annual addition, artisanal mining, all indigenous lands combined, 2023-2025 (MapBiomas Brazil, Collection 11, all indigenous lands combined (artisanal mining)) |
| `br_ti_yanomami_add_2022` | 1,617 | ha | Addition Yanomami 2022 (MapBiomas Brazil, Collection 10.1, Indigenous Territories (class 4.3 Mining, all mining)) |
| `br_ti_yanomami_add_2023` | 824.2 | ha | Addition Yanomami 2023 (MapBiomas Brazil, Collection 10.1, Indigenous Territories (class 4.3 Mining, all mining)) |
| `br_ti_yanomami_add_2024` | 178.6 | ha | Addition Yanomami 2024 (MapBiomas Brazil, Collection 10.1, Indigenous Territories (class 4.3 Mining, all mining)) |
| `br_did_main_vs_Kayapo_ha_yr` | 904.8 | ha/yr | Descriptive DiD in mean annual additions: Yanomami vs Kayapo, 2020-2022 -> 2023-2024 (MapBiomas Brazil, Collection 10.1, Indigenous Territories (class 4.3 Mining, all mining)) |
| `br_did_main_vs_Kayapo_pct` | −4.37 | pp of 2022 stock | Same, additions as % of 2022 stock |
| `br_did_placebo_time_start_2020_ha_yr` | −354.9 | ha/yr | Descriptive DiD in mean annual additions: Yanomami vs Kayapo, 2017-2019 -> 2020-2022 (MapBiomas Brazil, Collection 10.1, Indigenous Territories (class 4.3 Mining, all mining)) |
| `br_rr_yanomami_share_2024` | 96.4 | % | Yanomami TI stock as share of Roraima municipal stock 2024 |
| `br_rr_outside_yanomami_add_2023_24` | 19.3 | ha | Change 2022 to 2024 in Roraima mining outside the Yanomami TI (Roraima stock minus TI stock) |
| `br_other19_add_mean_2020_2022` | 523.5 | ha/yr | Mean annual addition, 19 other territories with mining, 2020-2022 (MapBiomas Brazil, Collection 10.1, Indigenous Territories (class 4.3 Mining, all mining)) |
| `br_other19_add_mean_2023_2024` | 560.5 | ha/yr | Mean annual addition, 19 other territories with mining, 2023-2024 (MapBiomas Brazil, Collection 10.1, Indigenous Territories (class 4.3 Mining, all mining)) |

## 7. Open problems

- **Publisher-side check numbers.** Peru ANP matches the MapBiomas platform (777 ha). Brazil territories: the platform only shows Collection 11 (Kayapó 2024 = 17,632 ha vs 18,176 ha in our Collection 10.1 file), so the Col 10.1 file has no publisher-side match yet. IBAMA shows no totals on its site. MAAP pages could only be saved as rendered text; a human must use "Save as" for raw HTML.
- **One treated unit per country.** Standard errors are not informative (Conley & Taber 2011). We use placebo-in-space ranks and the figure instead.
- **Partly treated controls.** Amarakaeri had its own interventions (Camanti decline in MAAP #130; Huepetuhe under the 2023 emergency). Munduruku had operations from Aug 2023 and Nov 2024. Kayapó's formal operation began May 2025, after the data end.
- **Spillovers bias the Peru DiD away from zero.** If miners moved from Tambopata into Amarakaeri, the control rises because of the treatment.
- **Confounders:** COVID-19 (2020), the gold price, which roughly doubled 2018–2025, and enforcement waves (Restauración 2021, emergency 2023) all overlap the post-period.
- **Measurement:** MapBiomas "mining" covers legal and illegal mining, and any mineral. Additions include re-mining and reclassification (see the Tambopata NR 2017 jump: forest classes swap in the same year). Satellites do not see **river dredges** or **mercury**. MAAP #193 counts 148 → 598 dredges in La Pampa (2021 → 2023) on already-degraded land, which a "new area" measure misses.
- **The "rest of Madre de Dios" mixes legal and illegal mining.** It contains the D.L. 1100 corridor (74% of 2021–24 mining deforestation per MAAP #208). The regional rise is therefore not all illegal displacement. The spatial prototype can separate the corridor from the rest using AMW patches, but not with MapBiomas tables.
- **Brazil scale problem:** the DiD sign flips between hectares and % of stock. Pre-trends differ (placebo ≠ 0). Only 2 post years (Col 10.1 ends 2024).
- **IBAMA mining flag** is a free-text regex and has not been validated by hand. The embargo file is BLOCKED.
- **AMW** onset_year 2018 is a stock, not an addition. Its 480 m patches overstate area, and 2025–26 values are provisional.

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

**Part 1. The question (~½ page).** FZS supports SERNANP's enforcement against alluvial gold mining in the Tambopata–Bahuaja-Sonene landscape (FZS programme page). Operations are expensive and temporary. FZS needs to know what happens in the targeted area, and around it, when one ends. Our question: *after Operation Mercurio (Feb 2019), did mining in the Tambopata buffer zone fall, move, or wait?* Places: Tambopata buffer zone (targeted) vs Amarakaeri buffer zone (comparison), plus the reserve itself and the rest of Madre de Dios. Years 2014–2025. Brazil (Yanomami, Feb 2023) as a second case.

**Part 2. Data and provenance (~¼ page).** MapBiomas Peru Collection 4 (buffer zones; protected areas), annual mining area class 4.2. Check: Tambopata buffer zone 2025 = 20,730 ha. MapBiomas Brazil Collection 10.1 indigenous territories. Check: Kayapó mining 2024 = 18,176 ha (Collection 10.1); platform (Collection 11) shows 17,632 ha — collection difference, see log. World Bank Pink Sheet gold price. Check: Aug 2026 = $4,411/oz. One check per dataset, logged in DOWNLOAD_LOG.csv.

**Part 3. Findings (one figure).** Use `output/fig_brief_main.png`: top panel, additions in Tambopata BZ vs Amarakaeri BZ vs Tambopata NR; bottom panel, Madre de Dios total vs rest. Text: **[description]** 1,640 → 163 ha/yr in Tambopata vs 289 → 574 in Amarakaeri (DiD −1,762); placebo 209; department total 3,610 → 4,640 → 12,049; Tambopata back to 1,829 in 2022–25. Every sentence labelled description. One causal sentence at most, stated conditionally: "if Amarakaeri would have moved in parallel…".

**Part 4. What FZS can do with this.** (a) **[prediction]** Expect a local fall, a regional shift and a return within 3–4 years unless presence is maintained; budget for permanent presence and watch the next-nearest unprotected land and the reserve core. (b) Why it could mislead: one treated unit; spillovers into the control; COVID and the gold price; MapBiomas cannot tell legal from illegal mining; river dredging and mercury are invisible. (c) What would let us say more: dated enforcement records (patrol days, interdictions per zone), the AMW patches in distance rings with 2018+ quarterly data, more treated units (Plan Restauración zones 2021), river-dredge counts (MAAP-style SkySat), mercury sampling. Include the required AI prompt output in the appendix, both raw and edited.

---
*Built 2026-10-11 00:03 from git commit c3930a3 (working tree may contain uncommitted changes). Numbers from output/numbers.csv (269 rows).*
