# Overnight log, 2026-10-10 → 2026-10-11

Branch: `analysis/overnight-2026-10-10`. Orchestrator: Claude Opus (subagents: sonnet/haiku). Deadline: 07:00 Berlin, 2026-10-11.
Start: 2026-10-10 23:40 CEST.

**Firecrawl calls used: 14 / 100** (ANP 1, MAAP 5, IBAMA 5, Brazil TI 2, scout 1, spatial 0, DETER/prod 0; Chrome-check + literature agents pending)

## Status by phase
| Phase | Status |
|---|---|
| 1 Data | mostly done (publisher-side checks via Chrome pending) |
| 2 Code | done (main.py + modules; all checks OK) |
| 3 Peru descriptive | done (incl. ANP inside reserves, event study, placebo-in-space) |
| 4 Brazil descriptive | done (TI Col 10.1, Roraima, IBAMA, DETER monthly) |
| 5 Robustness | done (Peru + Brazil robustness CSVs) |
| 6 Spatial feasibility | in progress (code/spatial.py + maps) |
| 7 Report | todo |

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
| D2 | Pack-based Peru analysis (phase 2/3) starts in parallel with the downloads; new datasets plug in later as separate modules. | Wait for downloads | The core Peru design only needs `data/` |

## Round log
### Round 1 (23:40)
- Created branch from main (15f6049). Read agent.md, basics.html §6–7.
- Launched batch 1 (parallel): Peru ANP download, Brazil TI download, Brazil enforcement source, MAAP citations, enforcement records, spatial data feasibility, code/main.py (Peru core).

### Round 1 results (00:05)
- DONE Peru ANP Col 4 (`data_raw/mapbiomas_peru/…AREAS-PROTEGIDAS.xlsx`, curl). Publisher-side check PENDING (platform is JS; try Chrome).
- DONE Brazil TI Col 10.1 (Dataverse doi:10.58053/MapBiomas/1F2TLA). Publisher check PENDING (MapBiomas factsheets quote Col 7/8 garimpo only; try platform via Chrome).
- DONE IBAMA autos de infração (zip via Azure blob behind dadosabertos; dadosabertos itself 403). Embargo file BLOCKED (no URL found). Sources: Nunes et al. 2024 Sci Rep (opened).
- DONE MAAP citations notes; raw HTML PENDING (maapprogram.org 403 to curl) → Chrome save.
- DONE enforcement timeline (controls partly treated: Amarakaeri yes, Munduruku yes from Aug 2023, Kayapó light).
- DONE code/main.py Peru core; all checks OK.
- Batch 2 launched: Peru ANP+robustness+figure fixes; Brazil module (TI, Roraima, IBAMA, robustness). Still running: spatial feasibility, extra-data scout.
- NEXT: Chrome agent for publisher-side checks + MAAP HTML; merge DOWNLOAD_LOG rows; phase 6 review; report.

### Round 1, continued (00:00)
- DONE Peru ANP+robustness (code/peru_anp.py, peru_robust.py), Brazil (brazil.py, brazil_ibama.py), DETER (brazil_deter.py), production (peru_production.py). All committed.
- Running: spatial module/maps; Chrome publisher checks + MAAP HTML; literature verification.
- NEXT: merge DOWNLOAD_LOG rows; brief main figure; report builder (numbers pulled from output/numbers.csv); clean-run verification.

### Round 1, continued (00:30)
- DONE: publisher checks (Peru ANP platform 777 ha = file 776.9 ha OK; Brazil TI: platform only Col 11 → collection mismatch, no Col 11 per-TI file exists); MAAP pages saved as rendered text (raw HTML blocked); literature verified (notes/literature.md); DOWNLOAD_LOG merged (30 rows, sha256); agent.md §14 + README updated; brief figure `output/fig_brief_main.png`; report builder + REPORT.html/REPORT.md (draft).
- Firecrawl total still 14 / 100 (Chrome-check, literature, Col 11 search: 0 each).
- Running: adversarial review (read-only), synthetic control + AMW zones, visual QA of REPORT.html.
- NEXT: apply review fixes; add synth + zones to report; clean run from scratch; publish artifact; final log.
