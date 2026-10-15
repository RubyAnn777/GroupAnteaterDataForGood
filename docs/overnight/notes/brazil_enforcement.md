# Brazil federal enforcement 2019-22: sources and IBAMA data (overnight run, 2026-10-10)

Status: OK for the IBAMA fines file and for sources; BLOCKED for the IBAMA embargo file (URL not found, see Problems).

## 1. Peer-reviewed / report sources (all opened 2026-10-10)

### A. Nunes et al. 2024 (Scientific Reports), main citable source
- Reference: Nunes, F.S.M., Soares-Filho, B.S., Oliveira, A.R., Veloso, L.V.S., Schmitt, J., Van der Hoff, R., Assis, D.C., Costa, R.P., Boerner, J., Ribeiro, S.M.C., Rajao, R.G.L., de Oliveira, U., Costa, M.A. (2024). Lessons from the historical dynamics of environmental law enforcement in the Brazilian Amazon. Scientific Reports 14, published 21 Jan 2024. DOI 10.1038/s41598-024-52180-7. https://www.nature.com/articles/s41598-024-52180-7 (accessed 2026-10-10, full text read via Firecrawl).
- Abstract: "The number of embargoes and asset confiscations dropped by 59% and 55% in 2019 and 2020, respectively." Same abstract: conciliation hearings and centralised legal processes in 2019 "reduced the number of actual judgments and fines collected by 85%" and cut the ratio of lawsuits ending in paid fines to filed ones "from 17 to 5%".
- Results section "Changes in enforcement intensity", Fig. 1: "IBAMA issued 4.6 thousand annual notices of infraction against the flora between 2012 and 2018 in the Amazon. In 2019-2020, only 2.6 thousand notices were issued yearly, a drop of 44%, despite a substantial rise in deforestation rates."
- Caveats: scope is Amazon deforestation/flora enforcement, not mining. Mentions the 2023 recovery: IBAMA's "infraction notices and sanctions in the Legal Amazon more than doubled compared to the average for the same period over the past four years" (Supplementary Fig. S5) and operations to remove miners from the Yanomami territory.

### B. Lopes & Chiavari 2021 (Climate Policy Initiative)
- Reference: Lopes, C.L. and Chiavari, J. (7 June 2021). An Analysis of the New Legal Framework for IBAMA's Administrative Enforcement Procedures and its Effects on Combating Deforestation in the Amazon. Climate Policy Initiative. https://www.climatepolicyinitiative.org/publication/an-analysis-of-the-new-legal-framework-for-ibamas-administrative-sanctioning-procedure-and-its-effects-on-combating-deforestation-in-the-amazon/ ; PDF https://www.climatepolicyinitiative.org/wp-content/uploads/2021/06/Relatorio-Analise-do-Novo-Procedimento-Administrativo-Sancionador-do-Ibama.pdf (accessed 2026-10-10; the web page was read through WebFetch, whose summary I am quoting; the PDF itself was NOT opened, so check page/figure there before citing).
- Statement: "The number of infractions against the flora, however, fell by half (56%) in 2020 versus 2018." and deforestation in 2020 was "47% higher than in 2018". (Note: "fell by half (56%)" is as returned; verify wording in the PDF.)
- Caveat: flora/deforestation, not mining.

### C. Mataveli et al. 2022 (Remote Sensing), mining on indigenous lands (context, not an enforcement count)
- Reference: Mataveli, G., Chaves, M., Guerrero, J., Escobar-Silva, E.V., Conceicao, K., de Oliveira, G. (2022). Mining Is a Growing Threat within Indigenous Lands of the Brazilian Amazon. Remote Sensing 14(16), 4092. DOI 10.3390/rs14164092. https://www.mdpi.com/2072-4292/14/16/4092 (accessed 2026-10-10, abstract read via Firecrawl).
- Abstract: "An increase in deforestation rates of the BLA in recent years, due to the weakening of the Brazilian environmental policy, is not confined to unprotected areas but is also occurring within ILs." Mining area in ILs "jumped from 7.45 km2 in 1985 to 102.16 km2 in 2020"; Kayapo, Munduruku and Yanomami hold 95% in 2020 (supports our choice of treated/comparison territories). It asserts the weakening but does not measure it; use A for the number.

### D. Not fully opened (do not cite yet)
- MAAP #242 (22 May 2026), Yanomami: search excerpt only (annual new mining impact peaked ~1,800 ha in 2022, then 330 ha 2023, 84 ha 2024, 45 ha 2025). Open the page before citing.

## 2. IBAMA open data
- Dataset page: https://dadosabertos.ibama.gov.br/dataset/fiscalizacao-auto-de-infracao ("Fiscalizacao - auto de infracao", metadata last updated 27 May 2026, daily refresh, temporal coverage from 1980).
- File: https://stibamadadosabertosprd.blob.core.windows.net/dados-abertos/dados/SIFISC/auto_infracao/auto_infracao/auto_infracao_csv.zip
- Saved: data_raw/ibama/auto_infracao_csv.zip, 122,900,569 bytes (117 MB), sha256 5e65aba9b3b1ba08c3098b59da7031dadb78d876fc4f4d560ddc984eb1f381e0, server Last-Modified 2026-10-09. Over 50 MB, so link it in the log instead of zipping it. Inside: one CSV per year 1977-2026 (; separated, 84 columns).
- Script: /private/tmp/claude-501/scr/build.py (copy into code/ if wanted); run with `uv run python -I build.py <unzipped dir> <outdir>`.
- Columns used: SIT_CANCELADO, DAT_HORA_AUTO_INFRACAO, UF, DES_INFRACAO, DES_AUTO_INFRACAO, DES_LOCAL_INFRACAO, OPERACAO, DS_BIOMAS_ATINGIDOS.
- Filters: keep SIT_CANCELADO == "N" (not cancelled) and year of DAT_HORA_AUTO_INFRACAO == file year. Counts are of autos (rows), all types (fines, warnings).
- Legal Amazon states: AC AP AM MA MT PA RO RR TO (by UF of the auto). n_amazon_biome: DS_BIOMAS_ATINGIDOS contains "Amazonia".
- Mining flag (accent-stripped, lower-case, on DES_INFRACAO + DES_AUTO_INFRACAO): regex `garimp|lavra|minerio|mineracao|extracao mineral|extrair.*(ouro|minerio|mineral)|\bouro\b|cassiterita|dragagem|recursos minerais|bens minerais|permissao de lavra|ccaa|mercurio`. Broad and not validated by hand: it will include some non-mining autos (e.g. "dragagem", "ouro", "ccaa") and miss autos with only generic text.
- Indigenous flag (on the above text plus DES_LOCAL_INFRACAO and OPERACAO): `terra indigena|terras indigenas|\bti\b|indigena|yanomami|munduruku|kayapo|raposa serra`. Free-text only; there is no structured indigenous-land field, so this undercounts and may also catch fines against indigenous persons.

### Annual table (docs/overnight/notes/ibama_annual.csv has all columns; state totals in ibama_by_state_year.csv)
| year | Brazil | Legal Amazon states | Amazon biome | mining Brazil | mining Legal Amazon | mining RR | mining PA | mining AM | mining+indigenous text, Legal Amazon |
|---|---|---|---|---|---|---|---|---|---|
| 2014 | 14775 | 6115 | 5467 | 461 | 119 | 16 | 61 | 16 | 21 |
| 2015 | 16558 | 7227 | 6741 | 306 | 101 | 6 | 35 | 15 | 5 |
| 2016 | 17084 | 7290 | 6884 | 352 | 128 | 9 | 46 | 16 | 8 |
| 2017 | 15358 | 7485 | 7324 | 300 | 186 | 4 | 42 | 80 | 13 |
| 2018 | 14577 | 5676 | 5351 | 359 | 213 | 1 | 90 | 31 | 19 |
| 2019 | 12480 | 5445 | 5010 | 231 | 120 | 1 | 57 | 9 | 2 |
| 2020 | 9062 | 3343 | 3191 | 223 | 106 | 1 | 47 | 7 | 12 |
| 2021 | 9163 | 3971 | 3728 | 313 | 182 | 20 | 80 | 13 | 38 |
| 2022 | 12339 | 4676 | 3062 | 369 | 182 | 19 | 35 | 65 | 23 |
| 2023 | 16386 | 7907 | 7379 | 464 | 354 | 61 | 105 | 51 | 46 |
| 2024 | 11668 | 5456 | 5246 | 537 | 415 | 47 | 218 | 21 | 65 |
| 2025 | 15564 | 6615 | 6118 | 400 | 278 | 35 | 40 | 24 | 96 |

Description (not causal): mean autos per year 2015-18 vs 2019-22: Brazil 15,894 -> 10,761 (-32%); Legal Amazon states 6,920 -> 4,359 (-37%); Legal Amazon, 2020 low of 3,343 is -41% vs 2018 and 2023 (7,907) is above every year since 2017. Mining-flagged autos in the Legal Amazon did NOT fall (2015-18 mean 157; 2019-22 mean 148; 2021-22 = 182) and then rose in 2023-24 (354, 415). So the data support "general fines fell 2019-20" but NOT "mining-specific fines fell"; do not say the latter without a better classifier (use the structured legal-basis table, enquadramento, e.g. Decreto 6.514 art. 55 and 63-ish provisions, which I did not check). Indigenous+mining text counts are tiny (2-96) and noisy.
Cross-check with source A (different definition): A reports flora notices in the Amazon falling from 4.6k/yr (2012-18) to 2.6k/yr (2019-20). Our all-types Legal Amazon count 2019-20 averages 4,394 vs 2012-18 not computed here; not comparable.

## 3. Check number
- Not found on IBAMA's own site: the dataset page shows no totals. Provisional check = file integrity: zip size 122,900,569 bytes (matches server Content-Length), and per-year file auto_infracao_2021.csv present. A check against IBAMA's "Autos de Infracao" query panel (gov.br/ibama, tutorial linked from the dataset page) was not possible overnight. Suggestion: someone open the panel in a browser and compare the 2021 count (ours: 9,163 non-cancelled autos dated 2021; raw rows for 2021 file were not counted separately).

## 4. Problems
- dadosabertos.ibama.gov.br returns HTTP 403 (Cloudflare bot page) to curl; I did not try to evade it. The dataset page was read with Firecrawl (which is permitted), which exposed the real file host (Azure blob), and that host downloaded fine with curl.
- Embargo file ("Termos de embargo"): the guessed URLs on the Azure host returned 404; I did not find the dataset page (Firecrawl budget kept for papers). Next step: scrape https://dadosabertos.ibama.gov.br/dataset/fiscalizacao-termo-de-embargo (slug is a guess) or search the CKAN site.
- Chrome extension needs a browser choice via a question to the user, which I could not ask; not used.
- nature.com and doaj.org returned 403/redirect to WebFetch; the Nature text came through Firecrawl.
- Firecrawl calls used: 5 (scrape IBAMA page, search, scrape Nature, search, scrape MDPI).
