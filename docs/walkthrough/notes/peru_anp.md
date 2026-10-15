# Peru ANP file (MapBiomas Peru Colección 4, Áreas Protegidas)

Status: OK (file downloaded, parsed). Publisher-side check of a *mining* number: NOT found (see below).

## What I did
- curl of https://peru.mapbiomas.org/descargas/estadisticas (HTTP 200) saved as `data_raw/mapbiomas_peru/page_descargas_estadisticas_2026-10-10.html`. The page lists the COL4 files, including the target.
- Downloaded with curl, no login/form:
  `https://peru.mapbiomas.org/wp-content/uploads/sites/6/2026/09/MAPBIOMAS-PERU-LULC-COL4-AREAS-PROTEGIDAS.xlsx`
- Saved as `data_raw/mapbiomas_peru/MAPBIOMAS-PERU-LULC-COL4-AREAS-PROTEGIDAS.xlsx` (unmodified).
- sha256 `d85f3e123c9531f400e232c5768c2cb5f81c8b954e69a2c0967b14827d11e503`, size 4,765,130 bytes (Microsoft Excel 2007+). READ_ME sheet: "Version 1, August 2026".
- Other COL4 files on the same page (not downloaded): AREAS-CONSERVACION-PRIVADA, AREAS-CONSERVACION-REGIONAL-1, BIOMES, CUENCAS, PERDIDA-VEGETACION, RESERVA-BIOSFERA, VEGETACION-SECUNDARIA. (Reserva Indígena / Territorial / Comunidad files exist only for COL3.)
- Parsed with `uv run python -I` (scripts in scratchpad).

## Structure
- Sheets: READ_ME, COVERAGE_4 (899 rows x 73 cols), PIVOT_COVERAGE, PIVOTCHART_COVERAGE, TRANSITION_4, PIVOT_TRANSITION, METADATA, LEGEND_CODE.
- COVERAGE_4 same layout as sibling files: block `_1` = the unit (`territory_level_2_1` = ANP name, `territory_level_3_1` = ANP category), block `_2` = department (`territory_level_2_2`), `_3` = country. `category_1` = NATIONAL_PROTECTED_AREAS. Class: `class` (id), `class_level_0..4`; years `y1985`..`y2025`. One row = ANP x department x class (class_level_4 names are the finest level).
- Mining = `class` 30, `class_level_2/4` = "4.2. Minería" (LEGEND_CODE: 4.2 Mining, ID 30). Same as sibling files. Area in hectares (non-integer).
- 10 ANP categories: Parque Nacional, Bosque de Protección, Reserva Nacional, Reserva Comunal, Coto de Caza, Reserva Paisajistica, Santuario Histórico, Refugio de Vida Silvestre, Santuario Nacional, Zona Reservada. 60 ANP names. Only 13 ANP x department rows have a 4.2 row; total ANP mining 2025 = 833.7 ha.
- Spellings: `Tambopata` / `Reserva Nacional`; `Bahuaja-Sonene` / `Parque Nacional` (departments Madre de Dios + Puno); `Amarakaeri` / `Reserva Comunal`; `del Manu` / `Parque Nacional`; `Alto Purús` / `Parque Nacional`; `Purús` / `Reserva Comunal`.
- CAUTION: the file is ANP *proper* (the reserve itself), not the buffer zone. Distinct from `peru_bufferzone_year.csv`.

## mining_ha (class 4.2), ha, summed over departments
| year | Tambopata NR | Bahuaja-Sonene NP | Amarakaeri RC | del Manu | Alto Purús | Purús |
|---|---|---|---|---|---|---|
| 2010 | 13.5 | 0.0 | 0.0 | 0 | 0 | 0 |
| 2011 | 51.1 | 0.0 | 0.0 | 0 | 0 | 0 |
| 2012 | 53.5 | 8.9 | 0.0 | 0 | 0 | 0 |
| 2013 | 47.7 | 8.7 | 0.4 | 0 | 0 | 0 |
| 2014 | 38.6 | 12.9 | 4.5 | 0 | 0 | 0 |
| 2015 | 58.9 | 11.3 | 9.2 | 0 | 0 | 0 |
| 2016 | 54.4 | 13.6 | 7.8 | 0 | 0 | 0 |
| 2017 | 588.1 | 13.7 | 4.8 | 0 | 0 | 0 |
| 2018 | 561.3 | 18.8 | 4.4 | 0 | 0 | 0 |
| 2019 | 534.7 | 20.2 | 3.5 | 0 | 0 | 0 |
| 2020 | 508.4 | 22.5 | 3.1 | 0 | 0 | 0 |
| 2021 | 461.7 | 23.2 | 3.1 | 0 | 0 | 0 |
| 2022 | 463.3 | 26.5 | 3.1 | 0 | 0 | 0 |
| 2023 | 523.1 | 28.3 | 3.2 | 0 | 0 | 0 |
| 2024 | 535.8 | 29.3 | 3.0 | 0 | 0 | 0 |
| 2025 | 776.9 | 30.9 | 3.1 | 0 | 0 | 0 |

del Manu, Alto Purús, Purús exist in the file (24/16/8 rows) but have NO class 4.2 row = zero mining (implicit zeros; treat as 0, not missing). Bahuaja-Sonene 2025: Puno 29.97 ha, Madre de Dios 0.96 ha.

## Things to note (description only)
- Tambopata NR jumps 54.4 -> 588.1 ha between 2016 and 2017 (+534 ha in one year), then declines slowly 2018-2021 (561 -> 462) and rises again, +241 ha in 2025. The 2017 step looks like a mapping/classification discontinuity or a one-off event; investigate before using 2017 additions (e.g. placebo window 2016-18). Not verified against any other source.
- Annual additions inside the reserve after Mercurio are small/negative (2019-21) and +241 ha in 2025, consistent with MAAP #241's report of new mining inside Tambopata NR in 2025. Magnitudes are tiny next to the buffer zone (20,730 ha in 2025).
- Files rows are class areas inside the reserve; mining here is at most ~0.3% of the reserve (776.9 / 277,829 ha).

## Check number
- Publisher-side mining match: NOT FOUND. plataforma.mapbiomas.org/projects/mapbiomas/peru is an interactive JS app; a scrape (1 Firecrawl call) only showed country-level 2025 totals (Non-vegetated 11,696,593 ha) which do not map to the ANP file. Territory selection needs clicking in the map; I did not do that. Manual step: open https://plataforma.mapbiomas.org/projects/mapbiomas/peru, Land Cover col. 4 > Coverage, group by "Protected areas" (or select Reserva Nacional Tambopata), year 2025, read Mining; compare with 776.9 ha.
- Best substitute (external, area not mining): file area of Tambopata (sum of all classes, 2025) = 277,828.5 ha = 2,778 km2 vs FZS page 2,746 km2 (+1.2%); Bahuaja-Sonene (Madre de Dios + Puno) = 1,092,509.7 ha = 10,925 km2 vs FZS 10,914 km2 (+0.1%) (FZS figures from agent.md §10, fzs.org page, accessed 2026-10-09; I did not re-open it). Plus internal: the file is constant in total area over years (Tambopata 277,829 ha in 2000 and 2025).
- Proposed log check_number: "Tambopata NR class 4.2 Mineria 2025 = 776.9 ha" (our number; needs the manual platform confirmation to count as a publisher match).

## Problems
- No login/captcha/form was met. Firecrawl calls used: 1.
- Chrome not used.
