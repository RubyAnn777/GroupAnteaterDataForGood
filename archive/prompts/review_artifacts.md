You are reviewing and polishing the deliverables of our Data for Good project (Group Giant Anteater, Question 2: "How does mining move with enforcement?", Peru Operation Mercurio + Brazil Yanomami). Read `agent.md` first — it is the project memory and its rules are binding.

## Scope
Work on branch `analysis/v2-raster` (the most up-to-date branch). Check `git status` and `git log -5` first; do not switch branches or commit without asking me.

Artifacts to review, in priority order:
1. **Brief** (graded, 2 pages + appendix): `docs/brief/brief_content.md` → built to `docs/brief/BRIEF_DRAFT.html`. Main figure: `output/fig_brief_main.png`.
2. **Walkthrough**: `docs/overnight/explainer_content.md` → `docs/overnight/EXPLAINER.html`.
3. **Methods page**: `docs/overnight/methods_content.md` → `docs/overnight/METHODS.html`.
4. **Figures**: `output/fig_*.png`, styled by `code/common.py`.

Also read before reviewing:
- **Handover summary:** `agent.md` §14 (latest results and decisions; trust it over any number quoted in this prompt).
- **New modules:** `code/v2_rdd.py`, `code/control_psm.py`, `code/peru_sdid.py`, `code/peru_context_models.py`, `code/placebo_explainer.py`, `code/v2_economics.py`.
- **Cited economics parameters:** `docs/overnight/notes/economics_sources.md` (check each parameter against its cited source and against how the code uses it).

How the pages work: text lives in the `*_content.md` files with `{{number_id:fmt}}` placeholders filled from `output/numbers.csv`; build with `uv run python docs/overnight/build_report.py`; the analysis runs with `uv run python code/main.py` (~1.5 min). Page syntax is documented in the header comment of `explainer_content.md`. Edit the content files and code, never the built HTML.

## Phase 1: critical review (no edits yet)
Use the installed skills where they fit:
- `blindspot` on `output/fig_brief_main.png` and the key results in `output/numbers.csv`: what are we not seeing (vices and virtues)?
- `referee2` in **code** mode on `code/` (econometrics audit + replication-package audit; skip the deck mode, we have no .tex slides). Put its scripts and report outside the replication zip contents.
- `event-study` for the Peru event study and the Brazil staggered design (concepts only; our code is Python/pyfixest, keep it that way).
- `dataviz` for every figure; `ui-ux-pro-max` for the HTML pages' layout and scannability; `smart-brevity` + `data-storytelling` for the brief's prose.

Review against the grading rubric (written work): framing and partner perspective 20% · provenance (data log, source check, replication, "what satellites cannot see" paragraph) 25% · **analysis and honesty about the claim 30%** · figure 10% · would FZS act on it 15%.

Check in particular:
- Every claim labelled **description, prediction or causal**; no accidental causal language ("Mercurio stopped/caused/drove"). The only causal sentence is the conditional one for 2019–21 (decision D19) — is it defensible given: one treated unit, partly treated comparison (Amarakaeri/Camanti), COVID 2020, Restauración 2021, the 2023 emergency, the placebo-in-space results, and the failing La Pampa 2010–13 pre-trend in the cell panel? Do the newer designs (road RD, PSM control, synthetic DiD, context models) agree with each other, and does the brief report their disagreements honestly?
- Every number in the brief traces to `output/numbers.csv` via code; external numbers (MAAP etc.) cited with author, year, page/figure; no AI cited as a source.
- Known traps from `agent.md`: the MINEM gold drop is a definition change; additions not levels; no mixing collections; no subtracting numbers across sources.
- Does the brief answer FZS's actual question — what to expect in the targeted area and around it when an operation ends — in terms Christof Schenck would act on?
- Brief fits 2 pages (parts 1–4); exactly one figure; part 4 has (a) learns / (b) could mislead incl. river dredging and mercury / (c) what data would help.

Output of phase 1: one prioritized list (blocker / should / nice), each item with file:line, the problem, and the proposed fix. Then stop and wait for my go.

## Phase 2: apply (after my approval)
Apply the approved fixes in small steps, rebuild after each, and verify: `code/main.py` runs clean, all checks OK in `output/checks.csv`, the brief PDF (headless Chrome) still fits parts 1–4 on 2 pages, and the numbers in the pages match `output/numbers.csv`. Update `agent.md` with any decision made. Report what changed and anything you could not verify.
