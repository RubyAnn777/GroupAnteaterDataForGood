# Method cards: causal methods review

One card per session of `docs/methods/causal_review_plan.md`. Each card explains the method in general first (simple, then Master's and PhD level), then applies it to our project, runs tests, and ends with proposed decisions and a verdict with exact wording for the brief.

Start with **00** (vocabulary and the treatment decision) and **14** (what it all adds up to).

| Card | Method | Attempts | Test script | Verdict |
|---|---|---|---|---|
| [00](00_potential_outcomes.md) | Potential outcomes, claim labels, the treatment | all | none | Treatment = start of Mercurio, Feb 2019 (decided) |
| [01](01_data_outcomes.md) | Data lineage and the three outcome measures | all | `code/review/s1_data_checks.py` | Measures not interchangeable; half the net fall is land stopping |
| [02](02_did_2x2.md) | 2×2 difference in differences | A1 | `s2_did_checks.py`, `s2_bz_composition.py` | D |
| [03](03_event_study_placebo.md) | Event study, placebo inference | A2 | `s3_event_study_checks.py` | D; raw rank 1 measures size |
| [04](04_twfe_ladder.md) | Two-way fixed effects ladder M1-M4 | A3 | `s4_twfe_checks.py` | D; M1 ≈ own before/after |
| [05](05_context_controls.md) | Context and bad controls | A4 | `s5_context_checks.py` | D; drop K-models from the brief |
| [06](06_synthetic_control.md) | Synthetic control | A5 | `s6_synth_checks.py` | D (of the failure); drop −411 |
| [07](07_synthetic_did.md) | Synthetic difference in differences | A6 | `s7_sdid_checks.py` | D; sensitivity only |
| [08](08_cell_panel.md) | Raster backbone, 1-km cell panel | A7 | `s8_cell_panel_checks.py` | D; before/after, depletion |
| [09](09_spatial_rd.md) | Spatial RD, road tests | A8, A9 | `s9_rd_checks.py` | D; a 2020-22 swing |
| [10](10_rule_based_twins.md) | Rule-based twins (Ruby's design) | A10 | `s10_twin_checks.py` | D |
| [11](11_matching.md) | Matching estimators | A11 | `s11_matching_checks.py` | D; no common support |
| [12](12_brazil.md) | Brazil: 2×2, staggered DiD, RI | A12-A14 | `s12_brazil_checks.py` | D; cannot separate operations from the end of the boom |
| [13](13_descriptive_predictive.md) | Displacement accounting, prediction, informed speculation | blocks, A15 | `s13_descriptive_checks.py` | D, P, speculation |
| [14](14_synthesis.md) | Synthesis: triangulation, the claim, the range, the fix list | all | cross-checks | One conditional [C] sentence (decided) |

All test scripts are read-only (they read `data/`, `data_intermediate/`, `output/`, `data_raw/` and write nothing). Run them from the repo root with `uv run python code/review/<script>.py`. S6, S8, S9 and S12 take 3-10 minutes; S8 and S9 read the committed raster `data_intermediate/zones_v2_mdd_full.tif`. Tests that need git-ignored raw files are listed in each card under "Tests not possible here".

Status: cards and tests done. Decided 2026-10-15: the brief keeps one narrowed conditional [C] sentence (D-S14-1/2/3), now in `brief_content.md`. Other decisions are **proposed** and wait for Ruby; no pipeline code (`code/*.py`) has been changed.

## After v3 (2026-10-15)

Plan v3 (`docs/PLAN_v3.md`, `code/definitions.py`) moved every module to one outcome (net mining additions = new land + re-mined − stopped, MapBiomas Peru Collection 4 rasters), one zone registry (official buffer zones whole) and one treatment (Mercurio, Feb 2019; reference 2018). Numbers quoted in the cards above come from the v2 pipeline; the v3 values are in `output/numbers.csv`, and the walkthrough and methods pages (`docs/walkthrough/explainer_content.md`, `methods_content.md`) now use them. The §10.1 priority-1 sentences of card 14 are gone from both pages. New on the pages: a quarter to a half of the 2019–21 fall in net additions is land stopping (LOG D32).
