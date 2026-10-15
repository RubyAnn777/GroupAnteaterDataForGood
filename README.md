# Group Giant Anteater · Data for Good, October 2026

**Illegal gold mining in the Amazon. Question 2: How does mining move with enforcement?**
Two cases, both described on our question card:
- **Peru:** Operation Mercurio (February 2019), La Pampa, Tambopata buffer zone, Madre de Dios.
- **Brazil:** weaker enforcement in indigenous territories (2019–2022), then the operation in the **Yanomami** territory (from February 2023).
**Team:** Ruby Ann Grambauer, Sebastian Schmid, Laurens van der Lely, Omkar Mate, Dhruv Chaudhari.
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
| Day 1, end of day | Team plan, half a page ([`docs/team_plan/`](docs/team_plan/), submitted) |
| Before Lesson 4 | Our added data downloaded, logged and checked; first descriptive statistics |
| Lesson 5 | Brief (2-page PDF), slides, replication zip. Presentation: 10 min + 5 min Q&A, opening with two fun facts about giant anteaters |

## Ground rules (from the assignment)

- **Annual additions, not levels.** Sum a unit's rows first, then take the difference from the previous year.
- **Label every claim** as description, prediction or causal.
- **Every number in the brief comes from our code**; cite outside numbers (MAAP etc.) with page or figure.
- **Say what satellites can't see**: river dredges, mercury, legality.
- **AI is not a source.** Keep the AI output for brief part 4 in the appendix.

---

The team's brainstorm of 8 October is kept in [`archive/README_brainstorm_2026-10-08.md`](archive/README_brainstorm_2026-10-08.md).
