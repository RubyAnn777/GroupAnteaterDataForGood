# Qualitative background: legality, enforcement, economics, health, Brazil (Q2)

Compiled 2026-10-12 (access date for every source below). Tools: WebSearch/WebFetch, curl, OpenAlex/Semantic Scholar APIs, **3 Firecrawl calls** (2 searches, 1 scrape).
Rules followed: only sources I opened are cited as "opened". "snippet" = seen only in a search result, not opened. Nothing committed; no other repo file edited.

**Three Peruvian PDFs used heavily below.** They were downloaded by the enforcement-intensity run and are logged, with SHA-256, in `docs/overnight/notes/enforcement_intensity.md` (raw files in `data_raw/enforcement_peru/pdf/`). I read their extracted text.
- **[PR21]** MINAM (2021), *Plan Restauración: Plan integral frente a la minería ilegal* (annex to DS 017-2021-MINAM). https://faolex.fao.org/docs/pdf/per206467anx.pdf. Page = PDF page = printed page.
- **[MINAM16]** MINAM (2016), *La lucha por la legalidad en la actividad minera (2011-2016)*, Informes sectoriales. https://www.minam.gob.pe/informessectoriales/wp-content/uploads/sites/112/2016/02/12-La-lucha-por-la-legalidad-en-la-actividad-minera.pdf. Page = PDF page.
- **[DAR23]** Vásquez & Vara (2023), *Desafiando la legalidad y la justicia: minería ilegal en Madre de Dios*, DAR. https://dar.org.pe/wp-content/uploads/2024/08/Mineria-ilegal-en-Madre-de-Dios-version-final.pdf. Printed page = PDF page − 2; both are given.

Related notes that already cover parts of this (not repeated here): `maap_citations.md` (MAAP #130, #193, #208, #241), `enforcement_timeline.md`, `enforcement_intensity.md` (PP 0128 spending, interdiction counts), `brazil_enforcement.md`, `brazil_data_and_operations.md`, `literature.md`.

---

## 1. Illegality: what is legal where in Peru

### 1a. Illegal vs informal (D.L. 1105, 19 Apr 2012), opened
Source: Decreto Legislativo 1105, *El Peruano*, 19 Apr 2012, INGEMMET copy https://portal.ingemmet.gob.pe/documents/73138/97939/DL_1105.pdf/8ca1e06d-5f29-4936-aa03-e75ee3b35f84 (PDF text extracted locally).
- **Art. 2(a), Minería Ilegal:** "Actividad minera ejercida por persona, natural o jurídica, o grupo de personas organizadas para ejercer dicha actividad, usando equipo y maquinaria que no corresponde a las características de la actividad minera que desarrolla (Pequeño Productor Minero o Productor Minero Artesanal) o sin cumplir con las exigencias de las normas de carácter administrativo, técnico, social y medioambiental que rigen dichas actividades, o que se realiza en zonas en las que esté prohibido su ejercicio. Sin perjuicio de lo anterior, toda actividad minera ejercida en zonas en las que esté prohibido el ejercicio de actividad minera, se considera ilegal."
- **Art. 2(b), Minería Informal:** the same failings, but "en zonas no prohibidas para la actividad minera y por persona [...] que hayan iniciado un proceso de formalización conforme se establece en el presente dispositivo."
- **Art. 3:** "El Proceso de Formalización culmina en un plazo máximo de veinticuatro (24) meses. Por Decreto Supremo [...] podrá ampliarse el mencionado plazo."
- **Art. 4, six steps:** "1. Presentación de Declaración de Compromisos. 2. Acreditación de Titularidad, Contrato de Cesión, Acuerdo o Contrato de Explotación sobre la Concesión Minera. 3. Acreditación de Propiedad o Autorización de Uso del Terreno Superficial. 4. Autorización de Uso de Aguas. 5. Aprobación del Instrumento de Gestión Ambiental Correctivo. 6. Autorización para Inicio/Reinicio de Actividades [...]"
- **The key point for the brief:** location decides the category. Outside a permitted zone, any mining is illegal (a crime). Inside a permitted zone, a miner who has started formalization is "informal" (an administrative failing, not a crime). MAAP #208 note 3 says the same (see `maap_citations.md`).
- MINAM16 p.82 confirms the formalization cut-off: "el 19 de abril de 2014 era la fecha de corte del proceso de formalización".
- DAR23 PDF p.24 (printed p.22): formalization "lo que los exime de responsabilidad penal" (registered miners are exempt from criminal liability).

### 1b. The Madre de Dios mining corridor (D.L. 1100, Feb 2012, Anexo 1), opened
- PR21 p.87: D.L. 1100 "a través de su Anexo N° 1 establece las zonas en las que se pueden realizar las mencionadas actividades [pequeña minería y minería artesanal en Madre de Dios], disponiendo de manera expresa en su tercera disposición complementaria y final, que fuera de tales limites no se otorgarán concesiones mineras ni se ejecutarán actividades de exploración, explotación o beneficio." Its fifth final provision: no "adecuación, promoción o formalización de actividades mineras que se realicen en áreas sujetas a procedimientos especiales tales como, Parques Nacionales, Santuarios Nacionales, Santuarios Históricos u otras zonas reservadas [...] así como en las zonas no comprendidas en el citado Anexo 1."
- MINAM16 p.48: "El mal llamado corredor minero en Madre de Dios tiene una extensión de 4 982.96 Km 2 ó 498 296 Has." and "La zona denominada 'La Pampa' (Zona de Amortiguamiento de la RNTC) tiene una extensión de 1 240.58 Km 2 ó 124 058 has." The same page: "La existencia del corredor minero no es una autorización para destruir la Amazonía, sino que es la determinación de una zona en la que se permite la actividad minera responsable".
- MINAM16 p.13-14 (precursor): Decreto de Urgencia 012-2010 (Feb 2010, García government) set "las zonas de minería aurífera así como zonas de exclusión minera, con lo que se prohibió del uso de dragas en los ríos y se reguló su decomiso y destrucción".
- **What this means by zone (synthesis; each piece sourced above or in `maap_citations.md` for MAAP #208):**

| Zone | Status |
|---|---|
| Inside the corridor (Anexo 1), with concession + REINFO | "informal" until fully formalized; not a crime |
| Inside the corridor, no REINFO / using banned equipment | illegal under Art. 2(a) (equipment / rules) |
| Outside the corridor: La Pampa (Tambopata buffer zone), other buffer zones, native-community lands, rivers/water bodies | illegal: "zonas en las que esté prohibido"; MAAP #208: "probable illegal mining" |
| Inside protected areas (Tambopata NR, Bahuaja-Sonene NP, Amarakaeri RC) | illegal; no formalization possible (5th final provision) |
| Dredges on rivers | banned since DU 012-2010 / D.L. 1100 (MINAM16 p.46: "dragas (que hoy están prohibidas)") |

### 1c. Ley 27651 (2002) categories, opened (MINAM16 p.44-45, table)
"ARTESANAL (LEY N.° 27651)": "Hasta 25 TM/día" or "Hasta 200m3/día", concessions "Hasta 1,000 hectáreas", Derecho de vigencia "US$ 0.50 por año por hectárea". "PEQUEÑA ESCALA (LEY N.° 27651)": "Hasta 350 TM/día" / "Hasta 3,000 m3/día", "Hasta 2,000 hectáreas", "US$ 1.00 por año por hectárea". General regime: "US$ 3.00 por año por hectárea". MINAM16 p.45 comment: "¿alguien podría suponer que es minería artesanal aquella que usa maquinaria tipo dragas, carrancheras o cargadores frontales? [...] Definitivamente que no". The p.44 text also notes concessions are so large that holders "invitan a otros a operar en su concesión, sin título o acuerdo".

### 1d. REINFO and its extensions
- Origin, opened: DAR23 PDF p.24 (printed p.22): "en el año 2016, se promulgó el Decreto Legislativo 1293, que estableció la formalización de la minería artesanal y de pequeña escala, y la creación del Registro Integral de Formalización Minera (REINFO), a cargo del Ministerio de Energía y Minas (MINEM)."
- Madre de Dios counts in 2021, opened: PR21 p.55-56: "el total de mineros en vías de formalización en Madre de Dios es de 9,592 [...] Manu y Tambopata [...] con 4,762 y 4,830 mineros"; "solo 145 mineros en Madre de Dios se encuentran totalmente formalizados."
- National, opened: Energiminas, 5 May 2025, https://energiminas.com/2025/05/05/us7000-millones-en-oro-ilegal-el-crimen-crece-y-el-reinfo-blinda/: "el 76% de los 84,470 registros están suspendidos"; suspended registrants still count as "informales" and not "ilegales", so they can avoid enforcement.
- Extension chain (counts differ between sources):
  - Ley 31388 (promulgated 31 Dec 2021) → 31 Dec 2024. Caretas, 6 Jan 2025, opened, https://caretas.pe/medio-ambiente/formalizacion-minera-demandan-anular-extension-del-reinfo-por-inconstitucional: "extender por quinta vez el proceso de formalización minera".
  - Ley 32213 (27 Dec 2024) → 30 Jun 2025, extendable 6 months. Same Caretas page: "extiende por sexta vez el plazo del Registro Integral de Formalización Minera". Gestión/IPE, 18 Feb 2025, opened: the Congress "prorrogó por quinta vez la vigencia" until 30 Jun 2025.
  - DS 012-2025-EM → 31 Dec 2025, valid registrations only; MINEM excluded "50.565 inscripciones" (snippet: lpderecho.pe PDF and reporteminero.cl; not opened).
  - **Latest:** a Comisión Permanente vote (13 for, 4 against, 2 abstentions) extended REINFO to **31 Dec 2026** or until a new MAPE law comes into force; "mantiene la exclusión de aproximadamente 50 mil registros". Canal N, opened (page undated; December 2025 per search snippets), https://canaln.pe/actualidad/congreso-amplia-reinfo-hasta-diciembre-2026-n489007. Mongabay/Forbidden Stories (3 Feb 2026, opened, §3) also says the deadline was extended to December 2026. Rospigliosi announced a further extension debate in 2026 (snippet: caretas.pe/?p=814545). **Status after June 2026 not verified.**

### 1e. MAAP #235's "presumption of illegality", opened
MAAP #235, "AI-powered detection of Amazon gold mining deforestation in real-time", 13 Nov 2025, https://www.maapprogram.org/amazon-gold-mining-2025/, Annex "New functionality: Legality of mining sites". It is location-based ("Based on an analysis of potential overlaps with land designations and applicable regulations"):
- **Very High:** "Activity is occurring without a permit and within a protected area that doesn't allow for any kind of resource exploitation"
- **High:** "Activity if occurring outside of any explicit concession for doing so"
- **Medium:** "Activity is happening within a concession, but active status could not be verified and/or concession doesn't meet legal requirements"
- **Low:** "Activity is happening within active concession, but compliance with all requirements could not be verified"
- Covers Bolivia, Brazil, Colombia, Ecuador and Peru. Peru example: San José de Karene native community = "High". Peru 2025 = 6,511 ha of recent mining expansion. (Ruby's `readings.md` gives 222 areas / 14,004 ha for 2025 PAs + ITs, from a different MAAP post; not re-checked.)
- **Use:** our MapBiomas class "Minería" cannot tell legality. MAAP's ladder gives a defensible proxy: corridor + REINFO = Low/Medium; buffer zone/native community outside the corridor = High; inside the reserve = Very High.

---

## 2. Enforcement history in Madre de Dios, 2009-2026

| When | Event | Source (opened unless marked) |
|---|---|---|
| 2009-2010 | Minister Antonio Brack issues the first rules by emergency decree, "que a su vez sustentan las primeras acciones de interdicción y control" | MINAM16 p.24 |
| Feb 2010 | DU 012-2010: mining and exclusion zones in MdD, dredges banned | MINAM16 p.13-14 |
| 2009 | "Large scale enforcement campaigns against illegal mining conducted by the Peruvian National Police began in 2009 when deforestation totaled 31,165 ha. By the end of 2017 [...] 95,750 ha, an increase of more than 240%" | ResearchGate paper quoted in Ruby's `readings.md` (Three decades of deforestation…); **not re-opened by me** |
| Feb/Apr 2012 | D.L. 1100 (interdiction, corridor) and D.L. 1105 (formalization) under Humala's delegated powers; also D.L. 1102 (crime, 4-8 yrs), 1103 (chemical inputs: mercury, cyanide, fuel), 1107 (machinery, gold trade) | MINAM16 p.24, p.48; DAR23 PDF p.22-24 (printed 20-22) |
| 2012-2013 | "interdictions that are said to have eradicated 90% of miners in the buffer zone in 2012–2013", then "a near doubling of the deforestation rate from mining in 2013–2014" | Asner & Tupayachi 2017, ERL, https://iopscience.iop.org/article/10.1088/1748-9326/aa7dab |
| 2012-2015 | D.L.s and the dredge ban "ha permitido reducir en 50 % la tasa de deforestación causada por este tipo de actividad" (MINAM's own claim) | MINAM16 p.48 |
| 2013-May 2016 | ACAFMIRA interdictions in MdD: 49 (2013), 22 (2014), 28 (2015), 1 (Jan-May 2016) | MINAM16 p.159, Tabla 15 (via `enforcement_intensity.md`) |
| 2014 | Police raid in Huepetuhe "destruyó equipos de minería por valor de US$20 millones" (exact month not given) | InSight Crime, 11 Mar 2019, https://insightcrime.org/es/noticias/noticias-del-dia/peru-sin-ideas-contra-mineria-ilegal-madre-de-dios/ |
| 19 Apr 2014 | Formalization cut-off of D.L. 1105; then "saneamiento" register (>40,000 enrolled) | MINAM16 p.82, p.87 |
| 2016-2017 | REINFO created (D.L. 1293); first of many extensions "desde 2017" | DAR23 PDF p.24; Energiminas 2025 |
| Nov 2018 | "Plan Integral frente a la Minería Ilegal La Pampa" approved by the Comisión Multisectorial (later called "Plan Mercurio") | PR21 p.7, p.24-25 (Tabla 1 source: "noviembre 2018, Resumen Ejecutivo") |
| 19 Feb 2019 | Operation Mercurio launched: "1,272 PNP agents [...] 300 Armed Forces members, and 70 Public Ministry representatives"; stage 1 "will last 14 days", consolidation "will last six months" | Andina, 19 Feb 2019, https://andina.pe/Ingles/noticia-peru-law-enforcement-agents-carry-out-operation-against-illegal-mining-742954.aspx |
| 2019-2021 | Three phases: Intervención (incl. "desalojo a los comerciantes ubicados en el km 106 al 108"), Consolidación ("tres Bases Temporales Mixtas de Alta Movilidad" in La Pampa), Sostenibilidad ("abarcará todo el 2021"). "las dos primeras tuvieron una duración de 12 meses aproximadamente" | PR21 p.33 |
| 2019 (month not given) | **Expansion:** police plan "MERCURIO II 2019" (Disposición de Comando N° 1873-2019-SCG-PNP/OFIPOI), "cuya misión amplía el teatro de operaciones en todo el departamento de Madre de Dios y provincias limítrofes con los departamentos de Cusco y Puno" | PR21 p.33 |
| Dec 2019 / 2020 | "in December 2019, as part of Operation Mercury, the Public Ministry [...] led an interdiction" in the Amarakaeri buffer zone (Camanti); "In 2020, as part of an extension of Operation Mercury, the Environmental Prosecutor's Office (FEMA) [...] announced that the buffer zone of the Amarakaeri Communal Reserve will be constantly monitored." | MAAP #115, Finer & Mamani, 17 Jan 2020, https://www.maapprogram.org/?p=20851 |
| 2019 vs 2020 | DIRMEAMB interdictions 198 → 231, almost all in Tambopata; FFAA personnel 690 / 672 / 887 (2019/20/21) | PR21 p.34-36 (via `enforcement_intensity.md`) |
| Spring 2020 | Forces stay "until the spring of 2020", then are "pulled away to address the pandemic" | Dartmouth press release on Dethier et al., Sep 2023, https://home.dartmouth.edu/news/2023/09/operation-mercury-curbed-illegal-gold-mining-peru |
| 2020-2021 | "there was a reduction in military and police presence at the bases, and deep budgetary cuts"; the pandemic was a "substantial setback" for financing | Mongabay, Dec 2023, https://news.mongabay.com/2023/12/perus-crackdown-on-illegal-gold-mining-a-success-but-only-briefly-study-shows/ |
| 2019→2021 | PP 0128 spending executed in MdD: S/ 31.1 M (2019) → 20.2 M (2020) → 9.7 M (2021) → 5.0 M (2025) | MEF Consulta Amigable, computed in `enforcement_intensity.md` §2a |
| Mar 2021 | RM 083-2021-PCM creates the working group for a new plan | PR21 p.25 |
| 24/25 Jul 2021 | **Plan Restauración** (DS 017-2021-MINAM): "asegura la continuidad y consolidación de las acciones frente a la minería ilegal" begun in 2019 as "Plan Mercurio"; adds Camanti (Cusco) and Ayapata (Puno); aims to contain the "efecto globo" | Andina, 25 Jul 2021, https://andina.pe/ingles/noticia-mineria-ilegal-aprueban-plan-restauracion-madre-dios-y-distritos-cusco-y-puno-854803.aspx |
| "Desde julio de 2021" | "la Operación Mercurio fue reemplazada por el Plan de Restauración (2021-2023)" | DAR23 PDF p.21 (printed p.19) |
| 2021-2022 | Castillo government: "the multiple ministerial changes [...] made maintaining a consistent policy near impossible"; some miners began to return "when enforcement relaxed in 2022" | Mongabay Dec 2023; Dethier et al. 2023 abstract |
| 7 Apr 2023 → | State of emergency (DS 046-2023-PCM) in 6 districts, renewed every 60 days | MAAP #241 (`maap_citations.md`) |
| 2023 | "Solo en Madre de Dios se realizan unos 25 operativos al mes"; only 2 FEMA prosecutors left | Actualidad Ambiental, 2 Mar 2023 (via `enforcement_intensity.md`) |
| 2025 | Navy withdrawn from Malinowski posts for lack of funds; 193 interdictions in MdD in 2025; ">5,000 dredges and tracas" in La Pampa and Delta Uno (national environmental prosecutor) | MAAP #241; Mongabay/Forbidden Stories, 3 Feb 2026 (§3) |

**Anti-corruption / monthly rotation.** Dethier et al. (2023) is titled "...armed forces intervention and anticorruption strategy..." (opened, metadata). I could **not open the full text**: the Firecrawl query failed, and the Wiley/MDPI pages return 403 to scripts. The press release and Mongabay coverage do not mention monthly rotation. The "monthly rotation of garrisons and commanders" claim in `docs/PLAN_v2.md` must be checked in the paper PDF before we cite it. The only documented failure I found is a June video of a soldier taking a presumed bribe from miners in La Pampa (Actualidad Ambiental headline; snippet, year not seen).

**Political cycle (testing the team's 2-year-dip hypothesis).** Presidents, from Wikipedia "List of presidents of Peru" (opened):

| President | In office | How it ended |
|---|---|---|
| Alan García | 28 Jul 2006 – 28 Jul 2011 | end of term |
| Ollanta Humala | 28 Jul 2011 – 28 Jul 2016 | end of term |
| Pedro Pablo Kuczynski | 28 Jul 2016 – 23 Mar 2018 | resigned |
| Martín Vizcarra | 23 Mar 2018 – 9 Nov 2020 | impeached ("vacancia") |
| Manuel Merino | 10–15 Nov 2020 | resigned |
| Francisco Sagasti | 17 Nov 2020 – 28 Jul 2021 | end of term |
| Pedro Castillo | 28 Jul 2021 – 7 Dec 2022 | impeached |
| Dina Boluarte | 7 Dec 2022 – 10 Oct 2025 | impeached |
| José Jerí | 10 Oct 2025 – 17 Feb 2026 | censured |
| José María Balcázar | 18 Feb 2026 – 28 Jul 2026 | end of term |
| Keiko Fujimori | from 28 Jul 2026 | incumbent |

- **Description, not evidence:** both dips start about 7-11 months after a new president takes office: the Humala decrees in Feb/Apr 2012, and Mercurio in Feb 2019 (Vizcarra from Mar 2018; plan approved Nov 2018). Both fade within roughly two years: the 2013-14 rebound, and 2020-21 with COVID, Vizcarra's removal and Castillo's ministerial churn. The money series fits: PP 0128 in MdD jumps from S/ 0.65 M (2018) to S/ 31.1 M (2019) and falls back by 2021.
- **What is missing:** we have no causal evidence on election-year effects in Peru. The only peer-reviewed election-deforestation results found are for Brazil (Pailler 2018: municipal deforestation +8-10% in election years with an incumbent running; snippet via Mongabay), the Atlantic Forest (Ruggiero et al. 2021) and pan-tropical data (Morpurgo et al. 2023). See `literature_v2.md`. Congress's repeated REINFO extensions (2021, 2024, 2025) are a second, documented political channel.

---

## 3. The 2017 spike in La Pampa

- **Size, opened:** Caballero Espejo et al. (2018) abstract: "10% of that deforestation occurred in 2017, the highest annual amount of deforestation in the study period, with 53% occurring since 2011." MAAP #208: "Illegal gold mining reached crisis levels between 2017 and 2018 in the area known as La Pampa" (`maap_citations.md`). Our MapBiomas Tambopata BZ additions: 707 ha (2016), 2,455 ha (2017), 1,757 ha (2018) (`output/peru_additions_2014_2025.csv`). Warning: `output/peru_anp_tambopata_class_change_2016_17.csv` shows a 2016→17 class shift, so part of the jump may be reclassification.
- **Gold price, against the price story (repo data, `data/prices_annual.csv`):** USD/oz 1,160.75 (2015), 1,249.0 (2016), 1,257.5 (2017), 1,269.25 (2018). The price was flat across 2016-18, so it cannot explain a one-year tripling. The price surges were in 2008-2012 (Asner et al. 2013: forest loss "tripled in 2008 [...] closely associated with increased gold prices") and in 2020 and 2024-25.
- **Gangs ("Guardianes de la Trocha"), opened:** Mongabay Latam + Forbidden Stories, "Perú: así funciona el sistema de extorsiones, amenazas y asesinatos que devasta los bosques en La Pampa", Yvette Sierra Praeli, 3 Feb 2026, https://es.mongabay.com/2026/02/peru-extorsiones-asesinatos-devasta-bosques-la-pampa/.
  - Criminal groups arrived "hace por lo menos diez años". Witness timeline: robberies and kidnappings from 2011; paying for "la seguridad" from 2013-14; killings from 2016. The Guardianes are "el grupo, por así decirlo, más fuerte".
  - Cupos of "1,000 soles a week per balsa"; control of gold transport; camera surveillance.
  - **The article gives no founding or takeover year, so a "2017 gang takeover" is not documented by this source.** A death toll of "at least 400" in 12 years (El Búho, citing Dirincri) is a snippet only.
- **Mercury, partial evidence:** DAR23 PDF p.24 (printed p.22): "en el año 2015, el Estado peruano tomó medidas para controlar las importaciones de mercurio [...] en el año 2016, ratificó el Convenio de Minamata". Swenson et al. 2011: Peru's mercury imports tracked the gold price (R² = 0.93, 2003-2009). EIA (July 2025, executive summary, opened): "200 tons of mercury smuggled from the mercury mines in Mexico (state of Queretaro) to the gold mines in Bolivia, Colombia, and Peru between April 2019 and June 2025", and "an average difference of at least 400 percent in the price paid for mercury at the gold mines in Colombia and Peru compared to Mexico (based on data gathered from February 2023 to June 2025)". **I found no 2016-2018 mercury price series for Madre de Dios.** The "Minamata → mercury price spike → gangs → 2017" chain is plausible but undocumented; present it as a hypothesis.
- **Better-documented candidates for 2017** (description): enforcement was nearly absent (ACAFMIRA interdictions in MdD fell from 49 in 2013 to 1 in Jan-May 2016; PP 0128 MdD spending S/ 0.24 M in 2016); and the Interoceanic Highway (km 98-115) gave road access to La Pampa (Asner et al. 2013 describe road- and river-based mining).

---

## 4. Taxes, costs, competition; why declared production fell

### 4a. What a formal small miner pays (opened unless marked)
- **Royalty (regalía minera):** Ley 28258, Art. 4.4 (vLex copy, https://vlex.com.pe/vid/ley-n-28258-regalia-735742481): "En el caso de los pequeños productores y mineros artesanales la regalía minera será de cero por ciento (0%)".
- **IGV/VAT on gold:** gold in raw form (7108.11/7108.12) is exempt under Apéndice I of the IGV law, with a 1.5% withholding (detracción) on the sale. SUNAT, "Apéndices del Sistema de Detracciones", https://orientacion.sunat.gob.pe/apendices-del-sistema-de-detracciones: "Oro y demás minerales metálicos exonerados del IGV (Anexo 2, código 36): 1.5%", which includes sales under "Ley N.° 27037 - Ley de Promoción de la Inversión en la Amazonia" (amalgam, gold waste, Chapter 26 ores). Taxed gold, or a seller who renounced the exemption: 10%.
- **Fuel:** fuel sold in the Amazon is IGV- and ISC-exempt. The IPE estimates S/ 2,940 M of forgone revenue in MdD over 20 years, "72% [...] (S/2,111 million) benefited illegal mining". Gestión/IPE, 18 Feb 2025, https://gestion.pe/economia/mineria-ilegal-capto-millones-aprovechando-beneficios-del-estado-ipe-combustible-subsidios-noticia/
- **Income tax:** 30% third-category rate, used in the CooperAcción evasion estimate (MINAM16 p.75, Tabla 3 note 2: "Resulta de aplicar la tasa del impuesto de 30 % sobre la utilidad"). Whether small producers use a lighter regime (RER/RMT) **was not verified**.
- **Costs of formalization:** six steps (D.L. 1105 Art. 4), the derecho de vigencia (US$ 0.50-1.00/ha/yr, Ley 27651), and an environmental instrument (IGAC). Álvarez-Berríos et al. (2021): "Miners resented the slow, costly formalization process but many sought titles to bolster territorial claims, avoid policing, obtain credit and recruit paying 'guest' miners who generally ignored regulations." **No peso/sol figure for the total cost of formalizing was found.**
- **Old canon gap:** DAR23 PDF p.21 (printed 19): the gold extracted is worth "S/. 1,600 millones anuales", but the region "sólo percibe S/. 42,000 por canon minero dejando de percibir entre 50 y 200 millones de soles en impuestos" (citing IIAP & MINAM 2011). MINAM16 p.73: "la región de Madre de Dios dejó de percibir por concepto de canon minero entre USD 47 y 73 millones en promedio anual durante el periodo 2003-2014" (Torres Cuzcano 2015).
- **Tracing gold:** the Registro Especial de Comercializadores y Procesadores de Oro (RECPO) had "más de 4 500 inscritos (es necesaria una depuración del mismo)" (MINAM16 p.240). Plan Restauración still lists "Reglamentación del Registro Especial de Comercializadores y Procesadores de Oro- RECPO e implementación de la aplicación para registrar las compras del oro" as a to-do (PR21 p.13, p.134).

### 4b. Declared production down, mapped mining up: evidence

The hypothesis to test: "miners in the legal corridor mine informally or illegally and do not declare their production".

**Evidence FOR (opened):**
1. **The official series falls long before 2019.** PR21 p.57, Tabla 17 (MINEM): Madre de Dios declared gold (TMF) 19.1 (2010), 22.6 (2011), 12.3 (2012), 16.1, 8.0, 12.7, 17.6, 12.8, 10.2 (2018), 7.1 (2019). Over the same years Puno rose 2.8 → 9.1 and Cusco 2.4 → 6.2.
2. **Ministry-level fall after 2019.** "la producción de oro en Madre de Dios se redujo 84% entre 2019 y 2024", per MINEM data. The same article says official figures do not reflect illegal mining (Energiminas, 5 May 2025). Gestión/IPE 2025: MINEM estimates "show a continuous decline since 2016", but "la realidad es otra" (more deforestation, crime and fuel use).
3. **Smuggling to Bolivia (official).** PR21 p.92: "A nivel nacional se observa una brecha entre la exportación y la producción de oro que, al 2019 alcanzaría las 24.9 toneladas al año. [...] Para el caso específico de Madre de Dios, dada su cercanía con la frontera con Bolivia, se presume que el oro informal y/o ilegal producido estaría saliendo de contrabando hacia el mencionado país". Tabla 27 gives Bolivia's gold exports: 1.7 t (2012) → 8.2 (2013) → 35.7 (2014) → 31.9 (2018). The jump starts right after the 2012 decrees. PR21 p.91: SUNAT and MINEM estimate MdD + Puno illegal production at "46.72 toneladas para el periodo 2019".
4. **Most mining is in the corridor, and the corridor is mostly not formal.** MAAP #208: 74% of 2021-24 mining deforestation lies inside the corridor. Only 145 of 9,592 REINFO miners in MdD were fully formalized (PR21 p.56). Formal status costs a 0% royalty and a 1.5% withholding, so declaring is cheap. That points to the main reason for not declaring being the illegal origin of the ore, or selling through traders who launder it, rather than tax.
5. **Unknown origin nationally.** Mongabay/Forbidden Stories 2026: of ~180 t of gold exported in 2024, "at least 80 tonnes" were of "origen desconocido". IPE: illegal exports of 92 t in 2024 (Gestión) or US$ 7,415 M (Energiminas).
6. **Laundering through REINFO paperwork** (snippets, not opened): a La Libertad conviction where the gold "ingresó al mercado formal tras verificarse únicamente la vigencia del [...] Reinfo y del RUC"; Caretas: REINFO "ha permitido formalizar entre comillas [...] la extracción de minerales y llevarlos a plantas de beneficio".

**Evidence AGAINST, or alternative explanations:**
- Mercurio really cut La Pampa output, which was the region's biggest producer. The Artisanal Gold Council (2017) sector table, quoted in DAR23 PDF p.47, puts La Pampa at 66 of ~83 t/yr (23-carat). That regional total is far above any official figure (MdD declared 12.8 t in 2017), so treat it with caution. Either way, La Pampa was the dominant producer, and part of the fall is real.
- Declared output may be re-registered where gold is processed or sold (Puno, Cusco, Arequipa/Nazca plants). The Puno and Cusco rise in Tabla 17 fits this, but also fits real growth (e.g. La Rinconada). **No source found that traces MdD gold declared in other regions.**
- Mapped area is a stock and includes re-mined old pits (MAAP #193: return on degraded land), so area can rise while output falls.
- **Verdict:** consistent with the hypothesis, but the evidence is indirect. In the brief, call it "description + plausible mechanism", not a finding.

### 4c. Size of the illegal economy (opened)
MINAM16 p.72: in 2012 MINEM estimated "la producción estimada de oro de procedencia informal e ilegal era de 40 toneladas anuales, por un valor aproximado de USD 2 146 millones"; in 2011-12 "la producción informal de oro se calculaba en 20 % de la producción nacional". Gestión, 4 Oct 2026: MdD concentrates "entre un 35% a 38% de la producción ilegal de oro en el país" (FCDS estimate).

---

## 5. Social and health

### 5a. Miners and livelihoods (opened)
- ACCA & USAID Prevenir (2022), quoted in DAR23 PDF p.29 (printed 27): "existen al menos 46,605 mineros artesanales, dentro de los cuales 31,390 son mineros informales y 9,323 son mineros ilegales". Method: 3,551 machines identified on sub-metre imagery × crew size from 260 interviews.
- Gestión, 4 Oct 2026, https://gestion.pe/economia/ingreso-en-madre-de-dios-crecio-40-entre-2017-y-2025-pero-desarrollo-humano-no-se-movio-mineria-ilegal-acecho-noticia/: "cerca de 46,601 habitantes de Madre de Dios (un 35.4% de su población) estaba vinculada directamente a la minería"; 12.6% formal, 67.3% informal, 20.01% illegal. Household incomes "se incrementaron en promedio en 40% entre los años 2017 y 2025" (Apoyo Consultoría); HDI "tuvo un crecimiento de 0 puntos entre los años 2017 al 2024".
- DAR23 PDF p.55 (printed 53): "Aproximadamente alrededor de 30,000 personas dependen de la minería de oro en Madre de Dios"; about 20,000 work with front loaders and trucks, ~500 operate dredges. The workers are mainly migrants from the Andes.
- Mongabay 2023: "around 50,000 miners, according to a 2022 study by USAID".
- **No individual wage figure found** (daily or monthly pay). CSF methodology p.11: the miner's profit is "cerca de 30%" of the gold value (a Brazilian assumption).

### 5b. Human trafficking (opened)
DAR23 PDF p.56 (printed 54), citing MINAM (2013): "alrededor de 4,500 mujeres están sometidas a explotación sexual en los establecimientos de comida y bares ubicados cerca de los campamentos mineros ilegales. De este grupo, el 78% son menores de edad y el 52% proviene específicamente de la región de Cusco." p.57: "más de cien establecimientos conocidos como «prostibares»" in Huepetuhe, Delta 1, La Pampa area camps, among others. Labour trafficking of young men from Cusco, Puno, Apurímac and Arequipa.

### 5c. CSF Mining Impacts Calculator (opened)
- Summary page, https://miningcalculator.conservation-strategy.org/methodology/resume: three damage categories ("Deforestation", "River sedimentation and soil erosion", "Environmental contamination by mercury, and its effects on human health"). Inputs include mining type ("alluvial, raft, or sinkhole"), population density and fish consumption. **Peru: "1 kg of gold generates socio-environmental impacts worth between US$81,000 and US$364,000."**
- MAAP #235 Annex: the calculator uses "the size of the mine, the amount of gold produced and the time of extraction" and is now built into Amazon Mining Watch.
- Methodology report (Brazil version): Gasparinetti, Bakker, Queiroz, Vilela, Lobo & Nagel (2021), *Metodologia de Valoração de Impactos do Garimpo Ilegal de Ouro na Amazônia*, CSF Série Técnica 53, https://miningcalculator.conservation-strategy.org/assets/download/metodologia.pdf (downloaded, text extracted). Default assumptions:
  - Hg:Au ratio: "pode variar consideravelmente de 1,3 até 8 gramas de mercúrio para cada grama de ouro extraído [...] Assume-se aqui uma proporção média (Hg:Au) de 2,6 :1" (section 3.5.1)
  - Release to water: "considera-se, de forma conservadora com um total de dispersão na água e solo de 12%, cerca de 7% do mercúrio utilizado" goes to water
  - Downstream reach: "estudos [...] variando de 4 até 100 km"; "em rios amazônicos, o raio de impacto significativo é de cerca de 50 km à jusante"; migratory catfish "podem migrar por 2000 km"; the calculator "assume-se a hipótese conservadora de que o mercúrio atingirá um raio de 100 km"
  - Productivity: "podem ser extraídos de 0,7 a 8,3 kg de ouro por hectare"
  - Health end-points: "(i) Perda de QI em crianças; (ii) Infarto do miocárdio; (iii) Hipertensão"
  - Brazil result: "1kg de ouro extraído gera impactos entre 1 e 2 milhões de reais, sua maioria relacionada aos impactos do mercúrio à saúde humana"; the social cost is "mais de dez vezes maior do que o benefício privado"
- Peru adoption: CSF trained "more than 200 Peruvian attorneys" (CSF page title; snippet). Mongabay (Mar 2024): Peru adopted it in 2023 (snippet).

### 5d. Mercury use, fish, people, transport (opened: abstracts via OpenAlex/Europe PMC unless noted)
- **Hg per kg gold in MdD:** the Artisanal Gold Council (2017) sector table, quoted in DAR23 PDF p.47 (printed 45, Tabla 9), uses Hg:Au ratios of 2.1:1 to 2.9:1 (La Pampa traca 2.3:1) and a total of **181.327 t Hg/yr** (La Pampa 145.2 t). The DAR text writes "181,327 toneladas", a decimal typo; the table total is 181.327.
- **Fish:** Diringer et al. 2015 (Environ. Sci.: Processes Impacts, online Dec 2014, doi:10.1039/c4em00567h): 62 sites over 560 km; ">one-third of carnivorous fish exceeding the international health standard of 0.5 mg kg-1"; "communities located hundreds of kilometers downstream of ASGM activity [...] are at risk". Vega et al. 2018, chart in DAR23 PDF p.50-51: 37% of fish from mining areas above 0.5 mg/kg vs 14% in the reference area. Martinez et al. 2018 (IJERPH): fish Hg not higher in the impacted river; sediment Hg was. So fish are a poor site-specific indicator.
- **Forests and air:** Gerson et al. 2022 (Nat. Commun., doi:10.1038/s41467-022-27997-3): intact forest near mining "intercepts large amounts of particulate and gaseous mercury"; Hg builds up "in soils, biomass, and resident songbirds in some of the Amazon's most protected and biodiverse areas". This matters for Tambopata NR itself.
- **People:** Reuben et al. 2020 (GeoHealth, doi:10.1029/2019GH000222): 164 children, mean hair Hg 2.06 µg/g, "32.9%" above the WHO 2.0 µg/g level; above-reference children "scored 4.68 IQ points lower". Carnegie 2012 (via DAR23 PDF p.51): Indigenous communities' Hg "2.5 veces más altas", and "77.9% de los adultos" above reference values.
- **Erosion:** Diringer et al. 2020 (EST, doi:10.1021/acs.est.9b06620): deforestation doubled soil mobilization in the Colorado watershed (4× in Puquiri). It also mentions the "two national state of emergency (2016 and 2019)" for mercury.
- **Downstream reach, summary:** Asner et al. 2013 (PNAS): sediment effects "persist for hundreds of kilometers, potentially well into Brazil". CSF uses 50-100 km for mercury.

---

## 6. Where enforcement would help conservation

- **The state's own map of displacement, opened:** PR21 p.50: in 2021 SERNANP found that "en el límite de la Reserva Nacional de Tambopata, los sectores de Apaylon y Alto Malinowski tienen los mayores puntos de minería ilegal". Miners now work "en horas de la noche con motores de menor potencia (18 CV)", and activity has spread to the buffer zones of Amarakaeri and Bahuaja-Sonene, and to Kosñipata, Camanti, San Gabán and Ayapata, plus Pariamanu outside the Tambopata buffer zone. p.52: San Juan del Oro and Yanahuaya (Sandia, Puno), "a 35 kilómetros aproximadamente" south of Bahuaja-Sonene NP.
- **PR21 p.53, Tabla 16 (MINAM), ha/month before → after Mercurio:** La Pampa 173 → 14 (−92%); Camanti 13.3 → 6.1 (−54%); Alto Malinowski 61 → 28 (−53%); RN Tambopata 6.5 → 0.5 (−93%); increases at Pariamanu 2.5 → 4.2 (+70%) and Apaylón 2.9 → 4 (+41%). The plan names this the "efecto globo" (balloon effect) and defines it on p.52.
- **Rivers as the access route, opened:** PR21 p.88: "los ríos Madre de Dios e Inambari son las principales vías de acceso fluvial". MAAP #241: Malinowski River posts lost their navy units in 2025, and 500 ha of mining followed inside the reserve. Asner et al. 2013: miners are "locating their operations back from the main stem of regionally important rivers [...] to better conceal their presence from law enforcement". The "within 10 km of rivers" figure **is not in the Asner et al. 2013 PNAS text** (searched the full PMC text). Do not cite it to that paper without finding the real source.
- **Roads:** Asner et al. 2013 mapped "road- and river-based gold mining" and "the thousands of small clandestine mines along roads and waterways". Mercurio's first phase evicted the traders at "km 106 al 108" of the Interoceanic Highway (PR21 p.33). Álvarez-Berríos et al. 2021 control for "accessibility".
- **Legal corridor as the release valve:** Dethier et al. 2023 (pond area +42-83%, deforestation +3-5 km²/yr just outside the targeted zone) and MAAP #208 (74% inside the corridor). For conservation, the priority is the corridor boundary near the reserve plus the river entry points (Malinowski, Tambopata, Inambari), not La Pampa alone.
- **FZS, opened:** https://fzs.org/en/programs/peru/bahuaja-sonene-and-tambopata/. "Support Peruvian authority of natural protected areas, SERNANP, in their law enforcement operations"; "Construction, equipment, and maintenance of control posts for park rangers"; "Support protected area management to undertake patrols in remote areas". The page has no explicit priority map. FZS is also named as a partner in PR21 (line ~1221: "Sociedad Zoológica de Fráncfort").
- **No published spatial prioritization study for enforcement in MdD was found.**

---

## 7. Brazil

- **Why garimpo in Indigenous lands is illegal, opened:** Constituição Federal (Planalto, https://www.planalto.gov.br/ccivil_03/constituicao/constituicao.htm), Art. 231 §3: "a pesquisa e a lavra das riquezas minerais em terras indígenas só podem ser efetivados com autorização do Congresso Nacional, ouvidas as comunidades afetadas". §7: "Não se aplica às terras indígenas o disposto no art. 174, § 3º e § 4º". Art. 174 §3-4 are the garimpeiro-cooperative priority rules. Congress has never passed the authorizing law, so no legal garimpo is possible inside a TI.
- **CFEM royalty on gold, opened:** Lei 13.540/2017, Anexo (Planalto, https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2017/lei/l13540.htm): "1,5% (um inteiro e cinco décimos por cento) — Ouro".
- **Gold rules, PLG, good faith, e-invoice, opened:** Rodrigues (2025), "Brazil's Journey Against Illegal Mining", *Brazilian Political Science Review*, doi:10.1590/1981-3821202500020006 (SciELO full text).
  - "individuals have a facilitated process to obtain wildcat mining permits and wildcat mining environmental licenses compared to the processes of companies" (the PLG regime; the paper does not use the acronym PLG)
  - "the Brazilian Supreme Court lifted the 'good faith' presumption from Law Nº 12,844 of 2013"; "the rapporteur of the action, Justice Gilmar Mendes, ruled for lifting the good faith presumption", with "a 90-day deadline to adopt a new regulatory framework" (ADI 7273; ADI 7345 is the companion case, Brasil 2026, Beijing Law Review)
  - "the Brazilian Revenue Service published a new rule adopting electronic invoices for gold from wildcat mining", "mandatory on August 1, 2023" (fn. 13)
  - Instituto Escolhas figures quoted there: "From 2015 to 2021, Brazil traded 282 tons of gold with evidence of illegality"; "In 2021 alone [...] up to 53 metric tons"; "half of the country's gold output is suspected of having dubious origin"
  - Yanomami: "In 2012, illegal mining areas in the Yanomami territory occupied 24 hectares, and in 2022, they reached 3,278 hectares"; working group created 26 Jan 2023
- **Illegality share, opened (abstract):** Cortinhas Ferreira Neto et al. 2024 (Nat. Commun.): "At least 77% of the 2022 mechanized mining area shows explicit signs of illegality"; Kayapó, Munduruku and Yanomami "concentrate more than 90% of the garimpo extraction across indigenous territories".
- **Yanomami operation phases 2023-2025:** dates for Jan 2023 (emergency), 6-10 Feb 2023 (Ibama/PF Operação Libertação), Munduruku (Aug 2023, Nov 2024) and Kayapó (May 2025) are already sourced in `enforcement_timeline.md` and `brazil_data_and_operations.md`. Newer, opened: Portal Amazônia, 28 May 2026, https://portalamazonia.com/meio-ambiente/garimpo-ti-yanomami-rr/, reporting an ISA/MAAP/Hutukara/Wanasseduume report of 22 May 2026:
  - new garimpo area "83.95" ha (2024) → "45.2" ha (2025, −46%)
  - 5,564 ha destroyed in total through Dec 2025; peak in 2022 ("1.800 hectares destruídos")
  - in 2025, 121 areas, "90% were under one hectare"; displacement toward the Venezuelan border (Parafuri-Parima, Hokomawë) and river logistics
  - Government figure (snippet only): "redução de 98,9% da área ocupada pelo garimpo ilegal" (Casa de Governo boletim, Feb 2026; it measures active area, not new clearing)
- **Health, opened (abstract):** Castro et al. 2025 (PLoS NTD): "a 1% increase in the annual mining area was associated with a 24% [...] increase in monthly malaria cases in the Yanomami"; "an estimated excess of 102,870 malaria cases occurred from 2018 to 2023".

---

## 8. Research papers
See `docs/overnight/notes/literature_v2.md` (one entry per paper).

---

## Gaps / not verified
- Full text of Dethier et al. 2023 (monthly rotation claim, exact end date of the armed-forces presence).
- Exact date of the 2023 STF injunction (the paper gives no date; ADI 7273).
- REINFO status after mid-2026; total cost of formalization in soles; income-tax regime for small producers.
- A 2016-2018 mercury price series for Madre de Dios; the founding/takeover year of Guardianes de la Trocha.
- Evidence that MdD gold is declared in other regions.
- The source of "mining within 10 km of rivers" (not in Asner et al. 2013).
