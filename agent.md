# agent.md: Group Giant Anteater, Question 2 (Peru)

Reference for future sessions (human or AI). It covers what the repo contains, what the assignment asks for, and the rules we must follow. **Status (2026-10-08): repo explored only. No analysis done yet.**

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
| `brazil_municipality_year.csv`, `mining_area.csv` | Brazil | | Not for us (Brazil variant of Q2) |

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
- **Starter verified:** all 6 checks print OK; the Tambopata/Amarakaeri table reproduces the card's numbers (1,640→163 and 289→574 ha; hand-computed DiD −1,762 ha/yr, which is *description*, not causal).

## 10. Open items / next steps

- [x] Run the starter and confirm the 6 OK checks (done 2026-10-08).
- [ ] Fill in `TEAM_PLAN.docx` (members, roles still unknown).
- [ ] Download "Áreas naturales protegidas" Colección 4 → log → check number.
- [ ] Replace the example last row of `DOWNLOAD_LOG.csv`.
- [ ] Decide comparison group(s) and justify (Amarakaeri is the starter default but suffers spillovers).
- [ ] Describe → Compare (+ displacement, placebo, persistence) → optional event study.
- [ ] Find MAAP #130 / #193 / #208 and cite with page/figure.
