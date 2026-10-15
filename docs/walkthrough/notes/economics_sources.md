# Economics of gold mining in Madre de Dios: cited parameters for an "informed speculation" section

Compiled 2026-10-13 (access date for every web source below, unless marked otherwise). Agent run; nothing committed, no other repo file edited.

**How to read the labels**
- **opened** = I opened the page or PDF and read the passage quoted. For PDFs, "p." is the PDF page; the printed page is given where it differs.
- **snippet only, verify** = the number appeared only in a search-result snippet. Do not cite it without opening the source.
- **team note** = taken from `docs/walkthrough/notes/qualitative_background.md` or `legality_data.md` (opened by an earlier run on 2026-10-12) and not re-opened today.
- **derived** = our own arithmetic from cited inputs. It is not a published number, so label it as our calculation in the brief.
- Three Peruvian PDFs were re-read today from the local copies in `data_raw/enforcement_peru/pdf/` (text extracted with pypdf):
  - **[PR21]** MINAM (2021), *Plan Restauración: Plan integral frente a la minería ilegal* (annex to DS 017-2021-MINAM). https://faolex.fao.org/docs/pdf/per206467anx.pdf
  - **[MINAM16]** MINAM (2016), *La lucha por la legalidad en la actividad minera (2011-2016)*. https://www.minam.gob.pe/informessectoriales/wp-content/uploads/sites/112/2016/02/12-La-lucha-por-la-legalidad-en-la-actividad-minera.pdf
  - **[DAR23]** Vásquez & Vara (2023), *Desafiando la legalidad y la justicia: minería ilegal en Madre de Dios*, DAR. https://dar.org.pe/wp-content/uploads/2024/08/Mineria-ilegal-en-Madre-de-Dios-version-final.pdf (printed page = PDF page − 2)
- A fourth PDF is stored in `data_raw/literature/CSF_2023_Metodologia_Valorizacion_Mineria_Ilegal_Oro_Peru.pdf` and logged in `DOWNLOAD_LOG.csv` (pages re-checked 2026-10-13 against that copy):
  - **[CSF-PE]** Gasparinetti, Bakker, Araujo, Macedo & Caller (CSF, for the World Bank/GEF ASL programme), *Metodología de Valoración de Impactos de la Minería Ilegal de Oro en la Amazonía Peruana* (PDF modified 2023-06-29), https://www.conservation-strategy.org/sites/default/files/field-file/Metodologia_Valorizaci%C3%B3n_Impactos_Miner%C3%ADa_Ilegal_Oro_Amazonia_Peruana.pdf, sha256 `92767cee2a450cf1b324693a1a7e834c44520e883787c685e944cb13fd1cafbf`. Page = PDF page (printed = PDF − 1).

**Scope warning.** Almost every economic number below is an **estimate** (IPE, CSF, CooperAcción, ministers' statements). The only **official statistics** are MINEM/BCRP declared production, SUNAT/MEF rules and budgets, and the MINEM REINFO register. Most numbers are **national**. Madre de Dios numbers are marked **MdD**.

---

## Summary table

| # | Parameter | Value | Range / alternatives | Source | Confidence |
|---|---|---|---|---|---|
| 1a | Gold recovered per hectare mined (alluvial, MdD) | **1.6–1.9 kg Au/ha** (2.5 m pit; Cuadro 3 sites Puquiri 1.6, Malinowski 1.7, Huepetuhe 1.9; the text on p.23 says "1.7 a 1.9") | 0.7–8.3 kg/ha (CSF Brazil default); ~1.9 kg per ha worked / ~2.5 kg per first-time ha implied by MINEM output, MdD 2016-18 (derived, `eco_implied_kg_ha_*`, §1c); ~12.5 kg/ha in-situ (derived from an opinion piece's 0.25 g/m³ × 5 m) | CSF-PE (2023) PDF p.22, Cuadro 3 | medium (model assumption built on AGC 2017 grades; CSF found **no grades for suction-pump mining**, p.22) |
| 1b | Grade of mined material | 0.37–0.45 g Au per tonne of ore; stripping ratio 7:1; 50% recovery loss | 0.25 g/m³ (opinion piece) | CSF-PE p.20–22; Lampadia 2014 | medium / low |
| 1c | Gold per miner per year (MdD) | ~0.3 kg (official output / miners, derived) | ~1.8 kg using the AGC 2017 sector estimate (derived) | PR21 Tabla 17 + ACCA/USAID 2022 via DAR23 | low |
| 1d | Value of 1 ha mined at Aug 2026 gold price | ~US$ 227,000–269,000 gross (derived: 1.6–1.9 kg × US$141.8/g) | ~US$ 65,000–77,000 at the 2016-18 price | CSF-PE yield × pack gold price US$4,411/oz | low (yield uncertain) |
| 2a | MdD declared gold production | 7.1 t (2019, incl. artisanal estimate); 1.2–1.5 t/yr declared by units 2021-25 | 19.1 t (2010) to 7.1 t (2019); series breaks in 2020 | PR21 p.57 Tabla 17; team MINEM/BCRP note | high (official) but definition breaks |
| 2b | Estimated real MdD output | ~16 t/yr (IIAP & MINAM 2011) | 83 t/yr 23-carat (AGC 2017 sector table, implausibly high); MdD + Puno illegal 46.7 t (2019) | DAR23 p.60, p.47; PR21 p.91 | low |
| 2c | Peru illegal gold exports, value | **US$ 7.4 bn (2024); > US$ 11.5 bn (2025)**; ≥ US$ 16 bn projected 2026 | 2024: US$ 6.8–7.4 bn depending on vintage; 2025: US$ 11.5–12 bn | IPE via El Comercio (5 May 2025), Energiminas (11 May 2026), ProActivo (17 Sep 2026) | medium (one method, one institute) |
| 2d | Peru illegal gold exports, volume / share | 77 t (2023), ~92 t (2024); > 104 t (2025, snippet); illegal = **54% of export volume in H1 2026** | 2024: "at least 80 t of unknown origin" of ~180 t (Mongabay); 2019: export–production gap 24.9 t; 2012: 40 t informal + illegal ≈ 20% of output | IPE (Energiminas 30 Jan 2025; ProActivo 2026); Mongabay 2026; PR21 p.92; MINAM16 p.72 | medium |
| 3a | Regalía minera, small/artisanal producers | **0%** (others 1–3% of sales) | – | SUNAT, Ley 28258 | high |
| 3b | IGV on gold | Raw gold sold IGV-exempt; detracción (withholding) 1.5% on exempt gold, 10% on taxed gold | – | SUNAT detracciones annex | high (rule) |
| 3c | Income tax | General rate 29.5%; RMT 10% up to 15 UIT of net income, 29.5% above (firms up to 1,700 UIT revenue) | Whether small miners may use RMT not verified | D.L. 1269 Art. 5 (SUNAT) | high (rule) |
| 3d | Derecho de vigencia (concession fee) | US$ 0.50/ha/yr artisanal; US$ 1.00 small; US$ 3.00 general | plus minimum-production penalties | MINAM16 p.44–45 | high (as of 2016) |
| 3e | Tax revenue lost to illegal mining (national) | **S/ 5,200 M income tax** (2025, of which S/ 2,600 M would be canon) | > US$ 100 M/yr (2010s); US$ 94–145 M/yr (2003-14); S/ 7,500 M/yr (IPE via Canal N) | Minister Montero via RPP (13 Jul 2025); PR21 p.127; MINAM16 p.73–75 | low–medium (method not published) |
| 3f | Tax lost, MdD | ~S/ 50 M/yr canon | US$ 47–73 M/yr canon (2003-14); US$ 70–120 M/yr (governor, 2020) | PR21 p.215; MINAM16 p.73; El Comercio 2020 | low |
| 4a | REINFO registrations, national | **31,641 total, 21,822 vigentes (11 Feb 2026)** | 84,358 (Dec 2024, 18,454 vigentes) before ~50,565 were dropped on 30 Jun 2025 | MINEM database via PerúCheck/El Búho; Gestión 27 Dec 2024; Energiminas 7 Aug 2025 | high |
| 4b | REINFO registrations, MdD | 9,004 (1,720 vigentes) Dec 2024; **3,838 (2,914 vigentes)** in the April 2026 GEOCATMIN layer | 9,592 (2021); 9,158 (Jul 2024) | Gestión 2024; repo `data_raw/reinfo/`; PR21 p.55 | high |
| 4c | Fully formalized | **145 of 9,592 in MdD (2021)**; 2,032 of 87,111 nationally (2.4%, Nov 2024) | ~12,000 cumulative since 2012 (industry estimate) | PR21 p.56; Caretas 3 Nov 2024 | medium |
| 4d | REINFO deadline | **31 Dec 2026** (Ley 32537, Dec 2025); Executive's Ley MAPE bill (to be filed 15 Oct 2026) proposes a 2-year regime, 1 Jan 2027–2028, for ~30,000 vigentes | ~6–7 extensions since 2012 | Exitosa 26 Dec 2025; RPP 9 Oct 2026 | high (law); medium (bill) |
| 4e | REINFO points outside the D.L. 1100 corridor, MdD | **11 of 9,125 (Feb 2025); 12 of 3,838 (Apr 2026)**; 0–1 inside a SERNANP ANP | – | our computation on repo raw data (derived) | high for registered coordinates; says nothing about where people actually mine |
| 5a | Price discount for informal gold (MdD) | Traders paid ~S/ 80 vs normal S/ 180 (per gram, the article says "onza") during the 2020 lockdown, i.e. ~56% below normal | no recent figure found | Governor Hidalgo via El Comercio (2 Jun 2020) | low |
| 5b | Cost of formalizing | US$ 135,000 per small/artisanal miner (Arequipa regional estimate, 2016) | IGAC up to US$ 100,000 (snippet only) | ProActivo 12 May 2016 | low |
| 5c | Profit margin of illegal/informal mining | 11%, 23.9% or 36.8% (three scenarios) | ~30% (CSF assumption) | Torres 2015 (CooperAcción) via MINAM16 p.74–75; CSF-PE p.7 | low–medium |
| 6a | Illegal mining vs other crime | Illegal mining > 66% of Peru's illegal economies in 2025 (41% in 2023), above drug trafficking | UIF suspicious-operation reports: US$ 6,036 M (2025); 2010–Jul 2019: mining US$ 6,706 M vs drugs US$ 3,226 M | IPE via Canal N (undated) and Energiminas (11 May 2026); PR21 p.127 | medium |
| 6b | Extortion in La Pampa | S/ 1,000 per balsa per week; S/ 20,000 from machine owners; S/ 200 per shop | 204 people reported missing in MdD in 2025 | Mongabay/Forbidden Stories, 3 Feb 2026 | medium (journalism) |
| 7a | Mercury per gold | **Hg:Au ≈ 2.6:1** (Peru range 2.4–2.8) | 2.1–2.9 by sector (AGC 2017); 1.3–8 in the literature; "up to 3 kg Hg per kg Au" | CSF-PE PDF p.43; DAR23 p.47 Tabla 9 | medium |
| 7b | Social cost per kg of gold (Peru) | **two separate CSF estimates, never mixed into one range:** (i) CSF-PE report PDF p.7: US$ 1.2–1.8 M per kg (mostly mercury health effects); (ii) CSF Mining Impacts Calculator, Work Methodology page (opened 2026-10-13): "In the case of Peru, 1 kg of gold generates socio-environmental impacts worth between US$81,000 and US$364,000." https://miningcalculator.conservation-strategy.org/methodology/resume | – | CSF-PE p.7; CSF calculator | low–medium (model) |
| 7c | Restoration cost | US$ 933/ha (natural regeneration) to US$ 2,536/ha (CINCIA), 2022 values; 1,100 seedlings/ha | – | CSF-PE p.24 | medium |
| 7d | Carbon value of forest | 509 tCO2/ha × US$ 10/tCO2 = ~US$ 5,090/ha (derived) | – | CSF-PE p.27 (SERFOR 2020; World Bank 2020) | medium |
| 8a | Operation Mercurio cost and staff | Plan budget ~S/ 200 M; 1,200 police + 300 army at launch; US$ 62.5 M commitment (Reuters 2019 via USAID) | FFAA in the zone 690 (2019), 672 (2020), 887 (2021) + ~840 navy | Actualidad Ambiental 19 Feb 2019; USAID 2020 p.5; PR21 p.36 | medium |
| 8b | PP 0128 budget (national) | S/ 121 M (2019) → S/ 89 M (2024) → S/ 70 M (2025) | MdD executed S/ 31.1 M (2019) → 5.0 M (2025) | IPE via El Comercio 2025; PCM via Energiminas 5 May 2026; team MEF scrape | high (MEF) / medium (press) |
| 9 | Gold-price response of mining | **No published elasticity found for Peru.** Mercury imports track the price (R² = 0.93, 2003-09); mining grew +53% while the price fell 26% (2012-17) | – | Swenson et al. 2011; Caballero Espejo et al. 2018 via USAID 2020 | low |

---

## 1. Gold yield per hectare and per miner

### 1a. CSF Peru methodology (opened, best available)
[CSF-PE], section 3.1.3, PDF p.22 (printed 21), Cuadro 3 "Productividad (gramos de oro por tonelada de mineral)":

| Site | g Au per t of ore | ha per kg Au (2.5 m pit) | kg Au per ha (2.5 m pit) |
|---|---|---|---|
| Huepetuhe | 0.45 | 0.5 | 1.9 |
| Puquiri | 0.37 | 0.6 | 1.6 |
| Malinowski | 0.4 | 0.6 | 1.7 |

- Quote (PDF p.23): "De la tabla anterior se pueden extraer de 1.7 a 1.9kg de oro por hectárea." (EN: "From the table above, 1.7 to 1.9 kg of gold can be extracted per hectare.") The table itself includes Puquiri at 1.6 kg/ha, so the code uses the full table range **1.6–1.9**.
- Assumptions (p.20, section 3.1.1): grades "0,37, 0,4 y 0,4 (Artisanal Gold Council, 2017; Alianza para la Minería Responsable, 2021) gramos de oro por tonelada de mineral"; stripping ratio "una relación de 7:1"; density "2,76 ton/m3"; and "hay una pérdida del 50% en la cantidad total de oro recolectado" (EN: grades of 0.37–0.4 g per tonne of ore; a 7:1 waste-to-ore ratio; a density of 2.76 t/m³; a 50% loss of the gold).
- Caveat (PDF p.22): "Las leyes de oro en la región Amazónica peruana para el método de extracción con bombas de succión no fueron identificadas" (EN: "Gold grades for the suction-pump method in the Peruvian Amazon were not identified"). La Pampa's method is exactly suction pumps, so the CSF figure comes from Huepetuhe/Puquiri/Malinowski. **Kg/ha scales linearly with pit depth**, so a 5 m pit would give ~3.4–3.8 kg/ha.
- Brazil version (team note, CSF Série Técnica 53, 2021): "podem ser extraídos de 0,7 a 8,3 kg de ouro por hectare" (EN: "0.7 to 8.3 kg of gold can be extracted per hectare").

### 1b. Other grade figures (low confidence)
- Lampadia, Rafael Belaunde A., "Minería aluvial", opinion piece, 11 Nov 2014, https://www.lampadia.com/opiniones/rafael-belaunde/mineria-aluvial/ (opened via Firecrawl): "Las zonas auríferas de Madre de Dios contienen, en promedio, 0,25 gramos de oro por cada metro cúbico, lo que significa que en los primeros cinco metros de subsuelo, una hectárea mineralizada puede contener el equivalente a US$ 500.000 en oro" (EN: "MdD's gold zones contain on average 0.25 g of gold per m³, so in the top five metres one mineralized hectare can hold the equivalent of US$500,000 in gold"). **Derived:** 0.25 g/m³ × 50,000 m³ = 12.5 kg/ha *in situ*, before recovery losses. This is an opinion piece with no source given.
- Geological papers in the search results (IRD colloquium PDF; SciELO RMCG 2025) were scans or could not be read. One snippet gave 200–500 mg/m³ for recent point bars and 2–4 g/m³ for older placers, and another gave 3–4 **mg**/m³ (unit conflict). **Snippet only, verify; do not use.**

### 1c. Derived cross-check from official production and our mapped hectares (as in `code/v2_economics.py`)
- Official MdD production (MINEM yearly files, `data_intermediate/minem_mdd_gold.csv`, `total_kg` = declared + MINEM's artisanal estimate up to 2019; PR21 p.57 Tabla 17 gives the same series: "Madre de Dios (TMF) 19.1 22.6 12.3 16.1 8.0 12.7 17.6 12.8 10.2 7.1" for 2010–2019).
- Hectares: our MapBiomas Col 4 raster accounting for MdD, 2016–18 mean, (a) first-time mined land + returns to old pits ("hectares worked") and (b) first-time mined land only.
- **Derived (code):** `eco_implied_kg_ha_2016_18` = MINEM gold / hectares worked = **1.9 kg/ha** (run of 2026-10-13); `eco_implied_kg_ha_new_2016_18` = per first-time hectare = **2.5 kg/ha**. Per hectare worked this matches the top of CSF's 1.6–1.9 kg/ha; per first-time hectare it is above it. Upward biases: part of the gold comes from river dredges that map no land; downward: official production may miss illegal output. Use only as an order-of-magnitude check. **Implication for the gold range:** the code gives old pits no gold and uses CSF's fresh-pit yield on first-time land only, so its 2022–25 gold range is, if anything, low.
- (The older figure in earlier drafts, 13.5 t / 3,610 ha of net MapBiomas additions ≈ 3.7 kg/ha, used the pack's NET additions (which subtract reclassified or abandoned land) instead of the raster accounting of land actually worked; it is superseded by the two code numbers above and should not be cited.)

### 1d. Gold per miner (derived, low confidence)
- Miners: "existen al menos 46,605 mineros artesanales, dentro de los cuales 31,390 son mineros informales y 9,323 son mineros ilegales" (ACCA & USAID Prevenir 2022, quoted in DAR23 p.29, team note) (EN: "at least 46,605 artisanal miners, of whom 31,390 are informal and 9,323 illegal").
- Output: official 7–13 t/yr (PR21 Tabla 17) or the AGC 2017 sector table total of ~83 t (23-carat) (DAR23 p.47, Tabla 9, opened today; La Pampa traca "66" t, Huepetuhe shute "13" t).
- **Derived:** 13 t / 46,605 ≈ 0.28 kg per miner per year; 83 t / 46,605 ≈ 1.8 kg. The AGC total is ~6× the official figure, so treat the high end with caution.
- Per machine: MAAP #193 counted "598 dragas" in La Pampa in Aug 2023 and estimated "2,392 personas" (4 per dredge) (team note `maap_citations.md`). Mongabay 2026: "nada más en La Pampa y Delta Uno hay más de 5000 dragas y tracas" (EN: "in La Pampa and Delta Uno alone there are more than 5,000 dredges and tracas").
- A Rebelión/EFE piece says a concession yields "10 to 100 grams of gold in one working day" (**snippet only, verify**).

### 1e. Value per hectare (derived)
Gold price in the data pack: US$ 4,411/oz (Aug 2026) = US$ 141.8/g. 1.6–1.9 kg/ha → **US$ 227,000–269,000 gross per hectare**. At the 2016–18 mean (~US$ 1,259/oz = US$ 40.5/g): US$ 65,000–77,000/ha. The gold price has roughly tripled the value of the same pit, which matters for the "re-mining old land" story (MAAP #193).

---

## 2. Production: official vs estimated; illegal share of exports

### 2a. Official MdD series (opened / team note)
- PR21 p.57 Tabla 17 (above): MdD fell from 22.6 t (2011) to 7.1 t (2019), while Puno rose from 2.8 to 9.1 t.
- **Series break (team note `legality_data.md` §0 and §4):** MINEM's yearly files include "PRODUCTORES ARTESANALES 1/ … Cifras Estimadas" for MdD up to 2019 (17.1 t in 2016 as read from the MINEM file by `code/peru_gold_minem.py`, id gold_minem_estimate_2016_kg; an earlier team note said 15.7 t, superseded). From 2020 that estimate is dropped. Production declared by units: 944 kg (2018), 1,101 (2019), 2,152 (2020), 1,622 (2021), 1,472, 1,488, 1,220, 1,362 kg (2025). **Do not present the 2018→2025 fall as a production fall.**
- USAID (2020), *Case Study: Artisanal and Small-scale Mining in Madre de Dios*, https://www.planetgold.org/sites/default/files/2020-12/USAID.%202020.%20Case%20Study%20ASM%20and%20ASGM%20in%20Madre%20de%20Dios.pdf (opened), p.2: "In 2019, the ASGM sector generated 22 percent (27.7 metric tons) of gold production in Peru (MINEM 2020)". p.4: "In 2018, following efforts to reduce illegal gold production, Madre de Dios' GDP decreased by 9.8 percent (BCRP 2018)", and "Official reports already show a reduction of 30.5 percent in the gold produced from January through October 2019".

### 2b. Estimated real output (MdD)
- DAR23 p.60 (printed 58), opened: "se estima que cada año se extraen al menos 16,000 kilogramos de oro con un valor de alrededor de 1,600 millones de soles" (IIAP & MINAM 2011) (EN: "at least 16,000 kg of gold worth about S/1,600 million are extracted each year").
- DAR23 p.47 Tabla 9 (Artisanal Gold Council 2017), opened: sector production sums to ~83 t/yr (23-carat). The method is "la producción diaria por el número de días hábiles [...] por la cantidad de equipos" (DAR23 p.46) (EN: daily output × working days × number of machines). It is far above any official figure.
- PR21 p.91, opened: "Madre de Dios y Puno tendrían una producción aproximada de 46.72 toneladas para el periodo 2019" (EN: "MdD and Puno would have produced about 46.72 t in 2019"), based on the export–production gap, national consumption, and the excess in Bolivian output.
- Gestión, 4 Oct 2026: MdD concentrates "entre un 35% a 38% de la producción ilegal de oro en el país" (EN: "35–38% of the country's illegal gold"; FCDS estimate) (team note).

### 2c. Illegal share of Peru's gold exports (national)
**Method (IPE):** illegal exports = SUNAT export volume minus MINEM declared production. Forbes Perú, 3 Oct 2025, https://forbes.pe/economia-y-finanzas/2025-10-03/exportaciones-de-oro-ilegal-alcanzarian-los-us12-000-millones-en-2025-proyeta-estudio-del-ipe/ (opened): "Se observa que las exportaciones son superiores al valor que correspondería según la producción" (EN: "Exports exceed what production would imply"). This residual also contains stock changes, recycling and imports re-exported, and it is not split by region.

| Year | Volume | Value | Source (opened unless marked) |
|---|---|---|---|
| 2012 | 40 t informal + illegal (~20% of national output; ~10% of export volume, 2011-12) | US$ 2,146 M | MINAM16 p.72: "la producción estimada de oro de procedencia informal e ilegal era de 40 toneladas anuales, por un valor aproximado de USD 2 146 millones" |
| 2014 | 112 of 290 t of exports (~38%) "likely from illegal gold mining in Madre de Dios" | ~US$ 3 bn | USAID 2020 p.4, citing GI-TOC 2016 |
| 2015 | ~28% of gold *mined* in Peru is illegal | – | GI-TOC 2016, *Organized Crime and Illegally Mined Gold in Latin America*: **snippet only, verify**. The BHRRC summary page (opened, 24 Apr 2016) only says "the value of illegal gold exports now exceeds the value of cocaine exports" (Peru and Colombia) |
| 2019 | export–production gap 24.9 t | – | PR21 p.92: "una brecha entre la exportación y la producción de oro que, al 2019 alcanzaría las 24.9 toneladas al año" |
| 2010s avg | 35 t/yr unrecorded (contraband) | US$ 1,426 M/yr | PR21 p.127, citing Valdés, Basombrío & Vera (2019, KAS) |
| 2023 | 77 t | US$ 4,833 M | IPE via Energiminas, 30 Jan 2025, https://energiminas.com/2025/01/30/ipe-en-2025-peru-podria-exportar-40-mas-toneladas-de-oro-ilegal-que-en-2024 |
| 2024 | ~92 t | **US$ 7,415 M** (+54%) | IPE via El Comercio, 5 May 2025, https://elcomercio.pe/economia/peru/ipe-exportaciones-de-oro-ilegal-alcanzaron-un-record-de-us7415-millones-en-2024-l-ultimas-noticia/: "US$7.415 millones"; Peru = "44% de las exportaciones de América del Sur" (of *South American* illegal exports, not 44% of Peru's exports) |
| 2024 | "at least 80 t" of ~180 t exported of "origen desconocido" | ~US$ 7 bn | Mongabay Latam / Forbidden Stories, 3 Feb 2026, https://es.mongabay.com/2026/02/peru-extorsiones-asesinatos-devasta-bosques-la-pampa/ |
| 2025 | > 104 t of 208 t (≈ 50%) | **> US$ 11,500 M** (+55%) | Value: IPE via Energiminas, 11 May 2026, https://energiminas.com/?p=45967 (opened). Tonnes: Expreso (403 when fetched): **snippet only, verify** |
| H1 2026 | illegal = **54%** of export volume; +19.4% vs H1 2025, while legal fell 5.9% | – | IPE via ProActivo, 17 Sep 2026, https://proactivo.com.pe/ipe-oro-ilegal-superaria-al-legal-en-exportaciones-durante-el-2026/: "la exportación de oro de origen ilegal ya supera a la de origen legal" (EN: "illegal-origin gold exports already exceed legal ones") |
| 2026 (proj.) | ≥ 110 t (52–55% of exports) | ≥ US$ 16,000 M | same ProActivo article |

- Destinations (IPE via Energiminas, 5 May 2025, opened): ~40% of shipments now go to India and the UAE, against ~75% to Switzerland, the US and Canada ten years earlier.
- MEF (Reporte Minero, 10 Jul 2025, https://www.reporteminero.cl/noticia/noticias/2025/07/mineria-ilegal-pbi-trazabilidad-exportaciones-mef, opened): illegal mining is "alrededor del 2,7% del Producto Bruto Interno (PBI)", "más de 4.500 millones de dólares" per year, and "casi 46 toneladas de minerales sin trazabilidad" (EN: ~2.7% of GDP; > US$4.5 bn a year; almost 46 t of minerals with no traceability).
- **Inconsistency to flag:** a Reuters piece (5 Jun 2026, via La República, opened) says informal mining exports were "about US$ 11,000 million in 2025", in line with IPE. A search snippet attributing "US$4.8bn in 2024 = 44% of total gold exports" to IPE mixes up the 2023 value and the South American share. **Do not use.**

---

## 3. Taxes and fees: formal small producer vs illegal miner

### 3a. What a formal pequeño productor / productor artesanal pays (rules, opened)
| Item | Formal small/artisanal | Illegal | Source |
|---|---|---|---|
| Regalía minera | **0%** ("la regalía será de 0% (cero por ciento)"); large producers 1% (to US$60 M), 2%, 3% | 0 | SUNAT, "Rangos para el pago de regalía minera – Ley N° 28258", https://orientacion.sunat.gob.pe/06-rangos-para-el-pago-de-regalia-minera-ley-ndeg-28258 |
| IGV (VAT) on gold sale | exempt raw gold; the buyer withholds a detracción of **1.5%** ("Oro y demás minerales metálicos exonerados del IGV", Anexo code 36, includes sales under "Ley N.° 27037" Amazonia); **10%** for "Oro gravado con el IGV" | none (cash sale to trader) | SUNAT, "Apéndices del Sistema de Detracciones", https://orientacion.sunat.gob.pe/apendices-del-sistema-de-detracciones (page undated, © 1997–2022). The detracción is a prepayment into a blocked account, not a final tax. From 2025, RS 086-2025/SUNAT requires the deposit before transport, because of "informalidad en la cadena" of gold (snippet only, verify) |
| Income tax | 29.5% general. **RMT** (D.L. 1269, in force 1 Jan 2017; revenue ≤ 1,700 UIT): Art. 5 "Hasta 15 UIT 10% / Más de 15 UIT 29,50%" | 0 | D.L. 1269, https://www.sunat.gob.pe/legislacion/mypeIR/dl1269.pdf (opened, p.4). **Whether mining concession holders may use RMT/RER was not verified.** |
| Derecho de vigencia | US$ 0.50/ha/yr artisanal, US$ 1.00 small, US$ 3.00 general | 0 | MINAM16 p.44–45 table "Cuota Derecho Minero" |
| Minimum production | US$ 25/50/100 per ha/yr (artisanal/small/general), then "5% UIT por año por hectárea" (artisanal) or "10% UIT" (small, metallic); penalties from year 11 | 0 | MINAM16 p.44; PR21 p.125 |
| Canon | 50% of income tax goes to the region (Ley del Canon; **not opened, verify**) | 0 | – |

- **Compliance in practice (PR21 p.129, opened):** of "88,838 registros" in REINFO (7 Dec 2020), "solamente 15,574 registros, es decir el 21.5% del total, habrían presentado su Declaración Jurada de impuesto a la renta del 2019" (EN: only 15,574, or 21.5%, had filed a 2019 income-tax return; 78.5% filed nothing).
- **Derived tax wedge per kg of gold:** with 0% royalty and the detracción only a prepayment, the formal miner's extra tax burden is mostly income tax: 29.5% × profit margin. With the 11–37% margins in Torres (2015) or the ~30% in CSF-PE, that is **~3–11% of gross value**, i.e. ~US$ 4,500–15,500 per kg at Aug 2026 prices, plus fees and formalization costs (§5). **Implication:** tax alone gives a weak reason to stay illegal. Location (La Pampa is outside the corridor, so it can never be formalized) and laundering margins matter more. This matches the team note §4b.4.

### 3b. Estimates of revenue lost (national)
| Estimate | Period | Source (opened unless marked) | Note |
|---|---|---|---|
| Income tax S/ 5,200 M; canon S/ 2,600 M | 2025 | Minister Jorge Montero via RPP, 13 Jul 2025, https://rpp.pe/politica/gobierno/ministro-de-energia-y-minas-anuncio-revision-de-normas-sobre-derechos-laborales-de-mineros-artesanales-noticia-1646159: "una pérdida en el impuesto a la renta de 5,200 millones de soles y en el canon minero de 2,600 millones de soles" | Canon is half of income tax, so **do not add the two**. No method given. Sanity check (derived): US$ 11.5 bn × 30% margin × 29.5% ≈ US$ 1.0 bn ≈ S/ 3.7 bn, the same order of magnitude |
| > S/ 7,500 M per year | 2025 | IPE via Canal N (undated), https://canaln.pe/actualidad/mineria-ilegal-mueve-us12-mil-millones-y-lidera-economias-delictivas-n488421 | The same page says total impact is "S/ 22,700 millones, equivalente al 25 % del PBI", which is implausible on its face, so treat the page as unreliable. A ProActivo snippet gives S/ 7,500 M for 2023–2025 *combined* (**snippet only, verify**) |
| > US$ 100 M income tax per year | 2010s | PR21 p.127: "se dejó de recaudar más de 100 millones de USD de impuesto a la renta por año" (Valdés, Basombrío & Vera 2019) | |
| US$ 94–145 M/yr income tax | 2003–2014 | MINAM16 p.73, Tabla 3 p.74–75 (Torres 2015, CooperAcción): 3rd-category income-tax evasion "fluctuó entre USD 94 millones y USD 145 millones en promedio anual"; scenarios MG = 11.0 / 23.9 / 36.8% give US$ 43.4 / 94.3 / 145.1 M per year | 30% rate |
| S/ 500 M | ~2013 | MINAM16 p.72 (Defensoría 2013): artisanal + small output "18 TM de oro", "S/. 2 200 millones", "evasión de impuestos ascendía a S/. 500 millones" | |
| Fuel tax exemption benefiting illegal mining in MdD: S/ 2,111 M over 20 years | 2005–2024 | Gestión/IPE, 18 Feb 2025 (team note) | MdD-specific |

### 3c. Revenue lost, MdD
- PR21 p.215: the region "deja de percibir más de S/ 50 millones por año por canon minero, producto de la evasión de impuestos" (EN: "the region loses more than S/50 million a year in mining canon because of tax evasion").
- DAR23 p.60: "la región podría beneficiarse con aproximadamente 50 millones de soles por concepto de canon minero anualmente. Sin embargo, la realidad es que apenas se reciben 42,000 soles" (IIAP & MINAM 2011) (EN: "the region could receive about S/50 million a year in canon; in reality it gets barely S/42,000").
- MINAM16 p.73: "Madre de Dios dejó de percibir por concepto de canon minero entre USD 47 y 73 millones en promedio anual durante el periodo 2003-2014" (EN: "MdD lost US$47–73 million a year in canon, 2003–2014").
- El Comercio, 2 Jun 2020 (opened): Governor Luis Hidalgo estimates the region loses US$ 70–120 M a year to informal mining.

---

## 4. REINFO

### 4a. What it is and why it shields miners
- REINFO was created by D.L. 1293 (Dec 2016): "en el año 2016, se promulgó el Decreto Legislativo 1293 [...] y la creación del Registro Integral de Formalización Minera (REINFO)" (DAR23 p.24, printed 22; team note).
- **Legal shield (opened):** Energiminas, 21 Nov 2024, https://energiminas.com/2024/11/21/ejecutivo-propone-eliminar-decreto-que-exime-de-responsabilidad-penal-a-mineros-inscritos-en-el-reinfo. MINEM's formalization director Mayra Figueroa says D.L. 1351 "exime de responsabilidad penal a aquellos que estaban en el Reinfo" (EN: "exempts from criminal liability those who were in REINFO"); the norm "protege de todo proceso penal a mineros que estén en proceso de formalización o que ya estén inscritos en el Reinfo" (EN: "protects from any criminal proceeding miners in formalization or registered in REINFO"). Same article: "84 mil registros", 77% suspended.
- IPE via El Comercio / Energiminas (5 May 2025, opened): suspended registrants "continúen siendo considerados por las autoridades como 'informales' y no 'ilegales'" (EN: they "continue to be treated by the authorities as 'informal' and not 'illegal'"). IPE "recomienda el cierre del Reinfo".
- Figueroa, 16 Jul 2024 (Energiminas, https://energiminas.com/?p=20688, opened): REINFO "sí ha venido siendo mal usado" and "ha servido como un paraguas" (EN: "has indeed been misused"; "has served as an umbrella").
- **Limits of the shield:** the exemption needs, among other conditions, that the miner "No desarrolle actividades en" prohibited zones. DAR (Jul 2025), *Análisis técnico legal del predictamen [...] Ley MAPE*, https://dar.org.pe/wp-content/uploads/2025/07/analisis_normativoMAPE080725.pdf (opened), p.5 quotes the bill's version: "Exención de responsabilidad penal durante la formalización minera [...] en tanto concurran, de manera conjunta, las siguientes condiciones: a) Esté inscrito [...] b) No desarrolle actividades en [zonas prohibidas]". Under D.L. 1100/1105, mining outside the corridor (La Pampa, buffer zones) or inside ANPs is illegal by location and cannot be formalized (team note §1a–1b, D.L. 1105 Art. 2; PR21 p.87).
- **Where registrations sit (our computation, derived, description):** we overlaid the REINFO point layers in `data_raw/reinfo/` on the D.L. 1100 corridor polygon (`data_raw/ingemmet/corredor_minero_madre_de_dios_DL1100.geojson`, 498,328 ha; MINAM16 p.48 gives 498,296 ha) and on SERNANP polygons.
  - SERV_REINFO (snapshot 2025-02-26): 9,125 MdD points; **9,114 inside the corridor, 11 outside** (7 vigente); 0 inside a SERNANP ANP; 2 inside the Tambopata buffer zone, both also inside the corridor (corridor ∩ Tambopata BZ = 2,140 ha).
  - temp_reinfo "abril_26": 3,838 points; **3,826 inside, 12 outside** (all vigente); 1 inside an ANP.
  - Reading: REINFO registrations are tied to rights *inside* the corridor, so **La Pampa miners cannot be REINFO-covered where they actually work.** The shield works through paperwork (selling La Pampa gold under a corridor registration), and points cannot show that. Note the conflict with `legality_data.md` §2, which reports 268 REINFO points in AMW "Very High". AMW uses RAISG protected areas, not SERNANP, and the team should reconcile the two before citing either.

### 4b. Registrations over time
| Date | National | MdD | Source |
|---|---|---|---|
| Apr 2020 | "more than 51,000 miners and 8,000 miner associations" | – | USAID 2020 p.2 (opened) |
| Jun 2020 | 48,711 registered | 5,343 in formalization | MINEM via El Comercio, 2 Jun 2020 (opened) |
| 7 Dec 2020 | 88,838 registrations; 15,574 filed 2019 income tax | – | PR21 p.129 |
| 2021 | – | **9,592** (Manu 4,762, Tambopata 4,830); **"solo 145 mineros en Madre de Dios se encuentran totalmente formalizados"** | PR21 p.55–56 (opened) |
| Jul 2024 | – | 9,158: "6,666 con registros suspendidos y solo 2,492 registros vigentes" | Energiminas 16 Jul 2024 (opened) |
| Nov 2024 | 87,111 registered; **2,032 formalized (2.4%)**; 69,107 suspended (79%) | – | Caretas, 3 Nov 2024, https://caretas.pe/politica/luis-miguel-castilla-sobre-el-reinfo-solo-el-2-logro-formalizarse (opened; no source for the figures given) |
| 26 Dec 2024 | 84,358; 18,454 vigentes ("solo un 21.8%") | 9,004; 1,720 vigentes ("un 19% de su total") | Gestión, 27 Dec 2024, https://gestion.pe/economia/reinfo-cuatro-de-cada-cinco-inscripciones-cierran-el-ano-suspendidas-donde-estan-noticia/ (opened) |
| May 2025 | 84,470; 76% suspended | – | IPE via El Comercio (opened) |
| 30 Jun 2025 | 50,565 holders' process ended; 31,560 extended to 31 Dec 2025 | – | Minister Montero via Energiminas, 7 Aug 2025 (opened) |
| Jul 2025 | 31,557 continuing: 26,703 vigentes + 4,854 suspended ≤ 1 yr | – | DAR Jul 2025 p.3 (opened): "un total de 31 557 REINFOs continúan con el proceso de formalización minera" |
| 11 Feb 2026 | **31,641 total; 21,822 vigentes** | – | MINEM database via PerúCheck / El Búho, 11 Feb 2026, https://elbuho.pe/?p=412908 (opened) |
| Apr 2026 | 40,640 points | 3,838 (2,914 vigente, 924 suspended) | GEOCATMIN layer "reinfo_abril_26", repo `data_raw/reinfo/` (team note) |
| Oct 2026 | ~30,000 vigentes eligible for the new regime | – | RPP, 9 Oct 2026 (opened) |

Cumulative formalizations, alternative figure: Pablo de la Flor (Poderosa) says ~1,000 per year, "12 mil" since 2012 (**snippet only, verify**).

### 4c. Deadline extensions (chronology)
| Date | Instrument | New deadline / content | Source |
|---|---|---|---|
| 2002 | Ley 27651 | Formalization starts | PUCP student essay (opened; low weight) |
| Feb/Apr 2012 | D.L. 1100 (corridor), D.L. 1105 (formalization, 24 months, extendable by DS) | Cut-off 19 Apr 2014 | team note (D.L. 1105 Art. 3); MINAM16 p.82 |
| 2014 | Extension of 2 years | Only ~3% of registrants formalized | PUCP essay citing Chávez 2019 (low) |
| Dec 2016 | D.L. 1293 | Creates REINFO | DAR23 p.24 |
| 2017–2020 | D.L. 1336 / D.L. 1451 / Ley 31007 | Ley 31007 extended to 31 Dec 2021 | **snippet only, verify** |
| 31 Dec 2021 | **Ley 31388** | → 31 Dec 2024 ("quinta ampliación", 104 votes in favour) | PUCP essay (opened); Caretas (team note) |
| 27 Dec 2024 | **Ley 32213** | → 30 Jun 2025, "puede prorrogarse, por única vez, hasta por seis (6) meses adicionales mediante Decreto Supremo" (EN: "may be extended, once only, by up to six months by supreme decree") | Cuatrecasas, https://www.cuatrecasas.com/es/latam/energia-infraestructura/art/amplian-plazo-del-reinfo-hasta-el-30-de-junio-de-2025 (opened) |
| Jun/Jul 2025 | DS 012-2025-EM; RD 0004-2025-MINEM/DGFM (3 Jul 2025) | → 31 Dec 2025 for vigentes and those suspended ≤ 1 yr; > 50,000 excluded | DS: snippet only, verify. RD: DAR Jul 2025 p.3 (opened) |
| 17 Dec 2025 (vote); ~26 Dec 2025 (published) | **Ley 32537** | → "31 de diciembre del 2026" or until the Ley MAPE is approved and regulated; 120 days to update georeferenced location; orders a national census of small and artisanal mining (INEI, MINEM, INGEMMET) | Exitosa, 26 Dec 2025, https://www.exitosanoticias.pe/politica/oficializan-ampliacion-reinfo-31-diciembre-2026-n165381 (opened); Energiminas 17 Dec 2025 (opened; Comisión Permanente 13–4) |
| 15 Oct 2026 (planned) | Executive's Ley MAPE bill | New 2-year "consolidation" regime from 1 Jan 2027 for "alrededor de 30.000 mineros que mantengan vigente su inscripción" (EN: "about 30,000 miners whose registration is still in force"); minister Guillermo Shinno rules out extending REINFO in its current form; those already excluded cannot re-enter | RPP, 9 Oct 2026, https://rpp.pe/economia/economia/gobierno-presentara-proyecto-de-la-ley-mape-el-15-de-octubre-plantea-que-30000-mineros-con-reinfo-pasen-a-nuevo-regimen-de-formalizacion-por-dos-anos-noticia-1711680 (opened). End date "31 de diciembre de 2028": IIMP/Instagram, **snippet only, verify** |

Count: Caretas calls Ley 32213 the "sexta" extension (team note), and IPE says REINFO "ha sido ampliado en cuatro ocasiones desde 2017". Counts differ by starting point, so say "repeatedly extended since 2012 (at least six times)".

---

## 5. Competition between formal, informal and illegal gold; traders and laundering

- **Price discount (MdD, 2020, opened):** El Comercio, 2 Jun 2020, https://elcomercio.pe/peru/madre-de-dios/coronavirus-en-peru-madre-de-dios-la-mineria-ilegal-de-oro-no-da-tregua-en-epoca-de-pandemia-informe-noticia/: Governor Hidalgo, "los acopiadores informales están adquiriendo el metal a S/80 la onza cuando su precio normal es de S/180" (EN: "informal traders are buying the metal at S/80 per ounce when its normal price is S/180"). The unit must be per gram (gold was ~US$ 1,735/oz ≈ S/ 190/g then). This was a lockdown situation (no legal buyers). **No peacetime discount figure for MdD was found.** In Juliaca, traders quote "un margen menor al precio internacional" (ProActivo, snippet only).
- **Formalization cost (opened):** ProActivo, 12 May 2016, https://proactivo.com.pe/?p=57384: Arequipa regional energy manager: "Un pequeño minero o artesanal requiere 135 mil dólares para formalizar sus actividades" (EN: "a small or artisanal miner needs US$135,000 to formalize"). No breakdown. Plan Restauración budgets the evaluation of 780 IGAFOM and the approval of 270 at "S/ 5´202,643.00" (PR21 p.140), which is public cost, not the miner's cost.
- **Profit margins (opened):** MINAM16 p.74–75 (Torres 2015, CooperAcción): margin scenarios of 11.0%, 23.9% and 36.8% of sales. CSF-PE p.7: "cerca del 30% de ese valor (US$16.5 mil) es ganancia de quien lo extrae" (EN: "about 30% of the value, US$16.5 thousand per kg, is the miner's profit"), at US$ 55,000/kg.
- **Evidence that illegal output displaces formal output (national, opened):** H1 2026, illegal exports +19.4% and legal −5.9% (IPE via ProActivo 2026). This is consistent with crowding-out, but it is a residual measure, not proof.
- **Laundering cases (opened):** InSight Crime, Seth Robbins, "Peru Targets Multinationals Linked to Sale of Illegal Gold", 10 Apr 2019, https://insightcrime.org/news/analysis/peru-targets-multinationals-illegal-gold/ (based on Ojo Público case files):
  - Swiss refiner Metalor reportedly processed ~US$ 3.5 bn in gold from Minerales del Sur (Minersur), 2010–2018, and stopped buying in March 2018. Metalor has not been charged.
  - Customs seized 91 kg of Minersur gold bound for Switzerland in March 2018.
  - Minersur's suppliers operate in Madre de Dios.
  - Elemetal (Dallas) bought ~US$ 350 M from four Peruvian firms and pleaded guilty to anti-money-laundering failures.
  - NTR Metals (Miami) declared US$ 980 M of Peruvian gold imports in 2013, up from US$ 73 M in 2012.
- **NTR Metals case (opened):** Fox News/AP, 6 Sep 2017, https://www.foxnews.com/us/2-guilty-of-laundering-billions-in-south-american-gold: "$3.6 billion money-laundering case involving South American gold"; Barrage and Granda pleaded guilty. Elemetal's US$ 15 M fine (AP, Mar 2018) is **snippet only**.
- **Laundering through REINFO (snippets, team note):** a La Libertad conviction in which gold "ingresó al mercado formal tras verificarse únicamente la vigencia del [...] Reinfo y del RUC" (EN: "entered the formal market after only REINFO and RUC (tax ID) validity were checked").
- **Gold traders register:** RECPO had "más de 4 500 inscritos (es necesaria una depuración del mismo)" (EN: "more than 4,500 registrants (it needs cleaning up)") (MINAM16 p.240, team note); PR21 p.139 budgets "S/. 250,000.00" for a RECPO app pilot "enlazado con Blockchain" (EN: linked to blockchain).

---

## 6. Criminal economy and politics

- **Size vs other crime:**
  - IPE via Canal N (undated): illegal mining "más de US$12 mil millones" in 2025; from 41% of illegal economies (2023) to more than 66% (2025), above drug trafficking, logging, trafficking and contraband combined. (The same page carries the impossible "25% of GDP".)
  - PCM high commissioner Gen. (r) Rodolfo García, via Energiminas, 5 May 2026, https://energiminas.com/?p=45709 (opened): the anti-illegal-mining budget is "solo una décima parte del destinado a la lucha contra las drogas" (EN: "only a tenth of the budget for fighting drugs"): S/ 70 M vs S/ 700 M in 2025.
- **Financial intelligence:**
  - IPE via Energiminas, 11 May 2026 (opened): UIF suspicious-operation reports tied to illegal mining "alcanzaron US$ 6,036 millones en 2025, más de 4 veces el valor en 2024" (EN: "reached US$6,036 million in 2025, more than 4× the 2024 value"). MdD illegal-mining complaints rose "de 245 a 427" (2021→2025).
  - PR21 p.127 (UIF, Jan 2010–Jul 2019): "Minería ilegal 49 6706" vs "Tráfico de drogas 176 3226" (number of reports, US$ million).
- **La Pampa extortion (opened, Mongabay/Forbidden Stories, 3 Feb 2026):**
  - "1000 soles (alrededor de 300 dólares) cada semana por operar una balsa" (EN: "S/1,000 (about US$300) a week to operate a raft").
  - "20 000 soles [...] exigidos a los dueños de las máquinas" (EN: "S/20,000 demanded from machine owners").
  - Shops: "La mayoría paga 200 soles" (EN: "most pay 200 soles").
  - Disappearances: "204 personas fueron reportadas como desaparecidas en Madre de Dios en 2025" (EN: "204 people were reported missing in MdD in 2025").
  - Violence "ha[n] ingresado a la reserva de Tambopata" (EN: "has entered the Tambopata reserve").
  - **Derived:** 598 dredges (MAAP #193, 2023) × S/ 1,000 × 52 weeks ≈ S/ 31 M a year in cupos, if every dredge paid.
- **Killings:** "at least 20 people killed or disappeared in La Pampa, Jan–Feb 2025" (La República, snippet only); Guardianes de la Trocha investigated for 20 murders (La República, 19 Aug 2025; fetch failed, **snippet only**); "at least 400 deaths in 12 years" (El Búho citing Dirincri, snippet only, team note). July 2026: an armed forces + police operation against "Los Guardianes de La Pampa", 20 captured, km 98–118 of the Interoceanic (gob.pe/Mindef; fetch blocked, **snippet only, verify**).
- **Human trafficking:** "alrededor de 4,500 mujeres están sometidas a explotación sexual [...] el 78% son menores de edad" (EN: "about 4,500 women are sexually exploited [...] 78% are minors") (MINAM 2013 via DAR23 p.56, team note).
- **2026 election (opened):**
  - Andina, 3 Jul 2026, https://andina.pe/ingles/noticia-peru-2026-elections-jne-to-officially-proclaim-secondround-results-at-noon-today-1082109.aspx: "Popular Force Party candidate Keiko Fujimori won with 50.135% of the valid votes" in the 7 Jun 2026 runoff.
  - Reuters via La República (Colombia), 5 Jun 2026, https://www.larepublica.co/globoeconomia/votos-de-mineros-informales-podrian-ser-clave-las-elecciones-presidencial-de-peru-4408680:
    - Fujimori was "prometiendo reprimir la minería ilegal, modernizar el sector informal y ampliar el acceso al crédito estatal" (EN: "promising to crack down on illegal mining, modernize the informal sector and expand access to state credit").
    - Roberto Sánchez "votó en el Congreso a favor de extender Reinfo" (EN: "voted in Congress to extend REINFO").
    - "ninguno de los candidatos parece dispuesto en el corto plazo a desmantelar el programa" (EN: "neither candidate seems willing to dismantle the programme in the short term").
    - "unos 500.000 mineros informales en Perú" (EN: "some 500,000 informal miners in Peru").
- **New (bicameral) Congress, opened:** El Búho / Cusco Post, 27 Aug 2026, https://elbuho.pe/?p=433692.
  - Deputies' Energy and Mines committee chair: **Yenifer Paredes** (Juntos por el Perú), who met Confemin.
  - Senate committee chair: Daniel Barragán (Obras), who wants an evaluation before any new extension.
  - Members with reported ties to informal mining: Juver Flores (Senate VP, says he won't back another extension), Jaime Quito, Víctor Flores (Fuerza Popular, voted for earlier extensions), Jesús Pérez.
  - Opponents of extension: Karla Schaefer, Rafael Yamashiro (Fuerza Popular), Ruth Luque, Francisco Giampietri.
  - Earlier Congress: Eduardo Salhuana (APP, Madre de Dios) received "65 mineros no formales" (EN: "65 non-formal miners") Jan 2023–Jun 2024 (América TV/Cuarto Poder, **snippet only**).

---

## 7. Social and environmental costs

- **Mercury per gold (opened):**
  - CSF-PE PDF p.43 (printed 42), section 3.3.4.1 a: the ratio "puede variar considerablemente de 1,3 a 8 gramos de mercurio por cada gramo de oro extraído [...] Para Perú específicamente, este valor puede tener una relación promedio (Hg:Au) de 2.4 a 2.8 (Artisanal Gold Council, 2017; MINAM, 2011). De forma conservadora, se utiliza el valor medio de 2,6." (EN: "can vary from 1.3 to 8 g of mercury per g of gold [...] for Peru the average ratio is 2.4 to 2.8 [...] conservatively, the mean of 2.6 is used.")
  - Release to water: "Para Perú se utiliza la referencia del 9% de pérdida en agua" (EN: "for Peru, a 9% loss to water is used") (UNEP 2018).
  - DAR23 p.47 Tabla 9 (AGC 2017): Hg:Au 2.1:1 (Huepetuhe shute) to 2.9:1; La Pampa traca 2.3:1; total "181.327" t Hg/yr, La Pampa "145.2" t. The text on p.46 misprints "181,327 toneladas".
  - El Comercio 2020: Ipenza, "each kilo of gold extracted requires up to three kilos of mercury".
  - Swenson et al. 2011 (PLoS ONE, opened): "The ratio of mercury use to resulting gold amalgam is at least 2 to 1 in artisanal mining".
- **Mercury in people and fish (opened unless marked):**
  - USAID 2020 p.6: "In a recent study by Duke University, 42 percent of the women of childbearing age and 20 percent of children analyzed along the Interoceanic Highway had mercury levels [above the limit]"; total ASGM mercury releases in Peru "as high as 180 metric tons annually (Defensoría del Pueblo 2019)".
  - Reuben et al. 2020 (GeoHealth): 32.9% of 164 children above 2.0 µg/g, and "4.68 IQ points lower" (team note).
  - Diringer et al. 2015: ">one-third of carnivorous fish" above 0.5 mg/kg (team note).
- **Monetised costs:**
  - CSF-PE p.7 (opened): "1 kg de oro extraído genera impactos entre US$ 1,2 millón y 1,8 millón de dólares, en su mayoría relacionados con los impactos del mercurio en la salud humana" (EN: "1 kg of gold extracted generates impacts of US$1.2–1.8 million, mostly mercury effects on human health"), compared with a sale price of US$ 55,000/kg. The CSF calculator web page gives "between US$81,000 and US$364,000" per kg for Peru (team note). That is a different vintage or module; **report both separately and say which** (the code registers `eco_social_busd_calc_*` and `eco_social_busd_pdf_*`; it never mixes the two into one range).
  - Restoration, CSF-PE p.24 (opened): "costos de recuperación de US$ 933/ha para regeneración natural (en 2022)" (IIAP 2009a) and "US$ 2.536 por/ha (en 2022)" (CINCIA 2019); "1.100 plántulas" per ha (p.25–26) (EN: recovery cost of US$933/ha for natural regeneration and US$2,536/ha; 1,100 seedlings per ha).
  - Carbon, CSF-PE p.27 (opened): "US$ 10,00 por tonelada de CO2 (Banco Mundial, 2020), considerando que en cada hectárea de la Amazonía peruana hay un stock de 509 tCO2 (SERFOR, 2020)" (EN: "US$10 per tonne of CO2, with a stock of 509 tCO2 per ha of Peruvian Amazon"). **Derived:** US$ 5,090/ha at US$ 10/t, or ~US$ 25,000/ha at US$ 50/t.
  - Timber: 127 m³/ha × US$ 287/m³, and non-timber products US$ 2,344/ha (CSF-PE p.27).
  - Spillover: impacted area "puede ocurrir en hasta 12 veces más que el área de la minería (Sonter et al, 2017)" (EN: "can be up to 12 times the mining area") (p.23).
- **Comparison (derived):** at Aug 2026 prices, 1 ha mined yields ~US$ 250k of gold (§1e). Restoration plus forest carbon is ~US$ 6–8k/ha, and the CSF report's cost is US$ 1.9–3.4 M per ha (1.6–1.9 kg × US$ 1.2–1.8 M). The private gain is far below the social cost, but far above the cost of restoring the land.

---

## 8. Enforcement cost

- **Operation Mercurio launch (opened):**
  - Actualidad Ambiental, 19 Feb 2019, https://www.actualidadambiental.pe/madre-de-dios-1500-policias-y-300-militares-realizaran-operativos-contra-mineria-ilegal/: "El presupuesto para este plan contra la minería ilegal es de aproximadamente de 200 millones de soles"; "1200 policías y 300 miembros del Ejército" (EN: "the budget for this plan is about S/200 million"; "1,200 police and 300 army members").
  - Phases: ~15 days of eviction at km 106–108; 180 days of temporary bases; 2 years of consolidation.
  - USAID 2020 p.5: "the Government of Peru committed to investing about $62.5 million. The operation's initial phases included the mobilization of 1,500 police and military and 300 troops to the department for six months (Reuters 2019)". The Reuters original was not opened. Mining Weekly (2019) was blocked (403).
  - Diálogo Américas, 1 May 2019 (opened): "More than 1,500 military and police personnel"; four temporary bases; "So far [as of March 29] we destroyed 63 dredges."
  - Andina, 5 Mar 2019, https://andina.pe/ingles/noticia-bienes-incautados-la-pampa-ascienden-a-s-54-millones-informa-ministro-moran-744390.aspx (opened): seized goods worth "54 millones de soles": "203 motores, 76 balsas, 56 dragas, 132 tolvas, 141 quemadores de oro"; consolidation phase with "320" police for 180 days.
- **Troops (PR21 p.36, opened):** FFAA "en el año 2019 se contó con el apoyo de 690 efectivos; en el 2020 con 672 efectivos y al año 2021, vienen desempeñándose 887 efectivos" (EN: 690 troops in 2019, 672 in 2020, 887 in 2021), plus "la cantidad aproximada de 840 efectivos miembros de la Marina de Guerra" (EN: about 840 navy personnel). MdD police: 724 in total, 525 available (Apr 2021) (PR21 p.44).
- **Seizures (PR21 p.39):** 2019: "11590 Kg de mercurio [...] y 1174.90 gramos de oro"; 316 camps destroyed in 2019, 232 in 2020.
- **PP 0128 "Reducción de la minería ilegal" budget:**
  - IPE via El Comercio, 5 May 2025 (opened): "ascendió a S/ 89 millones en el 2024", down from S/ 121 M in 2019; "S/ 0.50 of every S/ 100" of the public-order budget.
  - PCM via Energiminas, 5 May 2026 (opened): S/ 70 M in 2025.
  - MEF Consulta Amigable (team scrape, `enforcement_intensity.md`): national PIM 2019 S/ 97.8 M; MdD executed (devengado) S/ 31.1 M (2019) → 20.2 (2020) → 9.7 (2021) → 5.0 M (2025). Most national units book their spending under Lima, so the MdD figures are a lower bound.
  - The concepts differ (PIA, PIM, executed), so **use the MEF series in the brief**.
- **Exchange rate (opened, 2026-10-13):** BCRP series PN01234PM, "Tipo de cambio de las principales monedas – promedio del período (S/ por UM) – Dólar Americano", monthly, via https://estadisticas.bcrp.gob.pe/estadisticas/series/api/PN01234PM/json/2015-1/2025-12. Annual value = mean of the 12 monthly averages (our arithmetic): 2015 3.184, 2016 3.375, 2017 3.261, 2018 3.287, 2019 3.337, 2020 3.495, 2021 3.881, 2022 3.835, 2023 3.744, 2024 3.754, 2025 3.568 soles per US$. Hard-coded in `code/v2_economics.py` (`PEN_PER_USD`); each year's spending is converted at its own rate.
- **Interdictions (opened):** Energiminas, 5 May 2026: an average of "62 operativos al mes" (2024) → 86 (2025) → "supera las 130 acciones mensuales" (2026); seizures "valorados en más de S/ 7,000 millones" over two years (EN: 62 operations a month in 2024, 86 in 2025, over 130 in 2026; seizures worth more than S/7,000 million). 2024: "más de 720 operativos de interdicción", "más de S/ 2230 millones" (team note).
- **Explosives cost:** not found.

---

## 9. Gold price and mining effort

- **No published price elasticity for Peruvian artisanal mining was found** (searches 2026-10-13).
- Swenson, Carter, Domec & Delgado (2011), *PLoS ONE* 6(4): e18875, https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0018875 (opened):
  - "gold price is linked with exponential increases in Peruvian national mercury imports over time (R2 = 0.93, p = 0.04, 2003–2009)"
  - Mining deforestation rose "from 2003–2006 (292 ha/yr) to 2006–2009 (1915 ha/year)". No elasticity is reported.
  - Rough derived arc elasticity: area ×6.6 while the price roughly doubled (≈ +18%/yr), i.e. > 2. It is confounded by the road, so **do not cite as causal**.
- Caballero Espejo et al. (2018) via USAID 2020 p.4 (opened): "even when the price decreased by 26 percent from 2012–2017, gold mining expanded by 53 percent". This argues against a simple price elasticity.
- Álvarez-Berríos & Aide (2015, ERL): most South American mining deforestation came after 2007 with the post-crisis gold demand (search snippets of the paper and Mongabay, **snippet only**).
- Related causal evidence (Colombia; snippet only, verify): Saavedra & Romero (2021, *European Economic Review* 138:103843), "Local incentives and national tax evasion": a royalty reform that cut local revenue shares raised illegal mining by 4.47 pp of mining area (DiD with **Peru as control**).
- **Suggestion:** the team can estimate its own descriptive elasticity from `data/prices_annual.csv` and MdD additions. With one region and many shocks it stays description.

---

## Political and context items worth adding to the report ("what happens next")

1. **REINFO ends on 31 Dec 2026, unless Congress acts again.** Ley 32537 (published ~26 Dec 2025) set the end date. The Executive's Ley MAPE bill (to be filed 15 Oct 2026) would move ~30,000 vigentes into a new 2-year regime from 1 Jan 2027, and the minister rules out a plain REINFO extension. (Exitosa 26 Dec 2025; RPP 9 Oct 2026.) Every past deadline since 2012 has been extended, so the base rate favours "another extension under a new name".
2. **A new government and a new bicameral Congress.** Keiko Fujimori won the 7 Jun 2026 runoff with 50.135% (Andina, 3 Jul 2026). She campaigned on cracking down on illegal mining, but Reuters judged that neither candidate would dismantle REINFO soon (5 Jun 2026). The Deputies' mining committee is chaired by Yenifer Paredes, who met informal-miner federations, and several legislators have mining ties (El Búho, 27 Aug 2026).
3. **The gold price is at record highs.** It averaged ~US$ 4,500/oz in 2026, +44% year on year (IPE via ProActivo, 17 Sep 2026); the data pack has US$ 4,411/oz for Aug 2026. One hectare of MdD alluvium is worth ~US$ 240–270k gross at that price (derived, §1e), so old pits become worth re-mining (MAAP #193: 148 → 598 dredges in La Pampa, 2021 → 2023).
4. **Illegal gold now exceeds legal gold in exports.** Illegal-origin gold was 54% of Peru's export volume in H1 2026, and 2026 is projected at ≥ US$ 16 bn (IPE via ProActivo 2026). Destinations are moving to India and the UAE (IPE 2025). This is national, not MdD-specific.
5. **Enforcement capacity at the reserve fell in 2025.** Navy units at the Malinowski River posts were "withdrawn during 2025 due to a lack of funding", followed by ~500 ha of new mining *inside* Tambopata NR (H2 2025 to Feb 2026) (MAAP #241, `maap_citations.md`).
6. **The state of emergency keeps being renewed in 60-day steps.** The latest found is DS 093-2026-PCM, from 16 Jun 2026, for Tambopata, Inambari, Las Piedras, Laberinto, Madre de Dios and Huepetuhe (Caretas, 16 Jun 2026, opened). A later renewal (due ~14 Aug 2026) **was not verified**.
7. **Money: more operations, less budget.** Interdictions rose from 62 a month (2024) to over 130 (2026) (PCM, May 2026). The PP 0128 budget fell from S/ 121 M (2019) to S/ 70 M (2025), against S/ 700 M for counter-narcotics, and MdD executed spending fell from S/ 31.1 M (2019) to S/ 5.0 M (2025) (MEF). Our data show that mining in Tambopata returned after 2021 as spending fell (description).
8. **Organized crime has entered the reserve.** La Pampa has cupos of S/ 1,000 per raft per week, and Mongabay (Feb 2026) reports violence inside the Tambopata reserve. UIF suspicious operations linked to mining reached US$ 6.0 bn in 2025 (IPE, May 2026). For FZS this is a ranger-safety issue as well as a forest issue.
9. **REINFO does not legally cover La Pampa.** 99.9% of MdD REINFO registrations lie inside the D.L. 1100 corridor (our overlay), so mining in the Tambopata buffer zone outside the corridor is illegal by location. A Ley MAPE that "prioritizes those in REINFO" therefore does not legalize La Pampa. The risk is laundering corridor paperwork, plus pressure to redraw the corridor (the corridor is a D.L. and could be amended; speculation).
10. **Low tax wedge, high social cost.** A formal small producer pays 0% royalty, and income tax worth ~3–11% of gold value (derived). The social cost is US$ 1.2–1.8 M per kg (CSF-PE). Making formal gold cheaper to sell than illegal gold (traceability, RECPO, buyer due diligence in India/UAE/Switzerland/US) would probably move more output than tax changes would. This is a policy speculation, labelled as such.

---

## Gaps (not found or not verified)
- A peer-reviewed gold-per-hectare figure for **La Pampa suction-pump mining**. CSF says grades for that method "no fueron identificadas".
- A peacetime price discount for illegal vs formal gold in MdD.
- The original IPE reports. Only press coverage was opened, and the method is described only as "exports minus MINEM production".
- The full text of Ley 32537, D.L. 1351 and DS 012-2025-EM (El Peruano not opened). Also the eligibility of mining concession holders for RMT/RER.
- The cost of explosives and equipment destruction per interdiction, and the Reuters 2019 original for the US$ 62.5 M figure.
- Any published price elasticity of artisanal mining effort in Peru.
- Whether the MdD state of emergency was renewed after ~14 Aug 2026.
