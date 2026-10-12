# Plan v2: from zone tables to one raster, layered zones (2026-10-12)

Responds to Ruby's `review.md` and `readings.md`, MAAP #208, Asner & Tupayachi (2017) and Dethier et al. (2023).
Status: agreed decisions below; analysis not yet rebuilt. Owner of this file: whole team.

## Decisions (2026-10-12)

| # | Decision | Why |
|---|---|---|
| D26 | **One data backbone:** MapBiomas Peru Collection 4 annual rasters (30 m, 1985–2025), cut to our own polygons. AMW and the course tables become robustness checks. | Same product and grid everywhere (Ruby). Check passed: raster gives Tambopata buffer zone 2025 = 20,716 ha vs 20,730 published; reserve 776 vs 777; Amarakaeri BZ 14,087 vs 14,096. |
| D27 | **Layered units:** the buffer zone stays the official main unit; inside it La Pampa, Mangote and Kotsimba; around it the legal corridor (north vs south of the Interoceanic Highway), native communities, the reserve. | Separates "La Pampa reopened" (delay) from "Mangote grew" (displacement next door). |
| D28 | **Claim:** careful description as the core, plus one conditional causal claim with its threats. | Grading: honesty about the claim (30%). |
| D29 | **Scope:** run every analysis first, then choose what fits the 2-page brief and the 10-minute talk. | Team choice. |

## What the readings change

- **Dethier et al. 2023 (Conservation Letters)** already show La Pampa south of the highway shut down (ponds −4–5 %/yr after Feb 2019; 70–90 % abandonment) and mining jumped in legal concessions just north (ponds +42–83 %, +3–5 km²/yr deforestation). Anticorruption = monthly rotation of garrisons and commanders; forces stayed Feb 2019–Mar 2020; returns near the highway from mid-2021. Data stop in 2021. **Our added value:** to 2025, the whole region, inside the reserve, re-mining, an earlier enforcement wave, Brazil.
- **Asner & Tupayachi 2017 (ERL):** after the 2012 decrees and interdictions, mining loss dipped, then nearly doubled in 2013–14 → a second Peruvian "delay" case. Their buffer-zone total (30,047 ha forest lost to mining by 2016) is ~3.5× MapBiomas' 2016 mining area (8,714 ha): measures and boundaries differ, so we never mix them.
- **MAAP #208:** Jan 2021–Mar 2024, 73.8 % of mining deforestation inside the corridor, 7.9 % in buffer zones (mostly Tambopata, incl. Mangote), 14.6 % in native communities.

## Four questions, in order

1. **Target:** did mining stop in La Pampa itself, and for how long?
2. **Where did it go?** La Pampa → corridor across the highway → Mangote / Kotsimba → reserve. Share of new mining inside vs outside the corridor, per year.
3. **Region:** did Madre de Dios as a whole mine less?
4. **Is it typical?** The 2012–14 Peruvian wave; Brazil's staggered operations (2023–25).

## Work plan

| Step | What | Data | Output |
|---|---|---|---|
| S1 | **Spatial frame:** one polygon layer with flags and precedence: reserve, La Pampa, Mangote, Kotsimba, rest of buffer zone, corridor north / south of highway, native communities, other Madre de Dios. Boundary sources and dates logged; La Pampa and Mangote have no official polygon, so we define them and test two alternatives. | SERNANP, INGEMMET, RAISG (native communities, roads), raster | `data_intermediate/zones_v2.gpkg`, map figure. **Team checkpoint: review the map before S2.** |
| S2 | **Pixel accounting per zone and year:** new mining on forest, mining returning on old scars (re-mining), mining that stopped. | MapBiomas Peru Col 4 rasters | `zone_year_v2.csv` |
| S3 | **Descriptives:** series per zone; share inside the corridor over time; replaces "rest of Madre de Dios". | S2 | figures |
| S4 | **Comparisons:** La Pampa vs distant zones (event study, fake dates, fake places); twin abroad kept as a check. | S2 + existing | models |
| S5 | **Earlier wave 2012–14.** | S2 (1985–) | event study |
| S6 | **Monthly data:** check weekly forest-loss alerts (GLAD / RADD) for Peru without an account. | alerts | monthly series, if feasible |
| S7 | **Enforcement intensity:** search for interdiction counts per zone and year (Peru). | web / public data | table, if found |
| S8 | **Robustness across products:** raster vs course tables vs AMW vs published MAAP / Asner / Dethier numbers. | all | table |
| S9 | **Brazil:** staggered operations (kept), framed as post-COVID with a different design. | existing | — |
| S10 | **Context, not models:** 2017 spike (gangs, mercury), social cost, mercury travel, corridor legal framework, highway. | readings | brief part 4, talk |

## Process

- **One branch per rebuild** (`analysis/v2-raster`); `main` only via pull request after team review.
- **Checkpoints:** S1 map, then S3 descriptives, then S4 models. Ruby reviews each in `review.md`, citing the walkthrough step number.
- **Rules unchanged:** every number from `code/main.py` → `output/numbers.csv`; one check per dataset; cite only opened sources; claims labelled.
