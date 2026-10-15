# Group Giant Anteater · Data for Good, October 2026

**Illegal gold mining in the Amazon. Question 2: How does mining move with enforcement?**
Two cases, both described on our question card:
- **Peru:** Operation Mercurio (February 2019), La Pampa, Tambopata buffer zone, Madre de Dios.
- **Brazil:** weaker enforcement in indigenous territories (2019–2022), then the operation in the **Yanomami** territory (from February 2023).
Practice partner: **Frankfurt Zoological Society (FZS)**. We present to Christof Schenck (Executive Director) in Lesson 5.

> **New here?** Start with [`docs/basics.html`](docs/basics.html): where the places are, where mining is legal, what a buffer zone is, and what the enforcement was (5 min). Then read [`agent.md`](agent.md), the shared project reference (assignment, data rules, check numbers, decisions), and the strategy page `docs/strategy.html`.

---

## Quick start

```bash
git clone https://github.com/RubyAnn777/GroupAnteaterDataForGood.git
cd GroupAnteaterDataForGood
uv sync                                   # creates .venv with pandas, matplotlib, pyfixest, openpyxl
cd starter && uv run python gold_starter.py
```

You should see **six lines starting with `OK`** and a figure in `starter/output/starter_figure.png`.

**Full analysis (overnight branch):** from the repo root run `uv run python code/main.py` (about 1 minute). It re-runs every check, fails loudly if one fails, and writes all figures, tables and `output/numbers.csv` (every citable number with the function that produced it) to `output/`. Then `uv run python docs/overnight/build_report.py` rebuilds the team walkthrough `docs/overnight/EXPLAINER.html` (start here) and the brief draft `docs/brief/BRIEF_DRAFT.html`/`.md` from those numbers. Three large raw files are not in git (see `DOWNLOAD_LOG.csv`); without them `main.py` falls back to the small committed intermediates in `data_intermediate/` and skips the two maps.
No `uv`? Install it with `curl -LsSf https://astral.sh/uv/install.sh | sh`. The R starter (`starter/gold_starter.R`) needs base R only.

## The question

FZS supports Peru's protected-area authority (SERNANP) in enforcement against illegal gold mining in the Bahuaja-Sonene–Tambopata landscape. It needs to know whether an operation **reduces** mining (deterrence), **moves** it elsewhere (displacement), or only **delays** it.

**What our brief must tell FZS:** what should they expect in the targeted area, and around it, when an enforcement operation ends?

## Deliverables

| When | What |
|---|---|
| Day 1, end of day | Team plan, half a page ([`templates/TEAM_PLAN.docx`](templates/TEAM_PLAN.docx)) |
| Before Lesson 4 | Our added data downloaded, logged and checked; first descriptive statistics |
| Lesson 5 | Brief (2-page PDF), slides, replication zip. Presentation: 10 min + 5 min Q&A, opening with two fun facts about giant anteaters |

## Repository layout

| Path | What it is |
|---|---|
| `agent.md` | Shared project reference for humans and AI assistants |
| `CLAUDE.md` | Tells Claude Code to load `agent.md` automatically |
| `README.txt` | The course's original "start here" note |
| `gold_assignment_brief.pdf` | Assignment: deliverables, grading, data notes |
| `gold_question_cards.pdf` | Question cards; **page 3 is ours** |
| `docs/basics.html` | Start here: plain-language primer (map, legal zones, buffer zones, enforcement timeline) |
| `docs/strategy.html` | Strategy page: context, design, method, team plan, Claude Code how-to |
| `DATA_DICTIONARY.pdf` | Every variable in every table |
| `DOWNLOAD_LOG.csv` | Provenance log: one row per raw file, with URL, date, collection, sha256 and check number |
| `data_raw/` | Our own downloads, exactly as downloaded, one folder per source (MapBiomas Peru/Brazil, IBAMA, INPE DETER, BCRP, AMW, SERNANP, FUNAI, INGEMMET, MAAP) |
| `data_intermediate/` | Small derived tables rebuilt by `code/` from git-ignored raw files (IBAMA, AMW) |
| `code/` | Analysis: `main.py` is the single entry point; one module per part (Peru, Peru ANP, robustness, production, Brazil, IBAMA, DETER, spatial, brief figure) |
| `output/` | Everything `code/main.py` writes: figures, tables, `numbers.csv`, `checks.csv` |
| `docs/overnight/` | Overnight run of 10/11 Oct 2026: `LOG.md` (what happened, decisions), `EXPLAINER.html` (plain-language walkthrough of every step, figure and model), `notes/` (per-source notes and quotes) |
| `docs/brief/` | Brief draft (`brief_content.md` → `BRIEF_DRAFT.html`/`.md`, 2 pages) and the raw AI answer for part 4 |
| `data/` | The six data-pack tables (MapBiomas, World Bank Pink Sheet) |
| `starter/` | Starter code (Python, notebook, R): checks, levels vs additions, first DiD table |
| `how_the_panels_were_built/` | Scripts that built `data/` from raw files (reference only) |
| `templates/` | Team plan and replication README templates |
| `pyproject.toml`, `uv.lock` | Python environment |

## Ground rules (from the assignment)

- **Annual additions, not levels.** Sum a unit's rows first, then take the difference from the previous year.
- **Label every claim** as description, prediction or causal.
- **Every number in the brief comes from our code**; cite outside numbers (MAAP etc.) with page or figure.
- **Say what satellites can't see**: river dredges, mercury, legality.
- **AI is not a source.** Keep the AI output for brief part 4 in the appendix.

---

## Conceptual draft (team brainstorm, 8 Oct)

*Working ideas, not final decisions. See the strategy page and `agent.md` for the open questions.*

### Two exercises

**a) Displacement: figure out where the miners went.**
Measure how gold mining moves after enforcement. Look in the buffer zone and around the enforcement areas: which mines close, and where do new ones appear? The draft considers both enforcement cases on the card: Peru (Operation Mercurio, 2019) and Brazil (Yanomami territory, 2023).

**b) Difference-in-differences for each case, with a constructed/searched for control group.**

Here we can include the failed synthetic control approach and also use the unclean control in Brazil to show our efforts in establishing causality. 
### Control group selection

1. Get a map of all protected areas with their buffer zones.
2. Get the Amazon Mining Watch (AMW) polygons and build a panel by period and zone.
3. For every protected area, check whether its buffer zone has active mines, then whether there was active enforcement.
4. Pick controls that meet these criteria:

| Criterion | Why | How to check |
|---|---|---|
| Gold is present (rivers from the Andes) | Mining is possible at all | AMW polygons inside the zone |
| Far from the treated area | Avoid spillovers | Distance to La Pampa |
| Same country | Same regulation, same prices | Peru only |
| Geographically similar (climate, terrain) | Comparable conditions | Covariate data for treated and candidate zones |
| No enforcement at all | Otherwise it is not a control | Enforcement records (to be found) |

5. Find each treated zone's "geographic twin" with a matching algorithm, then run the DiD.

### Limitations noted so far

- Planes for transport?*(to clarify)*
- What exactly counts as "enforcement"?
- interoceanic highway (especially relevant for control group selection)
- mine abandonment and re-use (we cannot measure whether all mines have been abandoned or not)

### Other idea

Find out when gangs were active and when not, using relative prices of gold and coca as an instrumental variable.

### Still to fill in

- Descriptive exercise
- Control variables
- Graphs

### Draft structure for the presentation

Introduction - two fun facts about giant anteaters.

whats the difference between legal and illegal mining? 
regulations, impact, taxing etc etc. 
show the map and explain the zones (legal, illegal, buffer, protected, indigenous) and the enforcement operations.

Different manners of protection - what do they do? Protected vs indigenous territories -> (intro to SERNANP and their data) Cooperation with FENAMAD
How is illegality defined in data?
    Very High: Activity is occurring without a permit and within a protected area that doesn’t allow for any kind of resource exploitation
    High: Activity if occurring outside of any explicit concession for doing so
    Medium: Activity is happening within a concession, but active status could not be verified and/or concession doesn’t meet legal requirements
    Low: Activity is happening within active concession, but compliance with all requirements could not be verified

FZS impact and role + the zones they cover

Why illegality is an issue (social, environmental cost). Why it matters in other words.

Zone in on Peru and Brazil - explaining the initiatives 
(Operation Mercurio earls 2019 + The restauration plan since 2021)

Descriptives
-> how many of the areas are affected by mining today (indigenous + protected) (per country)
-> overall development of mining in studied area over time
-> comparison of mining activity before and after enforcement (also looking at buffer zone and close by areas)
**make sure we add the "number check" thing she wants us to do**

Trying to do causal analysis
-> failed synthetic control
-> looking for control 

Limitations and further research

Key limitation is that the enforcement is actually happening always somewhere in some unsystematic way. We need to find for the control a zone that has comparable levels of enforcement. Luckily in Peru its well done

Why was previous enforcement not effective? Even before 2017 there was a lot going on

Recommendations
local enforcement 
legal zone enforcement 
tracking systems
evaluating mercury travel in water
placement of enforcement operations as key measure
social cost (livelihoods of miners)
