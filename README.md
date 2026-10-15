# Group Giant Anteater · Data for Good, October 2026

**Illegal gold mining in the Amazon. Question 2: How does mining move with enforcement?**
Two cases, both described on our question card:
- **Peru:** Operation Mercurio (February 2019), La Pampa, Tambopata buffer zone, Madre de Dios.
- **Brazil:** weaker enforcement in indigenous territories (2019–2022), then the operation in the **Yanomami** territory (from February 2023).
Practice partner: **Frankfurt Zoological Society (FZS)**. We present to Christof Schenck (Executive Director) in Lesson 5.

> **New here?** Start with [`docs/basics.html`](docs/basics.html) (places, legality, buffer zones, the operations; 5 min), then the walkthrough [`docs/walkthrough/EXPLAINER.html`](docs/walkthrough/EXPLAINER.html). The shared project reference is [`agent.md`](agent.md); the current definitions are in [`docs/PLAN_v3.md`](docs/PLAN_v3.md).

---

## What to hand in (Lesson 5)

| Deliverable | File |
|---|---|
| Brief (PDF, 2 pages + references + appendix) | `deliverables/GroupAnteater_Q2_brief.pdf` (Word version for editing: `..._brief.docx`) |
| Slides | `deliverables/GroupAnteater_Q2_slides.pptx` (+ PDF, two map videos) |
| Replication zip | `replication/GroupAnteater_Q2_replication.zip` (course structure; its README is [`README.txt`](README.txt)) |
| Everything we made | `replication/GroupAnteater_Q2_all_materials.zip` |

Rebuild all of it: `uv sync` · `uv run python code/main.py` (~3 min) · `uv run python docs/walkthrough/build_report.py` (pages + brief) · brief PDF: headless Chrome print of `docs/brief/BRIEF.html` · Word: `cd docs/brief/docx_build && npm install && node make_docx.js` · deck: `cd presentation/deck && npm install && node build_deck.js` · `uv run python tools/make_delivery.py`. Check: `uv run pytest tests -q`.

## One outcome, one zone set, one treatment (plan v3)

Every number is **net mining additions** (ha/yr) = new land + re-mined − stopped, from the MapBiomas Peru Collection 4 rasters, on **one zone registry** (official buffer zones kept whole), with **one treatment** (start of Operation Mercurio, first treated year 2019). Defined once in [`code/definitions.py`](code/definitions.py); `tests/` fail if a module deviates.

## Repository map

| Folder | What |
|---|---|
| `README.txt`, `DOWNLOAD_LOG.csv`, `data/`, `data_raw/`, `data_intermediate/`, `code/`, `output/`, `tests/` | the replication files (course structure) |
| `deliverables/` | final brief, slides, videos (copied by `tools/make_delivery.py`) |
| `docs/brief/` | brief source (`brief_content.md`), AI prompt and answer, Word builder |
| `docs/walkthrough/` | team walkthrough and methods page (sources + builder), decision log `LOG.md`, source notes |
| `docs/methods/` | Ruby's causal review: method cards S0–S14, review plan |
| `docs/review/` | Ruby's review v2, referee reports |
| `docs/presentation/` | talk storyline |
| `presentation/` | deck and map-animation sources |
| `course/` | the course's own files (assignment, question cards, data dictionary, starter, templates) |
| `archive/` | superseded drafts |

## The question

FZS supports Peru's protected-area authority (SERNANP) in enforcement against illegal gold mining in the Bahuaja-Sonene–Tambopata landscape. It needs to know whether an operation **reduces** mining (deterrence), **moves** it elsewhere (displacement), or only **delays** it.

**What our brief must tell FZS:** what should they expect in the targeted area, and around it, when an enforcement operation ends?

## Deliverables

| When | What |
|---|---|
| Day 1, end of day | Team plan, half a page ([`docs/team_plan/`](docs/team_plan/)) |
| Before Lesson 4 | Our added data downloaded, logged and checked; first descriptive statistics |
| Lesson 5 | Brief (2-page PDF), slides, replication zip. Presentation: 10 min + 5 min Q&A, opening with two fun facts about giant anteaters |

## Ground rules (from the assignment)

- **Annual additions, not levels.** Sum a unit's rows first, then take the difference from the previous year.
- **Label every claim** as description, prediction or causal.
- **Every number in the brief comes from our code**; cite outside numbers (MAAP etc.) with page or figure.
- **Say what satellites can't see**: river dredges, mercury, legality.
- **AI is not a source.** Keep the AI output for brief part 4 in the appendix.

---

## Conceptual draft (team brainstorm, 8 Oct)

*Working ideas from 8 Oct, kept for the record; superseded where `docs/PLAN_v3.md` differs.*

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
