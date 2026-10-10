# agent.md: Group Giant Anteater, Question 2 (Peru and Brazil)

> Claude Code loads this file automatically through `CLAUDE.md`. Keep it current: when a decision is made or a fact is verified, update this file in the same commit.

Reference for future sessions (human or AI). It covers what the repo contains, what the assignment asks for, and the rules we must follow. **Status (2026-10-09):** environment set up, starter verified, research design drafted (strategy page `docs/strategy.html`). No final analysis yet. Team decisions still open: see §12.

## 1. The assignment in one paragraph

Data for Good course (Lessons 3 to 5, October 2026). Partner: **Frankfurt Zoological Society (FZS)**. We present to Christof Schenck (Executive Director): a 10-minute talk + 5 minutes Q&A. **Start the talk with two fun facts about the giant anteater.**
Our group is **Giant Anteater → Question 2: "How does mining move with enforcement?" → Peru, Operation Mercurio (from February 2019)**.
Question to answer for FZS: *what should they expect in the targeted area, and around it, when an enforcement operation ends?*

## 2. Deliverables and deadlines

| When | What |
|---|---|
| Day 1, end of day | **Team plan**, half a page (`templates/TEAM_PLAN.docx`): question + country; unit and years; what we compare to what; sources; one reproduced check number; who does what. |
| Before Lesson 4 | Download, log and check our added data against the publisher's numbers. Bring first descriptive statistics. |
| Lesson 5 | **Brief** (PDF, 2 pages) + **slides** + **replication zip**. One upload per group, before class. |

### Brief: 2 pages, 4 parts (references and appendix don't count toward the 2 pages)
1. **The question** (~½ page): FZS's problem, why it matters, our question, places and years.
2. **Data and provenance** (~¼ page): each dataset + source, and **one check per dataset** (our number = publisher's number).
3. **Findings**: **one figure** + short interpretation. **Label every claim as description, prediction or causal.** Never make a causal claim by accident.
4. **What FZS can do with this**: 3 short paragraphs: (a) what FZS learns; (b) why it could mislead (endogeneity, measurement error, **what satellites can't see: river dredging, mercury**); (c) what data or design would let us say more.

**Appendix:** data log, references, and the AI output used for part 4 (both the raw AI answer and our edited version). Required prompt for part 4:
> "Here is my comparison: [units, years, outcome, and what you compare to what]. List the reasons this comparison could mislead, distinguishing omitted variables, reverse causation, selection of units, and measurement error in the outcome. For each, say what data or design would fix it."

### Grading (written work only; the talk is required but not graded)
Framing and partner perspective 20% · Provenance (data log, source check, replication, "cannot see" paragraph) 25% · **Analysis and honesty about the claim 30%** · Figure 10% · Would FZS act on it 15%.
"A careful description and comparison count for more than a regression that you cannot explain."

## 3. Question 2 card (Peru): the actual steps

**Context.** Operation Mercurio started in Feb 2019 in **La Pampa**, the largest illegal mining area, in the **buffer zone of the Tambopata National Reserve** (Madre de Dios). MAAP #130: mining deforestation in La Pampa fell by about 90%, and rose in three nearby areas. MAAP #193: by 2023 miners had returned, on already degraded land.

**Concept.** Enforcement raises the expected cost of mining. Possible outcomes: **deterrence** (it falls), **displacement** (it moves), or **delay** (it returns when enforcement ends). In the targeted area alone these look the same, so we need a comparison group (DiD). Spillovers into the comparison area bias the estimate **away from zero** here.

| Step | What to do |
|---|---|
| **Describe** | Annual additions for the targeted unit (Tambopata buffer zone) and each possible comparison unit, **2014 → latest year (2025)**. |
| **Compare** | Before/after × targeted/comparison (the starter does Tambopata vs Amarakaeri, 2016-18 vs 2019-21). Then three checks: **Displacement:** sum the targeted unit + neighbours; did the total fall? **Placebo:** pretend the operation started 3 years earlier (2016). **Persistence:** extend the comparison to the latest year. |
| **Model** (optional) | Event study: `y_it = α_i + γ_t + Σ_k β_k (targeted_i × 1[t=k]) + ε_it`, omitting the year before the operation (2018). Plot the β_k. |

**Why it could mislead (must address in the brief):**
- COVID-19 started one year after Mercurio (2020).
- Spillovers: Amarakaeri buffer additions went from 54 ha (2018) to 1,086 ha (2022).
- In 2023 the gold price was rising and enforcement had weakened, and the data can't separate the two.
- Re-mining an old site counts as an addition (the La Pampa return was on degraded land).
- **One targeted unit means standard errors are not informative.** Show the figure + placebo instead.

**Data we must add ourselves (Peru):** "Áreas naturales protegidas" (**Colección 4**) from `peru.mapbiomas.org/descargas/estadisticas`, to see what happened *inside* the Tambopata reserve itself (the pack only has buffer zones). Log it in `DOWNLOAD_LOG.csv` and add a `check(...)` for it.

**Optional reading:** MAAP #130 (2020), MAAP #193 (2023), MAAP #208 (2024); Assunção, Gandour & Rocha (2023, AEJ Applied, DETER); Saavedra (2025, working paper, Colombia RCT with spillovers). The card mentions a folder `optional_readings_by_question/`, which is **not in this repo** (it's on the course page).

### Check numbers for Q2
- Tambopata buffer zone 2025: **20,730 ha**
- Mean annual additions 2016-18 → 2019-21: **Tambopata 1,640 → 163 ha; Amarakaeri 289 → 574 ha**
- (Brazil-side, not ours: all indigenous territories artisanal 2025 = 39,915 ha; Roraima 446 ha in 2018 → 4,745 ha in 2024)
- Pack-wide: gold Aug 2026 = $4,411/oz; Madre de Dios 2025 = 112,622 ha; Brazil all municipalities 2024 = 609,637 ha.

## 3b. Brazil case (decided 2026-10-09: we do both countries)

From question card 2: **Brazil: indigenous territories 2019–2022, and the operation in the Yanomami territory from February 2023.**
- Between 2019 and 2022 federal enforcement against illegal mining is widely reported to have weakened (**we must find and cite a source**). Artisanal mining inside indigenous territories rose from **13,704 ha (2018) to 30,980 ha (2022)**.
- January 2023: federal public-health emergency in the Yanomami territory; operations to remove miners from **February 2023**.
- So Brazil gives the mirror image of Peru: a period of *weaker* enforcement (2019–22), then a targeted operation (2023).
- **Data we add:** MapBiomas Brazil "Indigenous Territories" statistics (**Collection 10.1**, brasil.mapbiomas.org/en/estatisticas) for the **Yanomami, Munduruku and Kayapó** territories. It ends in **2024**, so only two post-operation years.
- **Pack data:** `mining_area.csv` (all indigenous lands combined, by type/substance, 1985–2025, Collection 11) and `brazil_municipality_year.csv` (Collection 10.1, to 2024). Don't mix collections in one series.
- **Brazil check numbers:** all Brazilian indigenous territories, artisanal, 2025: **39,915 ha** · Roraima (where most of the Yanomami territory lies), all municipalities: **446 ha (2018) → 4,745 ha (2024)** · Brazil all municipalities 2024: 609,637 ha.
- Possible design: Yanomami (treated 2023) vs Munduruku and Kayapó (comparison), additions 2014–2024; displacement into neighbouring municipalities / territories.
- Caveats: inside indigenous territories most artisanal mining has "no substance" recorded (27,875 of 39,915 ha in 2025), so define the measure; only 2 post years; municipal mining class includes industrial mines (iron ore Parauapebas, bauxite Oriximiná/Paragominas).

## 4. Repo layout

```
README.md / README.txt          course "start here" (README.txt is the real one)
gold_assignment_brief.pdf       the assignment (deliverables, grading, data notes, regression syntax)
gold_question_cards.pdf         5 question cards; p.3 = our Question 2
DATA_DICTIONARY.pdf             every variable, every table
DOWNLOAD_LOG.csv                provenance log; last row is a TEMPLATE example, so replace with our own downloads
data/                           the six pack tables (see §5)
starter/gold_starter.py|.ipynb|.R   loads tables, runs 6 checks (prints "OK ..."), levels vs additions,
                                     Tambopata-vs-Amarakaeri before/after table, one figure → starter/output/starter_figure.png
templates/TEAM_PLAN.docx        day-1 team plan template (7 prompts)
templates/REPLICATION_README.txt  template for the final replication README
how_the_panels_were_built/      01-04 scripts that built data/ from raw publisher files (read-only reference;
                                 raw files are NOT included, don't run). 04_panels.py §4 already sketches the Q2 Mercurio figure.
```

## 5. Data tables (all areas in hectares, no missing values, UTF-8 with accents)

| File | One row is | Years | Use for Q2? |
|---|---|---|---|
| `peru_bufferzone_year.csv` | buffer zone × pa_category × department × year | 1985-2025 | **Main table.** Cols: `buffer_zone, pa_category, department, year, mining_ha, forest_ha, total_ha` |
| `peru_department_year.csv` | department × biome × year | 1985-2025 | Context (Madre de Dios totals). Keep `biome == "Amazonía"` |
| `prices_annual.csv` / `prices_monthly.csv` | year (1961-2025) / month (to Aug 2026) | | Gold price context (2023 confounder). Nominal USD |
| `brazil_municipality_year.csv`, `mining_area.csv` | Brazil | 1985-2024 / 1985-2025 | **Brazil case.** Municipalities: keep `biome == "Amazônia"`, identify by state + name, drop tiny border rows. `mining_area.csv`: national vs all indigenous lands, by type/substance; working measure of illegal gold = `gold_or_nosub_artisanal_ha` |

**Buffer zones in Madre de Dios** (candidate targeted + comparison units): Tambopata (Reserva Nacional) is **TARGETED**. Others: Amarakaeri (Reserva Comunal), Bahuaja-Sonene (Parque Nacional), del Manu (Parque Nacional), Alto Purús (Parque Nacional), Purús (Reserva Comunal), Megantoni (Santuario Nacional). Some span several departments.

**Peru Amazon-biome departments:** Amazonas, Ayacucho, Cajamarca, Cusco, Huancavelica, Huánuco, Junín, La Libertad, Lima, Loreto, Madre de Dios, Pasco, Piura, Puno, San Martín, Ucayali.

## 6. Data rules (non-negotiable)

1. **Use annual additions, not levels.** addition = mining_ha(t) − mining_ha(t−1) for the same unit. Levels trend up like the gold price, so correlations are spurious.
2. **Aggregate first.** A buffer zone has one row per department, and a department one row per biome. Sum to one row per unit-year *before* differencing.
3. **Identify a buffer zone by `buffer_zone` + `pa_category`** ("de Calipuy" exists twice, but not in the Amazon).
4. **Peru: keep `biome == "Amazonía"`** for department-level work (other biomes hold large industrial mines).
5. `mining_ha` = MapBiomas class 4.2 Minería: **all** mining (legal + illegal, artisanal + industrial, any mineral). It can't tell legality. Additions can be negative (reclassification) and include re-mining of old scars.
6. **Never subtract numbers from different sources** (e.g. MapBiomas 112,622 ha vs MAAP 135,939 ha for Madre de Dios: stock vs cumulative deforestation).
7. **Don't mix collections** in one series (Peru Colección 3 vs 4).
8. Cite the **publisher + collection** (e.g. "MapBiomas Peru, Collection 4"), not the data pack.

## 7. Reproducibility and citation rules

- **Every number in the brief must be produced by our replication code.** No code output means don't report it. The instructor will trace one number back through code and log to the publisher.
- External numbers (MAAP etc.): cite author/org + year in text, full reference with link, access date, page/figure.
- **AI is not a source.** Don't cite AI for facts; only list references we actually opened.
- Replication zip structure (see `templates/REPLICATION_README.txt`):
  ```
  README.txt          software + version, which file to run, run time, outputs
  DOWNLOAD_LOG.csv    one row per raw file
  data_raw/           every file exactly as downloaded (files over 50 MB: leave out, link in log)
  code/               ONE script/notebook, runs top to bottom
  output/             the figure + every number in the brief, in order of appearance
  ```
- Optional regression: unit + year FE, SEs clustered by unit; check robustness to dropping the largest unit.
  Python: `pyfixest.feols("y ~ x | place + year", data=d, vcov={"CRV1": "place"})` · R: `fixest::feols(y ~ x | place + year, data=d, cluster=~place)`.

## 8. Figure style (from the starter)

Two panels with a shared x-axis rather than twin y-axes; title; source line underneath; plain style (no top/right spines, light y-grid). The brief has exactly **one** figure, which makes the main point.

## 9. Local environment (set up 2026-10-08)

- **uv project** in the repo root: `pyproject.toml` + `uv.lock`, env in `.venv/` (git-ignored). Python 3.13; packages: pandas, matplotlib, pyfixest, openpyxl, ipykernel.
- Run anything with `uv run python <file>`; add packages with `uv add <pkg>`. Notebook kernel: select `.venv` in VS Code/Jupyter.
- Starter: `cd starter && uv run python gold_starter.py`. It must be run from inside `starter/`, and it writes `starter/output/starter_figure.png`.
- System `python3` (3.9, no pandas) should not be used. R is at `/usr/local/bin/R` if needed.
- Teammates: `git pull && uv sync`, then work as usual.
- **Starter verified:** all 6 checks print OK; the Tambopata/Amarakaeri table reproduces the card's numbers (1,640→163 and 289→574 ha; hand-computed DiD −1,762 ha/yr, which is *description*, not causal).

## 10. Context and facts verified 2026-10-09 (cite the source, not this file)

**FZS's stake.** FZS runs a program in the *Bahuaja Sonene and Tambopata* landscape: Bahuaja-Sonene NP 10,914 km², Tambopata NR 2,746 km², buffer zone 4,500 km². It explicitly supports SERNANP's law-enforcement operations against alluvial gold mining in the buffer and core zones (fzs.org/en/programs/peru/bahuaja-sonene-and-tambopata/, accessed 2026-10-09). So FZS is part of the enforcement we study.
- Cross-check: Tambopata BZ + Bahuaja-Sonene BZ `total_ha` 2025 = 450,629 ha ≈ 4,506 km², which matches FZS's 4,500 km².

**Enforcement is a sequence, not one event** (MAAP #241, Pacsi et al., 10 May 2026, maapprogram.org/mining-peru-tambopata/):
| When | What |
|---|---|
| 2017–2018 | Series of operations and interdictions in the region (AIDER 2021, cited in MAAP #241), so the pre-period is not enforcement-free |
| Feb 2019 | **Operation Mercurio**, multisectoral, starting in La Pampa |
| 2020 | COVID-19: fewer patrols; miners re-entered Tambopata (Romo 2020, cited in MAAP #241) |
| 2021 | **Plan Restauración**: military interventions across critical zones of southern Peruvian Amazon |
| 7 Apr 2023 → | **State of emergency** (DS 046-2023-PCM): Tambopata, Inambari, Las Piedras, Laberinto, Madre de Dios and Huepetuhe districts, renewed every 60 days |
| 2025 | Navy units withdrawn from Malinowski River control posts (funding) |
| H2 2025–Feb 2026 | ~500 ha of new mining deforestation **inside** Tambopata NR (Malinowski River); Jan–Mar 2026 operations |

**Displacement evidence** (MAAP #130, Finer & Mamani, 1 Dec 2020, maapprogram.org/gold-mining-peru/), mining deforestation before → after Mercurio:
La Pampa 4,450 → 300 ha (165 → 17 ha/month, −90%) · Alto Malinowski 1,558 → 419 · **Camanti (Amarakaeri buffer zone) 336 → 105** · Pariamanu 72 → 98 · Apaylon 73 → 78 · Chaspa: new front, 113 ha. The legal mining corridor was excluded from MAAP's analysis.

**Implications for our design**
1. The control (Amarakaeri) was partly treated as well (Camanti declined; Huepetuhe/Madre de Dios districts are under the 2023 emergency). The DiD compares *more vs less* enforcement, not treated vs untreated.
2. 2021 (Restauración) and 2023 (emergency) are further treatment waves; mark them in every time-series figure.
3. Displacement may go **into the reserve** (MAAP #241) and **outside buffer zones** (Pariamanu, Chaspa), so we need the ANP file and the "rest of Madre de Dios" series.
4. No usable control outside Madre de Dios: in 2025 the Amazon-biome mining area is Puno 1,938 ha, Cusco 1,607, Huánuco 1,176, others < 400 ha (vs MdD 112,622).
5. "Rest of Madre de Dios" (department minus all buffer zones) includes the legal mining corridor, and MapBiomas can't tell legal from illegal.

**Descriptive numbers already produced (Madre de Dios rows, mean additions ha/yr):**
| Period | Tambopata BZ | Amarakaeri BZ | Rest of MdD | MdD total |
|---|---|---|---|---|
| 2016–18 | 1,638 | 284 | 1,688 | 3,610 |
| 2019–21 | 163 | 540 | 3,937 | 4,640 |
| 2022–25 | 1,829 | 1,199 | 9,020 | 12,049 |
The department total did not fall after Mercurio (description).

## 11. Team brainstorm (Ruby's conceptual draft, README.md)

Two exercises: (a) displacement, i.e. where did miners go; (b) DiD per enforcement case, with a control group chosen by criteria (gold present, far away, same country, geographic twin, no enforcement) and a matching algorithm. Other idea: gold/coca relative prices as an IV for gang activity. Our review of this draft:
- AMW detects mining **on land**, not river dredges (question card 4); polygon presence = mining happened, not "gold present". Select controls on **pre-2019** mining only, otherwise we select on the outcome.
- "No enforcement at all" is unlikely to exist in Madre de Dios 2019–2025 (Restauración, state of emergency). Use enforcement *intensity* or "less treated".
- AMW annual periods start in 2018, so there is essentially no pre-trend for Feb 2019. Pre-trends must come from MapBiomas.
- "Geographic twin" algorithms: nearest-neighbour / Mahalanobis matching on pre-2019 covariates, synthetic control, synthetic DiD.
- The gold/coca IV fails the exclusion restriction (the gold price drives mining directly); keep it for part 4 at most.

## 12. Open decisions (team)

- [ ] Members and roles (team plan item 7).
- [x] **Decided 2026-10-09: Peru AND Brazil.** Two case studies, one design (deterrence / displacement / delay). See §3b.
- [ ] How far to take the spatial extension? Overnight prototype (`code/spatial.py`) works; recommendation: brief part 4 / one robustness panel, not the core (AMW starts 2018 = stock, no pre-period).
- [ ] Meaning of "planes" in the limitations list.

## 13. Open items / next steps

- [x] Run the starter and confirm the 6 OK checks (done 2026-10-08).
- [ ] Fill in `TEAM_PLAN.docx` (members, roles still unknown). Draft answers are in `docs/strategy.html`.
- [x] Download "Áreas naturales protegidas" Colección 4 → log → check number (overnight 2026-10-10; platform shows 777 ha = file 776.9 ha).
- [x] Replace the example last row of `DOWNLOAD_LOG.csv` (overnight run).
- [x] Describe → Compare (+ displacement, placebo, persistence) → event study (overnight run, `code/`; **team must review**).
- [ ] Open and cite MAAP #130, #193, #208, #241 with page/figure (each team member opens what they cite). Quotes + locations drafted in `docs/overnight/notes/maap_citations.md`; raw HTML still needs a browser "Save as" (site blocks scripts).
- [ ] Review `docs/overnight/REPORT.html` (draft) and decide the brief figure (`output/fig_brief_main.png` proposed).

## 14. Overnight run 2026-10-10/11 (branch `analysis/overnight-2026-10-10`; DRAFT, needs team review)

Full story in `docs/overnight/LOG.md` (decisions D1–D11+) and `docs/overnight/REPORT.html`. Run: `uv run python code/main.py` → `output/` (+ `output/numbers.csv`, `output/checks.csv`).

**New data (all in `DOWNLOAD_LOG.csv`, raw files in `data_raw/<source>/`):**
| Data | Collection / version | Check |
|---|---|---|
| MapBiomas Peru ANP statistics `MAPBIOMAS-PERU-LULC-COL4-AREAS-PROTEGIDAS.xlsx` (sheet COVERAGE_4, ANP name `territory_level_2_1`, category `_3_1`, mining class 30 "4.2. Minería") | Collection 4 | Tambopata NR mining 2025 = 776.9 ha; platform shows 777 ha (screenshot) |
| MapBiomas Brazil coverage by indigenous territory (Dataverse doi:10.58053/MapBiomas/1F2TLA), class 30 = 4.3 Mining, all mining (no garimpo split per territory); identify by `geocode`, sum state/biome rows | Collection 10.1, to 2024 | Kayapó 2024 = 18,176 ha; platform shows only Col 11 (17,632 ha) → collection difference. No Col 11 per-territory file published (checked 2026-10-11) |
| IBAMA autos de infração (zip, 117 MB, git-ignored) | download 2026-10-10 | no total on IBAMA site; intermediate `data_intermediate/ibama_autos_annual.csv` |
| INPE DETER class MINERACAO (WFS) + FUNAI TI polygons | 2016–2026 | 2019 total 105.64 km² vs dashboard 105.40 km² |
| BCRP (source MINEM) declared gold production, Madre de Dios | 2001–2025 | monthly sums = annual |
| Amazon Mining Watch patches (source.coop, 112 MB, git-ignored), SERNANP ANP/BZ, FUNAI TIs, INGEMMET D.L. 1100 corridor | current | prototype only |

**Decisions made overnight (see LOG.md for alternatives):** buffer-zone units sum ALL department rows (reproduces the card; §10's 1,638/284 were MdD rows only); event-study pool A = Tambopata + Amarakaeri + Bahuaja-Sonene BZ, inference by placebo-in-space rank, not clustered SEs; event markers at Y − 0.5; Brazil DiD in ha AND % of 2022 stock; Kayapó = best Brazil control (Munduruku treated Aug 2023, Nov 2024).

**Headline descriptive results (numbers from `output/numbers.csv`):** Peru DiD −1,762 ha/yr (placebo +209; persistence −737 vs Amarakaeri, ≈0 vs all buffer zones); Tambopata ranks 1/15 in placebo-in-space; Madre de Dios total additions 3,610 → 4,640 → 12,049 ha/yr (2016–18 / 2019–21 / 2022–25), so no regional fall; Tambopata NR (inside) +241 ha in 2025; declared MdD gold production −88% 2018→2025 while mapped area 50,506 → 112,622 ha. Brazil: Yanomami additions 1,617 (2022) → 824 (2023) → 179 ha (2024), but Kayapó and Munduruku also fell, so the 2×2 is inconclusive (sign flips with scaling); IBAMA Legal Amazon autos 6,920/yr (2015–18) → 4,359/yr (2019–22) → 7,907 (2023).

**New facts from sources (cite the source, not this file):** MAAP #193: 148 → 598 dredges in La Pampa (2021 → 2023; the page's "more than 400%" is really +304%, cite the counts). MAAP #208: 74% of 2021–24 mining deforestation in MdD was inside the legal corridor. MAAP #241: 500 ha inside Tambopata NR (431 ha H2 2025 + 69 ha to Feb 2026); navy withdrawn from Malinowski posts in 2025. Nunes et al. 2024 (Sci. Rep., doi:10.1038/s41598-024-52180-7): embargoes −59% and confiscations −55% in 2019–2020. Munduruku operation from Aug 2023, desintrusão Nov 2024; Kayapó desintrusão May 2025 (search snippets only, verify).
