<!--
Source of docs/overnight/REPORT.html. Build: `uv run python docs/overnight/build_report.py`.
Placeholders {{id}} or {{id:fmt}} are filled from output/numbers.csv (default fmt ",.0f"; the build fails if an id is missing).
Claim tags: [[D]] description, [[P]] prediction, [[C]] causal. Figures: ![caption](output/fig_x.png) are embedded as base64.
Sections are split on "## ". Lines starting with "> " become callouts.
-->

# Overnight analysis report: how does mining move with enforcement?

> For the team (Group Giant Anteater, Question 2, Peru + Brazil). Produced overnight on 10/11 Oct 2026 on branch `analysis/overnight-2026-10-10` by Claude, an AI assistant, and its subagents. Every number below is read from `output/numbers.csv`, which `uv run python code/main.py` writes. Nothing here is checked by a human yet. Read it critically, re-open the sources you cite, and treat every claim tag as a proposal.

## 1. Summary of findings

**What FZS asked:** what to expect in the targeted area, and around it, when an enforcement operation ends.

**Short answer from our data:** Enforcement moved mining more than it stopped it. Mining also came back when enforcement eased.

**Peru (Operation Mercurio, Feb 2019)**

1. [[D]] New mining in the **Tambopata buffer zone** (where La Pampa lies) fell from {{mean_add_tambopata_2016_18}} ha/yr (2016–18) to {{mean_add_tambopata_2019_21}} ha/yr (2019–21). In the **Amarakaeri buffer zone** it rose from {{mean_add_amarakaeri_2016_18}} to {{mean_add_amarakaeri_2019_21}} ha/yr. The difference of the changes is **{{did_main}} ha/yr**, which reproduces the course check number.
2. [[D]] The fall in Tambopata is unusual. Among {{placebo_space_n_units}} Peruvian buffer zones with pre-2019 mining, Tambopata has the most negative 2019–21 coefficient (rank {{placebo_space_rank_raw}}). A fake operation in 2016 gives only {{did_placebo}} ha/yr.
3. [[D]] **The region did not gain.** New mining in all of Madre de Dios rose from {{mean_add_mdd_total_2016_18}} to {{mean_add_mdd_total_2019_21}} ha/yr and then to {{mean_add_mdd_total_2022_25}} ha/yr (2022–25). Most of this is outside the buffer zones ("rest of Madre de Dios": {{mean_add_rest_mdd_2016_18}} → {{mean_add_rest_mdd_2019_21}} → {{mean_add_rest_mdd_2022_25}} ha/yr), and that area includes the legal mining corridor. This pattern is what displacement would look like. It is not proof that the same miners moved. MAAP #208 finds that 74% of 2021–24 mining deforestation in Madre de Dios lay inside the official mining corridor, where small-scale mining can be legal, so part of this rise may be legal or formalising mining that MapBiomas cannot tell apart.
4. [[D]] **Delay:** after 2021, Tambopata returned to {{mean_add_tambopata_2022_25}} ha/yr in 2022–25, above its pre-Mercurio level. The persistence DiD shrinks to {{did_persistence}} ha/yr against Amarakaeri. Against the wider pool of buffer zones it is about zero ({{robust_did_persistence_all_peru_poolB}} ha/yr).
5. [[D]] **Inside the reserve itself** (new file: MapBiomas Peru ANP statistics), mining in Tambopata National Reserve is small but growing: {{anp_level_tam_nr_2025:,.0f}} ha in 2025, and {{anp_tam_nr_addition_2025}} ha were added in 2025 alone. This is consistent in direction with MAAP #241's report of new mining inside the reserve in late 2025, though MAAP's figures come from a different method. A third, independent source agrees on timing: Amazon Mining Watch first detects {{sp_amw_tambopata_nr_new_ha_2019_2024}} ha inside the reserve over 2019–24 combined, then {{sp_amw_tambopata_nr_new_ha_2025}} ha in 2025 alone (provisional). The three sources measure different things, so we compare only their direction, never their hectares.
6. [[D]] Declared (formal) gold production in Madre de Dios fell {{pe_prod_change_2018_2025_pct:.0f}}% between 2018 and 2025, while mapped mining area more than doubled ({{pe_prod_mapbiomas_level_2018_ha}} → {{pe_prod_mapbiomas_level_2025_ha}} ha). Either more gold left the region undeclared, or reporting rules changed. We cannot tell which.

**Brazil (weak enforcement 2019–22, Yanomami operation Feb 2023)**

7. [[D]] IBAMA issued {{br_ibama_aml_mean_2015_2018}} infraction notices per year in the Legal Amazon in 2015–18 and {{br_ibama_aml_mean_2019_2022}} in 2019–22, then {{br_ibama_aml_2023}} in 2023. In the same years, new artisanal mining in all indigenous lands combined rose from {{br_pack_art_add_mean_2016_2018}} ha/yr (2016–18) to {{br_pack_art_add_mean_2019_2022}} ha/yr (2019–22) and fell to {{br_pack_art_add_mean_2023_2025}} ha/yr (2023–25). The two series move as mirror images, which is what weaker enforcement would predict. It does not prove it.
8. [[D]] New mining in the **Yanomami** territory fell from {{br_ti_yanomami_add_2022}} ha (2022) to {{br_ti_yanomami_add_2023}} ha (2023) and {{br_ti_yanomami_add_2024}} ha (2024). It also fell in **Kayapó** and **Munduruku**, so the 2×2 comparison is inconclusive: {{br_did_main_vs_Kayapo_ha_yr:+,.0f}} ha/yr vs Kayapó in hectares, but {{br_did_main_vs_Kayapo_pct:+.1f}} percentage points of the 2022 stock. The sign depends on the scale, and a fake 2020 start already gives {{br_did_placebo_time_start_2020_ha_yr:+,.0f}} ha/yr.
9. [[D]] No sign of displacement into the rest of Roraima: {{br_rr_yanomami_share_2024:.0f}}% of Roraima's mapped mining lies in the Yanomami territory, and the rest changed by only {{br_rr_outside_yanomami_add_2023_24:+,.0f}} ha in 2023–24. Elsewhere, the 19 smaller mining territories kept adding mining ({{br_other19_add_mean_2020_2022}} → {{br_other19_add_mean_2023_2024}} ha/yr).

**What FZS can take from this** [[P]]: when an operation targets one hotspot, expect a sharp local fall, a rise in nearby less-protected land, and a return within 3–4 years if the presence is not kept up. The protected core is the last line, and in 2025 it is being crossed. This is a prediction from two cases and one treated unit each, not a causal estimate.

## 2. Data obtained

| Source | File (data_raw/ unless noted) | Years | Check number | Status |
|---|---|---|---|---|
| MapBiomas Peru, Collection 4, buffer zones (pack) | data/peru_bufferzone_year.csv | 1985–2025 | Tambopata BZ 2025 = 20,730 ha | OK (starter checks) |
| MapBiomas Peru, Collection 4, departments (pack) | data/peru_department_year.csv | 1985–2025 | Madre de Dios 2025 = 112,622 ha | OK |
| MapBiomas Peru, Collection 4, **Áreas protegidas** (new) | mapbiomas_peru/MAPBIOMAS-PERU-LULC-COL4-AREAS-PROTEGIDAS.xlsx | 1985–2025 | Tambopata NR 2025 = {{anp_level_tam_nr_2025:,.1f}} ha (internal); platform check see §7 | OK; publisher check OK: platform shows 777 ha (Tambopata NR, Minería 2025) and 20,730 ha (buffer zone); screenshots in data_raw/mapbiomas_peru/ |
| MapBiomas Brazil, Collection 10.1, **Indigenous territories** (new) | mapbiomas_brazil/MAPBIOMAS_BRAZIL-COVERAGE_STATISTICS-COL.10.1-INDIGENOUS_TERRITORIES_STATE_BIOME.xlsx | 1985–2024 | Kayapó 2024 = {{br_ti_kayapo_stock_2024}} ha; Col 10 vs 10.1 within {{br_col10_vs_col101_max_rel_diff_pct:.2f}}% (2018+) | OK; publisher check {{CHECK_BRAZIL_TI}} |
| MapBiomas Brazil, Collection 11, mining (pack) | data/mining_area.csv | 1985–2025 | All TIs artisanal 2025 = {{br_pack_art_level_2025}} ha | OK |
| MapBiomas Brazil, Collection 10.1, municipalities (pack) | data/brazil_municipality_year.csv | 1985–2024 | Roraima 2018 = {{br_rr_level_2018}} ha, 2024 = {{br_rr_level_2024}} ha | OK |
| IBAMA open data, autos de infração (new) | ibama/auto_infracao_csv.zip (117 MB, git-ignored; small intermediate in data_intermediate/) | 1977–2026 | No total shown on IBAMA site; file integrity only | OK (data) / check BLOCKED |
| IBAMA embargoes | – | – | – | BLOCKED (no download URL found) |
| INPE TerraBrasilis DETER, class MINERACAO (new) | inpe_deter/deter_amz_mineracao.geojson | 2016–2026 | 2019 = {{br_deter_2019_total_wfs_km2:.2f}} km² vs dashboard {{br_deter_2019_total_dashboard_km2:.2f}} km² | OK (0.2% domain difference) |
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

{{DECISIONS_TABLE}}

## 5. Figures

![Peru: annual additions by buffer zone, Madre de Dios total and rest, and the gold price](output/fig_peru_additions.png)
**Reading:** [[D]] Tambopata collapses after Mercurio, while Amarakaeri and the rest of Madre de Dios rise. All series jump in 2023. The gold price rises over the same years, and this data cannot separate the two.

![Event study: Tambopata vs comparison zones, 2018 = 0](output/fig_peru_event_study.png)
**Reading:** [[D]] 2019–22 coefficients sit far below the placebo band, then return to it from 2023. The pre-period is noisy (2016, 2017), so parallel trends are only roughly plausible.

![Displacement: sum of units vs Madre de Dios total](output/fig_peru_displacement.png)
**Reading:** [[D]] The targeted zones fall, the department total does not.

![Inside the reserves (ANP file) vs their buffer zones](output/fig_peru_inside_reserves.png)
**Reading:** [[D]] Mining inside Tambopata NR is small compared with its buffer zone, but it jumps in 2017 and again in 2025.

![Tambopata buffer zone plus reserve](output/fig_peru_displacement_into_reserve.png)
**Reading:** [[D]] Adding the reserve to its buffer zone barely changes the picture through 2024. 2025 is the first year where the reserve's share is visible.

![Declared gold production vs mapped mining area, Madre de Dios](output/fig_peru_production_vs_area.png)
**Reading:** [[D]] Declared production collapses after 2019 while mapped area keeps rising. These are two sources and two concepts, so we never divide one by the other.

![Map of Madre de Dios: zones, corridor, Amazon Mining Watch patches by onset period](output/fig_map_madre_de_dios.png)
**Reading:** [[D]] Most patches lie in the D.L. 1100 corridor and around La Pampa. The newest ones (2025–26, provisional) sit along the northern edge of Tambopata NR, where MAAP #241 reports the Malinowski incursion.

![Amazon Mining Watch: new mining area by distance ring around La Pampa](output/fig_spatial_rings.png)
**Reading:** [[D]] Within 50 km of La Pampa, the split of new AMW area across rings is the same in 2019–21 ({{sp_lp_ring_0_10km_share_2019_21:.0f}} / {{sp_lp_ring_10_25km_share_2019_21:.0f}} / {{sp_lp_ring_25_50km_share_2019_21:.0f}} %) and 2022–24. We see no ring-by-ring outward shift at this resolution.

![Brazil: Yanomami vs Munduruku vs Kayapó additions; all indigenous lands as context](output/fig_brazil_territories.png)
**Reading:** [[D]] All three territories peak during 2019–22 and fall in 2023–24. Yanomami peaks latest (2022), so the operation coincides with a nationwide fall.

![Brazil: IBAMA infraction notices vs mining additions in indigenous lands](output/fig_brazil_enforcement.png)
**Reading:** [[D]] Infraction notices dip in 2019–22 while mining additions surge, and they reverse in 2023.

![Brazil: DETER monthly mining alerts per territory](output/fig_brazil_deter_monthly.png)
**Reading:** [[D]] Yanomami alerts spike in Mar–Apr 2023, during the operation, then fade. Munduruku and Kayapó alerts had already fallen in mid-2022, before any 2023 action. Alerts are dated by detection, so they show when mining was seen, not when it began.

![Brazil: Roraima municipalities around Yanomami](output/fig_brazil_roraima.png)
**Reading:** [[D]] Roraima's mapped mining is almost all inside the Yanomami territory, so there is no visible spill into the rest of the state.

![Map: Yanomami, Munduruku, Kayapó with Amazon Mining Watch patches](output/fig_map_yanomami.png)
**Reading:** [[D]] Mining patches are concentrated inside the territories, not on their edges.

## 6. Numbers table

{{NUMBERS_TABLE}}

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

{{NEXT_STEPS_DIAGRAM}}

## 9. Brief skeleton (draft)

**Part 1. The question (~½ page).** FZS supports SERNANP's enforcement against alluvial gold mining in the Tambopata–Bahuaja-Sonene landscape (FZS programme page). Operations are expensive and temporary. FZS needs to know what happens in the targeted area, and around it, when one ends. Our question: *after Operation Mercurio (Feb 2019), did mining in the Tambopata buffer zone fall, move, or wait?* Places: Tambopata buffer zone (targeted) vs Amarakaeri buffer zone (comparison), plus the reserve itself and the rest of Madre de Dios. Years 2014–2025. Brazil (Yanomami, Feb 2023) as a second case.

**Part 2. Data and provenance (~¼ page).** MapBiomas Peru Collection 4 (buffer zones; protected areas), annual mining area class 4.2. Check: Tambopata buffer zone 2025 = 20,730 ha. MapBiomas Brazil Collection 10.1 indigenous territories. Check: {{CHECK_BRAZIL_TI_SHORT}}. World Bank Pink Sheet gold price. Check: Aug 2026 = $4,411/oz. One check per dataset, logged in DOWNLOAD_LOG.csv.

**Part 3. Findings (one figure).** Use `output/fig_brief_main.png`: top panel, additions in Tambopata BZ vs Amarakaeri BZ vs Tambopata NR; bottom panel, Madre de Dios total vs rest. Text: [[D]] {{mean_add_tambopata_2016_18}} → {{mean_add_tambopata_2019_21}} ha/yr in Tambopata vs {{mean_add_amarakaeri_2016_18}} → {{mean_add_amarakaeri_2019_21}} in Amarakaeri (DiD {{did_main}}); placebo {{did_placebo}}; department total {{mean_add_mdd_total_2016_18}} → {{mean_add_mdd_total_2019_21}} → {{mean_add_mdd_total_2022_25}}; Tambopata back to {{mean_add_tambopata_2022_25}} in 2022–25. Every sentence labelled description. One causal sentence at most, stated conditionally: "if Amarakaeri would have moved in parallel…".

**Part 4. What FZS can do with this.** (a) [[P]] Expect a local fall, a regional shift and a return within 3–4 years unless presence is maintained; budget for permanent presence and watch the next-nearest unprotected land and the reserve core. (b) Why it could mislead: one treated unit; spillovers into the control; COVID and the gold price; MapBiomas cannot tell legal from illegal mining; river dredging and mercury are invisible. (c) What would let us say more: dated enforcement records (patrol days, interdictions per zone), the AMW patches in distance rings with 2018+ quarterly data, more treated units (Plan Restauración zones 2021), river-dredge counts (MAAP-style SkySat), mercury sampling. Include the required AI prompt output in the appendix, both raw and edited.
