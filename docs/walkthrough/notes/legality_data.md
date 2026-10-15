# Legality data: classifying mining pixels by MAAP #235 legality level

Agent run 2026-10-12 (access date for every file below). Raw files are in `data_raw/<source>/` exactly as the server returned them. ArcGIS downloads are saved one file per request (`chunk_NNN.geojson`), with a `SHA256SUMS` file in each folder. `_objectids.json` in each folder is **ours**: it is the list of object IDs the server returned for the filter, kept so the request can be repeated. **Not yet in `DOWNLOAD_LOG.csv`** (the instruction was not to edit other repo files). Rows ready to paste are in §9.

## 0. Headline

1. **MAAP #235's four levels can be rebuilt from public data for Madre de Dios.** The legality layer behind Amazon Mining Watch (AMW) is itself public in the AMW GitHub repo (`data_raw/amw_github/illegality_v2_areas_simplified.geojson`, 69.6 MB, classes 1=Low, 2=Medium, 3=High, 4=Very High). The INGEMMET cadastre we downloaded reproduces it. Of the 27,943 AMW detection patches in the Madre de Dios bbox, by patch centroid:
   - **Low:** 12,176 of 12,263 fall in a *titled* INGEMMET right.
   - **Medium:** 6,887 of 8,451 fall in a "BLOQUEADO" (extinguished, to be published as free) right, 1,259 in an "en trámite" (application) right, and 273 in an extinguished right.
   - **High:** 6,531 of 6,983 fall outside every cadastre polygon.
   - **Very High:** 244 patches, i.e. protected areas with no resource use allowed.

   So: Low = titled concession; Medium = concession that is extinguished, blocked or only applied for; High = no right at all; Very High = strict protected area. The same mapping holds in Pará against ANM SIGMINE (§5).
2. **Warning, the BCRP series has a break.** MINEM's annual gold files up to 2019 include a block "PRODUCTORES ARTESANALES 1/ … Cifras Estimadas" for Madre de Dios, e.g. about 15.7 t in 2016 against only 486 kg declared by units. Estimate plus declared = 16.2 t, which equals the BCRP 2016 figure of 16,223 kg. **From 2020 that estimate is gone.** The "declared MdD gold production −88 % 2018→2025" in agent.md §14 (BCRP 10,077 kg → 1,234 kg) is therefore mostly the **estimate being dropped, not a fall in production**. Production declared by units (ESTAMIN) *rose*: 944 kg in 2018 to 1,362 kg in 2025. **The team must correct this claim before it goes into the brief.**
3. **Brazil:** SIGMINE (active mining processes) downloaded for RR, PA, AM and MT, plus Reservas Garimpeiras. CFEM was obtained only from Wayback Machine snapshots (2017 to March 2024), because `app.anm.gov.br` resets every connection from here (and from Firecrawl with a BR location).

## 1. Peru A: INGEMMET Catastro Minero (works)

Service directory: `https://geocatmin.ingemmet.gob.pe/arcgis/rest/services` (public, no token). ArcGIS 10.91 with **no pagination support** ("Pagination is not supported"). We fetched `returnIdsOnly` first and then POSTed `objectIds` in batches of 500, with `f=geojson&outSR=4326`.

| Folder | Layer URL | Filter | Features | Check |
|---|---|---|---|---|
| `data_raw/ingemmet/catastro_minero_wgs84_L0_mdd_bbox/` (10 chunks, 4.7 MB) | `SERV_CATASTRO_MINERO_WGS84/MapServer/0` "Catastro Minero" (daily update) | envelope −72.5,−13.5,−68.6,−9.8 (intersects) | **4,831** | server `returnCountOnly` = 4,831; downloaded 4,831 (every batch matched its ID count) |
| `data_raw/ingemmet/catastro_minero_dgm_L1_mdd_bbox/` | `SERV_CATASTRO_MINERO_WGS84/MapServer/1` "Catastro Minero – DGM (MINEM)" (rights under MINEM's DGM, i.e. larger producers) | same bbox | **153** | count = 153 |
| `data_raw/ingemmet/catastro_madre_dios_L0/` (3.5 MB) | `SERV_CATASTRO_MADRE_DIOS/MapServer/0` "Catastro Minero de Madre de Dios" (department-specific layer with **title resolution dates**) | all | **2,655** | count = 2,655 |
| `data_raw/ingemmet/catastro_madre_dios_L1_zpmma/` | `SERV_CATASTRO_MADRE_DIOS/MapServer/1` "Zona de Peq. Minería y Minería Artesanal" | all | 1 | this is the D.L. 1100 corridor again; we already have it as `corredor_minero_madre_de_dios_DL1100.geojson` |

**Fields (layer 0):** `CODIGOU` (unique right code, which joins to REINFO `ID_UNIDAD`), `CONCESION` (name), `TIT_CONCES` (holder), `HECTAGIS`, `ESTADO`/`D_ESTADO` (legal status code + text), `LEYENDA` (TITULADO / TRAMITE / BLOQUEADO / EXTINGUIDO / OTROS), `FEC_DENU` (date the claim was filed, 1977-12-02 → 2026-10-09), `RESOL_EXTI` + `FECHA_RESOL_EXTI` (extinction resolution and date; 1,891 non-null, 1993 → 2026-10-05), `CALIFICA` (M = small producer (pequeño productor), A = artisanal (productor artesanal), null = general regime), `SUSTANCIA` (M metallic / N non-metallic), `ESTADO_MINEM` (EXPLOTACIÓN 147, EXPLORACIÓN 6), `DEPA/PROVI/DISTRI`, `FECHA_ACTUALIZACION` (= 2026-10-12 for every row, so this is a **snapshot of today**). The Madre de Dios layer also has `FECHA_RESOL_TIT` (title date, 2,111 non-null, 1994 → 2026), `F_INCOR`, `TIPO_EX`, `NATURALEZA`.

**Counts (layer 0, bbox).** By LEYENDA: TITULADO 2,141 · BLOQUEADO 1,504 · TRAMITE 953 · EXTINGUIDO 126 · OTROS (canteras) 107. The bbox also catches Cusco (1,600) and Puno (278) rights. Area of rows whose DEPA contains "MADRE DE DIOS" (sum of HECTAGIS; overlaps are not removed): titled 208,834 ha · blocked 399,325 · in process 52,823 · extinguished 7,155. Claims filed per year jump in 2025 (428) and 2026 (501, to 9 Oct), compared with 50–150 a year in 2015–2021.

**Mapping to MAAP levels.** Low = inside `LEYENDA == TITULADO`. Medium = inside TRAMITE / BLOQUEADO / EXTINGUIDO and not inside any titled right. High = inside no polygon. Very High = inside a strict-use ANP (SERNANP polygons, already in `data_raw/sernanp/`). Use precedence when polygons overlap (we used TITULADO > TRAMITE > OTROS > BLOQUEADO > EXTINGUIDO).

**Limits.**
- It is a **current snapshot**, so status in past years has to be rebuilt from dates: titled before year *t* if `FECHA_RESOL_TIT < t` (Madre de Dios layer only); extinct after `FECHA_RESOL_EXTI`. Rights that were extinguished *and later removed* from the cadastre are missing, so Medium/High before about 2015 is uncertain.
- A title is not a permit to operate. The rights holder also needs environmental certification (IGAFOM/IGA) and permission to use the land. "Low" therefore means "possibly legal", as MAAP says.
- `CALIFICA` is the regime of the right (pequeño productor / artesanal), not of whoever actually mines it. REINFO miners are usually not the titular (see §2).
- The D.L. 1100 corridor (ZPMMA) is a separate zoning layer. MAAP #208: 74 % of 2021–24 mining deforestation was inside the corridor.

## 2. Peru B: REINFO (works, two versions)

Both are published in GEOCATMIN.

| Folder | Layer | Filter | Features | Snapshot |
|---|---|---|---|---|
| `data_raw/reinfo/serv_reinfo_mdd/` (19 chunks, 7.2 MB) | `SERV_REINFO/MapServer/0` "Reinfo – MINEM" (points) | `DEPARTAMENTO='MADRE DE DIOS'` | **9,125** (national 87,334) | `FECHA_ACTUALIZACION` = 2025-02-26 |
| `data_raw/reinfo/temp_reinfo_abril26_mdd/` (2.6 MB) | `temp_reinfo/MapServer/0` "reinfo_abril_26" (points) | `DEPARTAMEN='MADRE DE DIOS'` | **3,838** (national 40,640) | layer name says April 2026; no date field |

**Fields.** SERV_REINFO: `COD_REINFO`, `ESTADO` (VIGENTE 2,258 / SUSPENDIDO 6,867), `ORIGEN` (SUNAT 2020: 7,323, SUNAT 2017: 689, RS: 1,113), `TIPO_ACT` (EXPLOTACION 6,271 / BENEFICIO 2,854), `ID_UNIDAD` (derecho minero code, which joins to cadastre `CODIGOU`; 3,568 distinct codes), `NOMBRE_DM`, district, UTM and lat/lon. temp_reinfo adds `ESTADO_INS` (VIGENTE 2,914 / SUSPENDIDO 924), `SITUACION_` of the right (EXTINGUIDO 2,350 / VIGENTE 739 / blank 749) and `ES_TITULAR` (NO 3,452 / SI 386).

**Personal data.** Both layers name natural persons and give RUC numbers. They are public registers, but we should **not reproduce names** in the brief or the figures. Aggregate by status only.

**Cross-checks (ours).**
- 6,059 of 9,125 SERV_REINFO points have an `ID_UNIDAD` that exists in today's cadastre. Of those, 4,214 are in BLOQUEADO rights, 1,795 in TITULADO and 35 in TRAMITE.
- Points by AMW class: Low 2,603 · Medium 6,076 · High 178 · **Very High 268** (REINFO registrations inside strict protected areas).

**Mapping.** REINFO is the formalization overlay *within* MAAP's Medium/Low. A REINFO-VIGENTE miner on a titled right is the closest to "legal" that the data can show. A suspended REINFO entry, or one on an extinguished right, belongs in Medium. REINFO does not legalize mining in an ANP.

**Limits.** These are points (one coordinate per registration), not polygons. Two snapshots with different filters and counts (9,125 vs 3,838), and nothing explains the difference. There is no history of status changes. The REINFO deadline has been extended repeatedly (see SPDA, Calle 2025, cited in MAAP #241; not opened).

## 3. Peru C: MAAP #235 method (done)

`data_raw/maap/maap_235.txt` holds verified excerpts from https://www.maapprogram.org/amazon-gold-mining-2025/ (published 13 Nov 2025; scraped with Firecrawl because the site returns 403 to scripts). It contains:
- The four definitions, verbatim. "Very High: Activity is occurring without a permit and within a protected area that doesn't allow for any kind of resource exploitation. High: … outside of any explicit concession. Medium: … within a concession, but active status could not be verified and/or concession doesn't meet legal requirements. Low: … within active concession, but compliance with all requirements could not be verified."
- The scope: 5 countries (BO, BR, CO, EC, PE), "based on national datasets of land designations". The page does not name the concession datasets.
- Protected areas and indigenous territories come from RAISG (accessed Dec 2024). The model works on 480 m patches from Sentinel-2.

**The layer itself** is in the AMW repo `earthrise-media/mining-detector`:
- `data_raw/amw_github/illegality_v2_areas_simplified.geojson`, taken from the parent commit `3783c9e5fe7fb176a2e0375a7fca50dfae213d4c` of `3f2d205` ("Stop tracking standardized boundaries", 28 Aug 2026). Raw URL `https://raw.githubusercontent.com/earthrise-media/mining-detector/3783c9e5fe7fb176a2e0375a7fca50dfae213d4c/data/boundaries/illegality/out/illegality_v2_areas_simplified.geojson`.
- `standardize_illegality_areas.py`, the build script. The source is `Legality_v1.shp`, with categories Low/Medium/High/Very_High mapped to 1–4, plus a Bolivia v2 layer.
- `illegality_analysis_by_jurisdiction.csv` (date_published 2026-10-05, admin_year 202503), with hectares by class for every jurisdiction.
- `mined_areas_by_jurisdiction.csv`.

All four were taken from `main` at commit `5c910e9…` except the geojson.

**AMW check numbers (publisher's own, cumulative mined area in ha):**

| Unit | Total | Very High | High | Medium | Low |
|---|---|---|---|---|---|
| Madre de Dios | 159,587 | 1,253 | 35,901 | 48,359 | 74,062 |
| Tambopata NR | 1,443 | 0 | 1,266 | 0 | 177 |
| Tambopata buffer zone | 25,211 | 349 | 21,820 | 1,447 | 1,594 |
| Amarakaeri buffer zone | 16,707 | 43 | 4,826 | 3,574 | 8,262 |
| Yanomami TI | 7,535 | 0 | 7,535 | 0 | 0 |
| Munduruku TI | 9,304 | 0 | 9,293 | 12 | 0 |
| Kayapó TI | 20,966 | 0 | 20,953 | 10 | 3 |
| Roraima | 8,019 | 0 | 7,955 | 37 | 27 |
| Pará | 294,582 | 6,568 | 189,808 | 66,794 | 31,406 |

Two surprises. (1) **Tambopata National Reserve is "High", not "Very High"**: a Reserva Nacional is a direct-use ANP, so only strict-use areas get Very High. (2) **Indigenous territories in Brazil are "High"**, not Very High. If FZS cares about the reserve itself, use our own "inside ANP" flag rather than AMW's Very High. AMW also finds 177 ha of "Low" (titled rights) inside Tambopata NR, which points to rights that predate the reserve.

## 4. Peru F: MINEM production by producer (works, more granular than BCRP)

Source: https://www.gob.pe/institucion/minem/informes-publicaciones/5472883-produccion-minera ("Estadísticas Mineras", from ESTAMIN monthly declarations + DAC). Files are in `data_raw/minem_produccion/`:
- `5472883-2001-2020.7z` (7.6 MB; inner zips per year)
- `-2021.zip`, `-2022.7z`, `-2023.7z`, `-2024.7z`, `-2025.zip`, `-ene-jul-2026.zip`

URLs are `https://cdn.www.gob.pe/uploads/document/file/{6209848,6209623,6209624,7768910,7768911,7850353,9679417}/…`. To extract the .7z files use `bsdtar`, or Python `zipfile` for the zips; inner filenames are cp437/cp850 encoded.

**Fields (from 2020):** mineral, unit (g fine), stage, process, **stratum (ESTRATO / CLASIFICACIÓN: Régimen General / Pequeño Productor Minero / Productor Minero Artesanal)**, **holder (TITULAR)**, **unit (UNIDAD MINERA)**, department, province, district, and 12 monthly columns. So we get gold by producer, by district and by month.

**Madre de Dios gold, declared by units (our sums, g fine → kg):**

| Year | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 (Jan–Jul) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| kg | 556 | 486 | 635 | 944 | 1,101 | 2,152 | 1,622 | 1,472 | 1,488 | 1,220 | 1,362 | 787 |
| Holders | 136 | 125 | 132 | 153 | 166 | 178 | 176 | 182 | 174 | 156 | 179 | 183 |

Up to 2019 the files also carry estimated artisanal output for Madre de Dios ("PRODUCTORES ARTESANALES 1/ Cifras Estimadas"): about 15.7 t in 2016 and about 6.0 t in 2019. **BCRP check: 2016 BCRP 16,223 kg = estimate + declared.** From 2020 BCRP (1,460 / 1,396 / 1,279 / 1,301 / 1,090 / 1,234 kg for 2020–25) is close to, but **not equal to**, our declared sums. It is about 10 % lower, and 2020 is 1,460 vs 2,152. The likely causes are revisions or a different vintage; this is not resolved. In 2018 the stratum also switches: Régimen General 556 kg in 2015 vs Pequeño Productor 689 kg in 2018.

**Use:** this is the formal-production proxy for the Low/Medium level (it can be linked by holder name to cadastre `TIT_CONCES`). **Limits:** self-declared, so informal gold is absent by definition. The series breaks in 2018 (strata) and 2020 (estimate dropped). There is no right code, so the link to polygons has to go through holder names (fuzzy).

## 5. Brazil D: ANM SIGMINE (works through ArcGIS; the shapefile host is unreachable)

`https://app.anm.gov.br/dadosabertos/SIGMINE/...` resets every TLS connection from here, and Firecrawl failed too. The same data is served by ANM's public ArcGIS (`https://geo.anm.gov.br/arcgis/rest/services/SIGMINE/dados_anm/MapServer`, no token):

| Folder | Layer | Filter | Features (= server count) |
|---|---|---|---|
| `data_raw/anm_sigmine/processos_ativos_RR/` (4.2 MB) | `/0` Processos minerários ativos | `UF='RR'` | **1,769** |
| `…_PA/` (47 MB, 25 chunks) | same | `UF='PA'` | **24,147** |
| `…_AM/` (10.6 MB) | same | `UF='AM'` | **3,893** |
| `…_MT/` (47 MB) | same | `UF='MT'` | **13,601** |
| `data_raw/anm_sigmine/reservas_garimpeiras/` | `/4` Reservas garimpeiras | all | 17 (e.g. Médio Tapajós 2.83 Mha, Cumaru, Tepequém RR, Rio Madeira I/II) |

**Fields:** same as the SIGMINE shapefile. `PROCESSO` (NNNNNN/AAAA), `NUMERO`, `ANO`, `FASE` (phase), `NOME` (holder), `SUBS` (substance), `USO`, `AREA_HA`, `UF`, `ULT_EVENTO` (last event with date, e.g. "… PUBL EM 28/09/2026"), `DSProcesso`.

**Gold and PLG (permissão de lavra garimpeira):** PLG = FASE contains "GARIMPEIRA" (granted "LAVRA GARIMPEIRA", or "REQUERIMENTO DE LAVRA GARIMPEIRA" = application).

| State | Gold processes | PLG | PLG gold | Granted PLG | PLG ha |
|---|---|---|---|---|---|
| RR | 629 | 358 | 172 | 0 (all applications, 356) | 0.83 M |
| PA | 15,162 | 10,548 | 9,166 | 1,205 | 3.82 M |
| AM | 1,446 | 916 | 693 | — | 2.85 M |
| MT | 6,487 | 3,024 | 2,661 | 1,142 | 5.17 M |

**Mapping (our check in Pará; 82,374 AMW patches, centroid in process):**
- AMW Low: 6,066 of 7,037 are in *granted* titles (lavra garimpeira, concessão de lavra, licenciamento, registro de extração).
- AMW Medium: 15,536 of 19,079 are in *applications* (requerimento).
- AMW High: in no process (16,054), in an **exploration permit** (autorização de pesquisa, 24,222) or in "disponibilidade" (7,683).

So: an exploration permit counts as "no mining concession" (High), and Very High = strict protected areas. In Roraima nearly every AMW patch on the Brazilian side is outside any process (High). The Yanomami TI is 100 % High per AMW.

**Limits.**
- Active processes only. `Producao/Processos_Minerários_Inativos` exists but has only geometry and ID, with no UF or phase, so we skipped it. Rebuilding past status needs `ANO` and `ULT_EVENTO`.
- No mining is legal inside TIs (Constitution art. 231; from memory, verify), so inside a TI the level is High or worse whatever SIGMINE says.

## 6. Brazil E: CFEM royalties (partial: 2017 to March 2024, from Wayback)

The ANM host is unreachable (same TLS reset; `dadosabertos.anm.gov.br` serves a WAF challenge page, which we did not solve). The Internet Archive holds captures from 22 Mar 2024. We downloaded them `id_`-raw:

| File (`data_raw/anm_cfem/`) | Original URL | Wayback timestamp | Size (= archived content-length) | sha256 |
|---|---|---|---|---|
| `wayback_20240322061449_CFEM_Arrecadacao_2017_2021.csv` | `https://app.anm.gov.br/DadosAbertos/ARRECADACAO/CFEM_Arrecadacao_2017_2021.csv` (orig. last-modified 21 Mar 2024) | 20240322061449 | 63,525,108 B (first transfer broke at 55 MB, resumed with a range request, size now matches) | 0967a3a1744a0a54060c49706c07ccfb71aafe8b769281d4e47d615639424d66 |
| `wayback_20240322061030_CFEM_Arrecadacao_2022_2026.csv` | `…/CFEM_Arrecadacao_2022_2026.csv` | 20240322061030 | 30,380,283 B | 53c0f2a7703ab84d00ad67bde024c89655f4a0bd4f8cca50f1d9384e67919019 |
| `wayback_20240322100407_Dicionario_de_Dados_-_CFEM.pdf` | `…/Dicionário de Dados - CFEM.pdf` | 20240322100407 | 28,131 B | f2cd6b5f8a1237c4ae34bbb41be3836619d8889a421b29317637df6ed5798438 |

**Format:** `;`-separated, Latin-1, decimal comma. Columns: Ano, Mês, **Processo** + AnoDoProcesso (these join to SIGMINE `NUMERO`/`ANO`), Tipo_PF_PJ, CPF_CNPJ (masked for individuals), Substância (OURO / MINÉRIO DE OURO / OURO NATIVO), UF, **Município**, QuantidadeComercializada, UnidadeDeMedida (g/kg), ValorRecolhido (R$). Rows: 620,277 (2017–2021) + 295,783 (2022 to Mar 2024).

**Gold CFEM collected, R$ million (our sums):**

| State | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 (Jan–Mar) |
|---|---|---|---|---|---|---|---|---|
| PA | 4.15 | 14.79 | 25.17 | 70.76 | 86.63 | 74.95 | 36.19 | 2.31 |
| MT | 4.83 | 20.34 | 31.80 | 55.37 | 71.40 | 66.23 | 55.61 | 7.84 |
| AM | 0.13 | 0.24 | – | 0.37 | 0.80 | 0.88 | 0.43 | 0.02 |
| RR | 0.00 | – | – | – | – | – | – | – |

Roraima has essentially **no declared gold**, which matches "all Yanomami mining is illegal". There is **no publisher check number** yet. The ANM "Maiores arrecadadores" dashboard was not reachable.

**Limits.**
- 2015–2016 is missing (the 2012–2016 file was never archived) and nothing after March 2024 is available.
- The R$ value moves with the gold price and the royalty rate (Lei 13.540/2017 raised gold to 1.5 %; from memory, verify). Use `QuantidadeComercializada` (g) as a volume measure instead.
- CFEM on garimpo gold was booked against the PLG of origin declared by the first buyer (DTVM) under the "boa-fé" rule (STF suspended it in 2023; from memory, verify before citing). Laundered gold from TIs can therefore show up as legal CFEM in PA/MT municipalities: low CFEM does not prove there is no mining, and high CFEM does not prove the gold is legal.
- Re-download from ANM when it can be reached (probably needs a Brazilian IP).

## 7. Proposed pixel classification (Peru, per year *t*)

1. Inside a strict-use ANP (SERNANP) → **Very High**. Optionally treat Tambopata NR as Very High too, and document it (AMW says High).
2. Otherwise inside a titled right with `FECHA_RESOL_TIT < t` and no `FECHA_RESOL_EXTI < t` → **Low**. Flag REINFO-VIGENTE on the same `CODIGOU`.
3. Otherwise inside any right that is in process, extinct, blocked or not yet titled at *t* → **Medium**.
4. Otherwise → **High**. Native-community land (RAISG) can be a sub-flag; MAAP #235's Karene example is High.

Validate against AMW's `illegality_analysis_by_jurisdiction.csv`: Madre de Dios 74,062 / 48,359 / 35,901 / 1,253 ha (Low / Medium / High / Very High).

Brazil: TI or strict UC → High/Very High as in AMW; granted PLG/lavra → Low; application → Medium; none / exploration permit → High.

## 8. What did not work

- `app.anm.gov.br` (SIGMINE shapefiles, CFEM CSV): TCP reset during the TLS handshake; Firecrawl with a BR location also failed.
- `dadosabertos.anm.gov.br`: WAF challenge page (not attempted).
- `minem.gob.pe/_estadistica.php`: timeout. The data come from gob.pe instead.
- `maapprogram.org`: 403 to curl, so Firecrawl was used.
- SIGMINE inactive processes: no attributes.

## 9. Rows for DOWNLOAD_LOG.csv (not added)

Columns: file, used_for, source, url, platform_project, theme_or_table, group_by, territory, years, downloaded_by, date, check_number, notes

```
ingemmet/catastro_minero_wgs84_L0_mdd_bbox/chunk_*.geojson,legality level (Low/Medium/High),INGEMMET GEOCATMIN,https://geocatmin.ingemmet.gob.pe/arcgis/rest/services/SERV_CATASTRO_MINERO_WGS84/MapServer/0,Catastro Minero (daily),derechos mineros polygons,derecho minero,bbox -72.5 -13.5 -68.6 -9.8,snapshot 2026-10-12 (FEC_DENU 1977-2026),Claude (agent),2026-10-12,server count 4831 = downloaded 4831,10 chunks; SHA256SUMS in folder; objectIds batches (no pagination)
ingemmet/catastro_minero_dgm_L1_mdd_bbox/chunk_000.geojson,legality level,INGEMMET GEOCATMIN,https://geocatmin.ingemmet.gob.pe/arcgis/rest/services/SERV_CATASTRO_MINERO_WGS84/MapServer/1,Catastro Minero - DGM (MINEM),polygons,derecho minero,same bbox,snapshot 2026-10-12,Claude (agent),2026-10-12,count 153 = 153,
ingemmet/catastro_madre_dios_L0/chunk_*.geojson,legality level with title dates,INGEMMET GEOCATMIN,https://geocatmin.ingemmet.gob.pe/arcgis/rest/services/SERV_CATASTRO_MADRE_DIOS/MapServer/0,Catastro Minero de Madre de Dios,polygons,derecho minero,Madre de Dios,snapshot 2026-10-12,Claude (agent),2026-10-12,count 2655 = 2655,FECHA_RESOL_TIT / FECHA_RESOL_EXTI
ingemmet/catastro_madre_dios_L1_zpmma/chunk_000.geojson,corridor (duplicate),INGEMMET GEOCATMIN,https://geocatmin.ingemmet.gob.pe/arcgis/rest/services/SERV_CATASTRO_MADRE_DIOS/MapServer/1,Zona de Peq. Mineria y Mineria Artesanal,polygon,,Madre de Dios,current,Claude (agent),2026-10-12,1 feature,
reinfo/serv_reinfo_mdd/chunk_*.geojson,formalization status,MINEM via INGEMMET GEOCATMIN,https://geocatmin.ingemmet.gob.pe/arcgis/rest/services/SERV_REINFO/MapServer/0,REINFO - MINEM,points,registration,DEPARTAMENTO='MADRE DE DIOS',snapshot 2025-02-26,Claude (agent),2026-10-12,count 9125 = 9125 (VIGENTE 2258 / SUSPENDIDO 6867),contains names/RUC: do not republish
reinfo/temp_reinfo_abril26_mdd/chunk_*.geojson,formalization status,MINEM via INGEMMET GEOCATMIN,https://geocatmin.ingemmet.gob.pe/arcgis/rest/services/temp_reinfo/MapServer/0,reinfo_abril_26,points,registration,DEPARTAMEN='MADRE DE DIOS',April 2026 (layer name),Claude (agent),2026-10-12,count 3838 = 3838,contains names/RUC
maap/maap_235.txt,legality method,MAAP,https://www.maapprogram.org/amazon-gold-mining-2025/,MAAP report #235,rendered page text (excerpts),,Amazon,2025,Claude (agent),2026-10-12,,Firecrawl scrape
amw_github/illegality_v2_areas_simplified.geojson,legality layer (MAAP #235),Amazon Mining Watch (Earth Genome / ACA),https://raw.githubusercontent.com/earthrise-media/mining-detector/3783c9e5fe7fb176a2e0375a7fca50dfae213d4c/data/boundaries/illegality/out/illegality_v2_areas_simplified.geojson,mining-detector repo,illegality classes 1-4,polygon,Amazon (5 countries),v2 (2026),Claude (agent),2026-10-12,MdD L/M/H/VH 74062/48359/35901/1253 ha (jurisdiction csv),69.6 MB
amw_github/illegality_analysis_by_jurisdiction.csv,check numbers,Amazon Mining Watch,https://raw.githubusercontent.com/earthrise-media/mining-detector/main/data/public/illegality_analysis_by_jurisdiction.csv,mining-detector repo (main 5c910e9),ha by class,jurisdiction,Amazon,admin_year 202503; published 2026-10-05,Claude (agent),2026-10-12,,
amw_github/mined_areas_by_jurisdiction.csv,context,Amazon Mining Watch,https://raw.githubusercontent.com/earthrise-media/mining-detector/main/data/public/mined_areas_by_jurisdiction.csv,mining-detector repo,mined ha,jurisdiction x period,Amazon,2018-2026,Claude (agent),2026-10-12,,
amw_github/standardize_illegality_areas.py,method,Amazon Mining Watch,https://raw.githubusercontent.com/earthrise-media/mining-detector/main/scripts/boundaries/standardize_illegality_areas.py,mining-detector repo,build script,,,,Claude (agent),2026-10-12,,
minem_produccion/5472883-*.{7z,zip},declared gold by producer,MINEM (ESTAMIN/DAC),https://www.gob.pe/institucion/minem/informes-publicaciones/5472883-produccion-minera,Estadisticas Mineras - Produccion Minera,metallic production by titular/unidad/district/month,unit x month,Peru,2001-2026M07,Claude (agent),2026-10-12,MdD 2016 estimate+declared = BCRP 16223 kg,7 archives
anm_sigmine/processos_ativos_{RR,PA,AM,MT}/chunk_*.geojson,legality level Brazil,ANM SIGMINE,https://geo.anm.gov.br/arcgis/rest/services/SIGMINE/dados_anm/MapServer/0,SIGMINE dados_anm,processos minerarios ativos,processo,UF,snapshot 2026-10-12,Claude (agent),2026-10-12,counts RR 1769 PA 24147 AM 3893 MT 13601 = server,PA and MT ~47 MB each
anm_sigmine/reservas_garimpeiras/chunk_000.geojson,context,ANM SIGMINE,https://geo.anm.gov.br/arcgis/rest/services/SIGMINE/dados_anm/MapServer/4,SIGMINE dados_anm,reservas garimpeiras,polygon,Brazil,current,Claude (agent),2026-10-12,17 = 17,
anm_cfem/wayback_*_CFEM_Arrecadacao_{2017_2021,2022_2026}.csv,declared gold proxy Brazil,ANM (via Internet Archive),https://web.archive.org/web/20240322061449id_/https://app.anm.gov.br/DadosAbertos/ARRECADACAO/CFEM_Arrecadacao_2017_2021.csv (and 20240322061030 for 2022_2026),ANM Dados Abertos - Arrecadacao CFEM,CFEM by processo x municipio x substancia x month,processo-month,Brazil,2017-01 to 2024-03,Claude (agent),2026-10-12,sizes = archived content-length,ANM host unreachable from outside BR
```

Firecrawl calls used: 6 (4 searches: MAAP legality, MAAP #235 URL, CFEM mirror, MINEM production; 2 scrapes: MAAP #235 page, ANM directory with a BR location, which failed).
