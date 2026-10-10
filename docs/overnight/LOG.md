# Overnight log, 2026-10-10 → 2026-10-11

Branch: `analysis/overnight-2026-10-10`. Orchestrator: Claude Opus (subagents: sonnet/haiku). Deadline: 07:00 Berlin, 2026-10-11.
Start: 2026-10-10 23:40 CEST.

**Firecrawl calls used: 14 / 100** (ANP 1, MAAP 5, IBAMA 5, Brazil TI 2, scout 1; all other agents 0)

## Status by phase
| Phase | Status |
|---|---|
| 1 Data | DONE (IBAMA embargoes BLOCKED; MAAP raw HTML manual) |
| 2 Code | done (main.py + modules; all checks OK) |
| 3 Peru descriptive | done (incl. ANP inside reserves, event study, placebo-in-space) |
| 4 Brazil descriptive | done (TI Col 10.1, Roraima, IBAMA, DETER monthly) |
| 5 Robustness | done (Peru + Brazil robustness CSVs) |
| 6 Spatial feasibility | DONE (prototype + maps; recommendation: part 4 / robustness only) |
| 7 Report | DONE (REPORT.html published as private artifact, REPORT.md, agent.md, README) |

## Decisions
| # | Decision | Alternatives | Why |
|---|---|---|---|
| D1 | Subagents never edit DOWNLOAD_LOG.csv or commit; they write draft rows to `docs/overnight/notes/*_rows.csv`, the orchestrator merges and commits. | Each agent edits the log | Avoid merge conflicts between parallel agents |
| D3 | User (23:50) allows any additional public data source that adds value, esp. for figures; same provenance rules (log row, check number, cite publisher). Launched a data-scout agent. | Pack + listed sources only | User instruction |
| D4 | Peru buffer-zone units = sum over ALL department rows (Amarakaeri has a Cusco row, Tambopata a Puno row). Reproduces the card (1,640→163, 289→574, DiD −1,762); agent.md §10's 1,638/284 were MdD rows only. | MdD rows only | The card's check numbers are the reference |
| D5 | Event-study pool A = Tambopata + Amarakaeri + Bahuaja-Sonene BZ (MdD zones with non-zero 2014–18 additions); pool B = all 15 Peruvian BZ with pre-2019 additions (robustness/placebo donors). Inference by placebo-in-space rank, not clustered SEs (one treated unit). | Clustered SEs | Conley–Taber: with one treated cluster SEs are uninformative |
| D6 | Event markers: event in year Y drawn at x = Y − 0.5 (before the first annual addition that can reflect it). | Calendar position | addition(Y) = map(Y) − map(Y−1) |
| D7 | IBAMA zip (123 MB) git-ignored; code/brazil_ibama.py rebuilds a small committed intermediate `data_intermediate/ibama_autos_annual.csv` when the zip is present, else reads it. | Commit zip / skip | Keeps replication possible without a >50 MB file in git |
| D8 | Brazil per-territory = MapBiomas Col 10.1 class 4.3 (all mining; no garimpo/substance split per territory exists). Pack all-TIs series (Col 11, artisanal) kept as a separate panel, never in one series. | Mix collections | Rule 7 |
| D9 | Brazil best control 2023–24 = Kayapó (only light action, formal desintrusão May 2025, after data end); Munduruku partly treated (operation Aug 2023, desintrusão Nov 2024). | Pool both | Enforcement timeline evidence |
| D10 | Extra datasets added: INPE DETER mining alerts (monthly, per TI via FUNAI polygons) and BCRP/MINEM declared gold production Madre de Dios. GFW skipped (API key). | More sources | Monthly resolution around Feb 2023; formal vs mapped mining contrast |
| D11 | Brazil 2×2 DiD reported in ha/yr AND relative to 2022 stock; sign flips → reported as inconclusive. | One metric | Units differ ~4× in size; honest reporting |
| D12 | Placebo-in-space reported on a restricted pool (Amazon-department buffer zones with > 10 ha/yr pre-2019 additions, n = 6) as well as the full pool (n = 15); read as "no comparable zone fell", not a p-value. | Full pool only | Most of the 15 zones barely mine, so rank 1 was near-mechanical (review item 3) |
| D13 | Synthetic control tried (core + extended donor pools; levels, scaled, cumulative) and NOT used for claims. | Use the scaled version | Tambopata lies outside the donor range in 9/9 pre-years; scaled version ranks 1/6 only |
| D14 | Brazil publisher check for the brief = pack Col 11 all-TIs artisanal 2025 = 39,915 ha (card). Col 10.1 per-territory file logged as MISMATCH-documented (platform Col 11 17,632 vs 18,176 ha). | Claim OK | No Col 11 per-territory file published (Dataverse + statistics page checked 2026-10-11) |
| D15 | Pooled controls = per-unit mean; old SUM ids kept but marked "do not cite". | Delete them | Stable ids; scale mismatch flagged (review item 9) |
| D16 | Report states source disagreements explicitly (MapBiomas regional surge vs AMW corridor decline; DETER Yanomami 2023 rise vs annual maps fall) instead of picking one. | Cite the agreeing source only | Honesty criterion (30% of grade); review item 7 |
| D17 | Tambopata "return" reported with and without 2023; "came back when enforcement ended" dropped (2023 spike is inside the state of emergency). | Keep the simple story | Review item 6 |
| D18 | Brief figure title made neutral/descriptive. | "fell where Mercurio hit…" | Reads as causal (review item 13) |
| D2 | Pack-based Peru analysis (phase 2/3) starts in parallel with the downloads; new datasets plug in later as separate modules. | Wait for downloads | The core Peru design only needs `data/` |

## Round log
### Round 1 (23:40)
- Created branch from main (15f6049). Read agent.md, basics.html §6–7.
- Launched batch 1 (parallel): Peru ANP download, Brazil TI download, Brazil enforcement source, MAAP citations, enforcement records, spatial data feasibility, code/main.py (Peru core).

### Round 1 results (23:50)
- DONE Peru ANP Col 4 (`data_raw/mapbiomas_peru/…AREAS-PROTEGIDAS.xlsx`, curl). Publisher-side check PENDING (platform is JS; try Chrome).
- DONE Brazil TI Col 10.1 (Dataverse doi:10.58053/MapBiomas/1F2TLA). Publisher check PENDING (MapBiomas factsheets quote Col 7/8 garimpo only; try platform via Chrome).
- DONE IBAMA autos de infração (zip via Azure blob behind dadosabertos; dadosabertos itself 403). Embargo file BLOCKED (no URL found). Sources: Nunes et al. 2024 Sci Rep (opened).
- DONE MAAP citations notes; raw HTML PENDING (maapprogram.org 403 to curl) → Chrome save.
- DONE enforcement timeline (controls partly treated: Amarakaeri yes, Munduruku yes from Aug 2023, Kayapó light).
- DONE code/main.py Peru core; all checks OK.
- Batch 2 launched: Peru ANP+robustness+figure fixes; Brazil module (TI, Roraima, IBAMA, robustness). Still running: spatial feasibility, extra-data scout.
- NEXT: Chrome agent for publisher-side checks + MAAP HTML; merge DOWNLOAD_LOG rows; phase 6 review; report.

### Round 1, continued (23:58)
- DONE Peru ANP+robustness (code/peru_anp.py, peru_robust.py), Brazil (brazil.py, brazil_ibama.py), DETER (brazil_deter.py), production (peru_production.py). All committed.
- Running: spatial module/maps; Chrome publisher checks + MAAP HTML; literature verification.
- NEXT: merge DOWNLOAD_LOG rows; brief main figure; report builder (numbers pulled from output/numbers.csv); clean-run verification.

### Round 1, continued (00:04)
- DONE: publisher checks (Peru ANP platform 777 ha = file 776.9 ha OK; Brazil TI: platform only Col 11 → collection mismatch, no Col 11 per-TI file exists); MAAP pages saved as rendered text (raw HTML blocked); literature verified (notes/literature.md); DOWNLOAD_LOG merged (30 rows, sha256); agent.md §14 + README updated; brief figure `output/fig_brief_main.png`; report builder + REPORT.html/REPORT.md (draft).
- Firecrawl total still 14 / 100 (Chrome-check, literature, Col 11 search: 0 each).
- Running: adversarial review (read-only), synthetic control + AMW zones, visual QA of REPORT.html.
- NEXT: apply review fixes; add synth + zones to report; clean run from scratch; publish artifact; final log.

### FINAL (00:20, 2026-10-11) — loop stopped

**Done**
- Phase 1: new data downloaded, logged (DOWNLOAD_LOG.csv, 30 rows, sha256 + check numbers): MapBiomas Peru protected areas Col 4; MapBiomas Brazil indigenous territories Col 10.1 (+ Col 10); IBAMA autos de infração; INPE DETER mining alerts; BCRP/MINEM Madre de Dios gold production; Amazon Mining Watch; SERNANP, FUNAI, INGEMMET boundaries; MAAP #130/#193/#208/#241 text captures; literature notes.
- Phases 2–6: `code/main.py` (+ modules) runs from scratch in ~56 s after `rm -rf output` and `uv sync`, exit 0, all checks OK (incl. Peru ANP platform check 777 ha), 16 figures, 418 numbers. Fallback without the three big files also exits 0 (414 numbers; maps skipped).
- Phase 5 + review: adversarial review (`notes/review.md`), high/medium items fixed in code and text.
- Phase 7: `docs/overnight/REPORT.html` (self-contained, ~9.6 MB) + `REPORT.md`; private artifact https://claude.ai/artifact/Uxv7gt7n5iNcnjP9hregjo (only the owner can open it until shared); agent.md §14 and README updated.
- Extra: replication zip builder `docs/overnight/make_replication_zip.py` → `replication/GroupAnteater_Q2_replication.zip` (82 MB, git-ignored); unzipped copy reproduces numbers.csv exactly (max rel. diff 7e-15).

**BLOCKED / manual steps**
1. MAAP raw HTML: maapprogram.org returns 403 to scripts. Open each URL in notes/maap_citations.md in a browser → File › Save Page As (HTML only) → `data_raw/maap/maap_<n>.html` → `shasum -a 256` → update DOWNLOAD_LOG.csv rows.
2. IBAMA embargo file ("Termos de embargo"): no URL found. Browse https://dadosabertos.ibama.gov.br (Cloudflare blocks scripts), find the embargo dataset, download the CSV into `data_raw/ibama/`, log it.
3. Brazil per-territory publisher check: the MapBiomas platform shows only Collection 11; our file is Collection 10.1. Either wait for a Col 11 per-territory file on https://brasil.mapbiomas.org/en/estatisticas/ or the Dataverse, or state the mismatch (D14) and use 39,915 ha (pack, Col 11) as the Brazil check.
4. IBAMA check number: IBAMA's site shows no totals; if the team finds the IBAMA "Painel de fiscalização" totals, add one year's count as the check.
5. Verify the Kayapó desintrusão date (May 2025) and the "26 Sep 2024 Ibama Kayapó" item, which rest on search snippets (gov.br was offline).

**Firecrawl:** 14 of 100 used.

**First three things the team should do**
1. Read REPORT.html §1 and §7 together and agree on the claim wording. The DiD is description only, parallel trends fail (2016 pre-coefficient), and sources disagree on the regional rise. Decide whether `output/fig_brief_main.png` is the brief figure.
2. Each person re-opens the sources they will cite (MAAP pages, Nunes et al. 2024, FZS page) and saves raw HTML (manual step 1). AI is not a source.
3. Run the required AI prompt for brief part 4 and keep the raw and edited answers for the appendix. Then draft the 2-page brief from §9 (brief skeleton) and build the replication zip with `uv run python docs/overnight/make_replication_zip.py`.
