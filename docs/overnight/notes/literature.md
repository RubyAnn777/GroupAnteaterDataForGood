# Literature notes (accessed 2026-10-10 unless stated; Firecrawl calls: 0)

Verification levels. **PDF** = I downloaded the PDF and extracted the text myself (quotes are exact). **Crossref** = abstract from the Crossref API (exact). **WebFetch** = page text summarised by a small model, so wording may be paraphrased: re-check against the live page before putting it in quotation marks in the brief. Only cite sources marked "opened: yes" (agent.md section 7).

## 1. MAAP #242, Yanomami (Brazil)
- Reference: MAAP (Monitoring of the Andes Amazon Program), led by Instituto Socioambiental (ISA). "MAAP #242: Illegal gold mining in Yanomami Indigenous Territory (northern Brazilian Amazon)", 22 May 2026. Individual authors not named on the page.
- Link: https://www.maapprogram.org/gold-mining-brazil-yanomami/ (also ?p=27648)
- Opened: yes, via WebFetch (not PDF). My earlier guessed URLs 404'd.

| Claim | Quote (WebFetch; verify) | Location |
|---|---|---|
| Peak 2022 | "peaked in 2022 (nearly 1,800 ha)" | main text |
| 2023 | "major decreases in 2023 (330 ha)" | main text |
| 2024, 2025 | "(83.95 ha and 45.2 ha, respectively)"; "45 hectares (across 121 polygons) of new mining deforestation" | main text |
| Cumulative | "the total area impacted by mining reached 5,564 hectares in 2025" | main text |
| Series | Graph 1: "Annual increase in the area affected by illegal mining in Yanomami Indigenous Territory" (2020 baseline 400 ha) | Graph 1 |
| Source of data | ISA monthly visual interpretation of Planet mosaics and Sentinel-2 | Notes |
| Other source | Amazon Mining Watch: 2,470 ha 2018-2025; 850 ha (2022), 250 ha (2023), 80 ha (2024); no new mining in 2025 | Note 3 |

Snippet figures (1,800 / 330 / 84 / 45) are confirmed. Note the second dataset (AMW) gives about half the ISA numbers, so the level depends on the source; the decline pattern is the same.
Use: Brazil post-operation outcome (delay/persistence), and a cross-check of our DETER/MapBiomas series; remark that ISA's method is visual interpretation, not MapBiomas.

## 2. Lopes & Chiavari (2021), CPI/PUC-Rio
- Reference: Lopes, Cristina Leme and Joana Chiavari (2021). "Analise do Novo Procedimento Administrativo Sancionador do Ibama e seus Reflexos no Combate ao Desmatamento na Amazonia" (English title on CPI site: "An Analysis of the New Legal Framework for IBAMA's Administrative Enforcement Procedures and its Effects on Combating Deforestation in the Amazon"). Climate Policy Initiative / PUC-Rio, Rio de Janeiro, June 2021 (CPI page dated 7 June 2021). Portuguese only.
- Links: https://www.climatepolicyinitiative.org/publication/an-analysis-of-the-new-legal-framework-for-ibamas-administrative-sanctioning-procedure-and-its-effects-on-combating-deforestation-in-the-amazon/ ; PDF https://www.climatepolicyinitiative.org/wp-content/uploads/2021/06/Relatorio-Analise-do-Novo-Procedimento-Administrativo-Sancionador-do-Ibama.pdf
- Opened: yes, PDF text extracted (37 pages).

| Claim | Exact quote | Location |
|---|---|---|
| Flora infractions halved | "De acordo com dados do Inpe, a taxa de desmatamento na Amazônia em 2020 é 47% maior que a taxa registrada em 2018 (Inpe 2020). Entretanto, o número de autuações por infrações contra a flora caiu pela metade (56%) em 2020 na comparação com 2018 (Ibama 2021d)." | PDF page 32 of 37 (printed page number may differ) |
| English summary (CPI web page) | "The number of infractions against the flora, however, fell by half (56%) in 2020 versus 2018." | CPI publication page (WebFetch) |

Caveat: the sentence is a ratio-of-"fell by half (56%)" inconsistency in the source itself (half is 50%); quote it as "56%". It is about flora (deforestation) fines nationally, not mining; the source for it is IBAMA 2021d.
Use: the cited source for "federal enforcement weakened 2019-22" (Brazil case, description only).

## 3. Mataveli et al. (2022), Remote Sensing 14(16):4092
- Reference: Mataveli, G.; Chaves, M.; Guerrero, J.; Escobar-Silva, E.; Conceição, K.; de Oliveira, G. (2022). "Mining Is a Growing Threat within Indigenous Lands of the Brazilian Amazon." Remote Sensing 14(16), 4092. DOI 10.3390/rs14164092. Published 21 Aug 2022, CC BY.
- Link: https://www.mdpi.com/2072-4292/14/16/4092 (MDPI returns 403 to fetchers; use DOI https://doi.org/10.3390/rs14164092)
- Opened: abstract only (exact, from Crossref API). Full text not read.

| Claim | Exact quote (abstract) | Location |
|---|---|---|
| Policy weakening | "An increase in deforestation rates of the BLA in recent years, due to the weakening of the Brazilian environmental policy, is not confined to unprotected areas but is also occurring within ILs." | Abstract |
| Mining in ILs | "Such activity jumped from 7.45 km2 in 1985 to 102.16 km2 in 2020, an alarming increase of 1271%." | Abstract |
| Concentration | "Three ILs (Kayapó, Mundurukú, and Yanomami) concentrated 95% of the mining activity within ILs in 2020" | Abstract |
| Gold | "Most of the mining in ILs in 2020 (99.5%) was related to gold extraction." | Abstract |
| Data | "using the freely available MapBiomas dataset, we have quantified for the first time the total mining area within ILs of the BLA from 1985 to 2020" | Abstract |

Use: justifies picking Yanomami, Munduruku, Kayapo and MapBiomas as the measure; same data family as ours. Caution: it attributes the deforestation rise to weakened policy as an assertion of the abstract, not a tested result; label as description.

## 4a. Saavedra (2022), Colombia
- Reference: Saavedra, Santiago (2022). "Technology and State Capacity: Experimental Evidence from Illegal Mining in Colombia." Working paper, 30 June 2022 (University of Colorado Denver / Universidad del Rosario; AEA RCT Registry AEARCTR-0002397). Not peer-reviewed, no journal version found. (Agent.md calls it "Saavedra 2025"; the version I opened is dated June 2022, check the course reading for the newer version.)
- Link: https://poverty-action.org/sites/default/files/publications/Paper_inforevel.pdf (the old fr.poverty-action.org URL 301-redirects here)
- Opened: yes, PDF text extracted (47 pages).

| Claim | Exact quote | Location |
|---|---|---|
| Direct effect | "in treated municipalities, illegal mining is reduced by 11% in the disclosed locations and surrounding areas." | Abstract, p.1 |
| Spillover/displacement | "However, when accounting for negative spillovers — increases in illegal mining in areas not targeted by the information — the net reduction is only 7%." | Abstract, p.1 |
| Mechanism | "there might be negative spillovers if illegal activity relocates from disclosed locations to ..." (sentence continues) | Introduction, p.2-3 |
| Pattern | "There is also a reduction of similar magnitude in surrounding areas of disclosed locations (areas less than 1km away). However, there is an increase in illegal mining in other areas of the municipality away from disclosed mines." | Introduction, p.4 |
| Sign of bias | "Without the negative spillovers, the reduction in illegal mining due to the treatment would have been 11%, but due to the spillovers, the net reduction is only 7%." | Introduction p.4; Section on spillovers (around Figure 3) |
| Environmental outcome | "I do not find statistically significant effects on homicides or deforestation." | Introduction p.4 |

Use: the only experimental evidence that targeted enforcement against illegal mining displaces activity nearby; supports "spillovers bias DiD" paragraph. It is an information/monitoring treatment, not an operation like Mercurio.

## 4b. Caballero Espejo et al. (2018)
- Reference: Caballero Espejo, J.; Messinger, M.; Román-Dañobeytia, F.; Ascorra, C.; Fernandez, L.E.; Silman, M. (2018). "Deforestation and Forest Degradation Due to Gold Mining in the Peruvian Amazon: A 34-Year Perspective." Remote Sensing 10(12), 1903 (DOI 10.3390/rs10121903; Crossref issued date 29 Nov 2018; check volume/issue/article number on the publisher page before citing).
- Link: https://doi.org/10.3390/rs10121903
- Opened: abstract only (Crossref, exact).

| Claim | Exact quote | Location |
|---|---|---|
| Scale | "We identify nearly 100,000 ha of deforestation due to ASGM in the 34-year study period, an increase of 21% compared to previous estimates." | Abstract |
| Timing | "10% of that deforestation occurred in 2017, the highest annual amount of deforestation in the study period, with 53% occurring since 2011." | Abstract |
| Drivers | "We discuss their connections with, and impacts on, socio-economic factors, such as land tenure, infrastructure, international markets, governance efforts, and social and environmental impacts." | Abstract |
| Land-only method | Method "relies on a fusion of CLASlite and the Global Forest Change dataset, two Landsat-based deforestation detection tools" | Abstract |

Use: pre-2019 baseline (2017 highest year on record) and a measurement caveat (forest-loss based, land only). No usable enforcement-displacement sentence found in the abstract.

## 4c. Dethier et al. (2023), Nature
- Reference: Dethier, E.N.; Silman, M.; Leiva, J.D.; Alqahtani, S.; Fernandez, L.E.; Pauca, P.; et al. (2023). "A global rise in alluvial mining increases sediment load in tropical rivers." Nature 620, 787-793. DOI 10.1038/s41586-023-06309-9. Published 23 Aug 2023.
- Link: https://doi.org/10.1038/s41586-023-06309-9 (nature.com redirects to a login handshake for fetchers)
- Opened: no (Nature page not reachable). Only via search-result excerpts and the Mongabay article (Hanbury, 5 Sep 2023, https://news.mongabay.com/2023/09/muddied-tropical-rivers-reveal-magnitude-of-global-gold-mining-boom-study/, opened via WebFetch).

| Claim | Quote | Location |
|---|---|---|
| Satellite basis | "based on 7 million measurements taken from satellite images spanning four decades." (Mongabay's words) | Mongabay article |
| Policy responsiveness | Caption: "The gap in the mid- to late 2000s in Brazil shows how responsive rivers can be to environmental policy." | Mongabay, time-series caption |
| Rivers visible from space | Mining debris "making their heavy sediment flows clearly visible from space." | Mongabay |
| Search excerpt of abstract (not verified) | "80% have suspended sediment concentrations (SSCs) more than double pre-mining levels"; "35,000 river kilometres, 6% (±1% s.e.)" | search snippet only |

Use: supports the "what satellites cannot see" paragraph: land-cover maps miss dredging, but river sediment is a separate detectable signal. Do not cite Nature numbers until the abstract is opened. No displacement statement in the Mongabay piece.

## 4d. Hutukara / ISA "Yanomami sob ataque" (2022)
- Reference: Hutukara Associação Yanomami and Associação Wanasseduume Ye'kwana, with technical support from ISA (2022). "Yanomami Sob Ataque: Garimpo ilegal na Terra Indígena Yanomami e propostas para combatê-lo." 11 April 2022.
- Link to the report PDF: not found (the Unicamp copy URL returned HTML 404; acervo.socioambiental.org link was a different report). Press page opened: https://site-antigo.socioambiental.org/en/print/7572 (ISA, 11 Apr 2022, WebFetch).
- Opened: the ISA news page, yes (via WebFetch); the report itself, no.

| Claim | Quote (WebFetch; verify) | Location |
|---|---|---|
| Area Dec 2021 | "atingindo em dezembro de 2021 o total de 3.272 hectares" | ISA news page |
| 2021 growth | "Segundo dados extraídos do relatório, em 2021 o garimpo ilegal avançou 46% em comparação com 2020." | ISA news page |
| Long growth | "De 2016 a 2020, o garimpo na TIY cresceu nada menos que 3.350%" | ISA news page |

Search-snippet only (not opened): HAY later reported +54% in 2022 with 1,782 new ha (cumulative 3,817 ha since Oct 2018; 1,236 ha at the start). MAAP #242 says "nearly 1,800 ha" for 2022: consistent.
Use: pre-operation baseline for Yanomami; cite ISA page, not the unseen report.

## 4e. Government outcomes of the 2023 Yanomami operation (search results only, NOT opened)
Poder360 and others returned 403 to fetchers; these are snippets from a search engine summary, do not cite until opened:
- "Casa de Governo" reported alerts in the Yanomami TI fell 73% in Jan-Apr 2024 vs same period 2023 (102 alerts); baselines conflict across outlets (SBT/Censipam 378 alerts vs Poder360 192).
- ISA/Hutukara: illegal garimpo area in the TI "grew 7%, reaching 5,432 ha" in 2023, versus a Defence Ministry claim of a 78.51% reduction through 12 Sep 2023. This conflicts in direction with MAAP #242 (new impact falls to 330 ha in 2023), but the two measure different things: cumulative area vs annual new area; check before use.
Use: shows government claims are not a clean outcome measure; prefer MAAP #242/ISA series plus DETER.

## 5. Conley & Taber (2011)
- Reference: Conley, Timothy G. and Christopher R. Taber (2011). "Inference with 'Difference in Differences' with a Small Number of Policy Changes." The Review of Economics and Statistics 93(1): 113-125. DOI 10.1162/REST_a_00049 (Crossref lists it lower-case: 10.1162/rest_a_00049). NBER Technical Working Paper 0312, DOI 10.3386/t0312.
- Link: https://doi.org/10.1162/REST_a_00049 ; author PDF https://users.ssc.wisc.edu/~ctaber/Papers/ctabdd.pdf
- Opened: yes, author PDF (13 pages, the published-style version with REStat abstract), text extracted.

| Claim | Exact quote | Location |
|---|---|---|
| Problem | "In difference-in-differences applications, identification of the key parameter often arises from changes in policy by a small number of groups. In contrast, typical inference assumes that the number of groups changing policy is large." | Abstract, p.1 |
| Method | "We present an alternative inference approach for a small (finite) number of policy changers, using information from a large sample of nonchanging groups." | Abstract, p.1 |
| Consistency | "Treatment effect point estimators are not consistent, but we can consistently estimate their asymptotic distribution under any point null hypothesis about the treatment." | Abstract, p.1 |

Use: cite for "with one treated unit, conventional standard errors are not informative", and note that their method needs a large pool of untreated groups (we have few in Peru), so we show the placebo and the figure instead.
