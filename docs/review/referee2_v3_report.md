# Referee 2 report, round v3: GroupAnteater Q2 pipeline (branch analysis/v3-definitions, commit 3c7487d)

Date: 2026-10-15. Mode: code audit (referee2) plus a blindspot pass on the outputs.
I treated the repo as read-only. I did not run `code/main.py`, because it writes into the repo. I ran the tests with `-p no:cacheprovider`. All of my scripts and outputs are in this folder:

| File | What it does |
|---|---|
| `r2_raster.py` | Independent pixel accounting from the `.tif` rasters and SERNANP polygons. Does not import repo code. Uses a different formulation: first-mined-year array, explicit look-ahead, and WGS84 geodesic pixel area. |
| `r2_models.R` | Base-R replication of the 2x2 DiD, TWFE M1/M4, placebo ranks and the event study. This is the cross-language leg. |
| `cmp.py`, `cmp2.py` | Line-by-line comparison against `output/numbers.csv`, the workbook and `data_intermediate/zone_year.csv`. |
| `decomp.py`, `excess.py`, `r2_stopped.py`, `cells.py` | The "half is stopping" checks, a stopping-rate counterfactual, the age and longitude profile of stopped pixels, and the closed-form cell DiD. |
| `r2_zone_year.csv`, `r2_stopped_to.csv`, `r2_decomposition.csv`, `r2_stopped_profile.csv` | Outputs of the scripts above. |

Note: other agents edited the working tree while I worked (`docs/brief/brief_content.md`, `code/main.py`, and a new untracked `code/brief_checks.py`). `output/numbers.csv` is byte-identical to the 3c7487d version. Where it matters I say which version of the brief I mean.

---

## Summary

The core is correct and reproduces independently:
- The accounting identity and the definitions are right.
- The zone registry for Tambopata and Amarakaeri is right.
- The 2x2, M1, the event study, the cell DiD and the RD parts are linear and add up.

The main problems are about interpretation:
1. "About half of the fall is land stopping" is the upper end of a 12–55% range. It is fragile and concentrated in 2019.
2. The "stopped" split by land destination is partly broken: the "natural" category is always zero, and the water class collapses after 2022.
3. The verdict of the pre-trend test depends on whether the 2010 lead is included.
4. The size-relative placebo rank is 3, 4 or 6 of 7 depending on the variant.
5. The walkthrough and methods pages, and the brief as committed, still point to number ids that no longer exist.

Verdict: **Minor revision for the code. Major revision for the claims built on "stopped".**

---

## Audit 1: Independent replication (priority 1)

### 1a. Zone areas

| Zone | Area (my polygon) |
|---|---|
| Tambopata buffer zone (RN09) | 231,693.2 ha (equals the publisher's 231,693) |
| Amarakaeri buffer zone (RC03, minus RN09) | 283,467.8 ha |
| La Pampa sector | 61,355 ha |

The Tambopata buffer-zone polygon overlaps the ANP interiors by only 0.1 ha, so putting `tambopata_nr` and `other_anp` first in the partition costs nothing.

### 1b. Stocks against the publisher workbook

| | My geodesic area | Workbook | Repo (`*_stock_2025`) |
|---|---|---|---|
| Tambopata BZ 2018 | 12,925.8 | 12,925.7 | not registered |
| Tambopata BZ 2025 | 20,730.1 | 20,730.0 | 20,716.2 |
| Amarakaeri BZ 2018 | 7,511.6 | 7,511.6 | not registered |
| Amarakaeri BZ 2025 | 14,096.0 | 14,095.9 | 14,086.8 |

- My net additions match the workbook: Tambopata 1,639.70 / 162.51 against 1,639.65 / 162.51; Amarakaeri 289.26 / 573.83 against 289.17 / 573.83.
- **Pixel counts are identical** to the repo. All 328 period means of net/new/re-mined/stopped for the four zones differ from the repo by 0.03–0.07% only.
- That gap is a units issue, not a counting issue. `raster_zones.row_area` (`code/raster_zones.py:108-110`) uses a spherical approximation that is 0.065% smaller than the WGS84 ellipsoid.

### 1c. Accounting definitions: verified exactly

- `remined = mine_t & ~mine_{t-1} & before_prev` (`raster_zones.py:219`) means "mined at t, not at t−1, mined in some year ≤ t−2". The `before_prev |= prev` update at line 234 runs before `prev` is updated, so this is correct.
- `new = mine & ~ever` is correct.
- My formulation (`first == t` / `first < t−1`) gives identical results. The identity error is 4.5e-12.
- **Look-ahead** (`raster_zones.py:227-232, 251-253`): `stopped_back_1y` and `stopped_back_2y` match my own look-ahead to the hectare in every year from 2012 to 2023. Censoring is correct: back_1y is NaN in 2025, back_2y is NaN in 2024–25.
- **Water split:** `stopped_to_water` matches mine to the hectare.

### 1d. Cross-language (Python against base R) on my own T and A series

| Statistic | My R | Repo |
|---|---|---|
| 2x2 main (net / new / re-mined / stopped) | −1,761.8 / −1,109.7 / −2.1 / 650.0 | −1,760.6 / −1,108.9 / −2.1 / 649.5 |
| Placebo DiD | +208.6 | +208.5 |
| Persistence DiD | −737.0 | −736.5 |
| Base 2014 DiD | −1,663.5 | −1,662.3 |
| M1 during (net / new / re-mined / stopped) | −1,453.2 / −945.1 / 251.2 / 759.3 | −1,452.2 / −944.5 / 251.1 / 758.8 |
| M1 raw rank | 1 of 15 | 1 of 15 |
| M4 | −1.449, rank 3 of 7 | same |
| Cell DiD, La Pampa / across the road (closed form) | −1.6843 / +0.8943 | same exactly |

The cell DiD reproduces exactly from `cell_year.csv.gz`.

### 1e. Identity across all registered numbers

net = new + re-mined − stopped holds for all 328 registered net/parts groups, to within 0.5 ha. The five "violations" are p-values, which do not have to add up.

---

## Audit 2: Consistency (priority 2)

**La Pampa sector definition:** consistent everywhere I checked.
- Every module uses `D.LP_LON` with registry zone 3: `raster_zones`, `v2_stats.gradient`, `v2_rdd` (south side = zone `lapampa`), `spatial` (distance from zone 3), `brief_figure` (via `zonedata`), and `control_amw.lapampa_sector()`.
- Exceptions, both declared:
  - `glad_alerts.py:168-179` uses its own "70.15–70.00 W box" for GLAD-S2. It is labelled in the zone field.
  - `slides_map_export.py:45` hard-codes `LP_LON` and reads `zone_year_v2.csv`.

**Test suite:** 4 fail, 131 pass.
- `slides_figures.py`: workbook use, v2 intermediates, hard-coded windows.
- `slides_map_export.py`: v2 intermediates.
- `slides_figures.run` is commented out in `main.py:69`, so `numbers.csv` has 0 `sl_*` ids. `presentation/deck/build_deck.js` therefore throws "number … missing". This is known ("pending") but means the deck cannot currently be built.

**Window and measure violations the tests miss (Minor):**
- `spatial.py:64-66` defines its own AMW windows: "2022–24", and "2025–26 provisional". This is defensible for AMW but bypasses `PERIODS`.
- `peru.py:135` hard-codes `loc[2011:2018]`.
- The "later" stopped-return share (`*_later_stopped_share_back_within_2y`) is labelled 2022–25 but is only defined for 2022–23 because of censoring (`peru.py:75-76`). Its label should say so.
- `test_no_private_windows` only catches the literals `(2019, 2021)`, `loc[2019:2021]` and `!= 2018`. It misses `between(…)`, `range(…)` and the `2010-13` lead window. Extend the regex, or better, grep for every 4-digit year outside `definitions.py`.

**Major: docs are out of sync with `numbers.csv` at 3c7487d.**

| Page | Ids it uses | Ids missing from v3 `numbers.csv` |
|---|---|---|
| Committed `brief_content.md` | 51 | 37 (`mean_add_*`, `did_main`, `t5_m2_*`, `v2_new_*`, `rd_road_did`, `st_main_lapampasector_*`, …) |
| `explainer_content.md` | 468 | 234 |
| `methods_content.md` | 104 | 40 |

- None of the three pages can be built from this commit.
- The working-tree brief has been rewritten. It still lacks the 16 `chk_*` ids, presumably to come from the untracked `brief_checks.py`.
- The explainer and methods pages still say the corridor "passes" its pre-trend test and quote the v2 cell coefficients −1.21 / p = 0.08. Under v3 these are different (see Audit 3).
- **Fix:** add a test that every `{{id}}` in `docs/**/_content.md` exists in `numbers.csv`, and run it in CI before each commit.

**Minor: v2 intermediates are still tracked in git**, although the commit message says "removed": `zone_year_v2.csv`, `cell_year_v2.csv.gz`, `zones_v2_*.tif`, `official_unit_year_v2.csv`, `road_band_year_v2.csv`, `cell_attr_v2.csv`.

**Minor: reconciliation outlier, Alto Mayo (BP06).**
- Raster stock 2025 = 30.6 ha against workbook 93.1 ha; net correlation 0.87. Every other buffer zone matches within 0.1%.
- BP06 is in `AMAZON_BZ` and in pool B. Check its polygon or drop it from the Amazon pool, and say which.

---

## Audit 3: Econometrics (priority 3)

### 3a. Linearity: holds

net = new + re-mined − stopped holds for the 2x2, the event study (`peru.py:186-187`, closed form checked against pyfixest), M1–M3 (`peru_models.py:117-123`), the cell OLS (`v2_stats._assert_parts`), and the RD at a fixed bandwidth (`v2_rdd.py:162-167`, with h given and b = h by default). M4, the ranks and PPML are correctly labelled as net-only.

### 3b. Inference with one treated unit

**Raw placebo ranks measure size.** This is disclosed correctly: Tambopata is rank 1 in 2014, 2015 and 2016 as well, but 15 in 2017.

**Major: the size-relative rank depends on the variant.** The brief cites "rank 4 of 7". The same idea gives:

| Variant | Rank |
|---|---|
| `placebo_space_rank_scaled` (event study, 2018 single-year reference) | 6 of 7 |
| `model_m1_rank_scaled` (pooled 2014–18 reference, placebo donors = 14 pool-B zones) | 4 of 7 |
| Same as above, donors = scaled pool only (my R) | 6 of 7 |
| `model_m4_rank` (scale the outcome, then fit) | 3 of 7 |
| Baseline (pre-migration) `placebo_space_rank_scaled` | 10 |

- All variants agree on the qualitative point: Tambopata is not unusual relative to its size.
- The cited number is a choice among 3, 4 and 6. Report the range, or name one variant and say why.
- The zones that beat Tambopata in scaled terms are high-Andean (Junín RN02, Río Abiseo PN06, Cotahuasi RP02). `definitions.AMAZON_BZ` excludes exactly these. Among the scaled pool restricted to Amazon zones (RN09, RC03, PN08, RN10), Tambopata ranks 2 of 4.

**Major: cell-panel p-values come from comparison cells with no mining.**
- Comparison cells average 0.0005 ha/cell-yr before and 0.009 during, so the La Pampa coefficient is the zone's own before/after change. Check: −1.684 × 661 cells ≈ −1,113 ha/yr, the same as the zone change.
- CRV1 by 10-km blocks (16 La Pampa blocks) treats La Pampa-wide year shocks as independent across blocks: a classification regime, an operation, COVID. So p = 0.012 and WCB p = 0.007 overstate precision.
- The docstring says "descriptive". The figure headline puts p-values in the title (`v2_stats.py:212-216`).
- **Fix:** drop the p-values from figure titles, or add a time-placebo distribution (the same coefficient for fake windows 2011–13 vs 2014–16, etc.).
- **WCR implementation:** correct (`v2_stats.py:120-147`). FWL demeaning is exact because the panel is balanced; the null is imposed after the projection; Rademacher weights; the p-value uses `≥`. With 16 treated clusters, WCR is acceptable but not a cure for the common-shock problem above.

**Major: the pre-trend test verdict depends on the lead window.**
- `definitions.PANEL_YEARS = (2011, 2025)` makes 2011–13 the main lead window. Results:

| Zone | Outcome | Leads 2011–13 | Leads 2010–13 |
|---|---|---|---|
| La Pampa | net | p = 0.106 | p = 0.0086 |
| La Pampa | new | p = 0.128 | p = 0.0056 |
| Corridor across the road | net | **p = 0.041 (fails)** | p = 0.017 |
| Corridor across the road | new | p = 0.278 | not reported here |

- The v2 baseline used 2010–13 and reported "La Pampa fails".
- The migration therefore changed La Pampa's verdict from fail to pass by dropping one lead (2010, a pre-boom year at 199 ha), and changed the corridor's from pass to fail by switching to net.
- `fig_v2_stats_event` titles say "not rejected" for La Pampa.
- **Fix:** headline both windows. Say that 2010 predates the boom (net 199 ha in 2010, 1,467 in 2011), so the test is weak either way. State that the corridor's net pre-trend fails at 5%.

**Minor: RD weakened under net.**
- `rd_road_did_net` = +2.17 % of land per year, p = 0.25 (fixed-h p = 0.19), fake-start rank 2 of 10 (p = 0.20; the largest fake is 2.172, almost exactly the real value).
- v2 had +2.10, p = 0.079, rank 1.
- The committed brief cited `rd_road_did` / `rd_road_did_p`, which no longer exist. Do not reinstate it as evidence.

**Suspicious changes against the baseline that need a sentence of explanation (AMW and twins, not the core):**
- `top3_ratio` 0.40 → 0.16 and `psm_cem_gap_during` −11.7 → −41.5 pp. The treated unit is now the whole official BZ, and the twin set changed (`ctl_n_relaxed` 2 → 3).
- `psm_ps_nn1_n_ctl` = 0: no caliper match, so the "PS NN" estimators have no controls.
- `synth_core_addsc_rank` 1 → 4 of 5.
- `bs_sar_gap_logpts` flips sign (+0.31 → −0.74).

The core numbers did not move: the 2x2, M1, the 1,640 → 163 series, and the placebo.

### 3c. "About half of the fall is land stopping": not stable (Major)

Share of the fall in net additions that comes from more stopping. Own before/after uses the zone alone; the rate-adjusted column assumes stopping continued at the pre-2019 rate per hectare of last year's stock.

| Zone, pre window, post | Raw share | Excluding land back within 2 years | Excluding back within 1 year | Rate-adjusted excess |
|---|---|---|---|---|
| Tambopata BZ, 2016–18 → 2019–21 | **0.47** | 0.25 | 0.31 | 0.28 |
| Tambopata BZ, 2014–18 → 2019–21 | **0.54** | 0.30 | 0.37 | 0.21 |
| La Pampa, 2016–18 → 2019–21 | **0.51** | 0.24 | 0.32 | 0.33 |
| La Pampa, 2014–18 → 2019–21 | **0.55** | 0.27 | 0.35 | 0.27 |
| Tambopata BZ, 2016–18 → 2020–21 only | 0.31 | 0.11 | 0.20 | – |
| La Pampa, 2016–18 → 2020–21 only | 0.29 | 0.05 | 0.16 | – |
| Tambopata BZ, 2016–18 → 2019 only | 0.89 | 0.61 | 0.62 | – |
| DiD vs Amarakaeri (2x2 main) | 0.37 (650 / 1,762) | – | – | – |
| M1 (vs 14 zones) | 0.52 (759 / 1,452) | – | – | – |

What this shows:
- "About half" holds only for raw stopping, before/after or M1, and only with 2019 included.
- The stopping rate (stopped / last year's stock) in La Pampa was 6.0–9.7% in 2013–18, **15.2% in 2019**, then 7.8% and 8.8% in 2020–21. Those last two are inside the pre-2019 range.
- So after 2019 the higher hectares of stopping are mostly a bigger stock (the 2017–18 boom) stopping at the usual rate.
- Of the excess stopping above the pre-2019 rate in 2019–21, about two-thirds falls in 2019: 828 of 1,227 ha in Tambopata BZ, 820 of 1,112 in La Pampa (2016–18 rate).
- Part of the raw stopped share is offset by re-mining (−12% share), because land that flickers off and back on enters as both stopped and re-mined.

Defensible wording:
> "Between a quarter and a half of the 2019–21 fall is mined land leaving the mining class, almost all of it in 2019; after 2019 the fall is mostly less new land."

The working-tree brief (lines 29 and 33) says "About half … not fewer new pits" and "About half of it is land stopping (759 of 1,452)". Change both to the range, and register the flicker-adjusted and rate-adjusted shares in code.

**Other brief claims checked: all hold.**
- "Every 2019–21 year (≤ 417) was below every 2011–18 year (≥ 707)". It hinges on 2016 (707). The 2012 net is 743 in Tambopata BZ but 629 in La Pampa.
- "Amarakaeri stopped 542 → 584".
- "Rises elsewhere = 1.83× the fall".

---

## Audit 4: What "stopped" can and cannot tell us (priority 4)

### 4a. Split by land destination

**Major (code): the "natural" category is always 0.**
- `NATURAL = (10, 11, 12, 13, 29, 32)` (`raster_zones.py:57`) contains no class that mined pixels actually turn into.
- What stopped pixels actually become, in Tambopata BZ 2014–25 (ha):

| Class | Meaning | ha |
|---|---|---|
| 33 | water | 4,016 |
| 3 | forest | 1,920 |
| 23 | beach / sand bank (MapBiomas 4.3) | 2,064 |
| 21 | farm mosaic | 804 |
| 25 | other bare, anthropic | 773 |
| 51 | unidentified | 356 |
| 6 | flooded forest | 103 |
| 24 | urban | 50 |

- So `to_natural` = 0.0 in every row of `peru_stopped_split.csv`.
- "Other", which the docstring calls "farming/urban/bare", is about half sand banks: natural river-edge features and the classic confusion class for mining.
- **Fix:** take class codes from the MapBiomas Peru Col 4 legend file. Put 23 (beach), 22/25 and 51 in their own classes. Assert that every destination class is mapped.

**Major (data): the water class collapses after 2022 in every zone.**
- Water share of stopped land in 2012–22: 20–84% depending on zone. In 2023–25 it is 2–9% everywhere (La Pampa 0.08 / 0.08 / 0.04; Amarakaeri 0.02 / 0.07 / 0.03).
- The stopping rate is also unusually low in 2024 in every zone (La Pampa 0.7%, Amarakaeri 1.9%).
- This is a classification change at the end of the series, not behaviour (assumption A2 in method card 01).
- `*_later_stopped_share_to_water` therefore cannot be compared with earlier periods. Exclude 2023–25 from destination comparisons and say why.

### 4b. Can the data tell enforcement-driven abandonment apart from the alternatives?

| Alternative | What we can test | Result |
|---|---|---|
| Classifier flicker | Share of stopped land mined again within 2 years | Tambopata 28% before, 38% in 2019–21. It rose **more** in comparison zones: Amarakaeri 28% → 64%, corridor across the road 46% → 88%. The 2021–22 values pick up the 2023 MapBiomas re-mining spike, so the comparison is contaminated. Still, Tambopata's stopped land stayed out **more** often than elsewhere, which counts against flicker. |
| Depletion | Age of a pixel when it stops (years since first mined) | La Pampa 2019: median 4 years, 44% ≤ 2 years, 28% ≥ 6 years. 2018: 3 / 47% / 21%. 2017: 3 / 48% / 16%. The 2019 stopped pixels are not markedly older, so this is not the profile of exhausted old pits. Weak evidence against depletion. |
| Flooding or hydrology | Water share; whether the 2019 spike is regional | 78% of La Pampa's 2019 stopped land became water (58% in 2016–18). There is no 2019 stopping spike in Amarakaeri (7.7%), the corridor across the road (2.6%) or the rest of the corridor (7.9%). A regional flood or a classifier year should show up there too. |
| Normal pit lifecycle (2017–18 boom pits ending) | Stopping normalised by the previous two years' new land | 2019: 0.40; 2016–18: 0.12–0.26. Partly lifecycle, but still elevated. |
| Location | Longitude strips inside La Pampa | The 2019 stopped pixels sit in the central strips (−70.05 to −69.95: 6,607 + 3,352 px against 2,070 + 1,631 in 2018), where Mercurio operated. The western strip (−70.15 to −70.10) has no stopping spike (728 against 596), and its new land doubled (1,710 against 822 px). |

**Verdict on the team's narrative** ("stopping happened because enforcement was there; new pits still opened nearby"):
- Supported **for 2019 only.** The single largest stopping event of any zone-year in the region (1,494 ha in La Pampa) is specific to the target and its core strips, mostly flooded and mostly persistent.
- Not supported as a 2019–21 average. In 2020–21 the stopping rate is normal.
- New land did not fall in 2019 in the core strips either: 6,196 px against 6,498 in −70.05 to −70.00. This fits pits migrating within an active front, or pre-February clearing in an annual composite, as much as new pits opening "nearby".
- The genuinely displaced new land in 2019 is in the western strip and in the corridor across the road.

**What would falsify the narrative with the data already at hand (all cheap):**
1. **Placebo zones and years for the stopping rate.** Rank La Pampa 2019 (15.2%) among all zone-years whose stock exceeds 1,000 ha. It is 8th by rate; native communities often reach 13–21%. It is 1st in hectares.
2. **Distance test.** If 2019 stopped pixels are no closer to the operation's base or the IOH km 98–110 strip than 2016–18 stopped pixels, the enforcement attribution weakens.
3. **Persistence by strip.** If the core-strip 2019 stopped land is back by 2021–22 at the comparison-zone rate, it was a pause, not abandonment. The data say 31% of 2019 stopped land was back within 2 years, against 55–59% in Amarakaeri and the corridor.
4. **GLAD-S2 timing.** If mining alerts in the core strips continued through Mar–Sep 2019, the "stopped" is in the map rather than on the ground. Some of this exists in `glad_alerts.py` for the western box only.

Register 1–3 as numbers.

---

## Blindspot report

**Output audited:** `output/numbers.csv` at v3 (2,591 ids), the decomposition, the stopped splits, the cell panel, the RD and the ranks.

**Vice 1, the unexplained feature.** FLAG.
- Hardest to explain: the 2019 La Pampa stopping spike (15.2%, 78% to water). It is now the single biggest driver of the headline and is not separated from "2019–21".
- Also unexplained:
  - Water destination vanishes in 2023–25 in every zone.
  - 2024 stopping near zero everywhere.
  - Tambopata net additions are −111 in 2021.
  - Event-study pre-coefficients swing between −1,066 (2016) and +675 (2017), so the pre-noise band is ±1,000 ha against a 2019–21 effect of −1,360 to −1,910.
  - The 2012 one-year dip in La Pampa net additions (629 against 1,467 / 1,371). The team's notes say there is no dip; that rests on 2010–11 vs 2012–13 means, and 2010 is pre-boom.

**Vice 2, the convenient absence.**
- Missing: stopping-rate placebos; flicker-adjusted and rate-adjusted shares; destination splits restricted to years with a stable legend; a time-placebo distribution for the cell coefficients; a test that all docs ids resolve.
- No unexplained N changes. The scaled pool has 7 zones throughout.

**Virtue 1, the unasked question.**
- The longitude-strip pattern is a better displacement story than any of the six "causal attempts": the core stops, the western edge and the road's north side start, in the same year. It needs no comparison zone.
- Tambopata's stopped land returned **less** often than comparison zones'. That is a mechanism hint (pits kept closed) the team has not used.

**Virtue 2, the unexploited strength.**
- The 2019 stopping event is target-specific and absent in every comparison zone. As a "first-stage" footprint of enforcement on the map, it is more convincing than any p-value.
- Present it as such, with the rate-normalised series, instead of folding it into a 3-year mean.

**Ruling:** CONDITIONAL. Interpretation can proceed if the "about half" claim becomes a range, the destination split is fixed, and both pre-trend windows are reported.

---

## Ranked findings

| # | Severity | Where | Finding | Fix |
|---|---|---|---|---|
| 1 | **Major** | `docs/brief/brief_content.md:29,33` (working tree); `peru.py:124-128` | "About half of the fall is stopping" is the raw upper end. It is 25–33% net of flicker or of a constant stopping rate, ~10% for 2020–21, and two-thirds of the excess is in 2019. | Say "a quarter to a half, mostly 2019". Register flicker-adjusted and rate-adjusted shares and the 2019-only share. |
| 2 | **Major** | `raster_zones.py:57, 222-226` | `NATURAL` matches no real class, so `to_natural` ≡ 0. Sand banks (23), class 51 and bare land fall into "other (farming/urban/bare)". | Map from the legend. Assert full coverage. Split out beach/sand bank. |
| 3 | **Major** | `peru.py:62-81`; brief "half became water" | The water class collapses in 2023–25 in all zones, and the 2024 stopping rate is near zero everywhere: end-of-series classification. "Later" destination and return shares are not comparable. | Restrict destination comparisons to ≤ 2022. Label the "later" back-within-2y share as 2022–23. |
| 4 | **Major** | `definitions.py:57` (`PANEL_YEARS`), `v2_stats.py:155-180, 239-247` | The pre-trend verdict depends on the window: La Pampa passes with 2011–13 (p = 0.11) and fails with 2010–13 (p = 0.009). The corridor's net pre-trend fails (p = 0.041). Figure titles say "not rejected". | Report both windows equally. Remove pass/fail wording from the title. Correct the explainer's "corridor passes". |
| 5 | **Major** | `peru.py:226-229`, `peru_models.py:144-146`, brief line 33 | The size-relative rank is 3, 4 or 6 of 7 depending on reference and donor pool. The pool includes high-Andean zones that `AMAZON_BZ` excludes. | Cite the range, or justify one variant. Add the Amazon-only scaled rank (2 of 4). |
| 6 | **Major** | `docs/walkthrough/explainer_content.md`, `methods_content.md`, committed brief | 234 / 40 / 37 ids are missing from `numbers.csv`; the pages cannot be built at 3c7487d, and they carry stale v2 claims (cell −1.21 p = 0.08, RD p = 0.079, corridor pre-trend passes). | Add a pytest that every `{{id}}` resolves. Migrate the text. |
| 7 | **Major** | `v2_stats.py` (fig_zone headline), explainer | Cell-panel p-values (0.012, WCB 0.007) are a before/after change against zero-mining cells, with zone-wide common shocks ignored. | Keep them out of headlines. Add a placebo-window distribution. |
| 8 | Minor | `raster_zones.py:108-110` | Spherical pixel area is 0.065% low against the ellipsoid (20,716 against the publisher's 20,730). | Use a geodesic row area (pyproj `Geod`). It then matches the publisher to 0.1 ha. |
| 9 | Minor | `data_intermediate/bz_reconciliation.csv` (BP06) | Alto Mayo raster 30.6 ha against workbook 93.1 ha, and it is in the Amazon and B pools. | Investigate the polygon, or drop it with a note. |
| 10 | Minor | `tests/test_definitions.py:44-50` | The window regex misses `between`, `range`, `loc[a:b]` and lead windows. Slide modules fail 4 tests; the deck build breaks (no `sl_*` ids). | Broaden the test. Finish the slide migration, or mark those tests xfail explicitly. |
| 11 | Minor | git | v2 intermediates are still tracked, despite "removed". | `git rm` them, or fix the commit message. |
| 12 | Minor | `rd_road_*` | Under net the RD is +2.17, p = 0.25, fake rank 2 of 10. It is no longer suggestive. | Report it as uninformative. |
| 13 | Minor | AMW/twins numbers | `top3_ratio` 0.40 → 0.16, the PSM CEM gap ×3.5, the PS-NN matches have 0 controls, `bs_sar_gap` flips sign. | Add one line per number explaining the change (unit = whole BZ, new twin set). |

## Questions for the authors
1. Do you have any SERNANP or FZS dates for Mercurio actions inside the −70.05 to −69.95 strip in 2019? That strip carries most of the 2019 stopping.
2. Why was `PANEL_YEARS` moved from 2010 to 2011 in v3: before or after seeing the pre-trend tests?
3. Which MapBiomas Peru Col 4 legend file defines classes 23, 51 and 68?
