# Enforcement intensity against illegal gold mining, Madre de Dios (Peru)

Compiled 2026-10-12 (access date for every source below). Tools: WebSearch/WebFetch, curl, **1 Firecrawl call** (search). Raw files are in `data_raw/enforcement_peru/`, saved exactly as served. Nothing was committed and no other repo file was edited.
Only pages and files I actually opened are cited. "snippet" means the item came from a search result and was not opened.

**Bottom line.** No source gives annual **interdiction counts by zone** (La Pampa vs Amarakaeri vs corridor vs Huepetuhe) for 2010-2025. There are three kinds of evidence:
1. **Open, machine-readable annual series** (department level only): MEF budget execution for program PP 0128 "Reducción de la minería ilegal" (2015-2026) and Ministerio Público criminal complaints for minería ilegal (art. 307-A to E, 2020-2026), plus the FEMA environmental caseload (2019-2026).
2. **Official counts in PDF reports**, covering parts of the period: ACAFMIRA/PCM interdictions 2013-May 2016 (MINAM 2016), and DIRMEAMB-PNP interdictions, arrests, seizures, FFAA personnel and military seizures for 2019-2020 (Plan Restauración annex, 2021). The 2019 rows give the only **sub-department** split: 195 in Tambopata, 1 each in Las Piedras, Laberinto and Inambari.
3. **Press balances quoting the PCM** for 2024-2026: national totals, plus Madre de Dios for some periods.

## 1. Sources checked

| # | Source (publisher) | What | Years | Geography | Granularity | Format | Downloadable without login? | File in `data_raw/enforcement_peru/` |
|---|---|---|---|---|---|---|---|---|
| A | MEF Consulta Amigable, "Actividades y Proyectos", Programa Presupuestal **0128 Reducción de la minería ilegal**, broken down by "Departamento (Meta)" | PIA, PIM, certification, commitment, **devengado** (executed spending) in soles | 2015-2026 (2026 = year to date; PP 0128 not listed in 2012-2014) | department (where the spending target sits) | annual (month and quarter also exist on the site) | HTML table (ASP.NET postback; scraped with a form POST, no login) | yes | `mef_pp0128/mef_consulta_amigable_PP0128_departamento_<year>.html` (12 files) |
| B | Ministerio Público (MPFN), datosabiertos.gob.pe "Delitos denunciados ante el Ministerio Público [MPFN]" | number of criminal complaints by article; minería ilegal = arts. **307-A** (minería ilegal), 307-B (aggravated), 307-C (financing), 307-D (obstruction), **307-E** (trafficking chemical inputs/machinery) | 2020-2025 full years; 2026 Jan-Aug | distrito fiscal (= department for MdD; every MdD row sits at the Tambopata seat) | annual | CSV | yes | `mpfn_delitos_denunciados/*.csv` + dictionary |
| C | MPFN, datosabiertos.gob.pe "Casos fiscales ingresados y atendidos a nivel nacional [MPFN]" | cases filed and handled, by prosecutor type; "MATERIA AMBIENTAL" = FEMA caseload (all environmental crimes, not mining only) | 2019-2025; 2026 Jan-Aug | distrito fiscal | annual | CSV | yes | `mpfn_casos_fiscales/*.csv` + dictionary |
| D | MININTER, datosabiertos.gob.pe "Resultados de las operaciones policiales a nivel nacional" (CENOPPOL) | police operations ("OPERATIVOS"), detainees, seizures, by police unit | Oct 2022-Jul 2026 | unit: DIRMEAMB (environmental police) **national only**; "RP MADRE DE DIOS" = all crime in the region | monthly | CSV | yes | `mininter_produccion_policial_2022-10_2026-07.csv` + dictionary |
| E | DEVIDA, datosabiertos.gob.pe "Volumen de Insumos Químicos Fiscalizados decomisados según departamento (Kg)" | seized controlled chemical inputs (drug precursors; not mining-specific) | 2019-2025 | department | annual | XLSX | yes | `insumos_quimicos_fiscalizados_decomisados_departamento_2019-2025.xlsx` |
| F | OEFA, datosabiertos.gob.pe "Coordinación con las Fiscalías Especializadas en Materia Ambiental" | prosecutors' information requests to OEFA, by sender | 2019-2025 | sender (e.g. "FEMA MADRE DE DIOS") | per request | XLSX | yes | `oefa_pedidos_fiscalia_2019_2025_Pub.xlsx` |
| G | SERNANP, datosabiertos.gob.pe "Distribución gastos mantener ANP" | SERNANP budget by protected-area unit and activity (incl. "vigilancia y control") | **one snapshot**, cut-off 2023-05-25 | protected-area unit | snapshot only | XLSX | yes | `sernanp_distribucion_gastos_mantener_ANP.xlsx` |
| H | MINAM (2021), annex to DS 017-2021-MINAM "Plan Restauración" (FAOLEX copy faolex.fao.org/docs/pdf/per206467anx.pdf) | DIRMEAMB interdictions by district, detainees, seizures; FFAA personnel and bases; FFAA seizures; MPFN prosecutions and convictions; SUNAT checkpoint controls | 2019-2020 (FFAA personnel 2019-2021) | department; **district** for 2019 interdictions | annual | PDF | yes | `pdf/minam_plan_restauracion_anexo_DS017-2021-MINAM_faolex_per206467anx.pdf` |
| I | MINAM (2016), "La lucha por la legalidad en la actividad minera (2011-2016)", Informes sectoriales, Tabla 15 (source ACAFMIRA, Oficio 0198-2016-PCM/ACAFMIRA/04) | interdiction operations by region | 2013-May 2016 | region | annual | PDF | yes | `pdf/minam_2016_la_lucha_por_la_legalidad_en_la_actividad_minera.pdf` |
| J | DAR (Vásquez & Vara 2023), "Desafiando la legalidad y la justicia: minería ilegal en Madre de Dios" | secondary text: 107 interdictions in MdD 2013-2017 (citing MINEM via Vásquez 2019, Wayka) | 2013-2017 total | MdD | 5-year total | PDF | yes | `pdf/DAR_2023_Mineria-ilegal-en-Madre-de-Dios-version-final.pdf` |
| K | PCM balances reported in the press (Andina, El Peruano, Energiminas, Caretas, RPP) | interdiction operations, value destroyed | 2024-2026, scattered periods | national; MdD for some periods | weekly, monthly, annual | HTML news | yes (pages only, no data file) | none |
| - | MININTER "Denuncias policiales registradas" (SIDPOL) | only 7 aggregated categories (Robo, Hurto, Otros...); **no mining category** | 2018-2026 | district | monthly | CSV | yes | downloaded, checked and **deleted** (27 MB, no relevant content) |
| - | Observatorio de Minería Ilegal (observatoriomineriailegal.org.pe) | lists of formalised, sanctioned and sentenced miners; commission minutes; no interdiction statistics on the home page | - | - | - | HTML (curl blocked by mod_security, 406; opened with WebFetch) | page yes, no dataset found | none |
| - | MININTER Estrategia Nacional al 2030 (DS 003-2025-IN, cdn.www.gob.pe/uploads/document/file/8212554/6863361-003-2025-in.pdf) | 4-page decree only; the strategy document and the territorial diagnoses (which reportedly map interdictions by region) were not found | - | - | - | PDF | decree yes | not kept (no numbers) |
| - | DS 017-2021-MINAM decree (faolex per206842.pdf) | 5-page decree, no numbers | - | - | - | PDF | yes | not kept |
| - | Defensoría (Informe Defensorial 167, 2012-2014), Contraloría, SERNANP patrol reports, Plan Restauración half-year monitoring reports (RM 209-2021-MINAM), Dethier et al. 2023 supplementary data, MINEM REINFO | not found or not opened | | | | | | none |

Not found anywhere on datosabiertos.gob.pe: "interdicción", "minería ilegal", REINFO, DICAPI, FEMA operations, SERNANP patrols (portal searches run 2026-10-12).

## 2. Yearly numbers for Madre de Dios (each with its source)

### 2a. Open series (computed from the raw files)

| Year | PP 0128 devengado in MdD, soles (A) | MdD share of PP 0128 national devengado (A) | Complaints art. 307-A in MdD (B) | Complaints art. 307-E (B) | All minería ilegal complaints 307-A to E (B) | FEMA "materia ambiental" complaints filed, MdD (C) |
|---|---|---|---|---|---|---|
| 2015 | 2,316,668 | 8.2% | | | | |
| 2016 | 235,822 | 0.5% | | | | |
| 2017 | 1,010,098 | 1.8% | | | | |
| 2018 | 651,901 | 1.2% | | | | |
| 2019 | **31,120,611** | 33.7% | | | | 1,509 |
| 2020 | 20,246,451 | 31.5% | 74 | 350 | 434 | 852 |
| 2021 | 9,665,775 | 14.3% | 231 | 182 | 428 | 1,074 |
| 2022 | 7,751,438 | 11.7% | 447 | 139 | 587 | 1,108 |
| 2023 | 7,033,425 | 9.0% | 483 | 134 | 617 | 1,102 |
| 2024 | 6,335,330 | 7.1% | 475 | 142 | 618 | 1,075 |
| 2025 | 5,008,539 | 4.3% | 413 | 154 | 581 | 1,152 |
| 2026 (part) | 20,617,616 (to ~Oct) | 19.2% | 604 (Jan-Aug) | 145 | 1,031 | 1,007 (Jan-Aug) |

Notes on (A): PIM (modified budget) in MdD was 32,904,750 in 2019 and 39,604,173 in 2026. "Departamento (Meta)" records where the spending target is located. National units (DIRMEAMB, the Ministerio Público, FFAA HQ) book most of the money under **Lima** (e.g. 2019 Lima devengado 50.6 M of 92.3 M), so the MdD figure is a lower bound on spending for MdD. Check against the site: 2019 national PP 0128 row shows PIM 97,816,076 and the MdD row shows devengado 31,120,611. Both were read off the saved HTML and match the screen output.
Notes on (B): the per-file "fecha_corte" differs (2020-2022 files cut 15/06/2023; 2024 file 31/10/2025), so later revisions are possible. 307-B jumps to 280 in Jan-Aug 2026 (after DL 1695, Jan 2026). These are complaints filed, not interdictions.
Notes on (C): includes all environmental crimes (illegal logging, wildlife), not mining only.

(D) DIRMEAMB "OPERATIVOS" (national, all environmental crimes): 2023 = 8,500; 2024 = 8,365 (monthly rows). From 2025 the file switches to daily rows (730 rows in 2025), so the sums are not comparable across the break. No Madre de Dios split. Not usable for zones.
(E) DEVIDA controlled chemical inputs seized in MdD (kg): 2019 2,311; 2020 247; 2021 3,969; 2022 11,482; 2023 9,962; 2024 25,163; 2025 17,952. These are drug-precursor seizures and only loosely related to mining.
(F) OEFA requests from MdD senders (FEMA, Fiscalía Tambopata, PNP...): 2019 4; 2020 2; 2021 4; 2022 19; 2023 14; 2024 33; 2025 23. Too small to use.

### 2b. Official counts in PDF reports

| Year | Number | Source and verbatim quote |
|---|---|---|
| 2013 | **49** interdiction operations in MdD (national 77) | MINAM 2016 (I), p. 159, Tabla 15 "Operativos de interdicción llevados a cabo por ACAFMIRA 2013 - mayo 2016": row "Madre de Dios 49 22 28 1"; "Total 77 54 62 9" |
| 2014 | **22** (national 54) | same table |
| 2015 | **28** (national 62) | same table. Same report p. 163: "con el apoyo logístico del SERNANP se llevaron a cabo 4 interdicciones a cargo de la FEMA, DICAPI y la PNP durante todo el año 2015" (Tambopata NR) |
| 2016 (Jan-May) | **1** (national 9) | same table. p. 171: "sumando hasta la fecha 9 acciones interdicción en la Reserva Nacional Tambopata y su zona de amortiguamiento" (DICAPI from the Azul post) |
| 2013-2017 | 107 in MdD (5-year total) | DAR 2023 (J), section 4.2 "La interdicción en el delito de minería ilegal": "solo entre el 2013 y 2017 se llevaron a cabo 107 operativos de interdicción exclusivamente en Madre de Dios (Vásquez, 2019)". Secondary, citing MINEM through a Wayka article |
| 2019 | **198** DIRMEAMB interdictions: Tambopata 195, Las Piedras 1, Laberinto 1, Inambari 1 | Plan Restauración annex (H), p. 34, Tabla 3, "Fuente: DIRMEAMB-PNP". The table header says "Provincia", but Las Piedras, Laberinto and Inambari are districts and Tambopata is both a province and a district, so the zone split is ambiguous. "el total de operativos realizados en Madre de Dios, durante los años 2019 y 2020, asciende a 429 operativos" |
| 2020 | **231** (all Tambopata) | same: "En el año 2020, las acciones se concentraron en la Provincia de Tambopata con 231 operativos, 36 operativos más que en el año 2019" |
| 2019 / 2020 | detainees MdD: 170 / 66 | (H) p. 34-35, Tabla 4: 2019 Tambopata 130 (actos preparatorios) + 29 (307-A) + 11 (non-metallic) = 170; 2020 = 66 |
| 2019 / 2020 | DIRMEAMB seizures, Tambopata: fuel 23,527 / 12,702 gal; machinery 50 / 37 units | (H) p. 35, Tabla 5, "Fuente: DIRMEAMB" |
| 2019 / 2020 / 2021 | FFAA personnel supporting: **690 / 672 / 887** | (H) p. 36, Tabla 6 "Número de efectivos FFAA - 2019 a 2021", "Fuente: MINDEF". Also: "en el año 2019 se contó con el apoyo de 690 efectivos; en el 2020 con 672 efectivos y al año 2021, vienen desempeñándose 887 efectivos" and about 840 Navy personnel. Bases: 4 in 2019 (Alfa, Bravo, Charlie, Azul), 5 in 2020 (+Eco), 2021 Azul closed and Correntada added |
| 2019 | FFAA seizures: "1701 motores, 274 caballetes, 112 balsas dragas, 811 balsas, 128 dragas, 1160 tolvas ..."; "en el 2019 se destruyó 316 campamentos" | (H) p. 38-39 |
| 2020 | FFAA seizures: "466 motores, 208 caballetes, 36 balsas de draga, 396 balsas, 19 dragas, 389 tolvas ..."; "en el 2020, 232 campamentos" | (H) p. 38-39 |
| 2019 / 2020 | MPFN FEMA MdD prosecuted: 107 / 76; convicted: 97 / 15 | (H) p. 39-40, Tablas 7-8, "Fuente: MPFN" (the column header in Tabla 7 is mislabelled "condenados") |
| 2019 / 2020 | SUNAT checkpoint interventions MdD: 158,063 / 83,305 | (H) p. 42, Tabla 9; Palmeras checkpoint (Inambari) 85,042 / 83,305 |
| 2019 (Mercurio) | 1,200 police, 300 military, 70 prosecutors | (H) p. 33: "la participación de más de 1,200 policías, 300 militares y 70 fiscales" |

### 2c. Press balances (pages opened; they cite the PCM; not machine-readable)

| Period | Number | Source |
|---|---|---|
| Feb 2019-Feb 2020 | "6000" detained; "más de 1500 procesos de investigación"; 3 bases with "300 militares y 300 policías" | Actualidad Ambiental, 19 Feb 2020, actualidadambiental.pe/madre-de-dios-cuales-son-los-avances-a-un-ano-del-megaoperativo-contra-la-mineria-ilegal |
| 2023 (early) | "Solo en Madre de Dios se realizan unos 25 operativos al mes"; FEMA prosecutors 3 (2019-21), 5 (2022), "ahora solo se cuenta con 2 fiscales" | Actualidad Ambiental, 2 Mar 2023, actualidadambiental.pe/en-madre-de-dios-solo-existen-dos-fiscales-para-luchar-contra-la-mineria-ilegal |
| 2019 vs 2024 budget | PP "Reducción de la minería ilegal" "recibió S/ 119 millones" (2019), "recibirá S/ 79 millones" (2024) (IPE / El Comercio) | Actualidad Ambiental, 18 Dec 2023, actualidadambiental.pe/mineria-ilegal-operativos-no-tienen-efecto-esperado-y-ejecutivo-ha-reducido-presupuesto-para-combatir-este-delito/ (different budget concept from the MEF figures in table 2a) |
| 1-24 Aug 2024 | MdD 19 interdictions, nearly S/ 57 M (national 31) | El Peruano, 26 Aug 2024, elperuano.pe/noticia/251205-ejecutivo-intensifica-lucha-contra-la-mineria-ilegal |
| 2024 (to 28 Jul) | national "481 operativos de interdicción"; MdD = region with the most, no number | Energiminas, 9 Oct 2024, energiminas.com/2024/10/09/pcm-interdicciones-golpean-con-mas-de-s-2000-millones-a-la-mineria-ilegal |
| 2024 (year) | national "más de 720 operativos de interdicción", "más de S/ 2230 millones" | Energiminas, 9 Jan 2025, energiminas.com/?p=26698 |
| Jan 2025 | national "89 operativos de interdicción"; MdD "40 intervenciones (44 % del total)"; S/ 119,322,081 | RPP, updated 9 Feb 2025, rpp.pe/...noticia-1615159 |
| 25-31 Jan 2025 | MdD: "la PNP realizó ocho operativos y la Dicapi, tres" (national 24) | Andina, 2 Feb 2025, andina.pe/agencia/noticia-pcm-destruyen-materiales-mas-s41-millones-24-operativos-contra-mineria-ilegal-1017219.aspx |
| Jan-15 Dec 2025 | national "más de 1,000 operativos"; **MdD "276 operativos"**, S/ 1 095 M | Caretas, 19 Dec 2025, caretas.pe/politica/ofensiva-nacional-contra-la-mineria-ilegal/ |
| 2024 vs 2025 vs 2026 | national average 62 operations/month (2024), 86 (2025), "supera las 130" (2026); budget S/ 70 M (2025), S/ 178 M (2026) | El Peruano, 5 May 2026, elperuano.pe/noticia/295039-... |
| Jan-Feb 2026 | MdD "123 operativos", S/ 251 M (national 243) | Energiminas, 17 Mar 2026, energiminas.com/?p=43586 |
| 2026 (to mid-May) | MdD (Tambopata NR area) "más de 75 operativos", "370 campamentos", "211 balsas tipo traca", "202 motores" | Caretas, 19 May 2026, caretas.pe/?p=808004 |
| snippet | "La mayor cantidad de interdicciones se reportaron en Madre de Dios con 546, seguido por Loreto con 77 ..." (period unknown) | Rumbo Minero Facebook post (snippet only, not opened) |
| snippet | 2023: "ejecutamos 729 operativos de interdicción a nivel nacional" (Boluarte speech) | search summary only |

Inconsistency to flag: the press counts mix "operativos", "intervenciones" and "interdicciones", and different agencies (PNP, DICAPI, FEMA). The 276 MdD operations in 2025 (Caretas) do not match the 40 in January 2025 alone (RPP), which would imply about 480/year, unless January was unusual. Treat press numbers as orders of magnitude.

## 3. Recommendation: which series can measure enforcement intensity?

1. **Over time, department level (best available, open, reproducible): MEF PP 0128 devengado in Madre de Dios, 2015-2025 (A).** It is official, annual, scrapeable without login, and it moves with the known enforcement waves: about S/ 0.2-2.3 M per year in 2015-2018, then **S/ 31.1 M in 2019** (Mercurio), 20.2 M (2020), 9.7 M (2021), then a slow fade to 5.0 M (2025), and a jump in 2026. It is a spending input, not an action count, and it is a lower bound because national units book under Lima. Use it as the "enforcement intensity" line in a timeline panel (description), and for the "delay" story: intensity fell steadily after 2020 while mining additions rose.
2. **Companion series: MPFN complaints for minería ilegal, art. 307-A + 307-E, 2020-2025 (B).** Annual, department level, but it starts after Mercurio and mixes enforcement effort with crime volume, so it is endogenous to mining. Good as a robustness line, not as a treatment measure.
3. **Interdiction counts (closest to "intensity"), patchy:** 49/22/28 (2013-15, ACAFMIRA), ~107 over 2013-17 (MINEM via DAR), 198/231 (2019/2020, DIRMEAMB), about 25/month (2023, press), 276 (2025 to 15 Dec, PCM via Caretas). Use these only as annotated points in the figure, citing each source. Do not build a continuous series by joining them: definitions and agencies differ.
4. **Zones (Tambopata BZ / La Pampa vs Amarakaeri vs corridor vs Huepetuhe):** no source gives zone-level counts. The only split is 2019 DIRMEAMB (195 Tambopata vs 1 each in Las Piedras, Laberinto and Inambari; Huepetuhe and Madre de Dios districts (Manu province) are not listed). The Plan Restauración annex also lists Cusco/Camanti (Amarakaeri BZ side) separately: Camanti prosecuted 90 (2019) and 164 (2020) under 307-A, against 43/53 in MdD FEMA. That is evidence that the Amarakaeri side was also treated. To compare zones by intensity, keep the **legal/geographic proxies already in the repo** (enforcement_timeline.md: Mercurio bases in La Pampa; emergency decree districts from Apr 2023; navy posts on the Malinowski and Inambari rivers) and say clearly that intensity is not measured by zone.
5. **What would fix it (brief part 4c):** a transparency request (Ley 27806) to DIRMEAMB-PNP / PCM Alto Comisionado for interdictions by district and month 2015-2025 with geo-coordinates. The PCM clearly holds these, because the press releases give weekly counts by department. Also the MINDEF/CCFFAA operation logs, and the MINAM half-year Plan Restauración monitoring reports (RM 209-2021-MINAM), which I could not locate online.

Caveat for the brief: every enforcement series here is **endogenous** (the state sends more enforcement where mining is worse) and partly **measured with error** (definitions change; budget is booked by the location of the spending target, not the place of the action). Label any use as description.

## 4. Provenance of raw files (access date 2026-10-12, sha256 via `shasum -a 256`)

| File (under `data_raw/enforcement_peru/`) | URL | sha256 |
|---|---|---|
| mef_pp0128/mef_consulta_amigable_PP0128_departamento_2015.html | https://apps5.mineco.gob.pe/transparencia/Navegador/Navegar_7.aspx?y=2015&ap=ActProy, then POST "Programa Presupuestal", select 0128, then "Departamento (Meta)" (same for each year) | 30b941440afbf7e1666a09ecdc425a632f0440b4813d389e4bf197a56f9a3b5f |
| ..._2016.html | same, y=2016 | 2952b407c4ee449a40e78a9706bcb4bb01b79ca38bac6f7ecc0281e1c94ed9ac |
| ..._2017.html | y=2017 | 77cff2777f626a95f10338eba38df0a9243b59fe39a42e9e2409054f8acef006 |
| ..._2018.html | y=2018 | cc0045ecc4c77f2c757a943ca8ecb5f656495c43acd8451ff10c84a9c01383de |
| ..._2019.html | y=2019 | 0b5ecb1132ecd38c4de008a7f97cc542f80724de1f3688679bab2f774c91653b |
| ..._2020.html | y=2020 | eabe3084d7c38058f58f8802c9fd013aa14886d027f1e7748c43dded5c835f92 |
| ..._2021.html | y=2021 | ba7260cac70fb30c24819560d2b44a942f655b96caea501aae6bc37a64890578 |
| ..._2022.html | y=2022 | 87f8b838a65c166a06e7aadba562fbb822331c03084ef46090f7718603bcba75 |
| ..._2023.html | y=2023 | 70e8c11f55171682cfa0a79401909e51ada9e4e1e3161d14080a0bcff0c3e2a1 |
| ..._2024.html | y=2024 | 3d1135aa5e5a9b72ce07995f9c8c29918e53f0b550d3439224c67ebf8970b29a |
| ..._2025.html | y=2025 | c7c03eb0edbdeef405b211347cefeabf09fd9e2e9880b023534db1767d1d5266 |
| ..._2026.html | y=2026 (year to date) | 2fc14c9a7fca3cfd99f04c58c6acf63364541e256f8d4c1335b6bbc92312be75 |
| mpfn_delitos_denunciados/delitos denunciados 2020.csv | https://www.datosabiertos.gob.pe/sites/default/files/delitos%20denunciados%202020.csv | a3989f29340fbc13b52d3a67c9ab7282463f730eed5f0f59f04784a137c6a3f5 |
| mpfn_delitos_denunciados/delitos denunciados 2021.csv | .../delitos%20denunciados%202021.csv | 839d207ac0910a32865421959bdc54c596dc9b36dd3f1c32e0df04f1aad79a0e |
| mpfn_delitos_denunciados/delitos denunciados 2022.csv | .../delitos%20denunciados%202022.csv | a8b91331356984b5c4eeb7edc852b06c55346be0f2fe685ca45c13d95616c68b |
| mpfn_delitos_denunciados/delitos-denunciados-2023_0.csv | .../delitos-denunciados-2023_0.csv | ea1ed66dec578c40a4a20a91d856f2ef8c8834081f31efdc017e1ade3af674e6 |
| mpfn_delitos_denunciados/delitos-denunciados-2024.csv | .../delitos-denunciados-2024.csv | c8977c46c52d2a284b0e500c37c0afc2308707d5cc662783151149f87915c297 |
| mpfn_delitos_denunciados/BD-delitos-denunciados-2025-12.csv | .../BD-delitos-denunciados-2025-12.csv | 78f48061dcfb7a464ceeb8179b011358e8731cb9042c3168dba80387df270779 |
| mpfn_delitos_denunciados/DA-BD-delitos-denunciados-2026-08.csv | .../DA-BD-delitos-denunciados-2026-08.csv | 80092e364e5d9b26bd8ccb04e4e3194f9b36a6048b1bec29f08c9a2f63763127 |
| mpfn_delitos_denunciados/diccionario de datos - Delitos Denunciados.xlsx | .../diccionario%20de%20datos%20-%20Delitos%20Denunciados.xlsx | c9dad9f6e138e95b9a0535227b820df0c98edf8888d3c2f7b07fa7631280c447 |
| mpfn_casos_fiscales/BD-casos-fiscales-2019.csv | https://www.datosabiertos.gob.pe/sites/default/files/BD-casos-fiscales-2019.csv | 123db3f4676a9bc80d1473632f68b98e22873b67925b93f35c51f63c0bf1cbfe |
| mpfn_casos_fiscales/BD-casos-fiscales-2020.csv | .../BD-casos-fiscales-2020.csv | 0227b33abc56ea55561e327f775e57bb8fefdc16bafa298f389297710f26b3bd |
| mpfn_casos_fiscales/BD-casos-fiscales-2021.csv | .../BD-casos-fiscales-2021.csv | 31de7c9c94324609edb131b3e2af1c8dce34982e0e2c19280b857029bd9db33b |
| mpfn_casos_fiscales/BD-casos-fiscales-2022.csv | .../BD-casos-fiscales-2022.csv | b3c4e27bd16a2696e7a777917b5979833aa39a46b2e2a955b1d6843971b9e5a6 |
| mpfn_casos_fiscales/BD-casos-fiscales-2023.csv | .../BD-casos-fiscales-2023.csv | 903ae51c5eb198a1ae233a68df3fc35ae98f7118cf9b413fdfa79949ffb2fae1 |
| mpfn_casos_fiscales/BD-casos-fiscales-2024.csv | .../BD-casos-fiscales-2024.csv | 56b3df4e9095a9c5a225477b36d1315871dcd9ebe17d8eef0807289de715c084 |
| mpfn_casos_fiscales/BD-casos-fiscales-2025-12.csv | .../BD-casos-fiscales-2025-12.csv | df31f71454dd7882d5c7dfef4d9eb7f26ca460db2d44738447026b37398d6c6a |
| mpfn_casos_fiscales/DA-BD-casos-fiscales-2026-08.csv | .../DA-BD-casos-fiscales-2026-08.csv | 30a8c7147a5fac2adff090d3bff47a043683104a872eb4ce7bf110c87db765f6 |
| mpfn_casos_fiscales/diccionario de datos - Casos Fiscales.xlsx | .../diccionario%20de%20datos%20-%20Casos%20Fiscales.xlsx | 53939e54f51473ce76e1e52448b2177dfa334754ee6c63e3983b7f911d4d2edf |
| mininter_produccion_policial_2022-10_2026-07.csv | https://www.datosabiertos.gob.pe/sites/default/files/DATASET%20Produccion%20Policial%20Octubre%202022%20a%20Julio%202026.csv | add72c210e9d946943acb3faf47f5b85d3f9a3f9682f5822e69be28ad52f11d1 |
| DICCIONARIO_DATOS_Produccion_Policial.xlsx | https://www.datosabiertos.gob.pe/sites/default/files/DICCIONARIO_DATOS_Produccion_Policial.xlsx | 935c21ca3cacb0e980d970df66dee167916526d7dc1b17c7eb30c76f3a2b133a |
| insumos_quimicos_fiscalizados_decomisados_departamento_2019-2025.xlsx | https://www.datosabiertos.gob.pe/sites/default/files/-Volumen%20de%20Insumos%20Qu%C3%ADmicos%20Fiscalizados%20decomisados%20seg%C3%BAn%20departamento%20%28Kg%29%2C%202019%20-%202025.xlsx | f748878b58a4416783975c1c94ae6e85c908091957523ad58b7ec19b5971c118 |
| oefa_pedidos_fiscalia_2019_2025_Pub.xlsx | https://www.datosabiertos.gob.pe/sites/default/files/Pedidos_fiscalia_2019_2025_Pub.xlsx | 5a28883fb80f9f4a558e038ca5cf5245c3446cf858465d019c24a471ead3385e |
| sernanp_distribucion_gastos_mantener_ANP.xlsx | https://www.datosabiertos.gob.pe/sites/default/files/Distribuci%C3%B3n%20gastos%20mantener%20ANP.xlsx | 37e36dbc4de3cd42b6198425a344adb01b2b9de64b7012f034977a27505e5481 |
| pdf/minam_plan_restauracion_anexo_DS017-2021-MINAM_faolex_per206467anx.pdf | https://faolex.fao.org/docs/pdf/per206467anx.pdf | 0257002d07165ca14a7a954ad5523002c7d841a17a4e4111ab595ccdcb86679e |
| pdf/minam_2016_la_lucha_por_la_legalidad_en_la_actividad_minera.pdf | https://www.minam.gob.pe/informessectoriales/wp-content/uploads/sites/112/2016/02/12-La-lucha-por-la-legalidad-en-la-actividad-minera.pdf | d19baa0abf835eaf19e2a4115bb2daf639de3e9633cb8f797fadc4eac00b40ce |
| pdf/DAR_2023_Mineria-ilegal-en-Madre-de-Dios-version-final.pdf | https://dar.org.pe/wp-content/uploads/2024/08/Mineria-ilegal-en-Madre-de-Dios-version-final.pdf | 699909652a56ab15a165d44e016574820b3154439479bc8e4233b882eea1fb44 |

Extraction details. MPFN: filter `articulo` starting with "307-" and `distrito_fiscal == "MADRE DE DIOS"`, then sum `cantidad`. The 2020 files are UTF-8 with BOM. Casos fiscales: `especializada`/`especilizada` (the column name changes spelling) contains "MATERIA AMBIENTAL", `tipo_caso == "DENUNCIA"`, sum `ingresado`. MEF: row "17: MADRE DE DIOS", column 6 = Devengado. None of this is in `code/` yet. If the team uses a series, add a loader plus a `check(...)`, e.g. MdD PP 0128 devengado 2019 = 31,120,611 soles (as shown on the Consulta Amigable screen).
