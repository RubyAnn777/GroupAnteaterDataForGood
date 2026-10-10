# Brazil: MapBiomas per Indigenous Territory (Terra Indígena), Collection 10.1

Status: OK for the data (Collection 10.1, all territories, to 2024). NOT OK for the check number: no publisher figure for Collection 10.1 was found (see "Check number"). Firecrawl calls used: 2.

## File
- Dataset: "Coverage statistics by special territories - Indigenous Territories - MapBiomas Brasil Collection 10.1", MapBiomas Data (Dataverse), doi:10.58053/MapBiomas/1F2TLA, V1.1, released 2026-02-19. Dataset page: https://data.mapbiomas.org/dataset.xhtml?persistentId=doi:10.58053/MapBiomas/1F2TLA
- Download: `https://data.mapbiomas.org/api/access/datafile/523?format=original` (no login). Without `?format=original` Dataverse serves an ingested .tab (32 KB, lossy); use the original xlsx.
- Saved: `data_raw/mapbiomas_brazil/MAPBIOMAS_BRAZIL-COVERAGE_STATISTICS-COL.10.1-INDIGENOUS_TERRITORIES_STATE_BIOME.xlsx`, 5,225,214 bytes, sha256 `ad3b4eecf4e534ce746a3347fcbda39d80215d5ae09fce80883e9c7c1b0cee30`
- Sheets: READ_ME, COVERAGE_INDIGENOUS_TERRITORIES (data, 5,781 rows x 52 cols), PIVOT_*, METADADOS, LEGEND_CODE.
- Columns: country, biome, state, state_acronym, indigenous_territories (name + code, e.g. "Yanomami (50901)"), geocode (the code, numeric), class_id, class_level_0..4, then one column per year 1985..2024. Area unit: hectares (floats). Years end 2024.
- Mining = `class_id == 30` ("4.3. Mining", all mining: garimpo + industrial, any substance). Only 22 territories have a class-30 row (of 624 territory-state-biome units). A territory without a class-30 row has no mining (treat as 0 only after checking that the territory exists in the file).
- Territory identification: use `geocode` (unique per territory). One row per territory x state x biome x class. 3 territories span >1 state or biome in the file; Yanomami is in AM (geocode 50901, Amazonas) and RR (Roraima): the file has class-30 only for the RR row, so the AM part has no mining recorded. Always `groupby(geocode)` and sum over state/biome rows BEFORE differencing (agent.md rule 2). Kayapó and Munduruku are single rows (PA).
- Names exactly as spelled: `Yanomami (50901)`, `Munduruku (29801)`, `Kayapó (23001)`. Also `Munduruku-Taquara (58001)` exists (separate territory, no mining row; do not merge by name search).
- Mining module breakdown (artisanal vs industrial, substance) per territory: NOT available. The Col 11 "MINED-SUBSTANCES" files on https://brasil.mapbiomas.org/en/estatisticas/ exist only for municipality/state/biome/Legal Amazon/etc. units (no indigenous-territory file in the list). "Mining statistics - Collection 9" (doi:10.58053/MapBiomas/VC507I) is a 2.7 KB table only. So per-territory mining is class 30 (all mining); within these three territories it is overwhelmingly garimpo, but that is an assumption.
- No Collection 11 per-territory file found on the statistics page (page static HTML lists none). Nothing mixed: all numbers below are Collection 10.1.

## mining_ha (class 30), Collection 10.1, ha
| year | Kayapó (23001) | Munduruku (29801) | Yanomami (50901) |
|---|---|---|---|
| 2014 | 2,635.2 | 289.2 | 12.8 |
| 2015 | 2,885.8 | 343.9 | 12.1 |
| 2016 | 3,562.4 | 461.5 | 26.8 |
| 2017 | 4,849.3 | 871.1 | 107.4 |
| 2018 | 6,158.7 | 1,380.5 | 364.1 |
| 2019 | 7,990.0 | 2,509.8 | 667.0 |
| 2020 | 11,211.8 | 5,015.8 | 1,340.8 |
| 2021 | 14,003.4 | 6,772.4 | 1,956.0 |
| 2022 | 15,748.1 | 7,433.1 | 3,573.1 |
| 2023 | 17,130.2 | 7,664.1 | 4,397.3 |
| 2024 | 18,175.9 | 7,908.7 | 4,575.8 |

All 22 territories with mining, summed (ha): 2014 4,414 · 2018 9,522 · 2019 12,922 · 2022 30,080 · 2023 33,377 · 2024 35,107.
Yanomami additions: 2022 to 2023 +824 ha, 2023 to 2024 +179 ha (description: growth slowed after the Feb 2023 operation; stock never fell). Note these are net changes of a stock, can include reclassification.

## Top 15 territories by mining area, 2022 (ha, Col 10.1)
1 Kayapó (23001) 15,748 · 2 Munduruku (29801) 7,433 · 3 Yanomami (50901) 3,573 · 4 Tenharim do Igarapé Preto (44701) 1,147 · 5 Apyterewa (3002) 474 · 6 Sai-Cinza (40901) 428 · 7 Parque do Aripuanã (33601) 261 · 8 Sawré Muybu (Pimental) (56701) 216 · 9 Baú (6101) 198 · 10 Tupinambá de Olivença (55501) 162 · 11 Sararé (42101) 159 · 12 Las Casas (56801) 144 · 13 Évare I (12101) 47 · 14 Waimiri-Atroari (49501) 32 · 15 Enawenê-Nawê (11201) 19. (22 territories have class-30 rows in total.) Candidate comparison units outside the big three are tiny, so Kayapó and Munduruku are the only sizeable comparison territories.

## Check number (NOT resolved: no matching publisher figure)
Publisher pages found quote Collection 7 or 8, not 10.1:
1. MapBiomas factsheet "Proximidade de garimpo, rios e lagos na Amazônia" (18 Apr 2024), p.5: "Kayapó (13,79 mil ha), Munduruku (5,46 mil ha), Yanomami (3,27 mil ha)", source line "Coleção 8 do MapBiomas", year 2022, garimpo only. https://brasil.mapbiomas.org/wp-content/uploads/sites/4/2024/04/Factsheet_Mineracao-e-Agua_18.04.24.pdf (saved). Our Col 10.1 class 30, 2022: Kayapó 15,748, Munduruku 7,433, Yanomami 3,573. They differ (Collection 8 vs 10.1, and garimpo-only vs all mining). The Yanomami figure is closest (3.27k vs 3.57k, +9%).
2. MapBiomas "Destaques do mapeamento anual de mineração e garimpo no Brasil 1985 a 2021" (Sept 2022, Collection 7), p.5: "Top 5 ... área de garimpo em seus limites - 2021: 11.542 KAYAPÓ 1º, 4.743 MUNDURUKU 2º, 1.556 YANOMAMI 3º". Ours 2021: 14,003 / 6,772 / 1,956. Differ. https://brasil.mapbiomas.org/wp-content/uploads/sites/4/2023/11/MapBiomas_Mineracao_2022_30_09_1.pdf-_.pdf (saved).
Both confirm the ranking Kayapó > Munduruku > Yanomami, which the 10.1 file reproduces, but they are not a number match. Do not present either as "our number = publisher's number".
Only same-publisher cross-check that does match: the Collection 10 sibling file (doi:10.58053/MapBiomas/8RGIOR, V1.0, 2025-08-20; datafile 266; saved, 34,212,615 bytes, sha256 `71d466d43ebcc5a142f35e73824c43c4072d2185a76cb6e79cad2931dd15ce13`) gives 2022 Kayapó 15,746.9 / Munduruku 7,433.4 / Yanomami 3,573.3 (vs 10.1: 15,748.1 / 7,433.1 / 3,573.1), so 10 and 10.1 agree to <0.01% to 0.01%. This is a consistency check, not a publisher-quoted number.
Manual steps to get a real check: open the MapBiomas platform (plataforma.brasil.mapbiomas.org) or Monitor da Mineração (https://brasil.mapbiomas.org/iniciativas-e-produtos/cobertura-e-uso-da-terra/mineracao/monitor-da-mineracao/), select Coleção 10.1 (or 10), territory Terras Indígenas > Kayapó, class "Mineração", year 2022, and read the hectares; expected 15,748 ha (Col 10.1). The platform is JavaScript-rendered, so curl/Firecrawl could not read it. Alternatively a MapBiomas press release with Collection 10/10.1 garimpo-in-TI figures (not found).
The per-territory file also has a total check against the pack's `mining_area.csv` (Collection 11, all indigenous lands, artisanal 2022 = 30,980 ha per agent.md): our all-territory class-30 sum 2022 = 30,080 ha (Col 10.1). Different collection and measure; do not subtract or mix.

## Other files downloaded to data_raw/mapbiomas_brazil/ (context only)
- Hashes: Factsheet `42db12abd005daf0be6e42b47c6723c5b017df3f7a901e83d313ae4e234fd817`, Mineração 2022 PDF `48754a71d205962bb9b97bf55a4d1f69ec426fc4897da99ae0d15a5b4c45cdec`, Mining-Appendix ATBD Col 10 `2c4070b544cf469e43e495cb655e55d2b46864b2d5f8bff35559931458dafc22` (no territory numbers in it).
- File sizes: all < 50 MB (largest 34.2 MB, the Col 10 file; git-ignore it or leave out of the zip if not used).

## Problems / caveats
- Class 30 is all mining (garimpo + industrial); no legality, no artisanal split per territory.
- A stock series: additions = first difference after summing rows per geocode; reclassification can create negatives.
- Territory boundaries are fixed (FUNAI polygons), so growth is not boundary change; the Yanomami AM part has no mining row.
- Only two post-operation years for Yanomami (2023, 2024).
