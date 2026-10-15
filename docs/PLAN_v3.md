# Plan v3: one outcome, one zone registry, one treatment (from 2026-10-15)

Branch `analysis/v3-definitions` (from `origin/main` after Ruby's review PR #1). Trigger: Ruby's review v2 (`review.md`,
`docs/causal_review_plan.md` X1-X14, `docs/methods/01` T1/T5/T6, `14_synthesis.md` §10.1) and the team chat of
14-15 Oct 2026.

## Decisions (team, 2026-10-15)

| # | Decision | Where it lives in code |
|---|---|---|
| V3-1 | **One outcome everywhere: net mining additions** = mining(t) − mining(t−1) = new land + re-mined − stopped (ha/yr), MapBiomas Peru Collection 4 rasters, our pixel accounting. Split into the three parts wherever the estimator is linear; say so where it is not. | `code/definitions.py` (OUTCOME) |
| V3-2 | **One zone system: the raster, cut to one registry.** Official SERNANP buffer zones stay whole (Tambopata BZ = the publisher's 231,693 ha; Kotsimba is inside it); corridor and community land inside a zone is a tenure tag, not a carve-out. The statistics workbook is a reconciliation check only (`data_intermediate/bz_reconciliation.csv`); the course card numbers (1,640 → 163 etc.) stay as reproduction checks in `checks.py`. | `definitions.ZONES/UNITS`, `raster_zones.py`, `zonedata.py` |
| V3-3 | **One treatment:** start of Operation Mercurio, Feb 2019; first treated year 2019; reference 2018; later events are context; 2022-25 = "later years" (reported with and without 2023). | `definitions.py` (TREATMENT, PERIODS) |
| V3-4 | **Brief figure and headline move to net**, with the three parts shown where possible (reverses D-S14-9's first-time choice). | `brief_figure.py`, `slides_figures.py` |
| V3-5 | **No image validation sample** for "stopped" (out of scope). We split "stopped" with the data we have: what the land becomes (water, forest, other natural, other) and whether it is mining again within 1-2 years (flicker or re-entry). | `raster_zones.py` |
| V3-6 | **Word export of the brief only** (the final deliverable). | `docs/brief/` |
| V3-7 | Every registered number in ha names its measure, zone and period; every slide and figure states measure, unit, zone and period. | `common.Numbers`, `tests/` |

## Zone registry (exclusive, first match wins)

1 Tambopata National Reserve · 2 other protected areas · 3 La Pampa sector (Tambopata BZ, lon −70.15 to −69.80) ·
4 rest of Tambopata BZ · 5 Amarakaeri BZ (whole, incl. its Cusco part) · 6 Bahuaja-Sonene BZ · 7 other BZs ·
8 corridor across the road (D.L. 1100, ≤ 10 km north of the IOH, La Pampa longitudes, outside every BZ) ·
9 rest of the corridor · 10 native communities · 11 rest of Madre de Dios.
Tenure tag: corridor / Kotsimba / other community / none. `in_mdd` flag: department totals = sum of the same zones.
National panel: every buffer zone with mapped mining, whole, overlaps Tambopata → Amarakaeri → SERNANP code order.

**What changes versus v2:** v2 gave communities and the corridor precedence over buffer zones, so the raster
"Tambopata BZ" lacked Kotsimba (31,568 ha) and 21 km² of corridor, and zone designs used the workbook while pixel
designs used the raster (different land, T6). Amarakaeri in v2 raster covered only its Madre de Dios part.

## Exceptions (stated, not hidden)

- Amazon Mining Watch (AMW) and GLAD alerts cannot give net additions (no "stopped" state). They are kept only as
  independent checks of timing and of the twins idea, labelled with their own measure, and never in the same
  sentence as net additions.
- Brazil (backup slides only): MapBiomas Brazil Collection 11 rasters, same pixel accounting where available.
