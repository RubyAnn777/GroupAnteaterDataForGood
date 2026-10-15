# MAAP citations (Q2, Peru)

Access date: 2026-10-10. Fetch method: Firecrawl `firecrawl_scrape` (markdown, onlyMainContent), 4 scrapes + 1 search = 5 Firecrawl calls. Quotes below are copied from that markdown output.

**Raw HTML NOT saved, no sha256.** `curl` gets HTTP 403 from maapprogram.org (bot block) and web.archive.org returned empty bodies. Firecrawl returns content only into the session, not to disk. Firecrawl served #130 and #241 from its cache (cachedAt 2026-10-09), #193 and #208 live. TODO (human): save each page via browser "Save as" into `data_raw/maap/` and run `shasum -a 256`, then log in DOWNLOAD_LOG.csv.

**General caveat (method):** MAAP uses its own digitised/algorithmic mining-deforestation analysis (Planet imagery, LandTrendR, own polygons). These are NOT MapBiomas class 4.2 areas (except that #241 Graph 1 and Base Map list MapBiomas Peru among the data sources, mixed with CINCIA and ACA). Never add, subtract or compare MAAP hectares with MapBiomas hectares. MAAP #130 counts only "gold mining deforestation" (forest loss), the MapBiomas class counts mining land cover. Compare patterns/direction only, cite MAAP as qualitative evidence.

---
## MAAP #130
- **Reference:** Finer M, Mamani N (2020) "Illegal Gold Mining Down 79% in Peruvian Amazon, But Still Threatens Key Areas." MAAP: 130. (Page headline reads "Down 78%"; the page's own Citation line says "79%". Cite the headline number as 78% and note the inconsistency.) Published 1 Dec 2020.
- **URL:** https://www.maapprogram.org/gold-mining-peru/
- **Data/method:** Planet imagery 3 m (Planet Explorer), manually digitised mining deforestation at six sites, sites chosen from GLAD and Geobosques alerts. Before = Jan 2017 to Feb 2019 (26 months), after = Mar 2019 to Oct 2020 (20 months); standardised to ha per month. "The area referred to as the 'mining corridor' is not included in the analysis because the issue of legality is more complex." Data updated through Oct 2020. Support: USAID Prevent.
- **Sha256:** not available (see top).

| Claim | Exact quote | Location |
|---|---|---|
| La Pampa total ha | "In La Pampa, we documented the dramatic loss of 4,450 hectares within the buffer zone of Tambopata National Reserve (Madre de Dios region) prior to Operation Mercury. Following the Operation, we confirmed the loss of 300 hectares." | Section "Base Map - 6 Major Illegal Gold Mining Sites" |
| La Pampa ha/month, -90% | "In La Pampa, the gold mining deforestation averaged 165 hectares per month prior to Operation Mercury. Following the Operation, the deforestation dropped to 17 hectares per month, an overall 90% decrease." | Section "Gold Mining Deforestation Trends", text under Table 1 |
| Headline results | "1) Gold mining deforestation decreased 90% in La Pampa ... 2) ... increased in three key areas - Apaylon, Pariamanu, and Chaspa - indicating that some miners expelled from La Pampa moved to surrounding areas. ... 3) Overall, gold mining deforestation decreased 78% across all six sites ..." | Intro, "four major results" list |
| Total persists | "We documented 1,115 hectares of gold mining deforestation across all six sites since Operation Mercury (but, compared to 6,490 hectares before the Operation)." | Intro, result 4 |
| Alto Malinowski | "we documented the loss of 1,558 hectares prior to Operation Mercury. Following the Operation, we confirmed the loss of 419 hectares." Rate: "dropped from 58 hectares per month to 23 hectares per month ..., an overall 60% decrease." | Base Map section; Trends section (Table 1 text). Located in buffer zone of Bahuaja Sonene NP |
| Camanti (Amarakaeri BZ) | "In Camanti, located in the buffer zone of Amarakaeri Commuanl Reserve, we documented the loss of 336 hectares prior to Operation Mercury. Following the Operation, we confirmed the loss of 105 hectares." Rate 12.5 to 6 ha/month, "54% decrease". | Base Map section; Trends section. NB: our comparison unit also fell here |
| Pariamanu (displacement) | "72 hectares prior ... 98 hectares" after; "increased from 2.8 hectares per month to 5 hectares per month ... an overall 87% increase." "the government conducted a major intervention in August 2020." | Base Map section; Trends section |
| Apaylon (displacement) | "In Apaylon, located in the buffer zone Tambopata National Reserve ..., 73 hectares prior ... 78 hectares" after; "2.8 hectares per month to 4 hectares per month ..., an overall 43% increase." Gov "a series of interventions ... during 2020." | Base Map section; Trends section |
| Chaspa (new front) | "Chaspa, located in the buffer zone of Bahuaja Sonene National Park (Puno region), represents a unique case of a new gold mining front that appeared following Operation Mercury. Starting in September 2019, we documented the deforestation of 113 hectares ..." (8.5 ha/month) | Base Map section; Trends section |
| Displacement interpretation | "some miners expelled from La Pampa moved to surrounding areas" | Intro, result 2 (MAAP's interpretation, not a causal test) |
| Operation scope | "The Operation initially targeted an area known as La Pampa, the epicenter of the illegal mining. In 2020, it expanded to surrounding critical areas." | Intro |
| Timeline | "In early 2019, the Peruvian government launched Operation Mercury" | Intro |
| Legal corridor | "The area referred to as the 'mining corridor' is not included in the analysis because the issue of legality is more complex." | Methodology |
| Figures | Image 1 (Pariamanu SkySat), Base Map, Table 1 (rates before/after, bar graphic), Images 2-6 (SkySat of Pariamanu, La Pampa north, Chaspa, Camanti) | captions |

---
## MAAP #193
- **Reference:** Yupanqui O, Quispe M, Novoa S, Castaneda C, Escalante E, Finer M, Mamani N (2023) "El retorno de minería ilegal en La Pampa (zona de amortiguamiento de la Reserva Nacional de Tambopata)." MAAP: 193. Published 28 Sep 2023. Page headline: "El Retorno de la Mineria Aurifera Ilegal en Zonas Degradadas de la Pampa ..." (Spanish; the English URL redirected to the Spanish page, so all quotes are Spanish and the English renderings below are mine, not MAAP's).
- **URL:** https://www.maapprogram.org/es/retorno-mineria-la-pampa-peru/ (English-slug URL used in search: https://www.maapprogram.org/2023/retorno-mineria-la-pampa-peru/)
- **Data/method:** NOT hectares of new deforestation. Counts of mining dredges ("dragas") and active settling ponds from SkySat 0.5 m (Aug 2023) vs 2021 study (Aug+Oct 2021, ACCA/USAID Prevent population estimate); Random Forest in Google Earth Engine for ponds. Measures re-activation on already-degraded land, so it is invisible to a "new deforestation" measure and, for MapBiomas, appears at most as re-mining. Supports our caveat that re-mining of old scars is hard to count.
- **Sha256:** not available.

| Claim | Exact quote | Location |
|---|---|---|
| Mercurio success | "Un logro significativo ... ha sido la importante disminucion de la deforestacion por minería ilegal en la zona critica conocida como La Pampa ... a traves de la exitosa Operacion Mercurio a principios de 2019." | Intro (accents omitted here) |
| Return on degraded land | "un significativo incremento de infraestructuras mineras y la actividad minera en areas previamente deforestadas por la minería ilegal, las cuales habian sido recuperadas por el gobierno peruano tras la Operacion Mercurio." | Intro |
| Dredges 148 to 598 | "se identificaron 148 dragas remanentes en espacios degradados. Dos años despues, en agosto de 2023, ... se han encontrado 598 dragas, un aumento de mas del 400%." Note: 2021 "coincidio con el fin de la Operacion Mercurio e inicio del Plan Restauracion". | Section "Incremento notable de infraestructuras mineras en La Pampa"; Mapa Base; Figura 2 |
| People | "En 2021, se estimaron 592 personas, mientras que en 2023 se estimaron 2,392 personas" (4 persons per dredge) | same section, Figura 2 |
| Active ponds | "en el año 2021 ... solo se tenia una superficie de 788 hectareas de pozas activas ... en el año 2023 ... incrementandose la superficie en 2,550 hectareas (un incremento de mas de 320% en solo dos años)" | Section "Analisis de las pozas residuales mineras", Figura 5. Ambiguous whether 2,550 is the increment or the new total; check against the figure before citing |
| Direction of spread | "han ido avanzando de norte a sur, en dirección a la Reserva Nacional Tambopata" | Section "Analisis de densidad minera 2021-2023", Figura 3 |
| Mercury | pools "donde se concentran sedimentos ... y elementos contaminantes utilizados durante la extraccion del oro (Ej: mercurio)" | Section on residual ponds (supports "satellites cannot see mercury") |

---
## MAAP #208
- **Reference:** Finer M, Mamani N (2024) "Gold mining in the southern Peruvian Amazon, summary 2021-2024." MAAP: 208. Published 8 May 2024 (page modified 2026-02-04).
- **URL:** https://www.maapprogram.org/maap-208-gold-mining-in-the-southern-peruvian-amazon-summary-2021-2024/
- **Data/method:** LandTrendR on NICFI-Planet monthly mosaics (4.7 m), forest loss Jan 2021 to Mar 2024, baseline 2016-2020 removes older clearings, manual separation of mining vs other forest loss. Covers the Mining Corridor and outside it. Not MapBiomas.
- **Sha256:** not available.

| Claim | Exact quote | Location |
|---|---|---|
| Timeline | "Illegal gold mining reached crisis levels between 2017 and 2018 in the area known as La Pampa ... In early 2019, the Peruvian government implemented Operation Mercury ... This operation was later replaced (in 2021) by the Restoration Plan, which included interventions in other critical mining areas of the Madre de Dios region" | Intro |
| Total | "we recorded a total mining deforestation of 30,846 hectares" (Jan 2021 to Mar 2024; 28,292 ha in 2021-2023 and 2,554 ha in Q1 2024, note 8) | Intro, note 8 |
| Legal corridor share | "three-quarters (74%) of the deforestation occurred within the official Mining Corridor ... In other words, the vast majority of mining deforestation is not necessarily illegal"; "within the Mining Corridor, representing 73.8% of the total (22,756 hectares)" | Intro; Base Map section; Table 1 |
| Probable illegal | "The remaining one-quarter (26%) ... corresponds to probable illegal mining ... prohibited areas outside the Mining Corridor, such as protected areas, their buffer zones, territories of Native Communities, and bodies of water." | Intro |
| Buffer zones | "mining deforestation of 2,439 hectares (7.9%) in buffer zones of Protected Areas. The most affected are Tambopata National Reserve ..., Bahuaja Sonene National Park, and Amarakaeri Communal Reserve." | Base Map section, Table 1 |
| Inside PAs | "mining within the actual Protected Areas has been effectively controlled by the Peruvian government, through ... SERNANP." (2021-24; contradicted by #241 for 2025-26) | Base Map section |
| Native communities (outside buffer) | "10 Native Communities ... 4,494 hectares" (14.6%); San Jose de Karene 1,099 ha, Barranco Chico 1,008 ha, Tres Islas 827 ha | Base Map section |
| La Pampa | "the expansion of mining deforestation has been effectively stopped after Operation Mercury. A recent report (MAAP #193), however, showed a large increase in mining activity in previously deforested areas of La Pampa." | Base Map section, last paragraph |
| Operations in 2022-24 | "5 government-led operations between 2022 and 2024, in three communities: Barranco Chico, Kotsimba and San Jose de Karene"; Barranco Chico deforestation "decreased between 2021 and 2024, likely due to these types of interventions" | Section "Monitoring & Control of Native Communities by FENAMAD", Figure 2 |
| Pariamanu | "198 hectares in Brazil nut forestry concessions located in the Pariamanu area" | Base Map section |
| Corridor definition | Mining Corridor = "Zone of small mining and artisanal mining" (Legislative Decree 1100); categories formal / informal ("an administrative infraction, but not a crime") / illegal | Note 3 |
| Figures | Figure 1 (Mangote), Base Map, Table 1 (category table, image only, numbers not in text), Figure 2 (Barranco Chico) | captions |

---
## MAAP #241
- **Reference:** Pacsi R, Novoa S, La Torre S, Balbuena H, Finer M, Santana A, Castillo H (2026) "Rapid Expansion of Illegal Gold Mining in Tambopata National Reserve (Southern Peruvian Amazon)." MAAP: 241. Published 10 May 2026.
- **URL:** https://www.maapprogram.org/mining-peru-tambopata/
- **Data/method:** Historical mining deforestation in Madre de Dios from CINCIA (1984-2019), MapBiomas Peru (2020), Amazon Conservation/ACA (Jan 2021 to Mar 2024); LandTrendR on NICFI mosaics (4.7 m) Apr 2024 to Jul 2025, monitoring Aug 2025 to Feb 2026; SkySat 0.5 m for structures. Graph 1 is therefore a spliced series from three producers: do not treat as one consistent series or compare with our MapBiomas Collection data.
- **Sha256:** not available.

| Claim | Exact quote | Location |
|---|---|---|
| Mercurio date | "major government operation known as 'Operation Mercury' in February 2019, and a subsequent initiative known as the 'Restoration Plan' in 2021" | Intro |
| 2017-18 operations (pre-period not enforcement-free) | "During 2017 and 2018, a series of operations and interdictions were launched in the region that helped combat the advance of illegal mining (AIDER, 2021)." | Section "Annual Mining Deforestation in Tambopata NR", event 1, under Graph 1 |
| Mercurio effect | "Operation Mercury ... resulted in a major reduction that same year compared to 2016 and 2017 ... the success of Operation Mercury led to a substantial reduction in mining expansion within the Tambopata National Reserve and its buffer zone (MAAP #104, MAAP #121)." | same, event 1 |
| COVID 2020 | "In 2020, due to the COVID-19 pandemic, difficulties arose regarding the execution of operations and patrols within Tambopata National Reserve and its buffer zone, leading to a reduction in police and military presence in key sectors (AIDER, 2021; DAR, 2023; Vadillo, 2022). Consequently, instances of illegal miners re-entering Tambopata were recorded (Romo, 2020)." | event 2 |
| Plan Restauracion 2021 | "the 'Restoration Plan' - a series of military interventions conducted in 2021 in critical illegal mining zones ... - also resulted in a major decrease in mining deforestation that same year, compared to the previous year." | event 2 |
| Inside Tambopata NR 2025-26 | "illegal gold mining has resumed an alarming expansion within Tambopata National Reserve, primarily during the second half of 2025 and early 2026 (see Graph 1)"; "a total area of 500 hectares was deforested due to illegal mining in the northern part of the Reserve along the Malinowski River" | Intro; Base Map section |
| Split | "500 hectares ... during the second half of 2025 (431 hectares) and early 2026 (69 hectares through February)" | Base Map section |
| Exceeds pre-Mercurio | "(500 hectares), surpassing the figures registered during the critical years of 2016 and 2017 that led up to Operation Mercury." (Note: 500 ha over ~8 months vs annual figures) | event 3, under Graph 1 |
| Gold price | "This sudden increase was likely driven by the exponential rise in the international price of gold (see red line in Graph 1)." | event 3 (MAAP's hypothesis; confounder for us) |
| Case studies | A Isla Cordoba 106 ha (Jan 2025 to Jan 2026); B Sector A4 101 ha (Feb 2025 to Feb 2026); C Sector A7 25 ha; D Isla Correntada 111 ha (sum 343 ha, not 500; different windows, so don't add) | Case Studies A-D, Figures A1-D3 |
| Structures | "183 mining structures ... and 67 mining camps across five mining zones" (Feb 2026); "around 1,000 people" | Intro |
| Emergency | "state of emergency in Madre de Dios, in effect uninterruptedly since April 7, 2023, ... Supreme Decree No. 046-2023-PCM ... districts of Tambopata, Inambari, Las Piedras, and Laberinto ... Madre de Dios and Huepetuhe in the Manu province." Extended every 60 days; "Supreme Decree No. 017-2026-PCM ... until April 6, 2026". | Section "Public Policies", 1. State Response |
| 2026 operations | Interdiction "carried out between January and March 2026"; "340 mining camps were dismantled. Nevertheless, satellite monitoring indicates that these actions failed to reverse the expansion" | same, 1. |
| Navy withdrawal | "the special units of the Peruvian Navy, which maintained a permanent presence at control and surveillance posts along the Malinowski River ..., were withdrawn during 2025 due to a lack of funding." | 2. Structural Limitations |
| Legislative | REINFO fifth extension (Law 32537, 26 Dec 2025, until end 2026); Legislative Decree 1695 (20 Jan 2026) stiffens penalties | 3. Legislative Setbacks; 1. |
| Legal corridor | No explicit statement about the Mining Corridor found in this page text (searched). | n/a |
| Graph/figures | Image 1; Graph 1 (annual mining deforestation 2016-2025 with gold price line; image only, annual values not in text); Base Map; Figures A1-D3 | captions |

---
## Assuncao, Gandour & Rocha (2023) - opened
- **Reference:** Assuncao J, Gandour C, Rocha R (2023) "DETERring Deforestation in the Amazon: Environmental Monitoring and Law Enforcement." American Economic Journal: Applied Economics 15(2): 125-156. DOI: 10.1257/app.20200196. Page: https://www.aeaweb.org/articles?id=10.1257/app.20200196 (opened 2026-10-10 via WebFetch, which summarised the page).
- **Key sentence (abstract, as relayed):** "Findings indicate that monitoring and enforcement effectively curb deforestation." Method: cloud cover that blocks DETER detection used as an instrument for the presence of environmental authorities. Full abstract not read verbatim; read the paper before citing more.
- Note: it concerns Brazilian Amazon deforestation, not mining, and not spillovers.
