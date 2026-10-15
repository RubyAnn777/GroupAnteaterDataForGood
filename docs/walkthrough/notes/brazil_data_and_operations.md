# Brazil: newer data and documented operations per Indigenous Territory (2026-10-11)

Status: DRAFT, team must review. Access date for everything below: 2026-10-11. Firecrawl calls used in this step: 4 (all `firecrawl_search`, 0 scrapes). Everything else via curl, WebSearch and WebFetch.
Companion files: `brazil_ti_interventions.csv` (one row per search, 39 rows), `brazil_ti_candidates.csv` (mining per TI + distance to Yanomami), script `scratch_scripts/brazil_ti_candidates.py`.

## Task 1: newer data

### 1a. Collection 11 (or later) statistics per indigenous territory: still NOT published
- https://brasil.mapbiomas.org/en/estatisticas/ (curl, 2026-10-11): 28 download links, all Collection 11: coverage (Biome/State, AMACRO, Atlantic Forest Law, DHN250, Legal Amazon, MATOPIBA, Priority areas, Quilombos, Semiarid), irrigation, and **mined substances** (AMACRO, Atlantic Forest Law, Biosphere reserve, DHN250, Legal Amazon, MATOPIBA, Municipality, Priority areas, Quilombos, Semiarid). **No Indigenous Territories file**, same as on 2026-10-10.
- MapBiomas Dataverse (data.mapbiomas.org): HTTP 502 Proxy Error on three tries (search API and the dataverse page). Could not re-check today. Yesterday's check (see `brazil_ti.md`) found Col 10.1 as the newest TI dataset (doi:10.58053/MapBiomas/1F2TLA).
- Monitor da Mineração page (https://brasil.mapbiomas.org/iniciativas-e-produtos/cobertura-e-uso-da-terra/mineracao/monitor-da-mineracao/): only PDFs (factsheets, reports), no per-TI table.
- Firecrawl search "MapBiomas Coleção 11 estatísticas terras indígenas mineração garimpo download": no file.
- So per-TI data remain Col 10.1 coverage class 30 (all mining, to 2024). The Col 11 per-TI numbers exist only in the platform UI (JavaScript).

### 1b. Mining module with garimpo vs industrial split: found at MUNICIPALITY level (Col 11), downloaded
Both files saved in `data_raw/mapbiomas_brazil/` exactly as served, logged in `DOWNLOAD_LOG.csv`.

| File | URL | Collection | Size (bytes) | sha256 | Server Last-Modified |
|---|---|---|---|---|---|
| MAPBIOMAS-BRAZIL-MINED-SUBSTANCES-MUNICIPALITY-COLLECTION_11.xlsx | https://brasil.mapbiomas.org/wp-content/uploads/sites/3/2026/10/MAPBIOMAS-BRAZIL-MINED-SUBSTANCES-MUNICIPALITY-COLLECTION_11.xlsx | 11 (VERSION v1.1) | 6,233,503 | 510a522684c800f3598432073b8efad94cb32a2399f9a6d4f774c6b5d03614c2 | 2026-10-02 |
| MAPBIOMAS-BRAZIL-MINED-SUBSTANCES-LEGAL-AMAZON-COLLECTION_11.xlsx | https://brasil.mapbiomas.org/wp-content/uploads/sites/3/2026/10/MAPBIOMAS-BRAZIL-MINED-SUBSTANCES-LEGAL-AMAZON-COLLECTION_11.xlsx | 11 | 3,286,565 | dfe4b6cc7a8b3a3fa79e20d82227b7653880d8ad3e81a9d29bb0f6b7bc0b58ba | 2026-10-02 |

- Structure: sheet `MINED_SUBSTANCE`, columns COUNTRY, BIOME, REGION, STATE, MUNICIPALITY, GEOCODE, VERSION, COLLECTION, CLASS_ID, CLASS_NAME (substance, e.g. Ouro, Sem Substância, Estanho), CLASS_LEVEL_1 (**Garimpo** / **Industrial**), CLASS_LEVEL_2 (**Solo exposto** / **Revegetação**), y1985..y2025. Hectares. Sum over biome rows per GEOCODE before differencing.
- **Check (passes):** Brazil garimpo 2025 = 445,986.5 ha, industrial = 243,865.3 ha. The pack's platform export (MapBiomas Brazil Collection 11, logged by the instructor) says 445,987 / 243,865 ha. Match.
- Caveat: "Revegetação" rows are old mining scars regrowing (Brazil garimpo 2025: 60,288 ha revegetating vs 385,699 ha bare). Decide whether the outcome is total or "Solo exposto" only, and keep it fixed.
- Why useful: garimpo-only series to 2025 for the Yanomami municipalities (RR: Iracema, Amajari, Alto Alegre, Mucajaí, Caracaraí; AM: Barcelos, Santa Isabel do Rio Negro, São Gabriel da Cachoeira) and for displacement checks into neighbouring municipalities. Roraima garimpo (Col 11 mining module): 2,455 ha (2018), 4,794 (2022), 5,523 (2023), 5,704 (2024), 5,873 (2025). Municipalities include land outside the TI, so this is not the TI series. Note: this is a different product from the Col 10.1 coverage class 30 used for Roraima's check number (446 ha in 2018). Do not mix the two series.
- No per-TI garimpo split exists in any collection as a downloadable file (checked Col 7 to 11). Per-TI garimpo numbers appear only in MapBiomas PDFs (Col 7, Col 8), already logged.

### 1c. Other Yanomami garimpo series after 2023 (context only, not downloaded)
| Source | What | URL | Opened |
|---|---|---|---|
| MAAP #242 (Amazon Conservation, led by ISA, 22 May 2026) | Annual new mining impact in the Yanomami TI: ~400 ha (2020), >1,000 (2021), ~1,800 (2022 peak), 330 (2023), 84 (2024), 45 ha (2025). Visual interpretation of Planet monthly mosaics + Sentinel-2. Cumulative 5,564 ha by Dec 2025 (ISA via Portal Amazônia) | https://www.maapprogram.org/gold-mining-brazil-yanomami/ | yes |
| ISA / Hutukara / Seduume report (via Portal Amazônia, 28 May 2026) | 45.2 ha new (2025) vs 83.95 ha (2024), −46%; cumulative 5,564 ha | https://portalamazonia.com/meio-ambiente/garimpo-ti-yanomami-rr/ | yes |
| Greenpeace "Ouro tóxico" (via Agência Pública, 8 Apr 2025) | New garimpo area 2023 → 2024: Yanomami 239 → 223 ha; Kayapó 1,019 → 704; Munduruku 152 → 66; **Sararé 619 → 1,197 (+93%)** | https://apublica.org/2025/04/garimpo-ilegal-migra-na-amazonia-e-dispara-na-ti-sarare-mt-alerta-greenpeace/ | yes |
| Greenpeace H1 2025 monitoring (~Sep 2025) | Jan to Jun 2025 new garimpo: Yanomami 8.16 ha, Munduruku 11.81, Kayapó 232.1, Sararé 773.02 ha (Planet 4.77 m) | https://www.greenpeace.org/brasil/blog/acoes-de-desintrusao-fazem-garimpo-recuar-nas-maiores-terras-indigenas-da-amazonia/ | yes |
| Casa de Governo Yanomami monthly bulletins (Casa Civil) | Monthly operation reports (e.g. Dec 2025) | https://www.gov.br/casacivil/pt-br/casa-de-governo-yanomami/boletins-mensais/FLDRelatorioYanomamiDEZ25.pdf | snippet only |
| INPE DETER class MINERACAO | Already downloaded (`data_raw/inpe_deter/`) | | |

The sources disagree on 2024 Yanomami (ISA 84 ha vs Greenpeace 223 ha), so the method matters. Cite each with its method and don't mix them.

Note: the gov.br news pages (agenciagov.ebc.com.br) currently show "Em respeito à legislação eleitoral vigente, esta página está desativada temporariamente" (election blackout). Official press releases from 2023 to 2025 can't be opened right now; I used press copies instead.

## Task 2: documented operations per TI, 2022 to 2025

Mining figures are from MapBiomas Brasil Collection 10.1, class 30 (all mining). Distance is the shortest boundary-to-boundary distance to the Yanomami TI (FUNAI polygons, EPSG:5880), from `brazil_ti_candidates.csv`. "Opened" means I opened the page and quote it in the CSV.

| TI | Mining 2018 / 2022 / 2024 (ha) | Dist. (km) | Operation 2022–2025? | Dates (source opened?) |
|---|---|---|---|---|
| Yanomami (treated) | 364 / 3,573 / 4,576 | 0 | yes | 2023 (MAAP #242, opened) |
| Kayapó | 6,159 / 15,748 / 18,176 | 1,352 | **yes** | Ibama Op. Xapiri – Tuíre Kayapó **6–14 Sep 2024** (opened); **desintrusão from 2 May 2025** (opened). Op. Xapiri Mebêngôkré, June (2024 or 2026, page conflicting) |
| Munduruku | 1,381 / 7,433 / 7,909 | 945 | **yes** | Ibama operation from **10 Aug 2023** (opened); **desintrusão from 9 Nov 2024**, main phase ended Jan 2025 (opened) |
| Tenharim do Igarapé Preto | 984 / 1,147 / 1,185 | 987 | unclear | Ibama GEF 2018 (opened, outside window); "Operação Warã II" undated, AGU/Ibama injunction reported 21 May 2025 (opened) |
| Apyterewa | 38 / 474 / 500 | 1,265 | **yes** | desintrusão from **2 Oct 2023** (opened; invaders mainly cattle ranchers) |
| Trincheira-Bacajá | (no class-30 row) | – | **yes** | same desintrusão, Oct 2023; "desintrusada em 2024" (Pública, opened) |
| Sai-Cinza | 0 / 428 / 478 | 942 | unclear | Op. Mundurukânia May 2021 (outside window); reportedly part of the Nov 2024 Munduruku operation (snippet only). Adjacent to Munduruku, so spillover risk |
| Parque do Aripuanã | 83 / 261 / 307 | 1,294 | **yes** | Op. Golden Border **13 Mar 2025** (opened) |
| Roosevelt (Cinta Larga) | (no class-30 row; diamonds) | – | **yes** | Op. Golden Border 13 Mar 2025 (opened) |
| Sawré Muybu | 154 / 216 / 241 | 888 | none found | – (Munduruku region, spillover risk) |
| Baú | 0 / 198 / 216 | 1,166 | **yes** | PF Op. Mercúrio **8–10 Jul 2022** (opened); next one 28 Jul–1 Aug 2026 (opened, outside window) |
| Sararé | 155 / 159 / 991 | 1,706 | **yes** | Ibama+PRF from **23 Sep 2024** (opened); ≥4 operations by May 2025 (Greenpeace, opened); Op. Alfeu Mar 2023, Ouro Viciado Apr 2024, Xapiri-Sararé Aug 2025 (snippets only); desintrusão 2026. **Likely displacement destination** (Greenpeace: new garimpo +93% 2023→24) |
| Las Casas | 51 / 144 / 145 | 1,659 | none found | – (Kayapó neighbour, spillover risk) |
| Évare I (Tikuna) | 0 / 47 / 114 | 498 | none found | – |
| Waimiri-Atroari | 19 / 32 / 36 | 197 | none found | – (too close to Yanomami; Pitinga/Taboca industrial mining nearby) |
| Enawenê-Nawê | 18 / 19 / 19 | 1,422 | none found | – |
| Cachoeira Seca (+ Kuruaya) | (no class-30 row) | – | **yes** | Ibama+PF **5–7 Dec 2023**; "diversas operações" through 2023 (opened) |
| Vale do Javari | (no class-30 row; river dredges) | – | **yes** | PF+Ibama Op. Xapiri from **5 Nov 2023** (opened); Apr 2025 (snippet) |
| Raposa Serra do Sol | (no class-30 row; river rafts) | – | **yes** | PF Op. Fox Uno **24–25 Jun 2025** (opened); Fox Três Nov 2025 (snippet) |
| Xikrin do Cateté | (no class-30 row) | – | unclear | Ibama Xapiri I undated (deforestation; snippet) |
| Menkragnoti, Arara, Zo'é, Tikuna areas, Andirá-Marau, Parque do Xingu | (no class-30 row) | – | none found | – |
| Tupinambá de Olivença (BA) | 89 / 162 / 176 | 3,077 | none found | sand extraction, not gold; exclude |

ADPF 709 desintrusão plans (STF homologation reported 6 Mar 2024, Conjur, opened): Yanomami, Karipuna, Uru-Eu-Wau-Wau, Kayapó, Araribóia, Munduruku, plus Apyterewa and Trincheira-Bacajá.

### Rule-based comparison set: what is left
Rule: Amazon TI, gold garimpo (class 30 > 0) before 2023, no documented federal anti-mining operation 2022–2025, at least ~500 km from Yanomami, and not next to a treated TI.
- Excluded as treated: Kayapó, Munduruku, Apyterewa, Parque do Aripuanã, Baú, Sararé (plus Sai-Cinza as unclear and adjacent).
- Excluded by distance or adjacency: Waimiri-Atroari (197 km), Las Casas (next to Kayapó), Sawré Muybu (Munduruku region).
- **Left: Tenharim do Igarapé Preto (unclear status, 1,147 ha), Évare I (47 ha), Enawenê-Nawê (19 ha).** Together that is about 1,213 ha in 2022 against Yanomami's 3,573 ha. Tenharim's mining is largely a legacy area (Paranapanema 1969–85, snippet) with near-flat growth (+41 ha/yr 2019–22).
- Even the lenient pool (adding Sawré Muybu, Las Casas and Waimiri-Atroari: 1,604 ha in 2022) adds about 95 ha/yr in 2019–22 and 68 ha/yr in 2023–24. Yanomami adds 802 and 501 ha/yr (description, Col 10.1).
- Implication: no "clean" untreated territory has garimpo dynamics comparable to Yanomami. All three large garimpo TIs (Kayapó, Munduruku, Yanomami) were treated between 2023 and 2025, at different dates. That points to a **staggered-adoption design** (Yanomami 2023, Munduruku Aug 2023 / Nov 2024, Kayapó Sep 2024 / May 2025), where not-yet-treated TIs serve as controls only before their own start, rather than one fixed control. The small "none found" pool is a robustness check at most. Sararé is better used as a **displacement** outcome than as a control.

### Caveats
- **No hits ≠ no enforcement.** The searches cover Portuguese and English press and NGO pages. Ibama/PF actions that weren't reported, or are only on gov.br (which is offline in the election blackout), are missed. IBAMA autos de infração (already downloaded) could be geocoded to TIs to measure enforcement systematically.
- Several operation names and dates come from search snippets. Only rows marked `opened = yes` in the CSV are verified.
- River dredges and rafts (Vale do Javari, Raposa Serra do Sol, Madeira) do not show up in MapBiomas land classes, so these TIs have no class-30 row even with active garimpo.
- Class 30 (Col 10.1) is all mining. Garimpo-only numbers per TI exist only in the platform or PDFs.
